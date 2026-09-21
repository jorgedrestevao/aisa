# Frame — fixture excerpt / Round F-01

## Single problem sentence

**(fixture — unchanged from the engagement's frame sentence)**

## What must survive into Options

### Process meaning
- C-072 — the daily price is computed as cedência → base → venda → mínimo, split até/após the week change
- C-070 — the same prices are delivered in four units for the system load
- C-071 — a separate biofuel-blend output family exists (`Outputs BIOS`)
- C-074 — the analyst projects Monday/Tuesday prices and plays the margin in an editable what-if copy

### Business invariants
- C-073 — Monday/Tuesday pricing must remain possible with incomplete quotes, under the agreed conservative behaviour
- C-026 — an independent approval precedes the price load
- C-076 — nothing is loaded below the minimum price
- C-009 — the output format the commercial team receives stays stable

### Structural constraints
- C-013 — the operating population is entirely internal (analysts + committee); the commercial team receives, does not operate
- C-036 — sensitivity is Interno
- C-028 — no separate budget; the internal IT team builds
- C-052 — SAP remains the truth for term-contract client terms
- U-035 — whether an existing or mandated data platform must hold pricing data is still open — swing: decisivo

### Decision-changing Unknowns
- U-028 — can the reference application's owner absorb a second pricing line? — `swing: decisivo: reuse vs build`
- U-032 — which inputs are missing on Monday/Tuesday and what does the process do today? — `swing: decisivo: fill gaps vs replace the estimation method`
- U-037 — is there a method today for estimating a missing quote? — `swing: decisivo: formalize vs design from zero`

### Material scope / task obligations
- C-075 — the daily entry of ~85 values per row is a task the to-be must serve
- U-033 — the consumer of the blend output family is unknown — an output family may not be dropped silently
- U-034 — whether the what-if task must survive is open
