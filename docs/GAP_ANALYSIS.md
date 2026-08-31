# aisa — Análise de Lacunas, Gaps e Inconsistências

> Data: 2026-08-31
> Âmbito: repositório completo (docs, kernel, packs, skills, agents, commands, hooks, settings, bootstrap)
> Método: leitura integral da documentação de base (ARCHITECTURE, PHILOSOPHY, ONBOARDING, IMPLEMENTATION_PLAN, MIGRATION, authoring guides) cruzada ficheiro-a-ficheiro com a implementação real, incluindo verificação programática (modos git dos hooks, slots declarados vs usados nos templates, greps de vocabulário vendor no kernel).
> Estado do build à data: fases 1–11 marcadas "done (structural)" no `IMPLEMENTATION_PLAN.md §16`; validação live end-to-end (`/frame` → `/render`) por executar; Fase 12 (pilot) por fazer.
>
> **Actualização 2026-08-31**: o passo 1 da sequência (§5) foi aplicado neste branch — **G-01, G-02, G-13, G-14, G-23 e G-24 corrigidos** (marcados ✅ abaixo).

---

## 1. Sumário executivo

O aisa está estruturalmente completo e o seu núcleo é sólido: o kernel é coerente, as 7 lenses seguem uma anatomia uniforme, a cadeia decision-tree → architecture-templates → deliverable-templates está bem ligada, e o conteúdo do pack `pp` cumpre os critérios de aceitação do plano. **Porém, existe uma classe consistente de problemas: a spec normativa (`ARCHITECTURE.md`) e o onboarding divergiram da implementação durante o build e não foram reconciliados.** Daí resultam:

1. **Promessas de enforcement que não são verdade hoje** — a única "hard rule" do sistema (`library/` read-only) não está enforced; 4 dos 5 hooks nem sequer são executáveis.
2. **Comandos documentados que não existem** — `/answer` (mecanismo central do walkthrough de onboarding), `/resume`, `/export`, `contradiction-scan`.
3. **Três especificações contraditórias para a fase Decision** (council vs interactivo) e um pipeline de render sem caminho definido para decisões não-tecnológicas — apesar de o sistema *obrigar* a propor opções non-tech/do-nothing.
4. **`ARCHITECTURE.md` corrompido por um rename global** — o sistema antecessor e o actual ficaram ambos com o nome "aisa", tornando secções inteiras ambíguas ("aisa substitui aisa").

Nada disto invalida o desenho; quase tudo é exactamente o tipo de problema que a validação live pendente (`/frame` → `/render --all`) e um passe editorial pré-pilot resolveriam. A secção 5 propõe a sequência.

---

## 2. O que está sólido (verificado)

| Área | Verificação |
|---|---|
| Kernel (`phases/states/orchestration/render-contract/glossary`) | Coerente entre si e com o CLAUDE.md nas 4 fases, 5 estados, 2 modos; sem jargão do sistema antigo. |
| 7 lens skills | Anatomia uniforme (6 secções, conforme `LENS_AUTHORING.md`); directiva de leitura de `inputs/` (fix `4fff337`) aplicada em todas; hard rules consistentes. |
| Cadeia de render | `decision-tree.md` declara 3 branches (`sharepoint-first`, `dataverse-first`, `hybrid`) e os 3 ficheiros em `architecture-templates/` existem com ids coincidentes; os `{{>> ...}}` dos templates resolvem para esses ids. |
| Deliverable templates | Os 6 têm frontmatter completo (`required_slots`, `optional_slots`, `slot_sources`); verificação programática: slots declarados = slots usados no corpo (0 divergências). |
| Pack `pp` | Question-bank com 88 perguntas em 7 lenses + quality gates (critério: ≥40); glossário com ~65 termos (critério: ≥30); 12 ficheiros de domain-knowledge declarados e presentes. |
| Commands | 8/8 comandos são thin pointers correctos para as skills respectivas. |
| `.gitignore` | Alinhado com o dual-repo (`projects/*`, `_tenant/`, `.env*`, `settings.local.json`). |
| Agent-memory `_universal/` | 14 ficheiros (2 × 7 personas), conteúdo substantivo, vendor-clean excepto `solution-architect/` (excepção esperada e registada no plano). |

---

## 3. Achados

Severidade: **P0** = quebra a experiência actual ou contradiz um princípio inviolável declarado; **P1** = inconsistência espec↔implementação ou defeito de conteúdo com impacto real; **P2** = menor/cosmético.

### 3.1 P0 — Críticos

#### G-01 · A única "hard rule" do sistema não está enforced
- **Evidência**: `CLAUDE.md` (princípio 5: "The only hard rule is `library/` is read-only") e `.claude/rules/library-readonly.md` ("Enforced by hook `pre-write-guard.sh` + `settings.json deny`") vs `.claude/settings.json:3` (`"deny": []`) e `:49` (`AISA_GUARD_MODE: "log"`). O hook em modo `log` apenas escreve um WARN em stderr (`pre-write-guard.sh:31-33`).
- **Contexto**: o `IMPLEMENTATION_PLAN.md §0.4` previa activar o enforce na Fase 11; a Fase 11 está marcada `done (structural)` mas o switch nunca foi ligado. O `HOOKS.md` admite honestamente o modo log-only — mas o CLAUDE.md, as rules e o ARCHITECTURE §9.1 afirmam o contrário.
- **Impacto**: qualquer sessão pode editar `library/` sem bloqueio; a documentação induz falsa confiança no único invariante "não negociável" do sistema.
- **Correcção sugerida**: com o build terminado, ligar o enforce (`AISA_GUARD_MODE=enforce` no `settings.json.env` + repor `deny: [Write(./library/**), Edit(./library/**)]`). Alternativa mínima: corrigir CLAUDE.md/rules para declararem log-only até v0.2.0.
- **✅ Corrigido (2026-08-31)**: `AISA_GUARD_MODE=enforce` por defeito (settings `env` + fail-closed no próprio script), deny rules repostas em `settings.json`, mensagem de bloqueio limpa, `HOOKS.md` e `.env.example` actualizados. Testado: enforce bloqueia `library/` (exit 2), deixa passar paths fora, log mode apenas avisa.

#### G-02 · 4 dos 5 hooks não são executáveis (committed como 100644)
- **Evidência**: `git ls-files --stage .claude/hooks/` → apenas `pre-write-guard.sh` é `100755`; `on-su-change.sh`, `phase-gate-check.sh`, `synthesis-validate.sh`, `render-validate.sh` são `100644`. O próprio `HOOKS.md` instrui "Mark executable (`chmod +x`)".
- **Impacto**: em Unix/macOS, todos os `Write|Edit` disparam 3 hooks que falham com *permission denied* (ruído em todas as escritas do engagement) e o matcher `Skill` idem — i.e., toda a observabilidade de soft gates prevista está inoperante fora do Windows.
- **Correcção**: `git update-index --chmod=+x .claude/hooks/*.sh` + commit.
- **✅ Corrigido (2026-08-31)**: os 4 hooks estão agora `100755` no índice git; sintaxe validada (`bash -n`).

#### G-03 · O onboarding depende de `/answer`, que não existe
- **Evidência**: `docs/ONBOARDING.md:236-242` (4 invocações de `/answer` + descrição do efeito Unknown→Confirmed com `was U-NNN`), `:252`, `:336`. Não existe `.claude/commands/answer.md` nem skill correspondente.
- **Impacto**: o passo 4 do walkthrough — o mecanismo central de progressão do Shared Understanding (resolver Unknowns/Conflicted com o sponsor) — não tem dono. Nenhuma skill descreve o procedimento de transição de estado fora do council; o consultor novo fica num beco sem saída no primeiro engagement.
- **Correcção**: criar `aisa-answer` (skill) + `/answer` (command) implementando as transições de `library/kernel/states.md`; ou, no mínimo, reescrever o ONBOARDING com o procedimento manual de edição do SU.

#### G-04 · `/resume` e `/export` documentados mas inexistentes
- **Evidência**: `CLAUDE.md:43` (tabela de slash commands inclui `/resume`), `ARCHITECTURE.md:725-726` (`/resume`, `/export`), e a própria skill `aisa-start/SKILL.md:20` responde "Engagement already exists. **Use /resume**". Não existem `commands/resume.md` nem `commands/export.md`.
- **Impacto**: o erro mais comum do `/start` aponta para um comando que não existe.
- **Correcção**: `/resume` é trivial (ler `_state.json` + delegar em `aisa-status`); `/export` pode ser removido das docs até existir.

#### G-05 · Fase Decision: três especificações contraditórias (council vs interactivo)
- **Evidência**:
  - `library/kernel/phases.md:74-76`: Decision = mode `council-independent`, "lenses active: solution-architect + chairman".
  - `library/kernel/orchestration.md:59`: cost envelope conta "Decision: 1 chairman + auto synthesize".
  - `chairman-synthesis/SKILL.md:3,17` e `chairman.md`: esperam ser invocados na Decision e produzir um draft `D-NNN (draft)`; os 7 agents têm "Mandate per phase → Decision".
  - `aisa-decide/SKILL.md:20`: "**Mode**: interactive (user-driven)" — não lança nenhum Task subagent, nunca invoca `chairman-synthesis`, e refere o draft do chairman com um revelador "(if it did)" (`:110`).
- **Impacto**: o princípio 4 do CLAUDE.md ("council-independent in Framing/Options/**Decision**") não é verdade na Decision; o draft do chairman nunca é criado; quem ler o kernel espera um comportamento que não acontece.
- **Correcção**: decidir o modelo — a implementação interactiva é defensável (a decisão é do humano) — e alinhar `phases.md`, `orchestration.md`, `chairman-synthesis`, os mandates dos agents e o CLAUDE.md com o que ficar decidido.

#### G-06 · `/decide` não escreve a linha `D-NNN` no Shared Understanding
- **Evidência**: `ARCHITECTURE.md §4.5` ("Cada `/decide` cria **uma linha em `## Confirmed`** com `id: D-NNN`... Mantém o SU completo") vs `aisa-decide/SKILL.md` → Outputs: `_state.json`, bloco em `decisions.md`, `_synthesis/`, `council-log.md` — o SU só é tocado para novos riscos.
- **Impacto**: viola a regra `shared-understanding-as-source-of-truth` ("SU é o documento autoritativo; deliverables renderizam de SU + decisions"): a decisão — o compromisso mais importante do engagement — fica fora do artefacto vivo; `/status` não a mostra.
- **Correcção**: acrescentar ao `aisa-decide` o passo de append da linha `D-NNN` em `## Confirmed` com cross-ref `decisions.md#D-NNN`.

#### G-07 · Decisão não-tecnológica ou do-nothing quebra o pipeline synthesize→render
- **Evidência**: o sistema **obriga** a propor do-nothing + non-tech (`aisa-options:94,103`, `decision-tree.md` §final, `chairman.md`). Mas: `architecture-story.template.md` exige como fonte "the pack's chosen architecture template (`architecture-templates/<branch>.md`)"; `solution-blueprint`, `claude-design-brief` e `estimate` embutem `{{>> architecture-templates/{{chosen_architecture}}.md}}`; para `chosen_architecture = "non-technology"` ou `"do-nothing"` esse ficheiro não existe. Nenhum contrato define que deliverables se aplicam nesse cenário — `ARCHITECTURE §5` afirma que "toda a engagement bem-sucedida termina com 6 entregas".
- **Impacto**: escolher a opção que o próprio sistema faz questão de pôr na mesa produz um render com gaps estruturais (ou falha), sem orientação. É um cenário de 1.º pilot perfeitamente plausível.
- **Correcção**: declarar no `pack.yaml` a aplicabilidade de cada deliverable por tipo de decisão (ex.: non-tech → discovery-report + executive-report + estimate) e definir fallback nos templates/`aisa-render` quando o branch não é tecnológico.

### 3.2 P1 — Importantes

#### G-08 · `ARCHITECTURE.md` corrompido pelo rename global (antecessor e sucessor ambos "aisa")
- **Evidência**: `:54` "`aisa` substitui `aisa` (SPEA v2)"; tabela do sumário executivo "aisa (rejeitado) | aisa (adoptado)"; "§1.2 Porque o aisa falhou estruturalmente"; "§11 Migração do aisa"; Apêndices B ("Glossário aisa (vs aisa)") e D ("Mapeamento Deliverables aisa → aisa").
- **Agravantes**: o changelog v2.0.0 anuncia renames nunca aplicados — skills sem prefixo `aisa-` (`:23`; a implementação usa `aisa-*` e o próprio corpo do doc §6 também), `MIGRATION_FROM_AISA.md → UPGRADE_V1_TO_V2.md` (`:25`; nunca renomeado, e o README/plan ainda apontam para o nome antigo); o rodapé diz "FIM — v0.1.0 DRAFT" (`:1126`) num documento v2.0.0.
- **Impacto**: o documento normativo — aquele que o plano manda reler no arranque de cada sessão de build — é ambíguo quanto a que sistema se refere em secções inteiras.
- **Correcção**: passe editorial único — dar um nome inequívoco ao antecessor (ex.: "SPEA v2 (aisa v1)") em todas as ocorrências, reconciliar o changelog com a realidade (prefixo `aisa-` mantido; rename do MIGRATION cancelado ou executado), corrigir o rodapé.

#### G-09 · Árvore §6 do ARCHITECTURE lista ~10 artefactos inexistentes ou com nomes errados
- **Evidência vs realidade**:
  | ARCHITECTURE §6/§7 | Realidade |
  |---|---|
  | `skills/contradiction-scan/`, `skills/gap-scan/` (`:393-394`) | Não existem |
  | `packs/pp/lenses-config.yaml` (`:457`, `:979`) | Embebido em `pack.yaml` (decisão do plano §3.1.4) |
  | `packs/_active.txt` (`:451`) | Deprecado pelo próprio doc (§10.5) mas ainda na árvore |
  | `architecture-templates/{canvas-only, model-driven-only, dataverse-led}` (`:466-469`, `:1002`) | Implementados: `sharepoint-first`, `dataverse-first`, `hybrid` |
  | `.mcp.json` (`:372`, `:843`; plano `:1462` diz "template já tem placeholders") | Não existe |
  | `.worktreeinclude` (`:373`) | Não existe |
  | `output-styles/client-ready.md` (`:434`) | Só `.gitkeep` |
  | `agent-memory/<agente>/{recurring-constraints,corporate-patterns}.md` (§7.3, §10.6) | Real: `_universal/<agente>/{universal-constraints,anti-patterns}.md`; não há pasta `chairman/` |
- **Impacto**: o §6 é usado como mapa por builders e autores de packs; cada divergência custa uma ida ao filesystem.
- **Correcção**: actualizar §6/§7/§10.6 para o estado real (ou mover a árvore para um doc gerado).

#### G-10 · `contradiction-scan` prometido em 4 sítios, inexistente
- **Evidência**: `ARCHITECTURE` princípio 4, §9.2, Apêndice A passo 9; `MIGRATION_FROM_AISA.md:178-184` responde à pergunta "como detecto contradições sem coherence-cells?" com uma skill standalone que corre (a) via hook `on-su-change.sh`, (b) `/contradiction-scan` manual, (c) no arranque do Framing — nada disto existe; `on-su-change.sh` é stub log-only.
- **Impacto**: hoje a detecção de conflitos assenta apenas no passo 3 do `lens-governance` e na síntese do chairman. É provavelmente suficiente para o MVP — mas então a resposta do MIGRATION §6.4 e o §9.2 do ARCHITECTURE estão errados, num ponto que era a *pedra angular* da crítica ao sistema antigo.
- **Correcção**: implementar a skill (o gap funcional mais relevante do kernel) ou reescrever §6.4/§9.2 para descrever o mecanismo real (governance-lens + chairman).

#### G-11 · Framing: "subset de 3-4 lenses" vs sempre-6
- **Evidência**: `phases.md:33` e `ARCHITECTURE §3.1` ("subset relevante das 6", "chairman picks the 3-4 most relevant") vs `aisa-frame` (lança sempre as 6 personas, passos 4-5).
- **Correcção**: alinhar — sempre-6 é mais simples e é o que está implementado; corrigir o kernel.

#### G-12 · Regressão de fase: kernel promete, skill recusa
- **Evidência**: `phases.md:97` "Phase regression is allowed (`/round` from Framing returns to Discovery scope if needed)" vs `aisa-round:12` ("If `phase != discovery` → stop"). O rollback existe apenas dentro do fluxo de validação do `aisa-frame` (passo 8a).
- **Correcção**: ou `aisa-round` oferece o rollback quando chamado em Framing, ou `phases.md` passa a descrever o rollback via `/frame` → "more rounds".

#### G-13 · Nome do ficheiro de auditoria do chairman diverge em 3 especificações
- **Evidência**: `chairman-synthesis/SKILL.md` e `chairman.md` → `chairman-synthesis-R<NN>.md`; `aisa-frame:37` → `chairman-synthesis-F-<NN>.md`; `aisa-options:34` → `chairman-synthesis-O-<NN>.md`.
- **Impacto**: em runtime o LLM recebe instruções conflituantes sobre o mesmo output; a auditabilidade entre rondas fragmenta-se.
- **Correcção**: canonizar `chairman-synthesis-<F|O|D>-<NN>.md` nos 3 ficheiros (+ ARCHITECTURE §4.4).
- **✅ Corrigido (2026-08-31)**: canonizado `chairman-synthesis-<round>.md` (`F-<NN>`/`O-<NN>`/`D-<NN>`) em `chairman-synthesis/SKILL.md`, `chairman.md`, `library/kernel/orchestration.md` e `ARCHITECTURE.md` §4.4/§6.

#### G-14 · Output do solution-architect não bate com o parser do chairman
- **Evidência**: `chairman-synthesis/SKILL.md:39` parseia 6 secções fixas, incluindo `Proposal`; `solution-architect.md` devolve `### Options (Options phase) / Architecture (Decision phase)` em vez de `### Proposal`.
- **Impacto**: warning de parser garantido em todas as rondas de Options (ou, pior, secção ignorada na síntese).
- **Correcção**: renomear a secção para `Proposal` no agent (ou ensinar o alias ao chairman).
- **✅ Corrigido (2026-08-31)**: secção renomeada para `### Proposal` em `solution-architect.md`, com a distinção Options/Decision preservada na descrição do conteúdo.

#### G-15 · `decision-tree.md`: regras degeneradas e inputs não declarados
- **Evidência**:
  - `R4` (`:82`): `IF ... → A=mínimo, B=alto, C=médio / ELSE → A=mínimo, B=alto, C=médio` — veredictos idênticos nos dois ramos (regra no-op; provável erro de edição). `R6` (`:93`) idem; `R5` tem o 2.º e 3.º ramos idênticos.
  - Os hard gates `R0` e o "Hybrid trigger" usam condições (`formula_count`, cross-list joins, precisão financeira >2 decimais, multi-stage approval, rejeição de premium licensing, >3 integrações externas, real-time, `entities_simple/complex`) que **não estão** em `inputs_used` no frontmatter — logo o protocolo "input em falta → STOP + Unknown" não cobre exactamente as regras mais destrutivas (as que eliminam branches).
- **Correcção**: rever os veredictos de R4-R6 (presumivelmente deviam variar); completar `inputs_used` com as condições de R0/Hybrid.

#### G-16 · Vocabulário de solução PP dentro do Discovery e do kernel
- **Evidência**:
  - `packs/pp/pack.yaml:31,38` — `extra_signals` das lenses de **Discovery** incluem `premium_connector_need`, `licensing_baseline`, `dataverse_vs_sharepoint`: vocabulário da solução Microsoft a orientar lentes que "MUST NOT name vendors" (a rule permite nomear o *estado actual*, mas `dataverse_vs_sharepoint`/`premium_connector` são conceitos do *destino* PP — enviesam a descoberta para PP antes de Options, contra o princípio 1 e contra a promessa de opções OutSystems/non-tech em pé de igualdade).
  - `library/kernel/synthesis-templates/architecture-story.template.md:27` nomeia "Canvas App + Dataverse tables + Power Automate flows, or SharePoint Online..." — no **kernel**, que o plano (§15) exige vendor-clean ("Grep `library/kernel/` por Power|Dataverse|Canvas → 0 hits").
- **Correcção**: renomear os sinais de Discovery para forma neutra (ex.: `structured_vs_document_storage_today`, `integration_licensing_exposure`) mantendo o mapeamento PP no pack; mover os exemplos do template do kernel para o pack.

#### G-17 · Colisões de prefixos de id (rondas vs linhas vs opções)
- **Evidência**: rondas `R-01/F-01/O-01/D-01` vs linhas Risky `R-001`, opções `O-001`, decisões `D-001` — os pares R/R, O/O, D/D distinguem-se apenas pelo número de dígitos. `aisa-decide` pede "which open **R-NNN** risks" numa tabela cuja coluna `ronda` contém `R-01`.
- **Impacto**: num sistema operado por LLM, é uma fonte previsível de citações trocadas (exactamente a classe de erro que o aisa v2 quer eliminar).
- **Correcção**: prefixos de ronda distintos (ex.: `RD-/RF-/RO-` ou campo numérico simples) — mudança barata agora, cara depois do pilot.

#### G-18 · `<tenant>` nunca é resolvido
- **Evidência**: todas as lenses e agents referem `.claude/agent-memory/_tenant/<tenant>/<agente>/` "(if present)", mas nada define o tenant — não está em `_state.json` (schema: engagement, pack, phase, round, aisa_version, created), nem em `context.json`, nem em env/settings.
- **Correcção**: acrescentar `tenant` ao `_state.json` (capturado no `/start`) ou convencionar que `_tenant/*/` é carregado integralmente.

#### G-19 · `/start` não valida packs; skeletons arrancam engagements que não renderizam
- **Evidência**: `ARCHITECTURE §7.1` "Schema validation acontece em load-time via aisa-start" vs `aisa-start:21` (só verifica a existência do `pack.yaml`). Os packs `outsystems/mendix/generic` declaram `question_bank`, `glossary` e `decision_tree` que **não existem** nos folders e `deliverables: []`.
- **Impacto**: `/start x outsystems` arranca; a Discovery corre; `/render --all` renderiza 0 entregas — o utilizador só descobre no fim.
- **Correcção**: `aisa-start` avisa quando `deliverables` está vazio ou ficheiros declarados faltam ("skeleton pack — Discovery/Framing OK, Options/Render limitados").

#### G-20 · `bootstrap.ps1` quebrado nos dois caminhos que se propõe automatizar
- **Evidência**:
  - **Junction**: `projects/` existe sempre num clone fresco (`projects/.gitkeep` é tracked) → o script cai sempre no ramo "real directory... Leaving as-is" e nunca cria a junction. O ONBOARDING (§2.2-A) manda remover `projects/` primeiro; o script não o faz.
  - **Env var**: o passo final instrui `. .\.env.local` — dot-sourcing de um ficheiro `KEY=value` **não é sintaxe PowerShell** (falha); e nada no runtime lê `.env.local`, portanto `AISA_ENGAGEMENTS_ROOT` morre com a shell do bootstrap.
  - **Convenções divergentes**: `.env.example` diz "copy to `.env`"; o bootstrap escreve `.env.local`.
  - O passo 3 "marca hooks executáveis" é um loop vazio (e não há bootstrap Unix), perpetuando o G-02.
- **Correcção**: remover `projects/` vazio antes de criar a junction; gerar snippet `$env:` para o `$PROFILE` em vez do dot-source; unificar `.env`; fazer o chmod real.

#### G-21 · ONBOARDING desactualizado face ao modelo de rondas R-00
- **Evidência**: `ONBOARDING.md:168` mostra `/start` a semear `"round": "R-01"`; o modelo convergido na Fase 5 (plano §16: "`/start` semeia R-00; `/round` incrementa no início") está correcto nas skills mas o ONBOARDING nunca foi corrigido (o plano até anota que o exemplo ficou "ilustrativo" — num doc de onboarding, é um erro à espera de confundir).

#### G-22 · ONBOARDING promete `.docx`; o render produz `.md`
- **Evidência**: `ONBOARDING.md:327-333` lista `galp-adv_discovery-report_v01.docx` etc.; `aisa-render` escreve exclusivamente `.md` (`render-contract.md`: "Conversion to .docx via Pandoc (post-render step, **optional in MVP**)") e não existe nenhum passo/hook de conversão. Também `:117` usa `/aisa-status --check` (o comando é `/status --check`).
- **Correcção**: ONBOARDING realista (outputs `.md` + conversão manual via Pandoc/Word) até existir o passo de conversão.

### 3.3 P2 — Menores / cosméticos

| Id | Achado | Evidência |
|---|---|---|
| G-23 | ✅ Corrigido (2026-08-31) — Resíduo de rascunho ("… — **wait,** in Options they *may* read…") no meio de uma regra normativa; nota reescrita (e corrigida: em council-independent as personas não veem o output do solution-architect in-flight) | `aisa-options/SKILL.md:132` |
| G-24 | ✅ Corrigido (2026-08-31) — Nota obsoleta: "lenses data/governance/financial arrive in a later build phase" (existem desde a Fase 6); reescrita como guarda para instalações truncadas | `aisa-round/SKILL.md:21` |
| G-25 | `states.md` lista "industry-standard claim" como evidência de **Confirmed**, contradizendo a decision rule logo abaixo ("based on typical engagements" → Assumed); e a tabela de transições não tem nenhum caminho para *sair* de Confirmed (ex.: Confirmed→Conflicted quando surge fonte contraditória) | `library/kernel/states.md:9,17,23-31` |
| G-26 | `phases.md` lista "solution-architect" (agent) como *lens* da Decision — mistura as duas taxonomias (a lens é `technology`) | `library/kernel/phases.md:74` |
| G-27 | `HOOKS.md` descreve matchers que não correspondem ao `settings.json` (phase-gate-check: "on `aisa-frame\|aisa-options\|aisa-decide`" vs matcher real `Skill`; on-su-change: "to `shared-understanding.md`" vs matcher amplo `Write\|Edit` com filtro interno) | `.claude/hooks/HOOKS.md:8-9` vs `.claude/settings.json:18-44` |
| G-28 | ARCHITECTURE §10.7 promete "Skill versions em frontmatter de cada SKILL.md" — nenhuma skill tem campo de versão | `docs/ARCHITECTURE.md:900` |
| G-29 | Mitigação do "risco principal" do MVP promete "`/status` mostra preview de cada deliverable em tempo real" — `aisa-status` não faz previews | `docs/ARCHITECTURE.md:1027-1028` |
| G-30 | Exemplo de `D-001` no §4.5 é a escolha tecnológica; no sistema real `D-001` é o frame (aisa-frame §8, phases.md) — exemplo desactualizado | `docs/ARCHITECTURE.md:287-291` |
| G-31 | Robustez do guard quando passar a enforce: os globs `*/library/*`, `./library/*`, `library/*` não cobrem paths Windows com backslashes; o deny de settings (quando reposto) só cobre o path relativo | `.claude/hooks/pre-write-guard.sh:27` |
| G-32 | `docs/ISSUES.md` referido no troubleshooting e na Fase 12 não existe ainda | `docs/ONBOARDING.md:395`, plano `:1440` |
| G-33 | `.env.example` e ONBOARDING §2.3 assumem configuração MCP; não existe `.mcp.json` (v. G-09) | `.env.example`, `docs/ONBOARDING.md:95-104` |

---

## 4. Causa-raiz transversal

Dois padrões explicam ~80% dos achados:

1. **A spec normativa não acompanhou as decisões do build.** O `IMPLEMENTATION_PLAN §16` registou fielmente os desvios (round-model R-00, 3 branches em vez de 4, lenses-config embebido, deny rules adiadas…), mas o `ARCHITECTURE.md` — que o próprio plano manda tratar como "spec normativa" e reler a cada sessão — nunca recebeu esses updates. O ONBOARDING idem (escrito na fase de design, antes das skills existirem).
2. **A validação live end-to-end nunca correu.** O plano identifica-o como próximo passo. Quase todos os P0 (hooks inexecutáveis, `/answer` ausente, Decision sem council, render non-tech) seriam apanhados na primeira passagem `/start → /round → /frame → /options → /decide → /render --all`.

---

## 5. Sequência de correcção recomendada

| Ordem | Âmbito | Achados | Esforço |
|---|---|---|---|
| 1 | Correcções mecânicas: chmod dos hooks; decidir e aplicar enforce (ou corrigir docs); limpar resíduos; canonizar nome do log do chairman; secção `Proposal` do solution-architect | G-02, G-01, G-23, G-24, G-13, G-14 | ✅ aplicado (2026-08-31, neste branch) |
| 2 | Decisões de design da fase Decision: modelo council vs interactivo; linha D-NNN no SU; caminho non-tech/do-nothing no synthesize/render | G-05, G-06, G-07 | ~1 sessão (requer decisão do sponsor) |
| 3 | Fechar o loop do utilizador: `/answer` + `/resume` | G-03, G-04 | ~1 sessão |
| 4 | Passe editorial pré-pilot: ARCHITECTURE (rename, árvore §6, changelog, exemplos), ONBOARDING (R-00, .md, /status), MIGRATION §6.4 | G-08, G-09, G-10, G-21, G-22, G-30 | 1-2 sessões |
| 5 | Backlog v0.2.0: decision-tree (regras + inputs), sinais neutros de Discovery, prefixos de ronda, tenant, bootstrap, validação de packs, transições de estado | G-15, G-16, G-17, G-18, G-19, G-20, G-25 | planeável |

Só depois do passo 4 faz sentido arrancar a **validação live end-to-end** e a **Fase 12 (pilot)** — os consultores do pilot vão ler exactamente os documentos hoje desalinhados.
