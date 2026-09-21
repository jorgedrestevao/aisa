# Fase 1 — Contrato, decisões técnicas e fixtures

Data: 2026-09-14. Ramo: `runtime-correction/pilot-r1-r7`, working tree em `f4ffef2`.
Plano: `docs/runtime-hardening/coverage-reconciliation-implementation-plan.md` §12, fase 1.

> **O motor não existe.** Esta passagem entrega o contrato, o denominador esperado e as
> fixtures. `library/kernel/tools/coverage.py` não foi escrito, nenhuma CLI foi criada,
> nenhum comando, hook ou portão mudou de comportamento, e nenhuma política de aprovação foi
> alterada no runtime. As fases 2 a 6 constroem e ligam o mecanismo.

Este relatório incorpora a **segunda, a terceira e a quarta voltas**, depois das revisões
que devolveram a fase 1. O que mudou em cada uma está na §3; o resto do documento descreve o
estado corrigido.

## 1. Âmbito entregue

| entregável | ficheiro |
|---|---|
| Contrato v1 | `library/kernel/coverage-contract.md` (46 KB) |
| Engagement sintético que reproduz o F06 | `.claude/tests/fixtures/coverage/fx-coverage-f06/` (29 ficheiros, 3 versões de desenho) |
| Denominador esperado | `.claude/tests/fixtures/coverage/inventory-expected.json` (79 unidades) |
| Exemplos JSON válidos e inválidos | `.claude/tests/fixtures/coverage/records/` (20 registos) |
| Mapa fixtures ↔ cenários ↔ fase | `.claude/tests/fixtures/coverage/README.md` |
| Geradores das fixtures (reprodutibilidade) | `.claude/tests/fixtures/coverage/build_workbooks.py` e `build_fixtures.py` |
| Teste de integridade da especificação | `.claude/tests/test_coverage_fixtures.py` (63 testes, verdes) |
| Este relatório | `docs/runtime-hardening/coverage-phase-1-report.md` |

56 ficheiros novos, ~636 KB. **Zero ficheiros existentes alterados.** `git status` mostra
apenas entradas novas (`??`); nada em `projects/`, nada em `.claude/skills/`,
`.claude/hooks/`, `.claude/commands/` ou `.claude/settings.json`.

## 2. Baseline verificado antes de escrever (§3 do plano)

| facto do plano | verificado |
|---|---|
| `bp_validate` aceita `concretizes_decision`, mas o leitor procura só `decision_ref` | **sim** — `dashboard.py:3066` (leitor) e `:3274` (validação). Reproduzido na fixture: `bp_read` devolve `decision_ref: ""` sobre um ficheiro com `concretizes_decision: D-002` |
| `build_model` calcula blueprint, síntese e render em separado | **sim** — `blueprint_state`, `synthesis_state`, `render_state` |
| `on-su-change.py` enumera directórios observados e `_coverage/` não está lá | **sim** — `TRIGGER_DIRS` em `.claude/hooks/on-su-change.py:34` |
| `render-validate.py` tem verificações de suficiência úteis, mas a sua selecção de blueprint não serve todos os deliverables | **sim** — o motor resolve tudo contra o blueprint **aprovado** |
| Os hooks são complementares e nem todos disparam | **sim** — ver o achado B1 abaixo |

Dois achados novos do baseline, registados e **não** corrigidos aqui:

- **B1 — qualquer directório com `_state.json` é resolvido como engagement pelos hooks
  `PostToolUse`, esteja onde estiver.** Ao escrever o espelho da fixture com a ferramenta
  `Write` (num directório temporário, fora do repositório), os hooks geraram lá
  `dashboard.html`, `council-log.md` e `_synthesis/_synthesis-checks.md`. Não é falha de
  segurança — é ruído — mas significa que **editar a fixture com Write/Edit contamina-a**.
  Está avisado no README das fixtures, há um teste que o detecta, e toda a fixture foi
  instalada por script.
- **B2 — `su-confirmed-guard` marca a linha `D-NNN` da SU como «Confirmed sem locator»**,
  porque `decisions.md#D-NNN` não é nenhuma das cinco classes de locator de `states.md`. O
  engagement real tem a mesma linha e o mesmo aviso. Fora do âmbito desta fase; fica listado.

### Integridade do engagement real

Manifesto SHA-256 de `projects/pricing-bunkers-v2` tirado **antes** de qualquer trabalho e
recomparado no fim das duas voltas:

```text
ficheiros: 76 -> 76
adicionados: []   removidos: []   alterados: []
VEREDICTO: ENGAGEMENT INTACTO
```

Nenhum comando de escrita foi corrido contra ele. O único uso do engagement real foi leitura,
para confirmar as formas dos artefactos.

## 3. O que a revisão devolveu, e o que mudou

Seis incoerências, todas aceites. Nenhuma dependia de resposta do negócio ou de IT.

### Segunda volta

| # | achado | correcção |
|---:|---|---|
| R1 | §4.4.1 exigia autoridade de âmbito quando havia materialidade `material`, e não dizia nada sobre `undetermined` nem sobre ligações vazias — materialidade desconhecida escapava | §4.4.1 passa a ter **tabela pela positiva**: dispensa **só** quando todas as unidades ligadas são `not-material` com razão; `undetermined` e ligação vazia são **impeditivos** (`COV-REVIEW-INCOMPLETE`). Fixture nova: `rec-neg-exclusion-undetermined.json` |
| R2 | os registos punham no manifesto os bytes de `decisions.md`, da SU, do `_blueprint/` e do `_render/` — acrescentar a própria aprovação, ou produzir uma versão nova, invalidaria a revisão | §6.3 ganha o **manifesto por etapa** e o campo `use` (`freshness` \| `informative`). A SU e as decisões são `informative` (comparam-se por fingerprint); `_blueprint/` e `_render/` saem do manifesto porque são **alvos**. Três testes novos cobrem-no |
| R3 | o README esperava `coverage: complete` para um registo com uma obrigação `partial` | o registo passa a chamar-se `rec-v03-blueprint-partial.json` e espera **`gaps`**. Entra a `_blueprint/ux-blueprint_v03.yaml` e o `rec-v04-blueprint-complete.json`: **cobertura completa e aprovação ausente**, que é a separação que faltava demonstrar |
| R4 | o denominador do desenho herdava as obrigações da reconciliação sem regra de correspondência: seis a montante, quatro a jusante | §4.4.4 nova define **identidade da obrigação** (`sorted(set(requirement_refs))`), fusão, exclusão herdada e pendências, e diz que a única subtracção legítima é a que `render` declara em `not_selected[]`. Todos os registos passam a carregar as seis; fixture nova: `rec-neg-obligation-dropped.json` |
| R5 | `§5.4` não existia e os fingerprints apontavam para `§6.2` estando em `§6.4`; a canonicalização não estava especificada | referências corrigidas e **§6.5 nova**: JSON canónico, NFC, chaves ordenadas, e a ordenação declarada para cada um dos três digests |
| R6 | o README remetia a regeneração dos workbooks para um relatório que não existia | o relatório existe (este), com o procedimento em §5.5, e o gerador passa a viver **na própria pasta das fixtures** |
| R7 | T39 só cobria alteração de template; a subida de `contract_version` não tinha cenário | §6.4 explicita a contrapartida de não hashear o contrato, e **T41** entra na tabela de cenários: template alterado → `stale`; contrato alterado → `unsupported` |

### Terceira volta

| # | achado | correcção |
|---:|---|---|
| R8 | a exclusão dos espelhos de aprovação estava definida para `su_fingerprint` mas **não** para `inventory_sha256`: o inventário incluía todas as linhas da SU, por isso acrescentar uma aprovação criava unidades novas, mudava o digest do inventário e invalidava a revisão que a aprovação estava a consumir — a correcção dos manifestos da §6.3 ficava a meio | §6.1 passa a tirar o **registo de uma aprovação de blueprint** do inventário **por inteiro**: fora do denominador (não gera `COV-UNREVIEWED`) e fora do `inventory_sha256` (§6.5 diz explicitamente que o digest é calculado depois de os retirar). A identificação é a mesma da §6.4 e continua positiva e estreita: só o bloco classificado `blueprint-approval` e a linha que o espelha; `D-001` e `D-002` ficam. Seis testes novos, sobre uma cópia temporária com aprovação acrescentada — **preparatórios** do T19, não o T19 (§9, limitação 10) |
| R9 | §4.4.1 permitia exclusão mecânica sem autoridade, e a regra agregada da §7 dizia que uma exclusão sem autoridade impede cobertura completa — o exemplo positivo caía nas duas regras ao mesmo tempo | §7 passa a ter tabela com as **duas** formas de autorização: a decisão explícita, e a **dispensa** quando todas as unidades ligadas são `not-material` com razão. `scope_basis_refs` vazio deixa de ser, por si só, ausência de autoridade — é a materialidade declarada que separa os casos |
| R10 | o gerador das fixtures vivia no scratchpad da sessão, e o procedimento de regeneração era só prosa | `build_fixtures.py` passa a viver com as fixtures, importável e executável. O teste usa a sua função `units()` sobre cópias temporárias, e verifica que o `inventory-expected.json` commitado **bate certo** com o que ela deriva |

As três correcções da terceira volta são mecânicas e testadas; nenhuma dependia de resposta
do negócio ou de IT.

### Quarta volta

| # | achado | correcção |
|---:|---|---|
| R11 | `build_fixtures.py` resolvia a raiz do repositório por `sys.argv[1]` **no corpo do módulo**. Importado por `unittest discover`, `sys.argv[1]` é a string `discover`, a raiz passava a ser `<cwd>/discover`, e quatro testes desta suite falhavam **consoante a forma de execução** — verdes em execução directa, vermelhos em discovery | os dois geradores resolvem a raiz por `__file__`; o argumento da linha de comandos só é lido dentro de `main()`, e serve para **validar** que aponta para o mesmo sítio (uma raiz errada falha alto em vez de escrever no lugar errado). Classe de regressão nova, `BuildersAreImportable`, com três testes: a raiz é a mesma sob quatro `sys.argv` diferentes; nenhum gerador lê `sys.argv` ao nível do módulo (lido pela **árvore sintáctica**, para um comentário sobre a regra não contar como violação dela); e a derivação do denominador dá o mesmo resultado sob discovery |
| R12 | o relatório dizia que o teste da aprovação era «a forma completa do T19»; compara conjuntos de chaves de unidades, não calcula digests nem avalia a base completa | a alegação passa a ser **teste preparatório**, na linha do achado, na docstring da classe e na lista de limitações. O T19 completo — base inteira, manifesto e os dois fingerprints, com veredicto `current` — fica declarado como trabalho da fase 2 |

Ambas são defeitos da entrega da fase 1, não do contrato, e nenhuma dependia de resposta do
negócio ou de IT.

Duas regras adicionais saíram das correcções da segunda volta, porque sem elas R1 e R3
ficavam a meio:

- **`unresolved_refs` não vazio é incompatível com `covered`** (§4.4). Senão bastava listar o
  que falta noutro campo para a mesma obrigação contar como coberta.
- **Uma pergunta em aberto não é uma obrigação** (§11, ambiguidade 17). `coverage[]` é uma
  entrada por obrigação **tratada**; a pergunta vive na SU e aparece em `unresolved_refs`. É
  por isso que uma reconciliação pode estar completa com perguntas em aberto (T37).

## 4. Decisões técnicas

Todas as ambiguidades fechadas estão na §11 do contrato (17 entradas). As que exigem
justificação estão aqui.

**D1 — A âncora de `covered` é diferente por etapa.** Em `reconciliation` o `target` é nulo e
`coverage[].targets` não é exigido, o que deixaria `covered` sem significado verificável. A
âncora passa a ser, nessa etapa, um `requirement_refs` que resolve para uma linha da SU ou
bloco de decisão existente — isto é, *a obrigação chegou a uma autoridade*. Em `blueprint`
exige-se um destino com `role: implementation`; em `render`, com `role: projection`. Um
destino com `role` `open_choice` ou `proof_obligation` **nunca** satisfaz `covered`.

**D2 — `source_review` só é exaustivo na reconciliação.** Exigir a revisão de todas as
unidades a cada versão do desenho (774 colunas, no caso real) treinaria toda a gente a
carimbar sem ler. O denominador de `blueprint` e de `render` são as **obrigações** herdadas
(D11), não as unidades. As três leituras partilham o código `COV-UNREVIEWED` porque são a
mesma falha — obrigação conhecida sem tratamento visível — e é a etapa que diz sobre que
conjunto se mede.

**D3 — A materialidade é declarada, não inferida, e desconhecê-la é impeditivo.** A fronteira
entre «excluir uma coluna mecânica tem fundamento de desenho» e «excluir um output de negócio
exige decisão de âmbito» não pode viver no kernel como regra de domínio. Resolve-se por
**forma**: cada unidade leva `materiality` com razão escrita, e a dispensa de
`scope_basis_refs` é a excepção estreita — só quando **todas** as unidades ligadas são
`not-material`. `undetermined`, ou nenhuma unidade ligada, é `COV-REVIEW-INCOMPLETE`.
Desconhecer a materialidade nunca é o mesmo que saber que a unidade não é material.

**D4 — Este contrato não entra na base por hash; os templates de pacote entram.** Hashear o
contrato inteiro faria de cada gralha uma invalidação geral, o que ensina toda a gente a
ignorar `stale`. O contrato é identificado por `contract_version`; os templates e regras de
pacote entram em `basis.authorities[]` com digest. A contrapartida está escrita: subir
`contract_version` torna os registos antigos **`unsupported`**, nunca lidos por aproximação.
São dois cenários distintos — T39 (`stale`) e T41 (`unsupported`) — e confundi-los deixaria
uma mudança de contrato passar por «basta rever».

**D5 — Do fingerprint da SU só saem as linhas que espelham aprovações de blueprint.** São
identificadas pelo **tipo do bloco** correspondente em `decisions.md`
(`classify_decisions` → `kind == "blueprint-approval"`), não pelo prefixo do id. Excluir todas
as linhas `D-*` deixaria uma mudança de decisão-solução passar sem invalidar nada.

**D6 — Exclusões da base por lista explícita, não por padrão.** `_coverage/`,
`dashboard.html`, `story.md` e os logs e ficheiros de verificação nomeados um a um. Um padrão
(«tudo o que acaba em `-log.md`») apanharia amanhã um ficheiro que é fonte.

**D7 — Índices em selectors só onde não há chave estável, e só com o `sha256` do target
preenchido.** Sem isso, uma reordenação move o índice sem mudar nada de visível.

**D8 — A fixture do F06 é sintética, e o mapa para o caso real é documental.** O plano exige
que a regressão detecte a perda «sem hardcode de `C-014`, BIOS, SharePoint ou do slug no
motor». Um engagement sintético garante isso por construção, e há um teste que verifica que
nenhum identificador do caso real entra em fixture nenhuma. A correspondência entre os dois
casos está na tabela do README das fixtures.

**D9 — Os três digests derivados levam placeholder nas fixtures.** `target.sha256`,
`basis.sources[].sha256` e `template_sha256` são digests de bytes — reais, sem escolha de
canonicalização. Os três derivados dependem da serialização que a §6.5 agora **especifica**
(JSON canónico, NFC, chaves e ordenação declaradas), mas cuja implementação é da fase 2;
congelar valores à mão agora era garantir que todas as fixtures nasciam stale no dia em que o
motor existisse. Levam `sha256("aisa-coverage-fixture-placeholder")`, e o harness das fases
2+ substitui-os pelo que o motor calcular.

**D10 — A cobertura não entra no grafo de autoridades semânticas.** `AUTHORITY_EDGES` em
`test_pp_pack_integrity.py` fica como está: a cobertura regista uma revisão **sobre**
autoridades, não é autoridade. Não escreve na Shared Understanding, não resolve perguntas,
não promove estados e não emite outcomes.

**D11 — A identidade que atravessa etapas é a obrigação, não o item.** O `id` de um item é
local ao registo. A identidade é `sorted(set(requirement_refs))`, e todas as identidades do
registo `based_on` reaparecem a jusante. Fusão escreve-se listando os `requirement_refs` das
obrigações fundidas — a cobertura da união é a prova, e não é preciso campo novo. Uma
exclusão autorizada **reaparece**, com a mesma autoridade, em vez de desaparecer. A única
subtracção legítima é a de `render`, declarada em `not_selected[]` com razão.

**D12 — O manifesto de fontes é por etapa, e cada entrada diz para que serve.** Sem isto, o
mecanismo mordia-se a si próprio de três maneiras: acrescentar a aprovação invalidaria a
revisão que a justifica; produzir a `v03` do desenho invalidaria a revisão da `v01`;
renderizar um deliverable invalidaria a revisão do desenho que ele projecta. `_blueprint/` e
`_render/` são **alvos** e entram por `target.sha256` e `based_on`.

**D13 — Um `excluded` com autoridade válida não é lacuna; sem ela, não deixa a cobertura
completa.** Estava implícito em §7 e passou a estar escrito, porque é a diferença entre
«removemos com decisão» e «removemos».

**D14 — O caso genuinamente completo precisava de uma terceira versão do desenho.** Com duas
versões, ou a fixture não tinha exemplo de cobertura completa, ou fingia que uma obrigação
`partial` não era lacuna. A `v03` fecha a escolha estrutural com `closure_basis` e desenha o
ponto de imposição; a cobertura fica completa **e a aprovação continua ausente**, que é
exactamente a separação entre as perguntas 3 e 4 do plano.

**D15 — Uma fixture negativa demonstra um código de cada vez.** A primeira versão de
`rec-neg-dead-ref.json` substituía a obrigação `{C-007}` pela referência morta, e falhava
também por obrigação perdida — um código escondia o outro. Agora a referência morta
**acrescenta-se** às seis obrigações.

**D16 — O registo de uma aprovação não é material de origem, e sai do inventário inteiro.**
Tirá-lo só do `su_fingerprint` deixava a aprovação a invalidar a revisão pela porta do
inventário: duas unidades novas, digest diferente, `stale`. A regra é a mesma da §6.4 e é
igualmente estreita — identificação **positiva** pelo tipo do bloco, e mais nenhuma linha
`D-*` sai, porque mudar a decisão-solução tem de continuar a invalidar. Vale a pena dizer o
princípio: o que entra no inventário é **material de origem**; o registo de uma decisão
humana sobre um artefacto do próprio engagement é autoridade, e lê-se à parte.

**D17 — `scope_basis_refs` vazio não é, por si só, exclusão sem autoridade.** A §4.4.1 prevê
uma dispensa, e a regra agregada tem de a reconhecer, senão o exemplo positivo de exclusão
mecânica é aceite por uma regra e recusado pela outra. O que separa os dois casos é a
materialidade declarada das unidades ligadas — e é por isso que ela é obrigatória.

**D19 — Ferramenta importável não lê os argumentos de quem a importa.** A raiz do
repositório resolve-se por `__file__`; o argumento da linha de comandos existe, mas só é lido
e validado dentro de `main()`. Um módulo que decide o seu comportamento a partir de
`sys.argv` passa a depender da forma de execução, e foi exactamente isso que pôs quatro
testes verdes em execução directa e vermelhos em discovery. A regressão está pinada por um
teste que lê a árvore sintáctica, não o texto.

**D18 — O derivador do denominador é ferramenta de fixtures publicada, não o motor.**
`build_fixtures.py` vive com as fixtures, é importável, e o teste verifica que o
`inventory-expected.json` commitado bate certo com o que ele deriva. Isto torna a expectativa
da fase 1 **executável** sem a confundir com `coverage.py`, que continua por escrever: a fase
2 reproduz o denominador com a sua própria implementação ou justifica a diferença.

## 5. As fixtures

### 5.1 O engagement `fx-coverage-f06`

Processo laboratorial inventado: registo diário de lotes, duas folhas de resumo (uma segue
por email, outra fica gravada para consulta) e um ficheiro de integração de duas colunas.
A forma é a do F06; o conteúdo não tem nada a ver com nenhum caso real.

Os artefactos de `_capture/` foram produzidos pelos **motores reais** — `xlsx_extract.py`
(L1 + L3) e `fields_draft.py` — sobre dois workbooks gerados. Isso garante que os locators de
coluna têm exactamente a forma que o runtime emite hoje
(`_capture/<workbook>.fields-draft.json#<Folha>/<Coluna>`) em vez de uma aproximação escrita
à mão.

Propriedades plantadas de propósito: dois workbooks com uma folha homónima; um grupo de três
colunas de forma repetida; uma entrada de dicionário sem dados; um ficheiro num formato fora
dos tiers de captura; uma pergunta que fica aberta (`U-010`); nenhum `_coverage/`; e os três
desenhos a usar `concretizes_decision`, que reproduz o F16.

### 5.2 A reprodução do F06, verificada por código

```text
python -B library/kernel/tools/dashboard.py --blueprint-check <fixture v01>
valid: yes (0 block, 0 warn)
exit: 0
```

E, sobre o mesmo ficheiro, nenhuma composição forçada por `C-007`, nenhum ecrã com `su_refs`
a citar `C-007`, e **uma entidade que cita `C-007`** — o destino decorativo.

É esta a asserção central do plano: *estrutura válida e requisito perdido coexistem*, e o
verificador instalado não sabe a diferença.

### 5.3 As três versões, e as cinco perguntas separadas

| versão | C-007 (a saída) | C-010 (a imposição) | estrutura | cobertura | aprovação |
|---|---|---|---|---|---|
| `v01` | só a entidade decorativa | não desenhada | válida | **gaps** | ausente |
| `v02` | publicação, consulta e campos de entrega | escolha em aberto | válida | **gaps** | ausente |
| `v03` | idem | componente no armazenamento + prova de recusa | válida | **complete** | **ausente** |

O estado que o runtime lê da fixture, para o registo:

```text
versions:                [v01 authorized valid 0 blocking, 1 structural open,
                          v02 authorized valid 0 blocking, 1 structural open,
                          v03 authorized valid 0 blocking, 0 structural open]
current.decision_ref:    ''                 # F16 reproduzido
approved:                None
latest_authorized:       v03 — not approved, awaiting business approval
synthesis architecture-story: ok
```

`v03` é o caso que ninguém consegue confundir: sem lacunas, sem escolha estrutural aberta,
sem aprovação. Nada no mecanismo pode inventar a que falta.

### 5.4 O denominador esperado

79 unidades, derivadas dos ficheiros e não de uma lista escrita à mão:

| classe | n | | classe | n |
|---|---:|---|---|---:|
| `su-row` | 18 | | `xlsx-column` | 18 |
| `enquadramento-theme` | 7 | | `answer-section` | 6 |
| `process-rule` | 6 | | `context-field` | 4 |
| `input-file` | 3 | | `phase-artefact` | 3 |
| `process-question` | 3 | | `decision-block` | 2 |
| `invariant` | 2 | | `lens-output` | 2 |
| `xlsx-sheet` | 2 | | `capture-index` | 1 |
| `xlsx-dictionary-entry` | 1 | | `replay-report` | 1 |

A fase 2 reproduz esta lista com a sua CLI `inventory`, ou justifica cada diferença no seu
relatório. É assim que o denominador fica pinado **antes** de existir código que o calcule —
que é a diferença entre especificar e racionalizar.

### 5.5 Procedimento de regeneração

Dois scripts, ambos na pasta das fixtures e ambos executáveis da raiz do repositório, **por
esta ordem**:

```bash
python .claude/tests/fixtures/coverage/build_workbooks.py .
python .claude/tests/fixtures/coverage/build_fixtures.py .
```

`build_workbooks.py` escreve `inputs/registo-de-lotes.xlsx` e
`inputs/registo-de-lotes-2024.xlsx`, corre `xlsx_extract.py` (L1 e L3) e `fields_draft.py`
sobre eles, e reescreve os artefactos de `_capture/`.

`build_fixtures.py` deriva o denominador dos **ficheiros** — é a expectativa executável da
fase 1 — e reescreve `inventory-expected.json` e os 20 registos de `records/`. Correr o
primeiro **obriga** a correr o segundo, porque os digests mudam.

Depois de regenerar, três coisas mudam por construção:

1. os `sha256` dos workbooks e dos artefactos de captura — os registos carregam-nos em
   `basis.sources[]`, e `build_fixtures.py` recalcula-os;
2. os `extracted_at` / `generated_at` dos artefactos de captura, que não são determinísticos;
3. o `_capture/_capture-log.md`, que é append-only.

**Tudo o resto da fixture é ficheiro fonte, editável à mão**, e os JSON dos registos são a
fonte de verdade: o gerador existe para os reescrever em massa, não para os substituir como
autoridade. O teste `test_coverage_fixtures.py` falha imediatamente se um `sha256` de registo
deixar de bater certo com o ficheiro que nomeia, ou se o `inventory-expected.json` divergir do
que o derivador produz — é essa a rede.

### 5.6 Os registos

20 registos, 5 positivos e 15 negativos, com o mapa completo para os cenários no README das
fixtures. Os cinco elementos do F06 que o plano exige: fonte/resposta (`answers.md#U-004` →
`C-007` + `A-003`), SU/decisão, desenho incompleto (`rec-v02-blueprint-missing.json`),
**destino decorativo** (`rec-neg-decorative-projection.json`, e a variante mal rotulada em
`rec-neg-decorative-invalid-target.json`) e desenho que cobre mesmo
(`rec-v03-blueprint-partial.json` para C-007, `rec-v04-blueprint-complete.json` para tudo).

O destino decorativo é apanhado por duas vias mecânicas distintas, de propósito: declarar
`role: projection` sobre a entidade dá `COV-MISSING-TARGET`; mentir no papel e escrever
`role: implementation` obriga a apontar para um nó que **existe**, e o componente de
publicação não existe na `v01` → `COV-INVALID-TARGET`. Nenhuma das duas prova que o código
entende semântica; provam que a existência de uma referência não substitui a avaliação.

## 6. Expectativas dos testes e a fase que os implementa

| cenário | fixture / mecanismo | fase |
|---|---|---|
| T01 requisito sem destino no desenho | `rec-v02-blueprint-missing.json`, `rec-v03-blueprint-partial.json` | 3 |
| T02 requisito citado só na entidade | `rec-neg-decorative-projection.json` | 3 |
| T03 percurso completo com fonte e revisão | `rec-v04-blueprint-complete.json` (aprovação ausente) | 3 |
| T04 resposta com obrigação ausente da SU | `rec-v01-reconciliation-complete.json` | 3 |
| T05 unidade ou obrigação sem tratamento | `rec-neg-unreviewed-unit.json` (unidade), `rec-neg-obligation-dropped.json` (obrigação entre etapas) | 3 |
| T06 fonte nova em `inputs/` após a revisão | mutação em cópia temporária | 2 |
| T07 workbook alterado com captura antiga | mutação em cópia temporária | 2 |
| T08 fonte não suportada | `rec-neg-capture-limit-as-covered.json` + `inputs/fluxo-de-libertacao.pptx` | 3 |
| T09 dois workbooks com folha homónima | no engagement; asserção sobre as chaves | 2 |
| T10 grupo de colunas com membros enumerados | `rec-v01-reconciliation-complete.json` | 3 |
| T11 `su_ref`/locator/target inexistente ou ambíguo | `rec-neg-dead-ref.json` | 3 |
| T12 campo de ecrã inexistente | `rec-neg-decorative-invalid-target.json` | 3 |
| T13 excluir requisito material sem decisão | `rec-neg-exclusion-no-decision.json`; variante de materialidade por declarar em `rec-neg-exclusion-undetermined.json` | 3 |
| T14 excluir coluna mecânica com fundamento | `rec-pos-exclusion-mechanical.json` | 3 |
| T15 `covered` que aponta só a pergunta/prova | `rec-neg-decorative-projection.json` | 3 |
| T16 `Assumed` com referência válida não sobe | SU da fixture (`A-002`, `A-003`) | 2 |
| T17 correcção de resposta substitui regra antiga | mutação em cópia temporária | 2 |
| T18 alterar logs/dashboard/markdown gerado | mutação em cópia temporária | 2 |
| T19 acrescentar aprovação legítima | acrescentar `D-003` em cópia | 2 |
| T20 mudar decisão-solução ou requisito | mutação em cópia temporária | 2 |
| T21 blueprint modificado após a revisão | `rec-neg-stale-target.json` | 2/3 |
| T22 rever uma versão e consumir outra | `rec-neg-authority-mismatch.json` | 5 |
| T23 revisão nova com lacunas e antiga completa | dois registos da mesma etapa/target | 3 |
| T24 registo ausente / JSON inválido / schema futuro | `rec-neg-schema-invalid.json`, `rec-neg-schema-future.json`, e o engagement sem `_coverage/` | 3 |
| T25 hooks não dispararam | invocação explícita das verificações | 4 |
| T26 CLI em cwd externo, caminho com espaços/acentos | execução a partir de temporário | 2 |
| T27 engagements múltiplos sem selecção | dois engagements na mesma raiz | 2 |
| T28 traversal/symlink no target | registo com `../` | 2 |
| T29 finalize concorrente | reservar a mesma versão duas vezes | 3 |
| T30 só revisão semântica pendente | `rec-neg-semantic-pending.json` | 3 |
| T31 selecção de versão por contrato de deliverable | `rec-v05-render-complete.json` | 5 |
| T32 render omite conteúdo e mantém o id em comentário | `rec-neg-render-id-in-comment.json` + `_render/..._v01.md` | 5 |
| T33 render com lacuna | registo `render` com `missing` | 5 |
| T34 caso sem UI / sem arquitectura autorizada | cópia com `authorization: not-authorized` | 5 |
| T35 legacy sem coverage com aprovação histórica | engagement + bloco de aprovação | 4 |
| T36 `concretizes_decision` normalizado | reproduzido no engagement; teste do leitor | 2 |
| T37 só perguntas/provas pendentes | `rec-v01-reconciliation-complete.json` (`U-010` aberta) | 3 |
| T38 verificação read-only repetida | correr duas vezes e comparar manifesto | 3 |
| T39 template de pacote alterado | alterar o template na cópia → **`stale`** | 5 |
| T40 relatório Markdown alterado à mão | editar o `.md` e reler o JSON | 3 |
| **T41** `contract_version` sobe por alteração semântica | registo com a versão antiga → **`unsupported`** | 3 |

**Nenhum teste novo foi deixado vermelho de propósito.** Os cenários sem motor não viraram
testes a falhar: viraram fixtures e a tabela acima. O único teste novo,
`test_coverage_fixtures.py`, está verde (63 testes) e verifica falhas observáveis — ancoragem
dos selectors, coerência do denominador, a propriedade F06, a sobrevivência das obrigações
entre etapas, os dois ciclos de invalidação que a aprovação poderia abrir (manifesto e
inventário), a regra de materialidade, a separação entre cobertura e aprovação, e a
estabilidade da importação dos geradores. Já apanhou quatro defeitos reais durante estas
voltas: ids duplicados numa fixture, uma fixture negativa que falhava por dois códigos ao
mesmo tempo, o filtro dos espelhos de aprovação que não estava a ser aplicado às duas
leituras que o precisavam, e um comentário que o primeiro scanner de `sys.argv` confundiu com
código.

## 7. Comandos e resultados

```text
python .claude/tests/fixtures/coverage/build_workbooks.py .
  -> registo-de-lotes.xlsx       4 sheets, 18 columns, sha256 a3ad78c6
  -> registo-de-lotes-2024.xlsx  2 sheets,  7 columns, sha256 3f28a101
  -> replay 0 findings; fields-draft 18 columns, 1 sem dados

python -B library/kernel/tools/dashboard.py --blueprint-check <fixture v01|v02|v03>
  valid: yes (0 block, 0 warn)   exit: 0   (as tres)

python .claude/tests/fixtures/coverage/build_fixtures.py .
  -> inventory-expected.json: 79 unidades; 20 registos reescritos

python -B .claude/tests/test_coverage_fixtures.py
  Ran 63 tests ... OK

Cinco formas de invocacao, todas verdes (R11):
  A  execucao directa, cwd na raiz                                         OK
  B  execucao directa, cwd externo ao repositorio                          OK
  C  python -m unittest discover -p "test_coverage_fixtures.py"            OK
  D  python -m unittest discover -p "test_coverage*.py"                    OK
  E  python -m unittest test_coverage_fixtures                             OK

Prova negativa: reintroduzido o `sys.argv[1]` no corpo do modulo, a suite passa a
2 falhas + 1 erro; reposto, volta a verde.
```

Suite completa (33 ficheiros, um por um, como `requirements-dev.txt` manda):

```text
31 ficheiros OK  (1484 testes)
 2 ficheiros FAIL — ambos PRÉ-EXISTENTES:

  test_options_artefact.py::test_per_option_entries_stay_short
      "pricing-bunkers-v2 O-004 entry is 226 words (budget 120)"
      Lê `projects/*/options.md`. É conteúdo do engagement real, que esta fase
      está proibida de alterar.

  test_state_scaffold.py::test_a_pre_v23_su_still_exists_untouched
      "no pre-v2.3 SU left to prove tolerance against"
      Precisa de pelo menos uma SU pré-v2.3 montada em `projects/`; o mount
      privado deste checkout só tem `pricing-bunkers-v2`, que é v2.3.
```

Ambas foram reproduzidas **com os ficheiros da fase 1 temporariamente retirados** da árvore,
e falham exactamente igual. Nenhuma das duas lê o que esta fase escreveu.

## 8. Critérios de saída

| critério do plano | estado |
|---|---|
| Esquema e exemplos coerentes | **cumprido** — 20 registos, verificados contra o contrato por 51 testes; as incoerências R1–R7 fechadas |
| Definição inequívoca do denominador | **cumprido** — `inventory-expected.json` (79 unidades) + a regra por etapa (§6.1) + a identidade da obrigação (§4.4.4) |
| Limites do julgamento semântico definidos | **cumprido** — §9 do contrato |
| Comportamento de cada etapa definido | **cumprido** — §2, §4.4.3, §4.4.4, §6.3, §8 |
| Caso F06 reproduzível documentalmente | **cumprido, e verificado por código** |
| Zero mutações nos engagements | **cumprido** — manifesto SHA-256 antes/depois idêntico, 76/76 ficheiros |
| Sem alterar comportamento de comandos, hooks ou gates | **cumprido** — nenhum ficheiro existente alterado |
| Não deixar testes novos vermelhos na suite principal | **cumprido** |

## 9. Limitações

1. **Não há motor.** Nada nesta entrega verifica cobertura de nada.
2. **Os três digests derivados são placeholders** (D9). A serialização está especificada
   (§6.5); a implementação é da fase 2, e até lá nenhuma fixture prova atualidade.
3. **O denominador esperado é uma expectativa da fase 1**, não a saída de um motor. Se a fase
   2 divergir, tem de justificar cada diferença.
4. **A compreensão semântica não é provada por código, e não passa a ser.** Um revisor que
   minta no `role` de um destino só é apanhado quando o nó não existe.
5. **O resolvedor de selectors do teste novo é mínimo** — só as formas que as fixtures usam, e
   existe para detectar apodrecimento das fixtures. Não é o resolvedor da fase 2.
6. **O derivador do denominador é a expectativa da fase 1, não uma implementação de
   referência.** `build_fixtures.py` deriva as 79 unidades dos ficheiros e o teste verifica
   que o JSON commitado bate certo com ele; mas a fase 2 escreve o seu próprio inventário e
   pode divergir com justificação. Não é um motor, não tem CLI de engagement, e não sabe
   avaliar cobertura nenhuma.
7. **Duas falhas pré-existentes na suite** (§7), nenhuma corrigida: uma exige alterar o
   engagement real, o que esta fase tem proibido; a outra exige montar outro engagement.
8. **Informação de negócio continua pendente.** Nenhuma pergunta em aberto do engagement real
   foi respondida, nenhuma aprovação foi registada, nenhum âmbito foi alterado. `U-028` e
   `U-030` continuam abertas e fora do âmbito desta passagem. As respostas que existem na
   fixture são **dados sintéticos inventados para a fixture**, não respostas de ninguém.
9. **Nada foi commitado nem publicado.** Os 56 ficheiros estão na working tree.
10. **O T19 não está provado, está preparado.** A classe
   `ApprovalDoesNotInvalidateItsOwnReview` verifica que acrescentar uma aprovação **não muda
   o conjunto de unidades** — que é a entrada do `inventory_sha256`. Não calcula digest
   nenhum, não compara a base completa e não emite veredicto de atualidade, porque não há
   motor que o faça e uma segunda implementação aqui competiria com a da fase 2. O T19
   completo — base inteira, manifesto e os dois fingerprints, com veredicto `current` — é
   trabalho da fase 2.

## 10. Dependências concretas para a fase 2

1. Ler este relatório e o README das fixtures antes de escrever código.
2. Implementar `build_inventory` contra `inventory-expected.json`: reproduzir as 79 unidades,
   ou justificar cada diferença no relatório da fase 2.
3. Implementar a canonicalização da §6.5 e trocar os placeholders no harness de teste.
4. Implementar o manifesto por etapa da §6.3 **e** a exclusão de inventário da §6.1, e
   escrever o **T19 completo**: acrescentar uma aprovação a uma cópia e verificar que a base
   inteira — manifesto, `inventory_sha256` e os dois fingerprints — dá `freshness: current`.
   O teste desta fase é preparatório e compara apenas conjuntos de unidades (§9, limitação
   10). Provar o mesmo para produzir uma versão nova do desenho e para renderizar um
   deliverable.
5. Corrigir o alias `concretizes_decision` → `decision_ref` com teste próprio (T36). A fixture
   reproduz o defeito hoje; quando a correcção entrar,
   `test_coverage_fixtures.py::test_f16_is_reproduced` **vai falhar de propósito** e tem de
   ser actualizado na mesma passagem — está escrito com essa mensagem.
6. Usar o adapter de leitores sem importar `dashboard.py` no topo de `coverage.py`.
7. Não integrar nada em `build_model`, skills ou hooks: isso é fase 4.

## 11. O que esta fase explicitamente não declara

O blueprint real **não** está aprovado, **não** está completo e **não** está validado E2E.
Nenhuma pergunta em aberto do engagement real foi respondida. Nenhuma aprovação foi registada
em nome de ninguém. A cobertura de nenhum engagement real foi avaliada, porque não existe
código que a avalie.
