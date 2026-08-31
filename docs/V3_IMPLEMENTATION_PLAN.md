# aisa v3 — Plano de Implementação (Vagas A–D)

**Plano operacional de build, passo-a-passo, para Claude (builder) executar autonomamente numa nova sessão.**

> Versão: v1.0.0 — pronto para arrancar a Vaga A
> Data: 2026-08-31
> Audiência: Claude (LLM builder, sessão nova SEM contexto desta conversa) + Jorge (reviewer/sponsor)
> Companion docs: `NEXT_LEVEL_PLAN.md` (estratégia), `LIVE_VALIDATION_REPORT.md` (prova de que a base funciona), `ARCHITECTURE.md` v2.1.0 (spec normativa da base), `GAP_ANALYSIS.md` (histórico), `IMPLEMENTATION_PLAN.md` (build v0.1 — padrão a seguir)
> Resultado final: **aisa v3.0** — as 5 peças epistémicas + camada de experiência, entregues em 4 vagas incrementais (v2.2 → v2.3 → v2.4 → v3.0), cada uma validada live.

---

## 0. Como usar este plano

### 0.1 Pré-flight da sessão nova (fazer por esta ordem, antes de qualquer edição)

1. Ler `docs/NEXT_LEVEL_PLAN.md` §1–2 (a tese e os horizontes) e `docs/LIVE_VALIDATION_REPORT.md` (o que já foi provado a funcionar).
2. Ler este plano inteiro.
3. Confirmar o estado do repo: `git log --oneline -10` — o último build relevante é a sequência `1f0c962` (next-level build) → `c3fc137` (validação) no branch `claude/repo-gaps-analysis-02922z`.
4. **Branch**: trabalhar no branch que a tua sessão designar. Se `claude/repo-gaps-analysis-02922z` ainda não foi merged, parte dele (`git checkout -B <teu-branch> origin/claude/repo-gaps-analysis-02922z`); se já foi merged para master, parte de master. Nunca fazer push para outro branch.
5. Verificar `§10 Resume tracking` no fim deste ficheiro — se uma vaga já está `☑`, retomar na seguinte.
6. `TaskCreate` para os itens da vaga corrente; `TaskUpdate` à medida que progride.

### 0.2 Constraints invioláveis (herdadas do repo + desta iniciativa)

1. **`library/` é hard-guarded**: o hook `pre-write-guard.sh` está em ENFORCE e o `settings.json` tem deny de Write/Edit em `library/**`. O caminho sancionado para editar kernel/packs é **administrativo**: scripts python via Bash (heredoc com replacements exactos) + git commit. Todos os builds anteriores usaram este padrão — segue-o. NUNCA desativar o guard.
2. **Sem CLI, sem event-store, sem base de dados.** Decisão explícita do Jorge (2026-08-31): a diferenciação é epistémica, não mecânica. O SU continua markdown legível; as skills continuam prosa; a única "máquina" são os hooks existentes. Se durante o build parecer que "um script resolvia isto", a resposta é: convenção + skill, não código de runtime.
3. **O schema governa onde as coisas se arquivam, nunca o que pode ser dito.** Os 5 estados ficam 5. Evidência é texto livre. Nenhuma peça nova pode constranger o *conteúdo* de um claim — só a sua *filiação* (data, classe de validade, custo, swing). Esta é a linha vermelha anti-regresso-ao-v1.
4. **Append-only no SU** mantém-se; as únicas edições sancionadas a rows existentes são as transições explícitas (marker `resolved →`) e, novo nesta versão, a **revalidação** (renovar `verificado_em`) — ver §3.2.
5. **Vendor-neutrality**: nada de nomes de vendor no kernel nem em artefactos de Discovery/Framing. Grep de verificação em cada vaga.
6. **Compatibilidade com engagements antigos**: SUs criados antes da v3 não têm as colunas novas. Regra universal: coluna ausente ⇒ tratar como `verificado_em = data da ronda` e `validade = organizacional`. Nunca migrar SUs antigos à força.
7. **Cada vaga termina com**: validação live (protocolo §7, versão reduzida ou completa conforme a vaga), commit(s) temáticos, push, e o `§10 Resume tracking` deste ficheiro actualizado. Mensagens de commit sem identificadores de modelo.
8. **Defaults de calibração** (§9) usam-se marcados como default; tudo o que precisar do Jorge fica `TODO(team)` no próprio ficheiro — nunca bloquear a vaga à espera de calibração.
9. Idioma: identificadores/estrutura em inglês onde o repo já o faz; conteúdo PT-PT.

### 0.3 Convenções de artefactos (iguais ao repo)

- Skills: `.claude/skills/<nome>/SKILL.md` com frontmatter `name` + `description` (a description é o gatilho — específica e completa).
- Commands: `.claude/commands/<nome>.md` thin pointer com `description` + `argument-hint`.
- Versionamento de outputs de engagement: append-only `v<NN>` (padrão `_render/`).
- Kernel docs: header `# <Título> — Kernel v0.2.0` (bump nesta iniciativa — ver Vaga D).
- Commits: 1–2 por vaga, prefixo `feat:`/`docs:`, corpo com bullet por peça.

### 0.4 Decisões já fechadas com o sponsor (NÃO re-litigar)

| # | Decisão | Origem |
|---|---|---|
| 1 | Sem CLI/event-store; aprofundar epistemologia, não mecânica | Jorge, 2026-08-31 |
| 2 | As 5 peças: metabolismo, economia da pergunta, pré-mortem+dialética, multiverso, biografias — mais narrativa e deliverable interrogável | conversa de redesenho v3 |
| 3 | Ordem de entrega: Vaga A (P0+P1+P3a) → B (P2+narrativa) → C (P3b+P4) → D (P5+interrogável+docs+validação) | estimativa aprovada implicitamente ("cria um plano para executar") |
| 4 | Versões: A=v2.2, B=v2.3, C=v2.4, D=v3.0; kernel 0.1.0→0.2.0 na Vaga D; pack pp 1.1.0→1.2.0 na Vaga D | este plano |
| 5 | Decision continua interactiva (user-driven); os 4 gates humanos mantêm-se: answers, frame, decide, blueprint | build anterior, validado |
| 6 | Fora de âmbito v3.0: scanner H2 (depende do MCP de authoring externo), operação assíncrona, pack não-software, "deliverable que responde com Claude" (fica interrogável estático v1; interactivo é v3.1) | NEXT_LEVEL_PLAN §4 |

---

## 1. Estado de partida (o que já existe e funciona)

- Pipeline completo validado live: `/start /round /answer /status /frame /options /simulate /decide /synthesize /blueprint /render /resume` — ver `LIVE_VALIDATION_REPORT.md`.
- Council-independent com Task subagents paralelos (6 no Framing, 7 nas Options); só o chairman escreve no SU; excertos incluem resoluções.
- `/simulate` já produz comparação por opção + secção VOI — a Vaga B **generaliza** este conceito, não o inventa.
- Blueprint com `su_refs`, aprovação D-NNN, render filtrado por `applies_to`.
- Guard enforce; hooks executáveis; pack pp v1.1.0 com `delivery-conventions.md`.
- **O fixture de validação (`projects/galp-adv-val`) é gitignored — NÃO existe numa sessão nova.** O Apêndice D tem o gerador para o recriar em ~2 minutos.

---

## 2. Arquitectura conceptual da v3 (resumo normativo)

Uma frase por peça, com a semântica exacta que o build deve implementar:

1. **Metabolismo (P1)**: cada row Confirmed/Assumed tem `verificado_em` (data) e `validade` (classe de decaimento). Uma row cujo `verificado_em + meia-vida(validade) < hoje` está **expirada**: conta como "a revalidar" no /status, é tratada pelas lenses/personas como *Assumed fraca* (nunca como Confirmed), e a re-pergunta é gerada automaticamente. Revalidar = renovar a data (edição sancionada); se o facto mudou, transição normal (`was <id>`).
2. **Economia da pergunta (P2)**: cada Unknown nasce com `custo` (email | reuniao | documento | spike) e `swing` (decisivo | dimensionante | cosmético + 1 frase "o que muda"). O /status produz a **agenda da reunião**: as perguntas custo=reuniao ordenadas por swing, e a lista explícita "não gastes tempo com" (cosméticos).
3. **Pré-mortem (P3a)**: antes do /decide, `/premortem` escreve o obituário do projecto datado a +12 meses — cada causa de morte ancorada a ids do SU; as mitigações viram requisitos ou tripwires candidatos.
4. **Dialética (P3b)**: quando o chairman detecta divergência material entre personas, dispara uma segunda vaga de Task calls **só para os lados divergentes** (tese→antítese→síntese). Máx. 3 divergências × 2 calls por ronda.
5. **Multiverso (P4)**: no /decide, as projecções das opções rejeitadas são congeladas como counterfactuals; as revision conditions ganham formato estruturado de **tripwires**; /status e /resume verificam tripwires; `/revisit` compara o presente com o counterfactual e recomenda (nunca decide).
6. **Biografias (P5)**: `/retro` no fecho: cada persona escreve o diário do engagement (staged, curadoria humana antes de entrar em `agent-memory/_universal/<persona>/diary.md`); as personas passam a citar casos do próprio diário.
7. **Experiência**: `story.md` (1 parágrafo narrativo por marco, voz de sponsor) e render `--html` do discovery-report com proveniência navegável (tooltips de evidência por id) — HTML puro, zero dependências externas.

---

## 3. VAGA A — v2.2 "o caderno ganha vida" (P0 + P1 + P3a)

**Objectivo**: metabolismo epistémico + pré-mortem. **Sessão estimada**: 2,5 sessões (~1 turno de build + validação).

### 3.1 Acções ficheiro-a-ficheiro

| # | Ficheiro | Acção |
|---|---|---|
| A1 | `library/kernel/states.md` (admin path) | (a) Schema Confirmed: `id \| lens \| claim \| evidência \| verificado_em \| validade \| ronda`; Assumed idem. (b) Nova secção **"Epistemic half-lives"** com as 6 classes e defaults do §9.1 + a regra de expiração + a regra de compatibilidade (coluna ausente ⇒ `verificado_em`=data da ronda, `validade`=organizacional). (c) Nova transição na tabela: `Confirmed (expirado) → Confirmed (revalidação: renova verificado_em — edição sancionada)` e `Confirmed (expirado) → Unknown (o facto pode ter mudado; re-pergunta)`. |
| A2 | `library/packs/pp/pack.yaml` (admin path) | Nova secção `epistemics:` com `half_lives_override:` (vazia por defeito, com comentário `TODO(team)`) — os defaults vivem no kernel; o pack só sobrepõe. |
| A3 | `.claude/skills/aisa-start/SKILL.md` | O skeleton do SU passa a incluir as colunas novas nas tabelas Confirmed/Assumed; header do SU ganha a linha `> Saúde epistémica: —` (preenchida pelo /status). |
| A4 | Todas as 7 lens skills + `chairman-synthesis` | Passo de escrita de rows: "ao escrever Confirmed/Assumed, carimba `verificado_em` = hoje e escolhe `validade` da tabela de classes do kernel (na dúvida: `organizacional`)". Passo de leitura: "rows expiradas (ver states.md) tratam-se como Assumed fraca — nunca cites uma row expirada como Confirmed; se ela sustenta uma conclusão, levanta a re-pergunta". |
| A5 | `.claude/skills/aisa-answer/SKILL.md` | Novo modo `--revalidate <id>`: confirma que o facto se mantém → renova `verificado_em` na row (edição sancionada) + registo em answers.md. Se a resposta revelar mudança → transição normal `was <id>`. |
| A6 | `.claude/skills/aisa-status/SKILL.md` | (a) Calcular **saúde epistémica** = vivas/(vivas+expiradas) sobre Confirmed+Assumed abertas; mostrar `Saúde epistémica: NN% (X expiradas)`. (b) Secção "A revalidar" com as expiradas top-5, cada uma com a re-pergunta já formulada (`/answer --revalidate <id>` ou `/answer <id> "..."`). (c) Actualizar a linha de saúde no header do SU. |
| A7 | `.claude/skills/aisa-premortem/SKILL.md` | **NOVO** — draft completo no Apêndice A; transcrever com ajustes mínimos. |
| A8 | `.claude/commands/premortem.md` | **NOVO** — thin pointer, `argument-hint: "[--horizon <meses>]"`. |
| A9 | `.claude/skills/aisa-decide/SKILL.md` | Pre-flight: "se `premortem.md` não existe ou é anterior à última ronda de Options → sugerir `/premortem` primeiro (soft, override livre)". |
| A10 | `CLAUDE.md` | `/premortem` na tabela de comandos; princípio 3 ganha meia frase: "Confirmed/Assumed carregam validade — conhecimento expira e revalida-se". |
| A11 | `docs/ONBOARDING.md` | Passo 3.4: mostrar a saúde epistémica no output do /status; novo passo 3.8b-pre: `/premortem` antes do `/decide`. |

### 3.2 Especificações de detalhe

**Regra de expiração** (texto normativo para states.md): *"Uma row está expirada quando `verificado_em + meia-vida(validade) < hoje`. Expirada ≠ falsa: significa que a confiança caducou. Efeitos: (1) /status conta-a em 'a revalidar' e a saúde epistémica desce; (2) lenses e personas tratam-na como Assumed fraca; (3) a re-pergunta sugerida é gerada a partir do claim ('Ainda é verdade que <claim>? Verificado pela última vez em <data>'). A revalidação renova `verificado_em` sem nova row; a mudança de facto segue a transição normal com `was <id>`."*

**Formato da célula `verificado_em`**: `2026-08-31` (ISO, só data). **`validade`**: uma das 6 classes do §9.1 (nome curto).

### 3.3 Validação e aceitação (Vaga A)

1. Recriar o fixture (Apêndice D). Correr `/start` + 1 `/round` — verificar colunas novas preenchidas pelas lenses.
2. Forjar expiração: editar 2 rows do fixture com `verificado_em` antigo (ex.: 2025-01-10, validade pessoas-disponibilidade) → `/status` mostra saúde <100% e as 2 na lista "a revalidar" com re-pergunta.
3. `/answer --revalidate` numa; `/answer` normal na outra com facto mudado → verificar renovação vs transição `was`.
4. `/premortem` sobre o fixture completo (usar o estado final do Apêndice D se a vaga correr depois da C; senão, correr até Options primeiro) → obituário com ≥3 causas, todas com ids, mitigações mapeadas.
5. Greps: `verificado_em` presente em rows novas; zero vendor no premortem de fase pré-Options... (premortem corre em Options/Decision — vendor permitido se ancorado); `bash -n` nos hooks intocados.
6. Commit `feat: epistemic half-lives + premortem (v2.2 wave A)`; push; §10 actualizado.

### 3.4 Riscos da vaga

| Risco | Mitigação |
|---|---|
| Tabelas SU ficam largas demais com 2 colunas | Datas curtas (ISO date) e classes curtas; testado no fixture antes de fechar a vaga |
| Lenses esquecem-se de carimbar | A regra vive em states.md (fonte única) + passo explícito em cada lens; validação verifica |
| Premortem vira lista de riscos requentada | Hard rule do skill: proibido repetir o texto das rows Risky — o obituário NARRA como as causas se combinam (ver Apêndice A) |

---

## 4. VAGA B — v2.3 "perguntas com preço" (P2 + narrativa)

**Objectivo**: economia da pergunta em todo o pipeline + a narrativa contínua. **Sessão estimada**: 2 sessões.

### 4.1 Acções

| # | Ficheiro | Acção |
|---|---|---|
| B1 | `library/kernel/states.md` (admin) | Schema Unknown: `id \| lens \| pergunta \| quem responde \| criticidade \| custo \| swing \| ronda`. Definições: `custo ∈ {email, reuniao, documento, spike}` (o que custa obter a resposta — §9.2); `swing` = `classe: frase` com `classe ∈ {decisivo, dimensionante, cosmético}` e a frase a dizer *o que muda* se respondida (ex.: `decisivo: elimina O-004 ou muda o branch`). Compatibilidade: colunas ausentes ⇒ custo=email, swing=dimensionante. |
| B2 | 7 lens skills | Passo de emissão de Unknown: estimar custo (por quem responde e como) e swing (que decisão/estimativa/desenho muda). Regra: swing `cosmético` é legítimo e útil — é o que permite ao /status dizer "não gastes tempo com isto". |
| B3 | `.claude/skills/aisa-status/SKILL.md` | Nova secção **"Agenda da próxima reunião"**: Unknowns abertas com custo=reuniao, ordenadas decisivo→dimensionante, cada uma com o swing; depois "Por outro canal" (email/documento); depois **"Não gastes tempo com"** (cosméticos, explícito). |
| B4 | `.claude/skills/aisa-simulate/SKILL.md` | A secção VOI cita as classes de swing das rows (deixa de as inferir do zero) e verifica coerência: um Unknown que o simulate considera decision-flipping mas está marcado cosmético → corrigir a row (transição sancionada de metadado) e anotar no output. |
| B5 | `.claude/skills/aisa-answer/SKILL.md` | Output final passa a citar o swing realizado ("resposta obtida; swing declarado: decisivo — verifica se O-004 caiu"). |
| B6 | `.claude/skills/aisa-{round,frame,options,decide,blueprint,render}/SKILL.md` | **Narrativa**: passo final de cada uma — "appenda 1 parágrafo a `<engagement>/story.md` (formato: `## Episódio <N> — <data> — <marco>`), voz para sponsor, 4-8 frases, máx. 2 ids citados, sem jargão de kernel". `aisa-start` cria `story.md` com o episódio 1 (o pedido). |
| B7 | `library/kernel/glossary.md` (admin) | Termos novos: half-life/validade, custo, swing, agenda da reunião, story. |
| B8 | `CLAUDE.md` + `ONBOARDING.md` | Agenda da reunião no walkthrough (§3.5 passa a começar pela agenda do /status); story.md na tabela "onde as coisas vivem". |

### 4.2 Validação e aceitação (Vaga B)

1. Fixture: 1 ronda → todos os Unknowns novos com custo+swing; `/status` produz agenda com as 3 listas.
2. Verificar o caso "cosmético": ≥1 pergunta explicitamente em "não gastes tempo com".
3. `/simulate` → VOI cita classes; forjar 1 incoerência (cosmético que flipa) → verificar correcção anotada.
4. `story.md` com ≥3 episódios legíveis por leigo após start+round+frame do fixture.
5. Commit `feat: question economics + continuous narrative (v2.3 wave B)`; push; §10.

---

## 5. VAGA C — v2.4 "o council discute e o mapa guarda-se" (P3b + P4)

**Objectivo**: dialética no council + multiverso/tripwires. **Sessão estimada**: 2,5 sessões (inclui validação live com subagents).

### 5.1 Acções — dialética (P3b)

| # | Ficheiro | Acção |
|---|---|---|
| C1 | `.claude/skills/chairman-synthesis/SKILL.md` | Step 2 ganha output explícito: lista de **divergências materiais** (claim vs counter-claim entre personas, com impacto no artefacto da fase). Novo Step 2b: "se ≥1 divergência material, devolve-as ao caller ANTES de escrever; o caller corre a ronda de antítese e re-invoca-te com teses+antíteses". Step 3: divergências que sobrevivem à antítese → Conflicted rows (nunca escolher vencedor em silêncio). |
| C2 | `.claude/skills/aisa-frame/SKILL.md` + `aisa-options/SKILL.md` | Novo passo 5b (condicional): para cada divergência (máx. 3 por ronda), lançar 2 Task calls — cada lado recebe a tese do outro com o prompt do §5.3 — em paralelo. Juntar antíteses e re-invocar chairman-synthesis. Actualizar a nota de custo. |
| C3 | `library/kernel/orchestration.md` (admin) | Secção nova **"Dialectic round"**: quando dispara, o cap (≤6 calls extra), porquê só nos pontos divergentes (o peer-review integral foi rejeitado por custo — isto é o substituto cirúrgico). Cost envelope actualizado: Framing/Options = 7-8 passes + 0-6 dialécticos. |

### 5.2 Acções — multiverso (P4)

| # | Ficheiro | Acção |
|---|---|---|
| C4 | `.claude/skills/aisa-decide/SKILL.md` | Novo passo 4c: para cada opção NÃO escolhida com projecção na última simulação, congelar `_simulation/counterfactuals/<O-NNN>.md` (a projecção + "condições em que este ramo ganharia", derivadas dos veredictos da árvore e do VOI). Passo 4 (bloco D-NNN): "Revision conditions" passam a formato tripwire estruturado (§5.4). |
| C5 | `.claude/skills/aisa-status/SKILL.md` + `commands/resume.md` | Passo novo: ler tripwires do último D-NNN; para cada um, verificar se há evidência de disparo no SU (rows novas que satisfazem a condição); disparado → alerta destacado com o counterfactual associado + sugerir `/revisit`. |
| C6 | `.claude/skills/aisa-revisit/SKILL.md` + `commands/revisit.md` | **NOVOS** — draft completo no Apêndice C. |
| C7 | `library/kernel/render-contract.md` (admin) | Nota: counterfactuals são artefactos de engagement (não deliverables); o executive-report ganha slot opcional `revision_tripwires` (e o template pp idem — admin path). |
| C8 | `CLAUDE.md` + `ONBOARDING.md` | `/revisit` na tabela; walkthrough ganha nota pós-decide. |

### 5.3 Prompt da antítese (usar verbatim nas skills)

```
Estás na ronda dialéctica de <fase> <ronda> do engagement <slug>. A tua proposta diverge da
da persona <X> neste ponto: <divergência, citada verbatim com ids>.
Lê a tese completa dela (em anexo). A tua tarefa NÃO é defender a tua — é atacar a tese
mais forte dela com a melhor evidência disponível, e depois dizer honestamente:
(1) onde ela tem razão; (2) onde falha e porquê (com ids/inputs);
(3) a síntese que proporias se tivesses de assinar as duas.
Devolve nas secções: Concedo / Contesto / Síntese proposta. Máx. 300 palavras.
```

### 5.4 Formato de tripwire (bloco D-NNN em decisions.md)

```markdown
- **Tripwires (condições de revisão estruturadas)**:
  - TW-1: <condição mensurável, com fonte no SU> → se disparar, comparar com `_simulation/counterfactuals/<O-NNN>.md`
  - TW-2: …
```

### 5.5 Validação e aceitação (Vaga C)

1. Fixture até Framing com uma divergência plantada (duas personas com posições opostas sobre a prioridade) → verificar: chairman devolve a divergência, 2 Task calls de antítese correm em paralelo, síntese final cita Concedo/Contesto, e a divergência não-resolvida vira Conflicted row.
2. Até /decide → `_simulation/counterfactuals/` com ≥2 ficheiros; D-NNN com ≥2 tripwires estruturados.
3. Drill de tripwire: inserir no SU uma row que satisfaz TW-1 → `/status` alerta → `/revisit TW-1` produz a comparação e a recomendação SEM alterar a decisão.
4. Custo: contar os Task calls da ronda dialéctica (≤6).
5. Commit `feat: dialectic council + decision multiverse (v2.4 wave C)`; push; §10.

---

## 6. VAGA D — v3.0 "o council envelhece" (P5 + interrogável + docs + versões)

**Objectivo**: biografias, deliverable interrogável v1, documentação, bump de versões, validação final. **Sessão estimada**: 3 sessões.

### 6.1 Acções — biografias (P5)

| # | Ficheiro | Acção |
|---|---|---|
| D1 | `.claude/skills/aisa-retro/SKILL.md` + `commands/retro.md` | **NOVOS** — draft completo no Apêndice B. Nota-chave: a skill PREPARA os diários em `<engagement>/_retro/`; a entrada em `agent-memory/` só acontece com aprovação humana explícita (mantém a regra "memória editada pelos consultores"). |
| D2 | 8 agents (`.claude/agents/*.md`) + 7 lens skills | "Memory consulted" ganha `diary.md`; instrução nova: "quando um padrão do teu diário se repete, cita o caso («num engagement anterior de <domínio>, vi…») — nunca nomes de cliente fora do repo tenant". |
| D3 | `.claude/agent-memory/_universal/<persona>/diary.md` | Criar 7 ficheiros com header + formato de entrada (data, engagement-slug anonimizado, acertos, falhas, padrões, conselho) — vazios de conteúdo. |

### 6.2 Acções — deliverable interrogável v1

| # | Ficheiro | Acção |
|---|---|---|
| D4 | `.claude/skills/aisa-render/SKILL.md` | Flag `--html`: além do `.md`, gerar `<slug>_discovery-report_v<NN>.html` — HTML puro auto-contido (CSS inline, zero externos): cada citação de id vira `<span class="prov" title="<estado> · <evidência> · verificado <data>">C-014</span>`; secção final "Proveniência" com a tabela id→lens→evidência→validade; nota no topo "documento gerado do Shared Understanding — cada afirmação é rastreável". |
| D5 | `library/packs/pp/deliverable-templates/discovery-report.template.md` (admin) | Nota de template: o render `--html` aplica a projecção de proveniência a este deliverable primeiro (os outros ficam para v3.1). |

### 6.3 Acções — docs, versões, fecho

| # | Ficheiro | Acção |
|---|---|---|
| D6 | `library/kernel/*.md` (admin) | Headers → `Kernel v0.2.0`; `settings.json` env `AISA_KERNEL_VERSION: "0.2.0"`; `.env.example` idem. |
| D7 | `library/packs/pp/pack.yaml` (admin) | `pack_version: 1.2.0` (colunas novas de Unknown/Confirmed usadas pelas lenses justificam o bump). |
| D8 | `docs/ARCHITECTURE.md` | Entrada de changelog **v3.0.0** (as 5 peças, uma linha cada + refs a este plano); §3.2 estados com validade; §8 tabela de comandos (+/premortem /revisit /retro, render --html); §4 SU schema actualizado. NÃO reescrever o resto. |
| D9 | `docs/ONBOARDING.md` | Walkthrough final com os passos novos (saúde, agenda, premortem, tripwires, retro); troubleshooting: "saúde epistémica baixa" e "tripwire disparado". |
| D10 | `CLAUDE.md` | Tabela final de comandos; princípios: acrescentar o 9.º — "Knowledge expires; questions have prices; decisions keep their counterfactuals." |
| D11 | `docs/NEXT_LEVEL_PLAN.md` + `docs/IMPLEMENTATION_PLAN.md §16` | Marcar v3.0 entregue; apontar para o relatório de validação v3. |
| D12 | `docs/V3_VALIDATION_REPORT.md` | **NOVO** — relatório da validação final (§7), mesmo formato do `LIVE_VALIDATION_REPORT.md`. |

### 6.4 Validação e aceitação (Vaga D)

1. Protocolo completo do §7 (end-to-end com TODAS as peças).
2. `/retro` no fixture → 7 diários staged; simular aprovação; verificar append em `_universal/*/diary.md`; correr 1 lens e verificar citação de diário quando plantado um padrão repetido.
3. `--html`: abrir o ficheiro (Read) e verificar tooltips + tabela de proveniência + zero requests externos (grep `http` no html ⇒ só anchors internos).
4. Greps de regressão: vendor no kernel = 0 (excepto glossary pack-list); `bash -n` hooks; `AISA_KERNEL_VERSION` coerente em settings + .env.example.
5. Commits `feat: persona diaries + interrogable deliverable (v3.0 wave D)` e `docs: v3.0 documentation + validation report`; push; §10; sugerir tag `v3.0` ao Jorge (não criar tag sem confirmação).

---

## 7. Protocolo de validação live v3 (usado na Vaga D; versão reduzida nas A-C)

1. Recriar o fixture com o gerador do Apêndice D (`projects/galp-adv-val2` para não colidir com resíduos).
2. Sequência com verificação por passo:
   - `/start` → SU com colunas novas + story.md episódio 1.
   - `/round` → rows com verificado_em/validade; Unknowns com custo/swing.
   - `/status` → saúde epistémica + agenda da reunião (3 listas).
   - Forjar 2 expirações → `/status` reflecte; `/answer --revalidate` + `/answer` normal.
   - `/frame` com divergência plantada → ronda dialéctica (≤6 calls) → Conflicted se sobreviver.
   - `/options` → 7 personas; árvore aplicada.
   - `/simulate` → VOI citando classes de swing.
   - `/premortem` → obituário com ≥3 causas ancoradas; mitigações → tripwires candidatos.
   - `/decide` → D-NNN + row SU + counterfactuals congelados + tripwires estruturados.
   - `/blueprint` → v01 + aprovação.
   - `/render --all --html` → deliverables + html interrogável; gaps required = 0.
   - Drill: plantar disparo de TW-1 → `/status` alerta → `/revisit` compara e recomenda.
   - `/retro` → 7 diários staged → aprovação simulada → append.
3. Relatório `docs/V3_VALIDATION_REPORT.md` com a tabela de evidência (formato do LIVE_VALIDATION_REPORT).
4. O fixture fica gitignored; o relatório é a evidência durável.

---

## 8. Definition of Done — v3.0

- [ ] Vagas A–D `☑` no §10, cada uma com commit(s) + push + validação.
- [ ] Protocolo §7 completo, com relatório publicado.
- [ ] Kernel 0.2.0 + pack pp 1.2.0 + ARCHITECTURE changelog v3.0.0 + CLAUDE/ONBOARDING coerentes.
- [ ] Zero regressões: os greps de vendor-neutrality e os testes de guard do GAP_ANALYSIS continuam verdes.
- [ ] Lista de calibração §9 entregue ao Jorge com os defaults em uso (para a retro do pilot).
- [ ] Tag `v3.0` proposta ao Jorge (criada só com o seu ok).

---

## 9. Defaults de calibração (usar já; Jorge valida na retro — `TODO(team)` em cada ficheiro)

### 9.1 Meias-vidas por classe (kernel states.md)

| Classe | Meia-vida default | Exemplos |
|---|---|---|
| `legal-regulatorio` | 24 meses | retenção legal, obrigações de auditoria |
| `plataforma-tecnica` | 12 meses | limites de produto, capacidades de plataforma |
| `organizacional` | 6 meses (DEFAULT) | processos, políticas internas, org |
| `financeiro` | 6 meses | envelopes, taxas, chargeback |
| `pessoas-disponibilidade` | 3 meses | quem aprova, aceites individuais, disponibilidades |
| `volatil` | 1 mês | estados operacionais correntes (backlogs, pendências) |

### 9.2 Custos de pergunta (kernel states.md)

| Custo | Significado |
|---|---|
| `email` | resposta assíncrona simples (~minutos de sponsor) |
| `documento` | obter/ler um documento existente |
| `reuniao` | exige 30-60 min síncronos de sponsor/stakeholder |
| `spike` | exige trabalho técnico (dias) para responder |

### 9.3 Ainda pendentes do Jorge (herdadas, inalteradas)

Thresholds do decision-tree (R4-R6), rácios do estimation-model, `TODO(team)` do delivery-conventions, e — novo — as meias-vidas e o cap da ronda dialéctica (≤6 default).

---

## 10. Resume tracking (a sessão de build actualiza no fim de CADA vaga)

| Vaga | Versão | Status | Data | Commit(s) | Notas |
|---|---|---|---|---|---|
| A — metabolismo + pré-mortem | v2.2 | ☐ todo | — | — | — |
| B — economia da pergunta + narrativa | v2.3 | ☐ todo | — | — | — |
| C — dialética + multiverso | v2.4 | ☐ todo | — | — | — |
| D — biografias + interrogável + docs + validação | v3.0 | ☐ todo | — | — | — |

Regras: marcar `☑ done` só com validação verde; desvios e decisões in-flight registados aqui em nota; se uma vaga falhar aceitação, fica `☐` com a razão e a sessão seguinte retoma daí.

---

## Apêndice A — Draft de `.claude/skills/aisa-premortem/SKILL.md`

```markdown
---
name: aisa-premortem
description: Write the project's obituary before deciding — a post-mortem dated N months in the future explaining why the initiative failed, every cause anchored to SU ids (Risky, Assumed, open Unknowns, surviving tensions). Run in Options or Decision, before /decide; its mitigations become requirements and tripwire candidates.
---

# aisa-premortem

## Usage
`/premortem [--horizon <meses>]` (default: 12)

## Phase gate
Options ou Decision. Antes disso não há opções para matar — stop com mensagem clara.

## Inputs (read)
`_state.json`, `shared-understanding.md` (Risky, Assumed com validade fraca/expirada, Unknown abertas,
Conflicted resolvidas com tensão residual), `frame.md`, `options.md`, `_simulation/*` (a mais recente),
`decisions.md` (se já houver decisão, o obituário mira a opção escolhida; senão, a líder da simulação).

## Execution
1. Escolher o alvo (opção escolhida ou líder) e a data do obituário (hoje + horizon).
2. Construir 3–6 CAUSAS DE MORTE combinando (não repetindo) o material: cada causa é uma NARRATIVA de
   como 2+ fraquezas se combinaram (ex.: "a delegação nunca definida (U-011) encontrou o pico de Junho
   (R-001) e o SLA morreu no primeiro fecho de trimestre"). PROIBIDO: parafrasear rows Risky uma a uma.
3. Para cada causa: probabilidade subjectiva (baixa/média/alta), o primeiro sinal observável, e a
   mitigação — classificada como REQUISITO (entra no implementation-spec), TRIPWIRE candidato
   (entra no /decide), ou ACEITAÇÃO consciente.
4. Escrever `<engagement>/premortem.md` (overwrite; audit no council-log):
   # Post-mortem de <app/opção> — <data futura>  ("escrito" como se o projecto tivesse falhado)
   ## O que matou o projecto (causas narradas, ids inline)
   ## Os sinais que estavam à vista desde o início (ids)
   ## O que teria evitado (mitigação → classificação)
   ## Probabilidades e o que vamos fazer com isto
5. Appendar episódio ao story.md + linha ao council-log.
6. Output: as causas em 1 linha cada + "leva isto ao /decide: N tripwires candidatos, M requisitos".

## Hard rules
1. Cada afirmação ancora em ids — um obituário sem proveniência é ficção, não análise.
2. Tom: narrativa sóbria de post-mortem real, não lista. É para ser LIDO pelo sponsor antes de assinar.
3. Nunca bloqueia o /decide — é soft por construção; a skill de decide apenas o sugere.
```

## Apêndice B — Draft de `.claude/skills/aisa-retro/SKILL.md`

```markdown
---
name: aisa-retro
description: Close-of-engagement retro — each council persona writes its diary entry for this engagement (what its lens got right, where it was naive, patterns to watch, one advice to its future self). Entries are STAGED in <engagement>/_retro/ for human curation; only after explicit user approval are they appended to .claude/agent-memory/_universal/<persona>/diary.md (via normal git commit). Personas cite their diaries in future engagements.
---

# aisa-retro

## Usage
`/retro` — tipicamente após o render final (qualquer fase aceite, com aviso se cedo).

## Execution
1. Lançar as 7 personas em PARALELO (Task), cada uma com: o SU final, o seu lens-output acumulado,
   answers.md, decisions.md, premortem.md, e o seu diary.md actual. Prompt: "escreve a entrada de
   diário deste engagement: 2-4 parágrafos — (a) o que a tua lens apanhou que importou; (b) onde
   falhaste ou foste ingénuo (sê específico); (c) padrões que esperas rever noutros engagements;
   (d) um conselho ao teu futuro eu. Sem nomes de cliente; domínio genérico (ex.: 'procurement de
   mid-cap'). Formato: ## <slug-anonimizado> — <data>."
2. Guardar cada retorno em `<engagement>/_retro/diary-<persona>.md` (staged).
3. Apresentar ao utilizador o conjunto + pedir aprovação (aprovar tudo / editar / excluir personas).
4. SÓ após aprovação explícita: appendar cada entrada aprovada a
   `.claude/agent-memory/_universal/<persona>/diary.md` e recordar que agent-memory é tracked —
   commit via git é o caminho (a skill prepara o diff; o commit segue o fluxo normal do repo).
5. Episódio final no story.md ("o council fecha o caderno e guarda o que aprendeu") + council-log.

## Hard rules
1. NUNCA escrever em agent-memory sem aprovação humana nesta sessão — a regra do repo é
   "memória editada pelos consultores"; a skill só reduz o custo da curadoria.
2. Anonimização: zero nomes de pessoas/cliente nas entradas _universal; detalhe proprietário
   pertence ao _tenant (repo privado).
3. Diário é falível por design: registar erros é o objectivo — uma entrada só de vitórias é suspeita.
```

## Apêndice C — Draft de `.claude/skills/aisa-revisit/SKILL.md`

```markdown
---
name: aisa-revisit
description: Compare the present against a frozen counterfactual when a decision tripwire fires (or on demand): what the rejected branch would look like now, what switching would cost, and a recommendation (keep / adapt / reopen Options). Advisory only — it never changes the decision; reopening goes through the normal /options round.
---

# aisa-revisit

## Usage
`/revisit <TW-n | O-NNN>` — requer decisão tomada (D-NNN) e counterfactuals congelados.

## Execution
1. Ler o tripwire (decisions.md) ou a opção alvo; carregar `_simulation/counterfactuals/<O-NNN>.md`
   e o estado actual do SU (incluindo rows posteriores à decisão e validades).
2. Responder a 4 perguntas, cada uma com ids: (a) o tripwire disparou mesmo? com que evidência;
   (b) como estaria o ramo rejeitado HOJE (actualizar a projecção congelada com o que se sabe agora);
   (c) custo de mudar agora (migração, retrabalho, moral) vs custo de ficar;
   (d) recomendação: MANTER / ADAPTAR (a decisão sobrevive com ajuste, dizer qual) / REABRIR
   (justifica nova ronda /options).
3. Escrever `_simulation/revisit_<data>_<alvo>.md` + episódio no story.md + council-log.
4. Se REABRIR: sugerir `/options` (nova ronda O-NN) — NUNCA alterar decisions.md nem o SU sozinho.

## Hard rules
1. Advisory absoluto: a revisão de uma decisão é decisão humana, pelo mesmo caminho da original.
2. O counterfactual congelado nunca é editado — a comparação escreve um artefacto novo.
```

## Apêndice D — Gerador do fixture de validação (correr via Bash/python)

O fixture `galp-adv-val` (cenário: aprovação de adiantamentos a fornecedores; sponsor António Silva) é gitignored. Recriá-lo numa sessão nova (~2 min):

```python
# python3 <<'EOF'  — cria projects/<slug> com /start executado + inputs sintéticos
import pathlib, json, csv, random, os
random.seed(42); slug='galp-adv-val2'
root = pathlib.Path(f'projects/{slug}'); (root/'inputs').mkdir(parents=True); (root/'lens-outputs').mkdir()
ctx = {"engagement":slug,"literal_request":"Precisamos de digitalizar a aprovação de adiantamentos a fornecedores. Hoje é tudo Excel e Outlook e perde-se imenso tempo. Queríamos também poder aprovar no telemóvel.",
 "requester":{"name":"António Silva","role":"Director de Procurement","authority":"orçamento até 500k€; deploy exige IT"},
 "inputs":["meeting-notes.md","adiantamentos-2026-anonimo.csv"],"captured":"<hoje>T10:00:00Z"}
(root/'context.json').write_text(json.dumps(ctx,ensure_ascii=False,indent=2))
st={"engagement":slug,"pack":"pp","phase":"discovery","round":"R-00","aisa_version":"0.2.0","created":"<hoje>"}
t=root/'_state.json.tmp'; t.write_text(json.dumps(st,indent=2)); os.replace(t,root/'_state.json')
# SU skeleton: usar o schema NOVO de aisa-start (com verificado_em/validade e custo/swing)
for f,h in [('council-log.md','# Council Log'),('decisions.md','# Decisions'),('answers.md','# Answers'),('story.md','# Story')]:
    (root/f).write_text(f'{h} — {slug}\n')
(root/'inputs'/'meeting-notes.md').write_text('''# Notas — reunião inicial com António Silva (30 min)
- Hoje: pedido por email → Excel partilhado → aprovação por email, passo único do Director.
- Volume: ~47 aprovações/mês (número do AS). Equipa: 12 requisitantes.
- AS quer multi-nível no futuro ("acima de certo valor passa pela Finance").
- Aprovadores viajam; pedido explícito de mobile; alguém sugeriu "mesmo sem rede, no avião".
- Auditoria interna 2025 apontou falta de rasto nas aprovações por email (trilho auditável obrigatório).
- Objectivo: decisões "no próprio dia". Sem orçamento/prazo discutidos; "queria isto a andar ainda este ano".
''')
rows=[]
for i in range(1,61):
    v=random.choice([random.randint(500,9500)]*8+[random.randint(10001,48000)]*2)
    m=random.choice([3,3,4,4,5,5,6,6,6,6]); e=random.choice(["Aprovado"]*49+["Rejeitado"]*6+["Pendente"]*5)
    rows.append({"pedido_id":f"ADT-2026-{i:04d}","data_submissao":f"2026-{m:02d}-{random.randint(1,28):02d}",
     "fornecedor":f"F-{random.randint(1,22):03d}","valor_eur":v,"estado":e,
     "aprovador":random.choice(["A. Silva"]*55+["(em falta)"]*5),
     "dias_ate_decisao":random.choice([1,2,2,3,3,3,4,4,5,6,7,9]) if e!="Pendente" else ""})
with open(root/'inputs'/'adiantamentos-2026-anonimo.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
print(f"Fixture {slug} pronto. Próximo: correr /round conforme as skills.")
# EOF
```

O fixture contém, por construção, os ingredientes de teste: conflito de volume (47 declarado vs ~15/mês registado), 4 aprovações sem aprovador (gap de auditoria observável), pendentes de valor alto, e a tensão offline∧sensibilidade — o suficiente para exercitar Conflicted, dialética, VOI, pré-mortem e tripwires.

---

**FIM — v1.0.0.** Próxima acção da sessão nova: pré-flight §0.1 → Vaga A.
