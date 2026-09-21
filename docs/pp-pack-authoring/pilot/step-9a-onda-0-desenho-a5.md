# Step 9A (cont.) — Onda 0, frente D — desenho de A5 `fields[]` / `access_contract` em papel

> Não é código, não é edição do kernel, não é re-render. É o item da **onda 0** que o plano reserva à frente D
> (`docs/CONSOLIDATED_PLAN.md` §5 → *«Desenho de A5 em papel, contra as 7 entidades de pilot-1 e as listas de
> dpt-galp-jp»*): fixar a **forma** que a spec §4/§6/§8 e a estimativa consomem **antes** de existir
> `fields_draft.py`. Regra do plano: *«se se saltar o desenho, o motor codifica uma forma que a spec depois não consome»*.
> Julgamento em Fable 5.1; contagens só pelo L1 (`*.extraction.json`), nunca à mão.

**Veredicto: `ONDA 0 (FRENTE D) — DESENHO DE A5 CONCLUÍDO — 12 DECISÕES DE FORMA, 7 DOMÍNIOS + 2 LISTAS MAPEADOS,
6 EMENDAS AO PLANO APLICADAS, 6 DECISÕES DO DONO FECHADAS (§11), NADA ESCRITO FORA DE docs/`.**

Os números que mudam o desenho: em pilot-1 as **291 named ranges** são o dicionário, mas apontam para **83 colunas**
(69 com 3 aliases cada) e **76 delas para colunas sem dados**; `Inputs` tem **8 colunas sem nome** e `Outputs` tem
**4 cabeçalhos em 76 colunas** — o motor não pode fazer `header → name`, tem de fazer `named range → formula ref → header → sem nome`.
Dos 7 domínios de `record_authority[]`, **6 são externos e 1 é `owned` com autoridade em aberto** (U-040), não «7 externos».
E o `schema_owner` que o plano manda ler de `A-001` não está lá: `A-001` é a corrupção do Excel; a âncora certa é `C-057` + `U-036` (aberta).

---

## 1. Base

| | |
|---|---|
| Branch / HEAD | `pp-pack-authoring/step-2-discovery-layer` · `0a7299f` (frente C fechada) · frente E em curso, não committed |
| Leu | `CONSOLIDATED_PLAN.md` (P-5, P-6, P-7, P-10, P-18 F04/F08, §2, §5) · `library/packs/pp/architecture-templates/architecture-core.md` (A5) · `step-9d-frente-b-estimativa.md` §1.2 · `blueprint-contract.md` · `aisa-blueprint/SKILL.md` step 2 (esquema actual de `record_authority[]`) · `implementation-spec.template.md` e `estimate.template.md` (frontmatter completo) · `render-contract.md` · `states.md` (limiar P-12) · `xlsx_extract.py` (`classify_columns`, `is_key_like`, `reads`) · `render-validate.py` (stub, 39 linhas) · testes `test_pp_deliverable_templates.py` (restrições a `slot_sources`) |
| `scratchpad/p18-design.md` | **não existe** neste scratchpad nem no repo — P-18 F04/F08 tratados aqui só na medida em que tocam A5 (§9) |
| Engagements medidos | `projects/pricing-marinha-pilot-1` — blueprint `v05` **aprovado** (`D-004`), `v06` **não aprovado** (4 escolhas estruturais abertas), L1 `PREÇO BANCAS_30_01_26.xlsx.extraction.json` (xlsx_extract 1.1.0) · `projects/dpt-galp-jp` — sem `_blueprint/`, spec `v01` pré-contrato, L1 `Dayly_pending_tickets_Anonimo.xlsx.extraction.json` |
| Escreveu | este ficheiro · nota de estado na memória do projecto |
| **Não tocou** | `library/` · `.claude/` · qualquer `projects/*` · `CONSOLIDATED_PLAN.md` (as emendas propostas ficam em §10 para o dono aplicar) |

---

## 2. Factos que condicionam a forma (medidos)

### 2.1 pilot-1 — o L1 contra os 7 domínios

| Facto | Medida (L1) | Consequência no desenho |
|---|---|---|
| O dicionário são as named ranges, não os cabeçalhos | 291 named ranges (**145** pares nome→alvo distintos — o mesmo nome repete-se por scope) · 266 ocorrências apontam para `Inputs` · **83 colunas** cobertas · máx. **2 aliases** reais por coluna · `Inputs` `header_row=1119` por `frozen-pane` (valores, não nomes — `C-017`) | `name` resolve-se por prioridade `named_range → formula_ref → header → none`; itens de `reads[]/writes[]` são **por coluna**, com `aliases[]`; nunca por named range |
| Entradas de dicionário sem dados | **42** entradas distintas apontam para colunas **não populadas** (36 `CustosLogísticos_*`, 5 `Index_*`, 1 `SEACARRIER_*`); 76 ocorrências brutas com repetições — o motor `fields_draft.py` 0.1.0 conta distintas | o contrato distingue *coluna com dados* de *entrada de dicionário sem dados*; as segundas não entram em `writes[]`, entram em `dictionary_entries_without_data[]` (`Unknown`: mortas ou reservadas) |
| Colunas sem nome em `Inputs` | 8: `F` (derived), `H`, `Y`, `Z`, `AA`, `AB`, `AL`, `CX` (manual) | `name: Inputs!<col>` · `name_basis: none` · `state: Unknown` — nunca inventado |
| `Outputs` quase sem cabeçalhos | 76 colunas · **4** com header · 59 `derived` · 17 `manual` · 82 padrões referenciam `Data_Lista` | para o domínio de saída, o nome vem da **linhagem** (`Index_<X>_Preço` → coluna «X — Preço»); `computed: true` + `lineage[]` |
| Chave de linha universal | `Data_Lista = Inputs!$B$9:$B$1469` (125 colunas partilham o intervalo 9–1469 ≈ 4 anos diários) | `key: [data]` em RA-2/RA-3/RA-4/RA-5; `grain.row = 1 dia`; `volume.rows ≈ 1 linha/dia` (driver de P-10) |
| Distribuição das 91 colunas populadas de `Inputs` por domínio × classe | KEY 1 · **RA-2** custos 22 + margens 7 + transporte 9 = **38 manual** · **RA-3** cotações/índices 22 manual + 5 derived, prémios/cedências por contraparte 17 manual = **39 manual + 5 derived** · sem nome 7 manual + 1 derived | os números de aceitação de §8 |
| Dimensões do dicionário (`<dim1>_<dim2>_<dim3>`) | sobre os nomes que apontam para uma coluna: dim1 **10** valores (7 contrapartes + `Index`, `PreçosSpot`, `CustosLogísticos`) · dim2 **22** combustíveis · dim3 **46** (métricas **e** portos misturados) — reproduzido pelo motor `fields_draft.py` 0.1.0 (124 nomes de 3 segmentos; `DF_GRID_1`, partido, não conta) | o motor emite `dimensions[]` com cardinalidade; a **separação** métrica/porto e contraparte/prefixo-técnico é julgamento da skill, não do motor |
| Clones de `Outputs` | `usd_ton` assinatura (coluna, classe) **idêntica** a `Outputs` (PM-003 confirmado por classe); `Simulador` difere (20 manual vs 17) | RA-4: **uma** vista parametrizada por unidade (`C-071`), não 4 contratos; `Simulador` não tem domínio (ver §5, `ProjecaoCenario`) |
| Linhagem entre folhas | `Outputs` lê `Inputs` + `BIOS`; `Base DFA`/`Base RF` lêem **`Outputs`** (não o contrário); `Outputs BIOS` lê `Base DFA`/`Base RF`/`Outputs` | confirma `C-076`; RA-4 BIOS é condicional (`U-033`) e a jusante do preço base |
| Feed de mercado | `Market View` 5 colunas (ECB USD/EUR + 4 Platts) · `UlyssesQuotes` 10 colunas com ids `model://…` · 5 derived de `Inputs` (`I`,`L`,`O`,`R`,`AC`) fazem lookup ao `Market View` | RA-3 `reads[]` do feed: 15 séries nomeadas pelo id do fornecedor; `by: feed` — é o «feed já na BD» de `C-057` |
| Listas de valores | `Outputs!AF14` `"USD,EUR"` · `AG14` `"TM,M3"` · `APOIO!D` `usd/mt, usd/cbm, eur/mt, eur/cbm` · `APOIO!F` portos (`key_like`) | tabelas de dimensão de RA-1 com `values[]` determinísticos e locator |
| Domínios vs entidades do blueprint | `record_authority[]` **7** · `entities[]` **10** · `ProjecaoCenario` e `Simulador` **sem domínio** · v02–v05 tinham **4** domínios (spec `v02` sobre-afirmou 2 — step-9d §1.2) | precisa-se de uma junção explícita `entities[].authority → record_authority[].key`; entidade sem domínio = **lacuna**, não analogia |
| Versão aprovada não parseia | `ux-blueprint_v05.yaml` (aprovado, `D-004`) falha `yaml.safe_load` em `irreversible_choices`; `dashboard.py` já lê com walker tolerante | **nenhum motor escreve no YAML do blueprint**; o rascunho vive em `_capture/`, a skill copia |

### 2.2 dpt-galp-jp — o L1 contra as listas de v01

| Facto | Medida (L1) | Consequência |
|---|---|---|
| Registo manual | `Priority_Store` 8 colunas: 7 `manual` + 1 `derived` (`Live Status`); `Ticket ID` e `Description` `key_like`; validação `E3:E301` = `"High,Medium,Low"` | `Prioridade: choice [High, Medium, Low]` sai **determinístico** do L1; `Exec. Order` `nulls 52/89` → `required: false` determinístico |
| Extracção da origem | `Dayly_extraction` 19 colunas: 14 `input` + **5 vazias** (`Data de Conclusão`, `VIP`, `Projecto`, `Project Name`, `Focal Point Midrange`); `_closed` idem com `Data de Conclusão` **157/157 populada** | uma coluna vazia é `type: unknown · evidence: header only`, nunca omitida; `Data de Conclusão` existe nos fechados e **v01 não a tem** — o rascunho apanha o que v01 perdeu |
| Vista | `Prioritized_View` 10 `derived` | folha-relatório → `reads[]` do consumidor, não campos novos |
| v01 | lista *Priority Decisions* **18** campos · *Audit Log* **7** campos · sem `_blueprint/` | aceitação por **cobertura de fonte** (§8.2), não por re-render — não há blueprint que o `/render` leia |

---

## 3. Decisões de forma (D1–D12)

| # | Decisão | Porquê |
|---|---|---|
| **D1** | A5 vive em `architecture.record_authority[]` do blueprint (o *architecture record* já é o bloco `architecture:` — `slot_sources.architecture_block`). Cada entrada ganha **`key`** (slug, único no scope, mesma regra de unicidade de `compositions[].component`). `entities[]` perde `fields_itemized` e ganha **`authority: <key>`** (ou `authority: none — <razão>` explícito) | é a junção que P-7 exige: ecrã → entidade → domínio → campos. Sem ela a suficiência não é verificável por máquina |
| **D2** | Dois sub-blocos **exclusivos por `access_mode`**: `owned` → `fields[]`; `keep-in-place` \| `virtualized` → `access_contract`; `replicated` → `access_contract` **obrigatório** + `fields[]` opcional derivado 1:1 de `reads[]` (a réplica não tem campos que a origem não tem) | plano §2 (*«fields[] para autoridade interna; access_contract para keep-in-place/virtualized»*); `replicated` não estava coberto |
| **D3** | **Estado epistémico por linha**: cada item de `fields[]`, `reads[]`, `writes[]`, `key[]` carrega `state: Assumed \| Confirmed \| Unknown` + `source` (locator P-12). Saída do motor = `Assumed` com `source: _capture/<ficheiro>.fields-draft.json#<folha>/<coluna>`; `Confirmed` só por `answers.md#…` do dono ou locator de classe 1 | P-6 (*«Assumed por linha; a skill julga, o sponsor confirma»*) + P-12 (limiar). Nenhum estado novo |
| **D4** | O motor `fields_draft.py` escreve **`_capture/<ficheiro>.fields-draft.json`** (artefacto do capture, determinístico, cabeçalho com `tool`, `version`, `source_sha256`). **Nunca** escreve no YAML do blueprint | locator de classe 1 (`states.md` regra 1); o YAML é de autoria LLM, versionado *never overwrite*, e o `v05` aprovado nem parseia |
| **D5** | O rascunho é **consumido em `/blueprint` step 2** (quando `record_authority[]` é autorado) e em `--refresh`. Não em `/decide` (não há registo ainda) nem por `/synthesize` (é *carrier*, `aisa-synthesize` I-1). O motor corre **dentro de `aisa-blueprint`**, idempotente por `source_sha256`; não corre no `/capture` do `/start`, para não abrir superfície de campos em Discovery (P-5: *«Campos — não é Discovery»*) | desvio ao texto de P-5/P-6 (*«aisa-decide/aisa-synthesize invocam o motor»*) — ver §10 |
| **D6** | **Resolução do nome**: `name_basis ∈ {named_range, formula_ref, header, none}`, nessa prioridade. Header só conta se não for número nem data. `none` → `name: <folha>!<coluna>` + `state: Unknown` | `C-017` (Inputs) e `Outputs` 4/76 cabeçalhos. `header → name` do plano falha em 2 das 3 folhas materiais de pilot-1 |
| **D7** | **Vocabulário de tipos** do registo (neutro de pack): `text \| number \| date \| datetime \| boolean \| choice \| reference \| identifier \| unknown`. Mapa L1: `str→text` · `number→number` · `datetime→datetime` · `bool→boolean` · `mixed(…)→unknown` + `rule: tipos mistos na origem` · `empty→unknown` + `evidence: header only` · `str` com validação `list` na coluna → `choice` com `values[]` de `formula1` · `key_like → identifier` + `index: candidate`. `required` = `nulls == 0` sobre a gama de dados → `required: true (draft)`; senão `false`. **`default` nunca inferido de `top_values`** | um valor frequente não é um default; `mixed` é sinal, não tipo. Tipos de plataforma (Choice SP, Dataverse OptionSet) são projecção do render, não do registo |
| **D8** | **Mapa de classes**: `manual`/`input` numa folha-registo → `writes[]` (alguém digita); `derived` → `reads[]` do consumidor **ou**, no domínio de saída, coluna `computed: true` com `lineage[]` (refs nomeadas do padrão de fórmula); `empty` com nome → `dictionary_entries_without_data[]`. A **folha** classifica-se pelo `process-model.md` §1 (`register`/`report`/`input`/`reference`), não pelo motor | o motor carrega factos, a skill o julgamento (`feedback-motor-carries-facts`) |
| **D9** | `schema_owner` é **valor com estado**: `{value, state, su_ref, open: U-nnn?}`. pilot-1: `Assumed — equipa que opera a BD partilhada (C-057); autoridade de mudança do schema em aberto (U-036)` | o plano cita `A-001` — errado (`A-001` = corrupção do Excel). `U-036` está aberta; escrever «equipa da BD» como facto seria `Confirmed` acima da evidência (P-12) |
| **D10** | **Sem números de serviço em A5** (render contract regra 6): `delegation_safe_paths[]` lista caminhos; tectos (1 000 registos, paging) citam a unidade de DK + linha SU verificada, nunca o literal | `dataverse.md §14`, `query-and-delegation.md §4` são a autoridade; o registo cita |
| **D11** | **Forma de lacuna em §4** (step-9d §1.2 achado 2): entidade sem `authority` ou domínio sem `fields[]`/`reads[]` renderiza linha `⚠️ lacuna — <o que falta> — dono — o que resolveria` **e** entrada em `render-gaps.md`; nunca célula *Notas* «ver §16», nunca analogia com a vizinha | a sobre-afirmação de `v02` (`PrecoDiarioConsolidado`, `AprovacaoCarregamento` como `keep-in-place` sem domínio) deixa de ser possível por construção |
| **D12** | **Disposição por coluna do rascunho** — reutiliza o vocabulário do princípio 10: `ADOPT` (vira campo/`reads`/`writes`), `MAP` (alias de campo já adoptado), `DISMISS — <razão>` (fora do to-be). Todas as colunas do L1 têm disposição no registo; nenhuma cai em silêncio | `orchestration.md` → *Comprehension survival* (*«não pode ser silenciosamente promovido ou descartado»*); dpt-galp-jp v01 descartou `Serviço`, `Origem`, `Data de Conclusão` sem dizer |

---

## 4. Forma de A5 — esquema

Substitui o bloco `record_authority:` do esquema em `aisa-blueprint/SKILL.md` step 2. Campos existentes mantêm-se; o que é novo está marcado `# NOVO`.

```yaml
record_authority:                       # 0..N — vazio SÓ com racionalização afirmativa (inalterado)
  - key: <slug único no scope>           # NOVO — junção com entities[].authority
    domain: <nome de negócio do domínio>
    authority: <governed relational store | list/library store | relational via connector | external system of record>
    access_mode: owned | virtualized | replicated | keep-in-place
    su_refs: [...]
    grain: {row: <o que é uma linha>, dims: [<dimensões>]}          # NOVO — o que define uma linha
    volume: {rows: <n · unidade>, cadence: <diária|mensal|evento>, state, source}   # NOVO — driver de P-10, com locator
    schema_owner: {value, state: Assumed|Confirmed|Unknown, su_ref, open: U-nnn}   # NOVO — D9

    # ── exclusivo: access_mode == owned ──────────────────────────────────────────
    fields:                                                          # NOVO — D2
      - name: <nome>
        name_basis: named_range | formula_ref | header | none | design   # D6; `design` = campo criado pela arquitectura, não pelo L1
        type: text|number|date|datetime|boolean|choice|reference|identifier|unknown   # D7
        values: [...]                     # só para choice; de validação L1 ou declaração do dono
        required: true|false
        default: <valor> | null           # nunca inferido
        index: primary | candidate | none
        set_by: [<papel | transição | processo>]     # consumido por §6/§8
        rules: [<regra de validação, com locator>]   # de L1 validations ou de A7/decisão
        computed: true|false
        lineage: [<refs>]                 # se computed
        state: Assumed|Confirmed|Unknown  # D3
        source: <locator P-12>            # _capture/…fields-draft.json#<folha>/<col> | answers.md#… | design (A7 audit)
        disposition: ADOPT|MAP|DISMISS    # D12 — MAP carrega `maps_to`; DISMISS carrega `reason`

    # ── exclusivo: access_mode in {keep-in-place, virtualized, replicated} ───────
    access_contract:                                                 # NOVO — D2
      reads:                              # colunas que a aplicação LÊ da autoridade externa
        - name, aliases: [...], name_basis, type, computed, lineage, by: [<papel|processo|feed>], state, source, disposition
      writes:                             # colunas que a aplicação ESCREVE na autoridade externa; [] afirmativo com readonly: true
        - name, aliases: [...], type, by: [<papel|processo>], cadence, write_semantics: insert|update|upsert|append, rules: [...], state, source, disposition
      readonly: true|false                # true ⇒ writes: [] é afirmativo, não lacuna
      key: [<coluna(s) de junção/identidade da linha>]               # obrigatório; nunca vazio sem `open: U-nnn`
      join_keys: [<pares domínio.coluna ↔ domínio.coluna>]
      dictionary_entries_without_data: [<nomes>]                     # §2.1 — Unknown: mortas ou reservadas
      delegation_safe_paths: [<filtro/ordenação que o mecanismo delega — cita DK, sem números>]   # D10
      mandatory_filters: [<coluna>]       # ex.: data — onde a DK exige filtro positivo
      store_facts:                        # o que o fit do mecanismo precisa saber da origem (U-036) — cada um com estado
        primary_key_type: {value, state, su_ref}
        primary_name_column: {value, state, su_ref}
        server_side_triggers: {value, state, su_ref}
        connection_identity: {value, state, su_ref}
      confidentiality: {row_level: {value, state, su_ref}, column_level: {value, state, su_ref}}   # U-037 → §8
      forfeits: [<o que o access_mode abdica — cita a unidade DK>]   # A5 «forfeits» já exigido, agora estruturado
```

`entities[]` do blueprint:

```yaml
entities:
  - name: <PascalCase>
    label: <negócio>
    authority: <record_authority[].key> | none — <razão>       # NOVO — substitui fields_itemized
    su_refs: [...]
    state_machine: [...]        # inalterado
    approval: true|false        # inalterado
    readonly / provisional / external / owned_here   # inalterados
```

**Regras de integridade** (para `render-validate.py`, P-7, e para o hook de blueprint se existir):

1. `key` único por scope; `entities[].authority` resolve para um `key` existente ou é `none — <razão>` explícito.
2. `owned` ⇒ `fields` presente e `access_contract` ausente; externo ⇒ o inverso; `replicated` ⇒ ambos, com `fields ⊆ reads` por nome.
3. Toda a linha de `fields`/`reads`/`writes` tem `state` **e** `source`; `Confirmed` exige locator de classe 1 (`states.md`).
4. `writes: []` só com `readonly: true`; `key: []` só com `open: U-nnn`.
5. Nenhum literal numérico de limite de serviço em `delegation_safe_paths`/`mandatory_filters`.

---

## 5. pilot-1 — os 7 domínios contra o L1

Junção proposta `entities[].authority` (v06, 10 entidades → 7 chaves):

| Entidade (v06) | `authority` | Nota |
|---|---|---|
| `DadosMestrePricing` | `master-data` | `state_machine` proposta→aprovada→activa é **workflow**, vive em `workflow-audit`; os dados vivem aqui |
| `CustosLogisticos` · `MargensAlvo` | `costs-margins` | um domínio, duas entidades (cadências distintas) |
| `InputsDiarios` | `daily-quotes` | |
| `PrecoDiarioConsolidado` | `daily-price` | `readonly`, `feeds_output` |
| `HistoricoPrecos` | `price-history` | |
| `AprovacaoCarregamento` · `JournalAuditoria` | `workflow-audit` | autoridade **OPEN** (U-040) |
| `TermosComerciaisCliente` | `sap-terms` | |
| **`ProjecaoCenario`** | **`scenarios`** — domínio `owned` **novo** (decisão do dono 2026-09-09: cenários gravados) | a junção expôs a entidade sem domínio; fecha-se com um 8.º domínio: `fields[]` 100 % `design` {id, data_base, autor, criado_em, inputs alterados (JSON/linhas filhas), margem de teste, resultado por produto×unidade, `estado choice [rascunho, revisto, descartado]`}; `Simulador` do Excel é clone de `Outputs`, não autoridade — `DISMISS — vista` |

| `key` | `access_mode` · `authority` | `grain` / `volume` (L1) | `reads[]` (L1 → contrato) | `writes[]` | `key[]` / `store_facts` | `schema_owner` |
|---|---|---|---|---|---|---|
| `master-data` | `keep-in-place` · SQL partilhado | linha = par (dimensão, valor); volume = 10 + 22 + 46 valores de dimensão + portos `APOIO!F` + unidades `APOIO!D`/`Outputs!AF14,AG14` | 4–5 tabelas de dimensão com `values[]`: **contraparte** (7 de dim1 — `Index`/`PreçosSpot`/`CustosLogísticos` são prefixos técnicos, `DISMISS`), **combustível** (22), **métrica** (subconjunto de dim3), **porto** (dim3 ∩ `APOIO!F`), **unidade** (4); `by: [Analista, Comité]` | alterações ao dicionário (`insert`/`update` de valores de dimensão), `by: [Dono de dados-mestre]`, `rules: [aprovação formal (C-058)]`, `cadence: evento` | `key: [dimensão, valor]`; `dictionary_entries_without_data: 76` | `Assumed` — C-057; `open: U-036` |
| `costs-margins` | `keep-in-place` · SQL partilhado | linha = dia (`Data_Lista`) × (contraparte, combustível, métrica/porto); ≈ 1 linha/dia · 38 valores | os mesmos 38 (motor lê) + `key` | **38** colunas `manual` no L1: 22 `CustosLogísticos_*` (`cadence: mensal`, C-016) · 7 `Margem/Desconto*` + 9 `Transporte*` (`cadence: diária`, C-002/C-025) — das 16 diárias, **12** são `AçoreanaMutualista_*` → `DISMISS` (C-052), ficam **26**; `by: [Analista]`, `write_semantics: upsert` por data | `key: [data]` + dims; `store_facts.*: Unknown (U-036)` | idem |
| `daily-quotes` | `keep-in-place` · SQL partilhado (feed incluído, C-057) | linha = dia; ≈ 85 valores/dia (PM-001); ≈ 4 anos de histórico (linhas 9–1469) | **feed**: 5 séries `Market View` + 10 séries `UlyssesQuotes` (`by: [feed]`, nome = id do fornecedor) · 5 `derived` de `Inputs` (`I`,`L`,`O`,`R`,`AC`) como `computed` com `lineage → Market View` | **39** colunas `manual`: 22 cotações/índices + 17 prémios/cedências por contraparte (`by: [Analista]`, `cadence: diária`, `rules: [valor estimado 2ª/3ª marcado — C-074]`) · **7 colunas sem nome** (`H`,`Y`,`Z`,`AA`,`AB`,`AL`,`CX`) como `state: Unknown` | `key: [data]`; `mandatory_filters: [data]` | idem |
| `daily-price` | `keep-in-place` · SQL — **calculado pelo motor** (`pricing-calculation-engine`) | linha = dia × unidade (4, C-071) × produto; 59 colunas calculadas | **59** `computed` com `lineage[]` (82 padrões via `Data_Lista`; refs `Index_*`, `CustosLogísticos_*` via `INDIRECT`, `PreçosSpot_*`); nome por `formula_ref`; BIOS: **15** `computed` de `Outputs BIOS`, `disposition: ADOPT` **condicional a U-033** | `[]`, `readonly: true` — **excepto** a pergunta que os 17 `manual` de `Outputs` levantam (overrides tipados sobre fórmulas): `Unknown` *«o to-be admite override manual do preço calculado?»* | `key: [data, unidade, produto]`; `delegation_safe_paths` cita `dataverse.md §14` | idem |
| `price-history` | `keep-in-place` · SQL (retenção na BD, C-060) | linha = dia × unidade; plurianual | = `daily-price.reads` + `data`; `mandatory_filters: [intervalo de datas]`; tectos por DK, sem literal (D10) | `[]`, `readonly: true` | `key: [data, unidade, produto]` | idem |
| `workflow-audit` | **`owned` — autoridade OPEN (U-040)** | pedido/aprovação; evento auditado | — | — | `fields[]` (D2): `AprovacaoCarregamento` {id, data_preco, estado `choice [pendente, aprovado, carregado]`, pedido_por, aprovado_por, aprovado_em, carregado_em}; `DadosMestre` pedido {id, dimensão, valor_antigo, valor_novo, estado `choice [proposta, aprovada, activa]`, …}; `JournalAuditoria` {evento `choice` = `identity_and_controls.audit.events`, actor, alvo, antes, depois, quando}. **Todos `name_basis: design`, `source: design (A7 audit / entities[].state_machine)`, `state: Assumed`**; `set_by` = transições de `state_machine` | `key: [id]`; `authority_state: open (U-040)` — §4 renderiza como *«domínio cuja autoridade está em aberto»*, nunca como facto | n/a (owned) — dono da app: equipa de pricing (C-068) |
| `sap-terms` | `keep-in-place` · SAP | linha = cliente × produto × semana | {cliente, produto, semana, preço (OZP01/OZP02)} — **sem locator L1**: `source: C-003/C-052`, `state: Assumed`; mecanismo `Unknown (C-063)` | `[]`, `readonly: true` | `key: [cliente, produto, semana]` | IT centralizado (C-063) — `Confirmed` (declaração do dono dentro da autoridade) |

O que a junção **expôs** e como o dono fechou (2026-09-09): (a) `ProjecaoCenario` sem domínio → domínio `scenarios` (`owned`, cenários gravados; a interactividade continua em `U-039`, o que se grava não); (b) o Excel guarda parâmetros de clientes a termo (`AçoreanaMutualista_*`, 36 nomes = **12 colunas** populadas: 4 `Margem` + 8 `Transporte*`, medido) que `C-052` diz serem do SAP → **`DISMISS — SAP é a fonte (C-052)`**: as 12 colunas saem de `costs-margins.writes[]` (38 → **26**) e ficam listadas com razão; (c) os 17 `manual` de `Outputs` (overrides) → **não admitidos**: `daily-price.readonly: true`, `writes: []`, um ajuste excepcional passa por margem/inputs — sem `Unknown` novo; (d) **por decidir pela skill** (não pelo motor): 9 colunas `PreçosSpot_<fuel>_Margem|DescontoAdicional` caem em `daily-quotes` pela regra de prefixo mas são margens por produto — candidatas a `MAP → costs-margins`; o número final de cada domínio move-se ±9 conforme essa disposição.

---

## 6. dpt-galp-jp — as duas listas de v01 contra o L1

Sem `_blueprint/`, a aceitação é **cobertura de fonte**: cada campo de v01 tem fonte L1, SU ou `design` — e o rascunho não perde nada que o L1 tenha.

| Campo v01 (*Priority Decisions*) | Fonte no rascunho | Classe |
|---|---|---|
| `TicketID` | `Priority_Store!A` «Ticket ID» (`key_like`) + `Dayly_extraction!A` «ID» | L1 → `identifier`, `index: primary` |
| `Descricao` | `Dayly_extraction!G` / `Priority_Store!C` | L1 → `text` |
| `Prioridade` | `Priority_Store!E` + validação `"High,Medium,Low"` | L1 → **`choice` determinístico** |
| `Exec_Order` | `Priority_Store!F` `number`, `nulls 52/89` | L1 → `number`, `required: false` determinístico |
| `Status` | `Dayly_extraction!F` (4 distintos) + `Priority_Store!H` «Live Status» (`derived`) | L1 → `choice` parcial; `Out of Source` = `design` |
| `SEV` | `Dayly_extraction!E` «Severidade» | L1 → `choice` (valores dos dois extractos) |
| `VIP` | `Dayly_extraction!I` **vazia** | L1 `header only` → `unknown`; `values [Commercial]` só por SU (C-005) → `Assumed` |
| `Equipa` · `Localizacao` · `Beneficiario` · `Requisitante` | `!L` · `!B` · `!H` · `!S` | L1 → `text` (PII: C-016 em `rules`) |
| `Tipificacao_N1..N6` | `!N` «Tipificação» (1 coluna) | L1 → **1 campo** `Tipificacao` (decisão do dono 2026-09-09); a divisão ×6 de v01 é `MAP 1→6` **só se um ecrã aprovado filtrar por nível** (C-015), com `name_basis: design` |
| `DataCriacao_EasyVista` | `!C` | L1 → `datetime` |
| `DataEntrada_PriorityStore` | `Priority_Store!G` «Priority date» (≈) | L1 → `datetime`, `Assumed` |
| `Prioridade_EasyVista` | `Dayly_extraction!Q` «Prioridade» (Baixa/Média/Elevada) | L1 → `choice` (C-013) |
| `Title` · `LastModifiedBy_Flow` · `LastModifiedAt_Flow` | — | `design` (convenção SP · auditoria A7) |
| *Audit Log* (7 campos) | — | `design` — `identity_and_controls.audit`, domínio `owned` |

**Colunas do L1 que v01 não carrega** (o rascunho obriga a disposição): `Data de Conclusão` (vazia nos pendentes, **157/157** nos fechados), `Serviço` (71/72), `Área de Negócio`, `Origem` (1 valor), `Projecto`, `Project Name`, `Focal Point Midrange` (vazias), `Priority_Store!B` «Creation Date» (duplicado de `!C`), `Prioritized_View` (10 `derived` — relatório, `DISMISS — vista`). Nenhuma fica sem `ADOPT`/`MAP`/`DISMISS`.

---

## 7. Consumo por slot

| Consumidor | O que lê de A5 | Forma |
|---|---|---|
| **spec §4 `entities_to_create`** | `entities[]` ⋈ `record_authority[]` por `authority` | uma linha por entidade: *Entidade · Domínio (`key`) · `access_mode` · o que abdica (`forfeits[]`) · **owned**: campos `nome · tipo · obrigatório · default` · **externo**: `lidas (n) · escritas (n) · chave` · Relações (`join_keys`) · Índices (`index` / `delegation_safe_paths`) · Estado (`n Assumed / n Confirmed / n Unknown`, `schema_owner`)*. Sub-tabela por entidade com as linhas. Entidade `authority: none` → linha **⚠️ lacuna** (D11). Conjunto vazio → racionalização verbatim (inalterado) |
| **spec §6 `flows_to_implement`** | `fields[].set_by` e `writes[].by/write_semantics/rules` por transição de `state_machine` | por transição: *quem transiciona* (= `set_by`/`by`) · *o que valida* (= `rules[]`) · colunas escritas · notifica quem e gatilho continuam de A7/`decisions.md` (inalterado); `not named` onde nenhum nomeia |
| **spec §8 `security_implementation`** | eixo Entidade × coluna: `reads[].by`, `writes[].by`, `confidentiality.row_level/column_level` | matriz Papel (A7) × Domínio (A5) com R/W derivado de `by[]`; linha/coluna: valor com estado (`U-037`) — a **forma** segue `security-craft.md §B`, a existência vem de A7 (inalterado) |
| **spec §7 `integrations`** | `store_facts.*`, `connection_identity` | por integração: autenticação e custódia = `connection_identity` (`Unknown (U-036)` renderiza como lacuna nomeada, P-7) |
| **spec §15 migração** | `access_mode` + `dictionary_entries_without_data` + `disposition: DISMISS` | o que **não** migra fica escrito |
| **architecture-story `## Data`** | tabela de domínios (chave · modo · n lidas/escritas/campos · dono do schema · estado) | *carrier* (I-1): copia, não decide; cabeçalho com `authority: ux-blueprint_v<NN>@<sha256>` (§9) |
| **estimate §3 `work_breakdown` — coluna `driver`** (P-10) | **via spec §4**: `n campos · n lidas · n escritas · grão · volume` | a estimativa lê **só** o inventário da spec (`forbidden_sources`: `_capture/*`, SU; teste `test_operational_impact_is_sourced_from_the_active_modes_inventory_only`); logo §4 tem de **renderizar os números** para a estimativa os citar como `spec §4 <entidade>` |
| **estimate `operational_impact`** (hoje **§17** — frente B renumerou; o plano diz §16) | via spec: tabela *passo · quem · tempo actual · novo processo · tempo novo · Δ*; o «novo processo» sai de A5 (`writes[].by` × `cadence` × `volume`: *85 valores/dia por Analista → grelha*); o «tempo actual» sai de `as-is.md# passos` (P-5) | **a aresta `as-is.md` entra na spec, não na estimativa** — a estimativa proíbe `as-is.md` de quatro formas e os testes de B congelaram-no (§10, emenda a P-10) |
| **`render-validate.py`** (P-7) | regras de integridade §4 + suficiência por entidade §8.3 | determinístico, lê YAML tolerante (`dashboard.py` já tem o walker) |

---

## 8. Critérios de aceitação

### 8.1 pilot-1 — por entidade (contra `v06` como registo mais recente; `v07` se `/answer U-036/U-040` chegar antes)

| Entidade | Critério determinístico (motor + validador) | Critério de julgamento (skill, revisto pelo dono) |
|---|---|---|
| `DadosMestrePricing` | `authority: master-data` resolve; `reads ≥ 4` tabelas de dimensão com `values[]` não vazios e `source` L1; `dictionary_entries_without_data == 42` (distintas; motor 0.1.0); `writes ≥ 1` com `rules` citando `C-058`; `schema_owner.state == Assumed` e `open == U-036` | contraparte tem **7** valores (prefixos técnicos `DISMISS`); métrica ≠ porto separados |
| `CustosLogisticos` · `MargensAlvo` | `authority: costs-margins`; `len(writes) == 26` (38 colunas `manual` do L1 − 12 `AçoreanaMutualista_*` com `disposition: DISMISS — C-052`), todas com locator L1, 0 `derived`; as 12 descartadas listadas com razão; duas cadências declaradas (22 mensais / 4 diárias); `key == [data, …]`; ±9 se a skill fizer `MAP` das `PreçosSpot_*_Margem` (§5 d) | disposição das 9 `PreçosSpot_*_Margem|DescontoAdicional` registada (`MAP` ou fica em `daily-quotes`) |
| `InputsDiarios` | `authority: daily-quotes`; `len(writes) == 39 + 7` (7 com `name_basis: none`, `state: Unknown`); `reads` inclui 15 séries de feed (5 + 10) com nome = id do fornecedor; 5 `computed` com `lineage → Market View`; `mandatory_filters == [data]` | regra `C-074` (valor estimado 2ª/3ª) em `rules[]` das escritas |
| `PrecoDiarioConsolidado` | `authority: daily-price`; `len(reads where computed) == 59`, cada uma com `lineage[]` não vazio; `readonly: true`, `writes == []`; BIOS: 15 `reads` com `disposition` condicional a `U-033`; `key == [data, unidade, produto]`; **0 literais numéricos** em `delegation_safe_paths`; os 17 `manual` de `Outputs` listados como `disposition: DISMISS — override não admitido no to-be (dono, 2026-09-09)` | — (fechado pelo dono) |
| `HistoricoPrecos` | `authority: price-history`; `reads == daily-price.reads ∪ {data}`; `mandatory_filters` não vazio; `readonly: true` | retenção cita `C-060`, não número da plataforma |
| `AprovacaoCarregamento` · `JournalAuditoria` | `authority: workflow-audit`; `access_mode == owned`; `fields ≥ 1` com `type ≠ unknown` por entidade; **100 %** `name_basis: design`, `source: design (…)`, `state: Assumed`; `set_by` cobre todas as transições de `state_machine`; `authority_state: open (U-040)` presente | §4 renderiza o domínio como *autoridade em aberto*; a spec continua **bloqueada** por escolha estrutural — o critério não é «spec produzida», é «§4 do `--dry-run` correcto» |
| `TermosComerciaisCliente` | `authority: sap-terms`; `reads ≥ 4`, `source` SU (`C-003`/`C-052`), `state: Assumed`; `writes == []`, `readonly: true`; `schema_owner.state == Confirmed` (C-063) | — |
| `ProjecaoCenario` | `authority: scenarios`; `access_mode == owned`; `fields ≥ 6` com `type ≠ unknown`, 100 % `name_basis: design`, `state: Assumed`; `index: primary` em `id`; `render-gaps.md` **sem** linha para esta entidade | interactividade (`U-039`) continua aberta como escolha de superfície, não de dados |

**Global pilot-1**: `render-validate.py` sobre o **`v02` antigo** (4 domínios, 7 entidades com `fields_itemized: false`) dá **≥ 3 lacunas `required`** (§4 campos, §6 fluxos `(none)` com 2 entidades `approval: true`, §8 sem matriz) — hoje dá 0; sobre o registo novo dá **0 lacunas por conteúdo** excepto as que o registo **declara** (`ProjecaoCenario`, `store_facts` U-036, overrides). §4 tem colunas *lidas · escritas · chave*. Nenhuma célula «ver secção 16».

### 8.2 dpt-galp-jp — cobertura

| Critério | Medida |
|---|---|
| Todos os 18 campos de *Priority Decisions* têm classe de fonte ∈ {L1, SU, design}; classe `none` == **0** | tabela §6 |
| `Prioridade.values == [High, Medium, Low]` e `Exec_Order.required == false` saem do motor **sem julgamento** | determinístico |
| Colunas do L1 sem campo em v01 (≥ 8) têm disposição; `Data de Conclusão` aparece como `ADOPT` candidato com evidência `157/157 nos fechados` | o rascunho não perde o que v01 perdeu |
| *Audit Log* 7 campos, todos `design`, domínio `owned` | — |
| Re-render **não** é critério aqui: não existe `_blueprint/` para o `/render` ler. Se o dono quiser re-render, é um passo a mais (autorar blueprint para dpt-galp-jp) fora da frente D | honestidade sobre o que se mede |

### 8.3 Suficiência por entidade (regras para `render-validate.py`, P-7)

| Regra | Falha ⇒ |
|---|---|
| `entities[].authority` resolve para `record_authority[].key` | lacuna `required` §4, dono `architecture` |
| `owned`: `fields ≥ 1` com `type ≠ unknown`; `fields ⊇` colunas `primary/secondary` que os `screens` referenciam à entidade; ≥ 1 `index: primary` | lacuna `required` §4 |
| externo: `reads ≠ []`; `writes ≠ []` **ou** `readonly: true`; `key ≠ []` **ou** `open: U-nnn`; `schema_owner` presente com `state` | lacuna `required` §4 |
| toda a linha tem `state` + `source`; `Confirmed` ⇒ locator existe (`inputs/`, `_capture/`, `answers.md`) | lacuna `required` §4 (linha) — mesma família do guard `su-confirmed` |
| `flows_to_implement == (none)` **e** ∃ entidade com `state_machine`/`approval: true` | lacuna `required` §6 |
| §8 sem tabela Papel × (Ecrã \| Entidade) | lacuna `required` §8 |
| `store_facts.connection_identity.state == Unknown` | **não** é lacuna de §4 — é lacuna nomeada de §7 (`integrations`, P-7) |
| literal numérico em `delegation_safe_paths`/`mandatory_filters` | defeito de contrato (D10) |

---

## 9. O que identifica uma versão de A5 (interface com P-18 F04/F08)

- **Identidade**: `ux-blueprint_v<NN>` + `sha256` do bloco `architecture:` normalizado + `fields-draft.json.source_sha256` + `tool.version`. O rascunho é reproduzível: mesmo L1 → mesmo rascunho; a **disposição** (D12) é o que muda entre versões e é o que o `blueprint-log.md` regista (step 11b já existe).
- **F04** (`synthesis_state` por tópico): `architecture-story.md` ganha no cabeçalho `authority: _blueprint/ux-blueprint_v<NN>.yaml#architecture @ <sha256>`; o motor compara com o `v<approved>` e dá `fresh` / `stale` / `desconhecido` (sem cabeçalho). `business-story` compara com a SU. Sem `max()` global.
- **F08** (`solution-blueprint` lê `v<latest authorized>`, spec lê `v<approved>`): A5 de um `v06` não aprovado aparece no *solution-blueprint* com a etiqueta *«com escolha estrutural aberta»* (e a §4 do `--dry-run` da spec mostra a forma), mas **nunca** numa spec real — `blocked_when` já o garante. O desenho não acrescenta estado: usa `approved`/`draft` que existem.
- **`p18-design.md`** não existe neste scratchpad; F04/F08 ficam **desenhados aqui apenas no que toca A5**. O resto de P-18 continua na frente E.

---

## 10. Desvios ao plano e emendas propostas (para o dono aplicar em `CONSOLIDATED_PLAN.md`)

| # | Onde | Diz | Deve dizer | Porquê |
|---|---|---|---|---|
| E1 | P-6 aceitação | «`schema_owner` = equipa da BD (de `A-001`)» | «`schema_owner` = `Assumed` (C-057), autoridade de mudança em aberto (`U-036`)» | `A-001` é a corrupção do Excel; `U-036` está aberta — afirmar dono seria `Confirmed` acima da evidência (P-12) |
| E2 | P-6 aceitação · frente D validação | «as 7 entidades **externas** têm `access_contract`» | «6 domínios externos têm `access_contract`; 1 domínio `owned` (`workflow-audit`, U-040) tem `fields[]` marcados `design`; 10 entidades resolvem `authority` ou declaram lacuna» | `v06`: 6 `keep-in-place` + 1 `owned` |
| E3 | P-5 / P-6 «Toca» | «`aisa-decide`/`aisa-synthesize` invocam o motor» | «`aisa-blueprint` step 2 e `--refresh` invocam o motor; `aisa-synthesize` carrega a tabela em `architecture-story.md ## Data`» | em `/decide` não há `record_authority[]`; `/synthesize` é *carrier* (I-1) |
| E4 | P-6 motor | «`header → name`» | «`named_range → formula_ref → header → none`» | pilot-1: `Inputs` sem cabeçalhos fiáveis (C-017), `Outputs` 4/76 |
| E5 | P-10 `operational_impact` | «fonte adicional autorizada `_synthesis/as-is.md# passos com tempo`» na **estimativa** | a aresta `as-is.md` entra na **spec** (fonte condicional para uma tabela *alteração de caminho operacional*); a estimativa continua a ler só o inventário da spec | `estimate.template.md` proíbe `as-is.md` «NOT required, NOT conditional, NOT fallback, NOT point-of-need» e `test_estimate_declares_as_is_forbidden_in_all_four_ways` congela-o (frente B fechada) |
| E6 | P-10 · frente D validação | «§16 da estimativa deixa de ser `not applicable`» | «`operational_impact` (hoje **§17**) deixa de ser `not applicable`» | frente B inseriu §16 *Equipa e esforço por perfil* |

Achados novos para a frente D absorver (não estavam no plano): `ProjecaoCenario` sem domínio; 76 entradas de dicionário sem dados; 17 overrides manuais em `Outputs` sem dono no to-be; parâmetros de clientes a termo no Excel vs SAP (C-052); `v05` aprovado não parseia em PyYAML (o motor de P-7 tem de usar o walker tolerante de `dashboard.py`, não `yaml.safe_load`).

---

## 11. Decisões do dono (2026-09-09, por `AskUserQuestion`)

| # | Tema | Decisão | Efeito no desenho |
|---|---|---|---|
| 1 | `ProjecaoCenario` | **domínio próprio `scenarios`, `owned`, cenários gravados** | 8.º domínio; `fields[]` de design (§5); §8.1 sem lacuna para a entidade; `U-039` fica só como escolha de superfície |
| 2 | Parâmetros de clientes a termo no Excel (`AçoreanaMutualista_*`) | **`DISMISS — SAP é a fonte (C-052)`** | `costs-margins.writes` 38 → 26; as 12 colunas (4 `Margem` + 8 `Transporte*`, medidas após a pergunta — a pergunta dizia 9) listadas com razão |
| 3 | Overrides manuais sobre o preço calculado | **não admitidos** | `daily-price.readonly: true`, `writes: []`; 17 `manual` de `Outputs` → `DISMISS`; sem `Unknown` novo |
| 4 | Onde corre o motor | **`aisa-blueprint` step 2 e `--refresh`** (D5 confirmado) | zero superfície de campos em Discovery |
| 5 | `Tipificação` (dpt-galp-jp) | **1 campo**; `MAP 1→6` só se um ecrã exigir | rascunho fiel ao L1 |
| 6 | Emendas E1–E6 | **aplicadas** a `CONSOLIDATED_PLAN.md` (P-5, P-6, P-10, onda 0, frente D, estado, P-18) | o plano e este desenho dizem o mesmo |

---

## 12. Regras cumpridas

- `library/` intocado; nenhum ficheiro de engagement tocado; nenhuma row criada.
- Nenhum vendor nomeado fora do contexto de Options/Decision (pilot-1 está em Decision; `dpt-galp-jp` idem).
- Contagens só pelo L1 (`extraction.json`), scripts descartáveis, sem edição à mão.
- Nada foi inventado: onde o L1 não dá nome, tipo ou dono, a forma prevê `Unknown` com locator do que existe.
