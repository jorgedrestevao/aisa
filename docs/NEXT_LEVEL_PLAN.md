# aisa — Next Level Plan

> Data: 2026-08-31 · Branch: `claude/repo-gaps-analysis-02922z`
> Companion: `docs/GAP_ANALYSIS.md` (auditoria), `docs/UX_BLUEPRINT_PROPOSAL.md` (desenho da camada UX)
> Estado: **Vagas 1–2 implementadas neste branch** (ver §3); validação live feita; pendências do sponsor em §5.
> **Sequela**: o build da v3 (5 peças epistémicas) tem plano de execução autónoma próprio em `docs/V3_IMPLEMENTATION_PLAN.md`.

---

## 1. Tese

O ativo do aisa é o **modelo de conhecimento com proveniência** (SU + ids + 5 estados + decisões + evidência). O next level não é "mais automação do mesmo" — é mudar a categoria do sistema em três reframings empilhados:

1. **Produto**: de documentar a decisão → a *derisker* da decisão (**simulação de opções + value of information**). O render determinístico torna barato projetar o futuro completo de cada opção antes do `/decide`.
2. **Operação**: de ferramenta operada → colega que corre o engagement entre gates humanos (ingestão MCP, answers assíncronos, rondas auto-disparadas). O humano fica onde o design já o exige: frame, decisão, aprovação do blueprint.
3. **Negócio**: de processo por projeto → **sistema operativo da procura de digitalização** (intake/triage de todos os pedidos; a maioria morre cedo como process-change/do-nothing; os sobreviventes chegam ao portfólio comparáveis entre si).

O combustível dos três: a **camada atuarial** — dados de portfólio (estimativas calibradas com actuals, base rates de risco, question-bank auto-priorizado). Cada engagement torna o seguinte melhor.

Regras de evolução (extraídas da história do próprio repo): enforcement mecânico, nunca disciplina de LLM; o SU mantém-se markdown legível, com índices derivados; nada de regressar a ledgers formais.

## 2. Horizontes

| H | Nome | Conteúdo | Estado |
|---|---|---|---|
| H0 | Consolidar | Fechar gaps de design (answer/resume/decision/non-tech), validação live, pilot | **Gaps fechados + validação live FEITA** (`LIVE_VALIDATION_REPORT.md`); falta o pilot |
| H1 | Do documento ao contrato | Blueprint UX com proveniência; deliverables como projeções de artefactos estruturados | **Implementado neste branch** (`/blueprint`) |
| NL | Wedge do next level | `/simulate` — opções concretizadas + VOI antes do `/decide` | **Implementado neste branch** (v1) |
| H2 | Atravessar o render | Stamping de ids nos artefactos PP (via MCP de authoring) + scanner + `/trace` `/drift` | Convenção preparada (`delivery-conventions.md §2`); scanner por construir |
| H3 | SU vivo pós-go-live | Manutenção/change re-entra pelo aisa; drift contínuo; produto recorrente | Regra semeada (`delivery-conventions.md §6`); depende de H2 |
| H4 | Portfólio | Estimativas calibradas, base rates, question-bank que aprende, packs OS/Mendix a sério | Depende de ≥10 engagements |
| H5 | Método/standard | Kernel+contratos+packs como protocolo; renderers e implementers como plugins | Visão |

## 3. O que ficou implementado neste branch (2026-08-31)

### Vaga 1 — Fechar o loop (H0)

- **`/answer`** (skill `aisa-answer` + comando): transições de estado de `states.md` executáveis — resposta verbatim em `answers.md`, novas rows `was <id>`, marcador `resolved →` na row original, Conflicted→Confirmed×N. Serve Discovery **e** feedback de protótipo. (Fecha G-03.)
- **`/resume`** (comando): re-entrada de sessão via `aisa-status` + próximo comando exato. (Fecha G-04; `/export` removido dos docs fica para quando fizer falta.)
- **Modelo da Decision resolvido**: interativa (user-driven) + `--consult` opcional (1 review do solution-architect); council só em Framing/Options. Alinhados: `phases.md`, `orchestration.md`, `chairman-synthesis`, `chairman.md`, `aisa-decide`, `CLAUDE.md`. (Fecha G-05.)
- **`/decide` escreve a row `D-NNN` no SU** (§4.5 da arquitetura cumprido; fecha G-06). `aisa-start` passa a criar `answers.md`; `aisa-status` distingue rows abertas de resolvidas.
- **Caminho non-tech no render**: `applies_to` por deliverable no `pack.yaml`; `aisa-render` filtra por tipo de decisão (skip ≠ gap) e trata o sub-template arquitetural em decisões non-tech; `architecture-story` com fallback de intervenção. (Fecha G-07.)

### Vaga 2 — Contrato + wedge (H1 + next level)

- **`/blueprint`** (skill `aisa-blueprint` + comando + `library/kernel/blueprint-contract.md`): o UX Architect que executa as `screen-consolidation-rules` do pack (existiam sem executor); produz `_blueprint/ux-blueprint_v<NN>.yaml` com `su_refs` em todos os nós, `excluded_from_ui`, `open_questions`, validação de caps → Conflicted rows; loop de validação com o negócio via `/answer`; aprovação = D-NNN; `claude-design-brief` e `implementation-spec` re-sourced do blueprint aprovado. Draft mode `--option` para o simulate.
- **`/simulate`** (skill `aisa-simulate` + comando): por opção — shape (blueprint draft/intervenção), banda de esforço via `estimation-model.md`, perfil de risco, veredictos do decision-tree; comparação lado-a-lado versionada em `_simulation/`; **secção value-of-information** (Unknowns que mudam o ranking, com direção do swing). Advisory por regra dura.

### Vaga 2b — Pack pp enriquecido (v1.0.0 → v1.1.0)

- `decision-tree.md`: **R4–R6 reescritas** (eram degeneradas — veredictos iguais nos dois ramos) com lógica real de licensing/manutenção/reversibilidade; `inputs_used` completado com os 8 inputs que R0 e o hybrid-trigger usavam sem declarar; changelog no ficheiro. **Thresholds a validar na retro** (fecha G-15).
- Sinais de Discovery neutralizados: `premium_connector_need` → `integration_licensing_exposure`; `dataverse_vs_sharepoint` → `structured_vs_document_storage_today` (pack.yaml + lens-business + lens-data); exemplo vendorizado removido do template kernel `architecture-story`. (Fecha G-16 — proteção do moat da neutralidade.)
- **Novo `domain-knowledge/delivery-conventions.md`**: naming, ALM/environments, connection references, segurança/anonimização, go-live checklist, e a **convenção de stamping `su:` nas descriptions** (a preparação concreta do H2). Defaults marcados `TODO(team)` para captura na retro.

## 4. O que falta (por ordem)

1. ~~**Validação live end-to-end**~~ ✅ **FEITA (2026-08-31)** — sequência completa corrida no engagement fixture `galp-adv-val`, incluindo `/answer`, `/simulate` e `/blueprint`; council com Task subagents reais (6+7 em paralelo); todos os critérios verificados; 3 defeitos encontrados e corrigidos. Evidência: `docs/LIVE_VALIDATION_REPORT.md`.
2. **Fase 12 — pilot** com 2 consultores; retro alimenta `TODO(team)` do delivery-conventions, thresholds do decision-tree e agent-memory.
3. **H2 — scanner de traceability**: no lado do MCP de authoring, escrever o stamping (a convenção já está no pack); depois um `/trace`//`/drift` que lê a solution e faz diff contra implementation-spec/blueprint.
4. ~~**Passe editorial ao ARCHITECTURE.md**~~ ✅ **FEITO (2026-08-31)** — antecessor desambiguado como SPEA v2 (aisa v1); árvore §6 reescrita ao estado real; changelog v2.1.0; tabela de comandos/fases/exemplos atualizados (fecha G-08/G-09).
5. **Operação assíncrona (reframing 2)**: MCPs de ingestão (§10.8) + answers assíncronos — depois do pilot provar o processo síncrono.

## 5. Pendências que dependem do Jorge

1. **Calibração do pack** (via A da conversa de enriquecimento — 15 min): limite real para SharePoint como backend; o padrão de pedido que é "process change disfarçado"; rácios de estimativa por complexidade de ecrã; multiplicadores (SAP, multi-idioma, offline, multi-nível). Destino: `decision-tree.md` + `estimation-model.md`.
2. **`TODO(team)` do `delivery-conventions.md`**: publisher prefix, nomes de environments, aprovador de deploy, SLA de hypercare.
3. **Re-validação com sponsor real** — a validação mecânica está feita (item 4.1, com fixture); 1 sessão contigo como sponsor num pedido real continua a valer antes do pilot.
4. Decisão de negócio (sem pressa): qual dos três reframings do §1 é o alvo comercial — condiciona o que o H2 prioriza (consultoria própria vs produto).
