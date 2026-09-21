# Fase 2 — Inventário, resolução de referências e atualidade

Data: 2026-09-14. Ramo: `runtime-correction/pilot-r1-r7`, working tree em `f4ffef2`.
Plano: `docs/runtime-hardening/coverage-reconciliation-implementation-plan.md` §12, fase 2.
Entrada: `coverage-phase-1-report.md`, fechado e revalidado antes desta passagem.

Este relatório incorpora a **segunda e a terceira voltas**, depois das revisões que
devolveram a fase 2. O que mudou está na §4; o resto descreve o estado corrigido.

> **A cobertura continua por avaliar.** Esta fase entrega o denominador, os locators e a
> atualidade. Não valida registos, não emite veredictos de cobertura, não tem `check`,
> `report` nem `finalize`, e não está ligada a comando, hook ou portão nenhum. Um
> engagement sem registos continua `not_evaluated`. **Nenhuma cobertura de blueprint foi
> avaliada nesta fase**, nem a do engagement real nem a de fixture nenhuma.

## 1. Pré-requisitos verificados

As sete dependências que a fase 1 declarou, e o que aconteceu a cada uma:

| # | dependência | estado |
|---:|---|---|
| 1 | ler o relatório e o README das fixtures antes de escrever código | feito |
| 2 | `build_inventory` reproduz as 79 unidades, ou justifica a diferença | **reproduz, chave a chave e pela mesma ordem** (§3.1) |
| 3 | implementar a canonicalização da §6.5 e trocar os placeholders no harness | feito; os registos da fase 1 hidratam e dão `current` (§3.4) |
| 4 | manifesto por etapa + exclusão de inventário + **T19 completo** | feito; o T19 compara a base inteira (§3.3) |
| 5 | corrigir o alias `concretizes_decision` com teste próprio | **entregue como patch, bloqueado pelo harness** (§5) |
| 6 | adapter de leitores sem importar `dashboard.py` no topo | feito (§2.2) |
| 7 | não integrar em `build_model`, skills ou hooks | respeitado — zero ficheiros existentes alterados |

Revalidação de fecho da fase 1 antes de começar: 63 testes verdes, e a `v01` da fixture
continua a passar a verificação estrutural com `valid: yes (0 block, 0 warn)` — a
propriedade F06 mantém-se.

## 2. O que foi construído

### 2.1 Ficheiros

| ficheiro | o que é |
|---|---|
| `library/kernel/tools/coverage.py` (novo, 47 KB) | o motor: inventário, manifesto, fingerprints, atualidade, locators, CLI `inventory` |
| `.claude/tests/test_coverage_inventory.py` (novo, 86 testes) | denominador, granularidade, exclusão da aprovação, locators, fronteira de caminhos, CLI |
| `.claude/tests/test_coverage_freshness.py` (novo, 50 testes) | canonicalização, T19 completo, ciclos que não podem morder, mudanças que têm de morder |
| `docs/runtime-hardening/patches/f16-decision-ref-alias.patch` (novo) | a correcção F16, por aplicar (§5) |
| `library/kernel/coverage-contract.md` | §6.2 clarificada: granularidade do tier de texto (§4.2) |

**Um único ficheiro existente alterado:** `library/kernel/tools/dashboard.py`, +19/-1,
que é a correcção F16 (§6). Tudo o resto são entradas novas. Nada em `projects/`, nada em
`.claude/skills/`, `.claude/hooks/`, `.claude/commands/` ou `.claude/settings.json` — a
integração nos comandos continua a ser fase 4.

### 2.2 A API, e porque tem esta forma

```python
build_inventory(eng, readers)                      -> dict   # o denominador
compute_basis(eng, inventory, stage, target, ...)  -> dict   # manifesto + 3 digests
check_freshness(record, current, target_now)       -> dict   # current | stale
resolve_unit(eng, unit_key)  /  resolve_target(eng, target)  # locators
canonical_json(obj) / digest(obj)                            # §6.5
```

**O adapter.** `coverage.py` não importa `dashboard.py` no topo: a classe `ReaderAdapter`
carrega-o sob procura, com um método por leitor usado. Não é um framework de plugins — é
um objecto simples e um ponto único onde trocar os leitores num teste. O plano §4.1 pedia
exactamente isto, e a razão é concreta: o dashboard vai chamar este módulo na fase 4, e um
import no topo dos dois lados fecharia o ciclo.

**A raiz do repositório vem de `__file__`, nunca de `sys.argv`.** É a lição da quarta volta
da fase 1, aplicada de origem: um módulo importável que lê os argumentos de quem o importa
passa a depender da forma de execução.

**Zero escrita.** Nenhuma função abre um ficheiro para escrita, cria directórios ou lança
subprocessos. Há um teste que corre a CLI duas vezes sobre uma cópia e compara o digest de
cada ficheiro antes e depois.

## 3. As provas que a fase pedia

### 3.1 O denominador é independente, e reproduz a expectativa da fase 1

```text
python library/kernel/tools/coverage.py inventory --engagement fx-coverage-f06
engagement: fx-coverage-f06
unidades: 79
  su-row 18 · xlsx-column 18 · enquadramento-theme 7 · answer-section 6 ·
  process-rule 6 · context-field 4 · input-file 3 · phase-artefact 3 ·
  process-question 3 · decision-block 2 · invariant 2 · lens-output 2 ·
  xlsx-sheet 2 · capture-index 1 · replay-report 1 · xlsx-dictionary-entry 1
limitações (1): inputs/fluxo-de-libertacao.pptx — sem extractor (COV-CAPTURE-LIMIT)
exit: 0
```

**79 unidades, as mesmas chaves, pela mesma ordem, as mesmas contagens por classe** que
`inventory-expected.json`. São duas implementações independentes da mesma derivação — a
expectativa da fase 1 e o motor da fase 2 — e é isso que faz da expectativa uma prova em
vez de um eco. Quando divergirem, alguém tem de dizer qual está certa.

A independência tem teste próprio: colocar um registo de cobertura dentro do engagement
não tira uma única unidade ao denominador. Se o registo o definisse, bastava omitir ao
mesmo tempo o requisito e a linha de revisão para obter falso verde — que é a falha que a
§6.1 do contrato existe para fechar.

### 3.2 Granularidade, e o que nunca desaparece

| caso | comportamento | teste |
|---|---|---|
| workbook **com** rascunho de campos | entra por **coluna** (18) | `test_a_workbook_with_a_fields_draft_enters_by_column` |
| o mesmo workbook | **não** entra também por folha — contaria duas vezes | `test_that_same_workbook_does_not_also_enter_by_sheet` |
| workbook **sem** rascunho | entra por **folha** (2) | `test_a_workbook_without_a_fields_draft_enters_by_sheet` |
| duas folhas homónimas em workbooks diferentes | chaves distintas, sem colisão (T09) | `test_homonymous_sheets_in_two_workbooks_do_not_collide` |
| grupo de colunas de forma repetida | os três membros separados; agrupar é do revisor (T10) | `test_the_repeated_column_group_keeps_its_members_separate` |
| entrada de dicionário sem dados | é unidade | `test_a_dictionary_entry_without_data_is_a_unit` |
| formato sem extractor | unidade **mais** limitação com motivo, impacto e acção (T08) | `test_an_unsupported_format_is_a_limitation_never_a_disappearance` |
| duas respostas ao mesmo id | ordinais explícitos, e a chave sem ordinal deixa de existir | `test_a_repeated_answer_section_gets_an_explicit_ordinal` |

A identidade da unidade sobrevive a uma mudança de conteúdo: muda o digest, não a chave
(contrato §5.2). É isso que permite dizer «esta unidade foi revista e depois mudou» em vez
de «apareceu uma unidade nova».

### 3.3 O T19, sobre a base completa

O ciclo que o plano §7.2 manda cortar: a revisão que autoriza a aprovação não pode ficar
`stale` no instante em que a aprovação é escrita. A fase 1 deixou este cenário como teste
preparatório sobre conjuntos de chaves; aqui compara-se **a base inteira**.

Acrescentando a uma cópia o bloco `D-003 — Blueprint bp-v03 aprovado` e a linha que o
espelha na Shared Understanding:

| dimensão da base | antes vs depois |
|---|---|
| `inventory_sha256` | **igual** |
| `su_fingerprint` | **igual** |
| `decision_fingerprint` | **igual** |
| manifesto, entradas `freshness` | **iguais** |
| veredicto | **`current`**, com `changed: []` |

E a prova de que o cenário não é vácuo: os bytes de `decisions.md` e de
`shared-understanding.md` **mudaram os dois**, e há um teste que o verifica. O que os
protege são duas regras diferentes a agir ao mesmo tempo — o manifesto marca-os
`informative` (§6.3) e o inventário retira-lhes o registo da aprovação (§6.1). Tirar só
uma das duas deixava a outra porta aberta, que foi o achado R8 da fase 1.

Os outros dois ciclos, pela mesma razão:

- **produzir uma versão nova do desenho** não invalida a revisão de uma anterior;
- **renderizar um deliverable** não invalida a revisão do desenho que ele projecta;
- **escrever num log ou regenerar o dashboard** não invalida nada (T18) — testado com
  `council-log.md`, `_capture/_capture-log.md`, `blueprint-log.md`, `dashboard.html`,
  `story.md` e `_synthesis-checks.md` todos tocados de uma vez.

### 3.4 O que **tem** de invalidar

| cenário | resultado | teste |
|---|---|---|
| T06 fonte nova em `inputs/` | `stale`, `source-added` | `test_a_new_source_file_makes_it_stale` |
| fonte removida | `stale`, `source-removed` | `test_a_removed_source_makes_it_stale` |
| T07 workbook alterado sem recaptura | `stale`, `source-changed` | `test_a_changed_workbook_without_recapture_makes_it_stale` |
| T20 requisito mudado, id igual | `stale` em `su_fingerprint` **e** `inventory_sha256` | `test_changing_a_requirement_row_makes_it_stale` |
| T20 decisão-solução mudada | `stale` em `decision_fingerprint` | `test_changing_the_solution_decision_makes_it_stale` |
| T17 resposta correctiva | `stale`, e a cadeia de supersessão preserva-se nos ordinais | `test_a_correcting_answer_makes_it_stale_and_keeps_the_old_one` |
| T21 alvo modificado | `stale`, `target-changed` | `test_modifying_the_target_makes_it_stale` |
| alvo desaparecido | `stale`, `target-missing` | `test_a_missing_target_is_reported` |
| T39 template de pacote alterado | `stale`, `authority-changed` | `test_a_changed_pack_template_makes_it_stale` |
| T41 `contract_version` diferente | sinalizado **à parte**, com a nota de que é `unsupported` | `test_a_different_contract_version_is_flagged_apart` |

`stale` traz sempre a razão de cada diferença e a nota de que **não declara falsa nenhuma
conclusão** — obriga a rever os impactos, que é o que o contrato §6.5 diz.

Os registos que a fase 1 escreveu **hidratam**: substituídos os três placeholders pelo que
o motor calcula, `rec-v04-blueprint-complete.json` dá `current` contra a fixture intacta, e
`stale` assim que uma fonte muda. Os digests de bytes que a fase 1 escreveu continuam a
bater certo com os ficheiros que nomeiam. Fecha a dependência 3.

### 3.5 Locators e fronteira de caminhos

Resolvem para **exactamente um nó**, ou devolvem o código — zero e dois nunca são um
fallback silencioso:

- nó do desenho, campo aninhado, ecrã, linha da SU, secção e linha de deliverable, coluna
  de Excel, passagem de transcrição por timestamp;
- **todas as 79 unidades do inventário resolvem** — se o motor a inventaria, tem de a
  saber encontrar outra vez;
- secção repetida sem ordinal → `COV-DEAD-REF` com `count: 2`; com ordinal → resolve;
- nó inexistente → `COV-INVALID-TARGET`;
- a linha que um render largou não resolve, mesmo com o id num comentário.

Fronteira (§5.3), recusado **sem ler**: traversal, escape relativo no meio do caminho,
absoluto fora do engagement. As autoridades do repositório — templates do pacote — são a
excepção declarada e continuam legíveis. Um selector com forma de expressão é dado
desconhecido, não código.

### 3.6 A CLI

| verificação | resultado |
|---|---|
| imprime o inventário, `exit 0` | ok |
| `--json` parseável, com `artefact` e `contract_version` | ok |
| corre de um directório de trabalho externo | ok |
| caminho com espaços e acentuação | ok |
| slug sob `AISA_ENGAGEMENTS_ROOT` | ok |
| engagement desconhecido | `exit 3`, com a mensagem |
| **vários engagements sem `--engagement`** | `exit 2`, nomeando-os — nunca escolher o primeiro (T27) |
| correr duas vezes | zero escrita, saída idêntica (T38) |

### 3.7 As provas da segunda volta

Cada achado foi **reproduzido antes de corrigir** e tem regressão que **falha quando o
defeito é reposto** — verificado com o motor revertido, não presumido:

| defeito reposto | testes que acendem |
|---|---|
| `inputs/` com `iterdir()` (A1) | 5 |
| erro de leitura a virar vazio (A2) | 4 |
| digest de autoridade copiado (A3) | 2 |
| versão do contrato em `changed` (A5) | 1 |

Os cenários, corridos sobre cópias temporárias:

```text
A1  inputs/extra/pedido.txt
    inventário  inputs/extra/pedido.txt  (nota: em subpasta de `inputs/`)
    manifesto   inputs/extra/pedido.txt  -> simétrico
    limitação   COV-CAPTURE-LIMIT (sem extractor)

A2  answers.md com bytes não-UTF-8
    unidades de resposta 0 · diagnósticos 1 · nível error · IMPEDITIVO
    inventário completo: False · CLI exit 4 · «DENOMINADOR INCOMPLETO»

A3  autoridade alterada, forma {path, sha256}
    declarado  d775d4f2a195e3f8
    actual     4f6c6fd9908646c1   -> recalculou

A4  library/packs/pp/deliverable-templates/...  permitido
    library/kernel/coverage-contract.md         permitido
    library/kernel/tools/dashboard.py           RECUSADO
    library/packs/mendix/pack.yaml              RECUSADO

A5  contract_version "0" vs "1"
    status: current · contract_version_mismatch.verdict: unsupported
```

A fuga por ligação (A4) é exercitada com **junção de directório** no Windows, porque o
symlink precisa de um privilégio que esta máquina não dá. A junção atravessa a fronteira
da mesma maneira. Num ambiente sem nenhuma das duas, os três testes **saltam** — e um
teste saltado não prova nada, o que fica dito.

## 4. O que a revisão devolveu, e o que mudou

Cinco achados. Quatro eram defeitos do motor, todos reproduzidos antes de corrigir e todos
com regressão que **falha quando o defeito é reintroduzido** — verificado, não presumido.

| # | achado | correcção | regressão |
|---:|---|---|---|
| A1 | `inputs/` percorrido com `iterdir()`: um ficheiro em `inputs/extra/pedido.txt` **entrava no manifesto** (que usa `rglob`) e **ficava fora do inventário**. O digest mudava e o denominador não — a pior assimetria possível, porque a fonte nova ficava invisível para a revisão e visível para a atualidade | percurso recursivo, com o caminho relativo inteiro como identidade: `inputs/extra/pedido.txt` não é `inputs/pedido.txt`. A limitação de captura acompanha-o, e a nota diz que veio de subpasta | `InputsAreWalkedRecursively`, 5 testes; reintroduzido o `iterdir()`, **5 falham** |
| A2 | `_read()` transformava erro de I/O ou de codificação em texto vazio: com `answers.md` ilegível saíam **zero unidades e zero diagnósticos** — uma fonte existente desaparecia calada | `read_source()` devolve `(texto, estado)` com `ok \| absent \| empty \| unreadable`. Ilegível é **diagnóstico impeditivo**; vazio é visível mas não impeditivo; o inventário passa a declarar `complete`, e a CLI sai **4** quando o denominador está incompleto | `UnreadableIsNotEmpty`, 7 testes; reposto o colapso, **4 falham** |
| A3 | `compute_basis()` copiava o `sha256` das autoridades recebidas em forma de mapa em vez de o recalcular: a base «actual» transportava evidência antiga, e uma alteração de template passava despercebida por essa via | o digest é **sempre** recalculado do ficheiro. O que o registo declara é histórico; a base é o presente. Autoridade ausente ou recusada pela fronteira é diagnóstico impeditivo, nunca um digest vazio em silêncio | `AuthorityDigestsAreAlwaysRecomputed`, 7 testes; reposta a cópia, **2 falham** |
| A4 | inventário e manifesto liam e hasheavam ficheiros **sem passar por `safe_path()`** — a fronteira só cobria os locators. E a lista de autoridades abrangia todo o `library/kernel/` e **todos** os pacotes | `engagement_files()` valida cada caminho resolvido **antes** de qualquer leitura, e é a porta única do inventário e do manifesto. Uma ligação para fora é recusada e **reportada** como impeditiva. As autoridades passam a lista fechada: os contratos e templates de síntese do kernel, e os templates do **pacote activo** — nem motores, nem outros pacotes | `EveryReadCrossesTheBoundary`, 5 testes, com junção de directório onde o symlink precisa de privilégio |
| A5 | `check_freshness()` descrevia a mudança de `contract_version` como `unsupported` e devolvia `status: stale` | sai de `changed` (que decide `stale`) para um campo próprio, `contract_version_mismatch`, com o veredicto `unsupported`. `stale` é «a base mudou, relê»; `unsupported` é «este motor não sabe ler este schema», e resolvê-lo com uma releitura não resolve nada | o teste do T41 foi virado: afirma `status: current` **e** o campo novo |
| A6 | F16 entregue como patch, sem aplicação nem testes | **mantido como pendência explícita** (§5). A entrega do patch não é a correcção instalada, e o relatório não o diz de outra maneira | dois testes continuam a afirmar o defeito |

### Terceira volta

Um achado, e é o mais instrutivo dos três lotes: **a correcção A4 estava incompleta**.

| # | achado | correcção |
|---:|---|---|
| A8 | F16 continuava entregue como patch e **não instalado** — «entregue» não é «corrigido» | o bloqueio do harness deixou de se aplicar nesta passagem e a correcção **foi instalada** em `library/kernel/tools/dashboard.py`. Os dois testes que afirmavam o defeito foram virados, como estava escrito neles desde a fase 1 |
| A7 | validei a **enumeração** dos ficheiros e deixei as fontes principais a serem lidas por `eng / nome`: contexto, enquadramento, respostas, SU, decisões, `_state.json`, os artefactos de captura por `glob`, e os dois fingerprints. Um caminho recusado na enumeração voltava a entrar pela outra via — e emitir um diagnóstico **depois** de ler não cumpre a obrigação de recusar **antes** | `guarded_read`, `guarded_read_json` e `guarded_sha256` passam a ser a **única** porta, e `refused` é um estado de leitura ao lado de `absent`, `empty` e `unreadable`. O `_capture/` percorre-se pela lista já validada, não por `glob` — um glob volta a enumerar o disco e dá a volta à fronteira. `_state.json` fica com a verificação de **raiz apenas**, e a razão está escrita: é ele que declara o pacote de que a lista de autoridades depende |

**A prova estrutural encontrou mais duas.** Escrevi um teste que lê a árvore sintáctica do
motor e falha se qualquer função de leitura chamar um leitor cru fora da porta. Passou a
acusar `build_manifest` e `compute_basis`, que liam caminhos **já validados** — o
comportamento estava certo, mas havia duas maneiras de ler, e quem viesse a seguir teria de
saber qual delas era segura. Ficou uma.

**E encontrou o mesmo defeito noutro sítio.** Com o percurso recursivo, o engagement real
passou de 1016 para **1036 unidades**: as 20 novas são
`lens-outputs/_council-prep/`, que o `iterdir()` não via. Estavam no manifesto e fora do
denominador — a mesma assimetria do achado A1, numa segunda pasta. **1016 estava errado.**

O contrato acompanhou: §5.3 passa a ter a lista fechada de autoridades e a exigir a
fronteira em **toda** a leitura, com a excepção de `_state.json` nomeada e justificada; §6.2 diz que `inputs/` é recursivo e que ausente, vazio e
ilegível são três estados distintos; §6.4 diz que o digest de uma autoridade é sempre
recalculado; §7 separa `unsupported` de `stale`. Quatro ambiguidades novas no registo da
§11. **Motor e norma não podem discordar em silêncio**, e a correcção de um sem o outro
seria meia correcção.

## 5. Decisões técnicas

**D20 — O workbook com rascunho de campos entra por coluna; o sem rascunho, por folha.**
A granularidade segue o que a captura produziu. Acrescentar unidades de folha a um
workbook que já entrou por coluna contaria a mesma coisa duas vezes, e um inventário que
conta a dobrar deixa de servir de denominador.

**D21 — O tier de texto entra como UM documento, não como N passagens.** Achado desta
fase: a CLI sobre o engagement real mostrou que `_capture/<ficheiro>.text.md` não entrava
no inventário — a superfície normalizada que as lentes lêem ficava fora do denominador,
que é precisamente a omissão silenciosa que este mecanismo existe para apanhar. A correcção
entra com a granularidade do **documento**: as 620 passagens dessa gravação dariam 620
unidades, que é a versão textual de «uma pergunta por célula» e cai na mesma proibição que
o contrato já impõe ao Excel. As passagens continuam **citáveis** —
`_capture/<ficheiro>.text.md#HH:MM:SS` resolve — porque um locator resolúvel e uma unidade
do denominador são coisas diferentes. O contrato §6.2 passou a dizer qual das duas leituras
vale, em vez de as deixar ambas em aberto; **motor e norma não podem discordar em
silêncio.** O ficheiro bruto e o documento normalizado são unidades distintas, e é
deliberado: o primeiro é autoritativo em conflito, o segundo é o que se lê.

**D22 — `None` colapsa para `""` na canonicalização.** Defeito apanhado por teste: o
contrato §6.5 diz que um valor ausente serializa como `""` e nunca `null`, e a primeira
implementação passava `None` inalterado. Sem isto, «campo vazio» e «campo ausente» davam
digests diferentes por acidente de leitura, e um leitor que mudasse de convenção
invalidava toda a gente.

**D23 — O `target` compara-se à parte do manifesto.** O alvo não está no manifesto (é um
alvo, não uma fonte), por isso `check_freshness` recebe o seu digest actual como terceiro
argumento. A alternativa — pôr o alvo no manifesto — reabriria o ciclo que a §6.3 fechou.

**D24 — `contract_version` diferente é sinalizado, não convertido em `stale`.** O motor
regista a diferença com a nota de que aquilo é `unsupported`, e deixa o veredicto de
validade para a fase 3, que é quem valida registos. Misturar os dois faria uma mudança de
contrato passar por «basta rever» (T39 vs T41).

**D25 — F16 entregue como patch, não aplicado.** §6.

**D26 — Um denominador incompleto declara-se incompleto.** O inventário traz `complete` e
`blocking_diagnostics`, e a CLI sai **4** quando há fontes que existem e não foram lidas.
Sair 0 com um ficheiro ilegível era dar por bom um denominador que já se sabia furado.

**D27 — A fronteira de leitura é uma porta, não um aviso.** `engagement_files()` valida
cada caminho resolvido antes de qualquer leitura ou hash, e é por lá que passam o
inventário e o manifesto. Ter a verificação só nos locators protegia o caminho que um
revisor escreve e deixava aberto o caminho que o motor percorre sozinho — que é o
contrário do que faz sentido.

**D28 — A lista de autoridades é fechada e depende do pacote activo.** Um motor do kernel
não é autoridade de leitura de uma revisão, e um pacote que este engagement não usa não o
condiciona. Prefixos largos (`library/kernel/`, `library/packs/`) davam acesso de leitura a
coisas que o contrato nunca autorizou.

**D29 — `unsupported` e `stale` são resultados diferentes e saem por campos diferentes.**
Misturá-los convida a tratar uma versão de contrato desconhecida com uma releitura.

**D30 — Uma porta, sem excepções para decorar.** Todas as leituras do motor passam por
`guarded_read` / `guarded_read_json` / `guarded_sha256`, incluindo as que já tinham o
caminho validado. Ter duas maneiras de ler obriga quem escreve código novo a saber qual é a
segura, e a resposta errada não dá erro nenhum — dá uma leitura que ninguém verificou.

**D31 — `_state.json` é a única excepção, e a excepção está escrita no código.** Leva a
verificação de raiz, porque é ele que declara o pacote de que a lista de autoridades
depende, e um ficheiro não se pode validar contra uma regra que ele próprio define.

**D32 — A regra de «uma porta» é verificada pela árvore sintáctica, não por revisão.** Um
teste percorre o motor e falha quando uma função de leitura chama um leitor cru fora da
porta. Foi assim que as duas últimas apareceram, e é assim que a próxima aparecerá.

## 6. F16: correcção instalada

O alias `concretizes_decision` → `decision_ref` **está corrigido no leitor**. Uma passagem
anterior não pôde tocar em `library/kernel/tools/dashboard.py` — o harness recusou a
modificação de um recurso partilhado — e entregou a correcção como patch, como o plano §2
manda nesse caso. Nesta passagem o bloqueio já não se aplicou, e a correcção foi instalada.

**A forma.** `decision_ref` conserva o valor **cru** do ficheiro, porque há fixtures e um
snapshot que o lêem tal e qual; `decision_id` é a forma **normalizada** — `D-002` tanto de
`decisions.md#D-002` como de `concretizes_decision: D-002` — e é essa que qualquer
consumidor deve comparar. Normalizar não é inventar: sem nenhuma das chaves, o id é vazio.

**O sintoma que desapareceu**, medido sobre o engagement real:

```text
antes   current.decision_ref: ""        (o YAML dizia concretizes_decision: D-002)
depois  current.decision_ref: "D-002"   decision_id: "D-002"
```

**Os dois testes que afirmavam o defeito foram virados**, como estava escrito neles desde a
fase 1: `test_coverage_fixtures.py::test_f16_is_fixed` e
`test_coverage_inventory.py::F16IsInstalled`. O segundo verifica o sintoma exacto que a
revisão do caso real registou, para que «entregue» e «instalado» não se confundam outra
vez. O ficheiro de patch fica como registo da alteração.

**O que não foi verificado, e não deve ser dado como verificado:** o snapshot de
`test_blueprint_yaml.py` **saltou** nesta máquina — `skipped 'engagements não montados'` —
porque os engagements que ele referencia não estão neste checkout. A hipótese de um
blueprint real de outro engagement precisar de uma entrada na lista de diferenças
justificadas continua **por testar**, e só um checkout com esses engagements montados o
pode dizer.

## 7. Comandos e resultados

```text
python library/kernel/tools/coverage.py inventory --engagement fx-coverage-f06
  79 unidades · 16 classes · 1 limitação · exit 0

python library/kernel/tools/coverage.py inventory --engagement pricing-bunkers-v2
  1036 unidades: xlsx-column 774 · su-row 112 · xlsx-dictionary-entry 42 ·
  answer-section 36 · lens-output 29 · process-rule 12 · process-question 8 ·
  enquadramento-theme 7 · context-field 4 · phase-artefact 3 · decision-block 2 ·
  input-file 2 · invariant 2 · capture-index 1 · replay-report 1 · text-extraction 1
  0 excluídas · 0 limitações · 0 diagnósticos · completo · exit 0
  (eram 1016 antes da terceira volta: as 20 diferenças são `lens-outputs/_council-prep/`,
   que o percurso não recursivo não via)

base do engagement real, etapa reconciliation:
  inventory_sha256    09da8bab30bb89d9708eb756bbcc96efbbb3161f952bf72f8129e572ee94b2f3
  su_fingerprint      3e9a3ea53d798072666a8a2a766c99fe1fd4abc200a9fc01519fbaecb93652ea
  decision_fingerprint 251653cf565f541907f7d3354b4f3d72f7ba18341b8fba569027c3e5b64a4540
  decision_ref        D-002 · pack pp
  manifesto           53 freshness + 2 informative
  informative         decisions.md · shared-understanding.md
  alvos no manifesto  nenhum
```

As 774 colunas do engagement real são a razão de o contrato §6.2 exigir contagens **por
tipo e por etapa**: anunciar «100% dos requisitos cobertos» porque 774 colunas receberam
disposição seria a mentira mais fácil deste mecanismo.

Suite completa, um ficheiro de cada vez, como `requirements-dev.txt` manda:

```text
34 ficheiros · 1644 testes
32 ficheiros OK
 2 ficheiros FAIL — os mesmos DOIS PRÉ-EXISTENTES de sempre:
   test_options_artefact.py::test_per_option_entries_stay_short
   test_state_scaffold.py::test_a_pre_v23_su_still_exists_untouched
Por discovery: as mesmas 2 falhas.
```

Os três módulos de cobertura: **64 + 86 + 50 = 200 testes, todos verdes.**

Integridade do engagement real, manifesto SHA-256 antes e depois de tudo:

```text
ficheiros: 76 -> 76   adicionados: []   removidos: []   alterados: []
VEREDICTO: ENGAGEMENT INTACTO
```

O motor correu **contra o engagement real**, e não lhe tocou.

## 8. Critérios de saída

| critério do plano | estado |
|---|---|
| inventário não controlado pelo registo do agente | **cumprido** — teste próprio: um registo no engagement não encolhe o denominador |
| nenhuma unidade omitida silenciosamente | **cumprido** — e a fase apanhou uma omissão real, o tier de texto (D21) |
| hashes e locators reproduzíveis | **cumprido** — canonicalização §6.5 implementada e testada; as 79 unidades resolvem |
| append de aprovação não invalida | **cumprido** — T19 sobre a base completa |
| execução em cwd externo funciona | **cumprido** — incluindo caminhos com espaços e acentuação |
| zero escrita em read-only | **cumprido** — digest de cada ficheiro antes e depois, duas execuções |
| testes existentes afectados continuam a passar | **cumprido** — as duas falhas pré-existentes e mais nenhuma |
| CLI `inventory` | **cumprido** |
| **nenhuma leitura fora da fronteira** | **cumprido** — inventário, manifesto, fingerprints, autoridades e locators pela mesma porta, com a excepção de `_state.json` nomeada e justificada (A4, A7). Verificado pela árvore sintáctica, não por leitura |
| **nenhuma fonte desaparece em silêncio** | **cumprido** — subpastas de `inputs/` (A1) e ficheiros ilegíveis (A2) |
| **a base actual não transporta evidência antiga** | **cumprido** — digests de autoridade sempre recalculados (A3) |
| corrigir o alias `concretizes_decision` | **cumprido** — instalado no leitor, com os dois testes virados (§6). Fica por testar a interacção com o snapshot, que salta neste checkout |

## 9. Limitações

1. **A cobertura continua por avaliar.** Nada nesta fase lê um registo, valida um schema ou
   emite um veredicto de cobertura. `check`, `report` e `finalize` são da fase 3.
2. **F16 está instalado, mas o snapshot não o testou** (§6). `test_blueprint_yaml.py`
   salta a comparação de snapshot neste checkout porque os engagements que ela referencia
   não estão montados. Um checkout com `pricing-marinha-pilot-*` pode revelar diferenças
   que precisem de entrada na lista justificada — **isso não foi verificado**.
3. **O tier de texto tem um só teste de formato.** A fixture não traz transcrição; os
   testes constroem uma em cópia temporária. O formato real foi lido do engagement, mas um
   `.docx` ou `.pdf` normalizado pode ter outra forma de passagem, e isso não está coberto.
4. **A política de atualidade é conservadora**, como o contrato §6.3 declara: uma mudança
   de formatação num ficheiro de fonte torna a revisão `stale`. É deliberado nesta primeira
   entrega, e o motor mostra sempre qual foi a diferença.
5. **Os registos das fixtures continuam com os placeholders.** Hidratam em tempo de teste e
   isso está provado; reescrevê-los com digests reais é opção da fase 3, quando `finalize`
   os passar a produzir.
6. **O inventário do engagement real não foi revisto por ninguém.** 1036 unidades é o
   denominador que o motor deriva; que sejam as unidades certas, com a granularidade certa,
   é julgamento que ninguém fez ainda.
7. **Duas falhas pré-existentes na suite**, nenhuma corrigida: uma exige alterar o
   engagement real, o que continua proibido; a outra exige montar outro engagement.
8. **O teste de fuga por ligação usa junção de directório no Windows.** O symlink precisa
   de privilégio que esta máquina não dá; a junção não, e atravessa a fronteira da mesma
   maneira. Num ambiente sem nenhuma das duas, os três testes **saltam** em vez de passar —
   e um teste saltado não prova nada, o que é dito em vez de escondido.
9. **Os seis achados foram encontrados por revisão externa, não pelos meus testes.** Os
   testes que agora os protegem foram escritos depois. Vale a pena dizê-lo: a suite da
   primeira volta estava verde com quatro defeitos lá dentro, e a da segunda estava verde
   com a correcção A4 feita pela metade. O teste que lê a árvore sintáctica existe por
   causa disso — foi escrito para ser o primeiro a apanhar o próximo.
10. **A contagem do engagement real mudou de 1016 para 1036** e a primeira estava errada.
   Nenhum número deste relatório deve ser lido como estável antes de a fase 6 correr a
   validação integrada.
10. **Nada foi commitado nem publicado.**

## 10. Dependências concretas para a fase 3

1. Correr `test_blueprint_yaml.py` **num checkout com os engagements do snapshot montados**
   e, se o F16 acusar diferença, acrescentar a entrada justificada com a sua regra. A
   correcção está instalada e os dois testes já foram virados; o que falta é esta
   verificação, que salta neste checkout (§6).
2. Implementar a validação de schema contra o contrato §4, usando os 20 registos da fase 1
   — os negativos existem para disparar um código cada um.
3. Implementar a selecção de revisão por etapa/target/autoridade (§6.6) e os veredictos
   separados da §7, com `not_evaluated` como resultado legítimo.
4. Implementar `check`, `report` e `finalize`, os códigos de saída da §7, e a finalização
   exclusiva que nunca sobrescreve uma versão publicada.
5. Demonstrar o F06 nos dois sentidos com os registos que já existem: `covered` sem destino
   falha; o destino decorativo mantém-se `partial`/`missing`; a revisão fundamentada do
   percurso completo pode dar cobertura completa **sem aprovação**.
6. Não integrar nada em comandos, skills ou hooks: isso continua a ser fase 4.

## 11. O que esta fase explicitamente não declara

Nenhuma pergunta em aberto do engagement real foi respondida — `U-028` e `U-030` continuam
abertas. Nenhuma aprovação foi registada em nome de ninguém. O blueprint real **não** está
aprovado, **não** está completo e **não** está validado E2E. A cobertura do engagement real
**não foi avaliada**: o que existe é o seu denominador, e um denominador não é um veredicto.
