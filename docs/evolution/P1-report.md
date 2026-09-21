# P1 — Ligar contratos ao código e fixar referências de aceitação

Estado: **IN_PROGRESS**

Não é GO. O template proíbe marcar GO com campos de evidência por preencher, e faltam
quatro dos cinco entregáveis.

## Identidade e precondições

- **Data/ambiente/runtime:** 2026-09-21 · Linux 6.18.44-fc-v37 x86_64 · Python 3.11.15
- **GO anterior e evidência:** P0 **GO** — `docs/evolution/P0-report.md`, baseline de 48
  ficheiros / 2009 testes em três modos de runner.
- **Estado do conjunto à entrada de P1:** verde. 48/48 ficheiros, 0 falhas, 0 erros,
  13 skips, 3 xfail, depois de `f04792e`.
- **Contratos aplicáveis:** `AUTHORITY_AND_KNOWLEDGE.md`, `WRITES_AND_RECOVERY.md`,
  `MIGRATION_AND_COVERAGE.md`.

### Âmbito de pilotos — decidido

Dois, não quatro, por decisão do operador:

| Engagement | Entrada | Tipo P8 |
|---|---|---|
| `dpt-galp-jp-pilot-4` | `Dayly_pending_tickets_Anonimo.xlsx` | operacional / tickets |
| `pricing-bunkers-pilot-4` | `PREÇO BANCAS_03_08_26.xlsm` + `.vtt` | Excel com regras e dependências |

`cae-automation-pilot-4` e `kam-onboarding-pilot-4` ficam em disco como dados de
engagement — `test_state_scaffold` varre `projects/` — mas não levam oráculo e não são
evidência de P8. Nada foi apagado.

## Entregáveis

| Entregável | Estado |
|---|---|
| `writer-reader-map.md` | **feito** — camada Python verificada por AST; camada das skills lida |
| `authority-map.md` | **feito** — 24 skills lidas; autoridades por artefacto e por modo |
| `integration-adr.md` | **parcial** — ADR-001 (linguagem de runtime) aceite; falta o mapeamento módulo a módulo do doador |
| `test-map.json` | **feito** — 61 casos ligados a fase, família e gate de saída; 0 implementados, e porquê |
| Oráculos dos 2 pilotos | **extraídos** — 22 itens, 13 críticos **por validar pelo responsável** |

## Progresso — o que está verificado

### Escrita, camada Python

Método: `ast.walk` por operação de escrita, seguido de inspecção da linha de origem de
**cada** ocorrência. A segunda passagem não é opcional: sem ela `str.replace` conta como
escrita e o mapa sai errado. A primeira tentativa, por verbos, marcou `dashboard.py` como
escritor da Shared Understanding e `coverage.py` como escritor de `_capture/`. Ambos falsos.

Confirmado contra o contrato, não aceite por declaração:

- **`coverage.py` escreve só em `finalize`, e só em `<engagement>/_coverage/`.** Oito
  chamadas, todas na mesma região (L3594-3660).
- **`dashboard.py` escreve só `dashboard.html`**, por `atomic_write` (L125-134):
  `makedirs` → `open(tmp,"w")` → `os.replace`, com o **pid no nome do tmp** porque o hook
  lança destacado e dois geradores podem sobrepor-se.
- **`pre-write-guard.py` e `pre-lens-order-check.py` não escrevem nada.** São guardas puras.
- **`on-su-change.py` não escreve directamente** — lança `dashboard.py` em
  `subprocess.Popen` destacado (L112).

### O ponto cego dos subprocessos está documentado no código

`on-su-change.py:38-40`, em comentário do próprio projecto:

> *engine's `finalize` writes with open() + os.replace() in a subprocess, which is
> filesystem I/O and not a tool call, so PostToolUse never fires on it.*

P0 registou isto como limite material inferido do wiring dos hooks. **Não era inferência:**
está escrito no código. Os seis hooks de escrita disparam em `Write|Edit`; nenhuma escrita
por subprocesso passa por eles.

### Mecanismos de coordenação que existem hoje

1. Escrita atómica **por ficheiro** (`atomic_write` do dashboard; `tmp → mv` declarado
   em 4 skills).
2. Um **lock**, só do `dashboard.py` (`_lock_path`, L7563/7579).
3. Hooks que só observam chamadas de ferramenta.

Nenhum destes dá atomicidade **entre** artefactos relacionados. Um lock de dashboard não
exclui escritas à SU nem a `_state.json`. É a lacuna que P2 tem de fechar, e agora está
medida em vez de suposta.

## Divergências herdadas de P0 — todas fechadas

| # | Item | Como fechou |
|---|---|---|
| 1 | Identidade dos inputs vs `SOURCE_MANIFEST.json` | Decisão do operador (2026-09-21): o conteúdo deste repositório **é** a versão actual e serve de baseline; o manifesto fica superado enquanto descrição das entradas. |
| 2 | `docs/FRAMEWORK-NEGOCIO.md` ausente | Fornecido e commitado (`d68459d`). Carrega `SCOPE-STATEMENT v1`; os 8 ficheiros de `SCOPE_FILES` passam. |
| 3 | `docs/CONSOLIDATED_PLAN.md` ausente | Fornecido e commitado (`d68459d`). Abre com errata datada 2026-09-11 — histórico com errata, não reescrito, como o critério exige. |
| 4 | `TOOL_VERSION` 1.13.0 vs 1.14.0 | Pino órfão, corrigido em `86221ba`. `coverage-phase-4-report.md` regista o bump `1.13.0 → 1.14.0` como deliberado da fase 4 e diz que o pino irmão em `test_blueprint_yaml.py` foi movido junto (está em `1.14.0`, L713). O `accept_phase1.py`, sendo da fase 1, ficou para trás. |

### Estado da aceitação

Corrida limpa das três fases contra a árvore corrigida, com os dois documentos no sítio e o
pino actualizado:

| Fase | Antes do fix de fronteira | Depois | Agora |
|---|---:|---:|---|
| `accept_phase1` | 2 critérios em falha | 1 | **exit 0 — todos passam** |
| `accept_phase2` | 5 | 4 | **exit 0 — todos passam** |
| `accept_phase3` | 2 | — | **exit 0 — todos passam** |

Terceiro modo de runner verde de ponta a ponta. Somado ao conjunto principal
(48/48 ficheiros, 2009 testes, 0 falhas), **os três modos de runner passam**.

## A «contradição» não existia — resolvida por leitura

A revisão anterior registou uma contradição entre o kernel e as skills: o kernel diz que
`chairman-synthesis` é o único escritor da Shared Understanding e que a escrita atómica de
`_state.json` é inviolável, enquanto o varrimento dava 7 candidatos a escritor de cada e só
4 skills a declarar `tmp → mv`.

Lidas as 24 skills uma a uma, **não há contradição**. O varrimento é que estava errado, nos
dois sentidos.

**Shared Understanding.** A regra do kernel é **por modo**, não global. Em Discovery
escrevem as 7 lentes, inline, uma linha por achado com `lens=<nome>`. Em Framing e Options
escreve `chairman-synthesis`, e só ele, append-only. Fora dos dois modos há exactamente
duas escritas mais, ambas declaradas: `aisa-start` cria o esqueleto (estrutura, não
conteúdo) e `aisa-status` actualiza o cabeçalho de saúde epistémica — a própria skill
chama-lhe «the one sanctioned write». Tudo o resto lê. `aisa-round` parecia escritor mas só
varre a SU para achar o próximo id livre por prefixo.

**`_state.json`.** São **6** escritores, não 7, e os **6** declaram escrita atómica, não 4:
`aisa-start`, `aisa-frame`, `aisa-options`, `aisa-decide`, `aisa-capture` e
`chairman-synthesis`. O varrimento contou listas de leitura como escrita e perdeu
`aisa-capture`, cujo verbo é *Increment* e não *escrever*. O princípio 8 do `CLAUDE.md`
está cumprido em todos os escritores declarados.

Fica a lição de método, que vale para o resto de P1: menção não é operação, e um cabeçalho
«Reads:» com dez caminhos produz dez falsos escritores em qualquer varrimento por verbos.

## O que P2 tem de acrescentar, agora delimitado

O alvo já tem as garantias **por artefacto**: `_state.json` atómico nos 6 escritores,
`coverage.py` com uma única porta de escrita confinada a `_coverage/`, `dashboard.py` com
escrita atómica e lock próprio, SU append-only. O que falta são três coisas, e nenhuma se
resolve com mais um hook de `Write|Edit`:

1. **Atomicidade entre artefactos** — uma operação toca SU + `_state.json` + `answers.md`;
   cada escrita é atómica por si, o conjunto não é.
2. **Exclusão para além do dashboard** — o único lock existente é do `dashboard.py`.
3. **Observação de escritas por subprocesso** — `PostToolUse` nunca dispara sobre elas,
   como o próprio código regista em `on-su-change.py:38-40`.

## Oráculos — extraídos, por validar

`docs/evolution/oracles/` · 22 itens · 13 críticos · método: leitura **directa** das fontes
(`openpyxl` com `data_only=False` para ler fórmulas, não valores em cache; `.vtt` em texto).
Nenhum artefacto de `_capture/` foi lido — o oráculo não pode derivar das conclusões do
candidato (`ACCEPTANCE.md` §5).

### `dpt-galp-jp-pilot-4` — tickets · 11 itens, 6 críticos

O mecanismo: reconciliação de **duas** fontes por `Ticket ID` — uma extracção diária volátil
(73 linhas) e um registo de prioridade manual durável (89 linhas). A vista de trabalho é
inteiramente derivada (103×10, tudo fórmula).

Factos que mais custam se se perderem:
- a prioridade é **juízo humano persistido**, não derivada da Severidade;
- o registo detecta tickets seus que desapareceram do export (`Live Status`), e o export
  mostra tickets sem prioridade em branco — **detecção de órfãos nos dois sentidos**;
- `Aging = TODAY() - INT(data)` é **volátil**, recalculado a cada abertura.

E o que a fonte não diz: dono e cadência do registo ficam `Unknown` — inferi-los seria
facto inventado.

### `pricing-bunkers-pilot-4` — Excel com regras · 11 itens, 7 críticos

18 folhas, **13 262 fórmulas**, 134 named ranges, VBA presente.

- As quatro folhas `usd_ton`/`eur_ton`/`usd_m3`/`eur_m3` partilham **249 de 249** padrões:
  são o mesmo cálculo em quatro apresentações. Tratá-las como quatro regras multiplica a
  estimativa por quatro.
- O preço decompõe-se em componentes nomeados por cliente × produto (Margem, Prémio,
  Transporte Barge/CT, Desconto, ISP, SLI…). Um preço escalar não representa isto.
- A origem é um **feed de mercado externo**: `UlyssesQuotes` traz `model://ECB_FX/`,
  `model://PLATTS_RI/`, `model://PLATTS_EB/`, `model://ICE_GASOIL/`.
- `Inputs` é série temporal de 1461 linhas — o histórico é mecanismo, não arquivo.

**A lacuna está declarada, não escondida.** `P-10` é `Unknown` **crítico**: a cadeia
aritmética através das 13 262 fórmulas não foi traçada. Traçada está a estrutura — named
ranges, simetrias, dimensões. A aritmética não. E o VBA existe e não foi descompilado
(`P-06`). Preferi declarar as duas lacunas a preencher com plausibilidade.

## Próxima acção concreta

**P1 fecha quando os 13 itens críticos forem validados.** Não marco GO antes disso: o
template proíbe GO com evidência por preencher, e a evidência que falta aqui não é minha
para produzir.

O que peço, por piloto, é confirmação ou correcção de cada item crítico. O mais valioso é
`P-10`: se o responsável explicar a ordem dos componentes no preço, fecha-se a maior lacuna
do piloto pesado sem traçar 13 mil fórmulas à mão.

Depois disso, **P2** — e o seu âmbito já está delimitado por `authority-map.md`: falta
atomicidade entre artefactos, exclusão para além do dashboard, e observação de escritas por
subprocesso. P2 leva 16 dos 61 casos.
