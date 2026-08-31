# Proposta — Camada UX Blueprint (raciocínio de design entre Decision e Render)

> Data: 2026-08-31
> Estado: **proposta** para revisão — não implementado
> Origem: brainstorm sobre a quebra de contexto entre conhecimento de domínio extraído e a representação visual que o negócio valida ("Business Domain ≠ UI Specification")
> Companion: `docs/GAP_ANALYSIS.md` (o loop `/answer` referido abaixo é o achado G-03)

---

## 1. O problema, no aisa concreto

O pipeline atual termina em 6 documentos. O `claude-design-brief` (deliverable #5) é o input para geração de protótipos, mas os seus slots resolvem de **narrativas de síntese**:

| Slot do design brief hoje | Fonte atual | Problema |
|---|---|---|
| `canvas_app_pages` | `_synthesis/architecture-story.md# Platform and components` | Componentes ≠ ecrãs. Ninguém decidiu a arquitectura de ecrãs |
| `page_navigation_map` | `_synthesis/as-is.md# End-to-end process today` | Navegação inferida do processo as-is — heurística, não desenho |
| `ux_requirements` | `_synthesis/as-is.md# Top friction points` | Dores ≠ hierarquia de informação, agrupamento de campos, ações primárias |

Ou seja: o aisa hoje faz `Requirements → Claude Design → Protótipo` sem a camada que **decide** o design. O sintoma downstream: protótipos que o negócio não reconhece como "a minha futura aplicação".

O paradoxo: **o conhecimento para essa camada já está no pack** e não tem executor:

- `domain-knowledge/screen-consolidation-rules.md` — a árvore de decisão campo-inventário → plano de ecrãs (contagem de campos editáveis → form/wizard/tabs; separação de roles → split de ecrãs; aprovação = ação no form, **não** ecrã; hard caps de 12 campos/5 ações com violação = Conflicted row). O próprio ficheiro diz "apply after the architectural branch is chosen and before the implementation-spec is written" — **nenhuma skill o aplica**.
- `domain-knowledge/screen-patterns.md` — catálogo dos 5 tipos de ecrã, densidade de informação, paleta de status, e **Excel Familiar Anchors** (o conhecimento "spreadsheet-to-app" — que ordem de colunas os utilizadores esperam, que âncoras visuais preservar).
- `domain-knowledge/security-patterns.md` — RBAC matriz ecrã × entidade×CRUD (visibilidade por role é decisão de design).
- `domain-knowledge/delegation-matrix.md` — volume por entidade → estratégia de gallery/pesquisa (constraint de plataforma que condiciona o design de listas).

Os "Agent 1/Excel Archaeologist" e "Agent 2/Domain Architect" do brainstorm **já existem**: são o protocolo *Reading input documents* do kernel (profiling de sheets, colunas, fórmulas, distribuições) + a lens-data (entidades, owners, relações, sensibilidade). O que falta é o **Agent 3 — UX Architect** e o artefacto estruturado que ele produz.

---

## 2. Decisão de desenho: onde encaixa (e onde não encaixa)

**Não é uma nova fase do kernel.** As 4 fases mantêm-se. O blueprint é iteração **dentro da fase Decision** — o kernel já abençoa "múltiplas rondas dentro da mesma fase". Razões:

1. O blueprint precisa da decisão tomada: o branch arquitectural (sharepoint-first / dataverse-first / hybrid) muda a arquitectura de ecrãs, e as consolidation-rules exigem branch escolhido.
2. A validação do protótipo pelo negócio é um refinamento da decisão, não uma fase nova — usa a maquinaria existente (SU append-only, D-NNN, re-synthesize, re-render versionado).
3. Pipeline leve: 1 skill nova + 1 comando + 1 contrato + re-sourcing de 2 templates. Zero invariantes novos.

O pipeline completo passa a ser:

```
necessidade → /start → Discovery (/round × N + resolução de Unknowns) → /frame → /options → /decide
                                                                                       │
                                                                             (auto) /synthesize
                                                                                       │
                                                                  NOVO  /blueprint  ← UX Architect
                                                                                       │
                                                                    _blueprint/ux-blueprint_v01.yaml
                                                                                       │
                                                geração do protótipo (Claude Design / externo) a partir do blueprint
                                                                                       │
                                              validação com o negócio → feedback entra no SU (rows com ids)
                                                                                       │
                                                    aprovação → D-NNN "Blueprint v<NN> aprovado"
                                                                                       │
                                                        /synthesize (refresh) → /render --all
                                        (claude-design-brief e implementation-spec passam a citar o blueprint aprovado)
```

Separa exatamente as duas coisas que o brainstorm distingue: **decidir o design** (`/blueprint`, dentro do aisa, auditável, com proveniência) vs **renderizar o design** (Claude Design ou qualquer motor futuro, fora do aisa, substituível).

---

## 3. O contrato — `ux-blueprint.yaml`

Resposta à pergunta "que informação exatamente o Claude Design precisa de receber?". O schema é **agnóstico de plataforma** (candidato a `library/kernel/blueprint-contract.md`); os valores vêm do pack (tipos de ecrã, naming, caps) e do SU (conteúdo). Três propriedades não-negociáveis:

1. **Proveniência em todos os nós** — cada ecrã, campo, ação e exclusão carrega `su_refs`. "Que requisito originou este campo?" torna-se query mecânica, e o diff protótipo-aprovado ↔ implementação fica possível a jusante.
2. **Secção `excluded_from_ui`** — o que vem do Excel e **não** deve aparecer, com razão e id. (A pergunta "que informação vem do Excel mas não deve aparecer ao utilizador?" é uma decisão de design de primeira classe, não uma omissão.)
3. **Validação embutida** — os hard caps das consolidation-rules são verificados sobre o próprio blueprint; violação gera Conflicted row no SU (mecânica já existente), não prosa.

```yaml
blueprint_id: bp-v01
engagement: <slug>
concretizes_decision: D-002        # a decisão que este blueprint torna visível
branch: dataverse-first            # de decisions.md — condiciona padrões de ecrã
app:
  name: Pricing Management
  device_targets: [desktop, tablet]     # su_refs: [C-018]
  language: pt

personas:                          # de SU lens=user + security-patterns
  - id: pricing-analyst
    label: Pricing Analyst
    rbac_group: Analysts           # liga à matriz RBAC do pack
    su_refs: [C-011, C-012]

entities:                          # compilado de SU lens=data (o "domain model" explícito)
  - name: PricingRequest
    volume_expected: "4700/ano; pico 120/dia"   # → estratégia de delegation/gallery
    state_machine: [Draft, Submitted, Approved, Rejected]
    su_refs: [C-021, A-005, R-002]

navigation:
  home_per_persona: { pricing-analyst: PricingRequestListScreen, pricing-manager: DashboardScreen }
  map:
    PricingRequestListScreen: [PricingRequestFormScreen]
    PricingRequestFormScreen: [PricingRequestListScreen]

screens:                           # output da árvore screen-consolidation-rules
  - name: PricingRequestListScreen           # naming convention do pack
    pattern: List                            # 1 dos 5 tipos do catálogo screen-patterns
    purpose: "Analista encontra, filtra e abre pedidos de pricing."
    primary_persona: pricing-analyst
    density: HIGH                            # screen-patterns § Information Density
    data:
      entity: PricingRequest
      columns_primary: [Status, Customer, RequestedPrice]     # hierarquia de informação
      columns_secondary: [CreatedDate, LastUpdated]
      delegation_note: "volume > 5k/ano → filtro server-side; ver delegation-matrix"
    actions:
      primary: [CreateRequest]               # cap: 5 ações (primárias visíveis + overflow)
      secondary: [DuplicateRequest, ExportList]
    rbac_visibility: { pricing-analyst: full, pricing-manager: read }
    ui_states: [loading, empty, error]       # estados obrigatórios, não opcionais
    excel_anchor: "Sheet 'Pending' — preservar ordem de colunas que a equipa usa há 10 anos"
    su_refs: [C-002, C-014, U-007]
  - name: PricingRequestFormScreen
    pattern: Form
    sections: [General, Customer, ProductLines, Calculation, Approval, History]   # agrupamento de campos
    approval: { as: actions-on-form, transitions: state_machine }   # regra: aprovação ≠ ecrã
    editable_fields_visible: 11              # cap ≤ 12 — verificado
    su_refs: [C-005, X-001]

excluded_from_ui:                  # decisões explícitas de NÃO mostrar
  - field: CostMarginRaw
    reason: "sensível — visível apenas a manager, e só agregado"
    su_refs: [X-003, C-030]

open_questions:                    # Unknowns que bloqueiam design (não inventar)
  - U-012                          # "logo oficial e paleta de brand?"

validation:
  consolidation_caps: pass         # ≤3 entidades/ecrã, ≤12 campos, ≤5 ações
  violations: []                   # cada violação vira Conflicted row no SU
```

Regra de ouro (herdada da filosofia do aisa): **o blueprint não inventa** — cada nó ancora em ids do SU; o que não tem fonte vira `open_questions`, nunca default silencioso.

---

## 4. O loop de validação (o protótipo como especificação executável)

Usa maquinaria existente — nada de novo além do hábito:

1. `/blueprint` produz `_blueprint/ux-blueprint_v01.yaml` (+ `blueprint-log.md`, versionamento append-only como o `_render/`).
2. O protótipo é gerado **fora** do aisa a partir do blueprint (Claude Design hoje; qualquer motor amanhã — o blueprint é o contrato, o renderer é substituível).
3. A sessão de validação com o negócio produz feedback que entra no SU como rows (`Confirmed` "negócio validou ecrã X", `Conflicted` "negócio quer Y, governança impede", evidência = sessão + screenshot em `_blueprint/feedback/`). Mesmo mecanismo dos answers de Discovery — o que reforça a prioridade do G-03 (`/answer`): **o mesmo loop serve respostas de Discovery e feedback de protótipo**.
4. Iteração: `/blueprint` de novo → `v02` (o feedback está no SU, o blueprint novo cita os ids novos).
5. Aprovação: linha `D-NNN — Blueprint bp-v02 aprovado pelo sponsor` em `decisions.md` (+ row no SU).
6. `/synthesize` refresca; `/render --all` produz os documentos finais — que agora citam um blueprint **aprovado pelo negócio**, não uma projeção de narrativas.

Fecho do ciclo a jusante (fora do âmbito desta proposta, mas o blueprint prepara-o): "identifica diferenças entre o protótipo aprovado e a implementação" = diff mecânico entre `ux-blueprint_v<aprovado>.yaml` e um scan da solution Power Platform — possível porque ambos partilham os mesmos ids.

---

## 5. Alterações concretas (quando aprovado)

| # | Ficheiro | Alteração |
|---|---|---|
| 1 | `.claude/skills/aisa-blueprint/SKILL.md` | **Novo.** O UX Architect: lê SU (lens=user/data/operations/governance), `frame.md`, `decisions.md` (branch), lens-outputs, e domain-knowledge do pack (consolidation-rules como procedimento, screen-patterns como catálogo, security-patterns para RBAC, delegation-matrix para constraints). Executa a árvore de consolidação, produz o YAML versionado, verifica caps, emite Conflicted/Unknown rows quando aplicável. Inline (não council) — é pós-decisão e determinístico dado o SU |
| 2 | `.claude/commands/blueprint.md` | **Novo.** Thin pointer, `argument-hint: "[--option O-NNN] [--refresh]"` (`--option` permite blueprint exploratório da opção líder ainda em Options, marcado draft) |
| 3 | `library/kernel/blueprint-contract.md` | **Novo.** O schema da §3 (agnóstico de plataforma) + regras do loop de validação. Edição administrativa via git (library/ é enforce) |
| 4 | `library/kernel/render-contract.md` | Pipeline atualizado: Decision → Blueprint → Validação → Synthesize → Render |
| 5 | `library/kernel/phases.md` | Fase Decision: outputs + exit criteria soft ganham "blueprint aprovado (D-NNN)" **quando o engagement tem componente UI** (soft — engagements sem UI, ex. só automação, saltam) |
| 6 | `deliverable-templates/claude-design-brief.template.md` | Re-sourcing: `canvas_app_pages` ← `_blueprint/…# screens`, `page_navigation_map` ← `# navigation`, `ux_requirements` ← `# screens.purpose + excluded_from_ui`; novo required slot `approved_blueprint` (D-NNN ref). O brief passa a ser a **projeção legível** do blueprint |
| 7 | `deliverable-templates/implementation-spec.template.md` | `screens_to_build` ← blueprint aprovado (garante: o que se constrói = o que o negócio validou) |
| 8 | `CLAUDE.md` + `docs/ONBOARDING.md` | `/blueprint` na tabela de comandos; passo 8b no walkthrough |

Esforço estimado: 1–2 sessões de build. Dependência recomendada: implementar primeiro o `/answer` (G-03), porque o loop de feedback do protótipo o reutiliza.

## 6. O que fica explicitamente fora (para manter a pipeline leve)

- **Geração do protótipo** — fora do aisa. O blueprint é o contrato; o renderer (Claude Design, Figma AI, futuro) é substituível.
- **Nova fase no kernel** — rejeitado; iteração dentro de Decision.
- **Peer review / council no blueprint** — o UX Architect corre inline; se surgir group-think em produção, aplica-se a mesma regra do kernel (adicionar isolamento só com evidência).
- **Diff blueprint ↔ solution implementada** — próxima evolução (exige o carimbo de ids nos artefactos Power Platform via MCP de authoring); esta proposta apenas garante que os ids existem para o tornar possível.
