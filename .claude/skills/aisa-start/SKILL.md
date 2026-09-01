---
name: aisa-start
description: Start a new aisa engagement. Captures the literal request + requester, scaffolds the engagement folder, and writes the initial _state.json (phase=discovery).
---

# aisa-start

## Usage

`/start <slug> [pack]`

- `<slug>`: kebab-case slug for the engagement (e.g., `galp-adv`).
- `[pack]`: pack id (default: `pp`). Must exist as `library/packs/<pack>/pack.yaml`.

## Execution steps

1. **Resolve the engagement root**:
   - If `$AISA_ENGAGEMENTS_ROOT` is set → `<root>/<slug>/`.
   - Else → `projects/<slug>/` (assumes a symlink/junction is configured, or local MVP testing).
2. If the folder already exists → stop with: "Engagement `<slug>` already exists. Use /resume." Do not overwrite.
3. **Validate the pack**: confirm `library/packs/<pack>/pack.yaml` exists. If not, list available packs and stop.
4. **Capture from the user** (interactive — ask, do not invent):
   a. The literal request, verbatim, with no reformulation.
   b. The requester: name, role, authority level.
   c. Optional: documents to drop into `inputs/`.
5. **Create the folder structure**:
   ```
   <slug>/
   ├── _state.json
   ├── context.json
   ├── shared-understanding.md   (skeleton — see below)
   ├── lens-outputs/             (empty)
   ├── council-log.md            (header only)
   ├── decisions.md              (empty header)
   ├── answers.md                (header only — filled by /answer)
   └── inputs/                   (any captured docs)
   ```
6. **Write `context.json`**:
   ```json
   {
     "engagement": "<slug>",
     "literal_request": "<verbatim>",
     "requester": { "name": "<name>", "role": "<role>", "authority": "<authority>" },
     "inputs": ["<filenames in inputs/>"],
     "captured": "<ISO-8601 timestamp>"
   }
   ```
7. **Write `_state.json` atomically** (write `_state.json.tmp`, then rename over `_state.json` — `Move-Item -Force` on Windows, `mv` on Unix):
   ```json
   {
     "engagement": "<slug>",
     "pack": "<pack>",
     "phase": "discovery",
     "round": "R-00",
     "aisa_version": "0.1.0",
     "created": "<ISO-8601 timestamp>"
   }
   ```
   (`round` seeds at `R-00` — no round has run yet. The first `/round` increments it to `R-01`.)
8. **Write the `shared-understanding.md` skeleton** (the 5 state sections with their column headers, per `library/kernel/states.md`; `verificado_em`/`validade` per its *Epistemic half-lives* section; the `Saúde epistémica` header line stays `—` here — `/status` fills it):
   ```markdown
   # Shared Understanding — <slug>

   > Engagement: <name>
   > Sponsor: <requester name>
   > Iniciado: <date>
   > Fase actual: Discovery
   > Última actualização: <timestamp>
   > Saúde epistémica: —

   ## Confirmed

   | id | lens | claim | evidência | verificado_em | validade | ronda |
   |----|------|-------|-----------|---------------|----------|-------|

   ## Assumed

   | id | lens | claim | base da assumption | verificado_em | validade | ronda |
   |----|------|-------|--------------------|---------------|----------|-------|

   ## Unknown

   | id | lens | pergunta | quem responde | criticidade | ronda |
   |----|------|----------|---------------|-------------|-------|

   ## Conflicted

   | id | lens | conflito | partes | criticidade | ronda |
   |----|------|----------|--------|-------------|-------|

   ## Risky

   | id | lens | risco | impacto | mitigação proposta | ronda |
   |----|------|-------|---------|--------------------|-------|
   ```
9. Write `council-log.md` with a header (`# Council Log — <slug>`), `decisions.md` with a header (`# Decisions — <slug>`), `answers.md` with a header (`# Answers — <slug>`), and `story.md` with `# Story — <slug>` + **Episódio 1** (o pedido: quem pediu, o quê, porquê — 4-6 frases na voz do sponsor).
10. Output: "Engagement `<slug>` created (pack: `<pack>`). Phase: discovery. Next: `/round` to run Discovery, or `/round business` lens-by-lens."
