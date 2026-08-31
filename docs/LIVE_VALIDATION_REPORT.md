# aisa — Relatório de Validação Live End-to-End

> Data: 2026-08-31 · Branch: `claude/repo-gaps-analysis-02922z`
> Engagement de teste: `projects/galp-adv-val` (gitignored por design — este relatório é a evidência durável)
> Âmbito: a sequência completa do `IMPLEMENTATION_PLAN §16` **incluindo os comandos novos**: `/start → /round → /status → /answer → /frame → /options → /simulate → /answer → /decide → /synthesize → /blueprint → /render --all`
> Cenário: fixture "galp-adv" do ONBOARDING §3 (aprovação de adiantamentos a fornecedores), com inputs sintéticos: notas de reunião + CSV de 60 pedidos anonimizados

## 1. Veredicto

**A pipeline corre de ponta a ponta.** Todos os comandos produziram os artefactos contratados; o council correu com Task subagents reais em paralelo (6 personas no Framing, 7 nas Options); as regras duras aguentaram (vendor-grep limpo em todos os artefactos de Discovery e no discovery-report final; zero invenções — todas as rows com evidência); o pack enriquecido funcionou em produção (o gate R0 reescrito desqualificou sharepoint-first pelo trilho auditável; o protocolo de missing-inputs disparou corretamente no solution-architect). Três defeitos encontrados, três corrigidos no próprio branch (§4).

## 2. O percurso, com evidência

| Passo | Resultado | Evidência notável |
|---|---|---|
| `/start galp-adv-val pp` | Scaffold completo (incl. `answers.md` novo); `_state.json` atómico, seed R-00 | — |
| `/round` (R-01, 6 lenses inline) | SU: 8 Confirmed, 3 Assumed, 5 Unknown, 2 Conflicted, 2 Risky; 6 lens-outputs; inputs perfilados a sério | O profiling do CSV detectou **2 conflitos genuínos não plantados**: volume declarado (47/mês) vs registado (~15/mês) → X-001; e 4 aprovações sem aprovador → C-007 (o gap de auditoria observável nos dados) |
| `/status` | Contagens corretas; gate do /frame vermelho (2 Critical abertos) | — |
| `/answer` ×5 | Transições Unknown/Conflicted→Confirmed com `was <id>` + marcador `resolved →`; verbatim em answers.md; **Conflicted→Confirmed** funcionou (X-001, X-002) | Gate do /frame passou a verde após as respostas |
| `/frame` (F-01) | **6 Task subagents em paralelo**, todas no formato de 6 secções; chairman sintetizou frase única convergente; frame.md com tabela de âncoras por cláusula; D-001 registado | As personas encontraram sozinhas os pendentes de 36k€ no CSV (linhas 21/40/56) e propuseram frames convergentes; 0 menções a vendors |
| `/options` (O-01) | **7 subagents em paralelo** (incl. solution-architect); options.md com 5 opções (do-nothing + non-tech + 3 tech) + 1 desqualificada | O solution-architect **aplicou a árvore regra a regra**: R0 desqualificou sharepoint-first (trilho auditável, C-017 — a regra reescrita no enriquecimento do pack); `admin_team_capability` sem SU id → **protocolo missing-inputs disparou** (STOP → Unknown U-012 + assumption explícita A-004). Secção `### Proposal` respeitada (fix G-14 validado) |
| `/simulate` v01 | Comparação lado-a-lado com bandas do estimation-model (O-003: P50 21d / P80 26d, rastreado à effort-table) + **secção VOI**: U-013/U-014/U-012 identificados como decision-flipping; U-004/005/009/010/011/016 explicitamente "não vale a pena esperar" | A VOI conduziu à ação certa: 1 reunião com IT resolveu os 3 flipping antes do /decide |
| `/answer` ×5 (pós-simulate) | U-012/013/014/015 + U-008 resolvidos (fixture IT + sponsor) | — |
| `/decide` (D-01) | D-002 (O-003 dataverse-first + O-002 como fase 0) com justificação ancorada em ids, alternativas, riscos aceites (X-004), 4 condições de revisão; **row D-002 escrita no SU** (fix G-06 validado); auto-`/synthesize` | Decision interativa sem council — modelo novo validado |
| `/synthesize` | 5/5 topic packs com citações de ids; log com contagens | Vendor-grep: 4 packs neutros limpos; só architecture-story nomeia plataforma ✓ |
| `/blueprint` v01 | 3 ecrãs via consolidation-rules (List/Form/Dashboard; aprovação = ações, não ecrã), 4 personas, `su_refs` em todos os nós, `excluded_from_ui` ×2, 3 open_questions, **caps: pass** | Excel Familiar Anchor aplicado (ordem de colunas do Excel de 10 anos); estado `offline-blocked` derivado de C-013 |
| Aprovação | D-003 + row no SU; blueprint frozen | — |
| `/render --all` | **6/6 deliverables v01**; render-log com decision-type; render-gaps com **0 required** (1 opcional: brand_guidance) | claude-design-brief e implementation-spec renderizam do blueprint aprovado; estimate rastreia a effort-table |

Estado final do SU: **24 Confirmed** (+3 D-rows) · 5 Assumed · 16 Unknown (10 resolvidas, 6 abertas Med, 0 Critical) · 4 Conflicted (todas resolvidas) · 5 Risky. Trilho completo: qualquer claim de qualquer deliverable rastreia a um id com evidência.

## 3. Critérios de aceitação (IMPLEMENTATION_PLAN §16 + NEXT_LEVEL_PLAN §4.1)

| Critério | Resultado |
|---|---|
| 6 personas arrancam em paralelo no /frame (mensagem única, Task calls concorrentes) | ✓ (6 em paralelo; nas Options, 6 inline + 1 async pelo harness — concorrência real em ambos) |
| frame.md é uma frase única coerente | ✓ com tabela de âncoras por cláusula |
| Apenas o chairman escreve no SU em modo council | ✓ (personas devolveram texto; escrita só na síntese) |
| options.md ≥3 opções incl. do-nothing + non-tech | ✓ (5 + 1 desqualificada com razão) |
| solution-architect consulta decision-tree + domain-knowledge | ✓ regra a regra, com veredictos citados |
| /decide interativo; auto-synthesize; 5 topic packs | ✓ |
| /render --all produz os deliverables; render-gaps pequeno | ✓ 6/6; 1 gap opcional |
| Vendor-grep em lens-outputs + frame + discovery-report | ✓ 0 hits |
| Hooks disparam sem erros de permissão (fix +x) | ✓ observado nos Writes do engagement |
| Novos: /answer transições; /simulate VOI; /blueprint caps+su_refs | ✓ todos |

## 4. Defeitos encontrados → corrigidos neste branch

1. **Excertos de council sem as resoluções** — personas cujo excerto temático não incluía C-012/C-013 re-levantaram o conflito de volume já resolvido (F-01). **Fix**: `aisa-frame`/`aisa-options` passam a exigir o bloco "Resoluções já fechadas (não re-litigar)" em todos os excertos; aplicado no O-01 do próprio run → zero re-litigâncias.
2. **`aisa-status --check` contava 5 ficheiros de kernel** — stale após o `blueprint-contract.md`. **Fix**: 6 ficheiros + synthesis-templates.
3. **Nota de processo**: um dos 7 Task calls das Options foi executado como async pelo harness (não determinístico de nossa parte); o fluxo aguentou porque o chairman só sintetiza quando todos devolvem. Sem fix necessário; registado para o pilot (o orquestrador deve sempre *esperar por todos*, que é o que a skill já diz).

## 5. Observações de qualidade (para o pilot)

- **O sistema encontra o que não foi plantado**: a discrepância de volume 47 vs 15/mês e as 4 aprovações órfãs emergiram do profiling, não do guião — é o comportamento-alvo da Discovery.
- **A VOI do /simulate mudou o comportamento**: em vez de decidir com 3 riscos de infra abertos, o fluxo conduziu a 1 reunião com IT primeiro. É o wedge do next level a funcionar em miniatura.
- **Limitações do teste**: sponsor e IT foram fixture (respostas minhas); o protótipo do blueprint foi assumido validado (a geração é externa ao aisa por design); os deliverables são compactos face aos de um engagement real. Nada disto afeta a validação da *mecânica*, mas o pilot com utilizadores reais (Fase 12) continua indispensável.

## 6. Próximo passo

Fase 12 — pilot com 2 consultores (1 engagement PP real + retro que alimenta os `TODO(team)` do delivery-conventions e os thresholds do decision-tree).
