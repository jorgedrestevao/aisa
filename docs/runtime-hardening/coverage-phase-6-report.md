# Fase 6 — Validação integrada e entrega

Data: 2026-09-16 · ramo `runtime-correction/pilot-r1-r7` · plano:
`docs/runtime-hardening/coverage-reconciliation-implementation-plan.md` §12 → *Fase 6*

**O que esta fase faz.** Valida. Não constrói mecanismo novo: corre os 40 cenários, o
percurso completo em fixture, a revisão do diff e a integridade do engagement real, e
corrige o que encontrar dentro do âmbito da implementação.

> **Os dois E2E, e a distinção que este relatório não deixa cair.**
>
> O que aqui se demonstra é o **E2E do protocolo do framework**: a sequência de
> verificações — fontes → reconciliação → desenho → aprovação → projecção — comporta-se
> como o contrato diz, do princípio ao fim, sem saltos, **em fixture**.
>
> O que aqui **não** se demonstra, não se tenta e não se afirma é o **E2E da solução de
> pricing**: que a solução desenhada funcione ponta-a-ponta com dados reais, utilizadores
> reais e integrações reais. Nada nesta frente executa uma solução. A aprovação que aparece
> no passo 7 do ensaio é escrita pelo próprio script numa cópia temporária e está marcada
> como simulada no bloco que a escreve.
>
> Confundir os dois seria exactamente a afirmação que este mecanismo existe para impedir.

---

## 1. As cinco fases, verificadas

| fase | entrega | evidência lida | estado à entrada da fase 6 |
|---|---|---|---|
| 1 — Contrato e cenários | contrato v1, 20 registos, fixture `fx-coverage-f06`, denominador de 79 unidades | `coverage-phase-1-report.md` | critérios cumpridos; 8 limitações declaradas, das quais a 1 («não há motor») fechada pela fase 2-3 |
| 2 — Inventário e atualidade | denominador independente, locators, fingerprints | `coverage-phase-2-report.md` | cumprida; limitação 2 (snapshot do blueprint salta neste checkout) **continua aberta** |
| 3 — Verificador e registos | CLI, 13 códigos, `finalize` versionado | `coverage-phase-3-report.md` | cumprida; limitação 4 («`render` não exercitada a sério») fechada pela fase 5 |
| 4 — Integração no desenho | `/blueprint` 1b e 13b, `status.coverage`, hooks | `coverage-phase-4-report.md` | cumprida e **validada por revisão independente** (45 testes; correcção do dashboard) |
| 5 — Preservação nos deliverables | pré-render, revisão de projecção, autoridade de versão | `coverage-phase-5-report.md` | cumprida **após correcção**: um falso positivo aceitava uma especificação sem aprovação (§2.9 dessa fase), e a classe foi varrida (§2.10) |

Duas limitações herdadas que esta fase **não** fecha, e diz porquê:

- **O snapshot de `test_blueprint_yaml.py` continua a saltar** (fase 2, limitação 2; fase 3,
  limitação 5). Precisa de um checkout com os engagements `pricing-marinha-pilot-*`
  montados, que este não tem. Fica **inconclusivo**, nunca «OK».
- **As duas falhas pré-existentes da suite** (`test_options_artefact.py`,
  `test_state_scaffold.py`) continuam. Leem conteúdo de `projects/`, que é um ponto de
  montagem privado; fechá-las exige alterar o engagement real, que esta frente tem proibido.

---

## 2. Os 40 cenários, executados

`docs/runtime-hardening/repro-coverage-phase6-matrix-2026-09-16.py` →
`docs/review-evidence/coverage-phase6-matrix-2026-09-16.md`

**40 OK · 0 falhas · 0 inconclusivos.**

A matriz é uma **execução**, não um mapeamento por citação: cada cenário é montado numa
cópia da fixture, corrido, e o veredicto observado comparado com o que o plano §13 exige.
A diferença importa — dez cenários (T04, T08–T15, T28) só tinham referência no README das
fixtures, e mapeá-los por citação teria dado a mesma tabela verde sem provar nada.

Um cenário que o executor não consiga montar sai **inconclusivo**, nunca OK. É a regra que
a fase 1 aprendeu quando «inconclusivo» foi lido como verde (P-15), e está no código do
executor, não só na prosa.

**Um defeito encontrado aqui, e era do teste.** O T25 (hooks que não dispararam) falhou à
primeira: a minha asserção procurava a frase documentada em português e ela está escrita em
inglês, nas duas skills que correm o motor. A asserção passou a verificar a frase real —
`the hook is a convenience, never the mechanism` — nas duas.

---

## 3. O percurso completo, de ponta a ponta do protocolo

`docs/runtime-hardening/repro-coverage-phase6-flow-2026-09-16.py` →
`docs/review-evidence/coverage-phase6-flow-2026-09-16.md`

Dez passos, em sequência, sobre **uma só** cópia da fixture — como um percurso real
correria, e não dez casos isolados:

| # | passo | resultado |
|---:|---|---|
| 2 | reconciliação completa sobre as fontes | `complete` · elegível |
| 3 | desenho v01: **estrutura válida, requisito perdido** | `gaps` · 0 bloqueios estruturais |
| 4 | v02 corrige C-007; C-010 ainda parcial | `gaps` |
| 5 | v03: cobertura completa e actual | `complete` · base `current` |
| 6 | **cobertura completa não é aprovação** | aprovada: nenhuma; a spec continua bloqueada |
| 7 | aprovação (simulada, fixture) **não invalida a revisão que consome** | base `current` |
| 8 | render v01: obrigação perdida, id em comentário | `gaps` |
| 9 | render v02: a projecção carrega o que foi pedido | `complete` |
| 10 | **resposta nova torna as três etapas `stale`** | render, desenho e reconciliação |
| 11 | a aprovação registada sobrevive à invalidação | aprovada: v03; cobertura por rever |

O F06 fica demonstrado **nos dois sentidos** no mesmo percurso: no passo 3 a versão que o
verificador estrutural dá por válida perdeu um requisito que a SU carregava; no passo 5 a
versão corrigida sai completa **sem** que isso aprove coisa nenhuma.

---

## 4. A revisão do diff

`docs/runtime-hardening/repro-coverage-phase6-review-2026-09-16.py` →
`docs/review-evidence/coverage-phase6-review-2026-09-16.md`

**6 de 6 limpas**, cada uma por medição:

| # | pergunta | como foi medida |
|---:|---|---|
| 1 | estados ou autoridades duplicados | a versão aprovada vem de `dashboard.blueprint_state` por delegação; o motor não tem segunda implementação |
| 2 | hardcodes do caso real | zero no motor e no contrato; os nomes dos exemplos são da **fixture** — 0 ocorrências em `projects/` |
| 3 | imports circulares | `coverage → dashboard` sob procura; `dashboard → coverage` não existe |
| 4 | hashes autorreferenciais | `_coverage/` e os alvos fora da base; publicar um registo não torna o anterior stale |
| 5 | fallback silencioso para revisão antiga | parte-se a revisão **mais recente**: escolhe-a na mesma e mostra a lacuna |
| 6 | alterações excessivas ao framework | 0 ficheiros apagados, 0 encolhidos; 93% do trabalho em ficheiros novos |

**Um defeito encontrado aqui, e era da verificação.** A pergunta 6 acusava, com um limiar
que eu tinha inventado (≤ 2 remoções por ficheiro) e que apanhava reescritas de linha — que
é o que quase toda a edição de prosa é. «Excessivo» não é o número de linhas removidas: é
comportamento retirado. A medição passou a ser essa — ficheiros apagados, ficheiros que
encolhem — e as 28 remoções são todas metade de uma reescrita.

---

## 5. O engagement real, antes e depois

`docs/runtime-hardening/repro-coverage-phase6-integrity-2026-09-16.py` →
`docs/review-evidence/coverage-phase6-integrity-2026-09-16.md`

**Zero ficheiros alterados pelos comandos read-only**, em 117, com manifesto SHA-256 antes
e depois. Correram-se 10 comandos: `inventory`, `check reconciliation`,
`report reconciliation`, `check blueprint v09` e os seis pré-render.

**Um achado, e é real.** `dashboard.py --json` **escreve** — reconstrói `dashboard.html` no
engagement, porque o `--json` é um *also dump*: exporta o modelo **e** rebuilda. Eu tinha-o
posto na lista de comandos read-only, e a primeira corrida acusou 1 ficheiro alterado. O
defeito era da minha classificação, não do dashboard:

- o que ele escreve é o artefacto **derivado** que qualquer `/dashboard` e o hook
  `on-su-change.py` reescrevem, e que o contrato já trata como derivado (§6.3,
  `DERIVED_FILES`) — não entra na base de atualidade de revisão nenhuma;
- entre duas reconstruções seguidas **só varia o carimbo de tempo** do comentário de build;
  o hash de build é idêntico;
- e a minha corrida regenerou-o. Está dito aqui porque foi uma escrita minha no engagement
  do utilizador, ainda que sem efeito no conteúdo.

O ensaio passou a medir as duas coisas em separado: os comandos read-only, que têm de
escrever zero, e o `--json`, que escreve por desenho e cujo efeito é nomeado.

**O engagement real está a ser usado com o mecanismo.** Encontrei 13 registos de cobertura
em `projects/pricing-bunkers-v2/_coverage/`, com datas de 15 e 16 de Setembro, publicados
por quem conduz o engagement — não por esta frente. Os veredictos que a evidência mostra
(`reconciliation: gaps, elegível`; `blueprint v09: complete`) são **lidos** desses registos.
**Não os produzi, não os revi e não os valido.** Uma cobertura `complete` continua a ser a
segunda das quatro perguntas, e só essa.

---

## 6. A suite requerida

`docs/review-evidence/coverage-phase6-suite-2026-09-16.txt`

Corrida como `requirements-dev.txt` manda — `python <ficheiro>`, um a um, todos os 39 —
com as versões do ambiente registadas no topo do ficheiro: Python 3.11.9, PyYAML 6.0.3,
openpyxl 3.1.5. As duas dependências de desenvolvimento estão instaladas, por isso **nenhum
teste ficou por correr por falta de dependência** — que é a forma de inconclusivo que a
fase 1 apanhou a ser lida como verde (P-15).

**39 ficheiros · 1906 testes · 2 falhas · 7 testes saltados.**

As **2 falhas** são as pré-existentes da §1, com o mesmo texto de sempre.

**Os 7 testes que não correram, um a um.** Nenhum deles é «OK»; todos são inconclusivos, e
seis são a mesma causa — este checkout não tem montados os engagements que eles leem:

| ficheiro | teste | razão declarada |
|---|---|---|
| `test_blueprint_yaml.py` | `Snapshot::test_no_unjustified_difference` | engagements não montados |
| `test_frame_identity.py` | `RealEngagementsStillParse::test_existing_approvals_are_legacy_not_broken` | no engagements mounted |
| `test_render_validate.py` | `RealPilot1::test_dry_run_writes_nothing` | pilot-1 v02 not mounted |
| `test_render_validate.py` | `RealPilot1::test_v02_against_the_approved_v05_yields_the_three_families_of_gaps` | pilot-1 v02 not mounted |
| `test_reopen_transition.py` | `RealEngagementUnaffected::test_pilot_1_still_reports_its_decision` | engagement not mounted |
| `test_synthesis_checks.py` | `StampHasToBeSupported::test_the_real_engagement_that_persists_pairs_is_read` | engagement nao montado |

O **sétimo é de outra natureza**, e é o que merece ser lido com atenção:

| ficheiro | teste | razão declarada |
|---|---|---|
| `test_coverage_integration.py` | `TheRealEngagementIsUntouched::test_a_real_engagement_without_records_is_not_evaluated` | **este engagement já tem registos de cobertura** |

Este teste verifica que um engagement real **sem** registos lê `not_evaluated`. Deixou de
poder correr porque `pricing-bunkers-v2` passou a ter 13 registos, publicados hoje por quem
conduz o engagement (§5). O teste salta-se sozinho, pela sua própria guarda, e está certo
em fazê-lo — a premissa que ele precisa deixou de se verificar. Mas isso significa que a
propriedade que ele protege **não está a ser verificada neste checkout**, e é inconclusiva
como as outras seis.

Os seis primeiros fecham-se com um checkout que monte `pricing-marinha-pilot-*`; o sétimo
fecha-se com um engagement sem `_coverage/` — a fixture tem essa forma, e a cobertura dessa
propriedade sobre fixture existe (`NeverGreenByAccident` na fase 5). Nenhum dos dois é
trabalho que este checkout possa fazer.

---

## 7. Evidência final da §15

`docs/review-evidence/coverage-phase6-evidence15-2026-09-16.md`, gerada por
`repro-coverage-phase6-evidence15-2026-09-16.py`.

| ponto | onde está |
|---|---|
| §15.1 ficheiros alterados e divergências do plano | §7 deste relatório + §6 da fase 5 e §4-§5 das fases 1-3 |
| §15.2 comandos e resultados, com falhas e limitações | §2, §3, §4, §5, §6 deste relatório |
| §15.3 F06 em fixture, nos dois sentidos | §3, passos 3 e 5 |
| §15.4 invalidação por resposta nova; aprovação não invalida | §3, passos 10 e 7 (e T17/T19/T20 na matriz) |
| §15.5 CLI JSON e Markdown reais, sem editar o engagement | evidência §15.5 — 0 ficheiros alterados em 117 |
| §15.6 sem identificadores do caso real; read-only não escreve | evidência §15.6 — máximo 0 fora da lista do guarda |
| §15.7 limites remanescentes | §8 deste relatório |
| §15.8 nada declarado sobre o blueprint real | o aviso do topo e §9 |

**Uma nota de medição na §15.6.** A primeira contagem acusou 5 ocorrências dos termos do
caso real em `test_coverage_fixtures.py`. São a lista de tokens que
`test_no_identifier_of_the_real_case_leaks_into_the_fixture` procura para os **proibir** —
o teste tem de os nomear. Contá-los como violação seria acusar a fechadura de ser a porta
aberta; a medição passou a distingui-los, e fora dessa lista o máximo é **0**.

### Divergências face ao plano, consolidadas

| divergência | justificação |
|---|---|
| O token de versão por deliverable vive no **template** (`blueprint_version_read`), não numa tabela do kernel | o plano §9.2 proíbe a tabela «requisito → deliverable» e manda reutilizar o que existe; o campo já existia num template. O motor não contém o nome de deliverable nenhum |
| Campo `blueprint_version_read` **ausente** é defeito, não `none` | era a única leitura que podia falhar em silêncio no campo que decide a autoridade |
| `applicability` é **opcional** no registo | um deliverable não produzido não tem registo; o seu *skip* em `render-log.md` é a resposta inteira |
| O pré-render é `check --stage render --deliverable <id>` **sem `--target`**, em vez de subcomando novo | antes de produzir não existe alvo |
| A regra do comentário **devolve o nó, marcado**, em vez de o esconder | escondê-lo fá-lo-ia passar por locator morto, que é outro defeito |

---

## 8. Limites remanescentes

1. **A compreensão semântica não é provada por código, e não passa a ser.** O motor
   verifica a forma da ligação — que o destino existe, que está no artefacto sob revisão,
   que não é um comentário. Se a secção apontada *diz* o que a obrigação exige é julgamento
   do agente, escrito e assinado (§9 do contrato). Os 40 cenários exercitam a **declaração**;
   nenhum deles prova compreensão.

2. **Há fontes que não se capturam.** Um `.pptx`, uma macro, um formato sem extractor entram
   como limitação declarada (`COV-CAPTURE-LIMIT`) e nunca como cobertas. O mecanismo garante
   que a limitação **aparece**, não que desaparece.

3. **O resultado depende do julgamento do agente.** Quais unidades geram obrigações, e se
   uma projecção preserva o que foi pedido, é declarado por quem revê.

4. **A classe «campos declarados que ninguém concilia» foi varrida por enumeração, não por
   prova** (fase 5, §2.10). Um campo acrescentado ao schema entra na mesma classe e precisa
   da mesma pergunta; nada no motor o obriga automaticamente.

5. **`deliverable.authority_sources` não é comparado com a prosa do template.** Compará-los
   por texto seria adivinhar; fica para a passagem destino → fonte, que é do agente.

6. **Sete testes não correram neste checkout** (§6), e nenhum deles conta como passado.
   Seis pedem engagements que não estão montados; o sétimo — o que verifica que um
   engagement real **sem** registos lê `not_evaluated` — deixou de poder correr porque o
   engagement passou a ter registos.

7. **Duas falhas pré-existentes continuam abertas** (§1), e nenhuma fase desta frente as
   pode fechar sem tocar no engagement real.

8. **A política de atualidade é conservadora.** Uma mudança de formatação numa fonte torna a
   revisão `stale`. É deliberado, e o motor mostra sempre qual foi a diferença.

---

## 9. O que esta entrega declara, e o que não declara

**Declara:** o mecanismo de reconciliação e cobertura está implementado nas três etapas,
ligado aos comandos, documentado nos contratos, e exercitado por 40 cenários, um percurso
completo e uma suite de 39 ficheiros. Os comandos read-only não escrevem. O código não
contém identificadores do caso real.

**Não declara:**

- que o desenho de `pricing-bunkers-v2` está aprovado — nenhuma aprovação foi registada por
  esta frente, e nenhuma aprovação histórica foi tocada;
- que está completo — a cobertura que existe foi publicada por quem conduz o engagement, e
  esta frente limitou-se a lê-la;
- que está validado ponta-a-ponta — o E2E demonstrado é o **do protocolo**, em fixture;
- que a implementação está concluída sem reservas — **sete testes não correram** neste
  checkout, e isso é inconclusivo, não verde. O plano é explícito: *«não declarar
  implementação concluída se houver fase/teste obrigatório pendente»*. Seis deles fecham-se
  num checkout com os engagements montados; o sétimo fecha-se contra um engagement sem
  registos de cobertura.

---

## 10. O que falta para fechar a frente

Nada disto é construção; é execução num ambiente que este checkout não tem.

1. **Correr a suite num checkout com `pricing-marinha-pilot-*` montados** e confirmar os
   seis testes que aqui saltaram — em especial o snapshot de `test_blueprint_yaml.py`, que
   está pendente desde a fase 2 e pode revelar diferenças que precisem de entrada na lista
   justificada.
2. **Correr `test_coverage_integration.py` contra um engagement sem `_coverage/`**, para
   que a propriedade «sem registos lê `not_evaluated`» volte a ser verificada sobre um
   engagement real e não só sobre fixture.
3. **Fechar ou reclassificar as duas falhas pré-existentes** — ambas exigem decisões sobre
   conteúdo de `projects/`, que é do dono do engagement, não desta frente.

Enquanto os três estiverem por fazer, a frente está **entregue e por confirmar**, não
fechada.
