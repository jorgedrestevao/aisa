# Knowledge States — Kernel v0.2.0

Each row in the Shared Understanding (`shared-understanding.md`) is in **exactly one** state. Phases are defined in [`phases.md`](phases.md).

## The 5 states

| State | Meaning | Required evidence |
|---|---|---|
| **Confirmed** | Verified by direct evidence, or declared by the process owner within their authority | A **machine-resolvable locator** of one of the five classes (*Confirmed threshold* below) **and** a claim at the level of that evidence; human confirmation only from the process owner or an authority they named |
| **Assumed** | Reasonable inference, explicitly declared | The basis: the locators the inference rests on, an industry-standard claim, an industry pattern, a prior engagement, a statement by someone who is not the owner |
| **Unknown** | Identified gap requiring an answer | Who can answer — a **role** or a **source to consult**, never a person's identity — plus criticality, and the three declarations of *Admission of a question* below |
| **Conflicted** | Stakeholders or sources disagree | Parties involved + criticality |
| **Risky** | High uncertainty with material impact | Impact + proposed mitigation |

## Decision rules (when the state is ambiguous)

- **Confirmed vs Assumed**: `Confirmed` needs both a locator of the five classes **and** a claim that says no more than that evidence says (*Confirmed threshold*, rules 1–3). A formula supports "the artefact calculates"; a transcript supports "X said at [t]"; the owner supports a business fact within their authority. One level up — a business rule read out of a formula, a fact taken from a third party's statement, a technical fact about another team's system confirmed by business, a conclusion drawn from a chain of rows, a policy generalized from two snapshots — is `Assumed`, basis = the locators. "Based on typical engagements like this" and industry-standard claims are `Assumed`. Inference remains the analyst's job; what changes is the state it is recorded in, not the freedom to make it.
- **Unknown vs Risky**: Unknown is "we do not know X". Risky is "we know X is a problem, magnitude unknown". Latency unknown? If you have no signal → Unknown. If you know it is variable and peak may exceed thresholds → Risky.
- **Conflicted vs Unknown**: Conflicted requires ≥2 sources/stakeholders disagreeing. Unknown is "nobody has answered yet".

## Confirmed threshold

Five rules. They own what `Confirmed` means; lens files and `aisa-answer` point here and do not restate them.

1. **Locator resolvable by machine**, in one of six classes:
   - `<ficheiro>.xlsx|xlsm#<folha>!<célula|coluna>` — an explicit formula (`custo + margem = preço`) or prose text in the cell; counts and structure from the extractor cite `<ficheiro>.extraction.json#<folha>` or `<ficheiro>.replay.md#<n>`;
   - `<ficheiro>.vtt|srt#[hh:mm:ss]` (or the capture-lite form `<file> · [hh:mm:ss] <speaker>`) — an explicit passage of a transcript;
   - `<ficheiro>.docx|pdf|txt|md#¶n` (or `<file> · §<heading> ¶n` / `· ¶n` / `· p.n`) — an explicit passage of a document. A `.txt` numbers every non-empty line; a `.md` keeps its headings, so it carries the `§` form too;
   - `<ficheiro>.csv#linha n` (or `<file> · linha n`) — an explicit row of a table in text. The extractor keeps **every** row, never a sample, so the row it cites is evidence like any other;
   - `answers.md#<secção>` or `enquadramento.md#M-n` — a **dated declaration of the process owner**, recorded by the executor via `AskUserQuestion`. The `answers.md` anchor is the first segment of the section heading (before ` — `), spaces as hyphens: `answers.md#U-073`, `answers.md#BLOCO-H`;
   - `_capture/<ficheiro>.<extracção>.json#<chave>` or `.md#<secção>` — a **direct extraction over the raw source, persisted**. When the capture pass did not cover what the claim needs — VBA text the extraction never decompiles, an aggregation the per-column statistics cannot answer, a sheet the model only summarizes — the lens may go to the raw source (`orchestration.md` → *Raw inspection*) **and what it takes from there is written to `_capture/`** under its own name, with the method and the source's SHA-256 in the artefact's header. The locator points at that file, never at the method. A method declared in prose and a result nobody can reopen is not a locator: without the artefact the class does not apply.
   Without a locator in one of these classes, the row is not `Confirmed`. The target must exist (`inputs/`, `_capture/`, `answers.md`, `enquadramento.md`); `context.json.literal_request` is the one accepted exception — the owner's own words at intake.
2. **Claim at the level of the evidence.** Formula → "the artefact calculates / contains"; transcript or document → "X said at [t] / the document says"; owner → a business fact **within their authority**; a persisted direct extraction → what that extraction *measured*, at its own precision, not the sufficiency conclusion drawn from it. Anything one level up is `Assumed` with the locators as basis (examples in the decision rule above). **Um replay falhado nunca impede a leitura**: uma fórmula que o motor não recomputa (`INDIRECT` dinâmico, `INDEX/MATCH` fora do alcance do replay) continua a suportar «o artefacto calcula», com o locator da célula — o replay verifica valores, a leitura verifica a fórmula, e são operações distintas sobre a mesma célula. O que o replay não computou fica `TO-READ` na captura (§7 do process-model), nunca `Unknown` por defeito.
3. **Human confirmation only from the process owner**, or from whoever the owner named as authority on the topic (recorded in `enquadramento.md`). A statement by anyone else — another team, IT, a sales rep — enters as an attributed declaration (transcript, document) or as `Assumed` with basis. The executor may confirm facts of the **engagement** itself — authorized scope, registration decisions — marked `[ÂMBITO AUTORIZADO]` in the claim, evidence = the decision record. Resolving an `X-` or `R-` row "by internal evidence, without an owner answer" produces `Assumed was X-nnn` / `Assumed was R-nnn`, never `Confirmed`.
4. **Industry-standard claims** are a legitimate basis of `Assumed`, never evidence of `Confirmed`.
5. **`Assumed → Confirmed`** ("validation done") requires the locator of the validation — an owner declaration (`answers.md#…`) or new evidence of the classes in rule 1 — written into the evidence of the new row.

Two halves enforce this: the deterministic half (a hook that checks the presence of a locator and the existence of its target on every new `C-` row, and a `sem locator` facet in `/status`) warns and never blocks — it verifies that an anchor is there and that it opens, never that the claim is true, and an empty warning list means "every locator points at something that exists", never "the facts are right"; the judgement half lives in the lenses' Hard rules and in the round arbiter (`aisa-round` step 5f), whose finding is **never a metadata edit** — a `Confirmed` that says more than its evidence becomes `A-nnn was C-nnn`, append-only, original marked resolved.

## Transitions

| From | To | Trigger |
|---|---|---|
| Unknown | Confirmed | Owner declaration (`answers.md#<secção>`), document or transcript locator found, or a persisted direct extraction (`_capture/…`) — claim at the evidence level (*Confirmed threshold*) |
| Unknown | Assumed | Reasonable inference accepted (must declare); an answer from someone other than the owner or a named authority; a fact about another team's system given by business |
| Unknown | Risky | Discovery reveals it is a risk dimension |
| Conflicted | Confirmed (×N) | The owner decides between the sides (creates N Confirmed rows, `answers.md#…`) |
| Conflicted | Assumed | Resolved by internal evidence, without an owner answer (`was X-nnn`, basis = the rows and locators used) |
| Conflicted | Risky | No resolution; tracked as risk |
| Assumed | Confirmed | Validation done **with a locator** of the classes in rule 1 (owner declaration or new evidence) |
| Risky | Confirmed | Mitigation implemented, or risk realized & resolved — declared by the owner or evidenced |
| Risky | Assumed | Closed by the executor's reasoning over a chain of rows, without owner confirmation (`was R-nnn`) |
| Confirmed | Assumed | Re-reading against the evidence: the claim says **more** than the evidence supports, or the evidence is **no longer resolvable** in the engagement → `A-nnn was C-nnn`, basis = the locators that remain |
| Confirmed | Confirmed | **Correction by evidence**: the evidence **contradicts the claim and settles the right value** → `C-nnn was C-nnn`, the new row carrying the corrected claim and the locator that fixes it. The state does not drop: the fact is still evidenced, better than before. Requires that locator — correction comes from better evidence, never from a better argument. Reading the corrected value off a persisted extraction is **citation, not human confirmation**: rule 3 stays intact |
| Confirmed (expirado) | Confirmed | **Revalidação**: the fact still holds → renew `verificado_em` on the row itself (sanctioned edit; no new row) |
| Confirmed (expirado) | Unknown | The fact may have changed → re-question; the answer then follows the normal transition (`was <id>`) |

Append rule: when a row transitions, the new row references the old id (`was U-007`). The old row stays for audit, and gains a ` — resolved → <new-id>` marker in its last column. Sanctioned edits to existing rows are exactly six: the `resolved →` marker on transition; **withdrawing a question for scope** (below); renewing `verificado_em` on revalidation (see *Epistemic half-lives*); **normalising terminology** (below); **completing the evidence locator** of a row whose evidence already names the source but not the anchor (`answers.md#<secção>`, `<ficheiro>.extraction.json#<folha>`) — the claim is not touched, and the batch is logged in `council-log.md`; and **the `criticidade` that follows a `swing` the arbiter has just lowered to `cosmético`** (*Admission of a question* below, where its bounds live). Reclassifying a `Confirmed` that says more than its evidence is **not** an edit: it is a transition (`A-nnn was C-nnn`). Nor is **correcting a claim the evidence contradicts**: that is a transition too (`C-nnn was C-nnn`, *Correction by evidence* above), never a sanctioned edit of its own. One question separates the two: **does the evidence settle the corrected value?** Yes → the new row stays `Confirmed`; no → `Assumed` with the locators as basis, or `Unknown` when there is not even a basis. No motor finds this case — the deterministic half checks presence and existence, never truth — so a contradiction is always a reading: the round arbiter's (`aisa-round` step 5f) or a person's. The `swing` class token of an `Unknown` may be corrected by `/simulate` or by the round arbiter (*Question economics*); and a row the arbiter has just lowered to `cosmético` has its `criticidade` lowered with it in the same pass — **the sixth sanctioned edit**, defined in *Admission of a question* below, where the rule that bounds it lives. Status counting treats marked rows as resolved, not open.

**Terminology normalisation** (P-20, the fifth sanctioned edit). Restoring a product, vendor, service or technical-artefact **literal** in a row that paraphrased it (`Dataverse` written as “loja governada”, `Azure SQL` as “a base relacional”) is an edit, not a transition: the claim asserts the same thing about the same product, and the paraphrase was a defect of expression that `glossary.md` → *Two languages* rule 5 now forbids. Nothing else in the row is touched — not the state, not `verificado_em`, not the evidence — and the batch is logged in `council-log.md`, one line, naming the literal restored and how many rows carried it. If the wording change would alter **what** is claimed, it is not a normalisation: it is a transition, or a correction by evidence.

**Withdrawal for scope** (P-21, the fourth sanctioned edit). A question that the process does not ask — by the role rule (*Question economics*), by failing *Admission of a question*, or because it sits outside the technical axes that decide anything (`library/packs/<pack>/decision-tree.md` §6.1) — leaves by a marker in its last column and by nothing else:

    — retirada P-21 (<razão curta>)

The row **stays** — it is audit, and a question someone once thought material is part of the record. It stops counting as open, it never appears in the meeting agenda or the value-of-information list, and it is **not** a closure: nothing was answered, so it counts in no round's balance and never as `fechada`. Withdrawal is available for `Unknown` and `Conflicted` rows only: a `Confirmed`, `Assumed` or `Risky` row states something about the world and leaves by transition or not at all. Where a withdrawn question has a **technical half worth keeping**, that half is written as a new row in the same pass, referencing the old id (`was U-nnn`) — withdrawal and transition are then both recorded, and the reason names which is which. The batch is logged in `council-log.md`, one line per row. Only the owner's ruling withdraws a question: no lens, no council persona and no motor may write this marker.
 The `/answer` skill applies these transitions; the verbatim answer is kept in `answers.md`.

## Schema of Shared Understanding rows

| Section | Columns |
|---|---|
| `## Confirmed` | `id \| lens \| claim \| evidência \| verificado_em \| validade \| ronda` |
| `## Assumed` | `id \| lens \| claim \| base da assumption \| verificado_em \| validade \| ronda` |
| `## Unknown` | `id \| lens \| pergunta \| quem responde \| criticidade (Low/Med/Critical) \| custo \| swing \| ronda` |
| `## Conflicted` | `id \| lens \| conflito \| partes \| criticidade \| ronda` |
| `## Risky` | `id \| lens \| risco \| impacto \| mitigação proposta \| ronda` |

### The form of `quem responde` (P-21 / F1.1)

Every part of that cell — and of `partes` on a `Conflicted` row — carries one of exactly **two** prefixes:

    role: <the role that owes the answer>          `role: dono dos dados` · `role: Operações`
    fonte: <the artefact or system to consult>     `fonte: contrato SAP` · `fonte: registo de acessos`

Two spellings, no synonyms and no English variant. A cell may carry several parts (`/`, `+`, `,`, `;`,
` e `), and **each part carries its own prefix** — a prefix does not reach across a separator.

A person's name is never a value here: the answer is owed by whoever holds the role, and no name is a
precondition for the next step. Where neither a role nor a source is known, the cell is left **empty** and
reads `por atribuir` — an empty cell is honest, an invented role is not. A council persona is not a value
either: it is a lens, not somebody who can be asked.

A part **without** a prefix is not interpreted. The motor keeps it verbatim and infers no role and no
source from it (`library/kernel/tools/dashboard.py` → `split_owner`): deciding whether free text names a
role or a person is judgement, and the motor does not judge. That is also what makes every row written
before this form read exactly as it did.

Id prefixes: `C-` (Confirmed), `A-` (Assumed), `U-` (Unknown), `X-` (Conflicted), `R-` (Risky), `D-` (Decision; cross-ref to `decisions.md`).

`lens` values: the six Discovery lenses (`business`, `operations`, `user`, `data`, `governance`, `financial`), `technology` (Options onward), `chair` (council synthesis rows) and `enquadramento` — the process owner's declared business mechanism, written by `/start` **before the first round** as `Confirmed` rows in ronda `R-00`, one per invariant `M-n`, evidence `declaração do dono do processo, <date> — enquadramento.md#M-n`, `validade = organizacional`. `R-00` is a legitimate `ronda` value: it means "declared by the owner, no lens has run". These rows are the owner's **hypothesis**: `/frame` confirms or corrects each one with evidence through the normal transition (`was C-nnn`); the R-00 row is never edited. Every `Unknown` — whoever writes it, in whatever phase — carries the three declarations of *Admission of a question* (*Question economics*): the `M-n` its answer serves, the answers it admits, and the technical axis each answer moves.

## Epistemic half-lives

Confirmed and Assumed rows carry two columns beyond the claim: `verificado_em` (ISO date, e.g. `2026-08-31` — when the fact was last verified) and `validade` (one of the 6 decay classes below, short name). Knowledge expires: the schema governs a claim's *filiation* (when it was verified, how fast it decays), never what the claim may say.

### Decay classes and default half-lives

| Classe (`validade`) | Meia-vida default | Exemplos |
|---|---|---|
| `legal-regulatorio` | 24 meses | retenção legal, obrigações de auditoria |
| `plataforma-tecnica` | 12 meses | limites de produto, capacidades de plataforma |
| `organizacional` | 6 meses (**DEFAULT** — na dúvida, usa esta) | processos, políticas internas, org |
| `financeiro` | 6 meses | envelopes, taxas, chargeback |
| `pessoas-disponibilidade` | 3 meses | quem aprova, aceites individuais, disponibilidades |
| `volatil` | 1 mês | estados operacionais correntes (backlogs, pendências) |

TODO(team): defaults em uso desde a v2.2 — validar as meias-vidas na retro do pilot. Packs podem sobrepor classes via `epistemics.half_lives_override` no seu `pack.yaml`; na ausência de override, valem os defaults acima.

### Expiration rule (normative)

Uma row está expirada quando `verificado_em + meia-vida(validade) < hoje`. Expirada ≠ falsa: significa que a confiança caducou. Efeitos: (1) /status conta-a em "a revalidar" e a saúde epistémica desce; (2) lenses e personas tratam-na como Assumed fraca; (3) a re-pergunta sugerida é gerada a partir do claim ("Ainda é verdade que <claim>? Verificado pela última vez em <data>"). A revalidação renova `verificado_em` sem nova row; a mudança de facto segue a transição normal com `was <id>`.

## Question economics

Every Unknown carries a price and a return, so discovery INVESTS in questions instead of listing them:

- **`custo`** — what it takes to get the answer: `email` (async, minutes of a stakeholder), `documento` (obtain/read an existing document), `reuniao` (30-60 synchronous minutes of sponsor/stakeholder), `spike` (days of technical work).
- **`swing`** — `classe: frase`, where classe ∈ `decisivo` (the answer changes WHICH option/branch/frame survives), `dimensionante` (changes sizing, effort, cost or design — not the choice itself), `cosmético` (changes nothing material). The frase states WHAT changes (e.g. `decisivo: elimina O-004 ou muda o branch`).

`cosmético` is legitimate and useful — it is what lets `/status` say "do not spend meeting time on this". `/status` renders the **meeting agenda** from these columns; `/simulate`'s value-of-information section consumes the classes and corrects them when the evidence disagrees (a sanctioned metadata edit, noted in its output).

**Admission of a question** (P-26). An `Unknown` is written only when the row itself carries **three** declarations. They are a **conjunction, not a menu**:

1. **what the answer serves**, in one of two admissible forms: the `M-n` of `enquadramento.md`, **or** the divergence it opens in the **to-be**, written with the marker `TO-BE DIVERGENCE` followed by what the target must decide. The second form is available **with or without** a declared `enquadramento` (owner's ruling, 2026-09-10): a narrow framing must not price a legitimate technical question at zero. It is a declaration, not a bypass — the marker without a stated divergence is an empty cell, and declarations 2 and 3 remain owed in full;
2. **≥ 2 possible answers**, named in the `swing` phrase;
3. **which technical axis moves** with each of those answers, from these eight: `tecnologia` · `padrão arquitetural` · `componentes` · `modelo de dados` · `plano de imposição de permissões` · `esforço de alto nível` · `custo` · `risco técnico`.

Citing an `M-n` is **necessary context and never sufficient**: it names the mechanism the answer serves, never what changes in the system to be built. The waiver that let an `M-n` stand in for declaration 3 is gone. A difference only in the **as-is** is not a difference; a divergence inferable with a declared basis is written `Assumed`, not asked.

**The organisation's ignorance is not the project's work.** What the lens owes is the **technical fact** it established. That the organisation has no written policy, no inventory, no demonstrated maturity and nobody who knows who does what describes the organisation, not the target. It becomes a row only through the three declarations above — and where the target must define what the organisation never defined, that is a **requirement** of the to-be (`Assumed` with its basis, or a `decisão` for the owner), never a question waiting on the organisation. The verification is the same either way: which of the eight axes moves.

| Missing | Outcome |
|---|---|
| declaration 3 | the row is `cosmético` |
| declaration 2 | the row **is not written** |
| a named referent, on a `decisivo` | the class is `dimensionante` |

**Whom it binds.** Every writer of an `Unknown`, in every phase: the six Discovery lenses (`R-` rounds), `chairman-synthesis` (`F-` and `O-` rounds), the technical verification obligation `aisa-answer` opens, and the `PM-U` rows `aisa-capture` prices. No writer and no phase sits outside it.

**The arbiter's two effects** (`aisa-round` step 5f). It verifies the three declarations are **present** — never whether they are true, never whether the question is material (its one materiality class is the role rule below). On a row missing one, in this order:

1. lower the `swing` class token and append ` — reclassificado P-26 (<ronda>): <declaration missing>` — a sanctioned metadata edit of the same class as `/simulate`'s correction;
2. **only if 1 fired**, and only from above `Low`: set `criticidade` to `Low` and append ` — criticidade baixada P-26 (<ronda>): <the reason that sustained it>` — the sixth sanctioned edit, so a question that changes nothing stops pressing the Discovery gate.

Both go on one `council-log.md` line. The descent is a **consequence** of step 1, never a judgement of its own: no arbiter, no motor and no persona lowers a `criticidade` for any other reason, a row already `cosmético` before this pass is left alone, and it moves **never upwards**. The arbiter never deletes a row and never rewrites a question.

**Three destinations for an uncertainty.** Not everything uncertain is a question:

| Destination | When | Where it lands |
|---|---|---|
| **Design assumption** | the uncertainty changes detail, configuration or a band | `Assumed` with basis, impact and revision condition |
| **Decisive question** | the answer changes the option or the pattern | `Unknown` with the three declarations above |
| **Later detail** | it only settles at implementation | no open row at all |

**The role rule** (P-21). An `Unknown` never asks for a person's identity, a signature, an approval, or a document proving a third party's position. Where authority matters the question asks for the **role**, the operation it must perform, and the plane that enforces it. A question whose only possible answer is a name or a piece of paper fails admission by construction — it moves none of the eight axes, so it changes no requirement, no data shape and no effort — and is therefore not written. The round arbiter enforces this one class of materiality (`aisa-round` step 5f).

**A third-party report closes; it does not open** (P-23). A statement about a third party's position, relayed by someone who does not hold it, resolves the row as `Assumed` with the relay declared in the basis — and **opens nothing**. The missing artefact does not become a new `Unknown`: the gap already lives in that row's basis, where every downstream reader meets it. Chasing the email, the minutes or the written acceptance is an engagement courtesy, never a decision input, and it never blocks a decision (`library/packs/<pack>/decision-tree.md` §6.1 for what does).

**Cost questions.** The as-is cost, the cost of doing nothing and the cost of delay are the financial lens's **baseline**, written as `Assumed` with the basis declared (volume × cycle time × rate, every input visible) — not asked as `Unknown`. A cost `Unknown` is `decisivo` only when it names the branch its magnitude would eliminate or keep alive (typically `do nothing`), `dimensionante` when it changes the effort or data shape of the to-be, and otherwise `cosmético` — including when the decision to build is already taken.

Compatibility: absent columns (pre-v2.3 SUs) ⇒ `custo = email`, `swing = dimensionante` — applied on read, never migrated.

### Compatibility (SUs created before v2.2)

Coluna ausente ⇒ tratar como `verificado_em = data da ronda` e `validade = organizacional`. A regra aplica-se **na leitura** — nunca migrar SUs antigos à força.
