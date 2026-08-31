# Knowledge States — Kernel v0.1.0

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

Append rule: when a row transitions, the new row references the old id (`was U-007`). The old row stays for audit, and gains a ` — resolved → <new-id>` marker in its last column (the one sanctioned edit). Status counting treats marked rows as resolved, not open. The `/answer` skill applies these transitions; the verbatim answer is kept in `answers.md`.

## Schema of Shared Understanding rows

| Section | Columns |
|---|---|
| `## Confirmed` | `id \| lens \| claim \| evidência \| ronda` |
| `## Assumed` | `id \| lens \| claim \| base da assumption \| ronda` |
| `## Unknown` | `id \| lens \| pergunta \| quem responde \| criticidade (Low/Med/Critical) \| ronda` |
| `## Conflicted` | `id \| lens \| conflito \| partes \| criticidade \| ronda` |
| `## Risky` | `id \| lens \| risco \| impacto \| mitigação proposta \| ronda` |

Id prefixes: `C-` (Confirmed), `A-` (Assumed), `U-` (Unknown), `X-` (Conflicted), `R-` (Risky), `D-` (Decision; cross-ref to `decisions.md`).
