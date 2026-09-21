# Coverage Contract — Kernel v0.2.0 · schema v1

> **Estado: activo nas três etapas.** Desde a fase 4 do plano de implementação
> (`docs/runtime-hardening/coverage-reconciliation-implementation-plan.md` §12) as etapas
> `reconciliation` e `blueprint` estão **ligadas ao runtime**: `/blueprint` corre a
> reconciliação antes de produzir (passo 1b) e a revisão da versão depois (passo 13b), e a
> condição de **nova** aprovação da §8.1 vale a partir daqui; `/answer` e `/capture` calculam
> o efeito na atualidade das revisões; `/status` expõe `status.coverage`; o hook
> `blueprint-validate.py` reporta a cobertura **ao lado** da estrutura, e nunca em vez dela.
> Desde a fase 5 a etapa `render` está ligada do mesmo modo: `/render` corre o **pré-render**
> por deliverable (§8.2) antes de produzir e a **revisão de projecção** depois, e a versão de
> autoridade que cada deliverable lê é verificada contra o que o seu template declara (§8.3).
>
> Ligado **não** quer dizer que o render passe a decidir: a cobertura verifica, não redefine.
> Um deliverable a que falte a sua autoridade fica *não aplicável* ou *bloqueado* — com a
> razão escrita — e isso **não** é lacuna (§8.2).
>
> Antes e depois: **ausência de registo de cobertura significa `not_evaluated`** — nunca
> "completo", nunca "reprovado", e nunca a revogação de uma aprovação já registada (§10).

## 1. O que a cobertura é, e o que nunca é

A revisão de cobertura responde a **uma** pergunta: *as obrigações que as fontes, o pedido,
os esclarecimentos, a Shared Understanding e a decisão já carregam receberam tratamento no
artefacto que se está a produzir?*

Cinco perguntas ficam **separadas** e nenhuma produz a seguinte:

| # | pergunta | quem responde |
|---:|---|---|
| 1 | A estrutura do artefacto é válida? | a verificação estrutural que já existe (`blueprint-contract.md` → *Validação estrutural*) |
| 2 | As fontes foram revistas e os requisitos materiais tratados? | `source_review` desta revisão |
| 3 | O desenho satisfaz esses requisitos? | `semantic_review` + `coverage[]` desta revisão |
| 4 | O negócio aprovou esta versão concreta? | um bloco `D-NNN` em `decisions.md` |
| 5 | As provas de conclusão E2E foram executadas e aceites? | as obrigações de prova e a sua evidência |

Um resultado positivo em 1–3 **nunca** produz 4 nem 5. `coverage: complete` lê-se
*cobertura revista*, nunca *correcção garantida por código*.

**A cobertura não é uma autoridade semântica.** Não cria facto, não resolve uma pergunta em
aberto, não promove estado epistémico, não escreve na Shared Understanding nem em
`decisions.md`, e não entra no grafo de autoridades do render. Regista uma revisão **sobre**
autoridades que já existem. Os estados epistémicos continuam a ser os cinco de
[`states.md`](states.md); os ids de cobertura são locais da revisão e **nunca** uma nova
taxonomia.

## 2. As três etapas

`stage` tem exactamente três valores:

| stage | pergunta | quando | `target` |
|---|---|---|---|
| `reconciliation` | as fontes → SU / requisitos / decisão | **antes** de desenhar | `null` |
| `blueprint` | requisitos e obrigações → versão concreta do desenho | depois de desenhar, antes de aprovar | a versão do desenho |
| `render` | autoridades que o template permite → deliverable concreto | depois de renderizar | o ficheiro renderizado |

Cada etapa produz um **registo novo** no mesmo contador `coverage_vNN`. Uma revisão anterior
nunca é editada. `based_on` liga às revisões anteriores relevantes.

`exit 0` em `reconciliation` significa *reconciliação completa, com pendências explícitas* —
não significa desenho completo, e nunca significa aprovação.

## 3. Artefactos e versionamento

- `<engagement>/_coverage/coverage_v<NN>.json` — o registo. Versionado, **imutável**, append-only.
- `<engagement>/_coverage/coverage_v<NN>.md` — projecção determinística do JSON e dos
  veredictos calculados. **Não é autoridade** e não se edita à mão: alterá-la não muda
  nada e não produz aprovação nenhuma.
- O contador `NN` é único por engagement e partilhado pelas três etapas.
- Nada em `_coverage/` entra na base de nenhuma revisão (§6.3): a cobertura não se hasheia
  a si própria.

Os vereditos **são recalculados em cada leitura**. Um `valid: true` persistido no ficheiro
não é lido como veredicto por ninguém; o JSON transporta as **conclusões do agente**, não o
resultado da verificação.

## 4. Esquema v1

### 4.1 Raiz

| campo | tipo | obrigatório | regra |
|---|---|---|---|
| `schema_version` | int | sim | `1`. Outro valor → `unsupported`, nunca interpretado por aproximação |
| `version` | `"vNN"` | sim | corresponde ao nome do ficheiro |
| `engagement` | string | sim | corresponde ao `_state.json.engagement` |
| `stage` | enum | sim | `reconciliation` · `blueprint` · `render` |
| `generated_at` | ISO-8601 | sim | quando o rascunho foi produzido |
| `based_on` | lista de `"coverage_vNN.json"` | sim (pode ser vazia) | §4.6 |
| `target` | mapa ou `null` | sim | `null` em `reconciliation`; obrigatório nas outras |
| `deliverable` | mapa | só em `render` | §4.5 |
| `basis` | mapa | sim | §4.2 |
| `source_review` | lista | sim | §4.3 |
| `coverage` | lista | sim | §4.4 |
| `semantic_review` | mapa | sim | §4.7 |

Campo desconhecido na raiz → diagnóstico (`COV-SCHEMA`, severidade `warn`), não é lido.
Campo obrigatório ausente, tipo errado, `version` que não bate com o nome do ficheiro, ou
combinação incompatível com a etapa → `contract_validity: invalid`.

**Um registo é dado, nunca código, e o tipo errado é sempre diagnóstico.** `target: "bad"`,
`based_on: [{}]`, `basis: "x"`, `unit_refs: "C-007"` — um campo com o tipo errado sai como
`COV-SCHEMA` com o nome do campo e o tipo que recebeu, `contract_validity: invalid` e
saída **2**, nunca como falha interna (`COV-UNEXPECTED`, saída 5) e nunca sem JSON. Saída 5
existe para falha do motor; um ficheiro mal escrito não é falha do motor, e tratá-lo como
tal manda o leitor procurar o problema no sítio errado. Em particular, uma **string** onde
o contrato pede uma lista não é uma lista de caracteres: é erro de forma.

### 4.2 `basis` — a base que a revisão diz ter lido

| campo | tipo | obrigatório | regra |
|---|---|---|---|
| `inventory_sha256` | 64 hex | sim | digest do inventário canónico — serialização em §6.5 |
| `su_fingerprint` | 64 hex | sim | §6.4, serialização em §6.5 |
| `decision_fingerprint` | 64 hex | sim | §6.4, serialização em §6.5 |
| `sources` | lista de `{path, sha256, role, use}` | sim | o manifesto **da etapa** (§6.3). `role ∈ {input, capture, engagement}`; `use ∈ {freshness, informative}` |
| `authorities` | lista de `{path, sha256}` | sim (pode ser vazia) | templates e regras de pacote efectivamente consumidos (§6.4). Sempre `freshness` |
| `decision_ref` | `"D-NNN"` | sim | a decisão-solução em vigor no momento da revisão |
| `contract_version` | string | sim | `"1"` — a versão **deste** contrato (§6.4) |
| `pack` | string | sim | o pacote activo |

`basis` é um **snapshot**, não um pedido. `finalize` recalcula a base actual e compara-a com
este snapshot; **nunca** substitui os valores antigos pelos actuais. Substituí-los carimbaria
como revista uma fonte que mudou sem ser relida.

### 4.3 `source_review[]` — uma entrada por unidade ou grupo declarado

**Quão exaustiva, por etapa** (§6.1): em `reconciliation` cobre **todo** o inventário —
uma unidade sem entrada é `COV-UNREVIEWED`. Em `blueprint` e `render` carrega apenas as
unidades que a etapa volta a consultar ou cujo julgamento mudou; rever outra vez
centenas de colunas a cada versão do desenho treinaria toda a gente a carimbar sem ler.
O que essas duas etapas têm de cobrir por inteiro é o **conjunto de obrigações** do
registo de `reconciliation` que `based_on` nomeia.

| campo | tipo | obrigatório | regra |
|---|---|---|---|
| `id` | string | sim | único no registo |
| `unit_refs` | lista de unit keys | sim, ≥1 | §5.2. Um grupo enumera os membros, um a um |
| `assessment` | enum | sim | `reviewed` · `unverifiable` · `not_applicable` |
| `materiality` | enum | sim | `material` · `not-material` · `undetermined` |
| `rationale` | string | sim | não vazio |
| `links` | mapa | sim | `{su_refs[], coverage_items[], obligations[]}` — listas, podem ser vazias |
| `limitation` | mapa | só se `unverifiable` | `{reason, impact, action}` — todos não vazios |

- **`reviewed` diz que a unidade foi lida, nunca que um requisito está satisfeito.** A
  satisfação vive em `coverage[].assessment` e em mais lado nenhum.
- `not_applicable` é um julgamento sobre a unidade **com razão escrita**; nunca o resultado
  de faltar extractor. Uma fonte sem extractor é `unverifiable` com `limitation`, continua
  no denominador e nunca vira `covered` por omissão (`COV-CAPTURE-LIMIT`).
- `materiality` ausente lê-se `undetermined`, **não** `not-material`: a falta de avaliação
  continua detectável.
- **`links` resolvem, ou são referências mortas.** `coverage_items` aponta para ids de
  `coverage[]` deste registo; `su_refs` e `obligations` para ids da Shared Understanding ou
  das decisões. Uma ligação para o que não existe é `COV-DEAD-REF`, como qualquer outra — e
  é a protecção que o **próprio revisor** tem contra o esvaziamento posterior do registo:
  quando as preenche, apagar um item deixa de ser silencioso.
- **Zero obrigações e material lido não podem ser verdade ao mesmo tempo.** Um registo com
  `coverage[]` vazio sobre um denominador em que alguma unidade foi declarada `material` e
  `reviewed` é uma revisão por acabar (`COV-REVIEW-INCOMPLETE`), não uma revisão que
  encontrou «nada a preservar». O motor **não** decide quais unidades geram obrigações —
  isso é do revisor (§9) — decide que as duas afirmações se contradizem.

### 4.4 `coverage[]` — uma entrada por obrigação tratada

| campo | tipo | obrigatório | regra |
|---|---|---|---|
| `id` | string | sim | único no registo |
| `requirement_refs` | lista de ids | sim, ≥1 | ids da SU / decisão / obrigações; todos têm de resolver |
| `source_unit_refs` | lista de unit keys | sim (pode ser vazia) | de onde vem a obrigação |
| `disposition` | enum | sim | `preserve` · `change` · `retire` · `clarify` |
| `scope_basis_refs` | lista de ids | sim (pode ser vazia) | §4.4.1 |
| `targets` | lista de mapas | sim (pode ser vazia) | §4.4.2 |
| `assessment` | mapa | sim | `{status, rationale, acceptance_basis_refs[]}` |
| `unresolved_refs` | lista de ids | sim (pode ser vazia) | perguntas em aberto que este item não fecha |
| `required_action` | string | sim quando `status ≠ covered` | o que falta fazer |
| `responsible_role` | string | sim quando `status ≠ covered` | papel, nunca pessoa |

`assessment.status ∈ {covered, partial, missing, excluded}`. **Campo ausente é revisão
incompleta** (`COV-REVIEW-INCOMPLETE`), nunca `missing` por defeito.

**`unresolved_refs` não vazio é incompatível com `covered`.** Um item que ainda aponta para
algo por resolver é, no máximo, `partial` — senão bastava listar o que falta noutro campo
para a mesma obrigação contar como coberta. Declarar as duas coisas ao mesmo tempo é
`COV-REVIEW-INCOMPLETE`.

`disposition` descreve **o tratamento exigido**, não o nível de evidência. O estado
epistémico vem da SU em cada leitura e não se duplica aqui.

`acceptance_basis_refs` liga ao requisito ou critério **que já existe**. O texto de revisão
pode explicar como se verifica a cobertura; **não pode inventar limiares nem políticas de
aceitação do negócio**.

#### 4.4.1 Quando a exclusão precisa de autoridade de âmbito

`scope_basis_refs` tem de estar preenchido, e resolver para uma decisão ou declaração
autorizada, quando:

- `assessment.status == "excluded"`, **ou**
- `disposition ∈ {retire, change}`

A **dispensa é a excepção estreita**, e lê-se pela positiva: só se dispensa autoridade de
âmbito quando **todas** as unidades ligadas estão declaradas `not-material`, cada uma com a
sua razão escrita. Qualquer outro caso exige `scope_basis_refs`:

| materialidade das unidades ligadas | resultado |
|---|---|
| todas `not-material`, todas com razão | dispensa; `scope_basis_refs` pode ficar vazio |
| alguma `material` | `scope_basis_refs` obrigatório → `COV-EXCLUSION-NO-DECISION` se faltar |
| alguma `undetermined` | **impeditivo**: `COV-REVIEW-INCOMPLETE`, e a exclusão não é aceite enquanto a materialidade não for declarada |
| `source_unit_refs` vazio, ou nenhuma unidade com entrada em `source_review` | lê-se como `undetermined` — **impeditivo**, pela mesma regra |

Desconhecer a materialidade nunca é o mesmo que saber que a unidade não é material.
Um item que retira uma obrigação sem que ninguém tenha dito o que ela pesa é uma revisão por
acabar, não uma exclusão fundamentada — e é por aqui que uma perda material passaria por
lacuna administrativa.

É esta a fronteira entre os dois casos que o plano separa: retirar da UI uma coluna mecânica
de cálculo pode ter fundamento de desenho; retirar o cálculo ou o resultado de negócio exige
decisão de âmbito. O motor verifica a **forma**; a classificação de materialidade é
julgamento do revisor e fica auditável.

`preserve` com `scope_basis_refs` vazio é legítimo e é o caso normal.

#### 4.4.2 `targets[]`

Cada target é um mapa `{file, selector, kind, role}`:

- `file` — caminho relativo ao engagement (ou a uma autoridade permitida, §5.3).
- `selector` — §5.1. Tem de resolver para **exactamente um** nó.
- `kind` — o tipo de nó que o selector aponta (`entity`, `screen`, `composition`, `field`,
  `record_authority`, `proof_obligation`, `open_architecture_choice`, `section`, `su_row`,
  `decision_block`). Descritivo; a resolução é que manda.
- `role` — **o que o target prova**:

| `role` | significado | conta como implementação? |
|---|---|---|
| `su_row` | a obrigação está escrita numa linha da SU | só em `reconciliation` |
| `decision` | a obrigação está escrita na decisão | só em `reconciliation` |
| `implementation` | o desenho concretiza a obrigação neste nó | só em `blueprint` |
| `projection` | o deliverable projecta a obrigação nesta secção | só em `render` |
| `open_choice` | a obrigação está ligada a uma escolha em aberto | **nunca** |
| `proof_obligation` | a obrigação está ligada a uma prova futura | **nunca** |

Um `role` **fora da sua etapa** — `projection` num registo de `blueprint`, por exemplo — não
é um código próprio: simplesmente **não conta como âncora**, e é a regra de `covered` da
§4.4.3 que o apanha (`COV-MISSING-TARGET`). Inventar um segundo código para o mesmo facto
faria dois achados de um, e o segundo esconderia o primeiro.

#### 4.4.3 O que `covered` exige, por etapa

| stage | âncora exigida para `covered` |
|---|---|
| `reconciliation` | ≥1 `requirement_refs` que resolva para uma linha da SU ou bloco de decisão existente |
| `blueprint` | ≥1 `targets[]` com `role: implementation` que resolva |
| `render` | ≥1 `targets[]` com `role: projection` que resolva |

**O destino que serve de âncora tem de estar no artefacto que a revisão diz estar a
rever.** Um `role: implementation` num registo de `blueprint` aponta para o ficheiro de
`target.file` e para mais nenhum; um `role: projection` num registo de `render`, o mesmo.
Sem isto, uma revisão da `v01` prova a sua cobertura com nós da `v03`: os locators
resolvem, porque a `v03` existe e tem-nos; o alvo confere, porque é mesmo a `v01`; e o que
está a ser dado por coberto não está na versão revista → `COV-AUTHORITY-MISMATCH`, e o
destino **não conta** como âncora. Um destino que não é âncora — uma linha da SU citada num
registo de desenho — pode viver noutro ficheiro: não é ele que prova a concretização.

Um item `covered` cujos únicos targets tenham `role: open_choice` ou `proof_obligation` →
`COV-MISSING-TARGET`. **Uma ligação a uma pergunta ou a uma prova futura não é cobertura**, e
uma declaração de risco aceite não elimina uma obrigação de negócio.

#### 4.4.4 Identidade da obrigação, e o que tem de sobreviver entre etapas

O `id` de um item (`item-001`) é **local ao registo** e não atravessa etapas. A identidade
que atravessa é a **obrigação**: o conjunto ordenado dos seus `requirement_refs`.

```text
obligation_identity := sorted(set(requirement_refs))
```

Um registo de `blueprint` ou de `render` tem de tratar **todas** as identidades de obrigação
do registo que `based_on` nomeia. Uma que desapareça é `COV-UNREVIEWED` — é exactamente
assim que um requisito se perde entre a reconciliação e o desenho sem nada gritar.

Três formas de tratamento contam, e mais nenhuma:

| forma | como se escreve | nota |
|---|---|---|
| **um para um** | um item a jusante com a mesma identidade | o caso normal |
| **fusão** | um item a jusante cujos `requirement_refs` contêm os de várias obrigações a montante | a **união** dos `requirement_refs` a jusante tem de conter a união a montante. Não é preciso campo novo: a cobertura da união é a prova |
| **exclusão herdada** | o item reaparece a jusante com a mesma disposição e os mesmos `scope_basis_refs` | uma exclusão autorizada **não** desaparece do registo seguinte: continua visível e continua a citar a autoridade que a permitiu |

Uma obrigação a montante com `status` `partial` ou disposição `clarify` **tem de reaparecer**
a jusante. Uma pendência não se fecha por mudança de etapa, e a etapa seguinte é precisamente
onde se vê se continua pendente.

Uma obrigação que desaparece é `COV-UNREVIEWED` — **revisão incompleta, não erro de
contrato**. O registo continua válido e legível, e a cobertura fica com lacunas: tratar um
requisito perdido como ficheiro inválido esconderia exactamente o achado que este mecanismo
existe para mostrar. O que **é** erro de contrato é a ligação partida: um `based_on` que
nomeia um registo inexistente ou ilegível (§4.6).

**A mesma regra vale entre versões do mesmo par (etapa, alvo), e é monótona.** Uma revisão
nova tem de tratar todas as identidades de obrigação que **qualquer** revisão anterior do
mesmo par tratou — a união de todas, não só a imediatamente anterior — um a um, por fusão,
ou reaparecendo com `disposition: retire` e a autoridade que o permite. Uma que desapareça é
`COV-UNREVIEWED`, com a revisão onde apareceu nomeada. Comparar só com a anterior deixava
**lavar** as lacunas: a `v02` que larga cinco obrigações sai com lacunas, e a `v03` que
repete a `v02` saía completa, porque «a anterior» já só tinha uma. Uma obrigação que
apareceu uma vez fica exigida até receber disposição — e a disposição, uma vez dada, tem de
ser transportada para todas as versões seguintes (a exclusão herdada reaparece). É o que
fecha o esvaziamento **parcial**: a `v02` de uma reconciliação que trata uma obrigação onde
a `v01` tratava seis não «mudou de opinião» em silêncio. Uma obrigação não desaparece;
recebe uma disposição.

A **única** subtracção legítima é a da etapa `render`: o contrato de projecção daquele
deliverable pode não seleccionar uma obrigação. Nesse caso ela é nomeada em
`deliverable.not_selected[]`, com a razão — ausência declarada, nunca ausência silenciosa.
Não existe subtracção legítima na etapa `blueprint`.

### 4.5 `deliverable` — só na etapa `render`

| campo | tipo | regra |
|---|---|---|
| `id` | string | o `template_id` do deliverable |
| `template` | caminho | o template do pacote efectivamente usado |
| `template_sha256` | 64 hex | conteúdo do template no momento da revisão |
| `authority_sources` | lista de strings | as autoridades que **esse** template declara e que esta revisão leu |
| `blueprint_version_read` | `"vNN"` ou `null` | a versão que o contrato do deliverable manda ler (§8.3) |
| `not_selected` | lista de `{requirement_refs, reason}` | as obrigações herdadas que **este** contrato de projecção não selecciona (§4.4.4). Pode ser vazia; nunca implícita |
| `applicability` | `{state, reason}` | opcional. `state ∈ {required, conditional, not_applicable, blocked}` — os **mesmos** quatro do `render-contract.md`, sem taxonomia paralela. `reason` é obrigatória sempre que o campo existe: ausência legítima é **declarada**, nunca silenciosa |

`blueprint_version_read` é verificado **duas** vezes, contra coisas diferentes, e nenhuma
substitui a outra: contra a revisão de desenho que o registo consome (`based_on`), e contra
a versão que o **template** daquele deliverable manda ler, resolvida no momento da
verificação (§8.3). Um registo coerente consigo próprio que leia a versão autorizada onde o
contrato exige a aprovada só é apanhado pela segunda.

**E antes das duas, a pergunta de que ambas dependem: o template é mesmo o deste
deliverable?** `id` e `template` são declarados pelo mesmo registo, e nada os obriga a
concordar. O template declara a sua própria identidade em `template_id`; `deliverable.id`
tem de ser igual a ela, e um template sem `template_id` não permite confirmar nada:

| caso | código |
|---|---|
| `id` ≠ `template_id` do template lido | `COV-AUTHORITY-MISMATCH` |
| template sem `template_id` | `COV-SCHEMA` |

Sem esta verificação, `deliverable.id` é decorativo: uma revisão que se diz da Implementation
Specification apoiada no template do Architecture Blueprint herda `v<latest authorized>`,
concorda consigo própria, e sai **completa sem existir versão aprovada nenhuma** — uma
especificação aceite sem aprovação, que é precisamente o que a §8.3 existe para impedir.
Confirmada a discordância, a versão de autoridade **não** é resolvida a partir do contrato
errado: o token do outro deliverable não substitui o que falta.

#### 4.5.1 Os campos declarados têm de concordar entre si

O registo descreve a mesma realidade por vários ângulos, e **cada par que ninguém concilie é
uma porta**: basta declarar os dois lados de forma coerente consigo mesma para a autoridade
se trocar sem que nada o note. A lista é fechada, e cada linha tem o seu código:

| o que se declara | tem de concordar com | código se não concordar |
|---|---|---|
| `deliverable.id` | o `template_id` do template lido | `COV-AUTHORITY-MISMATCH` |
| `deliverable.id` | o deliverable de `target.identity` (`<id>_vNN`, §4.6) | `COV-AUTHORITY-MISMATCH` |
| `deliverable.template` | uma entrada de `basis.authorities` | `COV-SCHEMA` |
| `deliverable.template` | um ficheiro legível do pacote activo | `COV-SCHEMA` |
| `deliverable.blueprint_version_read` | a versão que o template manda ler, resolvida agora (§8.3) | `COV-AUTHORITY-MISMATCH` |
| `deliverable.blueprint_version_read` | a versão da revisão de desenho consumida em `based_on` | `COV-AUTHORITY-MISMATCH` |
| um contrato que exige versão e **nenhuma** existe | uma aplicabilidade declarada (`blocked`/`not_applicable`), não um `blueprint_version_read: null` | `COV-AUTHORITY-MISMATCH` |
| `deliverable.applicability` não-produzido | a ausência de obrigações `covered` | `COV-REVIEW-INCOMPLETE` |
| `basis.pack` | o pacote activo do engagement | `COV-STALE` |

Quatro destas merecem a razão por extenso, porque são as que pareciam inofensivas:

- **`deliverable.template` fora de `basis.authorities`.** `authorities` é o que a atualidade
  recalcula e compara (§6.3). Um contrato de projecção consumido e não declarado ali pode
  mudar sem que a revisão fique *stale* por essa via. Numa revisão de `render` o template é
  sempre consumido: a lista nunca pode estar vazia.
- **Um template que não se lê é impeditivo, não um aviso.** Sem o ler, a identidade e a
  versão de autoridade ficam **ambas** por verificar — e um registo que aponte para fora do
  pacote activo passaria exactamente por essa porta. O caminho de erro é o que menos pode
  ser permissivo.
- **A autoridade que não existe não se satisfaz por omissão.** Quando o contrato do
  deliverable exige uma versão e **nenhuma** existe, um `blueprint_version_read: null`
  «concorda» com essa ausência e passaria limpo. O documento não podia ter sido produzido
  sem a sua autoridade: ou o registo declara a aplicabilidade (`blocked` / `not_applicable`,
  e então não dá obrigações por projectadas), ou é `COV-AUTHORITY-MISMATCH`.

**O que continua por conciliar, e é declarado como limite:** `deliverable.authority_sources`
é verificado na forma e no efeito que tem sobre a base de atualidade — não contra a lista que
o template declara em `authority_sources` / `conditional_sources`. Essa é prosa do contrato de
projecção, e compará-la por texto seria adivinhar. Fica por conta da passagem destino → fonte
da §9.

### 4.6 `target` e `based_on`

`target` (quando existe) é `{file, kind, identity, sha256}`:
`kind ∈ {blueprint, deliverable}`; `identity` é `vNN` para um desenho e
`<deliverable>_vNN` para um deliverable; `sha256` é o digest do ficheiro alvo.

`based_on` liga às revisões anteriores:

| stage | tem de referenciar |
|---|---|
| `reconciliation` | nada (lista vazia é o caso normal) |
| `blueprint` | ≥1 registo `reconciliation` do mesmo engagement |
| `render` | ≥1 registo `blueprint` quando existe arquitectura autorizada; caso contrário ≥1 `reconciliation` |

`based_on` só cita **versões estritamente anteriores**. As versões são imutáveis e crescem,
por isso uma cadeia que só aponta para trás não se pode fechar sobre si própria: a
auto-referência e qualquer ciclo ficam mortos por construção, sem percorrer grafo nenhum.
E não basta citar alguma coisa — tem de se citar uma revisão **da etapa** que a tabela
acima exige: uma cadeia só de desenhos nunca tocou na reconciliação.

**Uma revisão não vale mais do que aquela em que diz assentar.** A revisão citada em
`based_on` é avaliada com o mesmo motor, pelo seu próprio nome, e se ela não está
`valid` + `current` + `source_review: complete`, a de jusante **não pode** estar completa
(`COV-UNREVIEWED`, com a de montante nomeada). É o que a §8.1 já exigia — produzir uma
versão pede a reconciliação completa e actual — e sem esta verificação uma reconciliação
pobre, com zero obrigações, deixava declarar um desenho sem cobertura nenhuma como
completo: a herança de obrigações da §4.4.4 passava **por vacuidade**, porque não havia
obrigações a perder. As lacunas *encaminhadas* de montante não bloqueiam (§8.1); o que
bloqueia é montante por rever, alterado ou ilegível.

E **montante que não se consegue avaliar bloqueia da mesma maneira**, com a revisão que
falhou nomeada. Uma falha ao avaliar a revisão citada em `based_on` — um registo de
`reconciliation` que traz `target`, um leitor que rebenta — não é «nada a verificar»: é
`COV-SCHEMA` (quando é o registo de montante que está mal) ou `COV-UNEXPECTED` (quando é o
motor), sempre impeditivo, sempre com o ficheiro identificado. Uma lista de montante vazia
porque a avaliação falhou lê-se exactamente como uma lista vazia porque estava tudo bem, e
essa é a forma mais silenciosa de um falso verde (§8: falha de avaliação é «não avaliado»,
nunca sucesso silencioso).

Base, target ou `based_on` ausentes, malformados, duplicados, circulares, de etapa errada ou
incompatíveis com a etapa são **erro de contrato**, não avisos.

### 4.7 `semantic_review`

| campo | tipo | regra |
|---|---|---|
| `status` | enum | `completed` · `pending` · `not_started` |
| `performed_by` | `{kind, name}` | `kind ∈ {agent, human}`. **O autor é o executor efectivo**, nunca o sponsor inferido |
| `completed_at` | ISO-8601 | obrigatório quando `completed` |
| `method` | string | obrigatório quando `completed` |
| `passes` | `{source_to_target, target_to_source}` | ambos booleanos; ambos `true` é condição de `completed` |
| `limitations` | lista de strings | obrigatória (pode ser vazia; vazia é uma afirmação, não uma omissão) |
| `findings` | lista de ids de `coverage[]` | todo o item com `status ∈ {partial, missing, excluded}` tem de constar |

`findings` é condição de **`completed`**, não do registo: uma revisão declarada `pending`
ainda não tem os achados todos, e exigir-lhos seria acusar duas vezes a mesma pendência.

`semantic_review.completed` **não é aprovação humana nem prova de verdade**. É a declaração de
que as duas passagens da §9 foram feitas.

## 5. Locators resolvíveis

### 5.1 Gramática dos selectors

Sem JSONPath arbitrário, sem `eval`, sem expressão executada. Um selector é texto que se
resolve por travessia:

```text
selector    := segmento ( "/" segmento )*
segmento    := nome | nome "[" discriminador "]"
discriminador := chave "=" valor | inteiro
```

Formas por classe de fonte:

| classe | unit key / selector | nota |
|---|---|---|
| secção Markdown | `answers.md#U-004` | o id de domínio que já é a âncora da secção |
| secção repetida | `answers.md#U-020[2]` | ordinal explícito, 1-based. **Nunca escolher a primeira em silêncio** |
| linha da SU | `shared-understanding.md#C-007` | resolvida pelo leitor actual |
| bloco de decisão | `decisions.md#D-002` | idem |
| campo de contexto | `context.json#literal_request` | caminho pontuado, sem wildcards |
| invariante / tema | `enquadramento.md#M-1` · `enquadramento.md#T5` | |
| coluna de Excel | `_capture/<workbook>.fields-draft.json#<Folha>/<Coluna>` | **a mesma forma que `fields_draft.py` já emite** no campo `source` de cada coluna; o separador é a última `/`, porque o nome da folha pode ter espaços |
| entrada sem dados | `_capture/<workbook>.fields-draft.json#dictionary/entries_without_data/<Nome>` | |
| folha | `_capture/<workbook>.extraction.json#sheets[name=Resumo Aditivos]` | |
| regra do modelo | `_capture/process-model.md#PM-001` · `#PM-U-003` | |
| passagem de texto | `_capture/<ficheiro>.text.md#<id da passagem>` | |
| ficheiro sem extractor | `inputs/<ficheiro>` | sem `#`: a unidade é o ficheiro inteiro |
| nó do desenho | `_blueprint/ux-blueprint_v01.yaml#entities[name=ResumoAditivos]` · `#architecture/compositions[component=lote-export]` · `#screens[name=LoteListScreen]/data/primary_columns` | selecção única por `name`, `key`, `component` ou `su_ref` |
| secção do deliverable | `_render/<ficheiro>.md#A3` | a secção/slot que o template declara |

**Índices só onde não há chave estável**, e nesse caso a revisão só é válida com o `sha256`
do target preenchido: sem ele, uma reordenação move o índice sem mudar nada de visível.

Selector que não resolve → `COV-INVALID-TARGET`. Selector que resolve para mais do que um nó,
ou id que não existe → `COV-DEAD-REF`. **Nunca um fallback silencioso.**

### 5.2 Unit key

```text
unit_key := <caminho relativo POSIX> [ "#" <selector> ]
```

O caminho é relativo à raiz do engagement. A chave **deriva do caminho e do selector
estável**; o digest do conteúdo é um campo separado. A identidade da unidade **não muda
porque o conteúdo mudou** — é isso que permite dizer "esta unidade foi revista e depois
mudou" em vez de "apareceu uma unidade nova".

Duas folhas `Resumo Aditivos` em dois workbooks diferentes produzem duas chaves diferentes,
porque a chave inclui o ficheiro.

### 5.3 Caminhos e segurança

- Todo o caminho resolvido tem de ficar **dentro da raiz do engagement**, com uma excepção
  estreita: as autoridades do repositório abaixo, lidas só para leitura. A lista é
  **fechada**, não um prefixo largo:

| autoridade permitida | porquê |
|---|---|
| os contratos do kernel (`coverage-contract`, `blueprint-contract`, `render-contract`, `phases`, `states`, `orchestration`, `glossary`) | são a norma que a revisão cita |
| `library/kernel/synthesis-templates/` e `capture-templates/` | os templates que os artefactos seguem |
| `deliverable-templates/` e `architecture-templates/` **do pacote activo** | o contrato de projecção que um registo `render` consome |

  Tudo o resto é recusado, incluindo os **motores** do kernel — um motor não é autoridade
  de leitura de uma revisão — e **os outros pacotes**: um pacote que este engagement não
  usa não condiciona nada aqui. O pacote activo lê-se de `_state.json`.

- Um caminho de autoridade escreve-se **relativo à raiz do repositório**
  (`library/packs/<pack>/deliverable-templates/x.template.md`), e é aí que se resolve; um
  caminho de fonte escreve-se relativo ao engagement. Um caminho relativo tenta as duas
  leituras, **por esta ordem**: o engagement primeiro, e só quando o ficheiro lá está; a
  autoridade depois, e só se cair dentro da lista fechada acima. A segunda leitura não
  alarga a fronteira — `library/kernel/tools/` continua recusado — mas sem ela nenhuma
  autoridade seria alguma vez lida, porque `<engagement>/library/...` nunca existe.
- **Toda** a leitura passa por esta verificação, e «toda» quer dizer toda: o inventário, o
  manifesto, os dois fingerprints semânticos, os digests das autoridades e os locators. Uma
  porta só. Validar a **enumeração** dos ficheiros e depois ler as fontes principais por
  caminho directo não fecha nada — o caminho recusado volta a entrar pela outra via, e
  emitir um diagnóstico **depois** de ler não cumpre a obrigação de recusar **antes**.
- A única excepção é `_state.json`, e tem razão: é ele que declara o pacote activo, de que
  a lista de autoridades acima depende. Fazê-lo passar pela verificação completa seria
  pedir-lhe que se validasse a si próprio. Aplica-se-lhe a verificação que não depende
  dele — o caminho resolvido tem de ficar dentro da raiz do engagement — e ele nunca é
  autoridade externa, por isso não perde nada.
- Um caminho recusado é um **estado de leitura** (`refused`), ao lado de `absent`, `empty`
  e `unreadable`, e produz diagnóstico impeditivo. Não é uma excepção que se engole nem um
  ficheiro que simplesmente não aparece.
- A verificação faz-se sobre o caminho **realmente resolvido**, com symlinks e junções
  seguidos. Traversal (`..`), ligação para fora, caminho absoluto fora da raiz → recusado
  **sem ler**, e **reportado**: um ficheiro que o motor não pôde ler é um diagnóstico
  impeditivo, nunca um silêncio.
- O texto de um locator **nunca é executado**.

## 6. Inventário, atualidade e o ciclo da aprovação

### 6.1 O denominador é construído a partir das fontes, nunca do registo

O motor constrói o inventário a partir do sistema de ficheiros e dos leitores existentes.
**`coverage[]` fornecido pelo agente nunca define o denominador** — se definisse, bastaria
omitir ao mesmo tempo o requisito e a linha de revisão para obter falso verde.

Fontes obrigatórias do inventário: `context.json` · `enquadramento.md` (T1–T7, `M-n`,
conjuntos condicionais) · `answers.md` (**todas** as secções, incluindo respostas
historicamente corrigidas) · a Shared Understanding (**todas** as linhas, separando abertas
de resolvidas, sem apagar a cadeia de supersessão) · a decisão-solução em vigor (âmbito,
condições, pressupostos e riscos aceites, provas) e as anteriores de que dependa · `inputs/`
(manifesto de **todos** os ficheiros, mesmo os não suportados) · `_capture/` (extraction,
fields-draft, process-model, evidence-index, replay e limitações) · `frame.md`, `options.md`,
`premortem.md` e `lens-outputs/` como fontes auxiliares.

As fontes auxiliares **não criam verdade mais forte que a SU ou a decisão**: material que só
lá existe é um achado a reconciliar, não um requisito confirmado.

**O registo de uma aprovação de blueprint não é uma unidade de inventário.** Uma aprovação
escreve um bloco `D-NNN` em `decisions.md` e a linha que o espelha na Shared Understanding;
nenhum dos dois é material de origem — são o **registo de uma decisão humana sobre uma versão
do desenho**, e §6.4 lê-os à parte, como autoridade. Por isso ficam fora do inventário
**por inteiro**: fora do denominador (não geram `COV-UNREVIEWED` por não terem revisão) e
fora do `inventory_sha256` (não tornam stale a revisão que a aprovação está a consumir).

A identificação é a mesma da §6.4, e é positiva: o bloco cujo tipo o leitor de decisões
classifica como `blueprint-approval`, e a linha da SU cujo id é o desse bloco. **Nenhuma
outra linha `D-*` sai** — mudar a decisão-solução tem de invalidar, e sai do inventário
exactamente o que a aprovação acrescenta, nem mais um id.

Sem esta regra, a correcção dos manifestos da §6.3 ficaria a meio: os bytes de `decisions.md`
e da SU deixariam de ser comparados, e a mesma aprovação voltaria a invalidar a revisão pela
porta do lado — uma unidade nova no inventário, um digest de inventário diferente, `stale`.

**O denominador de cada etapa**, e o que `COV-UNREVIEWED` mede em cada uma:

| stage | denominador | unidade/obrigação sem tratamento |
|---|---|---|
| `reconciliation` | **todas** as unidades do inventário | `COV-UNREVIEWED` |
| `blueprint` | as obrigações de `coverage[]` do registo `reconciliation` que `based_on` nomeia | `COV-UNREVIEWED` |
| `render` | as obrigações que o contrato **daquele** deliverable selecciona | `COV-UNREVIEWED` |

As três leituras usam o mesmo código porque são a mesma falha — uma obrigação conhecida
sem tratamento visível — e é a etapa que diz sobre que conjunto se mede. Um deliverable
não é obrigado a carregar todos os requisitos: o denominador de `render` é o que o seu
próprio contrato de projecção selecciona, e a ausência legítima é *not applicable*.

### 6.2 Granularidade

- **Excel**: todas as folhas e colunas do inventário, aliases, entradas de dicionário sem
  dados, e as limitações de replay/macros/externos. Colunas repetidas podem ser **agrupadas
  explicitamente**, com os membros enumerados no snapshot — um membro omitido é detectado.
  Nunca uma pergunta por célula ou por fórmula.
- **Texto**: a unidade é o **documento normalizado** que a captura produziu
  (`_capture/<ficheiro>.text.md`), uma por documento — não uma por passagem. Uma gravação
  de reunião com 620 excertos daria 620 unidades, que é a versão textual de «uma pergunta
  por célula» e cai na mesma proibição do ponto anterior. As **passagens continuam
  citáveis**: `_capture/<ficheiro>.text.md#HH:MM:SS` resolve (§5.1), e é assim que uma
  revisão aponta para onde leu. Um locator resolúvel e uma unidade do denominador são
  coisas diferentes. Se uma passagem contém três obrigações, separá-las é do agente; o
  motor não afirma tê-las descoberto.
- **Ficheiro bruto e documento normalizado são unidades distintas.** `inputs/<ficheiro>` e
  `_capture/<ficheiro>.text.md` entram os dois: o primeiro é a fonte autoritativa em caso
  de conflito, o segundo é a superfície que as lentes leem. Inventariar só um deixaria o
  outro por rever sem ninguém dar por isso.
- **Ficheiro sem extractor**: `unverifiable` com motivo, impacto e acção. Não desaparece do
  denominador e não é `not_applicable` por falta de suporte.
- **`inputs/` percorre-se recursivamente**, e o caminho relativo inteiro faz parte da
  identidade da unidade: `inputs/extra/pedido.txt` não é `inputs/pedido.txt`. Um ficheiro
  numa subpasta que entrasse no manifesto e não no inventário seria a pior assimetria
  possível — o digest mudava e o denominador não.
- **Ausente, vazio e ilegível são três estados distintos, e nenhum colapsa no outro.**
  Ausente é ausente. Vazio é evidência de ausência de conteúdo, e é **visível** como
  diagnóstico. Ilegível — existe e não se lê, por I/O ou por codificação — é um
  **diagnóstico impeditivo**: as suas unidades ficaram fora do denominador, e uma revisão
  sobre essa base não pode ser completa. Tratar um erro de leitura como ficheiro vazio faz
  uma fonte existente desaparecer sem ninguém dar por isso, que é exactamente o que este
  mecanismo existe para impedir.
- O inventário declara se está **completo**. Um denominador incompleto não é um
  denominador, e quem o consome tem de o saber sem reler a lista de diagnósticos.
- As contagens apresentam-se **por tipo e por etapa**. Não se anuncia "100% dos requisitos
  cobertos" porque centenas de colunas receberam disposição.

### 6.3 Atualidade

- Digest SHA-256 sobre os **bytes** dos inputs e dos artefactos de conteúdo. Política
  conservadora nesta primeira entrega: uma mudança de formatação pode obrigar a rever, desde
  que o motivo seja mostrado.
- O manifesto inclui o **conjunto de ficheiros**, não só os digests dos conhecidos: adicionar
  ou remover um ficheiro é detectado.

**O manifesto é por etapa, e cada entrada declara para que serve.** `use: freshness` entra na
comparação de atualidade; `use: informative` fica registado e **nunca** é comparado. Sem esta
separação, acrescentar a própria aprovação, ou produzir um deliverable, invalidaria a revisão
no instante seguinte — que é o ciclo que a §6.4 existe para cortar.

| caminho | `reconciliation` | `blueprint` | `render` |
|---|---|---|---|
| `inputs/**` | `freshness` | `freshness` | `freshness` |
| `_capture/**` (menos o log) | `freshness` | `freshness` | `freshness` |
| `context.json`, `enquadramento.md`, `answers.md` | `freshness` | `freshness` | `freshness` |
| `frame.md`, `options.md`, `premortem.md`, `lens-outputs/**` | `freshness` | `freshness` | `freshness` |
| `shared-understanding.md` | `informative` | `informative` | `informative` |
| `decisions.md` | `informative` | `informative` | `informative` |
| `_blueprint/**` | **fora do manifesto** | **fora** — a versão alvo entra por `target.sha256` | **fora** — entra por `based_on` + `deliverable.blueprint_version_read` |
| `_synthesis/**` | fora | fora | `freshness`, só as que o template declara em `authority_sources` |
| `_render/**` | **fora do manifesto** | **fora do manifesto** | **fora** — o alvo entra por `target.sha256` |

Os dois ficheiros `informative` são comparados, sim — mas pelos **fingerprints semânticos** da
§6.4, nunca pelos bytes. Estão no manifesto para a auditoria poder ver que digest tinham, não
para a atualidade os ler.

`_blueprint/**` e `_render/**` ficam fora por uma razão mecânica: são **alvos**, não fontes.
Se estivessem no manifesto, produzir a `v03` do desenho invalidaria a revisão da `v01`, e
renderizar um deliverable invalidaria a revisão do desenho que ele projecta. A ligação a um
alvo faz-se por `target`, e a ligação entre etapas por `based_on`.
- **Excluídos da base**, por serem histórico ou derivados: `_coverage/`, `dashboard.html`,
  `story.md`, e os logs e ficheiros de verificação — `council-log.md`, `gate-log.md`,
  `_capture/_capture-log.md`, `_blueprint/blueprint-log.md`, `_render/render-log.md`,
  `_render/render-gaps.md`, `_synthesis/_synthesis-checks.md` — além de temporários
  (`*.tmp`, `*.bak`, `__pycache__/`). A lista é **explícita**, não um palpite por padrão.
  Lê-los para auditoria não os transforma em dependência autorreferencial, e **escrever num
  log ou regenerar o dashboard nunca torna uma cobertura stale**.

### 6.4 Fingerprints semânticos: a aprovação não pode invalidar a própria revisão

Aprovar acrescenta um bloco a `decisions.md` e uma linha `D-nnn` à SU. Um digest dos bytes
desses dois ficheiros invalidaria a revisão no instante em que ela é usada. Por isso estes
dois ficheiros entram na base por **fingerprint semântico**, calculado com os leitores que já
existem:

**`decision_fingerprint`** — depende do bloco da **decisão-solução em vigor** efectivamente
seleccionado (o leitor de decisões já distingue superseded de live), da sua identidade e do
seu estado de supersessão. Os blocos de **aprovação de blueprint** ficam de fora: são lidos à
parte, como autoridade humana.

**`su_fingerprint`** — depende, por cada linha de conhecimento, de: id, secção/estado, claim,
evidência/base, validade, `verificado_em` e estado de resolução; ordenado por (estado, id).
Fica de fora **apenas** o que o leitor consegue classificar positivamente como espelho de uma
aprovação de blueprint: uma linha `D-NNN` cujo bloco em `decisions.md` é do tipo
`blueprint-approval`. **Não se excluem todas as linhas `D-*`** — mudar a decisão-solução tem
de invalidar. Os cabeçalhos derivados (última actualização, saúde epistémica) não entram.
Conteúdo que o leitor não reconheça gera diagnóstico e entra na base por conservadorismo; não
é descartado em silêncio.

Consequências, todas testáveis: acrescentar uma aprovação legítima **não** invalida a revisão
dessa versão; mudar um requisito, uma fonte, a decisão-solução ou a versão alvo **invalida**,
mesmo que o id seja o mesmo. Uma aprovação de **outra** versão não torna esta revisão
aplicável a essa outra.

**Nada no desenho referencia o hash do relatório de cobertura.** A ligação ao target vive no
sidecar de cobertura; a aprovação pode citar a revisão sem fazer parte do conteúdo que ela
hasheia.

**Autoridades de pacote e a versão deste contrato.** Os templates e regras de pacote que uma
revisão declara ter consumido entram em `basis.authorities[]` com digest: mudá-los torna a
revisão correspondente stale. O digest de uma autoridade na base **actual** é sempre
**recalculado a partir do ficheiro** — o que o registo declara é histórico, e copiá-lo para
o lado actual faria a base transportar evidência antiga e uma alteração de template passar
despercebida por essa via. Uma autoridade declarada que não existe, ou que a fronteira
recusa, é diagnóstico impeditivo, nunca um digest vazio em silêncio. **Este contrato do kernel não é hasheado**; é identificado pelo
`contract_version` que o registo declara. Uma alteração que mude o significado do contrato
sobe esse número — e invalida por construção, porque o motor deixa de reconhecer a versão
antiga como a que verifica; uma correcção editorial não sobe nada. Hashear o ficheiro inteiro
faria de cada gralha uma invalidação geral, o que treinaria toda a gente a ignorar `stale`.

A contrapartida de não hashear é que a subida de `contract_version` **tem** de invalidar, e de
forma visível: um registo que declare uma versão que o motor já não implementa é
`contract_validity: unsupported` — nunca lido por aproximação, nunca tratado como válido por
ser o mais recente que existe. Quem subir este número no mesmo incremento actualiza o motor,
as fixtures e a evidência; quem só corrigir texto não lhe toca. Esta é a razão de o plano de testes
precisar de dois cenários e não de um: alterar um template torna a revisão `stale`
(T39); alterar o significado deste contrato torna-a `unsupported` (T41).

### 6.5 Canonicalização dos digests derivados

Os três digests derivados têm de ser reproduzíveis por qualquer implementação. A
serialização é **JSON canónico**, definido aqui e em mais lado nenhum:

- codificação UTF-8, sem BOM;
- chaves de objecto por ordem lexicográfica de code point;
- sem espaço insignificante: separadores `","` e `":"`;
- sem escapes não-ASCII (`ensure_ascii: false`), quebras de linha só `\n`;
- **toda a string** passa por: normalização Unicode **NFC** → sequências de espaço branco
  colapsadas num único espaço → `strip()`. Um valor ausente serializa como `""`, nunca
  `null`, para que "campo vazio" e "campo ausente" não produzam digests diferentes por
  acidente de leitura.

Sobre essa serialização, `sha256` do texto em UTF-8:

**`inventory_sha256`** — array de `{"unit_key", "class", "sha256"}`, **ordenado por
`unit_key`** (ordem de code point), sobre as unidades do inventário **depois** de retirados
os registos de aprovação de blueprint (§6.1). `sha256` é o digest do conteúdo da unidade quando a
unidade é um ficheiro inteiro, e o digest do conteúdo do nó seleccionado quando não é. Duas
unidades nunca partilham `unit_key` (§5.2), por isso a ordenação é total.

**`su_fingerprint`** — array de `{"id", "state", "claim", "support", "extra", "criticidade",
"verificado_em", "validade", "resolved", "retired"}`, um por linha de conhecimento,
**ordenado por `(state, id)`**. `resolved` e `retired` são booleanos. Ficam de fora as linhas
que espelham aprovações de blueprint (§6.4) e os cabeçalhos derivados do ficheiro.

**`decision_fingerprint`** — objecto `{"id", "supersedes", "superseded_by", "block"}` da
decisão-solução **em vigor**, onde `block` é o texto do bloco com cada linha `rstrip`-ada,
juntas por `\n`, e depois normalizado como qualquer string acima.

Uma implementação que precise de mudar esta serialização está a mudar o significado do
contrato: sobe `contract_version`.

### 6.6 Selecção de revisão e concorrência

- A revisão aplicável a uma acção selecciona-se por **etapa + identidade do target +
  ficheiro do target + autoridade exigida**, e valida-se a atualidade. *"O último coverage
  global"* não basta.
- **A identidade e o ficheiro cruzam-se nos dois sentidos.** `target.identity` tem de ser
  a identidade que o próprio `target.file` dá (§4.6), e o `target.file` do registo tem de
  ser o ficheiro que a acção está a pedir. Cruzar só a identidade deixa passar a troca de
  uma etiqueta: uma revisão da `v03` com `identity: "v01"` escrito à mão passava por
  revisão da `v01` — o digest do alvo confere, porque o registo aponta para a `v03`; a
  identidade confere, porque foi trocada; e o ficheiro revisto não é o que se pediu. Um
  registo que diga rever uma versão e aponte para outra **não se consegue situar** (acima),
  e bloqueia em vez de ficar invisível.
- Entre revisões da mesma etapa e do mesmo target, vale **a mais recente**. Uma revisão mais
  antiga **nunca** é escolhida para esconder que a mais recente falhou.
- Sem revisão → `not_evaluated`. Schema desconhecido → `unsupported`, nunca válido. Base
  alterada → `stale`. Registo ilegível → `invalid`.
- **Situar vem antes de filtrar.** Antes de descartar um registo por «não ser desta
  etapa», tem de se saber que par (etapa, alvo) é o dele. Um registo que não se consegue
  situar — não parseia, não traz `stage`, traz uma etapa que não existe, ou é de `blueprint`
  ou `render` e não diz a que versão se aplica — **bloqueia todas as etapas**, porque
  qualquer uma delas pode ser a sua. Filtrar primeiro fá-lo desaparecer em silêncio e deixa
  a revisão anterior a valer, que é a mesma falha por outra porta.
- Situar **não é validar**: um registo que declara outra `contract_version` ou outro
  `schema_version` mas diz a que par pertence é seleccionado normalmente, e é a validação
  que o traduz para `unsupported` (§7, T41). Bloqueá-lo na selecção transformaria
  `unsupported` em `invalid`, e são coisas diferentes.
- **Um registo que não se consegue situar bloqueia todas as etapas, não só a sua.** Não se
  sabe a que etapa nem a que alvo pertence — precisamente porque não se lê — e pode ser a
  revisão mais recente do par que está a ser avaliado. Escolher a anterior porque a seguinte está
  partida é escolher a que convém: o registo que impediria o verde é exactamente aquele
  que ninguém consegue ler. Enquanto houver um em `_coverage/`, o resultado é `invalid`,
  `coverage: not_evaluated` e `eligible: false`, com os ficheiros nomeados.
- **`stale` não prova que uma conclusão ficou falsa**: obriga a rever os impactos e a produzir
  nova revisão.
- **Finalização**: rascunho em ficheiro temporário → validação e recheck dos digests →
  criação **exclusiva** do próximo `vNN`. Nunca sobrescrever, nunca `os.replace` sobre uma
  versão publicada. Se a concorrência ocupar a versão, falha com informação clara e
  repete-se a reserva.
- **O último veredicto é o que manda.** Entre qualquer verificação e a linha seguinte há
  uma janela; o que não pode haver é publicar **depois** de a ter visto fechada. O estado
  que a operação vai reportar é o mesmo que decide se ela publica: se esse estado não é
  `current` e `valid`, a reserva desfaz-se e nada fica publicado. Uma revisão publicada
  nunca sai `stale` do sítio onde foi publicada — se ficar `stale` depois, é a leitura
  seguinte que o diz, e é para isso que `stale` existe.
- O recheck **de saída** é o mesmo de entrada, e cobre o mesmo: a base **e o alvo**. O alvo
  não está no manifesto (é um alvo, §6.3), por isso uma comparação que só olhe para o
  manifesto deixa passar uma versão publicada já `stale`. Uma revisão publicada está
  actual — se não estiver, não se publica, e a reserva desfaz-se.
- A revisão publicada é avaliada **por nome**, não por «a mais recente da etapa»: com duas
  finalizações concorrentes, a mais recente é a da outra, e o relatório de uma versão
  passaria a descrever outra.
- **mtime não é prova de atualidade.** Pode optimizar leitura; o teste decisivo compara
  conteúdo.

## 7. Resultado computado

```text
contract_validity: valid | invalid | unsupported | not_evaluated
freshness:         current | stale | not_evaluated
source_review:     complete | incomplete | not_evaluated
semantic_review:   completed | pending | not_evaluated
coverage:          complete | gaps | not_evaluated
action:            produce_blueprint | approve_blueprint | complete_deliverable
eligible:          true | false
reasons:           [...]
diagnostics:       [{code, severity, file, locator, item, message, resolves}]
```

`contract_validity: not_evaluated` é o caso em que **não há registo nenhum** para a etapa e
o alvo: não há contrato de ninguém para julgar, e devolver `invalid` leria como «o registo
está mau» quando não existe registo. Um registo que existe e não se lê é `invalid` (§6.6).

Quando `contract_validity` é `unsupported`, **nada mais é interpretado**: as outras quatro
dimensões saem `not_evaluated`. `unsupported` é «não sei ler isto», não «li e falta-lhe
coisa» — reportar incompletude a partir de um schema que o motor não implementa seria
inventar uma leitura.

`coverage: complete` significa **ausência de lacunas segundo uma revisão declarada, actual e
com referências verificadas**. Nada mais.

Lacuna é `partial` ou `missing`. Um item `excluded` **autorizado pela §4.4.1** não é lacuna —
é uma remoção fundamentada, e continua visível no relatório com o que a fundamenta. A §4.4.1
prevê **duas** formas de autorização, e a regra agregada reconhece as duas:

| forma | `scope_basis_refs` | resultado |
|---|---|---|
| decisão ou declaração autorizada que suporta a remoção | preenchido e resolúvel | não é lacuna |
| **dispensa**: todas as unidades ligadas declaradas `not-material`, cada uma com razão | legitimamente **vazio** | não é lacuna |
| alguma unidade ligada `material`, sem autoridade | vazio | `COV-EXCLUSION-NO-DECISION` — a cobertura não fica completa |
| alguma unidade ligada `undetermined`, ou nenhuma unidade ligada | indiferente | `COV-REVIEW-INCOMPLETE` — a cobertura não fica completa |

`scope_basis_refs` vazio **não é**, por si só, ausência de autoridade: pode ser a dispensa da
segunda linha. É a materialidade declarada das unidades ligadas que separa os dois casos, e é
por isso que ela é obrigatória.

**`unsupported` não é `stale`, e o motor não os mistura.** `stale` diz *a base mudou,
relê*; `unsupported` diz *este motor não sabe ler este schema*. Uma revisão que declare
outra `contract_version` sai num campo próprio do resultado de atualidade, e é a validação
de registos que a traduz para `contract_validity: unsupported`. Devolver `stale` para uma
versão de contrato diferente convidaria a resolvê-la com uma releitura, que não resolve
nada.

Códigos de saída da linha de comandos:

| código | significado |
|---:|---|
| 0 | verificação executada, sem lacunas impeditivas **para a etapa** |
| — | *(o inventário isolado devolve 4 quando o denominador está incompleto: há fontes que existem e não foram lidas)* |
| 2 | argumentos ou schema inválidos — inclui `contract_validity` `invalid` **e** `unsupported`: em ambos o que falha é a leitura do registo, não a cobertura |
| 3 | engagement ou ficheiro não encontrado |
| 4 | revisão ausente, stale ou incompleta, ou lacunas que impedem a acção |
| 5 | erro inesperado |

O JSON em `stdout` mantém resultados e diagnósticos **mesmo com saída 4**. `exit 0` nunca
significa aprovação nem E2E.

## 8. Códigos e regras de passagem

Uma tabela, usada pelo motor, pela linha de comandos e por quem der feedback. **A severidade
do achado é separada da elegibilidade por acção**: produzir para discussão não é aprovar.

| código | condição | efeito |
|---|---|---|
| `COV-SCHEMA` | schema, tipo ou versionamento ilegível | verificação inválida |
| `COV-NO-REVIEW` | sem revisão para a etapa/target | não avaliado |
| `COV-STALE` | manifesto, base ou target diferente do revisto | rever antes de usar |
| `COV-UNREVIEWED` | unidade do inventário sem tratamento | reconciliação incompleta |
| `COV-DEAD-REF` | id da SU/fonte/decisão inexistente, ou locator ambíguo | corrigir a ligação |
| `COV-MISSING-TARGET` | `covered` sem âncora pertinente à etapa (§4.4.3) | cobertura não demonstrada |
| `COV-INVALID-TARGET` | campo, acção, entidade ou secção que não existe | corrigir desenho ou ligação |
| `COV-EXCLUSION-NO-DECISION` | requisito material retirado ou alterado sem autoridade de âmbito | não aceitar a exclusão |
| `COV-REVIEW-INCOMPLETE` | falta julgamento, rationale, autor ou metodologia | revisão pendente |
| `COV-KNOWN-GAP` | `partial` ou `missing` declarado | lacuna visível; a regra é por acção |
| `COV-CAPTURE-LIMIT` | fonte não verificável ou limite de captura | mostrar impacto; **nunca** transformar em coberto |
| `COV-AUTHORITY-MISMATCH` | target ou revisão usa versão/autoridade errada | bloquear o consumo correspondente |
| `COV-UNEXPECTED` | falha interna de avaliação | não avaliado; **nunca** sucesso silencioso |

### 8.1 Entrada e saída do desenho

**Antes de produzir uma versão** (`action: produce_blueprint`): reconciliação completa e
actual — toda a unidade do inventário tem tratamento e toda a perda identificada foi
encaminhada. Perguntas em aberto podem permanecer, explícitas.

«Encaminhada» tem forma verificável: a lacuna traz `required_action` e `responsible_role`
preenchidos (§4.4). E um **achado impeditivo** — referência morta, `covered` sem âncora,
obrigação perdida, revisão por acabar — bloqueia a produção tal como bloqueia a aprovação:
a lacuna encaminhada é a única forma de vermelho que deixa produzir. Um registo com
referências mortas e lacunas todas encaminhadas não é elegível para nada. Uma reconciliação com lacunas **encaminhadas** é elegível para produzir
uma versão para discussão; com uma lacuna **sem dono nem próxima acção**, não é. É esta a
diferença entre `coverage: gaps` (que se reporta) e `eligible: false` (que bloqueia) — a
severidade do achado é separada da elegibilidade por acção, e é aqui que isso se vê.

Se faltarem requisitos na SU, o executor **reconcilia primeiro**, preservando estados e
autoridade, e só depois captura novo snapshot. Não se finaliza uma cobertura antes das
alterações a montante que ela descreve.

Pode produzir-se uma versão incompleta **para discussão**, com as lacunas explícitas. Não se
inventa `draft: true` para isso: esse campo já significa candidato pré-decisão
(`blueprint-contract.md` regra 4) e o seu significado não muda.

**Depois de produzir**: verificação estrutural actual **mais** cobertura do target. Uma versão
com lacunas continua disponível para revisão; **não se anuncia pronta para aprovação**.

**Para uma nova aprovação** (`action: approve_blueprint`) exige-se, em acumulação com tudo o
que já bloqueava:

1. cobertura da etapa `blueprint` **actual** para essa versão concreta;
2. `semantic_review.status == completed`, com as duas passagens;
3. ausência de requisitos materiais `missing` ou `partial` sem disposição de âmbito autorizada;
4. os bloqueios estruturais que já existem (regra 5 do contrato de blueprint, e uma versão que
   falha a verificação estrutural continua não aprovável);
5. o pedido de aprovação explícita ao negócio, que **nenhum motor substitui**.

Isto é uma **alteração explícita ao contrato de prontidão para aprovação**, não uma descrição
do que já existia. Os contratos em conflito actualizam-se no mesmo incremento que ligar esta
regra ao runtime (fase 4 do plano). Os portões soft entre fases **não** se transformam em
bloqueios globais.

Uma prova de implementação pendente **não bloqueia automaticamente o desenho**: tem de estar
modelada e atribuída ao momento em que é exigida. *"Aprovação independente desenhada, teste
previsto antes de produção"* é diferente de *"não sabemos como impedir a auto-aprovação"*.

Se a opção ou a decisão deixarem de estar sustentadas, usa-se a revalidação e o `/revisit` que
já existem. **A cobertura não altera `D-nnn` nem emite outcome novo.**

### 8.2 Deliverables

- **Pré-render**: revisão actual das autoridades que **aquele** deliverable exige, e
  aplicabilidade dos seus slots. Não se exigem todos os requisitos em todos os documentos.
- **Pós-render**: o registo da etapa `render` liga os itens e obrigações que o contrato
  seleccionou às secções e slots do documento. Verifica-se a referência **e** o julgamento de
  preservação; se falhou, regista-se um render-gap e **não** se declara completo.
- Reutilizam-se `applicability`, `authority_sources`, `slot_sources` e `sufficiency` que já
  existem. Só se acrescenta campo ao template quando indispensável e com definição normativa.
  **Não se cria uma tabela kernel «requisito → deliverable».**
- **Um id num comentário não prova preservação semântica.** Mecanicamente: um destino
  `role: projection` cuja única linha resolvida é uma linha de comentário **não conta como
  âncora** (`COV-INVALID-TARGET`), e a regra de `covered` da §4.4.3 apanha o item. O nó
  existe — por isso não é um locator morto; o que não existe é a projecção. O resto da
  preservação continua a ser julgamento declarado, não contagem de palavras (§9).
- O render **nunca** reabre o Excel para preencher um campo em falta: devolve a lacuna ao dono
  a montante e não altera factos, decisões, âmbito, epistémica nem prova.
- Um caso sem arquitectura autorizada não fica retido só por não haver cobertura de desenho:
  aplica-se a revisão de reconciliação e de projecção às fontes que o contrato usa, e a
  ausência legítima é **not applicable**, não lacuna.

### 8.3 Versão de autoridade por deliverable

A selecção de versão continua a ser a que o contrato de render já define: o Architecture
Blueprint lê a **última autorizada** e declara o estado de aprovação; a Implementation
Specification e o Claude Design Brief lêem a **aprovada**. A cobertura **verifica** que a
revisão consumida corresponde a essa versão; usar a revisão de `v01` para consumir `v02` →
`COV-AUTHORITY-MISMATCH`.

**Onde está escrito.** No campo `blueprint_version_read` do frontmatter do template daquele
deliverable — é o template que declara, e o motor que traduz e verifica. **De qual
deliverable é aquele template** lê-se no `template_id` do mesmo frontmatter, e é a §4.5 que
obriga os dois a concordar: a autoridade de versão só vale depois de se saber de quem é o
contrato que a declara. Três tokens, e mais nenhum:

| token | significa |
|---|---|
| `v<latest authorized>` | a última versão não-rascunho com autorização de arquitectura para pelo menos um âmbito |
| `v<approved>` | a versão que um `D-NNN` de aprovação nomeia |
| `none` | este deliverable **não lê** versão de desenho nenhuma |

O campo **ausente** não se lê como `none`: seria a leitura errada em silêncio, exactamente
no campo que decide qual a versão de autoridade. Ausente é defeito do contrato de projecção
(`COV-SCHEMA`), e quem não lê desenho declara-o.

Isto **não** é uma tabela kernel «requisito → deliverable», que a §8.2 proíbe: é a mesma
selecção de versão que o `render-contract.md` já define, lida de onde ela está escrita.

**Ausência de versão não é lacuna.** `v<approved>` sem nenhuma versão aprovada tem três
razões distintas, e o motor não as mistura: não há autorização de arquitectura nenhuma; há
autorização e o negócio ainda não aprovou; há uma escolha `structural: true` em aberto que
bloqueia a aprovação. Nos três casos o deliverable está **bloqueado**, com a razão — não em
falta.

## 9. A revisão semântica é do agente, não do código

Duas passagens explícitas, ambas obrigatórias para `completed`:

**Fonte → destino.** Pedido, invariantes, esclarecimentos, saídas e consumidores, percurso
normal, excepções, permissões e segregação, dados e cálculos, integrações, falhas e
recuperação, provas. Para cada obrigação material: qual o tratamento, e em que ponto concreto
do desenho.

**Destino → fonte.** Para cada mecanismo, regra ou acção material proposta: vem de requisito
confirmado, de pressuposto explícito, ou de decisão de desenho dentro do âmbito? É esta a
passagem que apanha invenção, ampliação de autoridade e exclusão implícita.

O agente pode concluir que uma unidade é observação sem requisito novo — tem de justificar, e
**não** deve criar centenas de perguntas artificiais. Perguntas novas continuam sujeitas às
regras de admissão que já existem (`states.md` → *Admission of a question*): insuficiência de
desenho é lacuna de execução, não pergunta ao negócio.

**O que o motor nunca faz:** contar palavras, procurar nomes, medir semelhança textual ou
tratar a existência de uma referência como prova de satisfação. O motor verifica a estrutura
da ligação; a adequação é revista e escrita pelo agente, e fica assinada por quem a fez.

## 10. Compatibilidade

- Engagement sem registos de cobertura → `not_evaluated`. Nunca "completo", nunca "reprovado
  retroactivamente".
- **Aprovações históricas não são apagadas, superseded nem reescritas** pela introdução deste
  mecanismo. Mostra-se a diferença entre *aprovação existente* e *cobertura ainda não
  verificada*.
- Execuções novas de desenho e de render seguem este contrato e criam registos. Para uma
  **nova** aprovação exige-se revisão aplicável, mesmo num engagement começado antes.
- Um render de autoridade legacy pode exigir reconciliação e revisão novas antes de ser
  declarado completo, **sem revogar** a aprovação histórica.
- Schema versionado: desconhecido **não** se interpreta por aproximação.
- **Não se acrescentam booleanos de verdade a `_state.json`.** O estado de cobertura é
  derivado dos registos e das fontes, em cada leitura.

## 11. Ambiguidades do plano resolvidas neste contrato

| # | ambiguidade | resolução |
|---:|---|---|
| 1 | O que é a âncora de `covered` quando `targets` não é exigido (reconciliation) | §4.4.3: em `reconciliation` a âncora são os `requirement_refs` resolvíveis; nas outras etapas é um target com o `role` da etapa |
| 2 | Quem decide que um requisito é "material" | §4.3: declaração explícita por unidade em `source_review[].materiality`, com razão. Ausente = `undetermined`, nunca `not-material` |
| 3 | Como distinguir a coluna mecânica do output de negócio sem regra de domínio no kernel | §4.4.1: a regra é sobre a **forma** (materialidade declarada × disposição), nunca sobre o nome do campo |
| 4 | Se este contrato entra na base por hash | §6.4: não. Entra por `contract_version`; templates e regras de pacote entram por hash |
| 5 | Que linhas `D-*` saem do fingerprint da SU | §6.4: só as que espelham aprovações de blueprint, identificadas pelo tipo do bloco em `decisions.md`. Nunca todas |
| 6 | O que fazer com `story.md` e outros derivados | §6.3: lista explícita de exclusões; derivados e logs não entram na base |
| 7 | Qual revisão vale quando há várias | §6.5: a mais recente da mesma etapa e target. Nunca uma antiga para esconder a falha da recente |
| 8 | Se `covered` pode nascer de uma pergunta em aberto ou de uma prova futura | §4.4.2 e §4.4.3: nunca. `open_choice` e `proof_obligation` não satisfazem `covered` em etapa nenhuma |
| 9 | Ordem entre reconciliar a montante e finalizar a cobertura | §8.1: primeiro as alterações a montante, depois o snapshot, depois `finalize` |
| 10 | O que é uma secção Markdown repetida | §5.1: ordinal explícito no selector; citar sem ordinal quando há mais do que uma é `COV-DEAD-REF` |
| 11 | Se `source_review` é exaustivo em todas as etapas | §4.3 e §6.1: exaustivo em `reconciliation`; nas outras duas o denominador são as obrigações herdadas, não as unidades |
| 12 | O que acontece a uma exclusão cuja materialidade ninguém declarou | §4.4.1: impeditivo (`COV-REVIEW-INCOMPLETE`). Só se dispensa autoridade quando **todas** as unidades ligadas estão declaradas não materiais, com razão |
| 13 | Se uma obrigação pode desaparecer entre etapas | §4.4.4: não. A identidade é o conjunto de `requirement_refs`; fusão é legítima, exclusão herdada reaparece, e a única subtracção é a que o contrato de um deliverable declara em `not_selected[]` |
| 14 | Que ficheiros entram na comparação de atualidade | §6.3: manifesto por etapa com `use`; a SU e as decisões são `informative` e comparam-se por fingerprint; `_blueprint/` e `_render/` são alvos e ficam fora |
| 15 | Como se serializam os digests derivados | §6.5: JSON canónico com NFC, chaves ordenadas e a ordenação declarada por digest |
| 16 | Se um item pode ser `covered` e ainda apontar para algo por resolver | §4.4: não. `unresolved_refs` não vazio limita-o a `partial` |
| 17 | Se uma pergunta em aberto é ela própria uma obrigação | §4.4: não. `coverage[]` é uma entrada por **obrigação tratada**; uma pergunta em aberto vive na SU e aparece em `unresolved_refs` dos itens que toca. Por isso uma reconciliação pode estar completa com perguntas em aberto |
| 18 | Se o registo de uma aprovação entra no inventário | §6.1: não. Sai do denominador **e** do `inventory_sha256`, pela mesma identificação positiva da §6.4. Excluí-lo só do fingerprint deixaria a aprovação a invalidar a revisão pela porta do inventário |
| 19 | Se `scope_basis_refs` vazio significa exclusão sem autoridade | §7: não necessariamente — pode ser a dispensa da §4.4.1. É a materialidade declarada que separa os dois casos |
| 20 | O que acontece a uma fonte que existe e não se lê | §6.2: diagnóstico **impeditivo**, e o inventário declara-se incompleto. Nunca tratada como vazia |
| 21 | Se `inputs/` inclui subpastas | §6.2: sim, recursivamente, e o caminho relativo inteiro é a identidade |
| 22 | Que caminhos fora do engagement são legíveis | §5.3: lista fechada — contratos e templates do kernel, e templates do **pacote activo**. Motores e outros pacotes não |
| 23 | Se uma `contract_version` diferente torna a revisão `stale` | §7: não. É `unsupported`, e sai num campo próprio |
| 24 | Que `contract_validity` tem um engagement sem registo nenhum | §7: `not_evaluated`. `invalid` é o registo que existe e não se lê; a ausência de registo não tem contrato para julgar |
| 25 | Se um `role` fora da sua etapa é um código próprio | §4.4.2: não. Não conta como âncora, e é `COV-MISSING-TARGET` que o apanha. Dois códigos para o mesmo facto escondem-se um ao outro |
| 26 | Se uma obrigação perdida entre etapas torna o registo inválido | §4.4.4: não. É `COV-UNREVIEWED` — revisão incompleta. Só a ligação partida (`based_on` que não resolve) é erro de contrato |
| 27 | Se `findings` é exigido a uma revisão semântica `pending` | §4.7: não. É condição de `completed`; exigi-lo a uma revisão em curso acusaria duas vezes a mesma pendência |
| 28 | Como se resolve o caminho de uma autoridade citada num registo | §5.3: relativo à **raiz do repositório**, depois de o engagement não o ter. A ordem é engagement → autoridade, e a fronteira não se alarga |
| 29 | Quando é que uma reconciliação com lacunas deixa produzir um desenho | §8.1: quando cada lacuna traz `required_action` e `responsible_role`. Lacuna sem dono bloqueia; lacuna encaminhada não |
| 30 | O que faz um registo ilegível às **outras** etapas | §6.6: bloqueia-as todas. Não se sabe a que etapa pertence, e pode ser a mais recente do par avaliado — escolher a anterior é escolher a que convém |
| 31 | Se o recheck de saída da finalização cobre o alvo | §6.6: sim, e é o **mesmo** recheck da entrada. O alvo não está no manifesto; uma comparação só do manifesto publica uma revisão já `stale` |
| 32 | O que se faz a um registo que parseia e não se consegue situar | §6.6: bloqueia todas as etapas. Situar vem antes de filtrar — filtrar por `stage` primeiro fá-lo desaparecer em silêncio |
| 33 | Se um schema desconhecido impede situar o registo | §6.6: não. Se traz `stage` e a identidade do alvo, é seleccionado e sai `unsupported`; situar não é validar |
| 34 | O que acontece se a base mudar entre a última verificação e o fim da operação | §6.6: a reserva desfaz-se. O veredicto que ia ser reportado é o mesmo que decide publicar |
| 35 | Se basta a identidade para escolher a revisão de um alvo | §6.6: não. Identidade **e** ficheiro, e a identidade tem de ser a que o próprio ficheiro dá. Só a identidade deixa passar a troca de uma etiqueta |
| 36 | O que faz o motor a um campo com o tipo errado | §4.1: `COV-SCHEMA` com o campo e o tipo, `invalid` e saída 2. Nunca `COV-UNEXPECTED` nem saída 5 — um ficheiro mal escrito não é falha do motor |
| 37 | Se um destino-âncora pode estar noutra versão do desenho | §4.4.2: não. Tem de estar em `target.file`, ou é `COV-AUTHORITY-MISMATCH` e não conta como âncora. Destinos que não são âncora podem viver noutro ficheiro |
| 38 | Se a revisão a montante é avaliada | §4.6: sim, com o mesmo motor. Montante por rever, alterado ou ilegível impede jusante de estar completa — senão a herança passa por vacuidade |
| 39 | Como se impedem ciclos em `based_on` | §4.6: `based_on` só cita versões estritamente anteriores. As versões são imutáveis e crescem; auto-referência e ciclos ficam mortos por construção |
| 40 | O que acontece quando a revisão de montante não se consegue avaliar | §4.6: bloqueia, com a revisão que falhou nomeada e o código da causa (`COV-SCHEMA` ou `COV-UNEXPECTED`). Engolir a falha deixava a lista de montante vazia, e vazia lê-se como «estava tudo bem» |
| 41 | Se `links` pode apontar para o que não existe | §4.3: não. É `COV-DEAD-REF` como qualquer referência morta, e é a protecção do próprio revisor contra o esvaziamento do registo |
| 42 | Se um registo pode ter zero obrigações | §4.3: só quando nenhuma unidade lida foi declarada material. Material lido e nenhuma obrigação contradizem-se; o motor não decide quais unidades geram obrigações, decide que as duas afirmações não coexistem |
| 43 | Se uma obrigação pode desaparecer entre versões do mesmo par | §4.4.4: não. Uma revisão nova trata tudo o que a anterior do mesmo par tratava — um a um, por fusão, ou com `retire` e autoridade. Fecha o esvaziamento parcial |
| 44 | Se um achado impeditivo bloqueia a produção de um desenho, ou só a aprovação | §8.1: bloqueia as duas. Só a lacuna encaminhada é um vermelho que deixa produzir |
| 45 | Com que revisões anteriores do par se compara uma revisão nova | §4.4.4: com **todas**, em união. Só com a imediatamente anterior, repetir uma revisão incompleta lavava as lacunas que ela tinha largado |

## 12. Onde os exemplos vivem

Os exemplos positivos e negativos deste contrato são ficheiros, não prosa, e estão em
`.claude/tests/fixtures/coverage/`. O engagement sintético `fx-coverage-f06` reproduz o caso
de origem: uma versão de desenho **estruturalmente válida** cujo requisito de saída não tem
percurso, e uma segunda versão que o concretiza. Ver o `README.md` dessa pasta para o mapa
completo entre fixtures, códigos e cenários de teste.

---

Ver também: [`blueprint-contract.md`](blueprint-contract.md) (produção, validação estrutural e
aprovação de versões) · [`render-contract.md`](render-contract.md) (autoridade por deliverable
e classes de lacuna) · [`phases.md`](phases.md) (as quatro fases; a cobertura integra-se na
Decision e **não** cria uma quinta) · [`states.md`](states.md) (os cinco estados, que este
contrato lê e nunca redefine) · [`orchestration.md`](orchestration.md) (*Comprehension
survival* — as classes semânticas que não se podem perder em silêncio).
