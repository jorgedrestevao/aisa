# Fixtures de cobertura — contrato `coverage-contract.md` schema v1

Fixtures da **fase 1** do plano de reconciliação e cobertura
(`docs/runtime-hardening/coverage-reconciliation-implementation-plan.md` §12). **O motor
ainda não existe**: estas fixtures são a especificação executável contra a qual as fases 2 a
6 o constroem, e o teste `test_coverage_fixtures.py` mantém-nas honestas entretanto.

## O engagement sintético `fx-coverage-f06`

Reproduz a **forma** do caso F06 — não o seu conteúdo. O domínio é laboratorial e inventado;
nada aqui descreve nenhuma organização real, e nenhum identificador do caso real aparece nas
fixtures ou no futuro motor. O mapa entre os dois é documental e vive aqui:

| caso real (`docs/review-evidence/pricing-bunkers-v2-review-2026-09-14.md`, F06) | análogo na fixture |
|---|---|
| resposta do dono: a saída fica disponível porque o ficheiro é gravado diariamente numa área partilhada | `answers.md#U-004` |
| a linha da SU que confirma o mecanismo de consulta interna | `shared-understanding.md#C-007` |
| a hipótese de consumidor externo que fica sem confirmação | `shared-understanding.md#A-003` |
| a saída que **é** distribuída por outro canal | `shared-understanding.md#C-006` |
| o ficheiro de integração de duas colunas, que **não revoga** as outras saídas | `shared-understanding.md#C-008` |
| o desenho que representa o domínio e não concretiza a entrega | `_blueprint/ux-blueprint_v01.yaml`, entidade `ResumoAditivos` |
| o verificador estrutural que devolve `valid: yes (0 block, 0 warn)` sobre esse desenho | idem — verificado pelo teste |
| o desenho que concretiza mesmo a saída | `_blueprint/ux-blueprint_v02.yaml` |
| a escolha estrutural que bloqueia aprovação enquanto não fecha | `U-009`, fechada em `C-010` e desenhada na `_blueprint/ux-blueprint_v03.yaml` |

**A propriedade central**, e a razão de a fixture existir: a v01 **passa** a verificação
estrutural do runtime com zero bloqueios e zero avisos, e mesmo assim perdeu um requisito
que a SU já carregava. Estrutura válida e cobertura são coisas diferentes.

As três versões do desenho existem para separar as cinco perguntas do plano:

| versão | C-007 (a saída) | C-010 (a imposição) | cobertura | aprovação |
|---|---|---|---|---|
| `v01` | sem percurso — só a entidade decorativa | não desenhada | **gaps** | ausente |
| `v02` | publicação, consulta e campos de entrega | escolha ainda em aberto | **gaps** | ausente |
| `v03` | idem | componente no armazenamento + prova de recusa | **complete** | **continua ausente** |

A `v03` é o caso que separa *cobertura revista* de *negócio aprovou*: não há gaps, não há
escolha estrutural aberta, e mesmo assim não existe bloco de aprovação nenhum em
`decisions.md`. Nada no mecanismo pode inventar um.

Outras propriedades plantadas de propósito:

- **F16** — os três desenhos usam `concretizes_decision: D-002`; o leitor actual devolve
  `decision_ref: ""`. A fixture reproduz o defeito; a fase 2 corrige-o com teste próprio.
- **Dois workbooks com uma folha do mesmo nome** (`Resumo Aditivos`) — as chaves de unidade
  não podem colidir.
- **Grupo de colunas de forma repetida** (`Custo_Posto_A/B/C`) com os membros enumerados, e
  uma **entrada de dicionário sem dados** (`Custo_Posto_D`).
- **Um ficheiro fora dos tiers de captura** (`fluxo-de-libertacao.pptx`, um marcador de bytes
  sem conteúdo real) — entra no denominador como `unverifiable`, nunca `not_applicable`.
- **Uma pergunta que fica aberta** (`U-010`, Med) — a reconciliação pode estar completa com
  perguntas em aberto, e é isso que uma pergunta em aberto é: não uma obrigação.
- **Nenhum `_coverage/`** no engagement: a ausência de registo tem de dar `not_evaluated`.
- **Nenhuma aprovação de blueprint registada** — e é deliberado. `decisions.md` tem a
  aprovação do enquadramento (`D-001`) e a decisão-solução (`D-002`), e mais nada. É o que
  permite demonstrar cobertura completa **sem** aprovação, e é o ponto de partida do teste
  que acrescenta uma aprovação numa cópia para provar que ela não invalida a própria revisão.
- Os artefactos de `_capture/` foram produzidos pelos **motores reais**
  (`xlsx_extract.py` L1+L3 e `fields_draft.py`), não escritos à mão, para que os locators de
  coluna tenham exactamente a forma que o runtime emite.

### Regenerar as fixtures

Dois scripts nesta pasta, os dois executáveis a partir da raiz do repositório:

```bash
python .claude/tests/fixtures/coverage/build_workbooks.py .   # os dois .xlsx + a captura real
python .claude/tests/fixtures/coverage/build_fixtures.py .    # inventory-expected.json + records/
```

`build_workbooks.py` escreve os dois workbooks e corre sobre eles os motores reais
(`xlsx_extract.py` L1+L3, `fields_draft.py`). `build_fixtures.py` deriva o denominador dos
**ficheiros** — é a expectativa executável da fase 1 — e reescreve os 20 registos. Correr o
primeiro obriga a correr o segundo, porque os digests mudam.

Tudo o resto da fixture é ficheiro fonte editável à mão, e os JSON dos registos são a fonte
de verdade: `build_fixtures.py` existe para os regenerar em massa, não para os substituir
como autoridade. O procedimento completo e o que muda em cada regeneração estão em
`docs/runtime-hardening/coverage-phase-1-report.md` §5.5.

`build_fixtures.py` **não é o motor**: `coverage.py` é da fase 2, e a fase 2 reproduz este
denominador com a sua própria implementação ou justifica a diferença no seu relatório.

> **Não editar ficheiros desta fixture com as ferramentas Write/Edit.** O engagement tem
> `_state.json`, por isso os hooks `PostToolUse` resolvem-no como engagement e escrevem-lhe
> `dashboard.html`, `council-log.md` e `_synthesis/_synthesis-checks.md` por cima. Editar por
> script, ou a partir de uma cópia temporária.

## `inventory-expected.json`

O **denominador esperado** da fase 1: 79 unidades derivadas dos ficheiros da fixture, por
classe. Não é output de motor nenhum. A fase 2 reproduz esta lista com a sua CLI `inventory`
ou justifica cada diferença no seu relatório — é assim que o denominador fica pinado antes de
existir código que o calcule.

## As seis obrigações, e o que atravessa as etapas

A identidade de uma obrigação é o conjunto dos seus `requirement_refs` (contrato §4.4.4). O
registo de reconciliação fixa seis, e **todas** reaparecem em cada registo a jusante:

| identidade | o que é | disposição |
|---|---|---|
| `{C-007}` | a saída que fica disponível para consulta | `preserve` |
| `{C-006}` | a saída que segue por email | `preserve` |
| `{C-008}` | o ficheiro de integração de duas colunas | `preserve` |
| `{C-002, C-005}` | quem regista não liberta — o invariante e o comportamento real | `preserve` (fusão de duas linhas numa obrigação) |
| `{C-010}` | onde a regra é imposta | `preserve` |
| `{C-009}` | o grupo de colunas residual | `retire` / `excluded`, com autoridade |

A etapa `render` é a única que pode subtrair, e só declarando: o registo de render nomeia
`{C-009}` em `deliverable.not_selected[]`, com a razão. `rec-neg-obligation-dropped.json`
existe para provar que uma obrigação que desaparece sem declaração é apanhada.

## Registos (`records/`)

Os registos **não** vivem dentro do engagement: `finalize` é da fase 3, e o engagement tem de
poder ser lido sem `_coverage/`. Os testes copiam o engagement para um temporário e colocam lá
o registo que querem exercitar.

| ficheiro | o que declara | resultado esperado | cenário | fase |
|---|---|---|---|---|
| `rec-v01-reconciliation-complete.json` | reconciliação com as 79 unidades tratadas (77 entradas: o grupo `Custo_Posto_*` conta como uma, com membros enumerados) | `source_review: complete`, `coverage: complete`, elegível para `produce_blueprint`, com `U-010` em aberto | T04, T10, T37 | 3 |
| `rec-v02-blueprint-missing.json` | **o F06**: `C-007` e `C-010` `missing` sobre a v01 | `coverage: gaps`, `COV-KNOWN-GAP`, não elegível para aprovação | **T01** | 3 |
| `rec-v03-blueprint-partial.json` | `C-007` coberto sobre a v02; `C-010` ainda `partial` | `coverage: gaps` — uma lacuna material conhecida impede «completo», mesmo com o requisito do F06 já entregue | **T01**, T15 | 3 |
| `rec-v04-blueprint-complete.json` | sobre a v03: as seis obrigações tratadas, nenhuma `partial` nem `missing`, a exclusão com autoridade | `coverage: complete` **e aprovação ausente** — a separação entre revisão e decisão humana | **T03** | 3 |
| `rec-v05-render-complete.json` | projecção do deliverable sobre o render que carrega tudo, com `{C-009}` em `not_selected` | `coverage: complete` para a etapa `render` | T31 | 5 |
| `rec-neg-unreviewed-unit.json` | o mesmo que o v01, menos uma coluna | `COV-UNREVIEWED` | **T05** | 3 |
| `rec-neg-obligation-dropped.json` | registo de desenho sem a obrigação `{C-008}` herdada | `COV-UNREVIEWED` sobre a obrigação, não sobre a unidade | **T05** (entre etapas) | 3 |
| `rec-neg-decorative-projection.json` | **o destino decorativo**: `covered` cujo único destino é a entidade, com `role: projection` | `COV-MISSING-TARGET` — um `su_ref` válido numa entidade não demonstra o percurso | **T02**, T15 | 3 |
| `rec-neg-decorative-invalid-target.json` | `covered` com `role: implementation` a apontar para um componente de publicação que a v01 não tem | `COV-INVALID-TARGET` | **T12** | 3 |
| `rec-neg-dead-ref.json` | requisito `C-999` inexistente, secção `answers.md#U-020` que não existe, entidade inexistente | `COV-DEAD-REF` + `COV-INVALID-TARGET`, nunca fallback silencioso | **T11** | 3 |
| `rec-neg-exclusion-no-decision.json` | retira `C-007` (unidade ligada declarada material) sem `scope_basis_refs` | `COV-EXCLUSION-NO-DECISION` | **T13** | 3 |
| `rec-neg-exclusion-undetermined.json` | retira `C-007` sem sequer ligar uma unidade — materialidade por declarar | `COV-REVIEW-INCOMPLETE`: desconhecer a materialidade não dispensa autoridade | **T13** (variante) | 3 |
| `rec-pos-exclusion-mechanical.json` | retira o grupo `Custo_Posto_*` (todas as unidades declaradas não materiais, com razão em C-009) | **aceite** — não se exige aprovação de âmbito para uma coluna mecânica | **T14** | 3 |
| `rec-neg-semantic-pending.json` | tudo resolve, `semantic_review.status: pending` | `semantic_review: pending`; referências válidas não completam a revisão | **T30** | 3 |
| `rec-neg-schema-future.json` | `schema_version: 2` | `unsupported`, nunca verde | **T24**, T41 | 3 |
| `rec-neg-schema-invalid.json` | sem `basis`, item sem `assessment` | `invalid` | **T24** | 3 |
| `rec-neg-stale-target.json` | target `v01` com o `sha256` do ficheiro da `v02` | `freshness: stale` | **T21** | 2/3 |
| `rec-neg-authority-mismatch.json` | render que declara ter lido `v01` sobre um alvo produzido da `v03` | `COV-AUTHORITY-MISMATCH` | **T22** | 5 |
| `rec-neg-capture-limit-as-covered.json` | o `.pptx` marcado `not_applicable` em vez de `unverifiable` | `COV-CAPTURE-LIMIT` — falta de extractor nunca é não-aplicabilidade | **T08** | 3 |
| `rec-neg-render-id-in-comment.json` | `covered` a apontar para a linha da publicação num render que só tem `<!-- C-007 -->` | `COV-INVALID-TARGET` — o id no comentário não é a linha | **T32** | 5 |

### O manifesto de fontes, e o que ele não pode conter

`basis.sources[]` segue o manifesto **por etapa** do contrato §6.3. Cada entrada declara
`use`:

- `freshness` — entra na comparação de atualidade;
- `informative` — fica registada e nunca é comparada. É o caso de `shared-understanding.md`
  e `decisions.md`, que se comparam pelos **fingerprints semânticos**. Sem isto, acrescentar
  a própria aprovação invalidaria a revisão no instante seguinte.

`_blueprint/**` e `_render/**` **não estão no manifesto**: são alvos, e entram por
`target.sha256` e por `based_on`. Se lá estivessem, produzir a `v03` invalidaria a revisão da
`v01`, e renderizar um deliverable invalidaria a revisão do desenho que ele projecta. Há um
teste para isso.

**A mesma aprovação tem uma segunda porta, a do inventário.** Aprovar acrescenta um bloco
`D-NNN` a `decisions.md` e a linha que o espelha na SU — duas unidades novas, um
`inventory_sha256` diferente, `stale`. Por isso o contrato §6.1 tira o **registo de uma
aprovação de blueprint** do inventário por inteiro: fora do denominador e fora do digest,
identificado positivamente pelo tipo do bloco, nunca pelo prefixo do id. `D-001` e `D-002`
continuam lá; mudar a decisão-solução continua a invalidar. A classe `ApprovalDoesNotInvalidateItsOwnReview`
do teste acrescenta uma aprovação a uma cópia temporária e verifica as duas coisas.

### Convenção dos digests

`target.sha256`, `basis.sources[].sha256` e `deliverable.template_sha256` são **digests reais**
dos ficheiros, calculados sobre os bytes: não há escolha de canonicalização nenhuma neles.

Os três digests **derivados** — `basis.inventory_sha256`, `basis.su_fingerprint` e
`basis.decision_fingerprint` — levam todos o mesmo valor de placeholder,
`b31c2af5507500ef2272d791693f3335b4be63f86ff8a781a8436d1cc253fb81`, que é
`sha256("aisa-coverage-fixture-placeholder")`. A serialização canónica desses três está
definida no contrato §6.5; o que não está congelado é a sua implementação, e por isso o
**harness de teste das fases 2+ substitui estes três valores pelo que o motor calcula** antes
de exercitar a atualidade — excepto quando o cenário é precisamente uma base alterada.

## Cenários da §13 que ainda não têm fixture aqui

Não por esquecimento: cada um precisa de mutação em tempo de teste (criar, apagar ou alterar
um ficheiro numa cópia temporária), o que é trabalho da fase que o implementa, não conteúdo
estático.

| cenário | como se exercita | fase |
|---|---|---|
| T06 fonte nova em `inputs/` depois da revisão | copiar o engagement, acrescentar um ficheiro | 2 |
| T07 workbook alterado com captura antiga | copiar, tocar no `.xlsx`, não recapturar | 2 |
| T09 dois workbooks com folha homónima | já está no engagement; a asserção é sobre as chaves do inventário | 2 |
| T16 `Assumed` com referência válida não sobe de estado | ler a SU da fixture | 2 |
| T17 correcção de resposta substitui regra antiga | acrescentar secção a `answers.md` na cópia | 2 |
| T18 alterar logs / dashboard / markdown gerado | criar `dashboard.html` e tocar nos logs da cópia | 2 |
| T19 acrescentar aprovação legítima de blueprint | acrescentar bloco `D-003` a `decisions.md` + linha na SU | 2 |
| T20 mudar decisão-solução ou requisito | editar `decisions.md` / a SU da cópia | 2 |
| T23 revisão nova com lacunas e antiga completa | colocar dois registos da mesma etapa e target | 3 |
| T25 hooks não dispararam | invocar as verificações directamente | 4 |
| T26 CLI em cwd externo, caminho com espaços e acentos | correr a CLI de um temporário | 2 |
| T27 vários engagements sem selecção | dois engagements na mesma raiz | 2 |
| T28 traversal / symlink no target | registo com `../` no caminho | 2 |
| T29 finalize concorrente | reservar a mesma versão duas vezes | 3 |
| T33 render com lacuna | registo `render` com `missing` | 5 |
| T34 caso sem UI / sem arquitectura autorizada | cópia com `authorization: not-authorized` | 5 |
| T35 legacy sem coverage e com aprovação histórica | o engagement como está, mais um bloco de aprovação | 4 |
| T36 `concretizes_decision` normalizado | já reproduzido no engagement; o teste é do leitor | 2 |
| T38 verificação read-only repetida | correr duas vezes e comparar manifesto | 3 |
| T39 template ou contrato de pacote alterado | alterar o template na cópia → `stale` | 5 |
| T40 relatório Markdown alterado à mão | editar o `.md` e reler o JSON | 3 |
| **T41** subir `contract_version` por alteração semântica do contrato | registo com a versão antiga → `unsupported`, nunca lido por aproximação | 3 |

T39 e T41 são deliberadamente **dois** cenários e não um: alterar um template de pacote torna
a revisão `stale` (a base mudou, relê-se); alterar o significado deste contrato torna-a
`unsupported` (o motor deixou de saber ler aquele schema). Confundir os dois deixaria uma
mudança de contrato passar por «basta rever».
