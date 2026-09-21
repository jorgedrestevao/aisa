# Evidence index

Shared evidence surface for this engagement — **parse once, reason many**
(`library/kernel/orchestration.md` → *Evidence contract*).

Normalized evidence below is the normal reading surface. Raw sources stay in `inputs/`,
are always openable, and are **authoritative on conflict**.

| source | format | normalized evidence | status | cite as |
|---|---|---|---|---|
| `registo-de-lotes.xlsx` | `.xlsx` | `process-model.md` (PM ids) + `registo-de-lotes.xlsx.replay.md` | `ok` | `PM-NNN → <sheet>!<cell>` |
| `registo-de-lotes-2024.xlsx` | `.xlsx` | `registo-de-lotes-2024.xlsx.extraction.json` | `ok` | `<file>!<sheet>!<cell>` |
| `fluxo-de-libertacao.pptx` | `.pptx` | — | `not captured` | leitura humana do ficheiro bruto |

**Status vocabulary** — `ok` extracted · `empty` extraction ran, the source has no content
(absence is evidence) · `failed` deterministic extraction could not run, read the raw source ·
`skipped` extraction library unavailable, read the raw source · `not captured` format outside
the capture tiers (not a failure) — read the raw source.
