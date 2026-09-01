# Knowledge States — Kernel v0.2.0

Each row in the Shared Understanding (`shared-understanding.md`) is in **exactly one** state. Phases are defined in [`phases.md`](phases.md).

## The 5 states

| State | Meaning | Required evidence |
|---|---|---|
| **Confirmed** | Verified by direct evidence or sponsor | Document citation, USER_ANSWER, industry-standard claim |
| **Assumed** | Reasonable inference, explicitly declared | Source of the assumption (industry pattern, prior engagement, etc.) |
| **Unknown** | Identified gap requiring an answer | Who can answer + criticality |
| **Conflicted** | Stakeholders or sources disagree | Parties involved + criticality |
| **Risky** | High uncertainty with material impact | Impact + proposed mitigation |

## Decision rules (when the state is ambiguous)

- **Confirmed vs Assumed**: if evidence is direct (a document, a sponsor answer, a piece of data) → Confirmed. If it is "based on typical engagements like this" → Assumed.
- **Unknown vs Risky**: Unknown is "we do not know X". Risky is "we know X is a problem, magnitude unknown". Latency unknown? If you have no signal → Unknown. If you know it is variable and peak may exceed thresholds → Risky.
- **Conflicted vs Unknown**: Conflicted requires ≥2 sources/stakeholders disagreeing. Unknown is "nobody has answered yet".

## Transitions

| From | To | Trigger |
|---|---|---|
| Unknown | Confirmed | USER_ANSWER, document found, sponsor decision |
| Unknown | Assumed | Reasonable inference accepted (must declare) |
| Unknown | Risky | Discovery reveals it is a risk dimension |
| Conflicted | Confirmed (×N) | Sponsor decides between options (creates N Confirmed rows) |
| Conflicted | Risky | No resolution; tracked as risk |
| Assumed | Confirmed | Validation done |
| Risky | Confirmed | Mitigation implemented or risk realized & resolved |
| Confirmed (expirado) | Confirmed | **Revalidação**: the fact still holds → renew `verificado_em` on the row itself (sanctioned edit; no new row) |
| Confirmed (expirado) | Unknown | The fact may have changed → re-question; the answer then follows the normal transition (`was <id>`) |

Append rule: when a row transitions, the new row references the old id (`was U-007`). The old row stays for audit, and gains a ` — resolved → <new-id>` marker in its last column. Sanctioned edits to existing rows are exactly two: the `resolved →` marker on transition, and renewing `verificado_em` on revalidation (see *Epistemic half-lives*). Status counting treats marked rows as resolved, not open. The `/answer` skill applies these transitions; the verbatim answer is kept in `answers.md`.

## Schema of Shared Understanding rows

| Section | Columns |
|---|---|
| `## Confirmed` | `id \| lens \| claim \| evidência \| verificado_em \| validade \| ronda` |
| `## Assumed` | `id \| lens \| claim \| base da assumption \| verificado_em \| validade \| ronda` |
| `## Unknown` | `id \| lens \| pergunta \| quem responde \| criticidade (Low/Med/Critical) \| custo \| swing \| ronda` |
| `## Conflicted` | `id \| lens \| conflito \| partes \| criticidade \| ronda` |
| `## Risky` | `id \| lens \| risco \| impacto \| mitigação proposta \| ronda` |

Id prefixes: `C-` (Confirmed), `A-` (Assumed), `U-` (Unknown), `X-` (Conflicted), `R-` (Risky), `D-` (Decision; cross-ref to `decisions.md`).

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

Compatibility: absent columns (pre-v2.3 SUs) ⇒ `custo = email`, `swing = dimensionante` — applied on read, never migrated.

### Compatibility (SUs created before v2.2)

Coluna ausente ⇒ tratar como `verificado_em = data da ronda` e `validade = organizacional`. A regra aplica-se **na leitura** — nunca migrar SUs antigos à força.
