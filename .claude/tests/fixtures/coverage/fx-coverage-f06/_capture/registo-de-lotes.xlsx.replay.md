# Replay report — registo-de-lotes.xlsx

> Source sha256: `f2f2462e1f03` | Replayed: 2026-09-14T23:15:54 | Tool: xlsx_extract.py v1.2.0 | Cells checked: 0 (skipped 0 empty lookups)
> Rule: **no check = no claim.** Every row below is a mechanical recomputation; anything the battery cannot replay is listed under *Not replayable*.

## Summary

| check | findings | high | medium | low | info |
|---|---|---|---|---|---|
| lookup integrity | 0 | 0 | 0 | 0 | 0 |
| key uniqueness | 0 | 0 | 0 | 0 | 0 |
| whitespace/casing | 0 | 0 | 0 | 0 | 0 |
| staleness | 0 | 0 | 0 | 0 | 0 |
| pattern exceptions | 0 | 0 | 0 | 0 | 0 |
| orphan references | 0 | 0 | 0 | 0 | 0 |

## Findings

**0 findings.** The battery ran and found nothing — absence of findings is itself evidence (checked cells: 0).

**Out of scope: 0 formula call(s) declined as not replayable** (see below). A declined call produces no finding in either direction: it is neither a defect nor a clean check.

## Not replayable

None — every formula family found was inside the supported battery.

## Notes

- Staleness ages are computed against the replay date (2026-09-14); re-running on another day shifts day counts, not conclusions.
- Text matching mirrors Excel: case-insensitive; the TRIM pass isolates whitespace-only defects.
- Declared limits of the battery: lookups are replayed first-to-last and literally. `XLOOKUP` with `search_mode` other than 1, and any criterion carrying Excel wildcards (`*`, `?`, `~`), are declined as not replayable instead of being compared under the wrong semantics — those formulas are correct in Excel and a literal comparison would report anomalies that do not exist.
