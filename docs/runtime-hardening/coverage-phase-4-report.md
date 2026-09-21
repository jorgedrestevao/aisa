# Fase 4 — Integração em blueprint, respostas e status

Data: 2026-09-15. Ramo: `runtime-correction/pilot-r1-r7`, working tree sobre `f4ffef2`.
Plano: `docs/runtime-hardening/coverage-reconciliation-implementation-plan.md` §12, fase 4.
Entrada: `coverage-phase-1-report.md`, `-2-` e `-3-`, lidos, com os pré-requisitos
verificados por execução antes de escrever código (§1).

> **O que mudou de estado.** A fase 3 entregou o motor e deixou-o desligado. Esta fase
> **liga-o em duas das três etapas**: `reconciliation` e `blueprint`. `/blueprint` passa a
> reconciliar antes de produzir e a rever a versão depois; `/answer` e `/capture` calculam o
> efeito na atualidade; `/status` expõe `status.coverage`; o hook do desenho reporta a
> cobertura **ao lado** da estrutura. **A etapa `render` continua por ligar** — é a fase 5, e
> `aisa-render` não foi tocado.
>
> **O que não mudou.** Nenhuma aprovação foi registada em nome de ninguém, e o motor
> continua sem conseguir escrever uma. Nenhuma aprovação histórica foi revogada. Nenhuma
> pergunta em aberto foi respondida. **A cobertura do engagement real continua
> `not_evaluated`** — verificado em leitura, com manifesto antes e depois. `not_evaluated`
> não é aprovação nem reprovação.

## 1. Pré-requisitos verificados

As seis dependências que a fase 3 declarou (§10 do seu relatório):

| # | dependência | estado |
|---:|---|---|
| 1 | chamar o motor de `/blueprint`, `/answer`, `/capture` e `/status`, com chamadas explícitas e sem booleano em `_state.json` | feito (§2.2, §2.3, §2.4); a ausência do booleano é testada (§4, `ReadOnly`) |
| 2 | actualizar `blueprint-contract.md`, `phases.md` e `orchestration.md` **no mesmo incremento** | feito (§2.5) |
| 3 | expor no `/status` as quatro perguntas separadas, em linguagem de negócio | feito (§2.4); bloco 5b, e o lint das duas línguas passa |
| 4 | ligar o feedback ao hook do desenho e os gatilhos de `_coverage/`, sem ciclos de escrita | feito (§2.6); a ausência de ciclo é testada, não afirmada |
| 5 | testar o legado: sem `_coverage/` e **com** aprovação histórica; hooks que não dispararam | feito (§4, `Legacy` e `test_no_hook_is_the_mechanism`) |
| 6 | não tocar na selecção nem na projecção dos deliverables | respeitado — zero linhas em `aisa-render`, `render-validate.py` ou `render-contract.md` |

Revalidação de fecho da fase 3 antes de começar: as cinco suites de cobertura verdes,
**354 testes**, `OK`.

## 2. O que foi construído

### 2.1 Ficheiros

| ficheiro | o que mudou |
|---|---|
| `library/kernel/tools/dashboard.py` | +~190 linhas: `coverage_module()` (carga tardia, sem ciclo de import), `_coverage_stage()`, `coverage_status()` e a sua entrada em `build_model` → `status.coverage`; `_coverage` em `INDEX_DIRS` + `GROUP_LABEL` (§3.4); `TOOL_VERSION` 1.13.0 → **1.14.0** |
| `library/kernel/tools/coverage.py` | só o cabeçalho: quem o chama, e que `render` continua por ligar. **Zero alterações de comportamento** |
| `library/kernel/coverage-contract.md` | cabeçalho: de «contrato em implementação» para «activo no desenho; pendente nos deliverables», com a fronteira escrita |
| `library/kernel/blueprint-contract.md` | regra dura **7** (nova aprovação exige revisão aplicável) + secção *Cobertura — a segunda pergunta sobre a mesma versão* |
| `library/kernel/phases.md` | saídas da Decision incluem `_coverage/`; nota *Readiness is not approval* nas regras de transição — sem quinta fase |
| `library/kernel/orchestration.md` | um parágrafo ligando a sobrevivência da compreensão ao registo, sem duplicar definições |
| `library/kernel/glossary.md` | 4 termos novos com a frase de negócio (`Coverage review`, `Reconciliation`, `Stale`, `not_evaluated`) |
| `.claude/skills/aisa-blueprint/SKILL.md` | passo **1e** (reconciliação antes de produzir), passo **13b** (revisão da versão produzida, duas passagens), passo **15** reescrito (dois checks + cinco condições + `AskUserQuestion`), 2 linhas novas no output, regra dura 10 |
| `.claude/skills/aisa-answer/SKILL.md` | passo **7b** (atualidade calculada, nunca declarada), 1 linha no output, regra dura 8 |
| `.claude/skills/aisa-capture/SKILL.md` | passo **7b** (recheck depois de mudar fonte ou extractor), 1 linha no output |
| `.claude/skills/aisa-status/SKILL.md` | leitura de `status.coverage`, bloco de output **5b** com as quatro respostas, regras duras 8 e 9, `--check` passa a 7 ficheiros de protocolo e 4 motores |
| `.claude/hooks/blueprint-validate.py` | reporta cobertura **em bloco separado** da estrutura; silencioso quando limpa; sem registo diz *não avaliada*; nunca escreve |
| `.claude/hooks/on-su-change.py` | `_coverage/` entra nos gatilhos, com a razão de não haver ciclo escrita no ficheiro |
| `.claude/hooks/phase-completeness.py` | dois itens de cobertura na Decision, **só depois de existir versão não-rascunho** |
| `.claude/commands/{blueprint,status}.md`, `.claude/hooks/HOOKS.md`, `docs/ARCHITECTURE.md` | descrição do protocolo e dos limites; nenhuma afirmação de check não implementado |
| `.claude/tests/test_coverage_phase4.py` (novo) | **45 testes** |
| `.claude/tests/test_coverage_fixtures.py` | 1 teste reescrito: o cabeçalho do contrato mudou de facto, e a asserção muda com ele |
| `.claude/tests/test_blueprint_yaml.py` | pino da versão do motor: 1.13.0 → 1.14.0 |

### 2.2 `status.coverage` — quatro perguntas, quatro campos

```python
coverage_module()                        -> dict | None   # carga tardia de coverage.py
coverage_status(eng, bp, pack)           -> dict          # a dimensão irmã de blueprint/síntese/render
```

```text
readiness.structure ...  valid | invalid | not_evaluated      (de bp_validate — o que já existia)
readiness.coverage  ...  complete | gaps | stale | invalid | unsupported | not_evaluated
readiness.approval  ...  approved | approved-other-version | absent   (um bloco D-NNN, nada mais)
readiness.e2e       ...  not_evaluated                        SEMPRE. Nada aqui prova ponta-a-ponta.
```

mais `stages.{reconciliation,blueprint}` com os veredictos por etapa, `gaps`, `codes`,
`blockers` (cada um prefixado pela etapa que o levantou), `limitations`, `diagnostics` e
`julgamento`.

**Não há ciclo de import.** `coverage.py` lê `dashboard.py` pelo seu `ReaderAdapter`;
importá-lo no topo recursava. A carga é tardia, e o adapter recebe os globals deste módulo
— o dashboard não é reconstruído do outro lado.

**Não há custo para quem não tem registos.** Sem nada em `_coverage/`, `coverage_status`
devolve `not_evaluated` sem construir denominador nenhum: não há contra o que o comparar, e
é o caso de todos os engagements existentes. Medido: **0,34 s** sem registos, **1,31 s** com
registos (uma única construção de inventário, partilhada pelas duas etapas).

### 2.3 As chamadas explícitas

| onde | quando | comando |
|---|---|---|
| `aisa-blueprint` 1e | antes de produzir | `coverage.py check --stage reconciliation` |
| `aisa-blueprint` 13b | depois de produzir | `finalize` + `check --stage blueprint --target …` |
| `aisa-blueprint` 15 | antes de pedir aprovação | `--blueprint-check` **e** `check --stage blueprint` |
| `aisa-answer` 7b | depois de responder | `check --stage reconciliation` (+ blueprint se houver versão) |
| `aisa-capture` 7b | depois de capturar | `check --stage reconciliation` |
| `/status` | em cada consulta | `dashboard.py --json` → `status.coverage` |

**O hook nunca é o mecanismo**, e está escrito nos três sítios (skill, hook, `HOOKS.md`):
uma sessão onde nenhum hook disparou perde visibilidade, não perde verificação.

### 2.4 A condição de **nova** aprovação (contrato §8.1)

Cumulativa com tudo o que já bloqueava:

1. revisão da etapa `blueprint` **actual** para **esta** versão concreta;
2. `semantic_review.status: completed`, com as duas passagens;
3. nenhum requisito material `missing`/`partial` sem disposição de âmbito autorizada;
4. os bloqueios estruturais que já existiam (regra 5 + verificação estrutural);
5. o pedido explícito ao negócio, por `AskUserQuestion`, que **nenhum motor substitui**.

`not_evaluated` **não** é passe. `eligible: true` diz que a versão pode ser **levada** ao
negócio — nada mais, e o `julgamento` do modelo diz isso por escrito.

**O que não mudou de propósito:** `draft: true` continua a significar *candidato antes da
decisão* (regra 4), e **não** passou a marcar «produzido com lacunas». Uma versão com
lacunas é produzida, escrita e discutida como qualquer outra; só não se anuncia pronta para
aprovação. Aprovações já registadas não são reescritas, superseded nem revogadas: uma versão
aprovada antes de o mecanismo existir mantém a aprovação, e a sua cobertura lê-se como *não
verificada* — a diferença que o contrato §10 manda mostrar.

### 2.5 Os contratos, no mesmo incremento

A regra só entra no runtime com os contratos actualizados, e entrou:
`blueprint-contract.md` (regra 7 + secção), `phases.md` (saídas + *readiness ≠ approval*,
sem quinta fase), `orchestration.md` (o registo como forma verificável da disposição que já
existia), `coverage-contract.md` (o cabeçalho deixa de dizer que nada está ligado).

### 2.6 Hooks: relatam, não impõem, e não geram ciclos

- **`blueprint-validate.py`** — dois blocos, nunca fundidos. Silencioso quando a estrutura
  está limpa **e** a cobertura está `complete`/`current`. Sem registo: uma linha a dizer
  *não avaliada… não revoga aprovação nenhuma*. Escreve zero (testado por manifesto).
- **`on-su-change.py` + a detecção de alterações do dashboard** — `_coverage/` entra nos
  gatilhos do hook **e** em `INDEX_DIRS`, que é o que `_needs_rebuild` percorre. As duas
  metades são precisas: o hook lança o gerador **sem** `--force`, por isso um gatilho
  sozinho não regenerava nada (§3.4). **Não pode ciclar**: o `finalize` escreve com
  `open()` + `os.replace()` num subprocesso, que é I/O e não uma chamada de ferramenta,
  por isso o `PostToolUse` nunca dispara nele; e o dashboard lê `_coverage/` e escreve só
  `dashboard.html`, que fica na raiz do engagement e está excluído da varredura. Testado
  nos dois sentidos.
- **`phase-completeness.py`** — os dois itens de cobertura só existem quando há versão
  não-rascunho em `_blueprint/`. Logo depois de `/decide` não há desenho para cobrir: o hook
  não pede nada e não reporta nada. Lê os registos por nome e dois campos — sem inventário,
  porque um `Stop` corre em cada fim de turno.

## 3. As provas

### 3.1 O ensaio do percurso, gerado por código

`docs/review-evidence/coverage-phase4-rehearsal-2026-09-15.md`, produzido por
`docs/runtime-hardening/repro-coverage-phase4-2026-09-15.py` numa cópia temporária da
fixture. Os seis estados, como o executor os percorre:

| passo | estrutura | cobertura | aprovação | ponta-a-ponta | pode ir a aprovação |
|---|---|---|---|---|---|
| 1. sem revisão nenhuma | `valid` | `not_evaluated` | ausente | `not_evaluated` | — |
| 2. reconciliação publicada | `valid` | `not_evaluated` | ausente | `not_evaluated` | não (falta a do desenho) |
| 3. revisão da `v01` | **`valid`** | **`gaps`** (C-007, C-010 `missing`) | ausente | `not_evaluated` | não |
| 4. `v03` desenhada e revista | `valid` | `complete` | **ausente** | `not_evaluated` | **sim — «pode ser levada»** |
| 5. aprovação acrescentada | `valid` | `complete` | `approved (v03)` | `not_evaluated` | sim |
| 6. resposta nova (`/answer`) | `valid` | **`stale`** | `approved (v03)` | `not_evaluated` | não |

A linha 3 é a asserção central do plano, agora pelo caminho que o utilizador percorre: **a
mesma versão que o verificador estrutural dá por válida perdeu dois requisitos que a Shared
Understanding já carregava.** A linha 4 separa *cobertura revista* de *o negócio aprovou*. A
linha 5 fecha o ciclo que o §6.4 existe para partir — acrescentar a aprovação **não**
invalidou a revisão que ela consome. A linha 6 mostra `stale` com a aprovação intacta.

O hook, sobre a mesma `v01`, com exit 0 e zero escritas:

```text
[blueprint-validate] ux-blueprint_v01.yaml — cobertura: gaps · atualidade: current · registo: valid · leitura nos dois sentidos: completed
  lacuna · item-001 · C-007 · missing
  lacuna · item-005 · C-010 · missing
  códigos: COV-KNOWN-GAP
  → Há obrigações por cobrir ou por fundamentar; a versão pode continuar em discussão, mas não se anuncia pronta para aprovação.
  → estrutura e cobertura são perguntas separadas; nenhuma delas é aprovação. Detalhe: `python library/kernel/tools/coverage.py check --engagement fx --stage blueprint --target _blueprint/ux-blueprint_v01.yaml`
```

Sobre a `v03` corrigida, o mesmo hook fica **em silêncio**.

### 3.2 O engagement real, em leitura

```text
projects/pricing-bunkers-v2 — 75 ficheiros, manifesto SHA-256 antes e depois de DUAS
construções do modelo: idênticos, zero diferenças.

readiness: {structure: valid, coverage: not_evaluated, approval: absent,
            e2e: not_evaluated, current_version: v04}
```

Ninguém reviu nada neste engagement, e o relatório não diz o contrário. A `v04` continua sem
aprovação registada, e nada aqui a aprova nem a reprova.

### 3.3 Os testes

`.claude/tests/test_coverage_phase4.py` — **45 testes**, verdes, em 7 grupos:

| grupo | o que prende |
|---|---|
| `FourQuestions` (5) | T01 estrutura válida ≠ desenho coberto · T02 referência decorativa não é cobertura · T03 cobertura completa ≠ aprovação · ponta-a-ponta nunca afirmado · o bloco publica o seu julgamento |
| `NeverAFalseGreen` (9) | sem registo · leitura por acabar (T30) · registo ilegível (T24) · schema futuro · motor ausente · estrutura inválida como bloqueio próprio · **T22 revisão de outra versão não se consome para esta** · **T23 a mais recente ganha mesmo sendo a pior** · **T37 pergunta em aberto não é lacuna** |
| `Freshness` (5) | T17 resposta nova invalida · T20 decisão alterada invalida · **T19 aprovação acrescentada NÃO invalida** · T21 versão editada invalida · T18 dashboard e logs não invalidam |
| `Legacy` (3) | T35 aprovação histórica preservada e reportada; nenhuma decisão reescrita; `not_evaluated` não é passe nem chumbo |
| `ReadOnly` (3) | T38 duas leituras, mesmo resultado e zero mutações · nenhum booleano em `_state.json` · as skills proíbem-no por escrito |
| `Hooks` (10) | os dois blocos separados · «não avaliada» nunca como «sem lacunas» · zero escritas · **publicar uma revisão torna a página desactualizada (F01) e regenerá-la não pede outra** · a pasta entra no índice com nome de negócio · `_coverage/` como gatilho · T25 nada pedido antes de haver desenho, pedido depois, satisfeito pelos registos, e os checks explícitos correm sem hooks |
| `Protocol` (10) | passos 1e/13b, as cinco condições da nova aprovação, `AskUserQuestion`, `draft` intacto, atualidade sem flag, as quatro respostas no `/status`, os contratos, e o cabeçalho do motor a dizer onde está ligado |

Um defeito apanhado por estes testes durante a fase, e corrigido: o rótulo do passo novo
colidia com o `1b` que o portão de arquitectura já usava — passou a **1e**. Outro: dois
bloqueios com a mesma frase e sem dizer de que etapa vinham — passaram a trazer o prefixo da
etapa.

### 3.4 F01 da revisão independente — publicar cobertura não actualizava a página

Uma revisão independente correu sobre esta entrega e encontrou um defeito real, dentro do
âmbito (trabalho 5 da fase: *triggers/watch*). Está corrigido, e o mérito do achado é dela.

**O defeito.** Acrescentei `_coverage/` aos gatilhos de `on-su-change.py` e parei aí. Mas o
hook lança o gerador **sem `--force`**, e quem decide se vale a pena regenerar é
`_needs_rebuild`, que percorre `INDEX_DIRS` — onde `_coverage` não estava. Com a página já
existente, publicar uma revisão mais recente devolvia `needs_rebuild == False`: o modelo
mudava (`status.coverage`), a página ficava com o veredicto antigo, e o observador do
`--serve` também não a regenerava. **Meio arranjo lê-se como arranjo, e é pior do que
nenhum.**

**A correcção.** `_coverage` entra em `INDEX_DIRS` — que serve as duas coisas, a detecção de
alterações e o índice de ficheiros — e ganha rótulo em `GROUP_LABEL` («Conferência do que foi
pedido»). Uma linha de lista, e o comentário que diz porque é que ela lá está, para que o
próximo que a leia não a tire.

A revisão vive em `docs/review-evidence/coverage-phase4-validation-2026-09-15.md` (com a
sua própria evidência: `coverage-phase4-focused-*.txt` e `coverage-phase4-tests-*.txt`).
O seu repro, `docs/review-evidence/repro-coverage-phase4-watch-2026-09-15.py`, antes e
depois da correcção:

```text
antes:   coverage newer than dashboard: True · needs_rebuild: False · expected: True   (falha)
depois:  coverage newer than dashboard: True · needs_rebuild: True  · expected: True   (exit 0)
```

**E não cicla**, verificado nos dois sentidos e preso por teste: página escrita depois da
revisão → `needs_rebuild False`; revisão nova depois da página → `True`. O gerador escreve só
`dashboard.html`, que fica na raiz do engagement e está fora da varredura.

## 4. Comandos e resultados

```text
# revalidação de fecho da fase 3 (antes de tocar em código)
python -m unittest test_coverage_contract test_coverage_inventory test_coverage_freshness \
                   test_coverage_integration test_coverage_fixtures
  -> Ran 354 tests ... OK

# a suite da fase 4
python .claude/tests/test_coverage_phase4.py
  -> Ran 45 tests ... OK

# o repro da revisão independente (F01)
python docs/review-evidence/repro-coverage-phase4-watch-2026-09-15.py
  -> needs_rebuild: True · expected: True · exit 0

# o ensaio, gerado por código
python docs/runtime-hardening/repro-coverage-phase4-2026-09-15.py
  -> docs/review-evidence/coverage-phase4-rehearsal-2026-09-15.md

# custo do modelo
sem registos 0,34 s · com registos 1,31 s · engagement real 1,38 s (sem registos)
```

Suite completa do repositório: ver §7 — o resultado e as falhas pré-existentes.

## 5. Critérios de saída

| critério do plano | estado |
|---|---|
| nova resposta invalida revisão aplicável | **cumprido** — `Freshness`, e o passo 6 do ensaio |
| versão com lacunas pode existir mas não é anunciada pronta para aprovação | **cumprido** — produção nunca bloqueada, `approve_eligible: false`, e a frase está no contrato, na skill e no hook |
| checks funcionam explicitamente sem hooks | **cumprido** — `test_no_hook_is_the_mechanism`, e escrito nos três sítios |
| aprovação histórica não é revogada | **cumprido** — `Legacy` (3 testes) e §10 do contrato |
| o motor nunca escreve nova aprovação | **cumprido** — o motor não tem código para isso, os hooks não chamam `finalize`, e a skill pergunta por `AskUserQuestion` antes de escrever |
| a observação do status não gera ciclos de escrita | **cumprido** — manifesto igual depois de duas construções, no sintético e no real; e a razão de `_coverage/` não ciclar está escrita no hook |
| significado de `draft` inalterado | **cumprido** — testado (`Protocol`) e escrito no contrato |
| gatilhos e observação do dashboard capturam a cobertura | **cumprido** — `INDEX_DIRS` + gatilho do hook; repro da revisão independente passa; ausência de ciclo testada (§3.4) |
| render fora de âmbito | **cumprido** — zero linhas em `aisa-render`, `render-validate.py`, `render-contract.md` |
| testes prioritários T01–T04, T17–T25, T30, T35–T38 | **cumpridos** exceto T04, que fica parcial (§6, limitação 2). T36 ficou fechado na fase 2 e não se repete aqui |

## 6. Limitações

1. **A compreensão semântica continua por provar, e não passa a estar provada.** O motor
   verifica a **forma** da declaração — o destino resolve, o papel é pertinente à etapa, a
   exclusão tem autoridade. Quem julga se o desenho responde mesmo ao que foi pedido é o
   revisor, e assina. Um revisor que minta no `role` de um destino só é apanhado quando o nó
   não existe.
2. **T04 fica parcial.** *«Resposta contém obrigação ausente da SU → a unidade exige
   reconciliação»* está coberto na parte mecânica (a unidade entra no denominador e a sua
   ausência de revisão dá `COV-UNREVIEWED`, testado na fase 2). A parte que falta é
   semântica — **o motor não sabe quais unidades geram obrigações** (limitação 11 da fase 3),
   e continua a não saber. A fase 4 pede ao executor que preencha `links.coverage_items`; não
   o pode impor.
3. **O ensaio é do protocolo, em fixture sintética.** Não é o ponta-a-ponta de nenhuma
   solução de negócio, e `readiness.e2e` é `not_evaluated` em todos os seis passos, de
   propósito.
4. **A página do dashboard lista as revisões, mas não mostra os veredictos.** O modelo expõe
   `status.coverage`, o `/status` imprime as quatro respostas, e os ficheiros de `_coverage/`
   aparecem no separador *Ficheiros* como «Conferência do que foi pedido». O que **não**
   existe é um painel com as quatro respostas na própria página — não é critério desta fase,
   e mexer na projecção HTML tem o seu próprio risco de regressão. Recomendação explícita
   para a fase 6. Consequência prática: quem só olha para a página vê que houve revisões, não
   vê o que elas dizem.
5. **A etapa `render` está implementada e continua por exercitar a sério.** É a fase 5.
6. **A política de atualidade continua conservadora**: uma mudança de formatação numa fonte
   torna a revisão `stale`. É deliberado, e o motor mostra sempre qual foi a diferença.
7. **Custo.** Com registos, cada construção do modelo custa ~1,3 s (uma construção de
   inventário). O hook `on-su-change` regenera o dashboard em background e não bloqueia o
   utilizador; o `blueprint-validate` corre em primeiro plano, mas só numa escrita de
   desenho.
8. **O tempo medido inclui um segundo agente a correr testes neste mesmo working tree**, em paralelo com esta passagem.
9. **Uma revisão independente correu em paralelo, e encontrou um defeito que os meus testes
   não apanhavam** (§3.4). A lição é a de sempre nesta frente: uma verificação que confirma
   só a sua metade não está verificada. Acrescentei `_coverage/` aos gatilhos e escrevi o
   teste do gatilho; ninguém tinha testado o que o gerador faz **depois** de ser chamado.
   Os dois testes que agora prendem isso foram escritos a seguir ao achado, não antes.
10. **Nada foi commitado nem publicado.**

## 7. Suite completa do repositório

Executada ficheiro a ficheiro, como `requirements-dev.txt` manda
(`for f in .claude/tests/test_*.py; do python "$f"; done`):

```text
PASSED_FILES=36
FAILED_FILES: test_options_artefact.py  test_state_scaffold.py
```

**36 dos 38 ficheiros verdes.** As duas falhas são **as duas pré-existentes**, as mesmas que a
fase 3 já reportou, e nenhuma toca o mecanismo de cobertura:

| ficheiro | falha | porquê é pré-existente |
|---|---|---|
| `test_options_artefact.py` | `test_per_option_entries_stay_short`: *pricing-bunkers-v2 O-004 entry is 226 words (budget 120)* | mede o comprimento de um bloco de `projects/pricing-bunkers-v2/options.md`, ficheiro que esta fase não tocou. A palavra «coverage» que aparece neste ficheiro é *concern coverage* do artefacto de opções — outro conceito, sem relação com este mecanismo |
| `test_state_scaffold.py` | `test_a_pre_v23_su_still_exists_untouched`: *no pre-v2.3 SU left to prove tolerance against* | pede que exista em `projects/` uma Shared Understanding anterior à v2.3 para provar tolerância; não existe nenhuma montada neste checkout. É uma falha de fixture ausente, não de código |

Corri a suite **duas vezes**: uma em paralelo com o trabalho, outra em bloco sobre o código
final desta entrega. Os dois resultados são o mesmo, e as duas falhas são as mesmas nas duas.
Nenhuma foi corrigida aqui — corrigir a primeira é editar um engagement real, e corrigir a
segunda é montar uma fixture que não pertence a esta fase.

## 8. Dependências concretas para a fase 5

1. Ligar a etapa `render`: precheck por deliverable (autoridades exigidas + aplicabilidade
   dos slots) e postcheck de projecção, reutilizando `applicability`, `authority_sources`,
   `slot_sources` e `sufficiency` que já existem. Não criar tabela kernel «requisito →
   deliverable».
2. Selecção de versão por deliverable: *latest authorized* para o Architecture Blueprint,
   *approved* para a Implementation Specification e o Claude Design Brief — a cobertura
   **verifica**, não redefine (contrato §8.3).
3. Casos que não podem ficar retidos: sem UI, headless, sem arquitectura autorizada, legacy.
   Ausência legítima é *não aplicável*, nunca lacuna.
4. Um id num comentário não prova preservação: T32 é o teste que o prende.
5. O render nunca reabre o Excel para preencher um campo em falta — devolve a lacuna ao dono
   a montante.

## 9. O que esta fase explicitamente não declara

O desenho real **não** está aprovado, **não** está completo e **não** está validado
ponta-a-ponta. A cobertura do engagement real **não foi avaliada**. Nenhuma pergunta em
aberto foi respondida. Nenhuma aprovação foi registada, e nenhuma aprovação histórica foi
tocada. O que esta fase entrega é **a pergunta a ser feita no sítio certo, e a resposta a
aparecer separada das outras três**.
