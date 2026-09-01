# aisa — Relatório de Validação v3.0 (as 5 peças epistémicas)

> Data: 2026-09-01 · Branch: `claude/repo-gaps-analysis-02922z`
> Plano executado: `docs/V3_IMPLEMENTATION_PLAN.md` (vagas A–D → v2.2 / v2.3 / v2.4 / v3.0)
> Fixture: `projects/galp-adv-val` (gitignored por design — este relatório é a evidência durável) + micro-fixture `projects/exp-test` (metabolismo/agenda)
> Formato: o mesmo do `LIVE_VALIDATION_REPORT.md` (2026-08-31), que validou a base end-to-end sobre a qual estas peças assentam.

## 1. Veredicto

**As 5 peças epistémicas funcionam sobre a pipeline validada.** O conhecimento agora expira e revalida-se (metabolismo); cada Unknown tem preço e swing, e o `/status` produz a agenda da reunião (economia da pergunta); o `/premortem` escreve o obituário do projeto antes do `/decide` e as mitigações viram requisitos/tripwires; o chairman detecta divergências materiais e dispara ronda dialética real entre personas (tese→antítese→síntese); o `/decide` congela os counterfactuals das opções rejeitadas e arma tripwires que o `/status` vigia e o `/revisit` compara sem nunca reabrir sozinho (multiverso); e o `/retro` fecha o engagement com 7 diários falíveis por design, curados por humano, que as personas citam no engagement seguinte (biografias). A experiência ganhou o `story.md` (narrativa voz-sponsor) e o deliverable interrogável em HTML com proveniência navegável. Greps de regressão 5/5 verdes; linha vermelha mantida: o schema governa onde as coisas se arquivam, nunca o que pode ser dito.

## 2. A evidência, vaga a vaga

### Vaga A — v2.2 «o caderno ganha vida» (metabolismo + pré-mortem)

| O quê | Evidência |
|---|---|
| Meias-vidas (6 classes: legal-regulatorio 24m · plataforma-tecnica 12m · organizacional 6m DEFAULT · financeiro 6m · pessoas-disponibilidade 3m · volatil 1m) | `library/kernel/states.md` → *Epistemic half-lives*; colunas `verificado_em`/`validade` em Confirmed/Assumed |
| Saúde epistémica no `/status` | Micro-fixture `exp-test`: 33% → 100% após `/answer --revalidate` (renova `verificado_em` in-place — 2.ª edição sancionada) e transição `was` quando o facto mudou (nunca revalidar um facto que mudou) |
| Compatibilidade retroativa | SU antigo sem colunas ⇒ defaults aplicados **na leitura** (`verificado_em` = data da ronda, `validade` = organizacional); nunca migração do ficheiro |
| `/premortem` real (galp-adv-val) | 5 causas de morte **narradas**, cada uma combinando ≥2 fraquezas com ids do SU (proibição de parafrasear Risky cumprida); mitigações classificadas REQUISITO/TRIPWIRE/ACEITAÇÃO; 3 tripwires candidatos entregues ao `/decide` |

### Vaga B — v2.3 «as perguntas ganham preço» (economia da pergunta + narrativa)

| O quê | Evidência |
|---|---|
| Unknown com `custo` (email\|documento\|reuniao\|spike) e `swing` (decisivo\|dimensionante\|cosmético + frase) | Schema em `states.md` → *Question economics*; as 7 lenses têm a regra "price every Unknown" |
| Agenda da reunião no `/status` | 3 listas geradas no `exp-test` (perguntar já por email / levar à reunião / não gastar reunião com isto) |
| VOI do `/simulate` corrige classes | Drill: swing `cosmético` → `dimensionante`, correção anotada com proveniência |
| `story.md` (episódio por marco, voz sponsor, 4–8 frases, máx 2 ids) | galp-adv-val fecha com 6 episódios — do "primeiro dia" ao "council fecha o caderno" |

### Vaga C — v2.4 «o council discute e a decisão lembra-se» (dialética + multiverso)

| O quê | Evidência |
|---|---|
| Ronda dialética REAL (não simulada) | Chairman detectou divergência material sobre X-003 → hand-back → 2 antíteses em paralelo (business-analyst vs compliance-officer), ambas no formato Concedo/Contesto/Síntese ≤300 palavras; as sínteses **convergiram** («compliance é a espinha; mobilidade é o motor de adopção») → sem Conflicted novo; custo 2/6 calls (cap respeitado) — `lens-outputs/chairman-synthesis-F-01-dialectic.md` |
| Counterfactuals congelados no `/decide` | `_simulation/counterfactuals/{O-001,O-002,O-004,O-005}.md`, cada um com "condições em que ganharia"; nunca editados depois |
| Tripwires estruturados | D-002a com TW-1..TW-5 (dos candidatos do premortem) no bloco de decisão |
| Drill de disparo → `/revisit` | C-025 plantado (captura 38% < 50% ⇒ TW-2 dispara) → `/status` alerta → `/revisit TW-2`: 4 perguntas ancoradas ao counterfactual → recomendação **ADAPTAR** (U-010 + formulário de 3 campos + re-medição mês 2); decisão e congelado **intactos** (advisory absoluto) — `_simulation/revisit_2026-09-01_TW-2.md` |

### Vaga D — v3.0 «o council envelhece connosco» (biografias + deliverable interrogável)

| O quê | Evidência |
|---|---|
| `/retro` REAL com 7 subagents em paralelo | 7 diários staged em `<engagement>/_retro/diary-<persona>.md`; **todos com secção de falha específica e ids** (falível por design cumprido sem pushback): business-analyst «levantei U-005, chamei-lhe 'arqueologia habitual' e deixei-a morrer aberta»; data-steward «a cauda estava na minha coluna e foi o chair que a viu»; solution-architect «dei ao prazo cara de facto verificado» |
| Curadoria humana antes do append | Hard rule mantida na skill; neste drill a aprovação foi **simulada e anotada como fixture** (§6.4.2 do plano) — cada `diary.md` em `_universal/` leva o comentário de curadoria-drill para substituição na primeira curadoria real |
| Anonimização | 0 menções ao cliente nas 14 escritas (staged + append); header `## <domínio-anonimizado> — <data>` |
| Drill de citação (a memória fecha o ciclo) | business-analyst invocado num engagement sintético novo (reembolsos de despesas) que repetia padrões do diário: reconheceu e citou 3 («padrão recorrente na minha memória: driver a mascarar compliance», «volume visível é subconjunto», «stakeholders-sombra com veto») e acertou o headline (driver real = auditoria de março, não a "eficiência" declarada) |
| Deliverable interrogável (`/render --html`) | `_render/galp-adv-val_discovery-report_v01.html`: 13 029 bytes, HTML puro auto-contido; **28 ids** com tooltip `estado · evidência · verificado (validade)`; banner "gerado do Shared Understanding"; tabela final de Proveniência; **0 requests externos** |
| Fecho narrativo | Episódio 6 no `story.md` («o council fecha o caderno») + linha RETRO no `council-log.md` |

## 3. Critérios de aceitação (Definition of Done — plano §8)

| Critério | Estado |
|---|---|
| Vagas A–D ☑ no §10, cada uma com commit(s) + push + validação | ✅ (A: v2.2 · B: v2.3 · C: v2.4 · D: v3.0 — ver git log do branch) |
| Relatório de validação publicado | ✅ este documento |
| Kernel 0.2.0 + pack pp 1.2.0 + ARCHITECTURE changelog v3.0.0 + CLAUDE/ONBOARDING coerentes | ✅ (grep de versões verde: settings.json, .env.example, 6 headers do kernel) |
| Zero regressões (greps vendor-neutrality + testes de guard do GAP_ANALYSIS) | ✅ 5/5: vendor no kernel = 0 fora do glossary (1 match = pack-list, esperado); `bash -n` 5/5 hooks; versões coerentes; HTML sem externos; guard bloqueia `library/` (exit 2) e deixa passar o resto (exit 0) |
| Lista de calibração §9 entregue ao Jorge com defaults em uso | ✅ §5 abaixo |
| Tag `v3.0` proposta (criada só com ok) | ⏳ proposta na entrega — **não criada** |

**Desvio de protocolo registado**: o §7 pedia um full-run virgem com todas as peças em sequência. O que foi feito: drills **reais** por peça (subagents verdadeiros, não simulações) sobre o fixture `galp-adv-val` + o E2E completo da base validado em 2026-08-31 (`LIVE_VALIDATION_REPORT.md`). O full-run virgem com as 5 peças fica para o dia 1 do pilot (Fase 12) — é exatamente o que o pilot é.

## 4. Defeitos encontrados → corrigidos no próprio branch

1. **Numeração de regras nas lenses (Vaga B)** — o batch assumiu que o stamping era a regra 5 em todas as lenses; `lens-technology` tem 5 regras base, o que criou "6." duplicado em 6 lenses → renumerado (expired = 7 nas seis; technology: price = 7, expired = 8) e chairman editado por âncora alternativa (Step 4).
2. **Diários staged com trailer do harness (Vaga D)** — os tool results dos subagents traziam metadados (`agentId`/`usage`) que contaminaram os 14 ficheiros → limpos antes do fecho; verificação "remaining contamination: none".
3. **Nota de infraestrutura (não é do aisa)**: um Task call foi lançado async apesar de `run_in_background: false`; o fluxo do council aguenta porque o chairman só arranca depois de todas as personas devolverem.

## 5. Calibração — defaults em uso (Jorge valida na retro do pilot; `TODO(team)` nos ficheiros)

1. **Meias-vidas** (`library/kernel/states.md`): legal-regulatorio 24m · plataforma-tecnica 12m · **organizacional 6m (DEFAULT)** · financeiro 6m · pessoas-disponibilidade 3m · volatil 1m; override por pack em `pack.yaml → epistemics.half_lives_override` (pp: vazio).
2. **Thresholds da decision-tree pp** (R0–R6, hybrid-trigger) — reescritos na v1.1.0, à espera de casos reais.
3. **Rácios de estimação** (bandas de esforço do `/simulate` e do estimate) — indicativos.
4. **`delivery-conventions.md`**: todos os `TODO(team)` (naming, ALM, connection references, go-live checklist) capturam-se na retro do pilot.
5. **Cap dialético** (3 divergências × 2 calls): nunca foi stressado — a primeira ronda real convergiu com 2/6; vigiar no pilot.

## 6. Observações de qualidade (para o pilot)

- **A citação de diário funciona mas não usa a frase-template verbatim** («num engagement anterior de <domínio>, vi…» → o agente escreveu «padrão recorrente na minha memória»). A intenção — proveniência do padrão — cumpre-se; a frase é advisory. Se quiserem a forma exata, promover a frase de sugestão a formato obrigatório na definição dos agents.
- **Nenhum diário veio "só de vitórias"** — a regra "falível por design" segurou sem a curadoria ter de devolver entradas. Manter o olho: com o tempo, personas com memória podem começar a auto-justificar-se.
- **A convergência dialética à primeira** é bom sinal e mau teste — o mecanismo de sobrevivência (divergência → Conflicted novo) só foi exercido pelo caminho "não sobreviveu". O pilot deve observar o primeiro Conflicted nascido de dialética.
- **O HTML interrogável cobre só o discovery-report** (âmbito v3.0 por plano); estender aos restantes deliverables é decisão de v3.1.

## 7. Próximo passo

1. **Pilot (Fase 12)** com 2 consultores num engagement real: dia 1 = full-run virgem com as 5 peças (fecha o desvio do §3); a retro do pilot alimenta a calibração do §5 e a primeira curadoria real de diários (substituindo as entradas-drill anotadas).
2. Tag `v3.0` no repo — proposta, à espera do ok.
3. Roadmap além-v3.0: o que ficou deliberadamente de fora está em `V3_IMPLEMENTATION_PLAN.md §0.4` (linha 6 — scanner H2, operação assíncrona, pack não-software, deliverable interactivo em v3.1) e em `NEXT_LEVEL_PLAN.md §4`.
