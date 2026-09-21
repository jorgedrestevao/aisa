# Shared Understanding — fixture excerpt (pricing-marinha shape)

> Fixture. Engagement ids ≤ C-069 / U-031 / R-012 exist in the real SU with these meanings; ids C-070+,
> A-010+, U-032+ are what the 1.8.2 disposition step would have ADOPTED. Claims abbreviated.

## Confirmed

| id | lens | claim | evidência | verificado_em | validade | ronda |
|---|---|---|---|---|---|---|
| C-001 | business | the daily minimum price is sent to the commercial team as the negotiation floor and then loaded into the sales system | `Fluxograma...docx ¶67-73, ¶80-90` | 2026-08-07 | organizacional | R-01 |
| C-008 | operations | Monday/Tuesday pricing without a real quote assumes the worse scenario; by Friday ~4 real quotes are known | `Processos Pricing...vtt [00:49:06–00:49:28]` | 2026-08-07 | organizacional | R-01 |
| C-009 | operations | the front-sheet output format is a fixed convention the commercial team expects to continue | `Processos Pricing...vtt [00:43:16–00:43:33]` | 2026-08-07 | organizacional | R-01 |
| C-013 | user | three populations: analysts build/maintain; committee decides; commercial team receives | `Kick-off.vtt`, `Fluxograma...docx` | 2026-08-07 | organizacional | R-01 |
| C-016 | data | logistics costs and cedência data are re-entered by hand from separate artefacts | `Fluxograma...docx ¶13-22, ¶53-59` | 2026-08-07 | organizacional | R-01 |
| C-022 | governance | segregation rule: whoever decides the margin should not load the price | `Fluxograma...docx ¶115-117` | 2026-08-07 | organizacional | R-01 |
| C-023 | governance | Spain's load is system-blocked below the minimum; Portugal's manual load is checked only by the checklist | `Fluxograma...docx ¶80-90, ¶57-62` | 2026-08-07 | organizacional | R-01 |
| C-026 | governance | a superior approves the margin before the load — independent approval before execution | `USER_ANSWER 2026-09-04 (was X-001)` | 2026-09-04 | organizacional | R-01 |
| C-028 | financial | no separate budget; the internal IT team builds | `USER_ANSWER 2026-09-04 (was U-016)` | 2026-09-04 | financeiro | R-01 |
| C-036 | data | sensitivity classification: Interno | `USER_ANSWER 2026-09-04 (was U-011)` | 2026-09-04 | organizacional | R-01 |
| C-039 | operations | the conservative rule is tribal knowledge, never written, never measured | `USER_ANSWER 2026-09-04 (was U-006)` | 2026-09-04 | organizacional | R-01 |
| C-041 | data | the calculation logic is duplicated across six output sheets that have diverged | `replay.md #1-95`; `PM-003/PM-U-009` | 2026-08-07 | organizacional | F-01 |
| C-046 | operations | the conservative rule applies uniformly to all counterparties | `USER_ANSWER 2026-09-04 (was U-020)` | 2026-09-04 | organizacional | F-01 |
| C-052 | governance | SAP is the truth for term-contract client terms | `USER_ANSWER 2026-09-04 (was X-002)` | 2026-09-04 | organizacional | O-01 |
| C-056 | user | the commercial team will not use the new application; only the pricing team | `USER_ANSWER 2026-09-04` | 2026-09-04 | organizacional | O-01 |
| C-057 | data | a shared relational database already operated for other pricing processes will hold all pricing data of this engagement | `USER_ANSWER 2026-09-04 (was U-029)` | 2026-09-04 | plataforma-tecnica | D-01 |
| C-059 | data | when the six output sheets diverge, `Outputs` is authoritative | `USER_ANSWER 2026-09-04 (was U-026)` | 2026-09-04 | organizacional | D-01 |
| C-060 | governance | design decision: 10-year retention floor for price history | `USER_ANSWER 2026-09-04 (was X-005)` | 2026-09-04 | legal-regulatorio | D-01 |
| C-070 | data | the process delivers the same prices in four units (EUR/MT, USD/MT, EUR/m³, USD/m³) for the system load — an output requirement, distinct from the six-copy duplication | `Inputs, cálculos e outputs...docx ¶151-157`; synopsis `four unit outputs` (OBSERVED) | 2026-08-07 | organizacional | R-02 |
| C-071 | business | a separate biofuel-blend output family (`Outputs BIOS`) exists: reference price, logistics, minimum até/após, per port | `Inputs, cálculos e outputs...docx ¶137-143`; `PM-008`; synopsis `Outputs BIOS` | 2026-08-07 | organizacional | R-02 |
| C-072 | operations | the daily price is computed as Cedência (Platts + prémio + SLI) → Base (+ logistics) → Venda (+ margin) → Mínimo (− discounts), split até/após the week change | `Inputs, cálculos e outputs...docx ¶61-100`; synopsis `chain: cedência → base → venda → mínimo` | 2026-08-07 | organizacional | R-02 |
| C-073 | operations | pricing must remain possible on Monday/Tuesday with incomplete quotes, applying the agreed conservative behaviour — a behaviour any solution must keep | `Processos Pricing...vtt [00:49:06–00:49:28]`; synopsis `Mon/Tue pricing must remain possible` | 2026-08-07 | organizacional | R-02 |
| C-074 | operations | the analyst projects Monday/Tuesday prices and plays the margin in an editable what-if copy of the output | `Kick-off.vtt [00:57:44–00:58:23], [01:07:51–01:08:28]`; synopsis `what-if projection` | 2026-08-07 | organizacional | R-02 |
| C-075 | operations | the analyst types ~85 values per daily row into the input register | `PM-001`; synopsis `daily wide entry` | 2026-08-07 | organizacional | R-02 |
| C-076 | governance | nothing may be loaded below the minimum price — enforced by system in Spain, by checklist in Portugal; a to-be behaviour to keep | `Fluxograma...docx ¶86-90`; synopsis `no load below minimum` | 2026-08-07 | organizacional | R-02 |
| C-077 | operations | the weekly reference price takes the higher of the two weekly prices with an uplift rule | `Kick-off.vtt [00:42:37–00:44:25]`; synopsis `reference price rule` | 2026-08-07 | organizacional | R-02 |

## Assumed

| id | lens | claim | base da assumption | verificado_em | validade | ronda |
|---|---|---|---|---|---|---|
| A-010 | data | the model-style base sheets are where the per-product chain is applied row by row; formalising them sizes the calculation layer | synopsis INFERRED — `PM-007`; docx ¶61, ¶111 | 2026-08-07 | organizacional | R-02 |

## Unknown

| id | lens | pergunta | quem responde | criticidade | custo | swing | ronda |
|---|---|---|---|---|---|---|---|
| U-028 | chair | can the owner of the reference application already in production absorb a second pricing line? | reference-app owner / IT | Critical | reuniao | decisivo: decides between reuse and build | O-01 |
| U-032 | operations | on Monday/Tuesday which input columns are typically still empty, and what does the process do today when a quote is missing? (PM-U-002) | pricing analyst | Critical | spike | decisivo: fill gaps vs replace the estimation method | R-02 |
| U-033 | business | who consumes `Outputs BIOS`, how often, and in what form? | requester / operations lead | Med | reuniao | dimensionante: scope of the blend output family | R-02 |
| U-034 | user | besides the analyst, who reads the Simulador, and does the what-if task have to survive in the to-be? | requester | Med | reuniao | dimensionante: shapes the estimation feature | R-02 |
| U-035 | data | is there an existing or mandated data platform where pricing data must live (the Spain process is operated somewhere)? | IT / requester | Critical | reuniao | decisivo: eliminates or reshapes whole solution classes | R-02 |
| U-036 | operations | are the two market benchmark series read by anything downstream? (PM-U-006) | pricing analyst | Med | spike | dimensionante: preserve, merge or drop a feed | R-02 |
| U-037 | operations | is there a documented or tribal method for estimating a missing quote? (PM-U-003) | pricing analyst | Critical | reuniao | decisivo: formalize vs design from zero | R-02 |
| U-038 | business | where is the indicative reference price published, and who consumes the publication? | requester | Med | email | dimensionante | R-02 |

## Conflicted

| id | lens | conflito | partes | criticidade | ronda |
|---|---|---|---|---|---|
| X-007 | data | the document says quotes arrive automatically and only costs/margins are manual; the workbook-only model labelled the 85 manual columns as counterparty quotes | `Inputs, cálculos e outputs...docx ¶2-4` ∧ `PM-001` | Med | R-02 |

## Risky

| id | lens | risco | impacto | mitigação proposta | ronda |
|---|---|---|---|---|---|
| R-005 | governance | the only formal control is self-reviewed by the file's builder | no independent verification behind the sign-off | name an independent second reviewer | R-01 |
| R-006 | data | master-data ownership has no formal process | months of delay from unresolved master data | name an owner and a change process before Options | R-01 |
