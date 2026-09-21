# Plano consolidado — Discovery · Estimate · Implementation Spec

> **Errata (2026-09-11)** — o P-0 descrito neste plano lista os cinco temas de pricing como se fossem universais. O intake em vigor tem **sete temas genéricos** (T1..T7, `library/kernel/phases.md` → *Enquadramento (P-0)*) e os de pricing passam a **conjunto condicional**, activado por uma pergunta explícita ao dono. Este documento fica como registo; o contrato em vigor é o do kernel.

> Data: 2026-09-08
> Substitui, como plano de acção, os três documentos de diagnóstico de 2026-09-08: `DISCOVERY_CRITICAL_REVIEW.md` (D/F), `ESTIMATE_TARGET_FORM_REVIEW.md` (E-D/E/R), `IMPLEMENTATION_SPEC_HANDOFF_REVIEW.md` (G). Os três ficam intactos como histórico do raciocínio; a revisão adversarial que motivou esta consolidação está em `PLANS_ADVERSARIAL_REVIEW.md`.
> Contagens: `library/kernel/tools/dashboard.py --json` sobre `projects/pricing-marinha-pilot-3` (o modelo que `/status` consome). Nunca contagem manual.
> Estado: **plano**. Nenhuma alteração de código feita. Decisões do owner fixadas em §2.

---

## 0. Factos (motor, pilot-3, 2026-09-08)

| Métrica | Valor | Nota |
|---|---|---|
| Rows totais | 313 | 156 C · 29 A · 85 U · 9 X · 34 R |
| `Unknown` abertas | **41** | 44 resolvidas |
| `Unknown` Critical abertas | **9** | 4 `documento` · 2 `spike` · 2 `email` · 1 `reuniao` |
| `Unknown` abertas por `custo` | 27 `email` · 7 `reuniao` · 5 `documento` · 2 `spike` | |
| `Unknown` abertas por `swing` | 31 `dimensionante` · 8 `decisivo` · 2 `cosmético` | |
| `Unknown` abertas por lens | 11 data · 8 operations · 6 governance · 6 business · 5 user · 5 financial | |
| Criadas / fechadas por ronda de origem | R-01 34/22 · R-02 14/6 · R-03 15/7 · R-04 22/9 | as 4 rondas correram em 2026-09-07 |
| Saúde epistémica | 100 % · 0 expiradas | |
| `PM-U` em `process-model.md` | 39 | |

Três correcções ao diagnóstico anterior que decorrem destes números:

1. O gate `Unknown Critical = 0` **é alcançável**: 9 rows, 8 delas sem reunião.
2. O Discovery **fecha** — 44 de 85 no mesmo dia. O que não existe é a **medida** do rácio por ronda no output do `/round` e do `/status`.
3. As três perguntas que o doc de Discovery apontava como úteis da lens `financial` (`U-075`, `U-071`, `U-062`) **estão resolvidas** (`C-153`, `C-118`, `C-136`). O problema da `financial` não é volume: é mandato (5 abertas, 4 delas de envelope/ROI: `U-030`, `U-032`, `U-034`, `U-072`; e `U-033`, a única Critical `reuniao` do engagement).

E um facto que os três documentos não viram, e que é o mais caro do pilot:

4. **O mecanismo de negócio que dá sentido ao pedido chegou na R-04, ditado pelo dono do processo.** `C-137` (*"desfasamento entre a semana do preço e a semana do carregamento"*) e `C-136` (*"não é venda perdida, é valorização errada"*) têm evidência `USER_ANSWER 2026-09-07 — declaração do dono do processo, via AskUserQuestion`, sem locator em `inputs/`. Até lá: `U-007` (R-01, Critical, `reuniao`, `decisivo`), `X-001` e `X-005` (R-01), 4 `Assumed` em R-03 a inferir o porquê da exposição de 2ª e 3ª feira. Três rondas a inferir sobre o **sintoma** (remendo de projecção, arrastar ontem) sem o **porquê** (a venda da semana seguinte é valorizada à média das cotações desta semana). Rows sobre o tema, por ronda de origem: R-01 4 · R-02 1 · R-03 14 · R-04 30.

5. **`Confirmed` aceita afirmações acima da evidência.** Amostra de 30 `Confirmed` de pilot-3 (uma em cada cinco, ordem do ficheiro), dois testes:

| Teste | Falham | Rows |
|---|---|---|
| Classe da fonte (fórmula/prosa no Excel · transcrição · docx · dono) | 2 / 30 | `C-155`, `C-126` — resolvidas por raciocínio do executor, sem dono |
| Afirmação ao nível da evidência | **7 / 30** | + `C-147` (facto técnico confirmado por negócio), `C-097` ("não existe método" a partir de duas fórmulas), `C-111` ("é o motor de esforço"), `C-101` ("criado a partir do anterior", inferido), `C-021` ("todo o modelo" a partir de "padrão dominante") |

Todas as 156 citam uma das quatro classes; o problema não é a fonte, é a distância entre evidência e afirmação. 6 das 7 são R-04 — a subida acontece quando a ronda encadeia raciocínio sobre rows anteriores. Extrapolado: ~36 rows deviam ser `Assumed`. `states.md` linha 9 aceita ainda "industry-standard claim" como evidência de `Confirmed`.

6. **O runtime tem 12 defeitos de mecânica e identidade, independentes do conteúdo** — `docs/ADVERSARIAL_REVIEW_2026-09-08.md`, snapshot `beb9afc`. Re-executadas as 7 reproduções de `docs/review-evidence/` no HEAD `940a8cc`: **7/7 confirmam**; as 5 contradições de contrato confirmam por leitura do código. Nenhum toca a qualidade do Discovery ou dos entregáveis (âmbito das frentes A–D); dois condicionam-nas: **F06** (o guard de ordem bloqueia a segunda chamada `/round <lens>`) invalida qualquer validação da frente A feita lente a lente; **F03** (o replay marca fórmulas válidas como defeito) alimenta `PM-U` falsas que P-3 classificaria como `dados`. Nenhum finding cobre os 10 commits da frente A (`1279f00..82990c4`): o código mais recente não foi atacado. Suite completa inconclusiva por PyYAML em falta.

---

## 1. Diagnóstico único

Um defeito estrutural em cada camada, ligados em cadeia:

| # | Camada | Defeito | Sobrevive de | Evidência |
|---|---|---|---|---|
| **P-D0** | Início | Nenhum momento em que o **dono do processo declara o mecanismo de negócio** antes da ronda 1. `context.json` tem pedido literal e requerente; o `_capture` deriva um sinopse do artefacto. O porquê fica para as lentes inferirem | D4 (a intuição certa, a correcção errada), F1 (a fonte errada) | §0 ponto 4: `C-137` em R-04 por `USER_ANSWER`; `U-007` Critical `reuniao` em R-01 |
| **P-D1** | Discovery | Nenhuma `Unknown` tem de traçar a uma decisão ou a um requisito do to-be; o único teste é interno à lens ("consequence", indefinido, `lens-*/SKILL.md` step 5) | D1, D2, U-070 | `U-070` aberta: `dimensionante`, com frase de invariância que a própria lens escreveu e aprovou |
| **P-D2** | Discovery | `swing` não tem árbitro antes de Options; `/simulate` corrige, mas só na fase 3 | D2 | `states.md` l.77; `aisa-simulate` step 4 |
| **P-D3** | Discovery | Convergência não é medida nem reportada | D3 (corrigido) | JSON do motor já tem `ronda` × `resolved`; ninguém o lê no `/round` |
| **P-D4** | Discovery | `PM-U` de mecânica de ficheiro sobe a pergunta humana sem teste de conteúdo | D5 | `U-070` ← `PM-U-026` (protecção de folha); mas `U-075` ← `PM-U-003` (folhas escondidas) era pergunta certa |
| **P-D5** | Discovery | Mandato `financial` pressupõe portão de financiamento; o modelo operativo deste cliente não o tem | §5 | 4 de 5 abertas são envelope/ROI |
| **P-D6** | Discovery → downstream | Nenhuma lens recolhe **campos** (nome, tipo, obrigatoriedade) nem **tempos por passo** do as-is; a spec e a estimativa ficam sem fonte | G1 §3.1(a), E-D5 | 0 das 85 `Unknown` menciona campo/tipo/schema; `operational_impact` sai `not applicable` |
| **P-S1** | Spec | Dicionário de dados sem dono contratado; `fields_itemized` inventado pelo blueprint; `_capture` sem caminho autorizado | G1, G2 (restrito) | `grep fields_itemized library/ .claude/` = 0; `forbidden_sources` inclui `_capture/*` |
| **P-S2** | Spec | Gap check testa presença, não suficiência; motor é stub | G3 | `render-validate.py`: "v0.2.0 will validate slot completeness" |
| **P-S3** | Spec | Transições de estado caem entre §4 e §6 | G5 | blueprint v01 `state_machine` + `approval: true`; §6 `(none)` |
| **P-S4** | Spec | Template de 406 linhas de proibições, sem forma-alvo; causa da perda de densidade **não demonstrada** (comparação entre engagements de classe diferente) | G4, §6 (rebaixado) | `dpt-galp-jp` = SharePoint-first, colunas do Excel eram os campos; `pricing-marinha` = keep-in-place externo |
| **P-E1** | Estimate | Sem granularidade abaixo da fase, sem responsável por fase, sem ocupação por perfil | E-D1, E-D2 (rebaixado) | `estimate_v02` §5: fase · dias · dependências; §15: perfil · dedicação · fases |
| **P-E2** | Estimate | Riscos bem estruturados mas não chegam à fase que ameaçam; pré-condições diluídas em premissas | E-D4, E-D8 | §9 vs §5; §13 |
| **P-E3** | Estimate | Sem drivers de volume por unidade | E-D3 | depende de P-S1 |
| **P-E4** | Estimate | Sem padrão de staging de âmbito | E-D7 | `delivery_recommendations` só sequencia |
| **P-D8** | Entrada | Não existe caminho para quem **não começa por `/start`**. Uma mensagem em linguagem natural ("quero melhorar o processo de pricing") não recebe enquadramento do que o aisa vai fazer, dos passos, nem do que se espera do utilizador. `ONBOARDING.md` (487 linhas) é para consultor/developer com setup; não há uma página para quem só usa | owner 2026-09-08 | `CLAUDE.md` não tem regra de entrada sem comando; `grep -i "linguagem natural" CLAUDE.md` = 0 |
| **P-D9** | Todas | A linguagem que chega ao utilizador é a do kernel: `swing`, `PM-U`, `disposição`, `tripwire`, `epistémico`, `council`, `lens`, `undisposed`, `meia-vida`, `SU`. O próprio owner que orientou a construção não a percebe sempre. `glossary.md` define os termos para quem constrói, não diz como se dizem a quem usa | owner 2026-09-08 | `aisa-status/SKILL.md` step 4–9 imprime `Tripwires`, `swing`, `saúde epistémica`; `aisa-round` step 6 imprime `Undisposed: PM-U-NNN`; único precedente correcto: `story.md` "na voz do sponsor, sem jargão de kernel" |
| **P-D7** | SU (todas as fases) | O limiar de `Confirmed` testa a classe da fonte, não o nível da afirmação; resolução por "evidência interna" do executor entra como `Confirmed`; "industry-standard claim" é evidência aceite | regra do owner 2026-09-08, amostra §0 ponto 5 | 7/30 acima do nível (6 em R-04); 2/30 sem dono; `states.md` l.9 e l.17 |
| **P-R1** | Runtime · SU | Ids calculados uma vez por ronda (`aisa-round` 3.6c); lentes seguintes recebem o mesmo próximo id. Consumidor (`dashboard.py`) aceita duplicados, fica com o último, `diagnostics=[]` | F01 | repro `parsed_rows=2, drawer_entries=1`; **zero duplicados reais** nas 3 pilots |
| **P-R2** | Runtime · dashboard | `running_server` reata a qualquer servidor na porta do lock; não compara engagement | F02 | repro pediu A, leu `{"client": "B"}` |
| **P-R3** | Runtime · capture | Replay: XLOOKUP ignora `search_mode` (`args[5]`); COUNTIF trata wildcards como literal. Falsos `stale`/`miss` viram findings | F03 | repro REVERSE_XLOOKUP, WILDCARD_COUNTIF; `xlsx_extract.py` 1032–1043, 1094–1098 |
| **P-R4** | Runtime · síntese | `synthesis_state` usa `max()` de todos os tópicos: um tópico fresco valida a arquitectura velha | F04 | `dashboard.py` 2061; repro `stale_vs_approval=false` |
| **P-R5** | Contrato · Framing | `/options` só testa que `D-001` existe; frame regenerado em F-02 passa com aprovação de F-01 | F05 | `aisa-options` pré-flight 2; `aisa-frame` idempotência |
| **P-R6** | Contrato · Discovery | `/round <lens>` persiste a ronda; o guard exige as lentes anteriores na ronda **seguinte**; a segunda chamada bloqueia | F06 | repro exit 2; `pre-lens-order-check.py` 123–137 |
| **P-R7** | Contrato · Decision | `/revisit` → `REABRIR` → `/options`; `/options` rejeita `phase=decision` | F07 | `aisa-options` pré-flight 1; `aisa-revisit` step 4 |
| **P-R8** | Contrato · render | `solution-blueprint` lê `v<approved>`; a secção de candidatas só existe com escolha estrutural, que bloqueia aprovação | F08 | template 139, 209–214; `blueprint-contract.md` regra 5 |
| **P-R9** | Contrato · simulate | P50/P80 exigidos; `estimation-model.md` não tem distribuição nem quantis; `×1.4` sem fonte | F09 | `aisa-simulate` step 2; grep P50 em `estimation-model.md` = 0 |
| **P-R10** | Contrato · simulate | Simulação parcial pode despromover `swing` global | F10 | `aisa-simulate` VOI |
| **P-R11** | Runtime · capture | `text_extract` reutiliza cache `failed`/`skipped`; `xlsx_extract` já exige `status == ok` | F11 | repro FAILED_CACHE; `text_extract.py` 384–391 vs `xlsx_extract.py` 596 |
| **P-R12** | Runtime · dashboard | `inline_md` não valida esquema do URL: `javascript:` passa | F12 | repro SCRIPT_URI; `dashboard.py` 1234 |
| **P-R13** | Runtime · guard | `pre-write-guard.py` compara `library` case-sensitive; `LIBRARY/` passa em Windows. Protecção do `deny` em `settings.json` **não verificada** | obs. adicional | repro GUARD_CASE exit 2/0 |

**Cadeia:** P-D0 explica P-D1 (sem mecanismo declarado não há a que traçar uma pergunta, e o único denominador disponível é a perspectiva da lens). P-D1 explica P-D2 e P-D4 (sem denominador, toda a etiqueta e toda a `PM-U` passam). P-D6 explica P-S1 e P-E3 (o que não se recolhe não se renderiza). P-S2 explica porque nada disto aparece como lacuna.

---

## 2. Decisões fixadas (owner, 2026-09-08)

| Tema | Decisão | Consequência |
|---|---|---|
| Lens `financial` | **Flag `funding_gate` em `context.json`**, sem rename | F6a descartado. A `false`: cues `budget_envelope`, `capex_opex`, `funding_model`, `payback_roi` inactivos; mandato fica em `as_is_cost`, `do_nothing_cost`, `cost_of_delay`, `cost_sensitivity`. `cfo-lens` (council) lê a mesma flag. Perfil por tamanho (F6b) adiado até haver 2.º engagement que o justifique |
| Dono do dicionário de dados | **Architecture record**, bloco A5 `record_authority[]` | G1a e G1b descartados. `fields[]` para autoridade interna; `access_contract` para `keep-in-place`/`virtualized`. Gate no `/render`, não no blueprint. Blueprint fica UI |
| Mecânica do Excel (`PM-U`, named ranges, colunas) | **Um só critério, duas fases**: em Discovery sobe a `Unknown` só se muda **forma ou volume dos dados do to-be**; em Decision/Architecture o inventário L1 é **fonte autorizada de rascunho** de `fields[]` para autoridade **interna** | F5 e G2 reconciliados. Para `pricing-marinha` (externo) o L1 não gera schema; gera a lista de campos **lidos/escritos** para o `access_contract` |
| Enquadramento inicial | **`enquadramento.md` + rows `Confirmed` R-00 na SU** (owner, 2026-09-08) | P-0. O dono do processo declara o **mecanismo de negócio** antes da ronda 1, via entrevista `AskUserQuestion` no `/start`. Invariantes `M-n` em linguagem de negócio, fonte = declaração do dono. As lentes citam o `M-n` que cada `Unknown` serve. `/frame` valida-os com evidência |
| Frame provisório a partir do pedido (F1) | **Substituído por P-0** | F1 extraía `asks` do `literal_request`, que é solution-shaped ("alternativa ao Excel"); `ASK-3` aceitaria tudo. P-0 muda a **fonte** (o humano, não o texto do pedido) e o **conteúdo** (mecanismo, não pedido). O denominador de P-1 passa a ser `M-n` **ou** divergência no to-be |
| `decisivo` em Discovery (F3) | **Mantido**, com referente obrigatório | A frase tem de nomear o **frame candidato ou branch** que a resposta elimina; sem referente → `dimensionante`. Árbitro em P-1. Sem hook |
| Calendário na estimativa (E2) | **Só ocupação por perfil**, sem grid semanal | pessoa-dias ÷ dedicação → semanas mínimas por perfil; sobreposições **não** derivadas. Equipa vem de pré-condição declarada (P-8), não de inferência |
| Tarefas por fase (E1) | **Bandas, sem soma forçada** | tarefas só em fases ≥ 5 dias; cada tarefa com banda; soma das bandas contém o total da fase. Total global não muda |
| Economia de portfólio (E6) | **Nota, não correcção** | fora do engagement por arquitectura. Fica como frase em `delivery_recommendations` quando `context.json` nomear engagements irmãos |
| Regressão do template (G-§6) | **Hipótese a testar**, não facto | P-11 antes de qualquer edição ao template |
| Utilizador ≠ construtor | **O framework é para quem não o construiu** (owner, 2026-09-08) | P-13 e P-14. Tudo o que o utilizador lê ou responde vai em linguagem de negócio; o vocabulário do kernel fica nos ficheiros e nos ids. Uma mensagem em linguagem natural é uma entrada válida: recebe enquadramento, passos e o comando seguinte |
| Limiar de `Confirmed` | **Regra combinada** (owner, 2026-09-08, após amostra de 30): locator resolúvel por máquina **e** afirmação ao nível da evidência **e** confirmação humana só do dono do processo; "industry-standard claim" sai | P-12. A regra do owner (quatro classes de fonte + validação humana) é a base; a amostra mostrou que a classe da fonte apanha 2/30 e o nível apanha 7/30, logo os dois testes entram. `Assumed` com base declarada continua a ser o estado preferido para interpretação |
| Integridade do runtime | **Frente E**, separada de A–D (owner, 2026-09-08) | P-15 a P-18 mais três emendas (F09 → P-9, F10 → P-1, `LIBRARY/` → guard). Prioridade pela dependência com as outras frentes, não pelo P1/P2 da revisão: F06 e PyYAML antes de validar A; F03 antes de P-3 depender de classes `PM-U`. F01 reparte-se: consumidor é urgente (diagnóstico), protocolo é uma linha. Cada script de reprodução vira teste de regressão com a expectativa invertida |

---

## 3. Correcções consolidadas

Cada uma: o que resolve · o que toca · teste de aceitação. Ids `P-n`. Rastreabilidade em §8.

### P-0 — Enquadramento do mecanismo de negócio (resolve P-D0; dá denominador a P-1)

**O que é.** Antes da ronda 1, o dono do processo declara, por palavras suas, como o negócio funciona no ponto que o pedido toca: o que se vende e quando; quando se fixa o preço e quando acontece a venda; o que determina o custo; o que determina a valorização; de onde vem a incerteza e como evolui no tempo; o que se faz hoje com ela; o que o pedido quer mudar nisto. Não é o pedido. É o invariante que o pedido serve.

**Exemplo canónico** (pricing-marinha, declaração do dono, 2026-09-08 — a leitura que o Discovery devia ter tido no dia zero):

> *"Eu defino um preço hoje, para uma venda que só se vai verificar na próxima semana. Uma venda hoje é valorizada à média das cotações da semana anterior."*
>
> Consequências, também declaradas pelo dono: o custo de cedência é indexado a cotações Platts; a venda da semana seguinte é por isso valorizada à média das cotações **desta** semana, a semana em que o preço se fixa; à 2ª e 3ª feira conhecem-se 0–1 dessas cotações, à 6ª conhecem-se 4 e o diferencial já não é expressivo; **não se perde venda — pode-se não estar a valorizar ao que se devia**. Logo o pedido "estimar as projecções de 2ª e 3ª" é estimar o **fecho da média semanal**, não prever o mercado.

Em `M-n`:

| id | invariante | o que orienta |
|---|---|---|
| M-1 | O preço fixa-se hoje **como referência** para uma venda que se verifica na semana seguinte. A valorização real do custo dessa venda só fecha na 2ª feira da semana seguinte, quando as cotações desta semana completa estiverem fechadas. Uma venda na semana N é valorizada à média das cotações da semana N-1 | toda a pergunta sobre cadência, janela de 9:30, publicação de duas semanas, e sobre **quando** o custo de uma venda fica conhecido |
| M-2 | A venda é valorizada à média das cotações da semana anterior à venda — isto é, da semana em que o preço se fixa | o alvo da projecção é o fecho da média, não a cotação do dia |
| M-3 | O custo de cedência é indexado a Platts | fontes de cotação, feed, momento de conhecimento |
| M-4 | A incerteza decresce ao longo da semana (0–1 cotações à 2ª, 4 à 6ª) | o problema é de 2ª e 3ª; qualquer solução mede-se aí |
| M-5 | O efeito é valorização errada, não venda perdida | o KPI é margem apurada vs valorizada; volume não entra |

> **Canónico = `projects/pricing-marinha-pilot-3/enquadramento.md`** (decisão 3 do step-9b, 2026-09-08): M-1 foi corrigido pelo dono por palavras suas na entrevista do step-9a; a citação verbatim acima é a origem histórica, a tabela já reflecte a correcção. M-2..M-5 confirmados tal como estão.

**Mecânica.** `aisa-start` ganha o step *Enquadramento*, depois do pedido literal e antes do `/capture`: entrevista via `AskUserQuestion` (uma pergunta por tema acima; "Other" para texto livre), resposta verbatim guardada. Escreve `<engagement>/enquadramento.md` (cabeçalho: dono, data, pedido literal; corpo: declaração verbatim; tabela `M-n · invariante · o que orienta`). Cada `M-n` entra na SU como `Confirmed`, `lens = enquadramento`, `ronda = R-00`, evidência `declaração do dono do processo, enquadramento.md#M-n`, `validade = organizacional` (precedente: `A-001` em pilot-3). O `/round` passa `enquadramento.md` na invocação das lentes ao lado de `context.json`.

**Regras.** O enquadramento é a hipótese do dono, não facto verificado: `/frame` **confirma ou corrige** cada `M-n` com evidência (transição normal `was C-nnn`). O `/start` não infere `M-n` a partir do `literal_request` nem do `_capture` — só regista o que o humano disse; sem dono disponível, `enquadramento.md` diz *"não declarado"* e as lentes trabalham como hoje. Sem vendor, sem produto, sem solução: se o dono nomear uma, fica no verbatim e não entra em `M-n`.

**Toca:** `aisa-start/SKILL.md`; `aisa-round/SKILL.md` (linha de invocação); `phases.md` (entry criteria de Discovery: `enquadramento.md` existe, soft); `states.md` (lens `enquadramento`, ronda `R-00` legítimas); `dashboard.py` (reconhece `R-00`).

**Aceitação:** escrever `enquadramento.md` de pilot-3 com os M-1…M-5 acima e classificar as 85 `Unknown` (abertas e resolvidas) em três grupos: *serve um M-n* · *diverge no to-be sem M-n* · *nenhum*. O terceiro grupo é o custo que P-0 teria evitado. Em seguida, `/round` numa cópia com `enquadramento.md` presente: nenhuma `Unknown` nova pergunta o porquê da exposição de 2ª e 3ª; as que perguntam pelo **como** (que cotações, que feed, que regra de empolamento) citam M-2/M-4.

### P-1 — Teste de divergência **arbitrado** (resolve P-D1, P-D2)

**Regra** (nos 6 `lens-*/SKILL.md`, *Hard rules*, substitui o actual step 5 "no consequence"):

> Antes de escrever uma `Unknown`, cita o invariante `M-n` de `enquadramento.md` que a resposta serve, ou declara no campo `swing` as respostas possíveis e o que cada uma muda **no requisito, na forma dos dados ou no esforço** do sistema a construir. Se todas conduzem ao mesmo requisito, a pergunta é `cosmético` — escreve-a como `cosmético` ou não a escrevas. Diferença só no as-is não é diferença. Se a divergência é inferível com base declarada, escreve `Assumed` com a base; `Unknown` é para o que a inferência não alcança. `decisivo` exige nomear o frame candidato ou branch que a resposta elimina; sem referente, é `dimensionante`.

**Custo as-is (decisão 1 do step-9b, resolve a tensão P-1 × P-4 aberta na onda 0).** P-1 mantém as três diferenças. O custo as-is, o custo de não fazer e o custo de atraso são a *baseline* da lente `financial`, escritos como `Assumed` com base (mandato de P-4), não perguntados. Uma `Unknown` de custo é `decisivo` só se nomear o branch que a magnitude elimina ou mantém vivo — tipicamente `do nothing`, que é opção em Options, logo o kernel já cobre o caso sem quarta diferença —, `dimensionante` se muda esforço ou forma dos dados do to-be, senão `cosmético`, incluindo quando a decisão de construir já está tomada. Em `states.md` → *Question economics* → *Cost questions*.

**Árbitro** (`aisa-round/SKILL.md`, novo step 5f, depois de todas as lentes): o orquestrador relê **só as `Unknown` criadas nesta ronda** e, para cada uma, verifica três coisas mecânicas — (i) cita um `M-n` existente **ou** o `swing` nomeia ≥ 2 respostas; (ii) nomeia a diferença no to-be (dispensado quando cita `M-n`); (iii) `decisivo` nomeia um referente. Falha em (i) ou (ii) → reclassifica para `cosmético` (edição de metadados sancionada, mesma classe da correcção do `/simulate`, registada no `council-log.md` como `swing corrigido: U-nnn dimensionante → cosmético (sem divergência no to-be)`). Falha em (iii) → `dimensionante`. O orquestrador **não apaga rows nem julga materialidade**: verifica a presença das três declarações.

**Toca:** 6 `lens-*/SKILL.md`; `aisa-round/SKILL.md` step 5; `states.md` *Question economics* (uma frase: `decisivo` exige referente nomeado; o árbitro de ronda é sancionado como o de `/simulate`).

**Aceitação:** reclassificar à mão as 41 abertas de pilot-3 com a regra e com os M-1…M-5 de P-0; registar quantas viram `cosmético`. Depois, `/round` numa cópia: toda a `Unknown` nova tem as três declarações ou foi reclassificada com registo. `U-070` fica `cosmético` (preservar e criar dão o mesmo requisito; a pergunta boa é "quem pode alterar a composição de um preço", e essa é `Assumed`-able a partir de `C-052`).

### P-2 — Convergência reportada (resolve P-D3)

`/round` step 6 e `/status` passam a mostrar, a partir do JSON do motor: `Unknown criadas nesta ronda · fechadas nesta ronda (qualquer origem) · abertas totais · Critical abertas`. Uma ronda com `criadas > fechadas` é etiquetada `sem convergência` — visível, não bloqueante.

`phases.md` Discovery *Exit criteria*: `Unknown Critical = 0` **mantém-se** (é alcançável). Acrescenta-se um critério soft: `última ronda com criadas ≤ fechadas`. Nenhuma etiqueta nova, nenhum conceito de "bloqueante".

**Toca:** `dashboard.py` (expor `round_delta` no JSON — já tem os dados), `aisa-round` step 6, `aisa-status`, `phases.md`.

**Aceitação:** `/status` em pilot-3 mostra R-04: 22 criadas / N fechadas; o número bate com `dashboard.py --json`.

### P-3 — `PM-U` de mecânica: teste de conteúdo (resolve P-D4; reconcilia F5 com G2)

`orchestration.md` *Comprehension survival*, parágrafo *Material semantic disposition*, acrescenta:

> Uma `PM-U` sobre mecânica do artefacto (protecção, folhas escondidas, formatos, nomes de range, contagens) recebe `ADOPT` só quando a lens declara qual **forma, volume ou regra de dados do to-be** muda com a resposta. Se só muda o controlo ou o aspecto do artefacto velho, `DISMISS — mecânica do as-is`. O inventário L1 permanece fonte autorizada de rascunho de campos em Architecture (P-6).

**Toca:** `orchestration.md`; `aisa-capture` (a `PM-U` gerada leva `classe: mecânica | dados | processo`, string determinística a partir da origem do sinal — `protected_sheets`/`state`/formatos → `mecânica`; `columns`/`named_ranges`/`validations` → `dados`; síntese §4 → `processo`).

**Aceitação:** `PM-U-026` (protecção) classifica `mecânica`; `PM-U-003` (folhas escondidas moeda×unidade, 212 vs 465 colunas) classifica `dados` e continua a subir. Nenhuma `PM-U` Critical desaparece sem disposição.

### P-4 — `funding_gate` (resolve P-D5)

`aisa-start` step 6 escreve `"funding_gate": true|false` em `context.json` (pergunta ao utilizador via `AskUserQuestion`: "A decisão de avançar depende de aprovação orçamental?"). Default quando ausente: `true` (comportamento actual).

`lens-financial/SKILL.md`: step 2 e signal catalog condicionados — a `false`, não constrói envelope, não pergunta funding/limiares/CAPEX-OPEX; mantém custo as-is, custo de não fazer, sensibilidade, e o que hoje o negócio faz sozinho e passaria a depender de fila (`U-071` era isto). `cfo-lens.md` recebe a flag na invocação.

**Toca:** `aisa-start`, `lens-financial`, `cfo-lens.md`, `aisa-round` (passa a flag), `chairman-synthesis` (não exige monetização do frame quando `false`).

**Aceitação:** pilot-3 com `funding_gate: false`: `/round financial` numa cópia não gera nenhuma `Unknown` de envelope/limiar/imputação; `U-030`, `U-032`, `U-034`, `U-072` reclassificam `cosmético` neste engagement (registo no `council-log.md`).

### P-5 — Mandato de campos e de tempos (resolve P-D6)

**Campos** — não é Discovery. Entra em **Decision/Architecture**, quando o `record_authority[]` está fixado: o `/blueprint` já lê `lens=data` para `entities`; o **`/blueprint` step 2** (ao autorar `record_authority[]`) e o `--refresh` produzem o rascunho de A5 `fields[]` / `access_contract` (P-6) e marcam-no `Assumed` por linha até confirmação; o `/synthesize` **carrega** a tabela em `architecture-story.md ## Data` (carrier, nunca autoridade). *(Emenda E3, onda 0 de D: em `/decide` não existe `record_authority[]`; texto anterior dizia `/decide` → `/synthesize`.)* Em Discovery a `lens-data` ganha **uma** cue nova, `data_shape` (grão, dimensões, volume por entidade — o que `U-075` já era), não atributos.

**Tempos por passo** — `lens-operations` ganha cue `step_duration` e a instrução: "quando o as-is tem passos nomeados, regista tempo por passo como `Assumed` com base (transcrição, observação) ou `Unknown` `custo=email`". `_synthesis/as-is.md` ganha a coluna `tempo` na tabela de passos (template em `synthesis-templates/`). É a fonte contratada de P-10.

**Toca:** `lens-data`, `lens-operations`, `synthesis-templates/as-is.md`.

**Aceitação:** `as-is.md` de pilot-1 re-sintetizado tem tempo por passo (ou `Unknown` nomeada) para os passos do ciclo diário; `C-030` (< 1h/dia) aparece como total.

### P-6 — Dicionário de dados no architecture record (resolve P-S1)

`architecture-core.md` A5 `record_authority[]` ganha dois sub-blocos, exclusivos por `access_mode`:

- cada entrada ganha `key` (slug único no scope) e `entities[].authority: <key>` substitui `fields_itemized` — a junção ecrã → entidade → domínio → campos que P-7 verifica;
- autoridade **interna** (`owned`): `fields[] { name · name_basis · type · values · required · default · index · set_by · rules · state · source · disposition }`;
- autoridade **externa** (`keep-in-place`, `virtualized`): `access_contract { reads[] · writes[] · readonly · key[] · join_keys[] · dictionary_entries_without_data[] · delegation_safe_paths[] · mandatory_filters[] · store_facts · confidentiality · forfeits[] }` + `schema_owner {value · state · su_ref · open}`; `replicated` leva ambos (`fields ⊆ reads`).
- **Estado por linha**: toda a linha de `fields`/`reads`/`writes` tem `state` (`Assumed`/`Confirmed`/`Unknown`) e `source` (locator P-12). Forma completa: `docs/pp-pack-authoring/pilot/step-9a-onda-0-desenho-a5.md` §4.

**Motor** (novo, `library/kernel/tools/fields_draft.py`): lê `*.extraction.json` e escreve **`_capture/<ficheiro>.fields-draft.json`** (artefacto do capture, determinístico, `source_sha256` no cabeçalho — locator de classe 1; **nunca escreve no YAML do blueprint**, que é de autoria LLM e o `v05` aprovado de pilot-1 nem parseia). Regras: nome por prioridade **`named_range → formula_ref → header → none`** *(emenda E4: `header → name` falha em `Inputs`, C-017, e em `Outputs`, 4 cabeçalhos em 76)*; `inferred_type → type` (`str→text`, `number`, `datetime`, `mixed→unknown`, `empty→unknown` com `evidence: header only`, `str`+validação `list` → `choice` com `values[]`); `nulls == 0 → required (draft)`; `key_like → identifier` + `index: candidate`; classes reais do L1 `input|manual|derived|empty` → `writes` / `reads`·`computed` com `lineage[]` / entradas sem dados; `validations → rules`; named ranges `A_B_C` → `dimensions[]` com cardinalidade (a separação métrica/porto e contraparte/prefixo técnico é julgamento da skill). Itens por **coluna**, com `aliases[]` (pilot-1: 291 nomes = 145 pares distintos → 83 colunas; 42 entradas distintas para colunas vazias). `default` nunca inferido. Output é `Assumed` por linha; a skill julga e dá **disposição** `ADOPT`/`MAP`/`DISMISS` a toda a coluna do L1 (princípio 10); o sponsor confirma. Invocado por `aisa-blueprint` step 2 e `--refresh`, idempotente por `sha256` — não corre no `/capture` do `/start` (decisão do dono, 2026-09-09).

`implementation-spec.template.md`: `slot_sources.entities_to_create` passa a `A5 record_authority[].fields[] | access_contract`; `_capture/*` sai de `forbidden_sources` **apenas** para a transformação declarada `L1 column inventory → fields[] draft (Assumed)`. Blueprint deixa de ser fonte de entidades; fica fonte de ecrãs. `fields_itemized` removido do blueprint.

**Toca:** `architecture-core.md`, `fields_draft.py` (novo), `aisa-blueprint` (invoca o motor no step 2 e `--refresh`; remove `fields_itemized`; escreve `authority`), `aisa-synthesize` (carrega a tabela em `architecture-story.md ## Data`), `implementation-spec.template.md`. *(E3: `aisa-decide` sai da lista.)*

**Aceitação** *(emendas E1, E2 — `step-9a-onda-0-desenho-a5.md` §8)*: pilot-1 sobre o registo mais recente (`v06`, ou `v07` se entretanto houver respostas): os **6 domínios externos** têm `access_contract` com `reads[]`/`writes[]` por coluna do L1 (`costs-margins` 26 escritas `manual` = 38 do L1 − 12 `AçoreanaMutualista_*` `DISMISS` por C-052; `daily-quotes` 39 + 7 sem nome; `daily-price` 59 `computed` com `lineage`, `readonly: true`); o domínio **`owned`** (`workflow-audit`, autoridade em aberto U-040) e o novo `scenarios` (cenários gravados, decisão do dono 2026-09-09) têm `fields[]` 100 % `name_basis: design`; as 10 entidades resolvem `authority` (nenhuma sem domínio); `schema_owner` = `Assumed` (C-057) com `open: U-036` — **não** «equipa da BD de `A-001`» (`A-001` é a corrupção do Excel). §4 do render tem colunas *lidas · escritas · chave* e linha `⚠️ lacuna` onde a autoridade não cobre. `dpt-galp-jp` (sem `_blueprint/`): **cobertura de fonte** — os 18 + 7 campos de v01 têm fonte ∈ {L1, SU, design}, classe `none` = 0; `Prioridade.values` e `Exec_Order.required` saem do motor sem julgamento; as ≥ 8 colunas do L1 que v01 não carrega têm disposição.

### P-7 — Gap check por suficiência, como motor (resolve P-S2)

`render-validate.py` deixa de ser stub. Regras determinísticas por slot, lidas de um bloco `sufficiency:` no frontmatter de cada template:

- `entities_to_create`: cada entidade interna com ≥ 1 campo tipado **e** `fields ⊇` colunas `primary/secondary` que os `screens` do blueprint referenciam a essa entidade; cada externa com `reads[]` não vazio. Falha → lacuna `required` em `render-gaps.md`, não slot preenchido.
- `flows_to_implement`: `(none)` só se nenhuma entidade tem `state_machine` ou `approval: true`.
- `security_implementation`: existe uma tabela Papel × (Ecrã | Entidade) no corpo; citação do craft não conta.
- `integrations`: mecanismo de autenticação e custódia de segredos presentes, ou lacuna nomeada.

**Toca:** `render-validate.py`, os 6 templates (bloco `sufficiency:`), `aisa-render` (lê o resultado do hook, não o substitui).

**Aceitação:** re-render de pilot-1 v02 sem mais nada alterado produz ≥ 3 lacunas `required` (§4 campos, §6 fluxos, §8 matriz). Hoje produz 0.

### P-8 — Transições de estado e pré-condições com dono (resolve P-S3, P-E2 parte)

Spec: quando `experience.mode != none` e uma entidade tem `state_machine` ou `approval: true`, §6 carrega obrigatoriamente *quem transiciona · o que valida · o que notifica quem · o que dispara o ciclo*, mesmo sem streams assíncronos em A6.

Estimate: `estimate_assumptions` fica só para premissas de método; disponibilidade de SME, acessos, licenças e aprovisionamento rendem com a carriage de `build_gates` (*condição · dono · até quando · que fase trava · estado*), lidas de A8/A10 e de `decisions.md`. A equipa declarada aqui é o input de P-9.

**Toca:** `implementation-spec.template.md` (§6 `slot_conditions`), `estimate.template.md` (novo slot `estimate_preconditions`, `estimate_assumptions` restringido).

**Aceitação:** pilot-1: §6 da spec deixa de ser `(none)`; a estimativa lista SME 20 % e acesso à BD partilhada como pré-condições com dono e fase travada.

### P-9 — Tarefas em banda e ocupação por perfil (resolve P-E1)

`phases_table`: por fase ≥ 5 dias, sub-tabela *tarefa · banda (min–max) · perfil*; soma das bandas contém o total da fase; total global inalterado. Coluna *perfil responsável* na tabela de fases.

Novo slot condicional `profile_load`: por perfil de `team_effort`, `pessoa-dias ÷ dedicação → semanas mínimas`; engajado só quando P-8 declara a equipa. Nenhum grid, nenhuma sobreposição derivada; se a spec §14 tem dependências, lista-as como restrição ao paralelismo, em prosa.

`named_uncertainties`: cada item aparece também, numa linha, na fase que ameaça.

`delivery_recommendations`: quando a decomposição tem dimensão de repetição ≥ N (parques, produtos, clientes), recomenda piloto sobre subconjunto nomeado.

**Toca:** `estimate.template.md`.

**Aceitação:** re-render de pilot-1: cada fase ≥ 5d tem tarefas em banda cuja união contém o total; ocupação por perfil ≤ dedicação declarada; total 44 pessoa-dias **inalterado**; cada item de §9 aparece numa fase.

### P-10 — Drivers de volume e impacto operacional (resolve P-E3, restante P-D6)

`work_breakdown` ganha coluna `driver` citando **a spec §4** (`n campos · n lidas · n escritas · grão · volume`, que A5 carrega em `grain`/`volume` com locator L1 ou SU). A estimativa **nunca** cita `_capture/*` nem a SU directamente — `forbidden_sources` e `test_operational_impact_is_sourced_from_the_active_modes_inventory_only` proíbem-no; logo §4 da spec **renderiza os números** para a estimativa os citar.

`operational_impact` *(emenda E5)*: a aresta `_synthesis/as-is.md# passos com tempo` (de P-5) entra na **Implementation Specification** como fonte condicional de uma tabela *alteração de caminho operacional* — *passo · quem · tempo actual · novo processo · tempo novo · Δ* — onde «novo processo» sai de A5 (`writes[].by` × `cadence` × `volume`) e «tempo actual» de `as-is.md`. A estimativa continua a ler **só** o inventário da spec (`estimate.template.md` proíbe `as-is.md` «NOT required, NOT conditional, NOT fallback, NOT point-of-need», congelado pela frente B). Renderiza o que os dados dão — se o as-is é < 1h/dia, o Δ é pequeno e fica escrito. **Não** é a secção que justifica o investimento quando `funding_gate: false`; é a secção que quantifica o que muda para quem executa.

**Toca:** `implementation-spec.template.md` (fonte condicional `as-is.md# passos`, tabela de caminho operacional, números em §4), `estimate.template.md` (coluna `driver` em `work_breakdown`); depende de P-5 e P-6.

**Aceitação** *(emenda E6)*: pilot-1 `operational_impact` — hoje **§17** da estimativa (a frente B inseriu §16 *Equipa e esforço por perfil*) — deixa de ser `not applicable` ou diz exactamente qual passo não tem tempo.

### P-11 — Experiência de template antes de tocar no template (resolve P-S4)

Renderizar `pricing-marinha-pilot-1` §4 com a instrução antiga de uma linha (*"One row per entity: name, owner, fields, relationships, indexes"*), sem mais nada alterado. Três resultados possíveis, três acções:

- saem campos → o template de 406 linhas dilui a atenção: **cortar** proibições redundantes antes de acrescentar exemplos;
- não saem campos → a causa é upstream (P-6 resolve); G4 fica só como anexo curto de forma por secção (1 exemplo cada, ≤ 5 linhas), referência `plano-automacao-pricing-oil-es-tobe.text.md` §2–§7 e §9;
- saem campos inventados → o contrato é o que os impede; **não** cortar.

**Toca:** nada permanente; um render `--dry-run` em cópia.

### P-12 — Limiar de `Confirmed` (resolve P-D7)

**Regra** (`states.md`, substitui a linha `Confirmed` da tabela de estados e a decision rule *Confirmed vs Assumed*):

1. **Locator resolúvel por máquina**, numa de quatro classes:
   - `<ficheiro>.xlsx|xlsm#<folha>!<célula|coluna>` — fórmula explícita (`custo + margem = preço`) ou texto em prosa na célula; contagens e estrutura do extractor citam `<ficheiro>.extraction.json#<folha>` ou `<ficheiro>.replay.md#<n>`;
   - `<ficheiro>.vtt#[hh:mm:ss]` — passagem explícita de transcrição;
   - `<ficheiro>.docx#¶n` — passagem explícita de documento;
   - `answers.md#A-nnn` ou `enquadramento.md#M-n` — declaração do **dono do processo**, registada pelo executor via `AskUserQuestion`, com data.
   Sem locator numa destas classes, não é `Confirmed`.
2. **Afirmação ao nível da evidência.** Fórmula → "o artefacto calcula / contém"; transcrição ou docx → "X afirmou em [t] / o documento diz"; dono → facto de negócio **dentro da sua autoridade**. Sobe um nível — regra de negócio a partir de fórmula (`C-097`), facto a partir de afirmação de terceiro (`C-087`), facto técnico de sistema alheio confirmado por negócio (`C-147`), conclusão de cadeia de rows (`C-155`) — é `Assumed`, base = os locators. A inferência continua a ser o trabalho do LLM; muda o estado em que se regista, não a liberdade de a fazer.
3. **Confirmação humana só do dono do processo**, ou de quem ele nomear como autoridade sobre o tema (registado em `enquadramento.md`). O executor confirma factos do **engagement** — âmbito autorizado, decisões de registo — marcados como tal (`[ÂMBITO AUTORIZADO]`, precedente `A-001`). Resolução de `X-`/`R-` por "evidência interna, sem resposta de sponsor" (`C-126`) → `Assumed was X-nnn`, nunca `Confirmed`.
4. **"industry-standard claim" sai** da coluna de evidência de `Confirmed` (`states.md` l.9); passa a base legítima de `Assumed`.
5. Transição `Assumed → Confirmed` ("Validation done") passa a exigir o locator da validação — declaração do dono ou evidência nova das classes 1.
6. **Terceira edição sancionada** (decisão 2 do step-9b): completar o locator da evidência de uma row cuja evidência já nomeia a fonte mas não a âncora (`answers.md#<secção>`, `.extraction.json#<folha>`), sem tocar no claim, em lote registado no `council-log.md`. Regra da âncora de `answers.md`: primeiro segmento do título da secção antes de « — », espaços → hífens (`answers.md#U-073`, `answers.md#BLOCO-H`); `aisa-answer` escreve-a sempre.

**Mecânica.** Duas metades, uma por natureza:

- **Determinística** — hook novo `su-confirmed-guard.py`, `PostToolUse` sobre Write/Edit em `shared-understanding.md` (ao lado de `on-su-change.py`, mesmo padrão: nunca bloqueia, exit 0): para cada row `C-` nova, verifica por regex a presença de um locator das quatro classes **e** que o alvo existe (`inputs/`, `_capture/`, `answers.md`, `enquadramento.md`). Falha → aviso no output e linha `Confirmed sem locator: C-nnn` em `council-log.md`. `dashboard.py` ganha a faceta `sem locator` no JSON e no `/status`.
- **Julgamento** — a regra 2 vai para os 6 `lens-*/SKILL.md` (*Hard rules* 2 e 3, reformuladas) e para o árbitro de P-1 (step 5f): segunda leitura das `Confirmed` novas com a pergunta "a afirmação diz mais do que a evidência?". Sim → **não é edição de metadados**: é transição de estado, append-only — nova row `A-nnn was C-nnn` com base = locators, row original marcada `— resolved → A-nnn`, registo no `council-log.md`.

**Toca:** `states.md` (tabela, decision rules, transições, coluna de evidência); 6 `lens-*/SKILL.md`; `aisa-answer` (resolução por evidência interna → `Assumed`); `aisa-round` step 5f; `su-confirmed-guard.py` (novo) + `settings.json`; `dashboard.py`.

**Aceitação:**
1. As 7 rows da amostra recebem `A-nnn was C-nnn`; as 23 ficam.
2. ~~Hook sobre pilot-3 lista `C-155`, `C-126` e as "declaração em reunião" sem locator (`C-131`, `C-120`, `C-114`) como avisos — e nada mais das 156.~~ **Reescrita (onda 0 mediu 40 rows `USER_ANSWER` sem âncora, não 5; step-9b completou as 40 e transitou C-155/C-126 para `Assumed`):** hook sobre pilot-3 após o step-9b lista **só `C-002`** (`context.json.literal_request` — excepção aceite na regra 1) **e `C-026`** (contagens do extractor sem célula — completar com `.extraction.json#<folha>`), ou zero se as duas forem completadas; e nada mais das rows existentes. Calibrar falsos positivos em `dpt-galp-jp` e `cae-automation` antes de ligar em `settings.json`.
3. `/round` numa cópia de pilot-3: nenhuma `Confirmed` nova sem locator; toda a conclusão de cadeia entra como `Assumed`.
4. Invariante: nenhuma row apagada; contagem `Confirmed + Assumed` inalterada pela reclassificação.

### P-13 — Duas línguas: a do kernel nos ficheiros, a do negócio para o utilizador (resolve P-D9)

**Princípio.** O vocabulário do kernel é preciso e fica: nos ficheiros, nos ids, nos contratos. O que **o utilizador lê ou responde** — output de qualquer comando, perguntas `AskUserQuestion`, `story.md`, dashboard, deliverables — vai em linguagem de negócio, sem termo do kernel que não venha acompanhado da frase que o explica. O precedente já existe e é o certo: `story.md`, *"na voz do sponsor, sem jargão de kernel, máx. 2 ids citados"*.

**Mecânica.**

1. `glossary.md` ganha a coluna **"como se diz ao utilizador"**. Exemplos:

| Termo do kernel | Como se diz |
|---|---|
| `Unknown` · `Assumed` · `Confirmed` | pergunta em aberto · o que estamos a assumir (e porquê) · o que está verificado (e onde) |
| `swing: decisivo / dimensionante / cosmético` | a resposta muda o caminho / muda o tamanho / não muda nada — não gastes reunião nisto |
| `custo: reuniao / email / documento / spike` | precisa de reunião / resolve-se por email / está num documento / precisa de trabalho técnico |
| `PM-U` · `disposição` · `undisposed` | pergunta que o ficheiro levantou · o que fizemos com ela · ainda ninguém olhou para esta |
| `tripwire` | condição que, se acontecer, obriga a rever a decisão |
| `saúde epistémica` · `meia-vida` · `expirada` | quanto do que sabemos ainda está em prazo · até quando um facto vale · precisa de reconfirmar |
| `lens` · `council` · `chairman` | perspectiva (negócio, operações, utilizador, dados, controlo, custo) · as perspectivas em paralelo · quem junta as conclusões |
| `SU` / Shared Understanding | o registo do que sabemos |
| `ronda` | uma passagem das perspectivas pelo material |
| `frame` · `options` · `decide` · `blueprint` · `render` | a frase do problema · as alternativas · a escolha · o desenho dos ecrãs · os documentos finais |
| `gate soft` · `override` | aviso antes de avançar · avançar mesmo assim, com razão registada |

2. **Regra de output** em `CLAUDE.md` e em cada `SKILL.md` de comando (`status`, `round`, `resume`, `frame`, `options`, `decide`, `blueprint`, `render`, `answer`, `start`): a linha final e qualquer resumo para o utilizador usam a coluna "como se diz"; ids (`U-nnn`, `C-nnn`, `D-nnn`) aparecem entre parênteses depois da frase, nunca sozinhos; termos do kernel só entre parênteses depois da frase de negócio, na primeira ocorrência.
3. **`AskUserQuestion`**: pergunta e opções em linguagem de negócio; o id e o termo do kernel na `description`, não no `label`.
4. **`/status`**: já tem `next_action`; passa a abrir com três linhas — *onde estamos* (fase, em palavras) · *o que falta para o próximo passo* · *o que tens de fazer tu* — antes de qualquer tabela.
5. **Dashboard**: tabs e cabeçalhos pela coluna "como se diz"; o termo do kernel em tooltip.

**Toca:** `glossary.md`; `CLAUDE.md` (regra de output); os SKILL.md de comando (linha de output); `dashboard.py` (labels); templates de deliverable (já são para audiência externa — verificar apenas).

**Aceitação:** teste de leitura — o output de `/status`, `/round` e `/resume` sobre pilot-3, lido por alguém que não construiu o aisa, permite dizer **o que fazer a seguir e porquê** sem abrir nenhum ficheiro. Critério mecânico: zero termos da coluna esquerda do glossário nas linhas de output sem a frase da coluna direita ao lado.

### P-14 — Entrada em linguagem natural: enquadramento do processo e dos passos (resolve P-D8)

**O caso.** O utilizador não escreve `/start`. Escreve *"precisamos de ajuda a melhorar o processo de pricing, o Excel corrompe-se…"*. Hoje isso não é uma entrada. Passa a ser a entrada principal.

**Mecânica** — regra em `CLAUDE.md` (secção nova *Entrada sem comando*) e uma skill curta `aisa-orient`, invocada quando a mensagem descreve um processo, um problema ou uma intenção de começar e não há comando:

1. **Enquadramento do aisa, em 5 linhas de negócio**: o que vai acontecer (ouvir o dono, ler os ficheiros, fazer perguntas em passagens, chegar a uma frase do problema, comparar alternativas, escolher, desenhar, entregar documentos), quanto tempo de quem, e o que se espera do utilizador em cada passo (responder a perguntas, validar, decidir).
2. **Os passos, na ordem, com o comando de cada um** — mas o utilizador não precisa de os decorar: cada output termina com *"a seguir: …"* (P-13).
3. **Entrevista de enquadramento** (P-0), imediatamente — o mecanismo de negócio é a primeira coisa a recolher, e o utilizador já está a falar dele.
4. **Proposta de arranque** via `AskUserQuestion`: nome do engagement (slug proposto a partir do que foi dito), tipo de solução em vista se já declarado (pack), ficheiros a fornecer. Confirmado → `/start` corre com o `enquadramento.md` já preenchido.
5. **Se já existe engagement** e a mensagem é sobre ele ("já decidimos, quero a estimativa"): `aisa-orient` faz o que `/resume` faz hoje e diz, em linguagem de negócio, o que falta antes do que o utilizador pediu (ex.: "a estimativa vem depois da escolha e do desenho dos ecrãs; estamos na fase das alternativas — falta escolher").
6. **`ONBOARDING.md`** mantém-se para consultor/developer. Nova página `docs/COMO-USAR.md`, ≤ 1 página, para quem usa: o que é, o que dá, o que se espera de mim, como começo (basta descrever o processo), como sei o que fazer a seguir (o final de cada resposta diz).

**Regras.** Sem vendor nem produto no enquadramento (princípio 1). O `aisa-orient` nunca cria ficheiros por si: recolhe, propõe, e é o `/start` que escreve. Se a mensagem é ambígua entre começar e perguntar, pergunta via `AskUserQuestion` — nunca assume.

**Toca:** `CLAUDE.md`; `aisa-orient/SKILL.md` (novo, pequeno); `aisa-start` (aceita `enquadramento.md` pré-existente); `resume` (delega a linguagem em P-13); `docs/COMO-USAR.md` (novo).

**Aceitação:** sessão nova, sem comando, colar o `literal_request` de pilot-3 como mensagem. Resultado esperado: enquadramento em 5 linhas, os passos, a entrevista de P-0, a proposta de `/start` com slug — tudo sem um termo do kernel sem tradução. Segundo teste: com pilot-1 aberto, escrever "quero a estimativa" → resposta diz em que passo estamos e o que falta, e oferece o comando certo.

### P-15 — Ronda em curso ≠ ronda concluída; ambiente de testes completo (resolve P-R6; desbloqueia a validação de A)

**Regra.** `_state.json` distingue `round` (última **concluída**) de `round_in_progress` (aberta por `/round <lens>`, fechada quando a última lente da ordem escreve ou por `/round --close`). `aisa-round` step 3 reutiliza `round_in_progress` quando existe; o guard lê-a em vez de `round + 1`. `/round` sem argumento continua a abrir e fechar na mesma chamada.

**Engagement explícito no guard** (descoberto em operação, 2026-09-08, duas cópias `pilot-3-val-opus` / `pilot-3-val-sonnet` em ronda simultânea). `pre-lens-order-check.py` resolve o engagement pelo mais recentemente tocado entre os que estão em Discovery; com dois `/round` em paralelo verifica a cópia errada e pode bloquear falsamente (`exit 2`, "lens-X has not written output for round R-NN") ou deixar passar. A invocação da lente já carrega `engagement root <engagement>` na primeira linha: o hook lê o root de `tool_input.args` e só cai no "mais recente" quando ausente. Teste: dois engagements em Discovery, lentes desalinhadas, o hook verifica o certo.

**Ambiente.** `requirements-dev.txt` com PyYAML; `.claude/tests` corre completo antes de qualquer "validado" nas frentes.

**Toca:** `aisa-round` steps 3 e 5a; `pre-lens-order-check.py`; `dashboard.py` (lê `round_in_progress`); `aisa-start` (seed); `repro-round-order.py` → teste de regressão.

**Aceitação:** `/round business` seguido de `/round operations` numa cópia de pilot-3 corre sem bloqueio e ambas as lentes carimbam a mesma ronda; suite completa de `.claude/tests` verde.

### P-16 — Identidade e higiene do motor (resolve P-R1, P-R2, P-R11, P-R12)

Quatro correcções de motor, independentes, cada uma com o script de reprodução invertido como teste:

- **P-R1** — `dashboard.py` rejeita id duplicado na SU: `diagnostics` ganha `id duplicado: C-nnn (linhas a, b)` e o drawer mostra ambos marcados. Protocolo: `aisa-round` 3.6c recalcula o próximo id **antes de cada lente** (as lentes correm em sequência; custa um scan da SU).
- **P-R2** — `/__build` devolve `{slug, pid, started}`; `running_server` só reata quando `slug` e `pid` batem com o lock; o cliente compara `slug` antes de renderizar.
- **P-R11** — `text_extract.py` só aceita cache com `status == "ok"` (espelha `xlsx_extract.py` 596); `failed`/`skipped` repetem com o motivo no log.
- **P-R12** — `inline_md` só emite `href` para `http(s):`, `mailto:` e caminhos relativos; outro esquema renderiza como texto.

**Toca:** `dashboard.py`; `aisa-round` 3.6c; `text_extract.py`; 4 testes novos.

**Aceitação:** as 4 reproduções falham nas assertions actuais e passam nas invertidas; pilot-3 continua com `diagnostics=[]`.

### P-17 — Replay honesto sobre os seus limites (resolve P-R3; protege P-3)

XLOOKUP com `search_mode` ≠ `1`/vazio e COUNTIF com `*`/`?`/`~` no critério → `not_replayable` com motivo, **antes** de qualquer finding. Implementar a semântica só se houver caso real nas 3 pilots que a exija; caso contrário, declarar o limite é a correcção.

**Toca:** `xlsx_extract.py` `_replay_xlookup` e bloco COUNTIF; contagem `not_replayable` visível no `replay.md` e no `evidence-index.md`.

**Aceitação:** REVERSE_XLOOKUP e WILDCARD_COUNTIF dão `not_replayable`, zero findings; re-capture de pilot-3 não perde nenhum finding existente (diff do `replay.md`).

### P-18 — Identidade de versão e transições completas (resolve P-R4, P-R5, P-R7, P-R8)

Desenho antes de código, no mesmo passo que o desenho de A5 (onda 0 da frente D), porque tocam o mesmo conceito: **o que identifica uma versão aprovada**.

- **P-R5** — a aprovação em `decisions.md` cita `round` e `sha256` da frase do frame (ou do ficheiro aprovado); `/options` compara com o `frame.md` actual; cada aprovação nova tem id próprio. Mesma família que P-12: aprovação é `Confirmed` com locator.
- **P-R4** — `synthesis_state` avalia frescura **por tópico** contra a autoridade que cada tópico consome (`architecture-story` vs aprovação do blueprint; `business-story` vs SU); log incompleto → estado `desconhecido`, nunca "posterior à aprovação".
- **P-R7** — transição explícita `decision → options` em `aisa-options` pré-flight 1 quando existe `_simulation/revisit_*` com `REABRIR`: preserva a decisão anterior (`superseded_by`), retoma o contador `O-` da história, regista no `council-log.md`.
- **P-R8** — `solution-blueprint` lê `ux-blueprint_v<latest authorized>` e declara o estado (aprovado / com escolha estrutural aberta); `implementation-spec` e `claude-design-brief` mantêm `v<approved>`.

**Toca:** `aisa-frame` step 8; `aisa-options` pré-flight; `dashboard.py` `synthesis_state`; `solution-blueprint.template.md` `slot_sources`; `aisa-revisit` step 4.

**Aceitação:** os 3 contraexemplos estáticos da revisão (F05, F07, F08) deixam de ser possíveis por construção; `repro-synthesis-freshness.py` invertido passa.

### P-19 — Options nomeia a tecnologia, e cabe numa leitura (defeito observado pelo dono, 2026-09-09)

Duas falhas no `options.md` de `pricing-bunkers` O-01, ambas de **contrato**, não de modelo. O dono leu o ficheiro e o veredicto foi: *«em nenhuma das alternativas dizes se é Canvas app + Dataverse, ou Canvas app + SQL, ou model-driven + Dataverse. A fase das decisões é para nomear as tecnologias potenciais, e tu só descreves. Acho demasiada prosa, nenhum interlocutor vai ler isto tudo.»*

**Falha 1 — nenhuma opção nomeou a sua tecnologia.** O `solution-architect` devolveu só a metade do armazenamento (`O-C` sobre a base relacional partilhada, `O-D` sobre o armazenamento governado) e o chairman abstraiu mesmo essa metade nos títulos («esta plataforma sobre o armazenamento relacional que já corre»); os nomes de produto sobraram numa nota em itálico. `O-006` cobria em silêncio duas formas distintas. Causa: `ALT-004` era **uma** classe «in its several forms» — nada obrigava a nomear uma forma — e a regra do pacote *«no internal framework vocabulary · plain language only»* foi lida como proibição de nomear produtos. Prova de que é regressão e não tique do modelo: `cae-automation`, engagement anterior, nomeia as formas sem hesitar (*«Dataverse-first com Model-driven»*, *«Hybrid Dataverse+SharePoint+Canvas»*).

**Falha 2 — 8 542 palavras.** 13 campos obrigatórios × 11 candidatos (≈560 palavras por opção), mais 12 linhas de cobertura de temas, mais um `Summary` de 575 e um fecho de 1 020 que repetem as entradas. Cada campo era defensável; o ficheiro era ilegível. Comparação: `frame.md` do mesmo engagement tem 688 palavras.

**Correcção.**

- **Formas como membros da classe** — `decision-model/alternatives-register.md` §1.2 (novo): `ALT-004` passa a classe cujos membros são pares **`superfície × armazenamento`** nomeados em produtos, gerados em S1 e re-lidos em S9. A tabela **gera candidatos e não emite veredicto** (§0); uma forma que deixa de estar disponível é **redirecção dentro da plataforma, nunca desfecho de exclusão**. `decision-tree.md` §14.1: a **forma é campo obrigatório** de um candidato de plataforma, **uma opção por forma**; `«esta plataforma»` ou `«esta plataforma sobre a base que já corre»` é **malformado**. §14.3 passa a dizer o que a regra de vocabulário **não** cobre: *internal* é a maquinaria do framework, e nomear produtos é **obrigatório** em Options.
- **Contrato de artefacto novo** — `chairman-synthesis` escreve `options.md` como **tabela de decisão primeiro** (opção · tecnologia · veredicto · esforço · reverter · o que bloqueia), depois uma entrada curta por opção (6 campos), `Out of play` para eliminadas e não avaliáveis. **Orçamento vinculativo: ~1 500 palavras, ≤120 por opção.** O conjunto completo de campos e a cobertura dos 12 temas migram para `lens-outputs/chairman-synthesis-O-NN.md`: o artefacto é **projecção** desse registo, nunca substituto. `(none)` deixa de ser escrito no artefacto (campo omitido) **porque** o log o carrega — se o log não o carregar, o campo volta ao artefacto.
- **Consumidores** — `phases.md` Fase 3 (critério de saída + output), `aisa-options` step 6/7 (verificação de contrato + tecnologia na linha ao utilizador), `aisa-decide` (a tabela é a lista; o log é onde se lê um campo omitido), `aisa-simulate` (idem, e a forma entra na projecção porque duas formas sobre o mesmo armazenamento projectam diferente).

**Toca:** `library/packs/pp/decision-model/alternatives-register.md` §1.2; `decision-tree.md` §14.1/§14.3; `pack.yaml` → 1.9.0; `.claude/skills/chairman-synthesis/SKILL.md` steps 6/7; `library/kernel/phases.md` Fase 3; `aisa-options`, `aisa-decide`, `aisa-simulate`.

**Aceitação:** `.claude/tests/test_options_artefact.py` — contrato (pacote, artefacto, consumidores) mais os ficheiros reais: orçamento, tabela presente, **toda** a linha com tecnologia, nenhuma célula de tecnologia que seja menção nua à plataforma, ids da tabela ⊇ entradas. `pricing-bunkers` O-01 regenerado sob o contrato novo, com as formas partidas pelo `solution-architect`.

**Aplicação: aviso por teste, sem hook — e o critério que decide se isso muda.** A verificação vive
no teste, corrido a seguir a cada `/options` real; não há hook. Decisão do dono (2026-09-09), pela
regra que P-17 já usou: verificar se há caso real antes de construir maquinaria.

- **Custo de não ter hook:** o desvio é apanhado quando a suite corre, não no momento da escrita.
  Não há perda de dados nem estado corrompido — é qualidade de leitura, reversível por edição ou por
  nova passagem.
- **Critério de saída:** três passagens `/options` reais seguidas dentro do contrato → o hook não se
  faz e esta linha fecha.
- **Gatilho para construir:** um artefacto fora do contrato **e** o modelo a não corrigir depois de
  avisado. Aí o hook justifica-se — `PostToolUse` sobre `projects/*/options.md`, **avisa e regista**
  no `council-log.md`, nunca bloqueia (princípio 5: o único hard rule é `library/` read-only), com a
  lógica extraída para um módulo partilhado com o teste para os dois não divergirem.
- **Medição em curso:** passagem 1 de 3 — O-01 de `pricing-bunkers`, 2026-09-09: contrato cumprido na
  estrutura, **duas quebras de orçamento** (prosa 2 009 contra 2 000; entrada `O-007` com 192 contra
  160). Conta como passagem **não** limpa; o contador recomeça na próxima.

### P-20 a P-25 — o processo decide tecnologia, não arquitectura de pessoas (veredicto do dono, 2026-09-09)

O dono leu o `/simulate` e o `/premortem` de `pricing-bunkers` e o veredicto foi: *«este processo é
para definir opções de tecnologia com carácter técnico de implementação, não andar a ver que pessoa
é que faz o quê e quando. Isto trabalha-se por roles, não por pessoas. Não interessa quem assina o
quê.»* E, em separado: *«terminologia não se traduz»* — `Dataverse` tinha sido parafraseado como
«loja governada» 22 vezes nos ficheiros do engagement.

**Medida do desvio.** 95 `Unknown` escritas em `pricing-bunkers`; **30 de identidade nominal,
assinatura ou prova documental** (32%). Das 31 abertas, 12 (39%). Na lente de governação, 9 de 25.
E o efeito estrutural: **o conjunto que bloqueava a decisão era organizacional** (dono de publicação,
plano de operação financiado, revisor independente) **enquanto o conjunto que separava as formas de
tecnologia era técnico** (chave de negócio, regra de captura, trilha contra escrita directa, política
de conectores, catálogo das 114). Um processo que bloqueia no que não distingue não produz decisão.

**As cinco fontes do desvio, todas em prosa autorizada, nenhuma um erro de modelo.**

1. `question-bank.md` Q-BUS-05 / Q-GOV-06 / Q-GOV-07 — pediam quem assina, quem é o dono do
   orçamento, se são a mesma pessoa e se aceitaram.
2. `decision-tree.md` §6 portão S7 + concern C10 — *«operator, support, cross-boundary release owner,
   accountable ownership… make options **unavailable**»*, C10 *«with named people who accepted»*.
   É o motor que transformou «quem publica» num bloqueio de decisão.
3. `decision-model/blocking-set.md` B-02 — entrada de registo, `swing: decisivo` por construção, que
   fecha em *«a person who has accepted, in writing»* e torna padrões indisponíveis. A raiz mais funda.
   Mais B-16, B-17, B-23, B-26, B-28 pelo mesmo mecanismo, e B-04 a fechar num *signed matrix*.
4. `.claude/skills/lens-governance` + persona `compliance-officer` — *«what must be provable: audit
   trail, retention, sign-offs»*, sinal `go_live_approvals`, e o desafio *«a sign-off that exists only
   in someone's memory»*.
5. `library/packs/pp/glossary.md` §A2 — *«Accountable business owner: the named person who signs
   off… **named and accepted** is a different state from **named**»*. Vocabulário canónico do pack a
   exigir pessoa e aceitação: é daqui que C10 e S7 tiram autoridade.

Havia um travão que existia e estava desarmado: o teste de divergência (`states.md` → *Question
economics*) exige que o `swing` diga o que muda **no requisito, na forma dos dados ou no esforço**, e
«quem assina» não muda nada disso — mas o árbitro da passagem, por regra escrita, *«never judges
materiality»*.

**Decisões do dono, por `AskUserQuestion` (2026-09-09).** Saem do processo: identidade nominal de quem
executa ou autoriza · prova documental de terceiros · assinaturas, aprovações e portões de go-live ·
localização e custódia de ficheiros. Ficam, reformuladas em técnico: hora-limite como janela de
execução · população por grupo como dimensionamento de licenciamento e matriz de permissões ·
objectivo de recuperação como RTO mais mecanismo. Bloqueiam a decisão **só eixos técnicos**. `M-1`
(separação de funções da auditoria) entra **só como requisito de RBAC e de trilha**.

**Correcção.**

- **P-20 Terminologia não se traduz** — `glossary.md` §*Two languages* regra 5: produto, fornecedor,
  serviço, superfície, armazenamento, controlo e artefacto técnico são **literais** em todo o texto
  que o utilizador lê; não são termos do kernel e a regra 1 não se lhes aplica. Tabela
  *Forbidden paraphrases* legível por máquina, e a Part B do pack corre no sentido **oposto** (o nome
  que o participante diz converte-se no requisito **registado**), nunca a autorizar paráfrase de volta.
- **P-21 Roles, nunca pessoas** — regra dura nova nas lentes e no glossário do pack; `A2` passa a
  *Accountable role* e a *Operational ownership* por roles e mecanismos; Q-BUS-02/05/06, Q-GOV-05/06/07,
  P-GOV-01/07/10 reescritas por role, operação e plano de imposição; C7 e C10 idem; `go_live_approvals`
  sai dos sinais e entram `permission_enforcement_plane` e `audit_trail_mechanism`.
- **P-22 Só sete eixos técnicos bloqueiam** — `decision-tree.md` §6.1 (nova): modelo de dados e chave ·
  mecanismo de trilha · plano de imposição de permissões · política de ambiente, conectores e cadeia de
  licença · mecanismo de integração · catálogo de regras de cálculo · envelope de desempenho,
  concorrência e recuperação **medido**. O portão S7 desce a *requisitos do caminho escolhido*, e
  B-02, B-16, B-17, B-23, B-26, B-28 passam a `requirement (P-22)` — continuam no registo, deixam de
  bloquear e deixam de tornar opções indisponíveis. Razão escrita: uma lacuna organizacional recorre
  identicamente em todos os candidatos, logo não separa nada.
- **P-23 Relato de terceiro fecha, não abre** — `states.md`: o relato resolve como `Assumed` com a
  mediação declarada na base e **não abre nada**; o artefacto que falta não vira `Unknown`. `aisa-answer`
  só abre obrigação de verificação quando o input que falta é **técnico**.
- **P-24 Árbitro com uma classe de materialidade** — `aisa-round` 5f: uma linha cujo `swing` nomeia como
  consequência apenas pessoa, assinatura, aprovação, aceitação ou papel de terceiro desce a `cosmético`
  com marcador próprio. É a **única** materialidade que o árbitro julga, e é um teste de classe.
- **P-25 Premissas técnicas declaradas** — `orchestration.md` (secção nova): uma premissa técnica que o
  dono declara em conversa é registada **na mesma passagem**, como linha da SU e, em Options, como eixo
  de arquitectura. *Absorvido para o /simulate* deixa de ser resposta possível: foi assim que a ponte
  app↔BD por flow orquestrador contra conector directo, declarada pelo dono, não apareceu uma única vez
  no artefacto que comparou os candidatos.

**Toca:** `library/kernel/glossary.md`; `library/kernel/states.md`; `library/kernel/orchestration.md`;
`library/packs/pp/glossary.md`; `library/packs/pp/question-bank.md`; `library/packs/pp/decision-tree.md`
§5/§6.1/§12; `library/packs/pp/decision-model/blocking-set.md`; `.claude/skills/aisa-answer/SKILL.md`;
`.claude/skills/aisa-round/SKILL.md`; `.claude/skills/lens-governance/SKILL.md`;
`.claude/agents/compliance-officer.md`; `.claude/tests/test_user_language.py`. 40 edições + o lint.

**Aceitação:** `test_user_language.py` ganha `TestTechnicalTerminologyIsNeverTranslated` (tabela lida do
glossário, paráfrase apanhada, literal não apanhado, e nenhum bloco `user-output`, label do dashboard
ou linha de `COMO-USAR.md` a parafrasear um produto) — 25/25 verde, suite 21/21 ficheiros. Aceitação em engagement, feita: `pricing-bunkers` com 13 perguntas retiradas, 5 linhas novas
com a metade técnica (U-096 perfis e plano de imposição · U-097 janela de execução · U-098 ciclos e
critério de saída medido · U-099 RTO e mecanismo · U-100 controlo de acesso do destino), 29 paráfrases
restauradas ao literal, `diagnostics=0`, abertas 31 → 23 e o conjunto bloqueante todo dentro dos sete
eixos. `test_retirement.py` (19) novo; suite 22/22 ficheiros, com a única falha em
`test_options_artefact` a ser o orçamento de palavras do `options.md` escrito antes desta frente
(aceitação de P-19, ainda aberta). **Falta**: revalidar os veredictos de `options.md` numa passagem de
`/options`, e `/simulate` v02 para confirmar que o conjunto novo produz decisão.

### Emendas absorvidas

- **F09 → P-9**: a estimativa e a simulação chamam-lhes **intervalos de planeamento** (min–max sobre as bandas do método); `P50`/`P80` e o `×1.4` saem do texto de `aisa-simulate` até existir método probabilístico documentado no pack.
- **F10 → P-1**: o árbitro (step 5f) e o `/simulate` corrigem `swing` **para baixo** só com cobertura de todas as opções que a pergunta toca; com cobertura parcial registam impacto local na saída e não tocam a SU. Promoção pode apoiar-se numa evidência suficiente.
- **P-R13 → `pre-write-guard.py`**: canonicalizar o caminho (`Path.resolve()`, comparação case-insensitive em Windows) e **testar** se `Write(./library/**)` em `settings.json` é case-sensitive antes de contar com ele como segunda linha.

---

## 4. Dependências

```text
P-0 (enquadramento M-n) ──► P-1 (árbitro; denominador = M-n ou divergência)
P-3 (PM-U conteúdo) ────────┐  independentes de P-1; P-2 mede o efeito de todos
P-4 (funding_gate) ─────────┤
P-12 (limiar Confirmed) ────┘  partilha o árbitro de P-1 (step 5f); hook próprio

P-13 (duas línguas) ──► transversal: toca a linha de output de todos os comandos; P-14 depende dele
P-0 (enquadramento) ──► P-14 (entrada em linguagem natural: orient → P-0 → /start)

P-5 (mandato campos/tempos) ──► P-6 (A5 fields/access_contract + motor) ──► P-7 (sufficiency)
                              │                                            │
                              └──► P-10 (drivers, impacto operacional) ◄────┘
P-8 (transições, pré-condições) ──► P-9 (bandas, ocupação por perfil)
P-11 (experiência) ──► decide se G4 é cortar ou anexar

P-15 (ronda em curso, PyYAML) ──► validação de A (qualquer `/round <lens>` em cópia)
P-17 (replay honesto) ──► P-3 (classes PM-U só valem sobre findings verdadeiros)
P-16 (identidade do motor) ──► independente; antes do fecho de A
P-18 (versão e transições) ──► desenhado com A5 (onda 0 de D); antes de D
```

Reconciliações explícitas:

- **F5 ↔ G2**: P-3 governa Discovery (mecânica → `DISMISS` salvo forma/volume de dados); P-6 governa Architecture (L1 → rascunho `Assumed`, só autoridade interna). O mesmo artefacto, duas fases, um critério: *muda os dados do to-be?*
- **"Menos perguntas" ↔ "campos e tempos"**: P-1 reduz `Unknown` cosméticas em Discovery; P-5 adiciona campos **fora** do Discovery (Architecture) e tempos como `Assumed` preferencialmente. O saldo de P-2 mede Discovery; campos não entram nele.
- **"Sem portão de financiamento" ↔ "impacto operacional justifica"**: P-4 declara o portão; P-10 renderiza o Δ sem lhe atribuir função de justificação quando o portão não existe.
- **D1 como causa raiz ↔ ordem 5**: P-0 dá o denominador, P-1 aplica-o; vão em primeiro.
- **P-12 ("menos `Confirmed`") ↔ P-1 ("mais `Assumed`, menos `Unknown`")**: convergem. P-12 empurra interpretação de `Confirmed` para `Assumed`; P-1 empurra inferência de `Unknown` para `Assumed`. `Assumed` com base declarada é o estado central do Discovery; `Confirmed` é o que tem locator e fica ao nível; `Unknown` é o que a inferência não alcança. Nenhuma das duas regras pode ser lida como "pergunta ao executor".
- **D4 ("a ordem está invertida") ↔ princípio 1 (discovery before solution)**: a intuição de D4 estava certa — o alvo tem de existir antes do mapeamento. A correcção não é antecipar o Framing (que é síntese com evidência) nem extrair do pedido (F1): é pedir ao dono o **mecanismo**, que não é solução nem pedido. O Framing continua a ser a validação do que o dono declarou.

---

## 5. Sequência: onda 0 comum, depois cinco frentes

Um plano, quatro frentes de execução. Critério de corte: **mesmos ficheiros, mesma validação, mesmo risco**. Cada frente vira um passo do tracker (`docs/pp-pack-authoring/pilot/step-9<x>-*.md`, com freeze e tag) **quando arranca** — escrito já com os números da onda 0, não antes.

### Onda 0 — medir (comum, antes de tudo, zero código)

| Medição | Serve | Resultado esperado |
|---|---|---|
| Escrever `enquadramento.md` de pilot-3 (M-1…M-5); classificar as 85 `Unknown` em *serve M-n · diverge · nenhum* | P-0 | custo do Discovery sem enquadramento, em rows |
| Reclassificar as 41 abertas com a regra de P-1 | P-1 | número real de `cosmético` disfarçadas |
| Amostra de 30 `Confirmed` (feita: 7/30) → estender às 156; listar as `A-nnn was C-nnn` a criar | P-12 | número real de `Confirmed` acima do nível |
| `--dry-run` de pilot-1 §4 com a instrução antiga de uma linha | P-11 → frente D | veredicto: cortar template, anexar exemplos, ou causa upstream |
| Desenho de A5 `fields[]` / `access_contract` em papel, contra as 7 entidades de pilot-1 e as listas de `dpt-galp-jp` | P-6 → frente D | **feito 2026-09-09** — `step-9a-onda-0-desenho-a5.md`: 12 decisões de forma, 7 domínios + 2 listas mapeados por coluna do L1, 6 emendas ao plano (E1–E6, aplicadas), 6 decisões do dono fechadas |

### Frentes

| Frente | Correcções | Ficheiros | Validação | Ordem |
|---|---|---|---|---|
| **A — Discovery** | P-0, P-1, P-2, P-3, P-4, P-12 | 6 lentes · `aisa-start` · `aisa-round` · `aisa-answer` · `states.md` · `orchestration.md` · `phases.md` · `dashboard.py` · `su-confirmed-guard.py` (novo) | `/round` em cópia de pilot-3 com `enquadramento.md`: nenhuma `Unknown` nova pergunta o porquê de 2ª/3ª; `criadas ≤ fechadas`; toda a `Unknown` nova cita `M-n` ou tem as 3 declarações; nenhuma `Confirmed` sem locator; `financial` sem envelope. Contagens pelo motor | **1.ª**, logo após a onda 0 |
| **B — Estimativa** | P-8, P-9, P-11 | `estimate.template.md` · `implementation-spec.template.md` (§6 `slot_conditions`) | re-render pilot-1: §6 ≠ `(none)`; fases ≥ 5d com bandas cuja união contém o total; ocupação por perfil ≤ dedicação; cada item de §9 numa fase; **total 44 inalterado** | **em paralelo com A** — ficheiros disjuntos |
| **C — Entrada e linguagem** | P-13, P-14 | `CLAUDE.md` · `glossary.md` · linha de output de todos os comandos · `aisa-orient` (novo) · `aisa-status` · `resume` · `dashboard.py` (labels) · `docs/COMO-USAR.md` (novo) | teste de leitura de `/status`, `/round`, `/resume` por quem não construiu; sessão nova sem comando com o pedido de pilot-3 → enquadramento, passos, entrevista, proposta de `/start`, zero jargão sem tradução; "quero a estimativa" sobre pilot-1 → diz o que falta e o comando certo | **depois de A** — P-13 reescreve as linhas de output que A ainda está a mudar; P-14 depende de P-0 |
| **D — Dicionário e suficiência** | P-5, P-6, P-7, P-10 | `architecture-core.md` A5 · `fields_draft.py` (novo) · `render-validate.py` · `aisa-decide` · `aisa-synthesize` · `aisa-blueprint` · `lens-data` · `lens-operations` · `synthesis-templates/as-is.md` · spec e estimate templates · G4 conforme P-11 | pilot-1: `access_contract` nos 6 domínios externos e `fields[]` nos 2 `owned` (`workflow-audit`, `scenarios`), por coluna do L1, 10 entidades com `authority`; §4 com colunas *lidas · escritas · chave* e linha `⚠️ lacuna`; `render-validate.py` sobre v02 antigo dá ≥ 3 lacunas e sobre o novo dá 0 **por conteúdo**; `dpt-galp-jp` cobertura de fonte dos campos de v01 = 100 %, classe `none` = 0; `operational_impact` (§17) da estimativa deixa de ser `not applicable`; densidade de §4/§6/§8 ≥ `dpt-galp-jp` v01 sem violar proibições. Critérios por entidade: `step-9a-onda-0-desenho-a5.md` §8 | **última** — maior mudança estrutural; exige o desenho de A5 (onda 0) e o veredicto de P-11 (frente B) |
| **E — Integridade do runtime** | P-15, P-16, P-17, P-18 (+ emendas F09→P-9, F10→P-1, P-R13→guard) | `aisa-round` steps 3/5a/3.6c · `pre-lens-order-check.py` · `dashboard.py` (`running_server`, `synthesis_state`, `inline_md`, diagnostics) · `text_extract.py` · `xlsx_extract.py` replay · `aisa-frame` 8 · `aisa-options` pré-flight · `aisa-revisit` 4 · `solution-blueprint.template.md` · `pre-write-guard.py` · `requirements-dev.txt` · 7 testes de regressão | cada script de `docs/review-evidence/` invertido passa; suite completa de `.claude/tests` verde com PyYAML; `/round business` + `/round operations` sem bloqueio; pilot-3 `diagnostics=[]` e `replay.md` sem perda de findings | **P-15 antes da validação de A · P-17 antes de P-3 valer · P-16 antes do fecho de A · P-18 com o desenho de A5, antes de D** |

Regras entre frentes:

- **P-15 primeiro, em paralelo com o que resta da onda 0**: a frente A está `em curso` e a sua validação lente a lente está bloqueada pelo guard (F06). Sem P-15, "validado" em A só é possível com rondas completas.
- **P-17 antes de fechar P-3**: classes `PM-U` sobre findings falsos são falsos positivos com etiqueta.

- **A ∥ B** podem correr em simultâneo: não partilham um ficheiro.
- **C só depois de A fechar** — caso contrário cada commit de A obriga a refazer a linha de output de C.
- **D só depois de B** (P-11) **e do desenho de A5 em papel**. Se se saltar o desenho, o motor codifica uma forma que a spec depois não consome.
- Cada frente fecha com: cópia real validada, contagens pelo motor, linha no tracker, um commit por correcção, tag de freeze.

### Estado por correcção

| Correcção                                     | Frente     | Estado                                                                                                                                                                                                                                                                                                                                                                                                                                        | Passo do tracker                  |
| --------------------------------------------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| P-0 Enquadramento                             | A          | **congelado (step-9c, tag `step-9c-frente-a`)** — prosa `fb64021`, código `3321ff8`; R-05 nas duas cópias: nenhuma `Unknown` nova pergunta o porquê de 2ª/3ª, `R-00` reportada como enquadramento (dono)                                                                                                                                                                                                                                                               | `step-9c-frente-a-codigo.md` §5.2 |
| P-1 Teste de divergência arbitrado            | A          | **congelado (step-9c, tag `step-9c-frente-a`)** — prosa `9e775b8`, código `0e086e9` + correcção `3d18a5d` (o árbitro não reconhecia `(a) … (b)`, achado pela validação); R-05: 0 perguntas sem declaração, 0 `decisivo` sem referente dos dois lados                                                                                                                                                                                                                   | `step-9c-frente-a-codigo.md` §5.2 |
| P-2 Convergência reportada                    | A          | **congelado (step-9c, tag `step-9c-frente-a`) — mecanismo validado** — prosa `8ab6c73`, código `1279f00`/`7b5a1f4`/`be4ae20`; detectou e etiquetou a não-convergência. O **critério de saída** (`criadas ≤ fechadas`) foi cumprido pelo lado Sonnet (2/2) e não pelo lado Opus (7/0) — comportamento do modelo, não defeito do código                                                                                                                                             | `step-9c-frente-a-codigo.md` §5.2 |
| P-3 `PM-U` por conteúdo                       | A          | **congelado (step-9c, tag `step-9c-frente-a`)** — prosa `87e5129`, código `025a99a` + correcção `00e5649` (dois buracos na regra da `classe`, achados ao correr o `/capture`; um deles teria partido esta própria aceitação); cópia `-val-capture` run 4: `PM-U-026` mecânica, `PM-U-003` dados                                                                                                                                                                        | `step-9c-frente-a-codigo.md` §5.2 |
| P-4 `funding_gate`                            | A          | **congelado (step-9c, tag `step-9c-frente-a`)** — prosa `4ec644b`, código `82990c4`; R-05 com `funding_gate = false`: 0 `Unknown` de envelope/limiar/imputação dos dois lados. Falta um `/frame` de teste para a metade do frame enunciado sem monetizar                                                                                                                                                                                                               | `step-9c-frente-a-codigo.md` §5.2 |
| P-12 Limiar de `Confirmed`                    | A          | **congelado (step-9c, tag `step-9c-frente-a`)** — prosa `c69d5c7`, código `e7f5fab`/`684bff8`, hook ligado; pilot-3 a 0 avisos (139/139). O hook disparou em produção na cópia Sonnet e o modelo corrigiu na mesma ronda. Decisão nova do dono: extracção directa é prova legítima **se ficar persistida em `_capture/`** (`59009dc`) — quinta classe escrita em `states.md` e reconhecida pelo motor 1.4.0 (`d9cd05e`, `4a88ed2`, §5.4); determinismo fechado (§5.3). `C-163` fechado pela transição nova *correcção pela prova* (`995234d`, §5.5 — `C-164 was C-163`). Falta só o perfil de modelo → tag | `step-9c-frente-a-codigo.md` §5.2 |
| P-8 Transições e pré-condições                | B          | **congelado (step-9d, tag `step-9d-frente-b`)** — `6331df6`; spec §6 deixa de ser `(none)` sobre 2 máquinas de estado (4 transições, 13 células `not named` em vez de inventadas); estimativa §14 nova, 10 pré-condições com dono e fase travada, incluindo SME 20% e acesso à BD partilhada. Duas emendas ao `slot_sources` forçadas pela validação: `compositions[] boundary: outside-platform` e a team composition do método                                                                                                                                                                                                                                                                                                                                                                                                                                      | `step-9d-frente-b-estimativa.md` |
| P-9 Bandas e ocupação por perfil              | B          | **congelado (step-9d, tag `step-9d-frente-b`)** — `2ce2447`; 2 fases ≥ 5d com sub-tabela e `8,0 ≤ 8,0 ≤ 8,0`, 4 abaixo do limiar não decompostas, ocupação 44 ÷ 1,0 → ≥ 9 semanas, 6/6 incertezas na fase que ameaçam, total 44 inalterado. Terceira emenda: taxa pontual do método renderiza `min == max` marcado, nunca um `±` inventado                                                                                                                                                                                                                                                                                                                                                                                                                                      | `step-9d-frente-b-estimativa.md` |
| P-11 Experiência de template                  | B (onda 0) | **congelado (step-9d, tag `step-9d-frente-b`)** — `13658c1`; **ramo (b)**, 3/3 runs isolados: 0 campos produzidos, 0 inventados, 3/3 reportaram as lacunas. Sem mandato de corte; a causa é upstream (P-6). Achado extra: o template longo sobre-afirmou a autoridade de registo de 2 entidades onde a instrução curta reportou a lacuna → §1.2 do passo, para a frente D                                                                                                                                                                                                                                                                                                                                                                                                                                      | `step-9d-frente-b-estimativa.md` |
| P-13 Duas línguas                             | C          | **congelado (step-9e, tag `step-9e-frente-c`)** — glossário a 3 colunas como contrato de lint; regra dos parênteses em `CLAUDE.md`; 15 skills com blocos `user-output` fechados em `A seguir:`; `/status` reestruturado em 7 blocos (decisão do owner) com delta por estado no motor (`dashboard.py` 1.5.0); aceitação 90 → 0 (skills), 13 → 0 (dashboard), página construída 0; teste de leitura 3/3 acertam acção, dono e porquê sem abrir ficheiros                                                                                                                                                                                                                                                                                                                                                                                                                                      | —                                 |
| P-14 Entrada em linguagem natural             | C          | **congelado (step-9e, tag `step-9e-frente-c`)** — `aisa-orient` (novo, nunca escreve; `aisa-start` aceita a declaração recolhida), `docs/COMO-USAR.md` (35 linhas, 0 jargão); mensagem literal de pilot-3 sem comando: 3/3 runs com as cinco linhas, passos, entrevista P-0 e slug, 0 violações; «quero a estimativa» sobre pilot-1: diz onde estamos, o que falta e o comando (2 runs; os 42 deslizes dos primeiros eram dois defeitos de template, corrigidos → 0 e 1)                                                                                                                                                                                                                                                                                                                                                                                                                                      | —                                 |
| P-5 Mandato de campos e tempos | D | **em curso (frente D, 2026-09-09)** — `lens-operations` cue `step_duration` (tempo por passo `Assumed` com base ou `Unknown custo=email`, nunca estimado); `lens-data` cue `data_shape` (grão · dimensões · volume, não atributos); `as-is.template.md` ganha *Passos e tempo* (`passo · quem · tempo · estado · base · fonte`) como única fonte da secção de caminho operacional da spec, nunca da estimativa. Falta: re-síntese de pilot-1 com tempo por passo (aceitação) | `step-9a-onda-0-desenho-a5.md` |
| P-6 Dicionário no architecture record         | D          | **em curso (frente D, onda 1, 2026-09-09, Fable 5.1)** — `library/kernel/tools/fields_draft.py` 0.1.0 escrito e testado (`tools/tests/test_fields_draft.py`, 29: sintéticos + pilot-1 + dpt-galp-jp): nome `named_range → formula_ref → header → none`, tipos com `unknown` para mistos/vazios, `choice` por validação de lista com o intervalo citado, `required` por nulos, `default` nunca inferido, papel pela classe L1, itens por coluna com `aliases[]`, entradas de dicionário sem dados à parte, `disposition: null`, idempotente por sha256, `--engagement` + `--log` (linha `L1b` no `_capture-log.md`). Medido: pilot-1 `Inputs` 83 nomeadas / 8 sem nome exactamente as previstas, `Outputs` 59 computadas, 42 entradas sem dados, dimensões 10·22·46 = §2.1 do desenho; dpt `Prioridade` choice e `Exec_Order` não obrigatório sem julgamento. `aisa-blueprint` step 4 invoca o motor e exige disposição ADOPT/MAP/DISMISS por coluna. **Falta**: `architecture-core.md` A5 (esquema §4 do desenho), `entities[].authority`, `aisa-synthesize ## Data`, spec §4 forma + lacuna (P-7 no `render-validate.py`), re-render de pilot-1. Antes disso, o desenho de A5 (onda 0, só papel): 12 decisões de forma (D1–D12), 7 domínios de pilot-1 e 2 listas de dpt-galp-jp mapeados por coluna do L1, emendas E1–E6 aplicadas a P-5/P-6/P-10, 6 decisões do dono fechadas (`scenarios` owned; `AçoreanaMutualista_*` DISMISS por C-052; sem override do preço calculado; motor em `aisa-blueprint`; `Tipificação` 1 campo). Achados novos: 76 named ranges para colunas vazias, `Outputs` 4/76 cabeçalhos, `v05` aprovado não parseia em PyYAML | `step-9a-onda-0-desenho-a5.md` |
| P-7 Gap check por suficiência | D | **em curso (frente D, 2026-09-09)** — `render-validate.py` 1.0.0 deixa de ser stub: executa o bloco `sufficiency:` do template por conteúdo contra o blueprint aprovado (segue `SEE_Vnn`) e o texto renderizado; hook (append a `render-gaps.md`, nunca bloqueia) + CLI `--dry-run`/`--json`. **Aceitação cumprida**: pilot-1 v02 sem mais nada alterado → 21 lacunas em 3 famílias (§4 entidades sem `authority` e domínios sem `key`/`access_contract`/`schema_owner`; §6 `(none)` com 2 entidades de aprovação; §8 sem matriz) — antes 0. `test_render_validate.py` (21). Falta: 0 lacunas por conteúdo sobre o registo novo (depende de v07 com dicionário) | `step-9a-onda-0-desenho-a5.md` |
| P-10 Drivers e impacto operacional | D | **em curso (frente D, 2026-09-09)** — estimativa: coluna `driver` em `work_breakdown` citada à spec (§4 números · §5/§6/§7 contagens), `operational_impact` lê a secção *Alteração do caminho operacional* da spec; spec: nova §16 condicional (passo · quem · tempo actual · novo processo · tempo novo · Δ) alimentada só por `as-is.md# Passos e tempo` (emenda E5), §17 itens em aberto. Falta: re-render de pilot-1 (§17 da estimativa deixa de ser `not applicable`) | `step-9a-onda-0-desenho-a5.md` |
| P-15 Ronda em curso + PyYAML                  | E          | **feito (frente E, bloco E1)** — `_state.json.round_in_progress` separa a passagem aberta da concluída (`phases.md` → *Rounds*); `aisa-round` 3a-d/5a abre, reutiliza e fecha (`/round --close`), 5f não reclassifica duas vezes, 5d escreve um episódio por passagem; o guard lê a ronda aberta e resolve o engagement pelo `engagement root` da invocação (duas cópias em ronda simultânea); `dashboard.py` 1.5.1 publica `round_in_progress`; `/frame` avisa e limpa; `requirements-dev.txt`; 14 testes novos (`test_round_in_progress.py`), suite 13/13 ficheiros verde. Aceitação em cópia real de pilot-3: `business`→`operations` exit 0 (antes exit 2, procurava R-06), ordem mantida (`user` bloqueado), `diagnostics=0` | —                                 |
| P-16 Identidade do motor (F01, F02, F11, F12) | E          | **feito (frente E, bloco E2)** — F01: `parse_su` emite `id duplicado: C-nnn (linhas a, b)` como erro, o drawer guarda a **primeira** linha e mostra as outras marcadas, e `aisa-round` 3.6c recalcula os ids **antes de cada lente** (4c verifica colisão). F02: `/__build` devolve `{build, slug, engagement, pid, started}`; o reatar exige caminho+pid+arranque iguais ao lock (o slug é do `_state.json`, identidade da página, não do servidor) e o cliente pára e avisa quando o slug diverge. F11: `text_extract` só reutiliza cache com `status == "ok"`; `failed`/`skipped` repetem com o motivo no log. F12: `safe_href` allow-list (`http(s)`/`mailto`/relativo) — outro esquema fica texto visível. P-R13: `pre-write-guard` canonicaliza o caminho e compara conforme o filesystem (`LIBRARY/...` bloqueia). `dashboard.py` 1.5.2, `text_extract.py` 1.0.1, 19 testes novos (`test_motor_identity.py`); 4 cenários do `runtime_adversarial_repro.py` invertidos passam. Verificado vivo no browser: zero `href` perigosos, diagnóstico de id duplicado na página, aviso de servidor de outro projecto | —                                 |
| P-17 Replay honesto (F03)                     | E          | **feito (frente E, bloco E3)** — verificámos primeiro se há caso real: nas 3 pilots, zero `XLOOKUP` com 5+ argumentos e zero critérios com wildcard → **declarar o limite** é a correcção (implementar semântica seria maquinaria por testar). `search_mode` ≠ 1 e critérios/valores de procura com `*`/`?`/`~` (COUNTIF, XLOOKUP, VLOOKUP, MATCH) dão `not_replayable` **antes** de qualquer finding; `has_wildcards` é o único sítio que decide. O `replay.md` abre com `Out of scope: N formula call(s) declined`, as Notes declaram o limite, o log escreve `N findings, M not replayable` e o `evidence-index.md` mostra `N chamada(s) fora do alcance do replay`. `xlsx_extract.py` 1.2.0; 10 testes novos (`test_replay_scope.py`). Aceitação: replay HEAD vs novo em pilot-1/2/3 + dpt — **zero findings perdidos** (único diff = a linha de âmbito) | —                                 |
| P-18 Versão e transições (F04, F05, F07, F08) | E          | **F04 + F05 + F07 + F08 feitos (frente E, bloco E4 completo, 2026-09-09)**. **F04** (Fable 5.1, após o desenho de A5 §9): `synthesis_state` avalia frescura **por tópico** contra as autoridades que cada tópico consome, lidas dos `sources:` dos `synthesis-templates` (aprovação do blueprint · linhas SU do filtro do tópico por `verificado_em`, granularidade dia · blocos de `decisions.md`); `architecture-story` compara também a **identidade** da versão (carimbo `<!-- authority: _blueprint/ux-blueprint_vNN.yaml#architecture @ sha256:<bloco> -->` escrito por `aisa-synthesize` via `dashboard.py --authority-stamp`, ou a versão citada na linha do log) — em pilot-1 apanha `v04` sintetizada vs `v05` aprovada; pack sem linha no log → `desconhecido`, nunca «posterior à aprovação»; log em tabela (dpt-galp-jp) passa a ser lido; marco nomeia os tópicos e manda `/synthesize <tópico>`; `stale_vs_approval` mantido como atalho. **F08**: `solution-blueprint.template.md` lê `v<latest authorized>` e ganha o slot obrigatório `architecture_version_state` (aprovada (D-NNN) · não aprovada — N escolha(s) estrutural(is) em aberto · não aprovada — aguarda aprovação); spec e brief mantêm `v<approved>`; regra escrita em `render-contract.md`, `blueprint-contract.md` e `aisa-render`; `blueprint_state.latest_authorized` no motor (pilot-1: `v06 — not approved — 4 structural choice(s) open`). `dashboard.py` 1.7.0; `test_synthesis_freshness.py` (27) + 3 testes em `test_pp_deliverable_templates` + 1 em `test_status_model`; suite 18/18 ficheiros; `repro-synthesis-freshness.py` invertido passa, `verify_review.py` 8/8; 14 engagements com marco e `diagnostics` **idênticos** ao HEAD. **F05**: a aprovação cita `Frame sha256` da frase normalizada lida do `frame.md` (não do bloco — pilot-1 tem a frase em EN no ficheiro e em PT no D-001) + `Agreed in round`; `frame_sentence` passa a ler blockquote, negrito e `### Frame sentence` (os 4 engagements passam a ter frase e identidade; antes o motor lia `""`); veredictos `match` / `match-other-round` / `mismatch` / `legacy` / `none` / `no-frame` no pré-flight de `/options`, todos soft menos `no-frame`; id = próximo `D-NNN` livre (D-001 deixa de ser especial, hook incluído); frase igual em passagem posterior → linha no `council-log.md`, sem bloco novo. **F07**: transição `decision → options` por veredicto REABRIR (cabeçalho fixo no `revisit_*.md`, nunca prosa) ou `/options --reopen "<razão>"`; contador `O-` da **história** (`chairman-synthesis-O-NN` ∪ `## O-NN` do log ∪ estado) — o estado diria `D-01` e reiniciaria em O-01, por cima da ronda em revisão; `Supersedes` é o único ponteiro escrito, `superseded_by` derivado, e os tripwires seguem a decisão em vigor. `dashboard.py` 1.6.1 (`frame_identity`, `options_round_history`, `revisit_state`, `model["frame"]`); 23 testes novos (`test_frame_identity.py` 13 + `test_reopen_transition.py` 10), suite 17/17 ficheiros. Aceitação: contraexemplo de F05 dá `mismatch` por construção; `/revisit`→`/options`→`/decide` completo em cópia de pilot-1 (D-002 → D-005, O-02 da história, ficheiro append-only); 6 engagements reais com `diagnostics`, marco, comando e tripwires **idênticos** ao HEAD | —                                 |
| P-19 Options nomeia tecnologia + orçamento | F (nova) | **em curso (2026-09-09, defeito observado pelo dono)** — `alternatives-register.md` §1.2 (formas `superfície × armazenamento`, geram e não veredictam, forma perdida = redirecção), `decision-tree.md` §14.1 (forma obrigatória, uma opção por forma, menção nua = malformado) e §14.3 (a regra de vocabulário interno **não** proíbe nomear produtos — foi essa leitura que apagou os nomes), `pack.yaml` 1.9.0; `options.md` passa a tabela de decisão + entrada de ≤120 palavras, orçamento ~1 500, campos completos e cobertura dos 12 temas no log da ronda; consumidores ligados (`phases.md`, `aisa-options`, `aisa-decide`, `aisa-simulate`); `test_options_artefact.py` (35). **Caso real (O-01 regenerado pelo dono, 2026-09-09)**: contrato cumprido — tabela primeiro, 4 formas nomeadas (`canvas + Azure SQL`, `model-driven + Dataverse`, `shell model-driven + custom pages + Dataverse`, `canvas + Dataverse`), log com cobertura dos 12 temas e forma longa das 10 alternativas; 2 246 palavras contra 8 542. **Duas quebras**: prosa 2 009 (tecto 2 000) e entrada `O-007` com 192 palavras (tecto 160). **Defeito do próprio teste, encontrado pelo caso real**: o marcador de contrato era uma frase inglesa e o artefacto sai na língua do pacote — as verificações por ficheiro passaram em falso; a detecção passa a ser por **forma** da tabela (cabeçalho real com coluna de tecnologia + linhas por id), depois de uma primeira correcção por palavra solta ter apanhado um ficheiro legado com «non-technology» numa célula |
| P-20 Terminologia não se traduz | F | **em curso (2026-09-09, veredicto do dono)** — `glossary.md` regra 5 + tabela *Forbidden paraphrases*; lint `TestTechnicalTerminologyIsNeverTranslated` sobre blocos `user-output`, labels do dashboard e `COMO-USAR.md`. Defeito observado: `Dataverse` parafraseado como «loja governada» e `Azure SQL` como «a base relacional» — paráfrases de runtime, inexistentes em `library/` e em `.claude/`, que chegaram aos ficheiros do engagement. **Quinta edição sancionada** (`states.md` → *Terminology normalisation*, decisão do dono): restaurar o literal numa linha existente é edição, não transição — o claim afirma o mesmo sobre o mesmo produto. Aplicada a `pricing-bunkers`: **29 ocorrências** restauradas em 5 ficheiros (16 na SU), zero paráfrases restantes | — |
| P-21 Roles, nunca pessoas | F | **em curso (2026-09-09, veredicto do dono)** — regra dura nas lentes e no glossário do pack (`A2` → *Accountable role*, *Operational ownership* por roles e mecanismos); Q-BUS-02/05/06, Q-GOV-05/06/07, P-GOV-01/07/10 reescritas; C7/C10 por role e mecanismo; `go_live_approvals` fora, `permission_enforcement_plane` e `audit_trail_mechanism` dentro; `compliance-officer` desafia planos de imposição, não assinaturas. Medida do desvio: 30 de 95 `Unknown` de identidade, assinatura ou papel. **Quarta edição sancionada** (`states.md` → *Withdrawal for scope*, decisão do dono): uma pergunta que o processo não faz sai por ` — retirada P-21 (<razão>)` — a linha fica para auditoria, deixa de contar como aberta e **não é fecho**; só `Unknown` e `Conflicted` a admitem, e só o dono a decide. Motor 1.9.0 (`detect_retirement`, contador `retirada`, `retiradas` no balanço da passagem) + `test_retirement.py` (19). Aplicada a `pricing-bunkers`: 13 retiradas, 5 linhas novas com a metade técnica (U-096 a U-100), abertas 31 → 23 | — |
| P-22 Só sete eixos técnicos bloqueiam | F | **em curso (2026-09-09, veredicto do dono)** — `decision-tree.md` §6.1 nova (modelo de dados e chave · trilha · plano de permissões · ambiente/conectores/licença · integração · catálogo de regras · envelope medido); S7 desce a requisitos; B-02, B-16, B-17, B-23, B-26, B-28 passam a `requirement (P-22)`. B-02 era a raiz: fechava em «a person who has accepted, in writing» e tornava padrões indisponíveis | — |
| P-23 Relato de terceiro fecha, não abre | F | **em curso (2026-09-09, veredicto do dono)** — `states.md` → *Question economics*: o relato resolve `Assumed` com a mediação na base e não abre `Unknown` a pedir email, acta ou aceitação escrita; `aisa-answer` só abre obrigação quando o input que falta é técnico. O limiar de `Confirmed` (P-12) fica intacto — muda a consequência, não o grau de prova | — |
| P-24 Árbitro com uma classe de materialidade | F | **em curso (2026-09-09, veredicto do dono)** — `aisa-round` 5f: `swing` que nomeia como consequência só pessoa, assinatura, aprovação ou papel de terceiro desce a `cosmético` com marcador próprio. Arma o travão que já existia e estava desarmado (*never judges materiality*), sem lhe dar julgamento caso a caso | — |
| P-25 Premissas técnicas declaradas | F | **em curso (2026-09-09, veredicto do dono)** — `orchestration.md` secção nova: premissa técnica declarada em conversa entra na SU na mesma passagem e, em Options, como eixo de arquitectura; *absorvido para o /simulate* deixa de ser resposta. Defeito observado: a ponte app↔BD (flow orquestrador contra conector directo) declarada pelo dono não apareceu no artefacto de comparação | — |
| Emendas F09 → P-9 · F10 → P-1 · P-R13 → guard | E → B / A  | **F09 congelado (step-9d)** — `2ce2447`: `interval_vocabulary` declara intervalos de planeamento e proíbe quantil; `P50`/`P80` e o exemplo `SAP ×1.4` saíram de `aisa-simulate`; cada factor passa a ser citado à secção que o enuncia. **F10 feito (2026-09-09)**: `aisa-simulate` só baixa `swing` com cobertura de todas as opções que a pergunta toca — cobertura parcial regista impacto local na saída e não toca a SU; subida pode assentar numa evidência suficiente; o árbitro de `aisa-round` 5f só baixa por declaração em falta, nunca por inferência sobre opções. **P-R13 feito (frente E, bloco E2)**: `pre-write-guard.py` canonicaliza o caminho | `step-9d-frente-b-estimativa.md` (F09) |

Estados possíveis: `planeado` · `em curso (step-9x)` · `validado` · `mecanismo validado` (o código faz o que devia; o critério de saída depende do modelo ou do engagement — P-2 é o caso) · `congelado (tag)` · `descartado (razão)`. Actualizar aqui quando o passo do tracker muda; este quadro é o índice, o passo é o registo.

---

## 5.1 Modelo por momento

Regra: **julgamento em Fable 5.1, mecânica em Opus 5, validação no modelo de produção.** Mudar com `/model <id>` no início da sessão ou do passo indicado; uma sessão por linha da tabela sempre que o modelo muda.

| Momento                                                                                                                               | Modelo                                 | `/model`           | Porquê                                                                                                                            |
| ------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- | ------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| **Onda 0** — classificar as 85 `Unknown` contra M-n; 156 `Confirmed` ao nível da evidência; reclassificar as 41 abertas               | Fable 5.1                              | `claude-fable-5-1` | só julgamento; os dois erros desta revisão (contagem manual, afirmação acima da evidência) são o que um passe menos atento produz |
| **Onda 0** — `--dry-run` de P-11                                                                                                      | Opus 5                                 | `claude-opus-5`    | render de teste; o veredicto lê-se depois em qualquer modelo                                                                      |
| **Onda 0** — desenho de A5 em papel                                                                                                   | Fable 5.1                              | `claude-fable-5-1` | decisão de forma que spec e motor consomem; errar custa a frente D                                                                |
| **Frente A** — prosa de `states.md`, `orchestration.md`, `phases.md`, 6 lentes, `aisa-start` (P-0, P-1, P-3, P-4, P-12 regras)        | Fable 5.1                              | `claude-fable-5-1` | a prosa do kernel é o que as lentes obedecem em todas as rondas de todos os engagements                                           |
| **Frente A** — `su-confirmed-guard.py`, `dashboard.py` (`round_delta`, faceta `sem locator`), `aisa-round` step 5f/6 (P-2, P-12 hook) | Opus 5                                 | `claude-opus-5`    | código com critério fechado; fast mode aceitável                                                                                  |
| **Frente A** — validação: `/round` na cópia de pilot-3                                                                                | **modelo de produção dos engagements** | ver nota           | as lentes correm no modelo da sessão; validar noutro não prova nada                                                               |
| **Frente B** — templates (P-8, P-9)                                                                                                   | Opus 5                                 | `claude-opus-5`    | edições mecânicas, aceitação aritmética; fast mode aceitável                                                                      |
| **Frente B** — validação: re-render pilot-1                                                                                           | modelo de produção                     | ver nota           | idem                                                                                                                              |
| **Frente C** — glossário "como se diz", regra de output, `aisa-orient`, `COMO-USAR.md` (P-13, P-14)                                   | Fable 5.1                              | `claude-fable-5-1` | a linguagem é o entregável; o teste é de leitura humana                                                                           |
| **Frente C** — validação: sessão nova sem comando; `/status`, `/round`, `/resume` lidos por quem não construiu                        | modelo de produção                     | ver nota           | idem                                                                                                                              |
| **Frente D** — `fields_draft.py`, `render-validate.py`, `slot_sources`, `sufficiency:` (P-6 motor, P-7)                               | Opus 5                                 | `claude-opus-5`    | motor sobre JSON conhecido, regras por slot declaradas                                                                            |
| **Frente D** — `lens-data`/`lens-operations` cues, `as-is.md` template, G4 conforme P-11 (P-5, P-10)                                  | Fable 5.1                              | `claude-fable-5-1` | mandato e forma-alvo são prosa que outras skills obedecem                                                                         |
| **Frente D** — validação: re-render pilot-1 e `dpt-galp-jp`                                                                           | modelo de produção                     | ver nota           | idem                                                                                                                              |
| **Frente E** — P-15, P-16, P-17 (motor, hook, testes de regressão) | Opus 5 | `claude-opus-5` | correcções pequenas com reprodução executável como critério; fast mode aceitável |
| **Frente E** — P-18 desenho (o que identifica uma versão aprovada; transição `decision → options`) | Fable 5.1 | `claude-fable-5-1` | mesma sessão que o desenho de A5; decisão de forma que três comandos consomem |
| **Frente E** — P-18 código | Opus 5 | `claude-opus-5` | após o desenho |
| **Escrita dos passos do tracker** (`step-9x-*.md`) e actualização deste plano                                                         | Fable 5.1                              | `claude-fable-5-1` | registo que sobrevive à sessão; precisão da linguagem                                                                             |

**Nota — modelo de produção.** É o modelo em que os engagements reais vão correr `/round`, `/frame`, `/options`, `/render`. Candidatos: **Sonnet 5** e **Opus 5**, à escolha do utilizador. **"Sonnet passa ⇒ Opus passa" não é válido** para as regras deste plano: são regras de contenção (não escrever a `Unknown` invariante, não subir a afirmação acima da evidência, não usar jargão), e o modelo mais forte é o mais capaz de as contornar por raciocínio — as 7 `Confirmed` acima do nível em pilot-3 são 6 em R-04, a ronda com mais raciocínio encadeado. Regras:

- **Validar nos dois** enquanto os dois forem candidatos. Critérios distintos, registados no passo do tracker: em Sonnet 5, contar regras **não aplicadas** (passo saltado, `Unknown` sem `swing`, output curto); em Opus 5, contar regras **contornadas** (`Confirmed` acima do nível, `Assumed` promovida por cadeia, `decisivo` com referente inventado) e o saldo `criadas − fechadas` por ronda.
- Motores e hooks são independentes do modelo: validar uma vez.
- **Perfil por fase, não global — DECIDIDO pelo dono em 2026-09-08** (aceite sobre a medição de `step-9c` §5.2.4; implementação em `pack.yaml` pendente): **Discovery (`/round`, 6 lentes inline, volume alto) em Sonnet 5**; **Framing, Options e Decision (council, 7 subagentes, síntese) em Opus 5**; motores e hooks indiferentes. A linha "modelo de produção" da tabela acima lê-se agora por fase.
  A medição que sustenta a decisão, e o que ela **não** prova: R-05 em duas cópias de `pricing-marinha-pilot-3`, uma ronda por lado (`n = 1`, abaixo do ≥ 3 do protocolo §6.3), esforço `high` nos dois. **Zero regras contornadas dos dois lados** — a preocupação desta nota não se materializou. A diferença medida foi de posição, não de disciplina: Sonnet fechou 2 de 2 perguntas executando spikes, Opus abriu 7 e fechou 0. Fica **por medir** o comportamento no esforço por defeito: um passe em `high` é forte para as regras de contenção e **não transfere para baixo**, sobretudo no lado Sonnet, onde o critério é "regras não aplicadas". Revisitar se a produção correr fora de `high`, ou na retro do primeiro engagement real.

**Fast mode** (`/fast`): só nas linhas Opus 5 marcadas "fast mode aceitável". Nunca em julgamento, nunca em validação.

**Subagentes do council** (frentes que tocam `/frame`, `/options`): o modelo vem da definição em `.claude/agents/*.md`; não muda com `/model` da sessão. Fora do âmbito destas frentes — registar se aparecer.

---

## 6. Protocolo de validação (aplica-se a todas as frentes)

1. **Cópias reais, não fixtures**: `pricing-marinha-pilot-3` para Discovery; `pricing-marinha-pilot-1` (blueprint v05 aprovado, estado congelado) e `dpt-galp-jp` para render.
2. **Contagens pelo motor**: `dashboard.py --json` antes e depois. Contagem manual não é evidência.
3. **Não determinismo**: qualquer comparação de `/round` ou `/render` entre versões usa ≥ 3 runs por lado, ou usa um teste determinístico (reclassificação manual, `render-validate.py`).
4. **Invariantes**: total de pessoa-dias não muda com P-8/P-9/P-10 (são projecções); nenhuma row da SU é apagada; nenhuma `PM-U` Critical desaparece sem disposição; nenhuma `Confirmed` nova sem locator resolúvel (P-12); reclassificações são transições append-only, nunca edições de estado.
5. **Registo**: cada frente é um passo em `docs/pp-pack-authoring/pilot/` (tracker canónico), com um commit por correcção e tag de freeze; o quadro *Estado por correcção* em §5 aponta para o passo.

---

## 7. Descartado, e porquê

| Item | Motivo |
|---|---|
| F1 (frame provisório, `ASK-n` extraídos do pedido) | **substituído por P-0**: a fonte certa é o dono, o conteúdo certo é o mecanismo. Extrair do `literal_request` ancoraria num pedido solution-shaped e `ASK-3` aceitaria tudo |
| F3 como hook (`decisivo` proibido) | `decisivo` tem referente em Discovery (frame); o problema era a ausência de árbitro (P-1) |
| F4 (etiqueta "bloqueante") | recria a inflação de D2; a convergência mede-se sem etiqueta (P-2) |
| F5 por defeito (mecânica → `DISMISS`) | teria dispensado `PM-U-003` → `U-075`; substituído por teste de conteúdo (P-3) |
| F6a (rename `lens-effort`) | custo real toca hook, agente, pack, phases, dashboard; facto de um cliente no kernel; dimensionar to-be em Discovery |
| F6b (perfis de lentes) | adiado até haver um 2.º engagement com perfil distinto |
| E1 com soma exacta | força fabricação de granularidade; substituído por bandas (P-9) |
| E2 grid semanal | sobreposição é julgamento, equipa é inferida; substituído por ocupação por perfil (P-9) |
| E6 como correcção | fora do engagement por arquitectura; fica nota |
| G1a (campos no `ux-blueprint`) | negócio não aprova tipos; schema no artefacto de UX |
| G1b (`/datamodel`) | comando novo desnecessário; A5 já é o dono |
| G2 para autoridade externa | produziria o schema do artefacto errado; substituído por `access_contract` (P-6) |
| G3 como "custo baixo" | o motor é stub; é trabalho de motor (P-7) |
| G-§6 "regressão" como facto | não demonstrado; é hipótese (P-11) |

---

## 8. Rastreabilidade

| Origem | Destino |
|---|---|
| D4, F1, declaração do dono 2026-09-08 | P-0 |
| Regra do owner sobre `Confirmed` 2026-09-08, amostra de 30, `states.md` l.9/l.17 | P-12 |
| Owner 2026-09-08: "o framework é para quem não o construiu"; jargão do kernel no output | P-13 |
| Owner 2026-09-08: mensagem em linguagem natural sem `/start` tem de receber enquadramento e passos | P-14 |
| D1, D2, U-070, F2, F3 | P-1 |
| D3, F4 | P-2 |
| D5, F5, G2 (parte Discovery) | P-3 |
| §5, F6a, F6b | P-4 |
| G1 §3.1(a), E-D5 (fonte) | P-5 |
| G1, G2 (parte Architecture) | P-6 |
| G3, §4 | P-7 |
| G5, E-D8, E8 | P-8 |
| E-D1, E-D2, E-D4, E-D7, E1, E2, E4, E7 | P-9 |
| E-D3, E3, E5 | P-10 |
| G4, G-§6 | P-11 |
| `ADVERSARIAL_REVIEW_2026-09-08.md` F06 + PyYAML | P-15 |
| F01, F02, F11, F12 | P-16 |
| F03 | P-17 |
| F04, F05, F07, F08 | P-18 |
| F09 · F10 · observação `LIBRARY/` | emendas a P-9 · P-1 · `pre-write-guard.py` |
| R1–R8, G4.1 | mantêm-se como avisos do que **não** importar da referência |
| §9 dos três docs ("o que não está errado") | inalterado; nenhuma correcção toca a honestidade epistémica, os portões de construção, a aritmética declarada, a provenance |