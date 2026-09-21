# Step 9d — Frente B: estimativa (P-11, P-8, P-9, emenda F09)

> Passo do tracker para a **frente B** do `docs/CONSOLIDATED_PLAN.md` §5.
> Ficheiros: `library/packs/pp/deliverable-templates/estimate.template.md` ·
> `library/packs/pp/deliverable-templates/implementation-spec.template.md` ·
> `.claude/skills/aisa-simulate/SKILL.md` (emenda F09).
> Cópia de validação: `projects/pricing-marinha-pilot-1-val-b`, de `pricing-marinha-pilot-1`
> (blueprint v05 aprovado, estado congelado).
> Modelo: Opus 5 (`claude-opus-5`) para as edições; validação no modelo de produção.
> Invariante do plano: **total de 44 pessoa-dias inalterado** — P-8/P-9 são projecções, não recálculo.

---

## 1. Onda 0 de B — P-11: experiência de template antes de tocar no template

**Desenho.** Renderizar a §4 da Especificação de Implementação de `pricing-marinha-pilot-1` com a
instrução antiga de uma linha (*"One row per entity: name, owner, fields, relationships, indexes"*),
sem mais nada alterado — sem as proibições, sem o contrato de projecção, sem o `epistemic_projection`.

**Instrumento.** Três subagentes isolados (`n = 3`, protocolo §6.3), Opus 5, cada um com acesso
**apenas** às duas fontes que `slot_sources.entities_to_create` declara:

- `the architecture block# record_authority[]` — `_blueprint/ux-blueprint_v05.yaml` (versão aprovada);
- `_blueprint/ux-blueprint_v<approved>.yaml# entities` — v05 remete para v01.

O isolamento é deliberado: a sessão que conduz a frente já tinha lido o template completo e o render
`v02`, e não pode servir de sujeito ao seu próprio teste. Fixture e os três outputs em
`step-9d-evidence/p11/`.

**Facto determinístico anterior ao run.** As 7 entidades do blueprint têm `fields_itemized: false`
(3 explícito, 4 por ausência) e nenhuma declara relações ou índices. Nenhuma instrução — longa ou
curta — pode produzir campos sem os inventar. O run só decide entre os ramos **(b) não saem** e
**(c) saem inventados**.

### 1.1 Resultado

| Medida | run 1 | run 2 | run 3 |
|---|---|---|---|
| Campos produzidos | 0 | 0 | 0 |
| Campos/tipos inventados (`nvarchar`, `datetime`, `PK`, `FK`, …) | 0 | 0 | 0 |
| Colunas `campos`/`relações`/`índices` marcadas como não declaradas | sim | sim | sim |
| Secção de lacunas explícita | §4.2 (5 lacunas) | 3.ª subsecção | §4.1 |
| Reportou as 2 entidades **sem** `record_authority` | sim | sim (*"a lacuna mais material"*) | sim |
| Reportou o colapso `MargensAlvo` + `CustosLogisticos` num domínio | sim | — | — |

Contagem de tipos inventados por `grep -icE "nvarchar\|varchar\|datetime\|decimal(\|uniqueidentifier\|guid\|primary key\|foreign key\| PK \| FK "` = **0/0/0**.

### 1.2 Veredicto — ramo (b), e um achado fora dos três ramos

**Ramo (b): não saem campos → a causa é upstream.** Confirmado, 3/3. A §4 não tem de onde tirar
campos: o defeito está na autoridade (`fields_itemized: false` nas 7 entidades), não na instrução.
Consequência prevista no plano: **P-6 resolve** (frente D, `architecture-core.md` A5 `fields[]` /
`access_contract`), e **G4 fica só como anexo curto de forma por secção** — 1 exemplo cada, ≤ 5
linhas, referência `plano-automacao-pricing-oil-es-tobe.text.md` §2–§7 e §9.

**Não há mandato de corte.** O ramo (a) — *"saem campos → cortar proibições redundantes"* — não se
verificou. O template de 406 linhas não é absolvido, mas também não é o que impede os campos de sair.
Nada se corta nesta frente.

**Achado fora dos três ramos — a comparar com o render real.** O render `v02`, produzido com o
template completo, atribui `Autoridade de registo` = *"external system of record (SQL Server
partilhado)"* e `access_mode` = `keep-in-place` às **7** entidades. O `record_authority[]` aprovado
declara **4** domínios, e nenhum deles é o preço diário consolidado nem a aprovação de carregamento.
O template longo **sobre-afirmou** a autoridade de registo de 2 entidades; a instrução de uma linha
não sobre-afirmou em nenhum dos 3 runs — reportou a ausência, e em run 2 chamou-lhe a lacuna mais
material da secção.

Isto falsifica, para esta secção, a premissa do ramo (c) (*"o contrato é o que os impede"*): o
contrato não impediu a sobre-afirmação, e a sua ausência não a provocou. Duas consequências, **ambas
fora do âmbito da frente B**, registadas aqui para quem executar D:

1. **Defeito de conteúdo em `pricing-marinha-pilot-1`**: o `v02` da spec afirma autoridade de registo
   sem base para `PrecoDiarioConsolidado` e `AprovacaoCarregamento`. Corrige-se no re-render de D,
   não aqui — a §4 não é ficheiro da frente B.
2. **Defeito de forma da §4**: onde a autoridade não cobre uma entidade, a §4 tem de o **dizer como
   lacuna**, não preenchê-la por analogia com as vizinhas nem enterrá-la numa célula de *Notas* com
   um *"ver secção 16"*. Entra no desenho de A5 (P-6) e no `render-validate.py` por conteúdo (P-7).

**Toca:** nada permanente, como o plano previa. Só evidência.

---

## 2. P-8 — Transições de estado e pré-condições com dono

Commit: `6331df6`. Testes de regressão: 13, todos falham contra o estado anterior.

**Especificação, §6.** A ausência de stream assíncrono em A6 não é a ausência de transição a
especificar. `slot_conditions.flows_to_implement` passa a declarar o piso: onde
`experience.mode != none` e uma entidade do blueprint **aprovado** carrega `state_machine` ou
`approval: true`, a §6 carrega, por entidade, *quem transiciona · o que valida · o que notifica quem ·
o que dispara o ciclo*. O **conjunto** de transições é lido do blueprint; actor, regra, destinatário e
gatilho são projectados de A7 e de `decisions.md`, e renderizam `not named` **com item de trabalho em
aberto** onde nenhum os nomeia. Renderizar `(none)` sobre uma máquina de estados viva passa a
proibição explícita, tal como preencher uma transição por analogia com outra entidade ou outro role.

**Estimativa, §14 (nova).** Slot condicional `estimate_preconditions`, com a carriage dos portões de
construção: *condição · dono · até quando · **que fase trava** · estado*. `estimate_assumptions` fica
restringido a **premissas de método**; disponibilidade de SME, acessos, credenciais, licenças,
entitlements e aprovisionamento deixam de poder ser escritos como premissa — onde perdiam dono e
prazo, e é por isso que ninguém as fechava. A **dedicação** declarada aqui é o input da ocupação por
perfil de P-9: uma declaração, lida duas vezes.

**Duas emendas ao contrato, descobertas pela validação — não pelo desenho.** As fontes que declarei
primeiro para `estimate_preconditions` (A8, A10, `decisions.md`, portões da spec) não alcançavam
nenhuma das duas pré-condições que o plano nomeia na aceitação:

- **acesso à BD partilhada** — vive em `compositions[]` com `boundary: outside-platform` e o `owner`
  registado dessa composição, não em `decisions.md`;
- **dedicação de SME a 20%** — vive na *standard team composition* do método, e a exigência de a
  acordar à cabeça vive na sua guidance de entrega (R4).

Ambas entraram no `slot_sources`. A aceitação do plano funcionou como teste do contrato, e o contrato
falhou primeiro: sem estas duas fontes, a §14 renderizaria sem as duas linhas que justificam a
correcção.

## 3. P-9 — Tarefas em banda e ocupação por perfil

Commit: `2ce2447`. Testes de regressão: 13, todos falham contra o estado anterior.

- `phases_table`: coluna **perfil responsável**; fase com figura ≥ 5 pessoa-dias carrega sub-tabela
  *tarefa · intervalo de planeamento (min–max) · perfil*, com `soma(min) ≤ figura da fase ≤ soma(max)`.
  Abaixo de 5 pessoa-dias não se decompõe. A decomposição **redistribui**: figura da fase e total
  global idênticos antes e depois.
- `profile_load` (novo slot condicional): `pessoa-dias ÷ dedicação → semanas mínimas`, aritmética
  apenas, sobre a dedicação que a §14 declara. Sem dedicação declarada, o perfil renderiza
  `dedication not named` e nenhuma figura de semanas. Grelha, Gantt, data de calendário e
  sobreposição derivada entre perfis passam a proibidos — o paralelismo fica restrição em prosa.
- `named_uncertainties`: cada item aparece também numa linha da fase que ameaça, referenciado pelo id;
  quem não ameaça fase nenhuma di-lo e continua na lista.
- `delivery_recommendations`: dimensão de repetição com **N ≥ 3** instâncias nomeadas obriga a
  recomendar piloto sobre subconjunto **vindo do inventário**; sem repetição, não se fabrica piloto.

**Terceira emenda ao contrato, também da validação.** O método dá **taxas pontuais** (1d por ecrã
model-driven, 2d por approval workflow) e uma única banda (integração externa 3–5d). Exigir min–max
sem dizer o que fazer com uma taxa pontual convidava a fabricar um `±`. O contrato passa a declarar:
banda onde o método dá banda; `min == max` marcado *taxa pontual* onde dá taxa pontual; `min == max`
com a analogia nomeada e a marca *sem banda no método* onde não dá entrada. **Um intervalo degenerado
que diz porquê é informação; um `±` inventado não é.**

## 4. Emenda F09 — intervalos de planeamento, não quantis

Commit: `2ce2447`, junto com P-9 (mesmo ficheiro, mesma aceitação aritmética).

A estimativa e a simulação emitem **intervalos de planeamento** (min–max sobre as bandas do método).
`interval_vocabulary` declara-o uma vez, com a razão: o método tem taxas, factores e buffer, e **não
tem distribuição** — logo `P50`, `P80` ou qualquer quantil não se afirmam até existir método
probabilístico documentado e calibrado no pack. Afirmar quantil passa a proibição declarada.

De `aisa-simulate` saiu o `P50/P80` e saiu o exemplo `SAP integration ×1.4`, que **nenhuma secção do
método enuncia**. Regra nova no seu lugar: cada factor é citado à secção que o enuncia, e um factor
sem secção não se aplica.

## 5. Validação — re-render direccionado de pilot-1

**Cópia:** `projects/pricing-marinha-pilot-1-val-b` (de `pricing-marinha-pilot-1`, blueprint v05
aprovado, estado congelado). Modelo: Opus 5 — o render é pós-decisão, e o perfil de produção decidido
em step-9c põe Framing/Options/Decision em Opus 5.

**Desenho: re-render direccionado, não completo.** Só os slots que a alteração de contrato toca foram
re-executados, contra a mesma arquitectura aprovada e sem alteração upstream; tudo o resto foi
carregado de `v02` carácter a carácter. A razão é o próprio invariante do plano: um re-render completo
faria as 18 secções derivarem por motivos alheios a P-8/P-9, e *"total 44 inalterado"* deixaria de ser
verificável. Assim é: `step-9d-evidence/accept_frente_b.py` compara v02 e v03 secção a secção.

| Aceitação do plano (§5, frente B) | Resultado |
|---|---|
| §6 ≠ `(none)` | **passa** — 4 transições, uma linha cada, sobre 2 máquinas de estado; 13 células `not named` em vez de inventadas |
| fases ≥ 5d com bandas cuja união contém o total | **passa** — 2 fases no limiar (fase 3, 8d; fase 7, 8d); `8,0 ≤ 8,0 ≤ 8,0` nas duas; as 4 abaixo do limiar não são decompostas |
| ocupação por perfil ≤ dedicação | **passa** — developer: `44 ÷ 1,0 = 44` dias → ≥ 9 semanas; 44 ≤ 45 disponíveis |
| cada item de §9 numa fase | **passa** — 6/6; os 2 que ameaçam a migração dizem que a fase que ameaçam não está no total |
| **total 44 inalterado** | **passa** — 30,5d brutos e 44 pessoa-dias base idênticos; 10 secções da estimativa e 13 das 16 da spec idênticas carácter a carácter |
| SME 20% e acesso à BD partilhada como pré-condições com dono e fase travada | **passa** — §14 com 10 linhas |
| F09: sem quantis, sem `×1.4` | **passa** |

65 verificações, exit 0. Output em `step-9d-evidence/accept_frente_b.out`; os dois `v03` em
`step-9d-evidence/render/`.

### 5.1 O que a validação encontrou no conteúdo de pilot-1

Três defeitos reais, revelados pelas correcções e não inventados por elas:

1. **A §6 da `v02` renderizava `(none)` sobre duas máquinas de estado vivas.** Os 4 itens de trabalho
   em aberto que a `v03` acrescenta já existiam; a `v02` não os mostrava. O `(none)` era literalmente
   verdadeiro sobre A6 e materialmente falso sobre o que há para construir.
2. **Um portão de construção estava marcado *satisfeito* por meia evidência.** A condição de `D-002`
   pede *dono de dados-mestre nomeado **+** processo mínimo de controlo de mudança*; `C-058` nomeia o
   dono e exige aprovação formal, e não descreve o processo. Na `v03` fica **parcialmente satisfeito**,
   com a razão, e o processo entra como item em aberto.
3. **A `v02` não carregava pré-condição de entrega nenhuma** — nem SME, nem acessos, nem
   aprovisionamento, nem ambientes. Não estavam escritas como premissa: estavam ausentes. A §14 não as
   relocaliza, acrescenta-as.

### 5.2 O que fica por medir

- **`profile_load` com mais de um perfil quantificado.** Em pilot-1 só o developer tem pessoa-dias; o
  SME e o IT renderizam `not named`. O ramo com dois perfis quantificados — onde a ocupação de um pode
  exceder a sua dedicação — **não foi exercitado**. Exercita-se no primeiro engagement com Power BI
  developer ou com dois developers.
- **A dimensão de repetição foi exercitada só no ramo negativo.** pilot-1 não repete trabalho sobre
  N ≥ 3 instâncias nomeadas, e a §19 di-lo em vez de fabricar um piloto. O ramo positivo (parques,
  produtos, países) fica por exercitar.
- **Intervalos não degenerados.** Os 4 intervalos de pilot-1 são todos `min == max`, porque o método
  dá taxas pontuais para estes componentes. A única banda real do método (integração externa, 3–5d)
  cai numa fase de 4d, abaixo do limiar de decomposição. Um intervalo verdadeiramente largo **não foi
  renderizado**.
- **`n = 1` neste render.** O protocolo §6.3 pede ≥ 3 runs ou um teste determinístico para qualquer
  comparação; escolheu-se o teste determinístico, e é o que sustenta o resultado. Não há aqui medição
  de variabilidade do modelo.

## 6. Fecho

Frente B **congelada**. Commits: `13658c1` (P-11), `6331df6` (P-8), `2ce2447` (P-9 + F09), mais as
três emendas de contrato que a validação forçou. 26 testes de regressão novos, suite completa
`245/245` verde, aceitação determinística `65/65`.

Frentes seguintes, pela ordem do plano: **C** (P-13, P-14) está desbloqueada agora que A congelou;
**E** (P-15 a P-18) continua a bloquear a validação lente a lente de A e o desenho de A5; **D** fica
por último e já tem o veredicto de P-11 (§1.2) e três achados de conteúdo (§1.2, §5.1) à sua espera.
