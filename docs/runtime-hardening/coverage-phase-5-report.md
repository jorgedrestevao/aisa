# Fase 5 — Preservação em síntese e deliverables

Data: 2026-09-15, revisto a 2026-09-16 · ramo `runtime-correction/pilot-r1-r7` · plano:
`docs/runtime-hardening/coverage-reconciliation-implementation-plan.md` §12 → *Fase 5*

> **Revisão independente de 2026-09-16.** A fase 4 foi validada no seu âmbito (45 testes;
> a falha de actualização do dashboard está corrigida). A fase 5 **não** passou: um falso
> positivo aceitava uma especificação sem aprovação quando a revisão usava o template de
> arquitectura, e os 43 testes de então não o apanhavam. Está reproduzido, corrigido,
> escrito na norma e preso por teste — §2.9. E porque um defeito raramente vem sozinho, a
> **classe** a que ele pertencia foi varrida campo a campo (§2.10): mais cinco portas
> fechadas, uma delas encontrada por um teste novo. §3.4 mede-as.

**O que esta fase entrega.** A terceira etapa da cobertura — `render` — deixa de estar
implementada-e-desligada e passa a correr onde os deliverables se produzem. Duas
verificações, em dois momentos, e nenhuma responde pela outra: **antes**, as autoridades que
*aquele* deliverable declara e a versão de desenho que o *seu template* manda ler; **depois**,
a revisão de projecção do ficheiro escrito.

**O que esta fase não entrega.** Nada sobre o engagement real. O desenho de
`pricing-bunkers-v2` **não** está aprovado, **não** está completo e **não** está validado
ponta-a-ponta; a sua cobertura **não foi avaliada**; nenhuma pergunta em aberto foi
respondida; nenhuma aprovação foi registada, e nenhuma aprovação histórica foi tocada.

---

## 1. A fase 4, confirmada

A fase 5 não avança sobre critérios de saída por cumprir, por isso a primeira coisa foi
correr o que a fase 4 declarou.

| verificação | resultado |
|---|---|
| suite completa no estado de entrada da fase 4 | 38 ficheiros, 1845 testes, **2 falhas**, ambas pré-existentes e documentadas |
| `test_coverage_phase4.py` | 45 testes, verde — e confirmado por revisão independente a 2026-09-16, incluindo a correcção da actualização do dashboard |
| `test_coverage_contract/fixtures/freshness/integration/inventory` | 354 testes, verde |
| mecanismo da fase 4 a correr (pré-condição da fase 5) | `coverage_state` devolve os cinco veredictos nas etapas `reconciliation` e `blueprint` |

As duas falhas herdadas, verificadas uma a uma e **não** causadas por este trabalho:

| ficheiro | falha | porquê não é desta frente |
|---|---|---|
| `test_options_artefact.py` | `test_per_option_entries_stay_short`: *pricing-bunkers-v2 O-004 entry is 226 words (budget 120)* | mede o comprimento de um bloco de `projects/pricing-bunkers-v2/options.md`, ficheiro que nenhuma fase desta frente tocou |
| `test_state_scaffold.py` | `test_a_pre_v23_su_still_exists_untouched`: *no pre-v2.3 SU left to prove tolerance against* | exige que exista em `projects/` uma Shared Understanding anterior à v2.3 para provar tolerância; não há nenhuma montada neste checkout. Falha de fixture ausente, não de código |

Ambas falhavam já no relatório da fase 3 (§“Regressão existente”) e no da fase 4 (§7), com o
mesmo texto. `projects/` é um ponto de montagem privado: o conteúdo que estas duas leem não
está no repositório.

**Uma correcção de fronteira, dentro do âmbito permitido.** `test_coverage_phase4.py::
test_the_coverage_contract_says_render_is_still_not_wired` afirmava o estado de ligação da
etapa `render` — que é o que esta fase muda. Uma fase não afirma o estado de ligação de
outra: o teste passou a verificar o que a **fase 4** entregou (reconciliação e desenho
ligados, passos 1b e 13b, `status.coverage`), e a afirmação sobre `render` mudou-se para
`test_coverage_phase5.py`. Com duas asserções a dizer coisas diferentes sobre o mesmo
cabeçalho, um contrato desactualizado passaria despercebido.

---

## 2. O que foi construído

### 2.1 Ficheiros

| ficheiro | alteração |
|---|---|
| `library/kernel/tools/coverage.py` | +504 linhas: conciliação dos campos declarados, identidade do contrato de projecção, autoridade de versão por deliverable, pré-render, regra do comentário, `applicability`, CLI |
| `library/kernel/coverage-contract.md` | §4.5 (`applicability`, identidade do contrato de projecção, dupla verificação da versão), §8.2 (regra do comentário, mecânica), §8.3 (os três tokens, onde estão escritos, de quem é o template, e as três razões de ausência), cabeçalho de estado |
| `library/kernel/render-contract.md` | +21: *Coverage: two checks, and neither of them renders anything*; de quem é o contrato que se lê, e onde a selecção de versão está escrita |
| `.claude/skills/aisa-render/SKILL.md` | +66: passo 2b (pré-render), passo 9b (revisão de projecção), duas regras duras novas, `_coverage/` nos inputs |
| `.claude/skills/aisa-synthesize/SKILL.md` | +11: pendências transportadas, cobertura não é autoridade nem apagador |
| `.claude/hooks/render-validate.py` | +72: `coverage_report` + `coverage_line` — a cobertura ao lado da suficiência, read-only, sem duplicar regra nenhuma |
| `.claude/commands/render.md` | +6: as duas verificações, sem repetir o algoritmo |
| `.claude/hooks/HOOKS.md` | a linha de cobertura do `render-validate.py` documentada, com o seu limite |
| `docs/ARCHITECTURE.md` | a etapa de projecção deixa de estar marcada como «não ligada»; o que ela faz e o que não faz |
| 5 templates de deliverable do pacote `pp` | `blueprint_version_read` declarado (o `solution-blueprint` já o tinha) |
| `.claude/tests/test_coverage_phase5.py` | **novo**, 61 testes |
| `docs/runtime-hardening/repro-coverage-phase5-2026-09-15.py` | **novo** — o ensaio que gera a evidência |

### 2.2 A versão de autoridade: o template declara, o motor verifica

O `render-contract.md` já dizia qual versão cada deliverable lê. Não estava em lado nenhum
que o código pudesse ler. Agora está, no frontmatter de cada template:

```yaml
blueprint_version_read: v<latest authorized>   # Architecture Blueprint
blueprint_version_read: v<approved>            # Implementation Spec · Claude Design Brief
blueprint_version_read: none                   # Discovery · Executive · Estimate
```

Três tokens, e mais nenhum. **O campo ausente não se lê como `none`** — seria a leitura
errada em silêncio, exactamente no campo que decide a autoridade. Ausente é defeito do
contrato de projecção (`COV-SCHEMA`), e quem não lê desenho declara-o.

Isto **não** é a tabela kernel «requisito → deliverable» que o plano proíbe (§9.2): é a
selecção de versão que o contrato de render já define, lida de onde ela está escrita. O
motor não contém o nome de deliverable nenhum.

### 2.3 A verificação que faltava

`blueprint_version_read` já era comparado contra a revisão de desenho que o registo consome
(`based_on`). Passa a ser comparado **também** contra a versão que o template manda ler,
resolvida no momento. São factos diferentes, e o segundo apanha o que o primeiro não vê:

> A Implementation Specification a ler a última **autorizada** (`v03`), coerente com o
> `based_on` que consome. A verificação antiga não tem nada a dizer — a revisão consumida
> *é* a do desenho `v03`. É o contrato dela que exige a **aprovada**, que não existe.
>
> ```text
> [COV-AUTHORITY-MISMATCH] o contrato deste deliverable lê `v<approved>` = nenhuma versão
>   e a revisão diz ter lido v03 (§8.3) — há versão autorizada e o negócio ainda não
>   aprovou nenhuma
> ```

É por aqui que se construía sobre uma versão que ninguém validou.

### 2.4 Ausência de versão não é lacuna, e as razões não se misturam

`v<approved>` sem versão aprovada tem **três** razões, e o motor devolve-as separadas:

| estado | significa |
|---|---|
| `no-authorization` | não existe autorização de arquitectura para âmbito nenhum |
| `not-approved` | há versão autorizada e o negócio ainda não aprovou |
| `structurally-blocked` | uma escolha `structural: true` em aberto bloqueia a aprovação |

Colapsá-las apagava a diferença entre *falta decidir* e *falta aprovar*. Nos três casos o
deliverable fica **bloqueado** ou **não aplicável**, com a razão — e isso é um *skip* em
`render-log.md`, **nunca** uma entrada em `render-gaps.md`.

### 2.5 Um id num comentário não é uma projecção

A §8.2 já o dizia em prosa. Passa a ser mecânico: um destino `role: projection` cuja única
linha resolvida é uma linha de comentário **não conta como âncora**, e a regra de `covered`
da §4.4.3 apanha o item. O nó existe — por isso não é um locator morto; o que não existe é a
projecção.

O padrão é estreito de propósito (`^\s*<!--.*?-->\s*$`): um cabeçalho `# A3` não é um
comentário, e uma linha de tabela que cita o mesmo id continua a ser uma projecção válida.
Os dois casos estão presos por teste.

### 2.6 `applicability`, declarada e nunca silenciosa

Campo opcional novo no bloco `deliverable` (§4.5): `{state, reason}`, com
`state ∈ {required, conditional, not_applicable, blocked}` — os **mesmos** quatro do
`render-contract.md`, sem taxonomia paralela. Quando o campo existe, `reason` é obrigatória:
uma ausência legítima é declarada, nunca silenciosa. Um estado inventado é `COV-SCHEMA`.

### 2.7 O pré-render

```bash
python library/kernel/tools/coverage.py check --engagement <slug> --stage render \
    --deliverable <id> [--template <rel>] [--json]
```

Antes de produzir não há alvo para apontar, e a pergunta é outra. O resultado
(`aisa.coverage.render_precheck`) traz a versão declarada, a versão resolvida e porquê, o
estado do desenho (autorizado · aprovado · escolhas estruturais em aberto), a revisão a
montante que se consegue avaliar, e os achados. **Devolve factos**; quem decide se o
deliverable se produz é a declaração do template (`activation` / `blocked_when` /
`not_applicable_when`). O motor nunca deriva aplicabilidade.

Sai `0` quando não há achados impeditivos e `4` quando há — e uma autoridade que ainda não
existe **não** é achado impeditivo.

### 2.8 O hook relata, não impõe

`render-validate.py` ganha uma linha de cobertura **ao lado** da suficiência, nunca em vez
dela, lida através do motor — sem duplicar uma única regra. E não escreve a lacuna de
cobertura em `render-gaps.md`: o dono desse achado é a revisão, registada no passo 9b do
`aisa-render`. Fail-open como antes: qualquer erro sai como *não avaliada*.

### 2.9 A correcção de 2026-09-16: de quem é o contrato que a revisão leu

O defeito, reproduzido antes de se tocar em código:

```text
id declarado no registo : implementation-spec
template que ele usa    : solution-blueprint.template.md
versão aprovada         : None

cobertura  : complete
eligible   : True
achados    : nenhum
```

**Causa.** `deliverable.id` e `deliverable.template` são declarados pelo mesmo registo e
nada os obrigava a concordar. A verificação da §2.3 lia o token do template **que o registo
aponta** — e nunca perguntava se esse template era o deste deliverable. Um registo que se
diz da Implementation Specification apoiado no template do Architecture Blueprint herdava
`v<latest authorized>`, batia certo com `v03`, e saía completo. O `id` era decorativo.

Era o pior sítio possível para um campo decorativo: o que a §8.3 separa é *autorização* de
*aprovação*, e este caminho devolvia a autoridade mais fraca a quem exige a mais forte.

**Correcção.** O template declara a sua própria identidade (`template_id`, que os seis
templates do pacote já traziam). `deliverable.id` tem de ser igual a ela:

| caso | código |
|---|---|
| `id` ≠ `template_id` do template lido | `COV-AUTHORITY-MISMATCH` |
| template sem `template_id` | `COV-SCHEMA` |

E confirmada a discordância, **nenhuma versão é resolvida a partir do contrato errado**:
devolver `v03` a partir do template de outro deliverable era o próprio defeito.

**O mesmo dever no pré-render.** `check --stage render --deliverable implementation-spec
--template <o de arquitectura>` respondia `v03 available` — mandava o executor ler uma
versão que o contrato da especificação não aceita. Fechado pela mesma regra; o resultado
passa a `not_evaluated` com o achado.

**Porque é que os 43 testes não o apanhavam.** Todos verificavam a versão declarada contra
o template declarado, e nenhum perguntava de quem era esse template. Um teste que monta o
registo pelo par coerente nunca constrói o par incoerente — e era exactamente aí que a
autoridade se trocava.

### 2.10 O varrimento da classe

O defeito não era um caso; era uma **forma**. O registo descreve a mesma realidade por
vários ângulos, e cada par que ninguém concilie é uma porta: declaram-se os dois lados de
forma coerente consigo mesma, e a autoridade troca-se sem que nada o note. Varridos todos os
pares do bloco `deliverable` e da `basis`, um a um, cada caso a partir **um** par com o
registo coerente ao lado.

| par declarado | antes | agora |
|---|---|---|
| `id` ↔ `template_id` do template | **passava** | `COV-AUTHORITY-MISMATCH` (§2.9) |
| `id` ↔ o deliverable do documento revisto | **passava** | `COV-AUTHORITY-MISMATCH` |
| `template` ↔ `basis.authorities` | **passava** | `COV-SCHEMA` |
| `template` ↔ um ficheiro legível do pacote activo | **passava** | `COV-SCHEMA` |
| versão exigida inexistente, declarada por omissão | **passava** | `COV-AUTHORITY-MISMATCH` |
| `applicability` não-produzido ↔ obrigações `covered` | **passava** | `COV-REVIEW-INCOMPLETE` |
| `basis.pack` ↔ o pacote activo | **passava** | `COV-STALE` |
| `authority_sources` incoerentes | já prendia | (via atualidade) |
| `not_selected` a duplicar ou a inventar um id | já prendia | `COV-UNREVIEWED` |
| `target.identity` que o ficheiro não produz | já prendia | `COV-SCHEMA` |

Quatro merecem a razão por extenso:

**O documento revisto é de outro deliverable.** A porta gémea da §2.9: `id` e `template`
concordam um com o outro e nenhum deles com o **alvo**. A revisão diz ser da especificação e
revê o relatório de arquitectura. A identidade do alvo é `<id>_vNN` (§4.6) e agora tem de
começar pelo `id` declarado.

**Um template que não se lê era um *aviso*.** E o aviso era o buraco: sem ler o template, a
identidade e a versão de autoridade ficam **ambas** por verificar, e o registo passava por
essa porta — um `template` a apontar para um pacote que nem existe saía `complete`. O caminho
de erro é o que menos pode ser permissivo. Passou a impeditivo.

**O template consumido fora de `basis.authorities`.** É essa lista que a atualidade
recalcula e compara. Um contrato de projecção consumido e não declarado ali podia mudar sem
que a revisão ficasse *stale* por essa via. Numa revisão de `render` o template é sempre
consumido: a lista nunca pode estar vazia — e o primeiro guarda que escrevi (`if listed and
…`) tolerava precisamente a lista vazia, ou seja a versão mais limpa do defeito. Corrigido.

**A autoridade inexistente satisfeita por omissão.** Este foi encontrado por um teste novo,
depois de fechada a troca de template: com `v<approved>` a resolver para *nenhuma versão*,
um `blueprint_version_read: null` «concordava» com essa ausência e passava limpo — a
especificação projectada sem a sua autoridade, desta vez por omissão em vez de por troca. Ou
o registo declara a aplicabilidade (`blocked`/`not_applicable`, e então não dá obrigações por
projectadas), ou é achado.

**O que fica por conciliar, declarado como limite.** `deliverable.authority_sources` é
verificado na forma e no efeito que tem sobre a base de atualidade — não contra a lista que o
template declara em `authority_sources` / `conditional_sources`. Essa é prosa do contrato de
projecção, e compará-la por texto seria adivinhar. Fica por conta da passagem destino → fonte
da §9, que é do agente.

---

## 3. As provas

### 3.1 O ensaio, gerado por código

`python docs/runtime-hardening/repro-coverage-phase5-2026-09-15.py` →
`docs/review-evidence/coverage-phase5-rehearsal-2026-09-15.md`. Corre sobre uma cópia de
`.claude/tests/fixtures/coverage/fx-coverage-f06`; nenhum engagement real é lido ou escrito.

**Passo 1 — a selecção de autoridade, os seis deliverables.** A fixture tem `v03` autorizada
e nenhuma aprovada:

| deliverable | declara | resolve | estado |
|---|---|---|---|
| `discovery-report` | `none` | — | `no-blueprint-read` |
| `executive-report` | `none` | — | `no-blueprint-read` |
| `solution-blueprint` | `v<latest authorized>` | v03 | `available` |
| `implementation-spec` | `v<approved>` | — | `not-approved` |
| `claude-design-brief` | `v<approved>` | — | `not-approved` |
| `estimate` | `none` | — | `no-blueprint-read` |

**Passo 3 — o degrau, medido e não afirmado.** O mesmo registo, contra um motor igual em
tudo excepto na regra da §8.2:

| a regra da §8.2 | cobertura | pode avançar |
|---|---|---|
| desligada | `complete` | **sim** |
| ligada | `gaps` | não |

Era este o falso verde: o locator resolve (`ok=True`, `comment_only=True`), a linha
`<!-- C-007 -->` existe na `v01`, e o percurso de publicação não está lá.

**Passo 7 — o que o ensaio escreveu no engagement**: 0 ficheiros fora de `_coverage/`, onde
os registos do ensaio foram instalados de propósito.

### 3.2 Os testes

`.claude/tests/test_coverage_phase5.py` — 61 testes, verde:

| grupo | o que prende |
|---|---|
| `VersionAuthority` (20) | T31 e T22: cada template declara o token; o relatório de arquitectura lê a autorizada, spec e brief a aprovada; as três razões de ausência ficam distintas; uma aprovação torna a aprovada resolúvel; ler a versão errada é `COV-AUTHORITY-MISMATCH`; o caso que **só** a verificação nova apanha; e cobertura completa não é aprovação. Mais os **sete** da correcção de 2026-09-16 (§3.4) |
| `ProjectionIsNotAReference` (6) | T32 e T33: o comentário existe na fixture (sem o engodo o teste não provava nada); resolve e mesmo assim não é âncora; uma linha de tabela real continua a valer; um cabeçalho não é comentário; a saída perdida é lacuna; e verificar uma lacuna não escreve nada a montante |
| `NothingLegitimateIsHeld` (8) | T34 e T35: sem autorização, sem `_blueprint/` de todo, e um deliverable que não lê desenho — nenhum fica retido, e 0 achados impeditivos; `applicability` exige razão; um estado inventado é recusado; a aprovação histórica sobrevive e a cobertura lê `not_evaluated` |
| `NeverGreenByAccident` (6) | T24, T23 e T39: sem registo, registo partido, schema futuro; a revisão nova com lacunas não é substituída pela antiga completa; template alterado → `stale` |
| `Cli` (5) | o pré-render corre sem alvo; sem alvo nem deliverable é erro de uso; defeito de template nomeia o template; o pré-render não escreve nada (T38); editar o Markdown não muda autoridade nenhuma (T40) |
| `DeclaredFieldsMustAgree` (8) | §2.10: cada par declarado a ser partido um de cada vez, com o controlo coerente ao lado — e a declaração honesta (`blocked` **sem** obrigações cobertas) a não ser acusada |
| `WhatTheContractsSay` (8) | os contratos descrevem a ligação real, os três tokens são normativos e fechados, a tabela proibida continua proibida, skip ≠ lacuna, as duas verificações estão na skill, e a síntese transporta pendências |

### 3.3 A suite completa

`docs/review-evidence/coverage-phase5-tests-2026-09-16.txt` — **1906 testes**, 39 ficheiros,
**2 falhas**, as duas herdadas da §1. Nenhuma regressão introduzida, nem pela fase nem pela
correcção.

Cobertura em si: 460 testes nos sete ficheiros `test_coverage_*.py`.

### 3.4 As correcções, medidas

Os testes da §2.9, e o que cada um prende:

| teste | prende |
|---|---|
| `..._spec_reviewed_against_the_architecture_template_is_refused` | o caso reportado: `gaps`, não elegível, e o achado nomeia os dois deliverables |
| `..._no_approved_version_exists_in_the_fixture` | que o anterior não passa pela razão errada |
| `..._the_identity_is_accused_once_and_not_twice` | um facto, um achado — o segundo esconderia o primeiro |
| `..._the_mismatch_is_symmetric` | qualquer par discordante, não só este |
| `..._a_template_without_an_identity_cannot_confirm_the_contract` | sem `template_id` não se adivinha pelo nome do ficheiro |
| `..._the_precheck_refuses_another_deliverables_template` | o mesmo dever antes de produzir |
| `..._the_precheck_still_answers_for_the_right_template` | e continua a responder ao par certo |
| `..._the_contract_binds_the_record_id_to_the_template_identity` | a norma: o motor não impõe o que o contrato não escreve, e um contrato que a perca deixa o defeito voltar em silêncio |

E a medição, no ensaio (§4b), contra um motor igual em tudo excepto nesta verificação:

| a verificação de identidade | cobertura | pode avançar | versão aprovada |
|---|---|---|---|
| desligada | `complete` | **sim** | nenhuma |
| ligada | `gaps` | não | nenhuma |

O varrimento da §2.10 está no mesmo ensaio (§4c), com o controlo coerente na primeira linha:

| par declarado | cobertura | pode avançar | achado |
|---|---|---|---|
| (controlo) registo coerente | `complete` | sim | — |
| `id` vs `template_id` do template | `gaps` | não | `COV-AUTHORITY-MISMATCH` |
| `id` vs o deliverable do documento revisto | `gaps` | não | `COV-AUTHORITY-MISMATCH` |
| `template` vs `basis.authorities` | `not_evaluated` | não | `COV-SCHEMA` |
| `template` vs um ficheiro legível do pacote | `not_evaluated` | não | `COV-SCHEMA` |
| versão exigida que não existe, declarada por omissão | `gaps` | não | `COV-AUTHORITY-MISMATCH` |
| `applicability` não-produzido vs obrigações cobertas | `gaps` | não | `COV-REVIEW-INCOMPLETE` |
| `basis.pack` vs o pacote activo | `not_evaluated` | não | `COV-STALE` |

---

## 4. Comandos e resultados

```bash
# o pré-render, sobre a fixture
python library/kernel/tools/coverage.py check --engagement <fixture> \
    --stage render --deliverable implementation-spec          # exit 0
python library/kernel/tools/coverage.py check --engagement <fixture> \
    --stage render                                            # exit 2 (erro de uso)

# a revisão de projecção de um ficheiro produzido
python library/kernel/tools/coverage.py check --engagement <fixture> \
    --stage render --target _render/<...>_solution-blueprint_v02.md --json   # exit 0

# o ensaio e a suite
python docs/runtime-hardening/repro-coverage-phase5-2026-09-15.py
python .claude/tests/test_coverage_phase5.py                  # Ran 43, OK
for f in .claude/tests/test_*.py; do python "$f"; done         # 1888, 2 falhas herdadas
```

---

## 5. Critérios de saída

| critério (plano §12, *Fase 5*) | estado |
|---|---|
| saída exigida perdida no deliverable gera gap | **cumprido** — `ProjectionIsNotAReference`, e o ensaio passo 3 |
| o renderer não a inventa | **cumprido** — regras duras 7 e 8 da skill; verificar uma lacuna não escreve nada a montante (teste) |
| comentário com ID não substitui revisão semântica | **cumprido** — mecânico (§8.2) e medido (rule off → `complete`; rule on → `gaps`) |
| autoridade/versionamento correctos | **cumprido após correcção** — `VersionAuthority`, 18 testes. A primeira entrega tinha aqui um falso positivo (§2.9), fechado a 2026-09-16 |
| casos sem UI/arquitectura não são bloqueados por requisito inaplicável | **cumprido** — `NothingLegitimateIsHeld`, 0 achados impeditivos nos três casos |
| evidência: relatório + exemplo JSON/Markdown + resultados de selecção de autoridade | **cumprido** — este ficheiro + o ensaio §1, §6 |
| testes prioritários T22–T24, T31–T35, T39–T40 | **cumprido** — ver §3.2; T36/T37/T38 continuam onde a fase 4 os deixou |
| suites render, síntese e applicability | **cumprido** — `test_render_validate` (19), `test_synthesis_checks` (50), `test_synthesis_freshness` (27), `test_pp_deliverable_templates` (247), verdes |

---

## 6. Decisões de implementação que diferem do plano

1. **O token de versão vive no template, não numa tabela do kernel.** O plano (§9.2) proíbe
   a tabela «requisito → deliverable» e manda reutilizar o que existe. `blueprint_version_read`
   já existia no `solution-blueprint.template.md`; foi declarado nos outros cinco em vez de se
   criar um mapa no motor. Consequência: o motor genérico não contém o nome de deliverable
   nenhum, e um pacote novo declara a sua selecção sem tocar no kernel.

2. **Campo ausente é defeito, não `none`.** A leitura alternativa — ausente significa «não lê
   desenho» — era a única que podia falhar em silêncio no campo que decide a autoridade.
   Custo: cinco templates alterados (+19 linhas no total).

3. **`applicability` é opcional no registo, não obrigatório.** Um deliverable `not applicable`
   não produz registo nenhum: o seu *skip* em `render-log.md` é a resposta inteira. O campo
   existe para quem quiser declarar a aplicabilidade **dentro** de um registo que produz, e a
   `reason` é obrigatória quando ele existe.

4. **O pré-render é `check --stage render --deliverable <id>` sem `--target`**, em vez de um
   subcomando novo. Antes de produzir não existe alvo; o mesmo comando responde às duas
   perguntas do momento em que é feito.

5. **A identidade do contrato vem do `template_id` do próprio template**, não do nome do
   ficheiro nem de um mapa no motor. Um template pode ser movido ou renomeado; o que não pode
   é declarar-se de outro deliverable. Pelo caminho da convenção, `fake.template.md` a dizer
   `template_id: implementation-spec` passaria — e o nome do ficheiro não é declaração de
   ninguém.

6. **A regra do comentário devolve o nó, marcado, em vez de o esconder.** `_resolve_md`
   continua a resolver (`count: 1`) e acrescenta `comment_only`; é a regra da âncora que
   decide. Esconder o nó fá-lo-ia passar por locator morto, que é outro defeito.

---

## 7. Limitações

1. **A compreensão semântica continua por provar por código.** O motor verifica a forma da
   ligação — que o destino existe, que está no artefacto sob revisão, que não é um
   comentário. Se a secção apontada *diz* o que a obrigação exige é julgamento do agente,
   escrito e assinado. `T02`/`T32` exercitam a declaração, não a compreensão.

2. **A regra do comentário é sintáctica.** Apanha a linha que é só `<!-- … -->`. Uma linha de
   prosa vazia de conteúdo — «este requisito é tratado noutro sítio» — resolve e conta como
   âncora; é a passagem destino → fonte que a apanha, e essa é do agente.

3. **A aplicabilidade não é derivada.** O motor reporta os factos (há autorização? há
   aprovação? há escolha estrutural em aberto?); a decisão de produzir vem da prosa do
   template, que o código não interpreta. É deliberado — derivá-la seria o motor a decidir
   o que o contrato declara — e é uma dependência de julgamento, não uma garantia.

4. **O pré-render avalia a reconciliação quando não há versão resolvida.** Quando a versão
   exigida não existe, não há desenho para rever e o que resta é a reconciliação. O campo
   `upstream.stage` diz qual foi avaliada e `upstream_stage_required` qual seria a exigida —
   não se confundem, mas quem ler só o primeiro pode tirar a conclusão errada.

5. **Nenhum destes caminhos correu sobre um engagement real.** Toda a evidência é sobre a
   fixture. A fase 6 é que corre os 40 cenários e o ensaio ponta-a-ponta.

6. **Duas falhas herdadas continuam por fechar** (§1). São de conteúdo de `projects/`, não
   deste mecanismo, e nenhuma fase desta frente as pode fechar sem tocar no engagement real.

7. **A classe foi varrida, e o que resta dela está nomeado** (§2.10). Todos os pares do
   bloco `deliverable` e da `basis` estão conciliados; o que **não** está é
   `deliverable.authority_sources` contra a lista que o template declara em prosa — comparar
   as duas por texto seria adivinhar, e fica por conta da passagem destino → fonte, que é do
   agente. É uma dependência de julgamento declarada, não uma garantia.

8. **O varrimento foi por enumeração dos campos do contrato, não por prova.** Enumerei os
   campos que a §4.5 e a §4.2 declaram e parti cada par. Um campo que venha a ser acrescentado
   ao schema entra nesta mesma classe e precisa da mesma pergunta — nada no motor o obriga
   automaticamente.

---

## 8. Dependências concretas para a fase 6

1. **Os 40 cenários, um a um.** Esta fase exercitou T22–T24, T31–T35, T39–T40 na etapa
   `render`. T01–T21 e T25–T30 estão nas fases 1–4 e precisam de uma passagem conjunta.

2. **O ensaio isolado do fluxo completo** (plano §12, *Fase 6*, ponto 2): fontes →
   reconciliação → desenho com perda → revisão correctiva → cobertura actual → ausência de
   aprovação → aprovação simulada **só em fixture** → render com perda → render corrigido →
   nova resposta que invalida a cobertura. As peças existem todas; falta a corrida única.

3. **Revisão do diff** quanto a estados/autoridades duplicados, hardcodes do caso real,
   imports circulares e hashes auto-referenciais — com atenção ao par de verificações da
   §2.3, que é o sítio onde uma segunda autoridade se poderia ter instalado.

4. **Integridade do engagement real por manifesto antes/depois**, e ausência de mutações
   pelos comandos read-only.

---

## 9. O que esta fase explicitamente não declara

O desenho real **não** está aprovado, **não** está completo e **não** está validado
ponta-a-ponta. A cobertura do engagement real **não foi avaliada**. Nenhuma pergunta em
aberto foi respondida. Nenhuma aprovação foi registada, e nenhuma aprovação histórica foi
tocada. Nenhum deliverable real foi produzido ou re-produzido.

O que esta fase entrega é **a pergunta da preservação feita no sítio certo, com a versão
certa, e a resposta separada das outras três** — estrutura, cobertura, aprovação e
ponta-a-ponta continuam quatro perguntas, e nenhuma responde pela outra.
