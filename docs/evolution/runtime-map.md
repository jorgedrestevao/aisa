# P0 — Runtime map

Traçado por inspeção estática do commit registado em `source-inventory.json`.
Sem alterações de comportamento. Onde a inspeção não é conclusiva, está escrito
`NÃO VERIFICADO` — não foi inferido.

## 1. Pontos de entrada

17 comandos em `.claude/commands/`, 24 skills em `.claude/skills/`.

| Comando | Alvo | Nota |
|---|---|---|
| `/start` | skill `aisa-start` | único que escreve o scaffold inicial |
| `/orient` | — | sem comando; skill `aisa-orient` é invocada por mensagem sem `/` (P-14) |
| `/round` | skill `aisa-round` | corre as 6 lentes inline, ou uma isolada |
| `/capture` | skill `aisa-capture` | L1/L3/L2 + tier de texto (LT) |
| `/answer` | skill `aisa-answer` | transição de estado + `answers.md` |
| `/status`, `/resume` | skill `aisa-status` | ambos os comandos apontam à mesma skill |
| `/frame` | skill `aisa-frame` | → 6 personas em paralelo → `chairman-synthesis` |
| `/options` | skill `aisa-options` | → 7 personas (entra `solution-architect`) → `chairman-synthesis` |
| `/simulate` | skill `aisa-simulate` | advisory |
| `/premortem` | skill `aisa-premortem` | advisory |
| `/decide` | skill `aisa-decide` | auto-invoca `aisa-synthesize` |
| `/synthesize` | skill `aisa-synthesize` | 5 topic packs |
| `/blueprint` | skill `aisa-blueprint` | coverage etapa `blueprint` |
| `/render` | skill `aisa-render` | coverage etapa `render` |
| `/revisit` | skill `aisa-revisit` | advisory |
| `/retro` | skill `aisa-retro` | staging em `_retro/`, curadoria humana |
| `/dashboard` | **`library/kernel/tools/dashboard.py` diretamente** | não há skill `aisa-dashboard` |

Não existem skills `aisa-dashboard` nem `aisa-resume`: `/dashboard` chama o motor,
`/resume` reutiliza `aisa-status`.

## 2. Motores determinísticos (`library/kernel/tools/`)

| Ficheiro | Linhas | Papel |
|---|---:|---|
| `dashboard.py` | 7939 | modelo de estado + página; `build_model()`, `--json`, `--serve`, `--url` |
| `coverage.py` | 3943 | inventário, veredictos, relatório, publicação |
| `xlsx_extract.py` | 3227 | L1 extração + L3 replay de `.xlsx`/`.xlsm` |
| `text_extract.py` | 722 | tier LT: `.docx` (python-docx), `.pdf` (pypdf), `.vtt`/`.srt`/`.txt`/`.md`/`.csv` (stdlib) |
| `fields_draft.py` | 499 | rascunho de campos/contratos a partir de L1 |

Executar não é escrever: a regra read-only de `library/` cobre *edições* em runtime.

### Coverage — etapas e operações

`STAGES = ("reconciliation", "blueprint", "render")`

Subcomandos: `inventory` (denominador) · `check` (veredictos, read-only) ·
`report` (projeção Markdown, read-only) · `finalize` (publica rascunho como versão).

`finalize` é a **única operação de escrita** do motor e escreve só em
`<engagement>/_coverage/`.

Invocadores declarados: skills `aisa-answer`, `aisa-blueprint`, `aisa-capture`,
`aisa-render`, `aisa-status`.

## 3. Hooks

10 ficheiros em `.claude/hooks/`; **9 são hooks registados**, `_common.py` (142 linhas)
é biblioteca partilhada.

| Evento | Matcher | Hook |
|---|---|---|
| PreToolUse | `Write\|Edit` | `pre-write-guard.py` (fail-closed; guarda `library/`) |
| PreToolUse | `Skill` | `pre-lens-order-check.py` |
| PreToolUse | `Skill` | `phase-gate-check.py` |
| PostToolUse | `Write\|Edit` | `on-su-change.py` (atualiza dashboard) |
| PostToolUse | `Write\|Edit` | `su-confirmed-guard.py` |
| PostToolUse | `Write\|Edit` | `synthesis-validate.py` |
| PostToolUse | `Write\|Edit` | `render-validate.py` (610 linhas, o maior) |
| PostToolUse | `Write\|Edit` | `blueprint-validate.py` |
| Stop | `*` | `phase-completeness.py` |

`permissions.deny`: `Write(./library/**)`, `Edit(./library/**)`.

**Limite material para P2/P3**: todos os hooks de escrita disparam em `Write|Edit`.
Uma escrita feita por **subprocesso** (por exemplo `coverage.py finalize`, ou qualquer
script via Bash) não passa por `PostToolUse` e **não é observada** por estes hooks.
`on-su-change.py` é atualização assíncrona da projeção, não um mecanismo transacional.

## 4. Autoridades e artefactos por engagement

| Artefacto | Autoridade |
|---|---|
| `shared-understanding.md` | afirmações e estados epistemológicos (fonte de verdade) |
| `answers.md` | resposta literal do utilizador |
| `decisions.md` | decisões `D-NNN` |
| `_state.json` | fase e ronda |
| `_coverage/` | registos de cobertura (escritos só por `coverage.py finalize`) |
| `_capture/` | evidência de captura (entrada: `evidence-index.md`) |
| `_synthesis/`, `_blueprint/`, `_render/`, `_simulation/`, `_retro/` | artefactos de fase |
| `dashboard.html` | **projeção gerada**; nunca editar à mão |

Em modo council-independent, `chairman-synthesis` é o único escritor da SU.

### Escrita atómica

O padrão `tmp → mv` para `_state.json` está declarado em 4 skills
(`aisa-start`, `aisa-frame`, `aisa-options`, `chairman-synthesis`).
Os restantes escritores de `_state.json` **não declaram o padrão no texto da skill**.
NÃO VERIFICADO se o omitem em execução — P1 tem de mapear escritor a escritor.

## 5. Estados e fases

- `library/kernel/states.md` (175 linhas): 5 estados (Confirmed/Assumed/Unknown/
  Conflicted/Risky), transições com `was <id>` e `resolved →`, meias-vidas
  epistémicas, economia de perguntas, compatibilidade com SUs pré-v2.2.
- `library/kernel/phases.md` (268 linhas): Enquadramento (P-0) → Discovery →
  Framing → Options → Decision, com regras de transição e registo de aprovação
  de frame.
- `library/kernel/coverage-contract.md` (1099 linhas): esquema v1, locators,
  inventário/atualidade, fingerprints semânticos, concorrência de revisão,
  códigos de passagem.

## 6. Entradas de piloto (P8)

`projects/*` está em `.gitignore`. O checkout tem **4 engagements**, fornecidos fora de
banda e deliberadamente não versionados (dados de cliente):

| Engagement | Entradas |
|---|---|
| `cae-automation-pilot-4` | `CAEs - Processos para automatização.docx`, `analise_automatizacao_caes.md` |
| `dpt-galp-jp-pilot-4` | `Dayly_pending_tickets_Anonimo.xlsx` |
| `kam-onboarding-pilot-4` | `Requisitos_Onboarding_KAM_v1.pdf` / `.txt`, `sponsor-questions-R01.md` |
| `pricing-bunkers-pilot-4` | `PREÇO BANCAS_03_08_26.xlsm`, transcrição `.vtt` |

Cobrem os dois tipos que P8 exige (operacional/tickets e Excel com regras). Os oráculos
não estão construídos: `ACCEPTANCE.md` exige inspeção independente da fonte e proíbe
gerá-los a partir do candidato. Trabalho de P1.

## 7. Subárvores de apoio versionadas

Chegaram como entrada durante P0 e passaram a fazer parte do repositório.

### `docs/runtime-hardening/` — 44 ficheiros

- `patches/f16-decision-ref-alias.patch` — registo da correção já instalada em
  `dashboard.py` (`bp_decision_id` normaliza `decision_ref` e `concretizes_decision`).
- `accept_phase1..3.py` — **aceitação executável**. Correm contra os engagements reais em
  `projects/` (ou `$AISA_ENGAGEMENTS_ROOT`), não escrevem, saem 0/1. Terceiro modo de runner.
- `repro-coverage-*.py` (8) — ensaios que **escrevem** `docs/review-evidence/`. Não correr
  em medições de baseline.
- `coverage-phase-1..6-report.md`, `B1-inventario.md`, `intake-scenarios/`.

### `docs/pp-pack-authoring/` — 160 ficheiros

Evidência de autoria do pack `pp`, marcada em `test_pp_pack_integrity.py` como
**histórica, nunca runtime activo**. Contém também runners:
`pilot/step-9e-evidence/accept_frente_c.py` e `accept_p14_runs.py`,
`pilot/step-9d-evidence/accept_frente_b.py`, `pilot/tools/`.
`test_user_language.py` declara-se o motor por trás de `accept_frente_c.py`.

Caminhos de que os testes dependem — e só estes:
`research/pp/authoring/` e `pilot/step-8b-post-pilot-adjudication-report.md`.
`research/pp/evidence/` (5,2 MB) não é lido por teste nenhum, mas é referenciado por
ficheiros dentro de `research/pp/authoring/`; separá-lo partiria essas referências.

## 8. Divergência por adjudicar

`accept_phase1.py:387` afirma `TOOL_VERSION == "1.13.0"`;
`library/kernel/tools/dashboard.py:44` define `TOOL_VERSION = "1.14.0"`.
O script de aceitação está atrasado face ao motor. Qual dos lados corrigir **NÃO ESTÁ
DETERMINADO** — P1.
