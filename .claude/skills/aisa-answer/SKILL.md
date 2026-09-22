---
name: aisa-answer
description: Record an answer or resolution for a Shared Understanding row (Unknown, Conflicted, Assumed or Risky) and apply the state transition from library/kernel/states.md. The answer is kept verbatim in answers.md; the resolved content re-enters the SU as new row(s) with `was <id>`; the original row is marked resolved. Also handles --revalidate <id> for expired Confirmed/Assumed rows — the fact still holds, so verificado_em is renewed on the row itself (sanctioned edit, no new row); if the check reveals the fact changed, it falls back to the normal `was <id>` transition. Works in any phase — used for Discovery answers and for prototype-validation feedback alike.
---

# aisa-answer

## Usage

`/answer <id> "<answer>" [--source "<who/what>"] [--to confirmed|assumed|risky]`
`/answer --revalidate <id> ["<confirmation note>"] [--source "<who/what>"]`

- `<id>`: the SU row being resolved — `U-NNN` (Unknown), `X-NNN` (Conflicted), `A-NNN` (Assumed, being validated), or `R-NNN` (Risky, being closed). With `--revalidate`: an expired (or ageing) `C-NNN`/`A-NNN` row whose fact still holds.
- `"<answer>"`: the answer/resolution, verbatim — do not paraphrase away specifics (numbers, names, thresholds).
- `--source`: who or what answered (default: "dono do processo"). Becomes part of the evidence.
- `--to`: force the target state. Default inference (`library/kernel/states.md` → *Confirmed threshold*): a declaration of the **process owner**, or of an authority the owner named in `enquadramento.md`, about a business fact within their authority → `Confirmed`; a document or transcript passage with its locator → `Confirmed`; a statement by anyone else, a fact about another team's system given by business, an inference the answer makes reasonable, or a resolution by internal evidence without an owner answer → `Assumed` with the basis; an answer that reveals a material uncertainty → `Risky`.

## State transitions applied (per `library/kernel/states.md`)

| From | Default to | Notes |
|---|---|---|
| Unknown | Confirmed (or Assumed/Risky via `--to` or inference) | 1 new row |
| Conflicted | Confirmed ×N | One new row **per resolved side** (e.g., "multi-level >10k€, 1-step <10k€" → 2 rows) — when the owner decides |
| Conflicted | Assumed | Resolved by internal evidence of the engagement, without an owner answer (`was X-nnn`, basis = the rows and locators used) — never `Confirmed` |
| Assumed | Confirmed | Validation of the assumption **with the locator of the validation** (owner declaration `answers.md#…` or new evidence) |
| Risky | Confirmed | Mitigation done or risk resolved — declared by the owner or evidenced |
| Risky | Assumed | Closed by reasoning over a chain of rows, without owner confirmation (`was R-nnn`) |
| Confirmed/Assumed (expirado) | same row, renewed | `--revalidate`: renews `verificado_em` — sanctioned edit, **no new row** |
| Confirmed/Assumed (expirado) | normal transition | `--revalidate` but the fact CHANGED → falls back to `was <id>` flow |

## Execution steps

1. Resolve the engagement root (`$AISA_ENGAGEMENTS_ROOT/<slug>` or `projects/<slug>`) and read `shared-understanding.md` + `_state.json` (current round).
2. Locate the row `<id>` in its section. If not found → stop and list the open ids of that prefix. If already marked `resolved → …` → stop and say so.
3. **Decide the fact, then let the motor write it.** The judgement is this skill's; the
   writing is not. Extract the fact the answer supports — see the *verbatim boundary* below
   — and hand it to the engine:

   ```
   python library/kernel/tools/resolve.py \
     --engagement <slug> --row <id> \
     --answer "<verbatim answer>" \
     --claim "<the extracted fact, specifics preserved>" \
     --by "role: <who> | fonte: <what>" \
     --locator "answers.md#<id>" \
     [--inference] [--to confirmed|assumed|risky] [--settles fact|fit] \
     --json
   ```

   Run it with `--dry-run --json` first when the transition is not obvious: it computes the
   target state, the new id and the structural verdict **without publishing**, so the
   decision can be read before it is taken.

   What the engine does, and this skill therefore no longer does by hand:
   `answers.md` section (created with its header when missing, anchored `answers.md#<id>`) ·
   next free id · the new row with `USER_ANSWER <date> — <who>, <locator> (was <id>)` ·
   the ` — resolved → <new-id>` marker on the original · the graph mirror · **one atomic
   publication through the coordinator, with a receipt in `_ops/receipts/`**.

   Never write these files directly. A hand-written transition skips the state rules, the
   mirror and the receipt, and the guard on `Write`/`Edit` refuses it over an engagement
   that is not reconstructed.

   **The target state is the engine's**, from `library/kernel/states.md`: a locator plus an
   answer from the declared authority → `Confirmed`; no locator, or an answer from someone
   else, or `--inference` → `Assumed` with the reason recorded. `--to` may only **lower**
   the state — forcing it upwards is refused as `SILENT_UPGRADE`, which is hard rule 3
   enforced instead of asked for.

   `--by` must carry the `role:` / `fonte:` prefix: it is matched against the row's declared
   authority, and an unprefixed name matches nothing.

4. **The claim the engine writes is the one this skill extracts** — and its boundary is the
   judgement that stays here. The `Confirmed` claim may not exceed what the answer or
   evidence actually supports: no interpretive clause the respondent did not say ("…so
   connectivity is not an obstacle"), no conclusion the answer only suggests. Runtime
   inference that the answer makes reasonable becomes a **separate** `Assumed` row with its
   basis declared, or — **only where the missing input is technical** — an `Unknown` /
   verification obligation (`custo: documento|spike`, `swing` stated). That obligation is an
   `Unknown` like any other and passes the same admission rule (`library/kernel/states.md` →
   *Admission of a question*, P-26): it cites the `M-n` it serves — or carries the marker
   `TO-BE DIVERGENCE` with what the target must decide — names ≥ 2 possible answers, **and**
   names which of the eight technical axes moves with each — `tecnologia` · `padrão
   arquitetural` · `componentes` · `modelo de dados` · `plano de imposição de permissões` ·
   `esforço de alto nível` · `custo` · `risco técnico`. A verification obligation that names
   no axis is `cosmético` with `criticidade: Low`; one that names no second answer is not
   opened at all. Unless independently supported by a cited source. A second-hand statement
   about another team's systems or configuration is `Assumed` with the basis, not
   `Confirmed`, and it **opens nothing**: no `Unknown` is written to chase an email, minutes,
   a written acceptance or a signature, because the gap already lives in the row's basis
   (`library/kernel/states.md` → *a third-party report closes; it does not open*). Nor does
   such a gap block a decision — only the seven technical axes do
   (`library/packs/<pack>/decision-tree.md` §6.1).

   For a **Conflicted** row the owner resolves into N sides: run the engine once per side,
   each with its own `--claim`. Resolution by internal evidence — the analyst adjudicating
   from rows already in the SU, with no owner answer — is `--inference`, which the engine
   turns into `Assumed was <id>`, and `answers.md` says so in **Fonte** (`evidência interna
   do engagement; sem resposta do dono`).

4b. **Architecture-significant technical claims — fact ≠ fit.** Applies when the resolved row is the `su_ref` of a `structural: true` `open_architecture_choices` entry in the latest `_blueprint/ux-blueprint_v<NN>.yaml`, **or** when the new claim would settle or materially support a structural architecture conclusion (experience mode/surface, record authority, access mechanism, composition pattern, security/control boundary, integration mechanism, hard feasibility). It does **not** apply merely because a row carries `validade: plataforma-tecnica` on an unrelated engagement fact.
   - **Settle the fact that was named.** Compare the verbatim answer with the choice's `would_be_settled_by`. If the choice requires *mechanism + requirement fit* and the answer establishes only *a connection / gateway / capability exists* → record the engagement fact (per step 4) and say explicitly: `structural choice <…> remains open — the answer settles connectivity, not the mechanism or its fit`. Never mark the choice resolved from here.
   - **Closure basis.** A structural architecture conclusion may close on ONE sufficient basis: **A** authoritative RESEARCH / Domain Knowledge (file + section) read against the engagement's material requirements, exclusions and limitations included; **B** engagement-verifiable technical evidence from an accountable source (a named mechanism, configuration or artefact IT can show — not a business sponsor's yes/no about connectivity); **C** a proof / measurement / spike result. None present → the proposition stays `Unknown` (verification obligation) or `Assumed` with basis, and the structural choice stays open. No automatic web lookup, no three-source rule, no Domain Knowledge preload.
   - **Capability ≠ fit.** A capability may be `Confirmed` (with basis A/B/C) while a documented limitation may still defeat a material requirement (audit, row security, query shape, identity) — then the capability row is Confirmed and the fit stays open, per requirement, per data domain. The output names both.
5. **Check the receipt, do not re-do the write.** The engine publishes atomically and
   returns `operation_id`; `_ops/receipts/<operation_id>.json` is the proof the transition
   happened as one operation. A run that produced no receipt did not transition — say so
   and stop rather than patching the files by hand. The original row keeps its
   ` — resolved → <new-id(s)>` marker and is never deleted: append-only, and this marker
   plus the revalidation renewal are the only two sanctioned edits to an existing row.
6. Update the SU header `Última actualização` and append one line to `council-log.md`:
   `<round> — /answer <id> → <new-id(s)> (<state>)`. These two are outside the engine's
   write set on purpose — the log is the skill's narration of what it did, not part of the
   transition, and folding it in would make a narration failure look like a failed
   transition.
7. **Targeted revalidation** (only when the new fact **contradicts or materially changes** a premise downstream reasoning used — an unrelated answer produces `(none)` and no broad list). Find the dependents through the references that already exist: grep the resolved id and the new fact's subject across `frame.md` (anchors, survival block), `options.md`, `decisions.md` (justification, conditions, tripwires), `_blueprint/ux-blueprint_v<NN>.yaml` (`su_refs`, `forced_by`, `would_be_settled_by`, rationale text naming the changed field), `_synthesis/*.md`. For each dependent write one line — `still valid — <why>` or `revalidate — <what the conclusion assumed>` — in the output and in `council-log.md`. No dependency graph, no registry, no rerun of all phases. Dependents in `decisions.md` (a justification clause, a condition, a cited option strength) → run the tripwire check (`aisa-status` step 7) and name `/revisit` as the next command; the Decision is never rewritten here. Architecture dependents → name them for `/blueprint --refresh`, which records them (step 11b).
7b. **What the new fact did to the coverage reviews — computed, never declared.** A recorded coverage review says *these sources, in this state, were read*. A new answer changes `answers.md` and the SU, so a review written before it may no longer describe the sources it claims to have read. Ask the motor; do not write a flag:

   ```
   python library/kernel/tools/coverage.py check --engagement <slug> --stage reconciliation --json
   ```
   and, where `_blueprint/` carries a version, the same for `--stage blueprint --target <engagement>/_blueprint/ux-blueprint_v<NN>.yaml`.

   - `freshness: current` → nothing to say; the answer did not move the base of the review.
   - `freshness: stale` → say which review and **what changed** (the motor names it), and that it must be redone before it is used again. `stale` never means the earlier conclusion became false — it means nobody has re-read the sources since they moved (`coverage-contract.md` §6.3).
   - `not_evaluated` (no record) → say nothing: an engagement with no review has nothing to invalidate.

   **No boolean is written anywhere.** There is no `coverage_stale` in `_state.json` and none is added (`coverage-contract.md` §10): the state is derived from the records and the sources on every read, so it cannot drift from them. Redoing the review is `/blueprint`'s work (steps 1b / 13b), not this skill's — and this skill never finalizes a record.

8. Output (business language — `CLAUDE.md` → *Duas línguas*; kernel labels and ids only between parentheses):
   ```user-output
   Resolvido: <a pergunta, em meia linha> (<id>) → agora <verificado (Confirmed) | assumido (Assumed) | duas fontes ainda se contradizem (Conflicted) | risco identificado (Risky)> (<novo id>).
   O que se dizia que mudava com a resposta: <a frase declarada> → <mudou mesmo? caiu uma alternativa · mudou uma estimativa · nada>.
   Escolha estrutural: <não se aplica | continua em aberto — <porquê>> — um facto novo não fecha por si uma escolha de arquitectura.
   A rever à luz deste facto: <nada | <conclusão> — assumia <o quê>> …
   Conferência do desenho: <não se aplica — ainda não há nenhuma | mantém-se válida | tem de ser refeita: mudou <o que mudou>> — ninguém reconferiu as fontes desde que mudaram; não quer dizer que a conclusão anterior esteja errada.
   Ainda em aberto e grave: <N> perguntas, <N> contradições entre fontes.
   A seguir: <passo humano, se houver> → `/status` · mais `/answer` · `/round` · `/blueprint --refresh` · `/revisit TW-n`.
   ```

## Revalidation mode (`--revalidate <id>`)

For expired (or ageing) Confirmed/Assumed rows — see `library/kernel/states.md` → *Epistemic half-lives*. The implicit question is: "Ainda é verdade que <claim>? Verificado pela última vez em <verificado_em>."

1. Locate the row (`C-NNN`/`A-NNN`). Not found → stop and list the expired ids (per `/status`). Already `resolved → …` → stop and say so.
2. Judge the confirmation note (ask for one if absent): does the fact still hold **unchanged**?
   - **Holds** → renew `verificado_em` = today on the row itself. No new row, no `resolved` marker — this renewal and the `resolved →` marker are the only two sanctioned edits to existing rows.
   - **Changed** (the note contradicts or amends the claim) → say so and apply the NORMAL flow instead (steps 3–6 above): new row(s) with `was <id>`, original marked resolved. Never renew a changed fact.
3. Record the revalidation in `answers.md`:
   ```markdown
   ## <id> — <date ISO> (revalidação)
   - **Claim**: <original claim>
   - **Confirmação**: mantém-se — <verbatim note>
   - **Fonte**: <source>
   - **verificado_em**: <old date> → <today>
   ```
4. Update the SU header `Última actualização`. Append to `council-log.md`: `<round> — /answer --revalidate <id> (verificado_em renovado)`.
5. Output:
   ```user-output
   Reconfirmado: <o facto, em meia linha> (<id>) — volta a valer a partir de hoje.
   A seguir: `/status` mostra a confiança actualizada; mais factos a reconfirmar → `/answer --revalidate <id>`.
   ```

## Hard rules

1. **Verbatim in, structured out.** answers.md keeps the raw answer; the SU row carries the extracted fact. Never lose numbers or thresholds in the extraction.
2. **Never delete or rewrite** the original row beyond the `resolved →` marker.
3. **No silent upgrades**: an answer that is hearsay or inference goes to Assumed with the basis declared, not Confirmed — even if the user typed it confidently. Say so when downgrading. Only the process owner (or an authority named in `enquadramento.md`) confirms; a technical fact about another team's system stated by business is `Assumed` until IT shows the mechanism (fact ≠ fit, rule 7). A row closed by internal evidence is `Assumed was <id>`, never `Confirmed`.
4. If the answer itself surfaces a NEW conflict or risk, additionally append the corresponding Conflicted/Risky row (new id, this round) and mention it in the output.
5. **Revalidation never touches the claim text.** If any word of the claim must change, it is a transition (`was <id>`), not a revalidation — no matter how small the change looks.
6. New rows created by this skill carry `verificado_em` = today and a `validade` class (states.md decay table; in doubt: `organizacional`).
7. **Fact ≠ fit.** A technical/configuration fact (gateway configured, connection exists, capability documented) never closes an architecture-fit conclusion by itself (step 4b). `Assumed → Confirmed` is validation of *the assumption's proposition*, not of a narrower question answered sideways.
8. **Coverage state is derived, never stored.** This skill computes the effect of the new fact on the recorded reviews (step 7b) and reports it; it writes no flag, finalizes no record and redoes no review. A review that has gone stale is redone by `/blueprint`, against the sources as they are now.
9. **Revalidation is written, not implied.** When a premise changes, the dependent conclusions are named (step 7) — `(none)` when the fact is unrelated. A dependent that silently remains settled is a defect.
