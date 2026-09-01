# aisa — Plataforma de Pre-Development Discovery & Sensemaking

**Architecture & Concept Specification**

> Versão: v2.0.0 — DRAFT para revisão da equipa
> Data: 2026-05-28
> Estado: Conceptual — pré-build
> Autor: Jorge Estêvão
> Substitui: `aisa v1` / SPEA v2 (manter-se-á em arquivo como referência). Este documento define **aisa v2.0** — major architectural rewrite, mesmo brand.

---

## Changelog

### v3.1.0 — 2026-09-01 (process capture — a lógica as-is extraída do artefacto)

Merge da linha `local/capture-line` (módulo desenvolvido em paralelo, spec `docs/PROCESS_CAPTURE_SPEC.md`) na linha v3, mais o alinhamento ao kernel v0.2.0:

- **Process capture em 3 camadas**: L1 extracção determinística de `.xlsx`/`.xlsm` (estrutura, padrões de fórmula normalizados a R1C1, colunas `input`/`derived`/`manual`, células de excepção = overrides humanos, validações, formatação condicional, cor-como-dado, comentários, anomalias, flags de VBA/links externos); L3 **replay** — bateria fixa que re-executa lookups, unicidade de chaves, whitespace/casing, staleness, excepções de padrão e referências órfãs, com a regra dura *no check = no claim*; L2 **modelo de processo** (LLM) que reconstrói as regras de negócio evidenciadas (PM-NNN, sempre com citação de célula) e a lista de interrogação (PM-U-NNN) para os humanos.
- **As lenses consomem o modelo primeiro** (`orchestration.md`), com **spot-check obrigatório de ≥1 afirmação PM contra o ficheiro cru por ronda** — o raw é sempre autoritativo; divergência gera row **Conflicted**. É a mitigação da falha correlacionada (um modelo errado a envenenar 6 lenses).
- **Alinhamento epistémico**: as regras PM carregam `verificado_em` = data de modificação **do ficheiro** (não da corrida de captura — um Excel de janeiro é evidência de janeiro, e nasce expirado se passou a meia-vida) + `validade`; as PM-U carregam `criticidade`, `custo` e `swing`. As lenses herdam esses carimbos na promoção, sem re-datar.
- **Hooks migrados para Python** (cross-platform, sem dependência de `jq`), mais o novo `pre-lens-order-check.py` que impõe a ordem sequencial das lenses em Discovery. O `pre-write-guard.py` mantém-se **fail-closed**: enforce por default, `AISA_GUARD_MODE=log` é o override administrativo.
- Deliverable `estimate` reestruturado em 10 secções por fase.

Validação: fixture xlsx com os 3 defeitos do critério de aceitação do spec §10 — duplicado de chave, falha de lookup por espaço à direita, aging >120 dias — **todos reencontrados mecanicamente pelo replay, com citação de célula** e sem envolvimento de lenses.

### v3.0.0 — 2026-09-01 (as 5 peças epistémicas — kernel v0.2.0, pack pp v1.2.0)

Build das vagas A–D de `docs/V3_IMPLEMENTATION_PLAN.md` (validação por vaga em `docs/V3_VALIDATION_REPORT.md`):

- **Metabolismo epistémico**: Confirmed/Assumed carregam `verificado_em` + `validade` (6 classes de decaimento com meias-vidas default); rows expiram e revalidam-se (`/answer --revalidate`); `/status` mostra saúde epistémica + "a revalidar". Compat: SUs antigos lidos com defaults, nunca migrados.
- **Economia da pergunta**: Unknowns carregam `custo` (email/documento/reuniao/spike) e `swing` (decisivo/dimensionante/cosmético); `/status` produz a agenda da reunião (o que paga o tempo síncrono do sponsor — e o que explicitamente não); o VOI do `/simulate` consome e corrige as classes.
- **Pré-mortem + council dialético**: `/premortem` escreve o obituário do projecto (causas narradas com ids; mitigações → requisitos/tripwires); divergências materiais entre personas disparam a ronda de antítese (≤6 calls; Concedo/Contesto/Síntese) — o substituto cirúrgico do peer review.
- **Multiverso da decisão**: `/decide` congela counterfactuals das opções rejeitadas + tripwires estruturados (TW-n); `/status` vigia-os; `/revisit` compara o presente com o ramo rejeitado e recomenda manter/adaptar/reabrir (advisory absoluto).
- **Biografias do council**: `/retro` — as 7 personas escrevem diários (staged, curadoria humana) em `agent-memory/_universal/<persona>/diary.md`; personas citam casos anteriores. O council envelhece com o uso.
- **Experiência**: `story.md` (narrativa por marco, voz de sponsor) e `render --html` (discovery-report interrogável: tooltips de proveniência por id + tabela final).

### v2.1.0 — 2026-08-31 (build next-level + passe editorial)

Actualizações após o build registado em `docs/NEXT_LEVEL_PLAN.md` e a auditoria `docs/GAP_ANALYSIS.md`:

- **Enforcement ligado**: `library/` read-only é agora hard-enforced (hook em modo enforce + deny rules) — §9.1 é verdade.
- **Comandos novos**: `/answer` (transições de estado), `/resume`, `/simulate` (comparação de opções + value-of-information), `/blueprint` (arquitectura de ecrãs com proveniência; contrato em `library/kernel/blueprint-contract.md`).
- **Fase Decision**: modo `interactive` (user-driven) com `--consult` opcional — o council corre em Framing/Options apenas. §3.1/§4.4 actualizados.
- **Deliverables por tipo de decisão**: `applies_to` no pack.yaml; decisões non-tech/do-nothing renderizam só os aplicáveis.
- **Pack pp v1.1.0**: decision-tree R4–R6 reescritas, sinais de Discovery neutralizados, novo `delivery-conventions.md`.
- **Editorial**: o sistema antecessor passa a ser referido como **SPEA v2 (aisa v1)** em todo o documento — o rename global de v2.0.0 tinha deixado antecessor e sucessor ambos como "aisa"; árvore §6 actualizada ao estado real do repo.

### v2.0.0 — 2026-05-28 (rebranding: predev → aisa v2.0)

Decisão de continuidade de brand: o produto continua a chamar-se `aisa` (não há renomeação para `predev`). O que muda é a arquitectura interna (major rewrite vs aisa v1). Renames aplicados:

- Nome do produto: `predev` → `aisa` (continuidade)
- Versão: bump para v2.0.0 (marca o corte arquitectural vs v1)
- Repositório: `aisa/` (sibling de SPEA v5; SPEA v5 fica como aisa v1 legacy)
- Repositório privado: `aisa-engagements-galp/`
- Skill names: removido prefix (`start`, `round`, `synthesize`, `render`, etc.) **[não aplicado no build — as skills mantêm o prefixo `aisa-`; os nomes curtos são os comandos]**
- Env vars: `AISA_ENGAGEMENTS_ROOT`, `AISA_GUARD_MODE`, `AISA_KERNEL_VERSION`
- `MIGRATION_FROM_AISA.md` → `UPGRADE_V1_TO_V2.md` **[não aplicado — o ficheiro mantém o nome original]**
- Pasta de design: `predev-design/` → `aisa-design/`

Conteúdo arquitectural inalterado vs v0.2.0 — só naming/branding.

### v0.2.0 — 2026-05-27 (review pass)

Sete decisões adicionais incorporadas após revisão secção-a-secção:

- §3.1 — Ordem fixa das lenses em Discovery inline: `business → operations → user → data → governance → financial`.
- §3.3 — Cada lens produz **dois outputs**: rows estruturadas no SU + `lens-outputs/<lens>.md` (prose). Slots de prose dos deliverables consomem destes summaries.
- §3.4 — Council-independent corre **em paralelo via concurrent Task subagents**. Peer review **omitido no MVP** (considerar em v2 se houver evidência de group-think).
- §4 — Em modo council-independent, **apenas o chairman escreve no SU** (agentes não têm tool Write).
- §5, §6, §7.4, §8 — Nova **camada `_synthesis/`** entre Decision e Render. Skill `aisa-synthesize` (auto-run no fim de `/decide`) produz 4-5 topic packs (`business-story.md`, `as-is.md`, `architecture-story.md`, `risks-and-assumptions.md`, `financial-story.md`). `/render` compõe os 6 deliverables a partir destes + lens-summaries. Evita re-síntese × 6 e garante coerência cross-deliverable.
- §10 — Engagements vivem em **repositório privado separado** (`aisa-engagements-galp/`). `aisa/projects/` é mount-point/config-pointer. Agent-memory split: `_universal/` (tracked, partilhável) vs `<tenant>/` (gitignored). `.mcp.json` usa `${ENV_VAR}` + `.env.example`.
- §7, §10, §11 — **Pack activo per-engagement** (`projects/<slug>/_state.json.pack`), não global. `library/packs/_active.txt` deprecated.

Apêndice C actualizado com decisões #11–#17.

### v0.1.0 — 2026-05-27 (initial draft)

Documento inicial baseado em 10 decisões da sessão de brainstorm.

---

## Sumário Executivo

`aisa` é uma plataforma de **discovery e sensemaking organizacional** que antecede qualquer escolha tecnológica em projectos de digitalização (Power Platform, OutSystems, Mendix, custom). Resolve o problema de raiz: a maioria dos projectos falha em **discovery**, não em implementação — desalinhamento entre stakeholders, entendimento incompleto do problema, contexto fragmentado, e selecção tecnológica prematura.

O aisa v2 substitui o **SPEA v2 (aisa v1)**. O sistema anterior é estruturalmente over-engineered: força reasoning determinístico em cima de um LLM probabilístico através de um kernel com dezenas de invariantes (Ledger, claims tipadas, coherence-cells, event-order gates, YAML frontmatter mandatório). Dois runs com input idêntico produziram outputs divergentes e ambos não-conformes — o que prova que o problema é estrutural, não implementacional.

A nova arquitectura inverte a filosofia, conforme a `proposta_conceptual_operational_discovery`:

| SPEA v2 / aisa v1 (rejeitado)                 | aisa v2 (adoptado)                              |
|-----------------------------------------------|---------------------------------------------------|
| AI como motor determinístico                  | AI como facilitador de discovery                  |
| Governance pesada com 20+ cells em waves      | 7 lenses + 4 fases + 6 entregas canónicas         |
| Ledger de claims tipadas                      | Shared Understanding em 5 estados                 |
| Pipeline lock-step com invariantes prosa      | Hooks-enforced + advisory soft gates              |
| Cells reimplementam runtime em markdown       | Skills/agents/hooks/commands nativos Claude Code  |

`aisa` produz, no fim de cada engagement, **6 entregas canónicas** prontas para handoff: Discovery Report (cliente), Executive Report (C-suite), Architecture Blueprint (tech leadership), Implementation Specification (PP maker/dev), Claude Design Brief (geração de protótipos), Estimate (effort/cost/timeline). A fonte-de-verdade durante o engagement é um único artefacto vivo (`shared-understanding.md`); as 6 entregas são renderizadas determinísticamente a partir dele no fim da fase Decision.

---

## 1. Contexto e Motivação

### 1.1 O problema de raiz

As organizações iniciam projectos assim:

```
Need → Technology Selection → Implementation
```

Quando o fluxo correcto deveria ser:

```
Need → Operational Understanding → Multi-Perspective Discovery →
Alignment → Root Cause Analysis → Solution Framing →
Technology Selection → Implementation
```

A maioria dos projectos falha entre `Need` e `Implementation` porque os passos intermédios são saltados. Não é problema de capacidade técnica — é problema de **entendimento compartilhado**.

### 1.2 Porque o SPEA v2 (aisa v1) falhou estruturalmente

O aisa v1 tentou resolver isto com um kernel formal — `cells`, `waves`, `Claim Ledger`, `event ordering`, `coherence-cells`, `YAML frontmatter por output`. Em produção real, dois runs com **input idêntico e modelo idêntico** divergiram nos seguintes pontos (documentado em `aisa-output/dayly_pending_tickets_anonimo_20260527_2050/_diff/` e `..._20260527_2051/_diff/`):

| Critério | RUN-A | RUN-B |
|---|---|---|
| Ordem AGENT_DELEGATED ↔ MODEL_TIER_MISMATCH | Invertida | Correcta |
| YAML frontmatter em cell outputs | Ausente | Presente |
| Coherence-cell lifecycle gate (peers em QUESTION) | Violada (executou) | Respeitada (deferred) |
| Granularidade de Pending Questions | 5 compostas (errado) | 15 individuais (correcto) |
| Subagentes não-autorizados | Não | Sim (xlsx skill) |
| Cobertura do Ledger | Mais cells, contradições internas | Menos cells, sem contradições |

**Conclusão**: o LLM esquece-se de subconjuntos diferentes dos invariantes em cada run. O problema não é o LLM — é a densidade do contrato. Mais invariantes não resolvem; menos invariantes (mas enforced) resolvem.

### 1.3 A inversão filosófica

Da `proposta_conceptual_operational_discovery`:

> *"A AI não atua como árbitro da verdade; motor determinístico; sistema de governance pesada. A AI atua como facilitador de discovery; sintetizador contextual; detector de inconsistências; gerador de perguntas; amplificador de alinhamento organizacional."*

> *"A maioria das organizações não precisa de reasoning determinístico. Precisa de entendimento compartilhado."*

`aisa` adopta esta inversão como axioma. Tudo o que segue deriva daqui.

---

## 2. Princípios Fundamentais

Estes 9 princípios são vinculantes e o desenho deriva deles:

1. **Discovery antes de solução, sempre.** A ferramenta resiste activamente a nomear **vendor ou produto específico** até à fase `Options`. As 6 primeiras lenses (`business`, `operations`, `user`, `data`, `governance`, `financial`) podem identificar **necessidades digitalizáveis** ("processo precisa de mobile access", "dados sensíveis em SharePoint hoje") mas não nomeiam Power Platform / OutSystems / Mendix / Dataverse / etc. A lens `technology`, e só ela, é que entra em Options para mapear opções concretas a essas necessidades.

2. **Shared Understanding como artefacto de processo; deliverables como artefactos de transição.** O SU é o que o consultor mantém vivo durante todo o engagement (é onde se vê *onde estamos*). Os 6 deliverables são produzidos no fim como handoff para implementação. Não é "SU OU deliverables" — é "SU durante, deliverables na transição". Os deliverables são compostos a partir do SU + `_synthesis/` topic packs + `decisions.md`, de forma determinística.

3. **5 estados, não tags compostas.** Cada item do conhecimento está em exactamente um de: `Confirmed | Assumed | Unknown | Conflicted | Risky`. Sem `[FACTO]/[HIPÓTESE]/[DOC-FACTO]/[DOC-HIPÓTESE]` × modifiers. Legível por humanos.

4. **Lenses independentes em momentos críticos.** Framing, contradiction-scan, options e decision correm em modo **council-independent** (agentes paralelos via subagent, vendo apenas `context.json`, sem contaminação). Discovery corre inline para acumular contexto rápido. Modo declarado pela fase, não pela skill.

5. **Soft gates, hard guard.** Apenas uma regra é hard-enforced (via hook + settings deny): `library/` é read-only em runtime. Tudo o resto (ordem, completude, qualidade) emite warnings advisory; o utilizador pode override com justificação registada.

6. **Native Claude Code architecture.** Skills, agents, hooks, commands, agent-memory. Sem reimplementar runtime em markdown.

7. **Packs leves.** Um pack declara apenas: `glossary`, `question-bank`, `lenses-config`, `deliverable-templates`. Não declara cells, waves, event-orderings, schemas de claims. O pack `pp` é o único validado; `outsystems`, `mendix`, `generic` são scaffolds para a equipa preencher.

8. **6 entregas canónicas, first-class.** Toda a engagement bem-sucedida termina com Discovery Report + Executive Report + Architecture Blueprint + Implementation Spec + Claude Design Brief + Estimate. Não são renderings opcionais — são parte do contrato.

9. **Memory institucional cresce com uso.** `.claude/agent-memory/<agent>/` acumula constraints recorrentes, anti-padrões observados, padrões corporativos. Esta memória é lida pelo respectivo agente em todas as rondas subsequentes.

---

## 3. Arquitectura Conceptual

### 3.1 As 4 Fases

A engagement progride em 4 fases declaradas em `library/kernel/phases.md`:

| Fase | Objectivo | Lenses activas | Modo | Output da fase |
|---|---|---|---|---|
| **Discovery** | Mapear contexto operacional, stakeholders sombra, as-is process, constraints. Não menciona tecnologia. | business → operations → user → data → governance → financial (**ordem fixa, sequencial**) | inline | SU populado em estados `Confirmed/Assumed/Unknown/Conflicted/Risky` + `lens-outputs/<lens>.md` por lens |
| **Framing** | Sintetizar uma frase única de problema, validada pelo sponsor. Detectar contradições críticas. | as 6 lenses de Discovery (via personas) + chairman | council-independent | `frame.md` + Conflicted rows no SU |
| **Options** | Gerar opções (não-fazer / process change / use existing better / PP / alt). Avaliar cada uma contra constraints e critérios. | technology (entra aqui pela 1.ª vez) + chairman | council-independent | `options.md` com prós/contras matriciais |
| **Decision** | Escolher, justificar, registar alternativas, riscos, condições de revisão. Blueprint UX (engagements com UI). Renderizar as entregas. | o utilizador decide; lens-technology consultável (`/decide --consult`) | interactive | `decisions.md` + row D-NNN no SU + `_blueprint/` + deliverables em `_render/` |

**Soft gates entre fases:**

- `discovery → framing`: warning se `Unknown Critical > N` ou `Conflicted unresolved > 0`.
- `framing → options`: warning se a frase de framing não foi confirmada pelo sponsor (sem `Confirmed by sponsor` no SU).
- `options → decision`: warning se < 3 opções avaliadas, ou se `non-tech option` ausente.
- `decision → render`: warning se decisão não tem justificação ou alternativas registadas.

Todos overrideable com justificação. Nenhum bloqueia. As warnings vivem em `_state.json` e em `council-log.md`.

### 3.2 Os 5 Estados de Conhecimento

Cada linha do Shared Understanding está em **exactamente um** destes estados:

| Estado | Significado | Quando aplicar |
|---|---|---|
| **Confirmed** | Validado por evidência directa ou pelo sponsor | Documento citável, screenshot, USER_ANSWER explícito |
| **Assumed** | Inferência razoável, declarada como tal | Padrão da indústria, "tipicamente em projectos PP corporativos…", razoável mas não verificado |
| **Unknown** | Lacuna identificada que precisa de answer | Pergunta para o sponsor, gap entre stakeholders, dado necessário não disponível |
| **Conflicted** | Stakeholders ou fontes discordam | "Business diz X, Compliance diz não-X" — TEM de resolver antes de avançar para Decision |
| **Risky** | Alta incerteza com impacto material | "SAP API latency unknown — se >2s mata o caso de uso mobile" |

Transições típicas: `Unknown → (USER_ANSWER) → Confirmed` ou `Assumed`. `Conflicted → (sponsor decision) → Confirmed` ou `Risky`. Desde o kernel v0.2.0, Confirmed/Assumed carregam `verificado_em` + `validade` (classe de decaimento): conhecimento expira e revalida-se — ver `library/kernel/states.md` → *Epistemic half-lives* e *Question economics* (custo/swing nos Unknowns).

### 3.3 As 7 Lenses

Cada lens é uma skill em `.claude/skills/lens-<name>/SKILL.md`. Independente, idempotente, lê context.json + (depending on mode) parte ou totalidade do SU, emite contribuições com estado.

| Lens | Objectivo | Sinais que recolhe |
|---|---|---|
| **business** | Impacto, urgência, prioridade estratégica, KPIs | Stakeholders sombra, motivação não-declarada, urgência real vs declarada |
| **operations** | Processo real, fricção, bottlenecks, exceptions, saber tribal | As-is map, handoffs, decisões discricionárias, "Excel power users" |
| **user** | Experiência real dos utilizadores | Personas, jornadas, dores, friction concreta |
| **data** | Ownership, qualidade, sensibilidade | Inventário, classificação, lineage, master data, RGPD scope |
| **technology** | Viabilidade técnica (corre só em Options) | Constraints arquitecturais, integração existente, ecossistema |
| **governance** | Risco organizacional, compliance, segurança | RGPD, ISO, auditoria, separation of duties, RBAC |
| **financial** | Custo as-is, custo do-nothing, ROI esperado | TCO, OPEX vs CAPEX, payback, financial constraints |

**Importante**: a lens `technology` **não corre em Discovery**. É uma regra do kernel, não negociável.

**Output dual de cada lens**: ao terminar uma ronda, cada lens produz **dois artefactos**:
1. **Rows estruturadas no `shared-understanding.md`** (com `id`, `estado`, `evidência`, `ronda`).
2. **`projects/<slug>/lens-outputs/<lens>.md`** — prose narrativa do que a lens descobriu nessa ronda (1-3 parágrafos por ronda, append-only).

Os deliverables consomem os summaries narrativos para preencher slots de prose (`business_context`, `current_state_summary`, etc.) sem precisar de re-sintetizar a partir das rows. Isto garante: (a) determinismo do render; (b) coerência entre deliverables que partilham temas. Discovery é "qualquer coisa menos tecnologia".

### 3.4 Council Híbrido — Modos de Orquestração

Duas formas de invocar uma lens, **declaradas pela fase**:

- **`mode: inline`** — A lens corre como skill no thread actual. Vê context.json + SU acumulado + lens-outputs anteriores. Sequencial, na ordem fixa (business → operations → user → data → governance → financial). Contexto partilhado entre lenses. Usado em **Discovery**.
- **`mode: council-independent`** — Os 6/7 agentes correm **em paralelo via concurrent Task subagents**. Cada um vê apenas context.json + extracto temático do SU (não vê outputs dos outros agentes). Quando todos terminam, `chairman-synthesis` lê os outputs em conjunto e sintetiza. Padrão Karpathy. Usado em **Framing, Options, Decision**.

**Por que esta divisão**: em Discovery o objectivo é cobertura ampla rápida — partilhar contexto entre lenses ajuda. Em Framing/Options/Decision o objectivo é detectar **divergência genuína de perspectivas** — partilhar contexto contamina. O chairman é o único componente que vê todos os outputs de uma vez.

**Por que paralelo (não sequencial isolado)**: paralelo é mais rápido e tem isolation natural (cada Task subagent tem context isolado). Sequencial isolado seria ~6× mais lento sem ganho semântico. O Claude Code Task tool suporta concorrência nativa.

**Peer review**: omitido no MVP. O padrão Karpathy completo inclui peer review (cada agente comenta o do vizinho antes do chairman), adicionando ~50% de custo. Adicionamos em v2 só se observarmos group-think em produção (improvável dado o isolation completo).

Custo: Discovery = ~6 LLM passes por ronda (uma por lens, sequencial). Framing/Options/Decision = ~7-8 LLM passes (6 agentes em paralelo + chairman + às vezes lens-technology). Pacote total por engagement: ~30-50 LLM passes (vs 100+ no aisa v1 pp-consulting). Mais barato, mais correcto.

---

## 4. O Artefacto Vivo — `shared-understanding.md`

### 4.1 Schema

Markdown puro, sem YAML frontmatter. 5 secções por estado, cada uma uma tabela. (Kernel v0.2.0: Confirmed/Assumed têm ainda `verificado_em`+`validade`; Unknown tem `custo`+`swing` — exemplos abaixo mantêm o schema base por legibilidade; o normativo é `states.md`.)

```markdown
# Shared Understanding — <project-slug>

> Engagement: <name>
> Sponsor: <name>
> Iniciado: <date>
> Fase actual: <Discovery|Framing|Options|Decision>
> Última actualização: <timestamp>

## Confirmed

| id        | lens         | claim                                                                     | evidência                          | ronda |
|-----------|--------------|---------------------------------------------------------------------------|------------------------------------|-------|
| C-001     | business     | Sponsor é o Director de Procurement António Silva                         | USER_ANSWER 2026-05-27             | R-01  |
| C-002     | operations   | Processo actual usa Excel + Outlook; 47 aprovações/mês                    | inputs/process.xlsx; sponsor       | R-01  |
| ...       | ...          | ...                                                                       | ...                                | ...   |

## Assumed

| id        | lens         | claim                                                                     | base da assumption                          | ronda |
|-----------|--------------|---------------------------------------------------------------------------|---------------------------------------------|-------|
| A-014     | technology   | Tenant tem licenciamento E5 (Premium connectors disponíveis)              | Galp corporate baseline; precisa confirmar  | R-02  |
| ...       | ...          | ...                                                                       | ...                                         | ...   |

## Unknown

| id        | lens         | pergunta                                                          | quem responde       | criticidade | ronda |
|-----------|--------------|-------------------------------------------------------------------|---------------------|-------------|-------|
| U-007     | data         | Qual o tempo médio de resposta SAP API para validação NIF?        | IT Architecture     | Critical    | R-02  |
| ...       | ...          | ...                                                               | ...                 | ...         | ...   |

## Conflicted

| id        | lens         | conflito                                                                     | partes                          | criticidade | ronda |
|-----------|--------------|------------------------------------------------------------------------------|---------------------------------|-------------|-------|
| X-003     | user∧gov     | Users querem mobile + offline; Governance proíbe dados sensíveis offline     | UX team vs CISO                 | Critical    | R-03  |
| ...       | ...          | ...                                                                          | ...                             | ...         | ...   |

## Risky

| id        | lens         | risco                                                                        | impacto material                | mitigação proposta              | ronda |
|-----------|--------------|------------------------------------------------------------------------------|---------------------------------|---------------------------------|-------|
| R-002     | technology   | SAP API latency em horas de pico desconhecida — pode ser >5s                 | Mata caso de uso mobile         | Spike de 1 semana antes Decision| R-02  |
| ...       | ...          | ...                                                                          | ...                             | ...                             | ...   |
```

### 4.2 Regras de edição

- **Append-by-default**: as lenses adicionam linhas, não editam linhas existentes. Edição é permitida em transições de estado explícitas.
- **Cada linha tem `id` único** (prefixo `C-/A-/U-/X-/R-`). Os ids são citáveis em `decisions.md` e nos deliverables.
- **Transições de estado**: quando um Unknown vira Confirmed, fica `U-007` removido de `## Unknown` e aparece `C-018 (was U-007)` em `## Confirmed`. O id original é preservado para rastreabilidade.
- **`evidência` é mandatória** para Confirmed e Assumed (mesmo que seja "sponsor disse" ou "indústria padrão"). Sem evidência → não pode ser Confirmed.
- **Cada linha cita `ronda` (R-01, R-02, …)** — permite rastrear quem disse o quê e quando.

### 4.3 Provenance

O `council-log.md` tem o detalhe por ronda: que lens correu, que linhas adicionou ao SU, que perguntas levantou, que resoluções aconteceram. O SU é o "estado actual"; o council-log é a "história". Together = full audit trail sem precisar de claim ledger.

### 4.4 Quem escreve no SU (writer rules)

- **Modo `inline` (Discovery)**: a lens activa escreve directamente as suas rows no SU e o respectivo `lens-outputs/<lens>.md`. Cada lens corre uma a uma, vê o que as anteriores escreveram.
- **Modo `council-independent` (Framing / Options)**: **apenas o `chairman` escreve no SU.** Na Decision (interactiva) é a skill `aisa-decide` que escreve, guiada pelo utilizador. Os 6/7 agentes via Task tool não têm tool Write (declarado em §7.3 `tools: [Read, Grep, Glob]`). Cada agente devolve a sua contribuição como retorno da Task call; o chairman recebe-as todas, sintetiza, e escreve rows novas + um `chairman-synthesis-<ronda>.md` (`F-<NN>` / `O-<NN>` / `D-<NN>`) em `lens-outputs/`.

### 4.5 Decisões no SU

Cada `/decide` cria **uma linha em `## Confirmed`** com `id: D-NNN` cross-referenciada ao detalhe em `decisions.md`. Mantém o SU completo (entendimento + compromissos) sem duplicar conteúdo. Exemplo:

```markdown
| D-001 | chair | Frame validado pelo sponsor; ver decisions.md#D-001 | decisions.md#D-001 | F-01 |
| D-002 | chair | Escolhida a opção O-003 (branch dataverse-first); ver decisions.md#D-002 | decisions.md#D-002 | D-01 |
```

---

## 5. As 6 Entregas Canónicas

Toda a engagement bem-sucedida termina com **6 deliverables** renderizados a partir do SU + `decisions.md` no fim da fase Decision. **São first-class outputs, não opcionais.**

| # | Deliverable | Audiência | Formato | Slots principais | Template |
|---|---|---|---|---|---|
| 1 | **Discovery Report** | Cliente (sponsor + stakeholders) | docx | business_context, current_state_summary, identified_processes, data_inventory, pain_points, stakeholders, sources | `library/packs/pp/deliverable-templates/discovery-report.template.md` |
| 2 | **Executive Report** | C-suite | docx | one_page_summary, decision_options, recommended_path, financial_envelope, risk_summary | `executive-report.template.md` |
| 3 | **Architecture Blueprint** | Technical leadership / architects | docx | executive_summary, chosen_architecture, entity_inventory, rbac_matrix, integration_inventory, alternatives_considered, open_assumptions | `solution-blueprint.template.md` |
| 4 | **Implementation Specification** | PP maker / developer | md | solution_name, screens_to_build, tables_to_create, flows_to_implement, security_roles, integrations, test_scenarios, sequencing | `implementation-spec.template.md` |
| 5 | **Claude Design Brief** | Pipeline Claude Design → designer | md | canvas_app_pages, page_navigation_map, persona_users, ux_requirements, brand_guidance, accessibility_notes + domain-knowledge cross-refs (powerfx-patterns, screen-patterns, security-patterns) | `claude-design-brief.template.md` |
| 6 | **Estimate** | Sponsor + procurement | docx | effort_breakdown, timeline, team_composition, assumptions, risks, change_management | `estimate.template.md` |

### 5.1 Pipeline de produção (Discovery → Decision → Synthesis → Render)

A produção dos 6 deliverables segue um pipeline em **3 camadas**:

```
Discovery+Framing+Options+Decision    Synthesis              Render
   (engagement)                       (auto-/decide)         (/render)
        ↓                                  ↓                     ↓
shared-understanding.md                _synthesis/            _render/
lens-outputs/<lens>.md       →    business-story.md    →   discovery-report
decisions.md                       as-is.md                  executive-report
                                   architecture-story.md     solution-blueprint
                                   risks-and-assumptions.md  implementation-spec
                                   financial-story.md        claude-design-brief
                                                             estimate
```

**Por que a camada `_synthesis/`**: os 6 deliverables têm temas partilhados (`business_context` aparece em Discovery Report + Executive Report; `chosen_architecture` aparece em Blueprint + Implementation Spec). Sintetizar em 6 contextos independentes produz inconsistências (Executive diz X, Discovery diz Y sobre o mesmo facto). A `_synthesis/` produz **4-5 topic packs** uma única vez; os deliverables compõem-se a partir destes.

### 5.2 Synthesis contract

`.claude/skills/aisa-synthesize/SKILL.md` corre **automaticamente no fim de `/decide`** (também invocável manualmente). Lê SU + lens-outputs/ + decisions.md, e produz:

| Topic pack | Fontes | Usado por |
|---|---|---|
| `_synthesis/business-story.md` | SU.Confirmed[lens=business] + lens-outputs/business.md | discovery-report, executive-report |
| `_synthesis/as-is.md` | SU.Confirmed[lens=operations,user] + lens-outputs/{operations,user}.md | discovery-report, solution-blueprint |
| `_synthesis/architecture-story.md` | decisions.md + SU.Confirmed[lens=technology,data] + lens-outputs/{technology,data}.md + chosen architecture-template | solution-blueprint, implementation-spec, claude-design-brief |
| `_synthesis/risks-and-assumptions.md` | SU.Risky + SU.Assumed + SU.Unknown.criticality=Critical | executive-report, solution-blueprint, estimate |
| `_synthesis/financial-story.md` | SU.Confirmed[lens=financial] + lens-outputs/financial.md + decisions.md (cost/timeline) | executive-report, estimate |

Síntese é **determinística dado os inputs**: o prompt da synthesis-skill é fixo (mora em `library/kernel/synthesis-templates/<topic>.template.md`), as fontes são endereçadas explicitamente. Re-correr `/synthesize` com os mesmos inputs produz output semanticamente equivalente.

### 5.3 Render contract

A skill `.claude/skills/aisa-render/SKILL.md` lê os `_synthesis/` topic packs + `decisions.md` + o template de cada deliverable, e produz o output em `projects/<slug>/_render/`. Princípios:

- **Determinístico dado synthesis+decisions**: rodar `/render` duas vezes produz o mesmo output (módulo timestamps). Synthesis é onde o non-determinism é absorvido (uma única vez); render é composição puramente mecânica.
- **Render falha alto** se um topic pack obrigatório está vazio (slot required sem fonte). Não inventa — emite `_render/render-gaps.md` listando o que falta e qual lens/synthesis pack deve preencher.
- **`/render <deliverable>`** renderiza apenas um; **`/render --all`** renderiza os 6.
- **Versioning incremental**: `/render` produz sempre o próximo `v<NN>` (nunca sobrescreve). Se o consultor editou `v01` manualmente, fica intacto; `v02` é uma re-render limpa.
- **Domain-knowledge cross-refs** (especialmente para Claude Design Brief): templates podem referenciar ficheiros de `library/packs/pp/domain-knowledge/` (`powerfx-patterns.md`, `screen-patterns.md`, `security-patterns.md`) por embed ou citação inline.
- **Sub-templates por arquitectura escolhida**: o Architecture Blueprint embed `library/packs/pp/architecture-templates/<chosen>.md` (canvas-only, model-driven-only, hybrid, etc.).

### 5.4 Por que 6 e não 5

A separação `Implementation Spec` ↔ `Claude Design Brief` é deliberada:
- **Implementation Spec** = o quê construir (entities, flows, security, integrations) — para o maker que escreve Power FX e configura Power Automate.
- **Claude Design Brief** = como deve parecer/sentir (screens, navigation, personas, UX, brand, accessibility) — para Claude Design gerar mockups validados.

São audiências diferentes e os outputs juntos seriam inutilizáveis.

### 5.5 Por que Estimate continua canónico

Mesmo que o user message original não tenha mencionado explicitamente, em qualquer engagement enterprise o Estimate é o que o sponsor leva à Direcção para aprovar verba. Mantém-se. Pode ser declarado `optional` no pack se nalgum contexto (ex: discovery puro pré-RFP) não fizer sentido.

---

## 6. Estrutura do Repositório

```
aisa/                                              # repo 1 — partilhável dentro da empresa
├── README.md
├── CLAUDE.md                                        # princípios (lean, sem invariantes)
├── .env.example                                     # AISA_* + placeholders MCP
├── bootstrap.ps1                                    # setup Windows (junction + env var)
│
├── .claude/
│   ├── settings.json                                # deny Write/Edit(library/**) + hooks + env (enforce)
│   ├── rules/                                       # 4 princípios curtos, path-gated
│   │   ├── library-readonly.md
│   │   ├── no-tech-mention-before-options.md
│   │   ├── shared-understanding-as-source-of-truth.md
│   │   └── render-on-decision-only.md
│   ├── skills/
│   │   ├── lens-{business,operations,user,data,technology,governance,financial}/SKILL.md
│   │   ├── chairman-synthesis/SKILL.md
│   │   └── aisa-{start,round,answer,status,frame,options,simulate,decide,synthesize,blueprint,render}/SKILL.md
│   ├── commands/                                    # thin entry points
│   │   └── {start,round,answer,status,frame,options,simulate,decide,synthesize,blueprint,render,resume}.md
│   ├── agents/                                      # personas council-independent
│   │   ├── business-analyst.md · operations-lead.md · user-advocate.md · data-steward.md
│   │   ├── solution-architect.md · compliance-officer.md · cfo-lens.md
│   │   └── chairman.md
│   ├── agent-memory/
│   │   └── _universal/<persona>/{universal-constraints,anti-patterns}.md
│   │       # _tenant/ é gitignored — vive no repo privado (corporate-patterns etc.)
│   ├── output-styles/                               # (vazio; opcional)
│   └── hooks/
│       ├── pre-write-guard.sh                       # ENFORCE: library/ read-only (o hard guard)
│       ├── on-su-change.sh · phase-gate-check.sh    # log-only no MVP (validadores em v0.2.0)
│       └── synthesis-validate.sh · render-validate.sh
│
├── library/                                         # read-only em runtime (hook + deny)
│   ├── kernel/                                      # universal, vendor-agnóstico
│   │   ├── phases.md · states.md · orchestration.md
│   │   ├── render-contract.md · blueprint-contract.md · glossary.md
│   │   ├── synthesis-templates/{business-story,as-is,architecture-story,risks-and-assumptions,financial-story}.template.md
│   │   ├── capture-templates/process-model.template.md
│   │   └── tools/xlsx_extract.py                 # L1 extracção + L3 replay (lido e EXECUTADO, nunca editado)
│   └── packs/
│       ├── pp/                                      # Power Platform — VALIDADO (v1.2.0)
│       │   ├── pack.yaml                            # deliverables (c/ applies_to) + lenses_config + refs
│       │   ├── glossary.md · question-bank.md · decision-tree.md
│       │   ├── deliverable-templates/{discovery-report,executive-report,solution-blueprint,
│       │   │                          implementation-spec,claude-design-brief,estimate}.template.md
│       │   ├── architecture-templates/{sharepoint-first,dataverse-first,hybrid}.md
│       │   └── domain-knowledge/                    # powerfx-patterns · screen-patterns · security-patterns ·
│       │       # delegation-matrix · excel-patterns · dataverse/azure-sql/sharepoint refs ·
│       │       # anonymization · flows-patterns · estimation-model · screen-consolidation-rules ·
│       │       # delivery-conventions
│       ├── outsystems/pack.yaml                     # scaffold, sem conteúdo validado
│       ├── mendix/pack.yaml                         # scaffold
│       └── generic/pack.yaml                        # scaffold platform-agnostic
│
├── projects/                                        # MOUNT POINT (gitignored) → repo 2 privado
│                                                    # aisa-engagements-<tenant>; ver §10
└── docs/                                            # ARCHITECTURE · PHILOSOPHY · ONBOARDING ·
                                                     # IMPLEMENTATION_PLAN · PACK/LENS/DELIVERABLE_AUTHORING ·
                                                     # MIGRATION_FROM_AISA · REFERENCES_ANALYSIS ·
                                                     # GAP_ANALYSIS · NEXT_LEVEL_PLAN · UX_BLUEPRINT_PROPOSAL · ISSUES ·
                                                     # V3_IMPLEMENTATION_PLAN · V3_VALIDATION_REPORT · PROCESS_CAPTURE_SPEC

# Estrutura típica de UM engagement (vive em aisa-engagements-<tenant>/<slug>/):
#   <slug>/
#   ├── _state.json                              # phase, round, pack, round_mode (run em curso), atomic writes (tmp → mv)
#   ├── context.json                             # captura do /start
#   ├── shared-understanding.md                  # ARTEFACTO VIVO (5 secções por estado)
#   ├── answers.md                               # respostas verbatim do /answer
#   ├── council-log.md                           # narrativa cronológica por ronda
#   ├── decisions.md                             # D-NNN (frame, decisão, aprovação do blueprint)
#   ├── frame.md · options.md                    # artefactos de fase (chairman)
#   ├── inputs/                                  # documentos do cliente (abertos e perfilados)
#   ├── lens-outputs/                            # prose por lens + chairman-synthesis-<F|O>-<NN>.md
#   │   └── _council-prep/                       # excertos temáticos por persona (audit)
#   ├── _capture/                                # extraction.json + replay.md por input + process-model.md (/capture)
#   ├── _simulation/                             # options-comparison_v<NN>.md (/simulate)
#   ├── _blueprint/                              # ux-blueprint_v<NN>.yaml + blueprint-log.md (/blueprint)
#   ├── _synthesis/                              # 5 topic packs + _synthesis-log.md (auto no /decide)
#   └── _render/                                 # deliverables v<NN> + render-gaps.md + render-log.md
```

---

## 7. Contratos

### 7.1 Pack contract — `library/packs/<id>/pack.yaml`

```yaml
pack_id: pp
pack_version: 1.0.0
display_name: "Power Platform Discovery"
language: pt
description: >
  Discovery and sensemaking pack tuned for Power Platform engagements.
  Vocabulary, question-bank, and deliverable templates aligned with
  Canvas Apps, Model-driven Apps, Power Automate, Dataverse.

deliverables:
  # which of the 6 canonical deliverables this pack produces.
  # 'mandatory: true' = render-on-decision will fail if missing data.
  - id: discovery-report
    mandatory: true
    template: deliverable-templates/discovery-report.template.md
  - id: executive-report
    mandatory: true
    template: deliverable-templates/executive-report.template.md
  - id: solution-blueprint
    mandatory: true
    template: deliverable-templates/solution-blueprint.template.md
  - id: implementation-spec
    mandatory: true
    template: deliverable-templates/implementation-spec.template.md
  - id: claude-design-brief
    mandatory: true
    template: deliverable-templates/claude-design-brief.template.md
  - id: estimate
    mandatory: false
    template: deliverable-templates/estimate.template.md

lenses_config:
  # per-lens hints. The kernel runs all 7 lenses; the pack tweaks the
  # signals each lens should look for in this domain.
  business:
    extra_signals: [licensing_baseline, premium_connector_need]
  operations:
    extra_signals: [excel_anchors, sharepoint_lists_anchors]
  data:
    extra_signals: [dataverse_vs_sharepoint, master_data_owners]
  technology:
    # Only active in Options phase
    constraints_to_check: [premium_licensing, dataflow_capacity,
                           ALM_environments, dataverse_storage]
  governance:
    extra_signals: [DLP_policies, environment_strategy, sensitivity_labels]
  # ... user, financial mostly use kernel defaults

domain_knowledge:
  - domain-knowledge/powerfx-patterns.md
  - domain-knowledge/screen-patterns.md
  - domain-knowledge/security-patterns.md
  - domain-knowledge/delegation-matrix.md

question_bank: question-bank.md

decision_tree:
  # ONLY consulted in Options phase. Never in Discovery.
  source: decision-tree.md
```

**Validação**: hook `pre-write-guard.py` rejeita writes a `library/`. Schema validation acontece em load-time via `aisa-start`.

### 7.2 Lens contract — `.claude/skills/lens-<name>/SKILL.md`

Cada lens é uma skill com este formato mínimo:

```markdown
---
name: lens-<domain>
description: <short>
---

# Lens — <Domain>

## Role
<O que esta lens vê no mundo. Persona declarada.>

## Inputs (always reads)
- projects/<slug>/context.json
- (if mode: inline) projects/<slug>/shared-understanding.md
- (if mode: council-independent) extracto temático do SU passado pelo orchestrator

## Outputs (always writes)
- Linhas no shared-understanding.md (append-only, com id, estado, evidência, ronda)
- `projects/<slug>/lens-outputs/<lens>.md` (append-only, prose narrativa por ronda: 1-3 parágrafos do que descobri nesta ronda + sinalização de Conflicted/Risky relevantes)
- Optional: pergunta para `## Unknown` se faltar evidência

## Hard rules (kernel-enforced)
1. Nunca menciona tecnologia específica (Power Platform, OutSystems, etc.) excepto em Options.
2. Nunca emite Confirmed sem evidência (texto, citation, USER_ANSWER).
3. Se houver gap, emite Unknown — não inventa Assumed silenciosamente.
4. Identifica-se na coluna `lens` de cada linha que adiciona.

## Signal catalog (pack-extensible)
<Lista de sinais que esta lens procura. Pack pode adicionar via lenses_config.>

## Execution
<Steps numbered. ~5-8 steps maximum. Each step idempotent.>
```

### 7.3 Agent contract — `.claude/agents/<name>.md`

Personas para modo council-independent:

```markdown
---
name: <persona>
description: <short>
tools: [Read, Grep, Glob]  # restrictive; council agents don't write directly to SU
---

# <Persona Name>

## Identity
<Quem é. Background. Estilo de raciocínio.>

## Mandate
<O que esta persona deve produzir num round council.>

## Lens binding
This agent embodies: lens-<name>

## Memory consulted
- .claude/agent-memory/_universal/<name>/universal-constraints.md
- .claude/agent-memory/_universal/<name>/anti-patterns.md
- .claude/agent-memory/_tenant/<tenant>/<name>/corporate-patterns.md (repo privado, se existir)

## Output format
<Schema do que esta persona devolve ao chairman.>
```

### 7.4 Render contract — `library/kernel/render-contract.md`

Resumo aqui (detalhe completo em §5.1–5.3):

- `/synthesize` (auto-run no fim de `/decide`) produz `_synthesis/` topic packs a partir do SU + lens-outputs + decisions.
- `/render <deliverable-id>` resolve template + slots + sub-templates a partir dos topic packs + decisions.
- Slot resolution:
  1. Procura no `_synthesis/<topic>.md` declarado pelo template.
  2. Para slots estruturados (tabelas, listas): procura no SU (por estado e por lens) ou em `decisions.md`.
  3. Se não encontra E o slot é `required` → falha alta + linha em `_render/render-gaps.md`.
  4. Se não encontra E o slot é `optional` → omite a secção.
- Render é **mecanicamente determinístico** (composição). Synthesis absorve o non-determinism uma única vez.
- Markdown puro produzido em `_render/`. Conversão para .docx via hook ou ferramenta externa (Pandoc / Word via Office365).
- Versioning **incremental, nunca sobrescreve**: `v01`, `v02`, ... — se o consultor editou `v01` manualmente, fica preservado.

### 7.5 Synthesis contract — `library/kernel/synthesis-templates/`

Cada topic pack tem um template fixo em `library/kernel/synthesis-templates/<topic>.template.md`. Estrutura:

```markdown
---
topic_id: business-story
sources:
  - shared-understanding.md#Confirmed[lens=business]
  - shared-understanding.md#Assumed[lens=business]
  - lens-outputs/business.md
synthesis_prompt: |
  A partir das fontes citadas, produz uma narrativa coerente do contexto
  de negócio: quem pediu, porquê, qual o impacto, quais os KPIs em jogo.
  Cita ids do SU em parênteses (ex: "...impacto declarado pelo sponsor (C-001)...").
  Não inventes factos. Se uma área tem só Assumed, declara-o.
---

# Business Story

{{narrative}}

## Key facts citados
{{cited_ids_table}}
```

Synthesis-skill instancia este template para cada topic, e o output vai para `_synthesis/<topic>.md`.

---

## 8. Slash Commands e Fluxo do Utilizador

| Comando | Quando | O que faz |
|---|---|---|
| `/start <slug> [pack]` | Início de engagement | Captura literal do pedido, requester. Cria `projects/<slug>/{context.json, shared-understanding.md skeleton, _state.json: phase=discovery, round=R-01}`. Activa pack (default: pp). Não pergunta sobre tecnologia. |
| `/round [lens]` | Em qualquer fase | Corre uma lens (ou orquestra a sequência completa de uma ronda). Lens determinada pelo arg ou auto-escolhida com base na fase. |
| `/capture [file]` | Discovery (auto no `/start`, freshness check no `/round`) | Process-capture de inputs `.xlsx`/`.xlsm`: L1 extracção determinística (`library/kernel/tools/xlsx_extract.py`) → L3 replay (bateria fixa de verificações) → L2 modelo de processo (LLM). Escreve `_capture/{<f>.extraction.json, <f>.replay.md, process-model.md, _capture-log.md}`. `inputs/` fica evidência pura. Spec: `docs/PROCESS_CAPTURE_SPEC.md`. |
| `/answer <id> "..."` | Em qualquer fase | Resolve uma row Unknown/Conflicted/Assumed/Risky: resposta verbatim em `answers.md`, nova row `was <id>`, marcador `resolved →` na original. |
| `/status` | A qualquer momento | Mostra fase, ronda actual, contagem de items por estado (abertos vs resolvidos), contradições por resolver, gaps abertos, próxima acção sugerida. |
| `/frame` | Discovery → Framing | Transita para fase Framing. Corre lenses em modo council-independent + chairman. Produz `frame.md` (a frase única) + `contradictions.md` resolvidas. |
| `/options` | Framing → Options | Transita para Options. Corre lens-technology + outras lenses como council. Gera 3-5 opções (incluindo `do nothing` e `non-tech`). Consulta `decision-tree.md` pela 1.ª vez. |
| `/simulate [O-NNN ...]` | Em Options | Projecta cada opção (ecrãs/intervenção, banda de esforço, riscos, constraints) lado-a-lado em `_simulation/` + lista os Unknowns *decision-flipping* (value of information). Advisory. |
| `/premortem [--horizon <meses>]` | Em Options/Decision, antes do `/decide` | O obituário do projecto datado a +N meses: causas de morte narradas (ids), sinais observáveis, mitigações → requisitos/tripwires. Soft-sugerido pelo `/decide`. |
| `/decide [--consult]` | Options → Decision | Captura escolha + justificação + alternativas + riscos + condições. Regista em `decisions.md` + row D-NNN no SU. `--consult` = review opcional do solution-architect. **Auto-corre `/synthesize` no fim.** |
| `/blueprint` | Decision (draft em Options via `--option`) | Produz `_blueprint/ux-blueprint_v<NN>.yaml` — arquitectura de ecrãs com `su_refs`, via regras do pack. Iterado com o negócio até aprovação (D-NNN). Contrato: `library/kernel/blueprint-contract.md`. |
| `/synthesize` | Auto após `/decide` (ou ad-hoc) | Produz `_synthesis/{business-story, as-is, architecture-story, risks-and-assumptions, financial-story}.md` a partir do SU + lens-outputs + decisions. Camada intermédia para garantir coerência entre os 6 deliverables. |
| `/render [deliverable\|--all]` | Fim de Decision (após `/synthesize`) | Renderiza 1 ou todos os 6 deliverables em `_render/`. Lê dos topic packs em `_synthesis/`. Falha alto se faltam topic packs ou slots required. Versioning incremental (`v01`, `v02`, ...) — nunca sobrescreve. |
| `/revisit <TW-n\|O-NNN>` | Pós-decisão, quando um tripwire dispara | Compara o presente com o counterfactual congelado; recomenda manter/adaptar/reabrir. Nunca altera a decisão. |
| `/retro` | Fecho do engagement | As 7 personas escrevem diários (staged → curadoria humana → agent-memory). O council fica mais sábio a cada engagement. |
| `/resume` | Session retomada | Lê `_state.json`, mostra onde estamos, verifica tripwires e nomeia o próximo comando. |
| `/export` | (backlog — não implementado) | Snapshot completo do engagement (para handoff ou archive). |

**Fluxo típico end-to-end** (visto pelo consultor):

```
/start galp-adv pp
  → captura pedido, requester
/round              # auto-orchestra Discovery (6 lenses sequenciais)
  → SU populado, alguns Unknown + 1 Conflicted
[user resolve Unknowns com sponsor → answers]
/round              # nova ronda Discovery se necessário
/status             # vê 2 Conflicted Critical → tem de resolver
[user resolve Conflicted com sponsor]
/frame              # transita para Framing; council-independent
  → frase única; sponsor valida
/options            # transita para Options
  → 4 opções: do nothing / process change / PP Premium / OutSystems
[sponsor escolhe PP Premium]
/decide             # captura decisão + justificação
                    # auto-corre /synthesize no fim → _synthesis/ tem 5 topic packs
/render --all       # renderiza 6 deliverables a partir de _synthesis/ + decisions.md
  → _render/ tem 6 ficheiros v01 prontos para handoff
```

---

## 9. Hooks e Enforcement

### 9.1 Hard (não overrideable)

Todos os hooks são **Python 3** (`.claude/hooks/*.py`), cross-platform e sem dependências externas. Três invariantes são hard-enforced:

1. **`library/` é read-only em runtime.** Hook `pre-write-guard.py` rejeita qualquer Write/Edit a paths sob `library/`, e **falha fechado**: enforce é o default, só um `AISA_GUARD_MODE=log` explícito o desliga (override administrativo). Backup: `.claude/settings.json` `deny: Write(./library/**)`. Executar `library/kernel/tools/*.py` não é uma escrita — o guard não se aplica a corridas do script de captura.
2. **`_state.json` writes são atómicos.** Hook (ou skill convention) força padrão `_state.json.tmp` → `mv _state.json`. Crash mid-write nunca corrompe estado.
3. **Ordem das lenses em Discovery.** Hook `pre-lens-order-check.py` bloqueia a lens N se a lens N-1 ainda não escreveu output para a ronda em curso — uma lens a ler um SU meio construído tira conclusões de evidência que ainda não foi recolhida. Sem modo log. O `/round <lens>` (lens única, tipicamente re-corrida após um `/answer`) é o único escape, e é **declarado**: o `aisa-round` escreve `_state.json.round_mode = {mode, lens, round}` antes de invocar, e o hook só se afasta quando o marcador nomeia aquela lens para aquela ronda — marcador obsoleto, de outra lens, malformado ou ausente impõem a ordem.

### 9.2 Soft (advisory, overrideable com justificação)

- **`on-su-change.py`** — quando `shared-understanding.md` é modificado, regista a alteração (log-only no MVP; o contradiction-scan em background é v0.2.0). Hoje a detecção de contradições é feita pela lens-governance (passo de conflict-scan) e pelo chairman na síntese.
- **`phase-gate-check.py`** — antes de transição de fase, verifica entry/exit criteria. Emite warning se violados. User pode prosseguir com `/frame --override "razão"`.
- **`synthesis-validate.py`** — após `/synthesize`, verifica que todos os 5 topic packs em `_synthesis/` foram produzidos sem secções vazias críticas. Se algum está vazio, lista qual lens devia ter contribuído. Bloqueia `/render --all` com warning (overrideable com `/render --skip-validate`).
- **`render-validate.py`** — antes de produzir output `_render/`, verifica que todos os required slots têm fonte. Se algum falta, gera `render-gaps.md` e ASKS confirm.

### 9.3 Por que enforcement minimalista funciona

No aisa v1, a tentativa de enforcement por prosa ("orquestrador MUST emit AGENT_DELEGATED before MODEL_TIER_MISMATCH") falha porque o LLM eventualmente esquece. Em aisa:

- **A ordem deixa de importar.** Não há events.md ordenado. Council-log é narrativo, não consequente.
- **Frontmatter mandatório deixa de existir.** Outputs são markdown puro.
- **Coherence gate deixa de existir.** Não há cells coherence; contradictions são detectadas via scan (skill independente) que corre quando o utilizador quer, ou em background via hook.

Tudo o que era "MUST" em prosa no aisa v1 é (a) hook-enforced, (b) advisory, ou (c) não-existente no aisa v2.

---

## 10. Operacionalização Enterprise

### 10.1 Dual-repo structure (data privacy)

Os engagements contêm dados de cliente sensíveis (nomes de sponsors, processos internos, KPIs, integrações específicas). Não podem viver no mesmo repositório que o `aisa/` (que deve ser partilhável dentro da empresa e potencialmente entre tenants).

**Arquitectura adoptada — dois repositórios:**

```
aisa/                              # repo 1 — partilhável dentro da empresa
├── .claude/                         # skills, agents, hooks, commands
├── library/                         # kernel + packs (pp, outsystems, mendix, generic)
├── docs/                            # documentação para equipa
└── projects/                        # MOUNT POINT — vazio por defeito;
                                     # config aponta para repo 2 via symlink/junction
                                     # ou variável de ambiente AISA_ENGAGEMENTS_ROOT

aisa-engagements-galp/             # repo 2 — privado, encrypted, restrito ao tenant
├── <slug-1>/                        # 1 folder por engagement
│   ├── _state.json
│   ├── shared-understanding.md
│   ├── lens-outputs/
│   ├── _synthesis/
│   ├── _render/
│   └── ...
└── <slug-2>/
```

**Bootstrap**: ao instalar aisa na máquina de um consultor:
1. Clone `aisa/`
2. Clone `aisa-engagements-galp/` (privado) num local separado.
3. Configurar via:
   - **(Windows)** `mklink /J aisa\projects aisa-engagements-galp` (junction).
   - **(Unix)** `ln -s ../aisa-engagements-galp aisa/projects` (symlink).
   - **OU** `$env:AISA_ENGAGEMENTS_ROOT = "C:\path\to\aisa-engagements-galp"` lido pelas skills.

**Convenções:**
- **Branch por engagement em repo 2**: `engagement/<slug>` para isolamento.
- **Skills + agents + library/ + docs/ tracked em repo 1** — equipa contribui melhorias.

### 10.2 Agent-memory split (universal vs tenant-proprietary)

`.claude/agent-memory/` em `aisa/` contém apenas memória **universal** (constraints genéricos, anti-padrões de indústria). Memória **proprietária** (e.g. "Galp usa SAP S/4HANA") vive em `agent-memory/<tenant>/` sob o repo 2 ou em ficheiros gitignored:

```
aisa/.claude/agent-memory/
├── _universal/                      # tracked em repo 1; partilhável
│   ├── business-analyst/
│   │   ├── recurring-constraints.md # "RGPD afecta qualquer processo com PII"
│   │   └── anti-patterns.md         # "engagement Procurement sem CFO presente"
│   └── ... (outros agentes)
└── _tenant/                         # symlink → aisa-engagements-galp/agent-memory/
    └── galp/                        # gitignored em repo 1; tracked em repo 2 privado
        ├── business-analyst/
        │   ├── recurring-constraints.md  # "Galp usa SAP S/4HANA via OData"
        │   └── corporate-patterns.md    # "Galp environment strategy: DEV/UAT/PROD por BU"
        └── ...
```

Cada agente, em ronda, lê **ambas as folders** (universal + tenant). O loader é da skill, não do utilizador.

### 10.3 MCP integrations com credenciais

`.mcp.json` em `aisa/` declarará os MCP servers quando o primeiro for configurado (não existe no MVP — ver §10.8). Credenciais via `${ENV_VAR}` syntax (Claude Code padrão):

```json
{
  "mcpServers": {
    "sharepoint": {
      "command": "npx",
      "args": ["@anthropic/mcp-server-sharepoint"],
      "env": {
        "SHAREPOINT_TENANT_ID": "${SHAREPOINT_TENANT_ID}",
        "SHAREPOINT_CLIENT_ID": "${SHAREPOINT_CLIENT_ID}",
        "SHAREPOINT_CLIENT_SECRET": "${SHAREPOINT_CLIENT_SECRET}"
      }
    }
  }
}
```

`.env.example` ao lado lista as variáveis sem valores. `.env` real (com valores) é gitignored.

### 10.4 Sharing com a equipa (Galp + alargado)

`aisa/` é um repositório git standard partilhável. Equipa clona repo 1, recebe `aisa-engagements-galp/` (repo 2) via grupo restrito, configura symlink/env, está pronto.

### 10.5 Pack activo per-engagement

O pack activo deixa de ser global (não há `library/packs/_active.txt`). Cada engagement declara o seu pack em `<slug>/_state.json`:

```json
{
  "engagement": "galp-adv",
  "phase": "discovery",
  "round": "R-03",
  "pack": "pp",
  "pack_version": "1.0.0",
  ...
}
```

Permite a um consultor correr engagements `pp` e `outsystems` em paralelo na mesma máquina sem switch context.

`/start <slug> [pack]` aceita o pack como arg (default: `pp`). `/resume` lê `_state.json.pack`.

### 10.6 Conteúdo da agent-memory (universal + tenant)

Cada folder de agente (`agent-memory/<universal-or-tenant>/<agent>/`) pode conter:

- **`universal-constraints.md`** (na `_universal/`; o equivalente tenant chama-se `recurring-constraints.md`) — constraints que aparecem em ≥2 engagements (universal: "RGPD afecta qualquer processo com PII"; tenant: "Galp usa SAP S/4HANA via OData").
- **`anti-patterns.md`** — falhas observadas (universal: "engagements Procurement sem CFO presente geram conflict user∧finance em 80% dos casos"; tenant: padrões específicos).
- **`corporate-patterns.md`** — padrões corporativos (só faz sentido em tenant: "Galp environment strategy DEV/UAT/PROD por BU").

A memória é editada pelos consultores entre engagements (não pelo LLM autonomamente). Cada agente carrega ambas as folders (universal + tenant) no início de cada ronda.

### 10.7 Versioning

- **Kernel version** em `library/kernel/orchestration.md` (semver).
- **Pack version** em `library/packs/<id>/pack.yaml`.
- **Skill versions** em frontmatter de cada SKILL.md.
- **Engagement state version** em `<slug>/_state.json.aisa_version` (regista qual versão do aisa correu este engagement — útil para repro/audit).
- **Não há "kernel breaks pack" porque o kernel não declara contratos rígidos sobre o pack** (vs aisa que tinha `kernel 2.7.0 deprecates X`).

### 10.8 Roadmap futuro de MCPs

Não MVP, mas planeado:
- **Jira / Azure DevOps** — pull de tickets de discovery.
- **SharePoint / OneDrive** — pull de documentos da engagement.
- **Microsoft Graph** — stakeholder enrichment (org chart).
- **PowerPlatform Admin API** — environment + licensing context.

Skill `aisa-start` aceita inputs locais em `projects/<slug>/inputs/` até MCP estar disponível.

### 10.9 Multi-language

Pack declara `language: pt | en | es`. Templates traduzidos por pack. Kernel é agnóstico (mensagens em inglês técnico). `library/packs/pp/` será pt; cópias `library/packs/pp-en/` podem ser produzidas.

---

## 11. Migração do aisa v1 (SPEA v2)

### 11.1 O que carrega para o aisa v2

- **Domain knowledge** (`powerfx-patterns.md`, `screen-patterns.md`, `security-patterns.md`, `delegation-matrix.md`) — copy-paste para `library/packs/pp/domain-knowledge/`. São o conteúdo de maior valor do aisa v1.
- **Deliverable templates** (`solution-blueprint.md`, `discovery-report.md`, etc.) — adaptados para `library/packs/pp/deliverable-templates/` com schema novo (slots em vez de claims).
- **Architecture templates** (`templates/architecture/*`) — copy-paste para `library/packs/pp/architecture-templates/`.
- **Question bank** — extrair das `cells/` (cada cell tem secções "questions to consider") e consolidar em `question-bank.md`.
- **Glossary** — extrair de `pack-drafts/pp-predev/glossary.md` (se existe) ou construir a partir do vocabulário usado.

### 11.2 O que não carrega

- Toda a estrutura `kernel/` (eventos, schemas, protocolos, coherence-cells, claim ledger, tags, modifiers).
- A pasta `cells/` per se — os conceitos viram lenses, mas o formato (frontmatter, execution steps, ledger) é re-escrito.
- A pasta `branches/` — decision-tree do pack é mais simples.
- `forensics/` — pode reaparecer como skill futura (não MVP).
- O conceito de "waves" — substituído por "rondas dentro de fases".

### 11.3 Conceitos novos sem equivalente no aisa v1

- **`_synthesis/` (topic packs)** — camada intermédia entre Decision e Render. Não tinha equivalente em aisa (o pp-consulting renderizava directamente das cells, o que causa inconsistências cross-deliverable). Skill nova: `aisa-synthesize`.
- **`lens-outputs/<lens>.md` (prose narrativa por lens)** — não tinha equivalente directo (aisa tinha "workbench.md" partilhada, sem segmentação por lens; cell outputs misturavam prose com Ledger).
- **Pack per-engagement** — aisa tinha pack global activo.
- **Repo split engagements + library** — aisa misturava tudo em `aisa-output/`.

### 11.3 Estratégia de cutover

1. **`aisa/` greenfield**, novo repositório. Não tocar no `aisa` actual.
2. **Build MVP** (ver §12).
3. **Validate** com 2-3 engagements em paralelo: v1-RUN-X vs v2-RUN-X com o mesmo input.
4. **Switch** quando o aisa v2 produzir ≥ qualidade do melhor-caso do v1 em ≥2 engagements consecutivos.
5. **Archive do aisa v1** para `archive/aisa-reference/`. Read-only.

---

## 12. Roadmap MVP

### Fase 0 — Spec & Alinhamento (1 semana)

- [ ] Este documento revisto e aceite pela equipa
- [ ] `docs/PHILOSOPHY.md` em prosa-de-empresa para sponsors externos
- [ ] `docs/MIGRATION_FROM_AISA.md` detalhado
- [ ] Decisão final sobre repo name + Git location

### Fase 1 — Skeleton (1-2 semanas)

- [ ] Scaffold `aisa/` com estrutura completa
- [ ] `library/kernel/{phases,states,orchestration,render-contract,glossary}.md`
- [ ] `.claude/settings.json` com deny rules e hooks pre-write-guard
- [ ] `.claude/rules/` (4 ficheiros curtos)
- [ ] `.claude/commands/{start,round,status,frame,options,decide,render}.md` (entry stubs)

### Fase 2 — Discovery loop (2-3 semanas)

- [ ] `.claude/skills/lens-{business,operations,user,data,governance,financial}/SKILL.md` (6 lenses — technology fica para Fase 3)
- [ ] `.claude/skills/aisa-start/SKILL.md` (captura + scaffold project)
- [ ] `.claude/skills/aisa-round/SKILL.md` (orquestra ronda em modo inline)
- [ ] `.claude/skills/aisa-status/SKILL.md`
- [ ] `.claude/skills/contradiction-scan/SKILL.md`
- [ ] `library/packs/pp/{pack.yaml, glossary.md, question-bank.md, lenses-config.yaml}`
- [ ] Validação: corre Discovery end-to-end num engagement de teste; produz SU em `_state: phase=discovery_complete`

### Fase 3 — Framing + Options + Decision (2-3 semanas)

- [ ] `.claude/skills/lens-technology/SKILL.md`
- [ ] `.claude/skills/chairman-synthesis/SKILL.md`
- [ ] `.claude/agents/{business-analyst,operations-lead,user-advocate,data-steward,solution-architect,compliance-officer,cfo-lens,chairman}.md`
- [ ] `.claude/skills/aisa-{frame,options,decide}/SKILL.md` — `/decide` auto-corre `/synthesize` no fim
- [ ] `library/packs/pp/decision-tree.md`
- [ ] **Validar concorrência**: subagentes em paralelo via Task tool funcionam como esperado (isolation real, sem race conditions, chairman recebe outputs todos)
- [ ] Validação end-to-end: corre Framing→Decision em modo council-independent

### Fase 3.5 — Synthesis layer (1 semana)

- [ ] `library/kernel/synthesis-templates/{business-story,as-is,architecture-story,risks-and-assumptions,financial-story}.template.md`
- [ ] `.claude/skills/aisa-synthesize/SKILL.md`
- [ ] `.claude/hooks/synthesis-validate.sh`
- [ ] Validação: após `/decide`, `_synthesis/` contém 5 topic packs preenchidos sem secções críticas vazias

### Fase 4 — Render (1-2 semanas)

- [ ] `library/packs/pp/deliverable-templates/` (6 templates — discovery, executive, blueprint, implementation-spec, claude-design-brief, estimate)
- [ ] `library/packs/pp/architecture-templates/` (4 sub-templates — canvas-only, model-driven, hybrid, dataverse-led)
- [ ] `library/packs/pp/domain-knowledge/` (4 ficheiros transplantados do aisa — powerfx-patterns, screen-patterns, security-patterns, delegation-matrix)
- [ ] `.claude/skills/aisa-render/SKILL.md` — lê de `_synthesis/` + `decisions.md`; versioning incremental (v01, v02, …)
- [ ] `.claude/hooks/render-validate.sh`
- [ ] Validação: corre `/render --all` e produz 6 outputs com 0 gaps em engagement de teste; re-render produz v02 sem sobrescrever v01

### Fase 5 — Enterprise readiness (1-2 semanas)

- [ ] `docs/ONBOARDING.md`, `docs/PACK_AUTHORING.md`, `docs/LENS_AUTHORING.md`, `docs/DELIVERABLE_AUTHORING.md`
- [ ] **Dual-repo bootstrap**: criar `aisa-engagements-galp/` (privado); documentar setup (symlink / env var) em `docs/ONBOARDING.md`
- [ ] **Agent-memory split**: `_universal/` populado com padrões genéricos; `_tenant/galp/` populado com aprendizagens proprietárias (recurring constraints, corporate patterns)
- [ ] `.env.example` para MCP credentials; `.mcp.json` com `${ENV_VAR}` placeholders
- [ ] Scaffold `library/packs/{outsystems,mendix,generic}/` com `pack.yaml` mínimo
- [ ] Pilot com a equipa: 2 consultores correm engagements paralelos (1 PP, 1 OS) na mesma máquina para validar pack per-engagement

### Critérios de sucesso MVP

- ✅ Dois runs com input idêntico produzem outputs semanticamente equivalentes (Não exigimos string-equal — exigimos: mesmas decisões, mesmas opções avaliadas, mesmas contradições detectadas, deliverables com mesmas conclusões).
- ✅ Engagement completo (start → 6 deliverables) em ≤4 dias úteis com 1 consultor.
- ✅ Os 6 deliverables são handoff-ready (developer / cliente / exec / designer leem-no e usam-no directamente).
- ✅ Zero "halt-and-confused" do LLM (não conformance issues estilo aisa v1).
- ✅ Equipa consegue autoring de novo pack ou lens em ≤1 dia após ler `docs/PACK_AUTHORING.md`.

### Risco principal

**Risco**: equipa habituada ao aisa v1 pode resistir ao "Shared Understanding como single artefacto" — esperam 5 docx desde o início.
**Mitigação**: `/status` mostra preview de cada deliverable a partir do SU em tempo real. Não esperam até `/render`.

---

## Apêndice A — Os 12 Passos Antes da Análise de Solução

Resposta à pergunta de partida que motivou o refactor:

> *"Assim que o negócio levanta uma necessidade, quais são os primeiros passos antes de começar a analisar uma solução para implementação com Power Platform?"*

| # | Passo | Lens responsável | Estado típico |
|---|---|---|---|
| 1 | **Captura literal do pedido** (verbatim, sem reformulação) | aisa-start (não-lens) | Confirmed |
| 2 | **Mapeamento do requester** (papel, autoridade, motivação não declarada) | business + aisa-start | Confirmed/Assumed |
| 3 | **Stakeholders sombra** (quem é afectado e não está na sala) | business | Assumed/Unknown |
| 4 | **As-is map** (real, não documentado; com saber tribal, exceptions) | operations | Confirmed/Assumed |
| 5 | **Histórico de tentativas anteriores** | operations + business | Confirmed/Unknown |
| 6 | **Constraints conhecidos** (regulatórios, licenciamento, arquitectura) | governance + financial + data | Confirmed |
| 7 | **Hipóteses não declaradas** (E5 license? SAP latency? sponsor avail?) | data + governance | Assumed/Risky |
| 8 | **Gaps de informação** (unknown-but-knowable vs unknown-unknowable) | gap-scan | Unknown |
| 9 | **Contradições internas no input** (mobile ∧ sensitive offline) | contradiction-scan | Conflicted |
| 10 | **Framing partilhado** (a frase única validada pelo sponsor) | chairman (Framing phase) | Confirmed |
| 11 | **Opções não-tecnológicas primeiro** (do nothing / process change / use existing) | technology + business + financial (Options) | — |
| 12 | **Critérios de fit definidos antes das opções** (criticality, lifetime, users, sensitivity, integration, governance maturity) | technology (Options) | — |
| 13 | **Decisão + justificação + alternativas + riscos + revisão** | solution-architect + sponsor | Confirmed (decisions.md) |

Passos 1-9 = Discovery phase. Passos 10 = Framing. Passos 11-12 = Options. Passo 13 = Decision.

Em nenhum momento a ferramenta sugere tecnologia antes do passo 11.

---

## Apêndice B — Glossário aisa v2 (vs aisa v1)

| Conceito aisa v2 | Substitui no aisa v1 | Diferença material |
|---|---|---|
| **Lens** | Cell | Stateless skill. Sem frontmatter mandatório. Sem ledger output. Sem peers gating. |
| **Ronda** | Wave | Iteração dentro de uma fase. Não tem consolidation gate. Múltiplas rondas dentro da mesma fase são normais. |
| **Fase** | (não tinha) | Discovery / Framing / Options / Decision. Tem entry/exit criteria mas são soft gates. |
| **Shared Understanding** | Claim Ledger + workbench | Markdown legível por humanos. 5 secções por estado. Append-by-default. |
| **Estado** (Confirmed/Assumed/Unknown/Conflicted/Risky) | State (OBSERVED/DERIVED/CONTESTED/SPECULATIVE) × Tag ([FACTO]/[HIPÓTESE]/...) | 5 estados ortogonais e human-readable, sem combinatorial explosion. |
| **Council híbrido** | Single-threaded inline + Task subagent prohibition | Modo declarado pela fase. Council-independent usa Task tool para isolar agentes. |
| **Chairman** | Coherence-cell | Sintetiza outputs de agentes independentes. Não tem lifecycle gate complexo. |
| **Library** | Skill/ | Read-only em runtime (hook-enforced). Sem outputs aqui. |
| **Pack** | Content-pack | Leve: glossary + question-bank + lenses-config + deliverable-templates. Não declara cells/waves/events. |
| **Render** | Wave-5 deliverable cells | Determinístico, lê SU+decisions, falha alto se gaps. Não inventa. |
| **Render-gaps.md** | (não tinha equivalente) | Output explícito quando deliverable não tem fonte completa no SU. Lista accionável. |
| **Soft gate** | (não tinha) | Warning advisory, overrideable com justificação registada. |
| **agent-memory** | (não tinha) | Memória institucional por agente, cresce com uso da equipa. |

---

## Apêndice C — Decisões Já Fechadas (sessão de 2026-05-27)

### Decisões fundacionais (v0.1.0)

1. ✅ **Greenfield, novo repo, novo nome** — abandonamos nomenclatura aisa/kernel/cell/wave.
2. ✅ **Shared Understanding como source-of-truth + deliverables renderizados** (refinado depois: os 6 deliverables são first-class).
3. ✅ **Power Platform first, agnóstico-by-design** — pp pack único validado; outros packs são scaffolds.
4. ✅ **Nome: `aisa`**.
5. ✅ **Council híbrido por fase** — inline em Discovery, council-independent em Framing+Options+Decision.
6. ✅ **4 fases explícitas com gates soft** — Discovery → Framing → Options → Decision, com override+justificação.
7. ✅ **Schema do SU: secções por estado + tabelas em markdown puro** — sem YAML frontmatter, sem JSON canónico.
8. ✅ **Pack PP lean**: glossary + question-bank + lenses-config (deliverable-templates adicionados quando 6-entregas viraram first-class).
9. ✅ **Escrever `docs/ARCHITECTURE.md` como próximo step** — feito.
10. ✅ **Adição posterior**: 6 entregas canónicas first-class (Discovery Report, Executive Report, Architecture Blueprint, Implementation Spec, Claude Design Brief, Estimate) — não render-on-demand opcional.

### Decisões da review pass (v0.2.0)

11. ✅ **Ordem fixa das lenses em Discovery inline**: `business → operations → user → data → governance → financial`. Sequencial determinada, previsível, debuggable.
12. ✅ **Council-independent corre em paralelo via concurrent Task subagents**. Máximo isolamento + desempenho. Chairman recebe outputs todos quando todos terminam.
13. ✅ **Peer review omitido no MVP**. Adicionar em v2 só se observarmos group-think em produção.
14. ✅ **Output dual de cada lens**: rows estruturadas no SU + `lens-outputs/<lens>.md` (prose narrativa). Slots de prose dos deliverables consomem dos summaries; estrutura tabular vem das rows.
15. ✅ **Camada `_synthesis/` entre Decision e Render**. Skill `aisa-synthesize` (auto-run no fim de `/decide`) produz 4-5 topic packs. Garante coerência cross-deliverable + determinismo do render.
16. ✅ **Engagements em repo privado separado** (`aisa-engagements-<tenant>/`). Agent-memory também split entre `_universal/` (partilhável) e `_tenant/` (proprietário). `.mcp.json` com `${ENV_VAR}` syntax + `.env.example`.
17. ✅ **Pack activo per-engagement** em `<slug>/_state.json.pack`. `library/packs/_active.txt` deprecated. Permite engagements PP + OS na mesma máquina sem context-switch.

---

## Apêndice D — Mapeamento Deliverables aisa v1 → aisa v2

Confirmação que o trabalho de templates do pp-consulting (v1) transita para o aisa v2 sem perda de fidelidade:

| aisa v1 output | aisa v2 deliverable | Mudanças necessárias |
|---|---|---|
| `outputs/discovery-report.md` | discovery-report (#1) | Slots equivalentes; remover Claim Ledger refs; adicionar SU-id refs |
| `outputs/executive-report.md` | executive-report (#2) | Adicionar `decision_options` slot (vinha de wave-4 architecture-branching, agora vem de Options phase) |
| `outputs/solution-blueprint.md` | solution-blueprint (#3) | Refactor `chosen_branch_template` para `chosen_architecture` (vem de decisions.md) |
| `outputs/design-spec.md` | claude-design-brief (#5) | Manter audience: claude-design; manter cross-refs a domain-knowledge; clarificar separation com implementation-spec |
| (não existe — novo) | implementation-spec (#4) | NOVO. Extrair de solution-blueprint + design-spec o que é "build instructions" pura. Schema novo. |
| `outputs/estimate.md` | estimate (#6) | Slots equivalentes; vem agora de Options phase (não wave-5 estimator-cell) |
| `domain-knowledge/powerfx-patterns.md` | (mesma) | Copy-paste. Conteúdo de altíssimo valor; não tocar. |
| `domain-knowledge/screen-patterns.md` | (mesma) | Copy-paste. |
| `domain-knowledge/security-patterns.md` | (mesma) | Copy-paste. |
| `templates/architecture/*.md` | architecture-templates/* | Copy-paste; ajustar slot names ao novo blueprint template. |

---

**FIM** — v2.1.0. Estado: MVP estrutural + next-level build feitos; próximo passo: pilot (Fase 12).
