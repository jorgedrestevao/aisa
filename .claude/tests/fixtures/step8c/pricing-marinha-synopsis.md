## 4. Process synopsis (cross-source)

> Fixture — static re-capture of the Pilot-1 evidence in the 1.8.2 synopsis shape. Sources: `PM-NNN`
> (workbook), `Inputs, cálculos e outputs...docx` (¶), `Fluxograma...docx` (¶), `Kick-off.vtt` /
> `Processos Pricing...vtt` ([HH:MM:SS]). Dispositions: workbook USED · both docx USED · Kick-off.vtt
> TARGETED ([00:40:22–00:44:25], [00:57:44–00:58:23], [01:07:51–01:08:28]) · Processos Pricing.vtt
> TARGETED ([00:02:57–00:03:05], [00:41:35–00:49:28]).

### Purpose
- OBSERVED — the process produces, daily, the minimum bunker price per port × product that the commercial team uses as the negotiation floor and that is then loaded into the sales system — `Fluxograma...docx · ¶67-73, ¶80-84`; `Inputs, cálculos e outputs...docx · ¶121-127`.

### End-to-end flow
- OBSERVED — daily cycle: market quotes and FX arrive automatically; logistics costs and target margins are typed by the pricing analysts; the master workbook computes; a daily internal committee decides margin, projections and exceptions; the analyst reviews against a checklist, archives, sends the front sheet to the commercial team and loads the prices — `Fluxograma...docx · ¶3-66, ¶107-113`; `PM-001`, `PM-006`.
- OBSERVED — Monday is the heaviest day: several inputs from several sources are entered by hand before the automatic feed has caught up — `Processos Pricing...vtt · [00:02:57–00:03:05] Pedro`, `[00:41:35–00:41:44] Pedro`.

### Actors
- OBSERVED — pricing analysts (build, maintain, repair the workbook; type logistics costs and margins); the daily committee (decides, does not edit); the commercial team ("Campos", receives the output); Supply (sends cedência data by e-mail); another team operating the parallel Spain process — `Fluxograma...docx · ¶17, ¶84, ¶109`; `PM-001`; `Kick-off.vtt · [00:10:54–00:11:59] Pedro`.

### Inputs
- OBSERVED — automatic: Platts benchmark quotes and the USD/EUR rate (market feed) — `Inputs, cálculos e outputs...docx · ¶3-22`; `PM-010`.
- OBSERVED — manual: logistics costs per port and delivery mode (monthly, irregular), target margins (per product / client type), Supply cedência values (by e-mail) — `Inputs, cálculos e outputs...docx · ¶23-39, ¶53-59`; `Fluxograma...docx · ¶16-29`; `PM-001`.
- OBSERVED — densities per product block for unit conversion — `Inputs, cálculos e outputs...docx · ¶47-52`.
- OBSERVED (docx) vs INFERRED (workbook) — the document says only logistics costs and margins are manual and quotes arrive automatically; the workbook's 85 manual columns were labelled "counterparty quotes" by the workbook-only model. The two accounts are not reconciled here — `Inputs, cálculos e outputs...docx · ¶2-4`; `PM-001`.

### Transformation / calculation stages
- OBSERVED — `chain: cedência → base → venda → mínimo`: Preço Cedência = Platts + Prémio + SLI (per product, USD→EUR via FX) → Preço Base = Cedência + Custos Logísticos (port, product, delivery mode) → Preço de Venda = Base + Margem Alvo (client type, product, date) → Preço Mínimo = Venda − Descontos, split into "até" / "após" around the week-change date — `Inputs, cálculos e outputs...docx · ¶61-78, ¶91-100`.
- OBSERVED — `unit conversions`: USD/MT → EUR/MT (FX); EUR/MT → EUR/m³ (density); USD/MT → USD/m³ — feed the final prices sent to the commercial team and the system load — `Inputs, cálculos e outputs...docx · ¶79-90, ¶151-157`; `PM-003`.
- OBSERVED — `blend calculation`: Preço Blend = %Diesel × Preço Diesel + %FAME × Preço FAME + %HVO × Preço HVO + adjustments (density, premium), for DFA/RF/HVO blend levels — `Inputs, cálculos e outputs...docx · ¶101-111`; `PM-008`.
- OBSERVED — `reference price rule`: the weekly reference price takes the higher of the two weekly prices, with an uplift rule applied on top — `Kick-off.vtt · [00:42:37–00:44:25] Pedro`; `Inputs, cálculos e outputs...docx · ¶91-100`.
- INFERRED — the model-style `Base DFA` / `Base RF` sheets are where the per-product chain above is applied row by row; their formalisation sizes the calculation layer of any replacement — `PM-007`; `Inputs, cálculos e outputs...docx · ¶61, ¶111`.

### Intermediate state
- OBSERVED — `Preço Cedência` and `Preço Base` exist as intermediate computed values before margin and discounts — `Inputs, cálculos e outputs...docx · ¶62-72`.

### Decisions
- OBSERVED — the daily committee decides the daily margin, the projections and exceptional adjustments — `Fluxograma...docx · ¶107-113`.
- OBSERVED — `conservative rule`: on Monday/Tuesday, with no real quote known, the team always assumes the worse scenario (price rises) regardless of the market trend; by Friday about four real quotes are known — `Processos Pricing...vtt · [00:49:06–00:49:28] Pedro`.

### Outputs and consumers
- OBSERVED — `Outputs`: the daily minimum price per port × product (firm, minimum, spot, next-week), sent as the "folha de rosto" to the commercial team and used as the negotiation floor — `Inputs, cálculos e outputs...docx · ¶121-136, ¶144-150`; `Fluxograma...docx · ¶67-73`; `PM-002`.
- OBSERVED — `four unit outputs`: the same prices in EUR/MT, USD/MT, EUR/m³ and USD/m³, consumed by the manual/batch load into the sales system — `Inputs, cálculos e outputs...docx · ¶151-157`; `Fluxograma...docx · ¶52-55`; `PM-003`.
- OBSERVED — `Outputs BIOS`: the biofuel-blend price family (reference price, logistics, minimum até/após, per port) for HVO/DFA/RF blends — a separate output family layered on the base output — `Inputs, cálculos e outputs...docx · ¶137-143`; `PM-008`. UNKNOWN — its consumer and cadence are not stated in any source.
- OBSERVED — `Simulador`: an editable copy of the output used by the analyst to project Monday/Tuesday prices and to play the margin ("fazer uma projeção, uma estimativa… jogar em paralelo com a margem") — `Kick-off.vtt · [00:57:44–00:58:23] Pedro`, `[01:07:51–01:08:28] Pedro`; `PM-003`. HYPOTHESIS — the Simulador is the analyst's what-if task, not a report; who else reads it is not stated.
- OBSERVED — `publications`: an indicative reference price is published for named ports and quoted to clients — `Kick-off.vtt · [00:42:56–00:43:08] Pedro`. UNKNOWN — the publication channel and its consumer are not recorded.
- OBSERVED — `Checklist sign-off`: one dated, named review record of the pricing assumptions — the process's audit evidence — `PM-006`; `Fluxograma...docx · ¶57-62`.

### Variants
- OBSERVED — per port (Aveiro, Leixões, Viana, Lisboa, Setúbal, Sines, Olhão, Portimão, Nazaré, Peniche…), per product (DFA, RF, HVO and blends), per delivery mode (tank truck, barge, pipeline), per unit — `Inputs, cálculos e outputs...docx · ¶24-31, ¶102-105, ¶128-135`; `PM-005`.

### Exceptions and workarounds
- OBSERVED — `missing quotes`: Monday/Tuesday pricing with no real quote uses the conservative rule; large ship requests are priced through a hedged special sheet; spot-formula clients use indexed formulas — `Processos Pricing...vtt · [00:49:06–00:49:28] Pedro`; `Fluxograma...docx · ¶92-106`.
- OBSERVED — `protection removal`: analysts remove sheet protection to repair the workbook; typed values override conversion formulas in the base sheets — `PM-004`; `PM-013`.

### Business invariants
- OBSERVED — `approval before load`: committee decision and a superior's approval precede the price load; whoever decides should not load — `Fluxograma...docx · ¶115-117`; `Processos Pricing...vtt · [00:49:06–00:49:28] Pedro`.
- OBSERVED — `no load below minimum`: nothing may be loaded below the minimum price (enforced by system in Spain; by checklist in Portugal) — `Fluxograma...docx · ¶86-90, ¶57-62`.
- OBSERVED — `Mon/Tue pricing must remain possible`: pricing must still be produced on Monday/Tuesday with incomplete quotes, with the agreed conservative behaviour — `Processos Pricing...vtt · [00:49:06–00:49:28] Pedro`.
- OBSERVED — `traceable published price`: a published price must be traceable to its inputs (the checklist exists for that) — `PM-006`; `Fluxograma...docx · ¶57-62`.
- OBSERVED — `stable output format`: the front-sheet format the commercial team receives stays stable — `Processos Pricing...vtt · [00:43:16–00:43:33] Pedro`.

### Structural constraints
- OBSERVED — `internal audience`: only the pricing team and committee operate the process; the commercial team receives, does not operate — `Fluxograma...docx · ¶67-73`; `Kick-off.vtt · [00:10:54–00:11:59] Pedro`.
- OBSERVED — `parallel Spain process`: a parallel pricing process for Spain already exists with a system-side floor, sharing the committee — `Fluxograma...docx · ¶86-90, ¶108`.
- UNKNOWN — `where pricing data must live`: whether an existing or mandated data platform already holds pricing data for other processes is not stated in any Discovery source; the only hint is that the Spain process runs with a system-side floor somewhere — `Fluxograma...docx · ¶86-90`.
- OBSERVED — `term contracts priced in SAP`: SAP computes weekly term-contract prices with its own formulas — `Fluxograma...docx · ¶93-95`.

### Material user tasks
- OBSERVED — `daily wide entry`: the analyst types ~85 values per daily row into the input register — `PM-001`.
- OBSERVED — `what-if projection`: the analyst projects Monday/Tuesday prices and plays the margin in the Simulador — `Kick-off.vtt · [00:57:44–00:58:23] Pedro`.
- OBSERVED — `review and approve`: checklist review, committee decision, superior approval — `PM-006`; `Fluxograma...docx · ¶107-117`.

### Genuine vs accidental complexity
- HYPOTHESIS — `six copies`: four unit outputs are a genuine consumer requirement (`four unit outputs`), but five independent recomputations instead of one model with a unit toggle are implementation accident; the Simulador copy is a genuine task, not an accident — `PM-003`; `Inputs, cálculos e outputs...docx · ¶151-157`.
- HYPOTHESIS — `per-port lookup`: port-specific cost rules are genuine; the string-built dynamic lookup is accidental — `PM-005`.

### Material unresolved semantics
- UNKNOWN — `market feeds consumption`: whether the two market series are read by anything downstream — `PM-011`; `PM-U-006`.
- UNKNOWN — `base sheets alive`: the document says the base sheets apply all pricing logic; the workbook's base-sheet dates stopped advancing weeks before capture — `Inputs, cálculos e outputs...docx · ¶61`; `PM-U-007`.
