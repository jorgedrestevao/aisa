# Migração de `aisa` para `aisa`

**Guia prático para quem usou aisa (SPEA v2) e vai usar aisa.**

> Versão: v0.1.0 — DRAFT para revisão da equipa
> Data: 2026-05-27
> Audiência: consultores Galp que correram engagements em aisa.
> Companion docs: [`ARCHITECTURE.md`](ARCHITECTURE.md), [`PHILOSOPHY.md`](PHILOSOPHY.md), [`ONBOARDING.md`](ONBOARDING.md).

---

## 1. Por que estamos a migrar

Resumo de 3 parágrafos. Para a fundamentação completa, ver [PHILOSOPHY.md](PHILOSOPHY.md) e [ARCHITECTURE.md §1.2](ARCHITECTURE.md).

**Razão técnica.** Dois runs do mesmo input no aisa (em 2026-05-27, ambos com `pp-predev v1.0.0` + `claude-sonnet-4-6`) produziram outputs significativamente divergentes e ambos com violações de protocolo. RUN-A teve 3 violações CRITICAL e 2 HIGH; RUN-B teve 2 violações MEDIUM. Ambos falharam ordem de eventos, granularidade de perguntas, gating de coherence-cells, ou frontmatter. O sintoma estrutural: o kernel exige ao LLM manter dezenas de invariantes em working memory simultânea; o LLM esquece um subconjunto diferente em cada run.

**Razão filosófica.** O aisa tenta forçar reasoning determinístico em cima de um modelo probabilístico. A `proposta_conceptual_operational_discovery` declara explicitamente o oposto: AI como **facilitador**, não árbitro determinístico. aisa adopta esta inversão.

**Razão operacional.** O aisa não segue a estrutura canónica de um projecto Claude Code (`.claude/skills/`, `.claude/agents/`, `.claude/hooks/`, `.claude/commands/`). Reimplementa runtime em markdown. aisa usa primitivas nativas de Claude Code, é partilhável como repositório standard, e é compatível com práticas enterprise (CI, code review, agent-memory tracked).

---

## 2. Vocabulary mapping

| aisa term | aisa term | Diferença material |
|---|---|---|
| `cell` | `lens` | Stateless skill. Sem frontmatter mandatório. Sem ledger output. Sem peers gating. Sem state machine própria. |
| `wave` | `ronda` | Iteração dentro de uma fase. Não há "wave consolidation". Múltiplas rondas dentro da mesma fase são normais. |
| `wave-plan.md` | (não existe) | Ordem das lenses é fixa em `phases.md` no kernel; pack não declara waves. |
| (não existia) | `fase` | Discovery / Framing / Options / Decision. Soft gates entre cada. |
| `Claim Ledger` | `shared-understanding.md` | Markdown legível por humanos, 5 secções por estado. Append-by-default. Sem tag matrix combinatória. |
| `OBSERVED / DERIVED / CONTESTED / SPECULATIVE` | `Confirmed / Assumed / Unknown / Conflicted / Risky` | 5 estados ortogonais e human-readable. Sem multiplicação por tags. |
| `[FACTO] / [HIPÓTESE] / [DOC-FACTO] / [DOC-HIPÓTESE]` | (eliminado) | Estado + lens já carrega o significado. Tags compostas são over-engineering. |
| `⚠️ confirmed-by-user` modifier | Linha no SU referencia o `answers.md` | Sem modifiers; rastreabilidade vem do council-log. |
| `coherence-cell` | `chairman-synthesis` + `contradiction-scan` (skill) | Síntese explícita pelo chairman em modo council-independent. Detection de contradição é skill standalone, não cell com lifecycle gate. |
| `kernel/` (eventos, schemas, protocolos) | `library/kernel/` (5 ficheiros markdown) | 5 ficheiros: `phases.md`, `states.md`, `orchestration.md`, `render-contract.md`, `glossary.md`. Sem sub-pastas. |
| `content-packs/<id>/` | `library/packs/<id>/` | Pack ainda existe, mas mais leve: sem cells/, sem branches/, sem fixtures/. |
| `_active.txt` (pack global) | `<slug>/_state.json.pack` | Pack activo per-engagement, não global. Permite engagements PP + OS em paralelo. |
| `aisa-output/<solution>_<stamp>/` | `aisa-engagements-<tenant>/<slug>/` | Engagements em repo privado separado por privacy. |
| `state.json` | `_state.json` (em cada engagement) | Igual em essência; outras keys (kernel→aisa_version, etc). |
| `workbench.md` (partilhado) | `lens-outputs/<lens>.md` (por lens) | Prose narrativa segmentada por lens. Synthesis consome estes. |
| `events.md` | `council-log.md` | Narrativa cronológica, não estritamente ordenada por kernel rules. Sem event-order invariants. |
| `cells/<cell>.md` | (não existe equivalente directo) | Lens não produz "cell output file". Produz: rows no SU + lens-outputs/<lens>.md + opcional pergunta. |
| `branches/` (decision tree barroca) | `library/packs/pp/decision-tree.md` (simples) | Único ficheiro markdown, consultado **só em Options**. |
| Wave-5 deliverable cells (estimator-cell, design-spec-cell, etc.) | `aisa-synthesize` + `aisa-render` (camadas separadas) | Synthesis (1 camada) → Render (6 deliverables). Cross-deliverable coherence garantida. |
| `forensics/` template + `_forensics/` | (não MVP) | Pode reaparecer como skill `aisa-forensics` em v2. |
| `errata-cell` (wave 6) | `/decide --revise` (futuro) | Re-decisões registadas no `decisions.md`; cascade automática não MVP. |

---

## 3. Workflow mapping

### aisa (SPEA v2) — 3 sessões, 6 waves

```
S1 (Discovery):    wave 1 → wave 2 → wave 3 → wave 4 → CP-A → CP-B
S2 (Build Spec):   wave 5 (parcial) → CP-C
S3 (Delivery):     wave 5 (resto) → 5 deliverables
S+1 (optional):    wave 6 errata
```

### aisa — 1 (ou 2) sessões, 4 fases

```
Discovery → Framing → Options → Decision → (auto) Synthesize → Render
   |__________ inline__________|  |______ council-independent ______|
```

**Mapeamento wave → fase:**

| aisa wave | aisa cells | aisa phase | aisa lenses/skills |
|---|---|---|---|
| 1 — Observed claims | intake, schema, document-scan, forensics, forensics-challenger | Discovery (aisa-start + 1ª ronda) | aisa-start + lens-business (inicialmente lê inputs) |
| 2 — Derived logic | formula, workflow, dependency, process, wave-2-coherence | Discovery (rondas 2-3) | lens-operations + lens-user |
| 3 — Transversal | governance, security, integration, contradiction, translator, ux | Discovery (rondas 4-6) | lens-data + lens-governance + lens-financial (+ contradiction-scan transversal) |
| 4 — Architecture branching | architecture-branching-cell + CP-A | Framing → Options | aisa-frame + aisa-options (com lens-technology pela 1ª vez) |
| 5 — Deliverables | design-spec, estimator, solution-blueprint, blueprint-verifier, discovery-report, executive-report | Decision → Synthesize → Render | aisa-decide → aisa-synthesize → aisa-render |
| 6 — Errata (opcional) | errata-cell | (futuro) /decide --revise | — |

---

## 4. Content carryover guide

O conteúdo de valor do aisa transita para aisa. Detalhe por ficheiro:

### 4.1 Copy-paste directos (zero refactor)

| aisa source | aisa destination | Notas |
|---|---|---|
| `skill/content-packs/pp-consulting/domain-knowledge/powerfx-patterns.md` | `library/packs/pp/domain-knowledge/powerfx-patterns.md` | Delegation matrix + 8 traps + validation sequence + standard patterns. Conteúdo mais valioso. |
| `skill/content-packs/pp-consulting/domain-knowledge/screen-patterns.md` | `library/packs/pp/domain-knowledge/screen-patterns.md` | 5 screen types, Fluent 2 palette, information density rules, approval state machine. |
| `skill/content-packs/pp-consulting/domain-knowledge/security-patterns.md` | `library/packs/pp/domain-knowledge/security-patterns.md` | RBAC symbols + 2-matrix template + Power FX security blocks + audit patterns. |
| `skill/content-packs/pp-consulting/domain-knowledge/delegation-matrix.md` (se existir) | `library/packs/pp/domain-knowledge/delegation-matrix.md` | Connector × operation × delegation. |
| `skill/content-packs/pp-consulting/templates/architecture/*.md` | `library/packs/pp/architecture-templates/*.md` | Manter os 3-4 templates de architectura PP (canvas-only, model-driven, hybrid, dataverse-led). |

### 4.2 Refactor leve (preservar conteúdo, adaptar schema)

| aisa source | aisa destination | Refactor necessário |
|---|---|---|
| `skill/content-packs/pp-consulting/outputs/discovery-report.md` | `library/packs/pp/deliverable-templates/discovery-report.template.md` | Slots equivalentes; remover refs a Claim Ledger; adicionar refs a topic packs (`_synthesis/business-story.md`, `_synthesis/as-is.md`). |
| `skill/content-packs/pp-consulting/outputs/executive-report.md` | `executive-report.template.md` | Adicionar slot `decision_options` (vem agora de Options phase). |
| `skill/content-packs/pp-consulting/outputs/solution-blueprint.md` | `solution-blueprint.template.md` | Refactor `chosen_branch_template` → `chosen_architecture` (vem de `decisions.md`). |
| `skill/content-packs/pp-consulting/outputs/design-spec.md` | `claude-design-brief.template.md` | Renomear (era `design-spec`, agora `claude-design-brief`). Manter audience: claude-design e cross-refs a domain-knowledge. |
| `skill/content-packs/pp-consulting/outputs/estimate.md` | `estimate.template.md` | Slots equivalentes. Vem agora de Options phase. |
| (novo) | `implementation-spec.template.md` | **DELIVERABLE NOVO.** Extrair de aisa-solution-blueprint o que é "build instructions" (entities, screens, flows, security, integrations, test scenarios, sequencing). |

### 4.3 Extrair de cells (consolidar em ficheiros novos)

| aisa source | aisa destination | Como extrair |
|---|---|---|
| Cell files com secções "Questions to consider" | `library/packs/pp/question-bank.md` | Grep secções "## Pending Questions" e "## Questions" nas cell files; consolidar 40-60 perguntas tipicamente úteis em PP. |
| Vocabulário usado nas cells (Dataverse, Dataflow, Premium connectors, etc.) | `library/packs/pp/glossary.md` | Grep termos PP-específicos; produzir glossário 1-2 páginas. |
| Pack-specific signals (ex: `licensing_baseline` em estimation) | `library/packs/pp/lenses-config.yaml` | Extrair `extra_signals` por lens a partir do que as cells procuram. |
| Decision-tree barroca em `branches/` | `library/packs/pp/decision-tree.md` | Simplificar para 1 árvore markdown: Canvas vs Model-driven vs Hybrid + critérios de escolha. |

### 4.4 Não carrega (deliberadamente)

- Toda a estrutura `skill/kernel/` (eventos, schemas YAML, protocolos, coherence-cells, claim-ledger spec, tag spec).
- A pasta `skill/content-packs/<id>/cells/` (24 cells em pp-consulting; conceitos viram lenses, formato é re-escrito).
- A pasta `skill/content-packs/<id>/branches/` (decision-tree barroca).
- A pasta `skill/content-packs/<id>/forensics/` (não MVP).
- A pasta `skill/content-packs/<id>/fixtures/` (regression suite específica de aisa; aisa terá fixtures novos).
- Os ficheiros `wave-plan.md`, `PACK_GUIDE.md`, `pack.yaml` antigo (formato novo em aisa).
- O conceito "kernel version × pack version compatibility matrix".
- Cells `errata-cell`, `forensics-cell`, `forensics-challenger`, `solution-blueprint-verifier`, `wave-2-coherence-cell`.

---

## 5. O que fazer com runs em curso no aisa

Casos típicos:

### 5.1 Run em discovery (wave 1-3)

**Acção**: completar em aisa.

**Razão**: investiu-se já tempo do sponsor; arrancar do zero em aisa custa mais que terminar. Runs em discovery costumam ser estáveis (poucas violações).

**Output**: deliverables aisa funcionam, ainda que o pipeline tenha drift.

### 5.2 Run em wave 4 (Architecture branching) ou início wave 5

**Acção**: **avaliar criticidade**.
- Se engagement de baixo risco/valor: completar em aisa.
- Se engagement crítico (sponsor exigente, deliverables vão ao cliente directamente): considerar **terminar manualmente** a partir do estado actual, sem rodar mais cells.

**Razão**: wave 4-5 cells (architecture-branching, design-spec, blueprint) são onde o aisa diverge mais entre runs. Mais risco aqui.

### 5.3 Run a iniciar (wave 1 não começou)

**Acção**: **adiar e correr em aisa** (se aisa MVP estiver disponível); senão correr em aisa com supervisão acrescida.

**Razão**: se não há sunk cost, vale a pena começar bem.

### 5.4 Errata pós-delivery

**Acção**: tratar manualmente (sem `errata-cell`).

**Razão**: aisa ainda não tem equivalente; aisa errata-cell é pouco usada.

---

## 6. Common gotchas

### 6.1 "Não há frontmatter? como sei se a lens correu?"

aisa não usa YAML frontmatter em outputs. A evidência de que uma lens correu é (a) rows novas no SU com `lens: <name>` na coluna; (b) novo append em `lens-outputs/<lens>.md`; (c) entrada no `council-log.md`. Read these instead.

### 6.2 "Onde está o Ledger?"

`shared-understanding.md` substitui. As 5 secções (Confirmed / Assumed / Unknown / Conflicted / Risky) tomam o lugar das colunas state × tag. Cada linha tem `id`, `lens`, `claim`, `evidência`, `ronda` — basicamente o mesmo de uma claim ledger row, mas legível e sem schema barroco.

### 6.3 "E os events.md? Como audito a ordem?"

`council-log.md` é narrativo, não estritamente ordenado por kernel rules. Não há `AGENT_DELEGATED → MODEL_TIER_MISMATCH` order invariant (essa é uma das coisas que o aisa nunca conseguiu manter consistente). O council-log conta a história em prose; basta isso para audit.

### 6.4 "Como detecto contradições sem coherence-cells?"

Skill `contradiction-scan` standalone. Corre quando:
- (a) O hook `on-su-change.sh` dispara depois de cada update do SU.
- (b) O utilizador corre `/contradiction-scan` manualmente.
- (c) Início da fase Framing (chairman roda como parte da synthesis).

Sem lifecycle gate complexo. Mais robusto.

### 6.5 "Onde escrevo a memória institucional?"

`.claude/agent-memory/_universal/<agent>/` para padrões partilháveis (RGPD aplica-se a qualquer PII; Procurement engagements sem CFO geram conflict).

`.claude/agent-memory/_tenant/<tenant>/<agent>/` para padrões proprietários (Galp usa SAP S/4HANA via OData; Galp environment strategy DEV/UAT/PROD por BU). Esta folder vive no repo privado `aisa-engagements-galp/` e é symlinkada/junctioned.

### 6.6 "Como faço debug se o LLM esquecer-se de algo?"

No aisa, debugging exigia ler events.md cronológico e detectar onde o invariante foi violado. Em aisa:
- `council-log.md` mostra narrativa por ronda.
- `lens-outputs/<lens>.md` mostra o que aquela lens disse.
- `shared-understanding.md` mostra o estado actual.
- `_state.json` mostra fase/ronda.

Se algo correu mal, é tipicamente porque (a) o SU está incompleto/inconsistente — corre /round outra vez para a lens em falta; (b) decisions.md falta um campo — corre /decide outra vez. Não há "pipeline broken; restart from wave X".

---

## 7. Timeline de migração sugerida

Assumindo que o build do aisa seguirá o roadmap em [`ARCHITECTURE.md §12`](ARCHITECTURE.md):

| Sem | O que fazer |
|---|---|
| **W1-W2** (build aisa Fase 0-1) | Não tocar em aisa engagements em curso. Equipa contribui review do `ARCHITECTURE.md`, `PHILOSOPHY.md`. |
| **W3-W5** (build aisa Fase 2-3.5) | Equipa começa a "ensaiar" — corre 1 engagement de teste em aisa MVP em paralelo com 1 em aisa. Comparar outputs. |
| **W6-W7** (build aisa Fase 4-5) | Renderizar deliverables em aisa; comparar com aisa. Iterar templates. |
| **W8** (validação) | 2 consultores correm engagements paralelos (1 PP, 1 OS) em aisa. Confirmar pack per-engagement, dual-repo, agent-memory split. |
| **W9** (cutover) | Novos engagements **arrancam em aisa**. Engagements aisa em curso (se ainda existirem) terminam em aisa. |
| **W10+** (manutenção) | Aisa fica em archive read-only. Issues que apareçam em produção aisa → fix incremental. |

---

## 8. Riscos da migração e mitigações

| Risco | Mitigação |
|---|---|
| Equipa habituada ao Ledger/cells resiste ao SU em 5 estados | Workshop de 1h no início da W3; demonstrar com engagement real |
| Templates aisa têm slots que aisa synthesis não preenche | Iterar templates em W6-W7; render-gaps.md sinaliza problemas |
| Algum engagement aisa em curso precisa de re-correr em aisa | Avaliar caso-a-caso (ver §5); preferir terminar em aisa se já investido |
| Dual-repo confuso para consultores | Onboarding W8 documenta setup; bootstrap script automatizado |
| Pack per-engagement quebra fluxos antigos | Não há fluxo automatizado a quebrar; é melhoria pura |
| Domain-knowledge não trans-pasted correctamente | Validar com diff explícito vs aisa antes de cutover |

---

## 9. Quando NÃO migrar

Casos em que continuar em aisa pode ser razoável (por agora):

- **Engagements de auditoria forense pesada** — aisa tem `forensics-cell` mature; aisa v1 não terá equivalente. Esperar v2.
- **Engagements onde o cliente exige o pipeline aisa exacto** (improvável, mas se existir).
- **Estudo/research interno sobre comportamento de LLM em pipelines** — aisa é o sujeito-de-estudo; aisa é a alternativa proposta.

---

**Para detalhe técnico → [`ARCHITECTURE.md`](ARCHITECTURE.md).**
**Para fundamentação filosófica → [`PHILOSOPHY.md`](PHILOSOPHY.md).**
**Para setup prático → [`ONBOARDING.md`](ONBOARDING.md).**
