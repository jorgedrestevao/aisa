# Fase 3 — Validador, CLI e persistência versionada

Data: 2026-09-15. Ramo: `runtime-correction/pilot-r1-r7`, working tree em `f4ffef2`.
Plano: `docs/runtime-hardening/coverage-reconciliation-implementation-plan.md` §12, fase 3.
Entrada: `coverage-phase-1-report.md` e `coverage-phase-2-report.md`, lidos e com os
pré-requisitos verificados antes de escrever código (§1).

Este relatório incorpora as **sete voltas de revisão** que devolveram a fase 3. O que
mudou em cada uma está na §5.1 a §5.7; o resto descreve o estado corrigido.

> **O mecanismo continua desligado.** Esta fase entrega o verificador, a linha de comandos e
> a publicação versionada. **Nenhum comando, skill, hook ou portão mudou de comportamento**:
> `/blueprint`, `/answer`, `/status` e `/render` correm hoje exactamente como corriam ontem,
> e nenhum deles chama este motor. A integração é a fase 4. **Nenhuma cobertura do
> engagement real foi avaliada** — o que ele dá, e continua a dar, é `not_evaluated`.
> **Nenhuma aprovação foi registada em nome de ninguém**, e nenhuma pergunta em aberto foi
> respondida.

## 1. Pré-requisitos verificados

As seis dependências que a fase 2 declarou (§10 do seu relatório), e o que aconteceu a cada
uma:

| # | dependência | estado |
|---:|---|---|
| 1 | correr `test_blueprint_yaml.py` num checkout com os engagements do snapshot montados; se o F16 acusar diferença, justificá-la | **impossível neste checkout, e fechado por prova** (§4) |
| 2 | validação de schema contra o contrato §4, com os 20 registos da fase 1 | feito; os 20 exercitados, um código de cada vez (§3.2) |
| 3 | selecção por etapa/target/autoridade (§6.6) e veredictos separados, com `not_evaluated` legítimo | feito (§3.4) |
| 4 | `check`, `report`, `finalize`, códigos de saída e finalização exclusiva | feito (§3.5, §3.6) |
| 5 | demonstrar o F06 nos dois sentidos | feito, com a estrutura a dizer «válido» ao lado da cobertura a dizer «perdeu» (§3.1) |
| 6 | não integrar nada em comandos, skills ou hooks | respeitado — zero ficheiros de comando, skill ou hook alterados |

Revalidação de fecho da fase 2 antes de começar: os três módulos de cobertura verdes,
**64 + 86 + 50 = 200 testes**, e a suite completa com as duas falhas pré-existentes de
sempre e mais nenhuma.

## 2. O que foi construído

### 2.1 Ficheiros

| ficheiro | o que mudou |
|---|---|
| `library/kernel/tools/coverage.py` | +2095 linhas (1339 → 3434): validação, selecção, resultado computado, relatório, `finalize`, e a linha de comandos com quatro subcomandos |
| `library/kernel/coverage-contract.md` | 832 → 997 linhas: o cabeçalho e sete secções clarificadas, mais vinte e duas ambiguidades novas no registo da §11 (24–45) |
| `.claude/tests/test_coverage_contract.py` (novo) | **101 testes**: F06, schema, destinos, exclusões, herança, semântica, selecção, autoridade, elegibilidade, relatório, porta do rascunho |
| `.claude/tests/test_coverage_integration.py` (novo) | **53 testes**: códigos de saída, ambiente, zero escrita, `finalize`, **finalização sob mudança**, pré-visualização de rascunho, o relatório que não manda, engagement real |
| `.claude/tests/test_coverage_inventory.py` | a guarda da árvore sintáctica ganha **uma** excepção nomeada (`read_draft`) e passa a exigir que a razão dela esteja escrita no motor (§5, A10) |
| `.claude/tests/test_blueprint_yaml.py` | +2 testes: a prova do F16 contra o snapshot (§4) |

**Zero ficheiros de runtime alterados fora do motor**: nada em `.claude/skills/`,
`.claude/hooks/`, `.claude/commands/`, `.claude/settings.json` ou `projects/`.

### 2.2 A API

```python
load_records(eng)                                  -> list   # os registos de `_coverage/`
select_record(eng, stage, identity)                -> dict   # §6.6: a mais recente do par
validate_record(record, inventory, eng, ...)       -> dict   # §4: forma + disposições
coverage_state(eng, stage, target, record=None)    -> dict   # §7: o resultado computado
structural_check(eng, rel)                         -> dict   # §8.1.4: chama `bp_validate`
render_report(record, result)                      -> str    # a projecção Markdown
finalize(eng, draft_path)                          -> dict   # a ÚNICA escrita do módulo
read_draft(path)                                   -> tuple  # a porta do rascunho
```

**Os treze códigos da tabela §8 estão todos ligados.** A fase 2 emitia cinco; os oito que
faltavam — `COV-SCHEMA`, `COV-NO-REVIEW`, `COV-UNREVIEWED`, `COV-MISSING-TARGET`,
`COV-EXCLUSION-NO-DECISION`, `COV-REVIEW-INCOMPLETE`, `COV-KNOWN-GAP` e
`COV-AUTHORITY-MISMATCH` — entram aqui, da mesma tabela e com a mesma forma de
diagnóstico (`{code, severity, file, locator, item, message, resolves}`).

### 2.3 A linha de comandos

```text
coverage.py inventory --engagement <slug|caminho> [--json]
coverage.py check     --engagement <slug> --stage reconciliation [--json]
coverage.py check     --engagement <slug> --stage blueprint --target <ficheiro> [--json]
coverage.py check     --engagement <slug> --stage render --target <f> --deliverable <id>
coverage.py report    --engagement <slug> [--stage <etapa>] [--record <ficheiro>]
coverage.py finalize  --engagement <slug> --draft <rascunho.json>
```

`inventory`, `check` e `report` não abrem nada para escrita. `finalize` escreve **só** em
`_coverage/`, e só por reserva exclusiva de uma versão nova.

## 3. As provas que a fase pedia

### 3.1 O F06, nos dois sentidos

```text
estrutura da v01: 0 bloqueios, 0 avisos   (o verificador instalado diz «válido»)

v01  cobertura=gaps      elegível=False  lacunas: C-007=missing, C-010=missing
v02  cobertura=gaps      elegível=False  lacunas: C-010=partial
v03  cobertura=complete  elegível=True   lacunas: nenhuma

blocos em decisions.md: ['D-001 — Frame agreed (F-01)',
                         'D-002 — Adopt O-002 — aplicação com base de dados governada']
aprovação de desenho registada: NÃO
```

É esta a asserção central do plano, e agora é código a dizê-la: **a mesma versão que o
verificador estrutural dá por válida perdeu um requisito que a Shared Understanding já
carregava.** A `v03` fecha a outra ponta: sem lacunas, sem escolha estrutural aberta, e
**sem aprovação nenhuma** — que ninguém inventou, porque não há de onde a inventar.

O destino decorativo é apanhado pelas duas vias mecânicas que a fase 1 plantou:

| fixture | o que declara | código |
|---|---|---|
| `rec-neg-decorative-projection` | `covered` cujo único destino é a entidade que cita o id | `COV-MISSING-TARGET` |
| `rec-neg-decorative-invalid-target` | mente no papel (`implementation`) e aponta para um componente que a `v01` não tem | `COV-INVALID-TARGET` |

Nenhuma das duas prova que o código entende semântica. Provam que **a existência de uma
referência não substitui a avaliação**, que é exactamente o que o plano pede em T02.

### 3.2 Os vinte registos, um a um

Cada registo da fase 1 foi corrido contra a fixture e produz o que o README dela declara:

| registo | resultado calculado | código esperado | bate |
|---|---|---|:--:|
| `rec-v01-reconciliation-complete` | `source_review: complete`, `coverage: complete`, elegível, `U-010` em aberto | — | ✔ |
| `rec-v02-blueprint-missing` | `coverage: gaps`, C-007 e C-010 `missing` | `COV-KNOWN-GAP` | ✔ |
| `rec-v03-blueprint-partial` | `coverage: gaps`, só C-010 `partial` | `COV-KNOWN-GAP` | ✔ |
| `rec-v04-blueprint-complete` | `coverage: complete`, **aprovação ausente** | — | ✔ |
| `rec-v05-render-complete` | `coverage: complete` na etapa `render` | — | ✔ |
| `rec-neg-unreviewed-unit` | `source_review: incomplete`, 1 unidade nomeada | `COV-UNREVIEWED` | ✔ |
| `rec-neg-obligation-dropped` | obrigação `{C-008}` perdida entre etapas, registo **continua válido** | `COV-UNREVIEWED` | ✔ |
| `rec-neg-decorative-projection` | destino decorativo | `COV-MISSING-TARGET` | ✔ |
| `rec-neg-decorative-invalid-target` | nó que não existe | `COV-INVALID-TARGET` | ✔ |
| `rec-neg-dead-ref` | `C-999`, `answers.md#U-020`, entidade inexistente | `COV-DEAD-REF` + `COV-INVALID-TARGET` | ✔ |
| `rec-neg-exclusion-no-decision` | retira C-007 (unidade material) sem autoridade | `COV-EXCLUSION-NO-DECISION` | ✔ |
| `rec-neg-exclusion-undetermined` | retira sem ligar unidade nenhuma | `COV-REVIEW-INCOMPLETE` | ✔ |
| `rec-pos-exclusion-mechanical` | retira o grupo mecânico com fundamento | **aceite**, `coverage: complete` | ✔ |
| `rec-neg-semantic-pending` | tudo resolve, leitura por acabar | `semantic_review: pending`, não elegível | ✔ |
| `rec-neg-schema-future` | `schema_version: 2` | `unsupported`, tudo o resto `not_evaluated` | ✔ |
| `rec-neg-schema-invalid` | sem `basis`, item sem `assessment` | `invalid`, `coverage: not_evaluated` | ✔ |
| `rec-neg-stale-target` | target com o digest da versão errada | `freshness: stale` | ✔ |
| `rec-neg-authority-mismatch` | render que diz ter lido `v01` e consome a revisão de `v03` | `COV-AUTHORITY-MISMATCH` | ✔ |
| `rec-neg-capture-limit-as-covered` | o `.pptx` marcado `not_applicable` | `COV-CAPTURE-LIMIT` | ✔ |
| `rec-neg-render-id-in-comment` | `covered` sobre um render que só tem `<!-- C-007 -->` | `COV-INVALID-TARGET` | ✔ |

Duas notas de honestidade sobre esta tabela:

- **`rec-neg-decorative-invalid-target` dispara dois códigos**, `COV-INVALID-TARGET` e
  `COV-MISSING-TARGET`. Não é um código a esconder o outro (a proibição da D15): é o mesmo
  facto visto duas vezes — o único destino de implementação não resolve, logo a âncora que
  `covered` exige não existe. O primeiro diz o que está partido; o segundo, o que isso
  custa.
- **`rec-neg-dead-ref` dispara quatro.** O item que a fixture acrescenta tem um requisito
  inexistente, uma unidade de origem inexistente e um nó inexistente ao mesmo tempo, e o
  motor nomeia os três em vez de parar no primeiro.

### 3.3 A protecção contra carimbar fontes alteradas como revistas

É o pedido explícito desta passagem, e tem três fechos, não um:

```text
1) rascunho limpo  -> revisão publicada como v01 · exit 0
2) outra vez       -> revisão publicada como v02 · exit 0     (v01 intacta)
3) fonte nova em inputs/ ->
   a base mudou depois de a revisão ser escrita: inventário mudou desde a revisão
   — inventory_sha256; fonte nova depois da revisão — inputs/pedido-novo.txt —
   publicar agora carimbaria como revista uma fonte que mudou sem ser relida
   · exit 4
   v01 intacta:                            True
   digest do rascunho não foi reescrito:   True
   escrita fora de `_coverage/`:           nenhuma
```

| fecho | o que impede |
|---|---|
| **antes de reservar** | `finalize` recalcula a base e compara-a com o snapshot que o rascunho declara. Diferente → recusa, e os digests antigos **nunca** são substituídos pelos actuais |
| **depois de escrever** | recalcula a base **e o alvo**, e volta a correr a **mesma** comparação da entrada. Se alguma coisa se mexeu durante a operação, a reserva é desfeita e nada fica publicado (defeito P2) |
| **no fim, sobre o veredicto que vai ser reportado** | o último veredicto é o que manda: se o estado que a operação ia anunciar não é `current` e `valid`, a reserva desfaz-se. Há sempre uma janela entre uma verificação e a linha seguinte; o que não pode haver é publicar depois de a ter visto fechada (defeito P2b) |
| **na reserva** | `os.open(..., O_CREAT|O_EXCL)`. Quatro finalizações concorrentes na mesma cópia ficam com quatro versões distintas, e nenhuma escreve por cima de outra. **Não existe um `os.replace` neste ficheiro** — verificado pela árvore sintáctica, não por procura de texto, porque o docstring diz isso mesmo em prosa |

E a revisão publicada **avalia-se a si própria**, por nome: com duas finalizações
concorrentes, «a mais recente da etapa» é a da outra, e era esse o defeito P3.

Um rascunho com lacunas conhecidas **publica-se**: uma revisão que declara incompletude é
evidência válida, não lixo. O que não se publica é um registo que ninguém consegue ler
(`exit 2`) ou um que descreve uma base que já não existe (`exit 4`).

### 3.4 Selecção por etapa e por alvo

| cenário | resultado |
|---|---|
| duas revisões do mesmo par (etapa, alvo) | vale a **mais recente**; a anterior aparece em `superseded` |
| a mais recente tem lacunas e a anterior estava completa (T23) | escolhe a **recente**, com as lacunas à vista |
| revisão da `v01` e pergunta-se pela `v03` | `COV-NO-REVIEW` — uma revisão de outra versão não é aplicável a esta |
| sem registo nenhum | `not_evaluated` em toda a linha, `exit 4` |
| registo que existe e não se lê | `invalid` **em todas as etapas**, e o ficheiro é nomeado. Não se sabe a que etapa pertence — por isso bloqueia todas (defeito P1, §5.1) |
| um registo partido ao lado de um válido | `invalid`, `not_evaluated`, saída 2 — **nunca** o válido escolhido em silêncio |
| um registo que parseia e não se consegue situar (`{}`, sem `stage`, etapa inventada, desenho sem alvo) | o mesmo: situar vem antes de filtrar (defeito P1b) |
| um schema desconhecido que **diz** a que par pertence | seleccionado, e `unsupported` — situar não é validar |
| a revisão da `v03` com a etiqueta `identity` trocada para `v01` | não se consegue situar → `invalid`, saída 2 (defeito P1c) |
| a revisão que prova a cobertura da `v01` com nós da `v03` | `COV-AUTHORITY-MISMATCH`, e o `covered` fica sem âncora (defeito P1d) |
| uma revisão que assenta numa reconciliação por fechar | `COV-UNREVIEWED`, com a de montante nomeada (defeito P2d) |
| `based_on` para si própria, em ciclo, ou da etapa errada | `invalid`, saída 2 |
| a revisão de montante não se consegue avaliar | impeditivo, com o ficheiro que falhou e o código da causa (defeito P2e) |
| `coverage[]` esvaziado com as fontes revistas | `COV-REVIEW-INCOMPLETE` — material lido e nenhuma obrigação contradizem-se (defeito P1e) |
| a `v02` da reconciliação larga cinco das seis obrigações da `v01` | `COV-UNREVIEWED` ×5, com a revisão anterior nomeada — obrigações não desaparecem, recebem disposição |
| a `v03` **repete** a `v02` que largou cinco | `COV-UNREVIEWED` ×5 na mesma, nomeadas a partir da `v01` — repetir a revisão que largou não apaga (defeito P1f) |
| `links` para item, linha ou obrigação inexistente | `COV-DEAD-REF` |
| reconciliação com referência morta e lacunas todas encaminhadas | não elegível — um achado impeditivo bloqueia a produção, não só a aprovação (R8) |
| dois registos a declarar a mesma identidade sobre ficheiros diferentes | separados pelo ficheiro, não pela etiqueta |

### 3.5 Códigos de saída, e o JSON que sai com todos eles

| situação | código | verificado |
|---|---:|---|
| reconciliação completa e actual | 0 | ✔ |
| desenho com lacunas | 4 | ✔ |
| sem revisão | 4 | ✔ |
| schema inválido ou versão futura | 2 | ✔ |
| etapa que exige alvo, sem `--target` | 2 | ✔ |
| `reconciliation` com alvo | 2 | ✔ |
| engagement desconhecido | 3 | ✔ |
| vários engagements sem `--engagement` | 2 | ✔ |
| alvo fora da fronteira do engagement | 3 | ✔ |

`--json` imprime o resultado completo **mesmo com saída 4**, e `exit 0` não significa
aprovação: a saída 0 sobre a `v03` da fixture vem acompanhada da razão *«falta o pedido de
aprovação ao negócio, que nenhum motor substitui»*, e `decisions.md` continua sem bloco de
aprovação nenhum.

### 3.6 Zero escrita, e o relatório que não manda

- **Manifesto SHA-256 do engagement antes e depois** de duas rondas de `inventory`,
  `check` e `report`: idêntico, ficheiro a ficheiro.
- **Duas execuções seguidas** dão saída byte-idêntica e o mesmo código.
- **Árvore sintáctica**: `write_text`, `write_bytes`, `mkdir`, `unlink` e `rename` só
  existem dentro de `finalize` e de `_coverage_dir`. Uma função nova que escreva noutro
  sítio acende este teste no instante em que for escrita.
- **T40**: editar o `.md` publicado — trocar `gaps` por `complete`, `não` por `sim` e
  acrescentar «APROVADO POR TODOS» — não muda um único veredicto, porque os veredictos são
  recalculados a cada leitura e o `.md` não é lido por ninguém. `report` reimprime a
  projecção a partir do JSON e **não** reescreve o ficheiro.

### 3.7 Exemplo gerado por código

`check --stage blueprint --target _blueprint/ux-blueprint_v01.yaml --json`, **exit 4**:

```json
{
  "artefact": "aisa.coverage.state",
  "stage": "blueprint",
  "contract_validity": "valid",
  "freshness": "current",
  "source_review": "complete",
  "semantic_review": "completed",
  "coverage": "gaps",
  "action": "approve_blueprint",
  "eligible": false,
  "target": { "file": "_blueprint/ux-blueprint_v01.yaml", "identity": "v01" },
  "record": { "file": "_coverage/coverage_v02.json", "version": "v02",
              "generated_at": "2026-03-10T10:00:00+01:00" },
  "gaps": [
    { "item": "item-001", "status": "missing", "requirement_refs": ["C-007"],
      "required_action": "Concretizar a publicacao diaria e a consulta no desenho.",
      "responsible_role": "arquitetura" },
    { "item": "item-005", "status": "missing", "requirement_refs": ["C-010"],
      "required_action": "Desenhar o ponto de imposicao no armazenamento.",
      "responsible_role": "arquitetura" }
  ],
  "reasons": ["Há obrigações por cobrir ou por fundamentar; a versão pode continuar em
               discussão, mas não se anuncia pronta para aprovação."]
}
```

E a projecção Markdown do mesmo estado, gerada por `report` (extracto):

```markdown
# Revisão de cobertura — fx-coverage-f06 · etapa blueprint

> Projecção determinística do registo em JSON. **Não é autoridade**: os veredictos são
> recalculados a cada leitura e editar este ficheiro não muda nenhum deles.

| dimensão | resultado |
|---|---|
| contrato do registo | válido (valid) |
| actualidade da base | actual (current) |
| revisão das fontes | completa (complete) |
| leitura nos dois sentidos | concluída (completed) |
| cobertura | com lacunas (gaps) |
| pode avançar | não |

## Lacunas conhecidas

| item | requisito | estado | o que falta | a quem toca |
|---|---|---|---|---|
| item-001 | C-007 | missing | Concretizar a publicacao diaria e a consulta no desenho. | arquitetura |
| item-005 | C-010 | missing | Desenhar o ponto de imposicao no armazenamento. | arquitetura |
```

## 4. A dependência 1, e porque está fechada sem correr o teste que a pedia

A fase 2 deixou escrito: *correr `test_blueprint_yaml.py` num checkout com os engagements do
snapshot montados.* **Não é possível neste checkout, e não é por falta de vontade**:
`.gitignore` tem `projects/*`, os engagements vivem num repositório privado, e os 12
ficheiros que o snapshot referencia (`pricing-marinha-pilot-1` e `-val-b`) não estão aqui.
O teste **continua a saltar**, e um teste saltado não prova nada.

O que **é** possível é responder à pergunta que ele responderia, e a resposta é por
construção:

1. A correcção F16 mudou `decision_ref` de `yl_scalar_at("decision_ref")` para
   `yl_scalar_at("decision_ref") or yl_scalar_at("concretizes_decision")`.
2. O `or` **só chega ao segundo termo quando o primeiro é vazio**.
3. O snapshot registou `decision_ref: "decisions.md#D-002"` — **não vazio** — para os 12
   ficheiros. Logo o primeiro termo era verdadeiro em todos; logo o segundo nunca é
   avaliado; logo o valor não pode ter mudado.
4. `decision_id` é chave **nova**, e a comparação do snapshot percorre as chaves que o
   snapshot tem. Uma chave que ele não conhece não gera diferença nenhuma.

Isto está agora em dois testes, não em prosa:
`test_the_f16_alias_cannot_move_any_value_in_this_snapshot` falha se algum ficheiro do
snapshot tiver `decision_ref` vazio (o caso em que o alias **poderia** mexer, e que exigiria
entrada justificada), e `test_the_alias_only_fires_when_the_primary_key_is_absent` exercita
o leitor com as duas formas reais.

**O que isto não prova:** se um daqueles engagements ganhar amanhã um desenho sem
`decision_ref`, o snapshot terá de ser refeito de qualquer maneira. E a lista justificada
continua por confirmar contra os ficheiros reais — o que se fechou foi a pergunta do F16,
não o teste de snapshot inteiro.

## 5. Defeitos encontrados, e o que mudou

### 5.1 Oitava volta — repetir a revisão incompleta lavava as lacunas

| # | defeito | porque passava | correcção | regressão |
|---:|---|---|---|---|
| **P1f** | **três `finalize`**: `v01` seis obrigações, `complete`; `v02` mantém uma, `gaps`; `v03` **repete a v02** e sai `complete`, `eligible: true`. As cinco obrigações deixavam de ser exigidas sem disposição nenhuma | o R7 da sétima volta comparava só com a revisão **imediatamente anterior** — e a anterior da `v03` era a `v02`, que já só tinha uma. Corrigi o esvaziamento e deixei a lavagem: bastava repetir | o conjunto exigido é a **união** das obrigações de **todas** as versões anteriores do par. Uma obrigação que apareceu uma vez fica exigida até receber disposição, e cada perdida nomeia a versão onde apareceu. A disposição, uma vez dada, tem de ser transportada — a `v04` que volta a largar o que a `v03` retirou com autoridade é apanhada (a exclusão herdada reaparece) | `ObligationsDoNotVanish`: 3 testes; repostas «só a anterior» e a comparação inteira, **2 e 4 acendem** |

O padrão repete-se e fica dito: corrigi onde o defeito aparecia (a `v02` que larga) e não
onde nascia (o que é que uma revisão nova é obrigada a honrar). A resposta certa é
monótona — **tudo o que alguma vez foi obrigação** — e qualquer coisa menos do que isso tem
uma sequência de versões que a contorna.

### 5.2 Sétima volta — obrigações que desaparecem sem impedir o verde

| # | defeito | porque passava | correcção | regressão |
|---:|---|---|---|---|
| **P1e** | **`coverage[]` esvaziado com as fontes revistas dava `complete`**, na reconciliação e no desenho. E `source_review.links` aceitava referências inexistentes | o motor verificava que as fontes tinham sido lidas e nunca perguntava se alguma obrigação tinha sido tratada. Eu tinha visto esta porta na quinta volta e escrevi «não vou inventar uma regra sobre vazio» — e não era preciso inventar nenhuma: **material lido e nenhuma obrigação contradizem-se**, e isso é forma, não semântica | quatro regras pela forma: **R1** `links.*` resolvem, ou são `COV-DEAD-REF`; **R4** zero obrigações com material lido é revisão por acabar; **R7** obrigações não desaparecem entre revisões sucessivas do mesmo par — a regra da §4.4.4 entre etapas, aplicada entre versões, que é a que fecha o **esvaziamento parcial** (o reporte não o testou, e é o ataque realista: a `v02` larga cinco das seis); **R8** um achado impeditivo bloqueia a produção, não só a aprovação | `ObligationsDoNotVanish`: 9 testes; repostas as quatro, **1 + 1 + 1 + 2 acendem** |

O **R8** merece a sua linha: a elegibilidade da reconciliação só olhava para as lacunas
encaminhadas. Um registo com referências mortas ou um `covered` sem âncora saía elegível
para produzir um desenho. Nenhum teste anterior o apanhou porque nenhum registo negativo da
fase 1 é de reconciliação com achado impeditivo — e dois testes meus **estavam a passar por
cima desse buraco**: mutavam um registo substituindo `findings` (largando o item `excluded`),
o que é achado impeditivo, e saíam elegíveis na mesma. Com o R8 acenderam; corrigi os
testes, não a regra.

O que o motor **não** faz, e fica dito com todas as letras (limitação 11): não decide
**quais** unidades geram obrigações. Na fixture, 35 unidades de SU, respostas e
enquadramento estão todas `reviewed`/`material` e só 7 são obrigações — por escolha do
revisor, que o contrato §9 protege. Uma regra «material ⇒ obrigação» partia o registo
canónico sem inventar julgamento nenhum, e foi por isso recusada. O que a forma consegue
garantir é que a escolha do revisor **não se desfaz em silêncio**: nem toda de uma vez (R4),
nem entre versões (R7), nem largando as ligações que ele próprio escreveu (R1).

E um defeito da **fixture da fase 1**, encontrado pelo R1: os três registos de `render`
reutilizavam a revisão de fontes do desenho, cuja entrada `sr-006` liga a `item-006` — que
em `render` não existe, porque a obrigação `{C-009}` está em `not_selected`. Uma ligação
morta que ninguém verificava. `build_fixtures.py` passa a gerar a variante de render sem
essa ligação, e os registos foram regenerados (só os três de render mudaram).

### 5.3 Sexta volta — o erro engolido em montante

| # | defeito | porque passava | correcção | regressão |
|---:|---|---|---|---|
| **P2e** | **a falha a avaliar a revisão de montante era engolida.** Uma reconciliação com `target` — que a etapa proíbe — faz a sua avaliação levantar `CoverageError`. `upstream_health` apanhava-o e seguia com `continue`: `upstream: []`, e o desenho dava `complete`, `eligible: true`, saída 0 | escrevi `except CoverageError: continue` **com uma racionalização por cima** («o erro de forma já sai pela validação do registo») — e não sai, porque ninguém valida o registo de montante senão por aqui. Uma lista de montante vazia porque a avaliação falhou lê-se exactamente como vazia porque estava tudo bem | a falha fica **registada** na entrada de montante — ficheiro, erro, código (`COV-SCHEMA` quando é o registo de montante que está mal, `COV-UNEXPECTED` quando é o motor) — e é impeditiva. Contrato §8: falha de avaliação é «não avaliado», nunca sucesso silencioso. Uma varredura pela árvore sintáctica encontrou mais dois `except` com o corpo só de `continue`/`pass` — um `OSError` ao inspeccionar um caminho em `engagement_files` (o caminho desaparecia do inventário em silêncio; agora é diagnóstico impeditivo) e a reconfiguração da consola no entrypoint (passa a devolver um valor). Nenhum dos dois era falso verde; ambos violavam a regra | `TheChainIsValidated`: 2 testes (o `CoverageError` real, e um `RuntimeError` injectado); reposto o `continue`, **1 acende** |

Este é o défice mais embaraçoso das cinco voltas, e por isso o mais útil de escrever: o
mecanismo inteiro existe para que **nenhuma falha de avaliação se pareça com um verde**, o
contrato di-lo à letra em três sítios, e eu escrevi um `continue` que fazia exactamente
isso — com um comentário a explicar porque é que não fazia mal. A regra que fica: **um
`except` que não regista é um `except` que mente**, e a varredura que o encontrou passa a
correr como teste (`ReadOnly.test_no_except_swallows_silently`).

### 5.4 Quinta volta — o destino noutra versão e a cadeia por validar

| # | defeito | porque passava | correcção | regressão |
|---:|---|---|---|---|
| **P1d** | **os destinos que provam a cobertura viviam noutra versão.** Alvo e digest correctos da `v01`, e **todos** os `coverage[].targets` a apontar para a `v03`: `current`, `complete`, `eligible: true` | cada verificação confirmava a sua parte e nenhuma cruzava as duas: os locators resolvem (a `v03` existe e tem os nós), o alvo confere (é mesmo a `v01`), e ninguém perguntou se o nó que prova a concretização está **na versão revista** | um destino com o papel-âncora da etapa tem de estar em `target.file`. Fora dele: `COV-AUTHORITY-MISMATCH`, e **não conta como âncora** — logo o `covered` fica sem âncora e cai. Destinos que não são âncora (uma linha da SU citada num registo de desenho) continuam livres, com teste próprio | `TargetsBelongToTheReviewedVersion`: 4 testes; reposto o defeito, **2 acendem** |
| **P2d** | **a revisão a montante não era validada.** Uma reconciliação pobre — uma entrada de revisão, zero obrigações — deixava declarar um desenho com `coverage: []` como completo. E `based_on` era aceite a apontar para a própria revisão, ou em ciclo | a herança de obrigações da §4.4.4 passava **por vacuidade**: sem obrigações a montante, não há nenhuma a perder. A §8.1 já exigia a reconciliação completa e actual — o motor é que nunca a lia | a revisão citada em `based_on` é avaliada **com o mesmo motor, pelo seu próprio nome**; se não está `valid` + `current` + `source_review: complete`, a de jusante não pode estar completa. E `based_on` só cita **versões estritamente anteriores**: as versões são imutáveis e crescem, por isso auto-referência e ciclos morrem por construção, sem percorrer grafo nenhum. Mais a etapa: uma cadeia só de desenhos nunca tocou na reconciliação | `TheChainIsValidated`: 7 testes; repostas as duas guardas, **2 e 1 acendem** |

E um terceiro, que não veio da revisão: o meu próprio arnês de reprodução passou uma
**string** onde `coverage_state` espera um mapa, e o motor rebentou com `COV-UNEXPECTED`.
É o P2c outra vez, uma camada acima — o argumento da API em vez do campo do registo — e
está fechado pela mesma régua: tipo errado é erro de uso, saída 2, nunca falha interna.

### 5.5 Quarta volta — a etiqueta trocada e o tipo errado

| # | defeito | porque passava | correcção | regressão |
|---:|---|---|---|---|
| **P1c** | **a cobertura de uma versão validava outra.** Na revisão completa da `v03`, trocando **só** `target.identity` para `"v01"`, a `v01` saía `complete`, `eligible: true`, saída 0 | a selecção cruzava a identidade e mais nada. E as outras verificações confirmavam-se todas a si próprias: o digest do alvo confere (o registo aponta para a `v03` e compara-se com a `v03`), a identidade confere (foi trocada à mão), e ninguém perguntava se o **ficheiro revisto** era o que se pediu | o cruzamento passa a ser nos **dois sentidos**: `target.identity` tem de ser a identidade que o próprio `target.file` dá, e o `target.file` tem de ser o ficheiro que a acção pede. Um registo que diga rever uma versão e aponte para outra **não se consegue situar** — bloqueia, em vez de ficar apenas fora de toda a selecção, que era seguro e **invisível** | `Selection`: 4 testes novos; repostos os dois cruzamentos, **1 + 1 acendem** |
| **P2c** | **tipo errado dava falha interna.** `target: "bad"` e `based_on: [{}]` davam `COV-UNEXPECTED`, saída **5** e stdout vazio. E não eram dois: `based_on: 7` e `basis: "x"` faziam o mesmo | o motor lia o registo como se o tipo estivesse certo (`(rec.get("target") or {}).get(...)` sobre uma string, `chain.get(name)` sobre um mapa não-hashável). A validação de forma existia, mas o acesso vinha antes dela | `_as_dict()` e `_as_list()` em todo o acesso que possa receber outro tipo, mais diagnósticos de `COV-SCHEMA` que nomeiam o campo **e o tipo recebido**. Saída 2, com JSON. Uma string onde o contrato pede lista é erro de forma, não uma lista de caracteres | `WrongTypesAreSchemaErrors`: 3 métodos, **22 formas de tipo errado**; reposto `_as_dict`, **19 acendem** |

O P2c é o mais revelador dos oito: **a validação de forma estava escrita e o motor lia o
registo antes de a correr.** Um `exit 5` sem JSON manda quem lê procurar o problema no
motor, quando o problema é o ficheiro dele — e é a diferença entre um diagnóstico e um
beco.

### 5.6 Terceira volta — os dois que sobreviveram à segunda

A segunda volta corrigiu o sintoma de dois deles e deixou a causa de pé. **É o achado mais
instrutivo dos três lotes**, e é sobre a forma das minhas correcções, não sobre o contrato:

| # | defeito | o que a segunda volta corrigiu, e o que deixou | correcção | regressão |
|---:|---|---|---|---|
| **P1b** | **o mesmo falso verde, pela porta do lado.** Com a `v01` válida e a `v02` a conter `{}`, `{"schema_version": 99}`, uma etapa inventada ou um registo de desenho **sem alvo**, o motor voltava a devolver `complete`, `eligible: true`, saída 0 | a segunda volta bloqueou o registo que **não parseia**. Mas a selecção filtrava por `stage` **antes** de perguntar se o registo se conseguia situar — e um registo que parseia sem `stage` legível «não era desta etapa», desaparecia em silêncio, e a revisão anterior ficava a valer | **situar vem antes de filtrar**. `_cannot_situate()` responde a uma pergunta só: *a que par (etapa, alvo) pertence isto?* Não parseia, não traz `stage`, traz uma etapa que não existe, ou é de desenho/render sem `target.identity` → impeditivo em **todas** as etapas. E situar **não é validar**: um schema desconhecido que diga a que par pertence continua a ser seleccionado e a sair `unsupported`, nunca `invalid` | `Selection`: 2 testes novos (4 variantes + a fronteira `unsupported`); reposto o defeito, **4 acendem** |
| **P2b** | **publicava apesar de já ter visto que não devia.** Mexendo no desenho entre a verificação de saída e `coverage_state`, saía outra vez `published: true` com `freshness: stale` | a segunda volta pôs a verificação de saída a cobrir o alvo. Mas a seguir vem `coverage_state`, que recalcula tudo outra vez — e o seu veredicto, já `stale`, ia para dentro do resultado **sem desfazer nada**. A operação detectava e publicava na mesma | **o último veredicto é o que manda**, e é o mesmo que vai ser reportado: se não é `current` **e** `valid`, a reserva desfaz-se ali. Há sempre uma janela entre uma verificação e a linha seguinte; o que não pode haver é publicar depois de a ter visto fechada | `FinalizeUnderChange`: 2 testes novos; reposto o defeito, **2 acendem** |

O padrão dos dois é o mesmo, e vale a pena dizê-lo: **corrigi onde o defeito aparecia, não
onde ele nascia.** No P1 fui ao caso que o reporte mostrou (JSON corrompido) em vez de à
pergunta que o gera (*consigo situar este registo?*); no P2 tapei a janela que me apontaram
e deixei a seguinte aberta. Uma correcção que fecha o exemplo e não a classe volta com
outro exemplo — e voltou.

### 5.7 Segunda volta — os três primeiros

Os três foram **reproduzidos antes de corrigir**, e cada correcção tem regressão que
**falha quando o defeito é reposto** — verificado com o motor revertido, não presumido.

| # | defeito | porque passava | correcção | regressão |
|---:|---|---|---|---|
| **P1** | **falso verde por ficheiro corrompido.** Com a `v01` válida e a `v02` com JSON partido, a selecção escolhia a `v01` e devolvia `coverage: complete`, `eligible: true`, **saída 0** | o registo ilegível entrava como diagnóstico e mais nada: não mexia em `contract_validity` nem na elegibilidade. E o ponto é esse — **não se sabe a que etapa nem a que alvo pertence**, precisamente porque não se lê. Podia ser a revisão mais recente deste par, e escolher a anterior é escolher a que convém (T23/T24) | qualquer registo ilegível em `_coverage/` torna o resultado `invalid`, `coverage: not_evaluated` e `eligible: false` — **em todas as etapas**, porque não há como saber qual é a dele. A CLI sai **2**. Os ficheiros partidos vêm nomeados em `unreadable_records` e na razão | `Selection`: 2 testes novos; reposto o defeito, **2 acendem** |
| **P2** | **publicava uma revisão já desactualizada.** Alterando o desenho **durante** a operação, saía `published: true` com `freshness: stale` | a verificação de saída era uma comparação escrita à mão (`_basis_moved`) que só olhava para os três digests e para o manifesto. **O alvo não está no manifesto** — é um alvo (§6.3) — e as autoridades também não entravam. Era a segunda definição de «a base mudou», e divergiu da primeira, que é exactamente o que a D41 dizia para não fazer | a verificação de saída passa a ser a **mesma** da entrada: `finalize_recheck` sobre a base recalculada **e** sobre o alvo recalculado. `_basis_moved` foi apagado. Uma revisão publicada está actual, ponto | `FinalizeUnderChange`: 3 testes novos (alvo, fonte, e a propriedade dita de uma vez); reposto o defeito, **2 acendem** |
| **P3** | **o relatório de uma versão falava de outra.** Seis finalizações concorrentes publicaram `v01`…`v06` e **as seis** disseram `record.version: v06` | depois de publicar, `finalize` chamava `coverage_state(...)` sem dizer qual — e a selecção devolve *a mais recente da etapa*, que com concorrência é a da outra | `finalize` avalia **o registo que acabou de publicar**, passado por valor e por nome, com o nome de ficheiro para a verificação da §4.1. Cada `.md` nomeia a sua própria versão | `FinalizeUnderChange`: 2 testes novos; reposto o defeito, **2 acendem** |

Vale a pena dizer o que isto significa sobre a primeira volta: **os 110 testes desta fase
estavam verdes com estes três defeitos lá dentro**, e dois deles são falsos verdes — a
falha que este mecanismo inteiro existe para impedir. E os 117 da segunda volta estavam
verdes com os dois da §5.1. A lição é a mesma da fase 2, e agora
com um caso concreto: o P2 nasceu de eu ter escrito uma segunda comparação à mão **depois
de escrever a decisão que dizia para não a escrever** (D41). A regra estava certa; a
implementação não a seguiu, e nenhum teste meu perguntou se seguia.

### 5.8 Primeira volta

Seis, apanhados pelos testes desta fase, e todos com regressão que os prende.

| # | achado | onde nasceu | correcção |
|---:|---|---|---|
| **A9** | **um caminho de autoridade nunca era lido.** `safe_path` resolvia todo o caminho relativo contra o engagement, e `<engagement>/library/packs/pp/deliverable-templates/...` não existe. O registo de `render` declara o template por caminho relativo ao **repositório**, e o motor dava-o por ausente — logo o digest não batia certo, logo a revisão saía `stale` por uma razão falsa. Nenhum teste da fase 2 o apanhou porque as fixtures declaravam `authorities: []` e os testes de fronteira usavam caminhos **absolutos** | fase 2 | um caminho relativo passa a ter duas leituras, **por esta ordem**: o engagement primeiro, e só quando o ficheiro lá está; a autoridade depois, e só se cair dentro da lista fechada da §5.3. A fronteira não se alarga — `library/kernel/tools/` continua recusado. Contrato §5.3 acompanhou |
| **A10** | a guarda da árvore sintáctica da fase 2 acusava `read_draft` | fase 3 | a excepção é **uma** função, nomeada, com a razão escrita no motor e disciplina própria testada (`TheDraftDoor`, 5 testes): um rascunho é argumento explícito de uma operação explícita e vive fora do engagement por desenho; directório, ausente e não-JSON são três estados distintos e nenhum é «vazio» |
| **A11** | **uma obrigação perdida entre etapas tornava o registo `invalid`**, e a cobertura saía `not_evaluated` — o achado mais importante do mecanismo ficava com cara de erro de ficheiro | fase 3 | `_check_inheritance` e `_check_deliverable` devolvem **dois** veredictos: `structural` (erro de contrato: `based_on` que não resolve) e `review` (revisão incompleta: obrigação perdida, autoridade errada). Só o primeiro invalida. Contrato §4.4.4 acompanhou |
| **A12** | a regra dos `findings` era aplicada a revisões `pending`, acusando duas vezes a mesma pendência | fase 3 | `findings` passa a ser condição de **`completed`**. Contrato §4.7 acompanhou |
| **A13** | com `schema_version` desconhecido, o resultado reportava `source_review: incomplete` — uma leitura que o motor nunca fez | fase 3 | `unsupported` devolve `not_evaluated` em todas as outras dimensões. «Não sei ler isto» não é «li e falta-lhe coisa». Contrato §7 acompanhou |
| **A14** | `report --record <rascunho>` mostrava as obrigações do rascunho debaixo dos veredictos do registo **publicado** (ou de nenhum) | fase 3 | `coverage_state` aceita um registo dado e avalia-o. Pré-visualizar um rascunho antes de o publicar passa a ser uma operação honesta; 5 testes novos |

Duas saídas antecipadas de `validate_record` devolviam menos chaves do que a saída normal e
rebentavam no consumidor **exactamente no caminho de erro** — passaram a partilhar
`_no_verdict()`.

**O contrato acompanhou o motor em tudo isto**: o cabeçalho (o motor existe; os comandos
continuam por ligar), sete secções alteradas (§4.4.2, §4.4.4, §4.7, §5.3, §6.6, §7, §8.1) e
vinte e duas ambiguidades novas no registo da §11 (24–45) — as dezasseis últimas são os
defeitos das sete voltas de revisão, porque uma correcção no motor sem a regra escrita é meia correcção. *Motor e norma não
podem discordar em silêncio* — a regra da fase 2 vale aqui na mesma.

## 6. Decisões técnicas

**D33 — Os ids de requisito resolvem contra a Shared Understanding e as decisões, não contra
o inventário.** A §6.1 tira do inventário o registo de uma aprovação de blueprint; resolver
por lá faria de um id legítimo uma referência morta. A pergunta que `requirement_refs`
responde é *«este requisito existe como linha ou como decisão?»*, e é aí que se procura.

**D34 — Um `role` fora da sua etapa não tem código próprio.** `projection` num registo de
`blueprint` simplesmente não conta como âncora, e é `COV-MISSING-TARGET` que o apanha.
Inventar um segundo código para o mesmo facto faria dois achados de um, e o segundo
esconderia o primeiro — que é a proibição que a D15 já tinha escrito.

**D35 — `contract_validity` ganha `not_evaluated`.** Sem registo nenhum não há contrato de
ninguém para julgar; devolver `invalid` leria como «o registo está mau» quando não existe
registo. `invalid` fica para o registo que existe e não se lê, como a §6.6 manda.

**D36 — Erro de contrato é forma; revisão pobre é conteúdo, e não se misturam.** Um campo
ausente, um tipo errado ou um `based_on` que não resolve invalidam o registo. Uma obrigação
perdida, uma exclusão sem autoridade ou uma leitura por acabar deixam-no válido e legível, e
saem como lacuna. Confundi-los esconderia o achado (A11).

**D37 — A elegibilidade é por acção, e é aí que a severidade deixa de mandar.** Produzir um
desenho exige a reconciliação actual e **cada lacuna encaminhada** — `required_action` e
`responsible_role` preenchidos; não exige cobertura completa, porque «toda a perda
identificada foi encaminhada» é o que a §8.1 pede. Aprovar exige tudo isso **mais** cobertura
completa, leitura nos dois sentidos concluída e zero bloqueios estruturais. Uma versão com
lacunas continua a poder existir para discussão; o que ela não faz é anunciar-se pronta.

**D38 — A verificação estrutural entra no veredicto da etapa `blueprint`, e é chamada, não
reescrita.** `structural_check` invoca o `bp_validate` que já existe. Uma versão que falha a
estrutura não fica aprovável por ter cobertura, e o contrário também não: são duas perguntas,
e o resultado traz as duas. Isto não liga nada a comando nenhum — é o motor a responder o que
a §8.1.4 manda responder.

**D39 — `finalize` atribui a versão, e é a única coisa do rascunho que reescreve.** A
identidade de um registo é o seu ficheiro (§4.1), e o nome do ficheiro só se sabe na reserva.
Os digests, as disposições e os julgamentos saem intactos — reescrever qualquer um deles era
o defeito que esta fase existe para impedir.

**D40 — A reserva é exclusiva e repete-se; a versão publicada nunca se toca.**
`O_CREAT|O_EXCL`, e quando a concorrência ocupa a versão sobe-se para a seguinte. Um
`os.replace` sobre uma versão publicada não existe neste ficheiro, e há um teste de árvore
sintáctica a garanti-lo — procurar o texto não servia, porque o docstring diz a regra em
prosa.

**D41 — O recheck da finalização é `check_freshness`, de propósito.** Uma segunda comparação
escrita à mão seria uma segunda definição de «a base mudou», e mais cedo ou mais tarde as
duas divergiriam.

**D42 — O Markdown é projecção e diz que o é.** Cabeçalho explícito, nenhum `datetime.now()`,
e o mesmo estado dá o mesmo texto. Editá-lo não muda veredicto nenhum porque ninguém o lê —
`report` regenera-o a partir do JSON.

**D43 — `read_draft` é a única excepção à porta de leitura, e tem disciplina.** Um rascunho é
um argumento explícito de uma operação explícita e vive num temporário por desenho, onde
`safe_path` recusaria tudo. O que ela não faz é ler às cegas: ausente, directório, não-JSON e
JSON que não é objecto são estados distintos, e nenhum deles é «vazio» — a lição A2 da fase
2, aplicada de origem.

## 7. Comandos e resultados

```text
# engagement real -- leitura, e só leitura
python library/kernel/tools/coverage.py inventory --engagement projects/pricing-bunkers-v2
  1036 unidades · 16 classes · 0 limitações · completo · exit 0

python library/kernel/tools/coverage.py check --engagement projects/pricing-bunkers-v2 \
       --stage reconciliation
  contrato do registo        por avaliar (not_evaluated)
  actualidade da base        por avaliar (not_evaluated)
  revisão das fontes         por avaliar (not_evaluated)
  leitura nos dois sentidos  por avaliar (not_evaluated)
  cobertura                  por avaliar (not_evaluated)
  passo: produce_blueprint · pode avançar: não
  [COV-NO-REVIEW] não há revisão de cobertura para a etapa 'reconciliation'
  exit 4

integridade de `projects/pricing-bunkers-v2`, manifesto SHA-256 antes e depois:
  ficheiros: 76 -> 76   adicionados: []   removidos: []   alterados: []
  VEREDICTO: ENGAGEMENT INTACTO   (e continua sem `_coverage/`)
```

Suite completa, um ficheiro de cada vez, como `requirements-dev.txt` manda:

```text
37 ficheiros · 1800 testes
35 ficheiros OK
 2 ficheiros FAIL — os mesmos DOIS PRÉ-EXISTENTES de sempre:
   test_options_artefact.py::test_per_option_entries_stay_short
       (lê `projects/*/options.md`; exige alterar o engagement real, que está proibido)
   test_state_scaffold.py::test_a_pre_v23_su_still_exists_untouched
       (exige montar um engagement pré-v2.3, que não existe neste checkout)

E a mesma suite em discovery, para o caso de a forma de execução mudar alguma coisa:

python -m unittest discover -s .claude/tests -p "test_*.py"
  Ran 1800 tests · FAILED (failures=2, skipped=6)   — as mesmas duas, e mais nenhuma
```

Os módulos de cobertura: **64 + 86 + 50 + 101 + 53 = 354 testes**, todos verdes. Os 154
novos são desta fase.

Os mesmos 354 correm também **em discovery** (`python -m unittest discover -s .claude/tests
-p "test_coverage*.py"`), verdes, porque a lição R11 da fase 1 é que um módulo que muda de
comportamento com a forma de execução não está testado.

**Prova negativa das dezassete guardas** — reposta cada uma no motor, quantos testes acendem:

```text
P1   registo ilegível deixa de bloquear         6 falha(s) em 14 testes
P1b  filtrar por etapa antes de situar          5 falha(s) em 14 testes
P1c  identidade sem cruzar com o ficheiro       1 falha(s) em 14 testes
P1c2 o registo mentiroso volta a situar-se      1 falha(s) em 14 testes
P1d  destino noutra versão prova cobertura      2 falha(s) em  4 testes
P2   a verificação de saída deixa de ver o alvo 2 falha(s) em  7 testes
P2b  o veredicto final deixa de desfazer        2 falha(s) em  7 testes
P2c  tipo errado volta a rebentar              20 falha(s) em  3 testes
P2d  montante deixa de ser avaliado             4 falha(s) em  9 testes
P2d2 a cadeia volta a aceitar ciclos            1 falha(s) em  9 testes
P3   a finalização volta a ler «o mais recente» 2 falha(s) em  7 testes
P2e  o erro de montante volta a ser engolido    1 falha(s) em  9 testes
R1   ligações mortas deixam de ser referências   1 falha(s) em 12 testes
R4   coverage[] vazio volta a passar            1 falha(s) em 12 testes
R7   obrigações voltam a desaparecer entre versões 4 falha(s) em 12 testes
R7b  comparar só com a versão imediatamente anterior 2 falha(s) em 12 testes
R8   achados impeditivos deixam de bloquear     2 falha(s) em 12 testes
motor restaurado: True
```

O `P1c` acende **um** teste, e há uma razão escrita para isso: com o registo mentiroso já
bloqueado por não se conseguir situar, o cruzamento do ficheiro só se distingue quando o
nome do alvo não deixa derivar uma versão (`ux-blueprint-final.yaml`). Foi preciso escrever
esse caso de propósito para a guarda ficar presa por um teste seu — uma guarda redundante
sem regressão própria é uma guarda que alguém apaga amanhã sem nada acender.

**Sobre o modo de execução da suite.** O `requirements-dev.txt` deste repositório declara o
modo, e não é discovery:

```bash
for f in .claude/tests/test_*.py; do python "$f" || exit 1; done
```

E declara também a razão, que vem de uma revisão anterior: *«could not run the full suite
because PyYAML was missing, and "inconclusive" was read as "green" (P-15)»*. Uma execução
sem `PyYAML>=6.0` e `openpyxl>=3.1` instalados **não valida nada** — nem a favor, nem
contra. Os números acima são de um ambiente com as duas dependências presentes
(PyYAML 6.0.3), e quem os quiser reproduzir precisa do mesmo.

Confirmação da §15.6 do plano: `grep -Ei "C-014|BIOS|SharePoint|pricing-bunkers|marinha"`
sobre o motor e sobre os testes novos não devolve nada. **Nenhum identificador do caso real
entrou no código**, e a fixture é sintética por construção.

## 8. Critérios de saída

| critério do plano | estado |
|---|---|
| verificação standalone funciona do inventário ao diagnóstico | **cumprido** — 13 códigos ligados, 20 registos exercitados |
| registo incompleto nunca produz falso verde | **cumprido** — unidade omitida, obrigação perdida, destino decorativo, exclusão sem autoridade, materialidade por declarar, `covered` com pendências, fonte sem extractor, registo corrompido ou que não se situa ao lado de um válido, **e a etiqueta de versão trocada** (P1c): dez maneiras de tentar, dez recusas |
| tipo errado nunca produz falha interna | **cumprido** — 22 formas no registo (P2c) e o argumento da API (§5.1), todas com saída 2 e JSON |
| uma revisão nunca vale mais do que a cadeia em que assenta | **cumprido** — montante avaliado com o mesmo motor; ciclos mortos por construção (P2d); falha a avaliar montante é impeditiva e nomeada (P2e) |
| obrigações não desaparecem em silêncio | **cumprido** pela forma — nem todas de uma vez (R4), nem entre versões (R7), nem largando as ligações do próprio revisor (R1). **Não cumprido por semântica**, e não pode ser: quais unidades geram obrigações é do revisor (§9, limitação 11) |
| `finalize` não sobrescreve nem escreve SU/decisões | **cumprido** — reserva exclusiva, versão ocupada intacta byte a byte, manifesto fora de `_coverage/` idêntico |
| relatório derivado do JSON | **cumprido** — determinístico, e editá-lo não muda veredicto (T40) |
| fontes alteradas durante a revisão impedem a finalização | **cumprido** — três fechos (§3.3), a mesma comparação à entrada e à saída, e os digests do rascunho nunca são reescritos |
| ausência de revisão em engagement real produz `not_evaluated` | **cumprido** — verificado contra `pricing-bunkers-v2`, em leitura |
| não activar condições novas nos comandos | **cumprido** — zero ficheiros de comando, skill ou hook alterados |
| testes prioritários T01–T04, T11–T15, T21–T24, T29–T30, T37–T40 | **cumpridos** — ver §3 e a tabela de §3.2 |

## 9. Limitações

1. **Nada disto está ligado.** Nenhum comando chama o motor; a prontidão que a §8.1 define
   não bloqueia aprovação nenhuma hoje, porque nada a consulta. Fase 4.
2. **A cobertura do engagement real continua por avaliar.** O que existe é o denominador
   (1036 unidades) e o veredicto `not_evaluated`. Ninguém reviu nada, e este relatório não
   diz o contrário.
3. **A compreensão semântica não é provada por código, e não passa a ser.** Um revisor que
   minta no `role` de um destino só é apanhado quando o nó não existe. A §9 do contrato
   continua a ser uma declaração do agente, com autor e método, e é isso que o motor
   verifica: a forma da declaração, nunca a verdade dela.
4. **A etapa `render` está implementada e não está exercitada a sério.** Os três registos de
   render da fixture passam, mas a selecção de versão por deliverable, os slots e a
   suficiência são trabalho da fase 5 — o que existe aqui é a verificação de autoridade
   (§8.3) e a subtracção declarada (§4.4.4).
5. **O teste de snapshot do blueprint continua a saltar** (§4). A pergunta do F16 está
   fechada por prova; a lista justificada do snapshot continua por confirmar contra os
   ficheiros reais, e só um checkout com esses engagements o pode fazer.
6. **Os registos das fixtures continuam com os placeholders nos três digests derivados**, e
   hidratam em tempo de teste. Reescrevê-los com digests reais continua a ser opção, não
   necessidade: `finalize` já os produz, mas congelá-los nas fixtures torna-as frágeis à
   primeira regeneração dos workbooks.
7. **A política de atualidade continua conservadora** (§6.3 do contrato): uma mudança de
   formatação numa fonte torna a revisão `stale`. É deliberado, e o motor mostra sempre qual
   foi a diferença.
8. **Duas falhas pré-existentes na suite**, nenhuma corrigida, ambas pelas razões de sempre.
9. **Os treze defeitos das sete voltas vieram de revisão externa, não dos meus testes**
   (§5.1–§5.7). **Nove eram falsos verdes**, e três deles sobreviveram a uma correcção
   minha. A suite desta fase esteve verde em sete estados diferentes do motor, e em seis
   deles havia um falso verde lá dentro.
11. **O motor não sabe quais unidades geram obrigações, e não passa a saber.** Na fixture,
   35 unidades de SU, respostas e enquadramento estão `reviewed`/`material` e só 7 são
   obrigações — escolha do revisor (§9). O esvaziamento **parcial** de uma primeira
   reconciliação, sem versão anterior com que comparar, continua a não ser detectável pela
   forma; só a revisão semântica o apanha. O que a forma garante é que a escolha, uma vez
   escrita, não se desfaz em silêncio (R1, R4, R7). A fase 4 deve pedir ao executor que
   preencha `links.coverage_items` em cada entrada material — é a ferramenta que o contrato
   já lhe dá para tornar a sua própria escolha verificável. O padrão que os liga está escrito na §5.1 e na
   §5.3: cada verificação confirmava a sua parte e nenhuma cruzava as duas — identidade sem
   ficheiro, destino sem versão, herança sem montante. **Um invariante que só se verifica
   por partes não está verificado.** Os testes que agora os prendem foram escritos depois, e
   nenhum número deste relatório deve ser lido como estável antes de a fase 6 correr a
   validação integrada.
10. **Nada foi commitado nem publicado.**

## 10. Dependências concretas para a fase 4

1. Chamar o motor a partir de `/blueprint` (pré-produção e pós-produção), de `/answer` e de
   `/capture` (revalidação), e de `/status` (`status.coverage`), com **chamadas explícitas** —
   sem booleano de verdade em `_state.json`, porque o estado deriva dos registos e das fontes.
2. Actualizar `blueprint-contract.md`, `phases.md` e `orchestration.md` para a condição de
   **nova** aprovação da §8.1, **no mesmo incremento** em que a regra ficar activa. O
   significado de `draft` não muda, e aprovações históricas não se revogam (§10 do contrato).
3. Expor no `/status` as quatro perguntas separadas — estrutura, cobertura, aprovação,
   ponta-a-ponta — em linguagem de negócio, pela coluna *Como se diz ao utilizador* do
   glossário. O motor fala kernel; o utilizador não tem de o aprender.
4. Ligar o feedback ao hook de blueprint e aos triggers de `_coverage/` (`on-su-change.py`
   não observa essa pasta hoje — achado do baseline da fase 1), garantindo que **observar o
   estado não gera ciclos de escrita**.
5. Testar o legacy: engagement sem `_coverage/` e **com** aprovação histórica →
   `not_evaluated` e aprovação preservada (T35); hooks que não dispararam → os checks
   explícitos continuam disponíveis e documentados (T25).
6. Não tocar na selecção nem na projecção dos deliverables: isso é a fase 5.

## 11. O que esta fase explicitamente não declara

Nenhuma pergunta em aberto do engagement real foi respondida — `U-028` e `U-030` continuam
abertas. Nenhuma aprovação foi registada em nome de ninguém. O blueprint real **não** está
aprovado, **não** está completo e **não** está validado ponta-a-ponta. A cobertura do
engagement real **não foi avaliada**: o que ele devolve é `not_evaluated`, e `not_evaluated`
não é aprovação nem reprovação. O E2E demonstrado nesta fase é o do **protocolo**, numa
fixture sintética — nunca o da solução de negócio.
