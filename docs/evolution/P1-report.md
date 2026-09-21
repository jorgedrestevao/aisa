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
| `writer-reader-map.md` | **parcial** — camada Python verificada; camada das skills por ler |
| `authority-map.md` | por fazer |
| `integration-adr.md` | **parcial** — ADR-001 (linguagem de runtime) aceite; falta o mapeamento módulo a módulo do doador |
| `test-map.json` | por fazer |
| Oráculos dos 2 pilotos | por fazer |

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

## Contradição registada, por resolver

O kernel declara que em modo council-independent `chairman-synthesis` é o **único** escritor
da Shared Understanding, e que a escrita atómica de `_state.json` é princípio inviolável.
O varrimento das skills dá 7 candidatos a escritor da SU e 7 de `_state.json`, dos quais só
4 declaram `tmp → mv` no texto.

O varrimento **sobre-reporta** e não serve de prova. Resolver exige ler as 24 skills uma a
uma e registar a operação declarada, não a menção. É o próximo passo.

## Próxima acção concreta

1. Ler as 24 skills; fechar `writer-reader-map.md` e produzir `authority-map.md`.
2. `integration-adr.md` — **ADR-001 fechado**: Python stdlib-only, Node fora, com medição
   (arranque 19,0 ms vs 41,9 ms; ~114 ms de hooks por escrita) e o núcleo portável do
   doador inventariado em 2917 linhas. Falta o mapeamento módulo a módulo contra o alvo,
   com os casos não equivalentes nomeados.
3. `test-map.json` — ligar os 61 IDs de `cases.json` a fases e testes.
4. Oráculos dos dois pilotos, por inspecção independente da fonte.

### Limitação a declarar já, sobre os oráculos

`ACCEPTANCE.md` exige que o oráculo **não** seja gerado a partir das conclusões do candidato.
Ler os ficheiros de origem directamente satisfaz a letra da regra. Mas quem constrói o
oráculo e quem opera o candidato seriam, aqui, o mesmo agente — o que enfraquece a
independência mesmo respeitando o procedimento. Os itens críticos devem ser validados pelo
responsável do processo antes de contarem como referência. Isto fica dito antes de haver
resultado, não depois.
