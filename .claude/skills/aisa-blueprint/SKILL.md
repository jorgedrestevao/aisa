---
name: aisa-blueprint
description: Produce the UX blueprint (ux-blueprint_vNN.yaml) — the designed screen architecture derived from the Shared Understanding, the decision's branch, and the pack's screen rules. The reasoning layer between domain knowledge and prototype generation; iterated with the business until approved (D-NNN). Draft mode (--option) supports /simulate during Options.
---

# aisa-blueprint

## Usage

`/blueprint [--option <O-NNN>] [--refresh]`

- No argument: requires `phase == decision` and a final `D-NNN` decision. Produces the next `_blueprint/ux-blueprint_v<NN>.yaml` for the chosen option.
- `--option <O-NNN>`: **draft mode** — allowed in Options phase; blueprints a candidate option (marked `draft: true`, never approvable). Used by `/simulate`.
- `--refresh`: shorthand after new `/answer` rows (e.g., prototype feedback) — re-runs against the updated SU and produces the next version.

The contract (schema, hard rules, versioning) is `library/kernel/blueprint-contract.md`. This skill is the executor of the pack's screen-consolidation rules — it **decides the design**; rendering the prototype happens outside aisa, from this artefact.

## Inputs (read)

- `<engagement>/_state.json`, `context.json`, `shared-understanding.md`, `frame.md`, `decisions.md`, `options.md` (draft mode), `lens-outputs/*.md`.
- Pack knowledge (`<pack>` from `_state.json.pack`):
  - `library/packs/<pack>/domain-knowledge/screen-consolidation-rules.md` — **the procedure** (field counts → screen types; role separation; approval-as-action; hard caps).
  - `screen-patterns.md` — the screen-type catalogue, density rules, Excel Familiar Anchors.
  - `security-patterns.md` — RBAC groups and visibility matrix conventions.
  - `delegation-matrix.md` (or pack equivalent) — volume constraints that shape list/search design.
  - `library/packs/<pack>/architecture-templates/<branch>.md` — the chosen branch's platform shape.
- Previous blueprint version (if any) + `answers.md` (feedback already absorbed into the SU).

## Execution steps

1. **Pre-flight.** Resolve the engagement; read `_state.json`. No `--option`: require `phase == decision` and a final D-NNN with a technology branch (a non-technology decision has no blueprint — stop and say so). With `--option`: require `phase ∈ {options, decision}` and the option to exist in `options.md`.
2. **Compile the domain view from the SU** (no invention — ids or it doesn't exist):
   - `entities` ← `lens=data` rows (+ volumes from `lens=operations`), with state machines where approval flows exist.
   - `personas` ← `lens=user` rows, mapped to RBAC groups per `security-patterns.md`.
   - Constraints ← `lens=governance` rows (sensitivity, audit) and platform limits for the branch.
3. **Run the consolidation tree** (`screen-consolidation-rules.md`) over the field inventory per entity: derive each screen's type (from the pack catalogue), sections/tabs, role visibility, approval actions. Apply the pack naming convention.
4. **Design navigation**: home per persona, screen map. Prefer the shortest journey for the highest-frequency task (from `lens=operations` volumes).
5. **Decide the exclusions**: fields present in inputs/SU that must NOT appear (sensitivity, internal calc columns) → `excluded_from_ui` with reason + `su_refs`.
6. **Carry the open questions**: any design decision blocked by an Unknown goes to `open_questions` (never a silent default). If a NEW unknown emerges (e.g., brand palette), append the `U-NNN` row to the SU first, then reference it.
7. **Validate the caps** (pack hard caps). Each violation: record in `validation.violations` AND append a Conflicted row to the SU (`partes: ux∧<lens>`), per the contract.
8. **Write** `_blueprint/ux-blueprint_v<NN>.yaml` (next version, never overwrite; `draft: true` + `option: O-NNN` in draft mode) and append to `_blueprint/blueprint-log.md`: timestamp, trigger, SU ids consumed, violations. Append one line to `council-log.md`.
9. **Output** to the user:
   ```
   Blueprint v<NN> produzido: <N> screens (<patterns>), <N> personas, <N> entidades.
   Excluídos da UI: <N> campos (ver excluded_from_ui).
   Perguntas abertas que condicionam o design: <U-NNN, …>
   Violações de caps: <none | X-NNN …>

   Próximo: gerar o protótipo a partir deste blueprint (Claude Design ou outro renderer);
   registar o feedback da validação com /answer; re-correr /blueprint --refresh;
   quando o negócio aprovar, regista a aprovação — escreverei o D-NNN e o blueprint fica frozen.
   ```
10. **On approval** (user says the business approved v<NN>): append the `D-NNN — Blueprint bp-v<NN> aprovado` block to `decisions.md` + the matching SU row, and note it in `blueprint-log.md`. Later renders read this version.

## Hard rules

1. Every node carries `su_refs`; a node without an anchor becomes an `open_questions` entry or is dropped.
2. Never overwrite a previous version; the approved version is frozen.
3. No prototype-tool specifics in the blueprint — platform constraints enter only via the pack's notes.
4. Vendor naming is allowed here (post-Options) but only branch-anchored, mirroring `lens-technology`'s rules.
