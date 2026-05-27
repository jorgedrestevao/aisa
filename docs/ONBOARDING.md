# aisa — Onboarding

**Setup + primeira engagement, do zero ao /render --all em 1-2 horas.**

> Versão: v0.1.0 — DRAFT
> Data: 2026-05-27
> Audiência: novo consultor (ou desenvolvedor) a usar aisa pela primeira vez.
> Companion docs: [`ARCHITECTURE.md`](ARCHITECTURE.md), [`PHILOSOPHY.md`](PHILOSOPHY.md), [`MIGRATION_FROM_AISA.md`](MIGRATION_FROM_AISA.md).

---

## 1. Antes de começar

### 1.1 Pré-requisitos

- **Claude Code instalado** (CLI, VS Code extension, ou desktop app). Verificar: `claude --version`.
- **Git** instalado. Verificar: `git --version`.
- **Python 3.10+** ou PowerShell 5.1+ (depende do OS).
- **Pandoc** (para conversão markdown → docx). Opcional para MVP; necessário para `/render` em formato docx.
- **Acesso ao grupo Galp** que dá acesso ao repositório privado `aisa-engagements-galp`.

### 1.2 Mental model em 60 segundos

aisa tem 2 repositórios + 1 sistema de fases:

```
┌─────────────────────────────────────────────────────────────────┐
│ REPO 1: aisa/  (público dentro da empresa)                    │
│   ├── .claude/skills/      ← lenses, commands, synthesis        │
│   ├── .claude/agents/      ← personas para council              │
│   ├── library/kernel/      ← fases, estados, render contract    │
│   ├── library/packs/pp/    ← templates, glossary, q-bank        │
│   └── projects/            ← MOUNT POINT → repo 2               │
└─────────────────────────────────────────────────────────────────┘
                              ↓ symlink/junction
┌─────────────────────────────────────────────────────────────────┐
│ REPO 2: aisa-engagements-galp/  (privado, encrypted)          │
│   ├── galp-adv/             ← engagement 1                      │
│   │   ├── _state.json       ← phase + round + pack              │
│   │   ├── shared-understanding.md  ← ARTEFACTO VIVO             │
│   │   ├── lens-outputs/     ← prose por lens                    │
│   │   ├── _synthesis/       ← topic packs (auto)                │
│   │   ├── _render/          ← 6 deliverables (v01, v02, ...)    │
│   │   └── ...                                                   │
│   └── galp-procurement/     ← engagement 2 (em paralelo)        │
└─────────────────────────────────────────────────────────────────┘
```

Fluxo de uma engagement: `Discovery → Framing → Options → Decision → (auto) Synthesize → Render`.

---

## 2. Instalação

### 2.1 Clonar os 2 repositórios

```powershell
# Numa folder de trabalho:
cd C:\Users\<you>\Documents\Galp\
git clone <aisa-repo-url> aisa
git clone <aisa-engagements-galp-url> aisa-engagements-galp
```

> **Se ainda não existe `aisa-engagements-galp` no Git da Galp**: criar repo privado novo. É vazio inicialmente; será preenchido pelo `/start` de cada engagement. Falar com o admin de DevOps para criar com permissões restritas.

### 2.2 Configurar o mount point (`aisa/projects/`)

**Opção A — Junction (Windows recomendado):**

```powershell
cd C:\Users\<you>\Documents\Galp\aisa
# Se já existe projects/ vazio, remover primeiro:
Remove-Item projects -ErrorAction SilentlyContinue
# Criar junction para o repo 2:
cmd /c "mklink /J projects ..\aisa-engagements-galp"
```

**Opção B — Symlink (Unix-like):**

```bash
cd ~/Galp/aisa
rm -rf projects 2>/dev/null
ln -s ../aisa-engagements-galp projects
```

**Opção C — Variável de ambiente (cross-platform, mais explícito):**

```powershell
# Em $PROFILE (PowerShell profile):
$env:AISA_ENGAGEMENTS_ROOT = "C:\Users\<you>\Documents\Galp\aisa-engagements-galp"
```

As skills do aisa lêem `AISA_ENGAGEMENTS_ROOT` primeiro; cai para `aisa/projects/` se não definido.

### 2.3 Configurar variáveis de ambiente (MCP, se necessário)

```powershell
cd aisa
cp .env.example .env
# Editar .env e preencher valores (SHAREPOINT_TENANT_ID, etc.).
# .env está gitignored; nunca o committar.
```

Se MCP não está a ser usado (não MVP), pode-se ignorar este passo.

### 2.4 Verificar que tudo está pronto

```powershell
cd aisa
# Open in Claude Code:
claude .
```

No Claude Code, executar:

```
/aisa-status --check
```

Output esperado:

```
✓ aisa/ repo: OK (kernel v0.1.0)
✓ aisa-engagements-galp/ mount: OK (0 engagements)
✓ active pack: none (definido per-engagement em /start)
✓ MCP servers: 0 configured (não MVP)
✓ ready.
```

Se falha:
- `aisa/ repo: FAIL` → não estás no directório `aisa/`.
- `aisa-engagements-galp/ mount: FAIL` → junction/symlink/env var não configurados (rever §2.2).

---

## 3. A tua primeira engagement (walkthrough)

Vamos correr uma engagement de teste do princípio ao fim, em `~1 hora`. Cenário fictício mas representativo.

### 3.1 Cenário

> *"O director de Procurement, António Silva, pediu para 'digitalizar a aprovação de adiantamentos a fornecedores'. Hoje usam Excel + Outlook. 47 aprovações/mês. Querem mobile + aprovações multi-nível. Reunião inicial de 30 min foi tudo o que sabemos."*

Inputs iniciais que temos:
- 1 ficheiro Excel anonimizado do processo actual: `Dayly_pending_tickets_Anonimo.xlsx`.
- Notas da reunião inicial (1 página).
- Não temos acesso ainda a outros stakeholders.

### 3.2 Passo 1 — `/start`

```
/start galp-adv pp
```

O `aisa-start` vai:
1. Criar a folder `aisa-engagements-galp/galp-adv/`.
2. Pedir-te (interactivamente) os 3 inputs iniciais:
   - "Cola o pedido literal (verbatim da reunião)" → tu colas.
   - "Quem é o requester? Papel, autoridade." → "António Silva, Director Procurement, autoridade orçamento até €500k".
   - "Há documentos para o discovery? Mete em `inputs/`." → tu copias o `.xlsx` + notas.
3. Criar o `shared-understanding.md` skeleton.
4. Criar o `_state.json`:
   ```json
   {
     "engagement": "galp-adv",
     "pack": "pp",
     "phase": "discovery",
     "round": "R-01",
     "aisa_version": "0.1.0",
     "created": "2026-05-27T14:00:00Z"
   }
   ```
5. Output esperado:
   > `Engagement galp-adv criado. Phase: discovery. Próximo passo: /round (corre Discovery completo) ou /round business (lens-a-lens).`

### 3.3 Passo 2 — `/round` (Discovery completo)

```
/round
```

O `aisa-round` em Discovery corre as 6 lenses **sequencialmente** na ordem fixa (business → operations → user → data → governance → financial). Em modo `inline`, cada lens vê o que as anteriores escreveram.

Cada lens:
1. Lê `context.json` + `shared-understanding.md` + `lens-outputs/` anteriores (se existirem).
2. Identifica sinais relevantes para a sua perspectiva.
3. Adiciona rows ao SU (cada uma com id, estado, evidência).
4. Escreve 1-3 parágrafos em `lens-outputs/<lens>.md`.
5. Se há gap, emite Pending Question em `## Unknown`.

Output esperado (~ 5-10 min):

> *"Ronda R-01 completa. SU populado: 12 Confirmed, 8 Assumed, 14 Unknown, 1 Conflicted, 2 Risky. Próximo passo: /status para ver detalhe; ou /round para nova ronda; ou responder a Unknowns para promover a Confirmed."*

### 3.4 Passo 3 — `/status`

```
/status
```

Output:

```
Engagement: galp-adv
Phase: discovery
Round: R-01

Shared Understanding:
  ## Confirmed (12)
    C-001 — Sponsor é António Silva, Director Procurement (lens: business)
    C-002 — Processo actual: Excel + Outlook, 47 aprovações/mês (lens: operations)
    ...
  ## Assumed (8)
    A-001 — Tenant Galp tem E5 licensing (lens: technology) [⚠️ confirmar]
    ...
  ## Unknown (14, 3 Critical):
    U-001 — Quem mais aprova além do director? (lens: business) [Critical]
    U-002 — Há mobile na infra hoje? (lens: technology) [Critical]
    U-003 — Tempo médio actual end-to-end de uma aprovação? (lens: operations) [Critical]
    ...
  ## Conflicted (1, 1 Critical):
    X-001 — Sponsor diz "aprovação multi-nível"; nota de reunião diz "1-step" (lens: business)
  ## Risky (2):
    R-001 — Aprovações de pico (fim de mês) podem ser >120/dia (lens: operations)
    ...

Next suggested action:
  → Resolve 3 Critical Unknowns + 1 Critical Conflicted with sponsor antes de /frame
```

### 3.5 Passo 4 — Resolver Unknowns + Conflicted com sponsor

Em reunião com sponsor (ou async), resolves os 4 críticos. Voltas e fazes append em `answers.md`:

```
/answer U-001 "Para >€10k, aprova Director + Finance Manager. Para <€10k, só Director."
/answer U-002 "Mobile suportado via Intune wrap; offline NÃO permitido para dados procurement (sensíveis)."
/answer U-003 "Hoje: 3.5 dias úteis. Objectivo: 1 dia útil."
/answer X-001 "Multi-nível para >€10k. 1-step para <€10k. Notas estavam erradas."
```

O `/answer` actualiza o SU: linhas U-001..U-003 transitam de Unknown → Confirmed (com `was U-NNN`); linha X-001 sai de Conflicted e cria 2 Confirmed (uma por banda).

### 3.6 Passo 5 — `/round` (segunda ronda Discovery se necessário)

```
/round
```

A segunda ronda explora gaps remanescentes; pode emitir novos Unknowns que dependiam dos primeiros (ex: agora que sabemos da regra €10k, lens-governance pergunta "qual o limite para audit trail mandatório?").

Iterar /round + /answer até `/status` mostrar:

```
## Unknown (2 Critical): 0
## Conflicted (1 Critical): 0
```

Tipicamente 2-4 rondas de discovery são suficientes.

### 3.7 Passo 6 — `/frame`

```
/frame
```

Transita de `phase: discovery` → `phase: framing`. Activa modo `council-independent`.

Os 6 agentes (business-analyst, operations-lead, user-advocate, data-steward, compliance-officer, cfo-lens) correm **em paralelo via Task subagents**, cada um vê só `context.json` + extracto temático do SU.

Cada agente propõe a "frase única" da sua perspectiva. O `chairman` lê os 6 outputs e sintetiza uma única frase.

Output esperado:

> *"Framing proposto: 'O problema é o tempo de aprovação de adiantamentos a fornecedores (média 3.5 dias úteis, objectivo 1 dia), sentido pelas equipas operacionais Procurement (n=12) e pelos fornecedores afectados, hoje custa atraso operacional e cobranças tardias com impacto na liquidez, e a evidência é o registo de Excel actual + sponsor reporting.' Confirmas? (y/n/edit)"*

Tu validas ou editas. Validação fica registada em `decisions.md` (D-001).

### 3.8 Passo 7 — `/options`

```
/options
```

Transita para `phase: options`. **lens-technology entra pela primeira vez.**

Os 7 agentes (agora incluindo solution-architect / lens-technology) correm em paralelo. Cada um propõe opções da sua perspectiva. Chairman sintetiza ~4 opções:

1. **Não fazer nada** — manter Excel + Outlook. Custo: 3.5 dias × 47 aprov/mês = ineficiência. Risco: baixo. Investment: 0€.
2. **Mudar o processo sem tecnologia** — eliminar 1 step de validação manual via mudança de policy. Custo: 1h training × 12 pessoas. Risco: baixo. Investment: ~500€.
3. **Power Platform Premium (Canvas + Power Automate + Dataverse)** — automação full, mobile, audit. Custo: ~60 dias dev + Premium licenses. Risco: médio (integração SAP). Investment: ~80k€.
4. **OutSystems** — alternativa enterprise. Custo: ~50 dias dev. Investment: ~100k€ (licensing + dev).

Cada opção vem com prós, contras, e referências aos constraints do SU (ex: opção 3 referencia A-001 "tenant tem E5" como pre-requisito a confirmar).

### 3.9 Passo 8 — `/decide`

```
/decide
```

O sistema pede:
1. Qual opção escolhes? → "3 (PP Premium)".
2. Justificação? → "Permite mobile + audit + escala. OutSystems mais caro sem ganho diferencial. Process change apenas é insuficiente para mobile."
3. Alternativas consideradas? → (preenchidas automaticamente das opções).
4. Riscos aceites? → "Integração SAP latency (R-001); migração Excel histórico não incluída."
5. Condições de revisão? → "Re-avaliar em 6 meses se >20% de aprovações foram fora do app."

Tudo registado em `decisions.md` (D-002).

**Auto-corre `/synthesize` no fim** → produz 5 topic packs em `_synthesis/`:
- `business-story.md`
- `as-is.md`
- `architecture-story.md`
- `risks-and-assumptions.md`
- `financial-story.md`

### 3.10 Passo 9 — `/render --all`

```
/render --all
```

Lê `_synthesis/` + `decisions.md` + templates de `library/packs/pp/deliverable-templates/`. Produz em `_render/`:

```
galp-adv_discovery-report_v01.docx        (cliente)
galp-adv_executive-report_v01.docx        (C-suite)
galp-adv_solution-blueprint_v01.docx      (technical leadership)
galp-adv_implementation-spec_v01.md       (PP maker)
galp-adv_claude-design-brief_v01.md       (Claude Design)
galp-adv_estimate_v01.docx                (sponsor + procurement)
render-gaps.md                            (warnings se algum slot ficou vazio)
```

Se `render-gaps.md` está vazio → tudo OK. Se tem entradas → render-validate sinaliza qual slot/topic precisa de mais conteúdo; tu corres /round ou /answer adicional, depois /synthesize + /render outra vez (produz v02).

---

## 4. Onde as coisas vivem (quick reference)

| Procurar... | Está em... |
|---|---|
| Slash commands disponíveis | `.claude/commands/*.md` |
| O que cada lens faz | `.claude/skills/lens-<name>/SKILL.md` |
| Personas dos agentes (council mode) | `.claude/agents/*.md` |
| As 4 fases + entry/exit | `library/kernel/phases.md` |
| Os 5 estados + rules | `library/kernel/states.md` |
| Templates de deliverables | `library/packs/pp/deliverable-templates/*.template.md` |
| Templates de synthesis | `library/kernel/synthesis-templates/*.template.md` |
| Domain knowledge PP | `library/packs/pp/domain-knowledge/*.md` |
| Question bank PP | `library/packs/pp/question-bank.md` |
| Glossário PP | `library/packs/pp/glossary.md` |
| Memória institucional (compartilhada) | `.claude/agent-memory/_universal/<agent>/*.md` |
| Memória institucional (Galp) | `.claude/agent-memory/_tenant/galp/<agent>/*.md` (via symlink) |
| Estado actual da engagement | `projects/<slug>/_state.json` |
| Artefacto vivo da engagement | `projects/<slug>/shared-understanding.md` |
| Outputs por lens | `projects/<slug>/lens-outputs/<lens>.md` |
| Topic packs intermédios | `projects/<slug>/_synthesis/*.md` |
| Deliverables finais | `projects/<slug>/_render/*.docx,*.md` |

---

## 5. Troubleshooting

### 5.1 `/start` falha com "AISA_ENGAGEMENTS_ROOT not set"

Verificar que (a) symlink/junction `aisa/projects/` existe; OU (b) `$env:AISA_ENGAGEMENTS_ROOT` está definido. Ver §2.2.

### 5.2 `/round` "lens-business not found"

A skill não está no path. Verificar: `ls .claude/skills/lens-business/SKILL.md`. Se não existe, é porque ainda estamos pré-Fase 2 do roadmap — aisa MVP ainda não está completo.

### 5.3 `/render --all` produz `render-gaps.md` com vários slots vazios

Significa que o `_synthesis/` não tem conteúdo suficiente para preencher slots required dos templates. Soluções:
1. Corre `/round` para a lens que devia ter contribuído (ver `render-gaps.md` para qual).
2. Resolve Unknowns que estão a bloquear synthesis.
3. Corre `/synthesize` manualmente (se foi /decide --no-synthesize por engano).
4. Depois corre `/render --all` outra vez; produz v02 sem sobrescrever v01.

### 5.4 Dois engagements em paralelo conflitam

Não devem. Cada engagement tem `_state.json` próprio. Se há conflict (raro), verificar que o pack activo é diferente em cada (`_state.json.pack`).

### 5.5 Erro hook "library/ read-only"

Está a tentar escrever em `library/`. aisa impede isto por design. Se precisas mesmo de editar (raro — ex: adicionar template de pack), faz-lo via git em ambiente local + commit; o hook está em runtime, não previne edits administrativos.

### 5.6 "Claude esquece-se de um step"

aisa não tem invariantes que o Claude tenha de lembrar simultaneamente (foi essa a razão do refactor). Se notar comportamento anómalo:
1. Confirma que estás na fase correcta (`/status`).
2. Re-corre a skill (skills são idempotentes).
3. Reporta o problema em `aisa/docs/ISSUES.md` (ou Jira/GitHub Issues).

---

## 6. Próximos passos depois do MVP

Depois de correres ~3 engagements em aisa, considera:

- **Contribuir para o question-bank PP** — perguntas que repetidamente fazes em PP discoveries vão para `library/packs/pp/question-bank.md` (PR aprovado pela team lead).
- **Acumular agent-memory** — anti-patterns que observas (ex: "Procurement sem CFO presente → conflicto financial"), recurring constraints (ex: "Galp Premium licenses dependem do BU; verificar early").
- **Adicionar pack** — se a Galp começa OutSystems projects, podes scaffold `library/packs/outsystems/` (cf. `docs/PACK_AUTHORING.md`).
- **Configurar MCP** — SharePoint connector para pull automático de documentos de discovery do tenant. Bater no admin.

---

**Para detalhe técnico → [`ARCHITECTURE.md`](ARCHITECTURE.md).**
**Para fundamentação filosófica → [`PHILOSOPHY.md`](PHILOSOPHY.md).**
**Para migração de aisa → [`MIGRATION_FROM_AISA.md`](MIGRATION_FROM_AISA.md).**
