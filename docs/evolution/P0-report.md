# P0 — Estabelecer verdade do repositório

Estado: **GO**

Revisão 2 — as três entradas que a revisão 1 registou como ausentes chegaram e foram
incorporadas. O baseline foi remedido de raiz contra o repositório completo.

## Identidade e precondições

- **Data/ambiente/runtime:** 2026-09-21 · Linux 6.18.44-fc-v37 x86_64 · Python 3.11.15
- **Commit de entrada:** `e81d50da3cb0b7fdb5736033cb90d9b6ec8fd270`
- **GO anterior:** N/A — P0 é a primeira fase.
- **Contratos/casos aplicáveis:** nenhum caso de `validation/cases.json` pertence a P0.
- **Pacote:** `docs/AISA_Evolution_Plan.zip`, rev. 2.

### Entradas recebidas durante P0

| Entrada | Destino | Versionado |
|---|---|---|
| `pp-pack-authoring.zip` | `docs/pp-pack-authoring/` — 160 ficheiros, 8,1 MB, 5 runners `.py` | sim |
| `runtime-hardening.zip` | `docs/runtime-hardening/` — 44 ficheiros, 0,5 MB, 11 runners `.py` | sim |
| `pilots.zip` | `projects/` — 4 engagements com entradas reais | **não** (`projects/*` em `.gitignore`; contém dados de cliente) |

Ambos os ZIPs de `docs/` chegaram em duas versões. A segunda de `runtime-hardening`
acrescenta `patches/`, os relatórios de fase e os scripts `repro-*`. A segunda de
`pp-pack-authoring` é a primeira **menos** `research/pp-framework/` (371 ficheiros),
sem nada acrescentado; nenhum teste lê essa pasta. Ficaram as segundas versões.

### Divergência de identidade face ao `SOURCE_MANIFEST.json`

Nenhum dos três ZIPs do manifesto corresponde byte-a-byte ao que este repositório recebeu:

| Papel | Manifesto | Aqui |
|---|---|---|
| target | `aisa-rt-fix(1).zip`, 74 371 086 B | upload de 5 877 644 B |
| donor | `ai-solution-architect-main 2(2).zip`, 669 489 B | `ai-solution-architect-main.zip`, 2 548 035 B, 877 ficheiros |
| previous_plan | `AISA_Evolution_Plan(1).zip`, 19 198 B | não fornecido |

**RESOLVIDO por decisão do operador (2026-09-21).** O conteúdo que este repositório tem
**é** a versão actual, e é adoptado como baseline; o `SOURCE_MANIFEST.json` fica
superado enquanto descrição das entradas. A identidade do alvo passa a ser o commit
deste repositório e os sha256 por ficheiro em `source-inventory.json`. P1 deixa de dever
o diff contra os ZIPs do manifesto.

Não resolve a divergência de `TOOL_VERSION`: os dois ficheiros em causa são ambos
actuais, logo é uma inconsistência **dentro** do baseline, não desfasamento de checkout.

## Nota pré-alteração

- **Problema e hipótese verificável:** não existe baseline reproduzível. Hipótese: o
  conjunto corre integralmente e as falhas são identificáveis e reproduzíveis.
- **Autoridades, leitores e escritores afetados:** nenhum. P0 é inventário e medição.
- **Comportamento esperado e risco:** zero alteração de comportamento. Risco: medir um
  baseline incompleto e tratá-lo como verde.
- **Recuperação/reversão:** os entregáveis são ficheiros novos em `docs/evolution/`.

## Alterações realizadas

- **Ficheiros e razão:** entregáveis novos em `docs/evolution/` (`P0-report.md`,
  `baseline-test-inventory.json`, `source-inventory.json`, `runtime-map.md`), mais as duas
  subárvores de apoio recebidas como entrada.
- **Comportamentos adicionados/alterados:** nenhum. Nenhum ficheiro de produto foi tocado.
- **Alterações intencionais de testes:** nenhuma. Nenhum teste foi alterado, saltado ou
  desativado. O baseline não foi corrigido silenciosamente.

### Alterações de ambiente, declaradas

Instalados antes de medir, ausentes de `requirements-dev.txt`: `pypdf 6.19.0`,
`python-docx 1.2.0`, `cffi 2.1.1`, e `pytest 9.1.1` como runner auxiliar.
Sem os três primeiros, `test_text_extract.py` falha (5 erros + 3 falhas).
É lacuna de declaração de dependências, não correção de código.

## Verificação

| Runner/comando exato | Ambiente | Collected | Passed | Failed | Skipped | Xfail | Errors | Duração | Log |
|---|---|---|---|---|---|---|---|---|---|
| `python3 <ficheiro>` × 48 (unittest, **autoritativo**) | Py 3.11.15 / Linux | 2009 | 1990 | 3 | 13 | 3 | 0 | timeout 300 s/ficheiro, nenhum atingido | `baseline-test-inventory.json` + log por ficheiro |
| `python3 -m pytest .claude/tests library/kernel/tools/tests -q` (auxiliar) | idem, pytest 9.1.1 | 2017 | 1950 (+181 subtests) | 3 | 9 | 3 | — | 191,35 s | via `accept_phase1.py` |
| `python3 docs/runtime-hardening/accept_phase1.py` (aceitação) | idem | — | — | 2 critérios | — | — | — | — | output da execução |

Aritmética: 1990 + 3 + 13 + 3 = 2009. Zero erros de colecção, zero timeouts.
As diferenças de skip entre modos são de classificação de subtests, não de cobertura:
ambos cobrem os 48 ficheiros.

### Runners descobertos — **três modos, não dois**

1. **`python3 <ficheiro>`** — os 48 ficheiros têm bloco `__main__`. Modo declarado no
   `requirements-dev.txt`. Autoritativo.
2. **`pytest`** — não declarado, mas usado pelo operador. Colhe os 48 ficheiros.
3. **Scripts de aceitação** — `docs/runtime-hardening/accept_phase1..3.py`. Correm contra os
   engagements reais em `projects/`, não escrevem, saem 0/1. **Só existiram depois de as
   entradas chegarem**; a revisão 1 deste relatório não os podia ter descoberto.

Registados e **não executados**, com razão:
- 8 scripts `docs/runtime-hardening/repro-*.py` — são ensaios que **escrevem** em
  `docs/review-evidence/`. P0 não altera nada.
- 5 scripts em `docs/pp-pack-authoring/pilot/**` (`accept_frente_b/c.py`, `accept_p14_runs.py`,
  `tools/`) — aceitação do lado da autoria do pack, fora do âmbito de P0. P1 mapeia-os.

Procurados e inexistentes: `conftest.py`, `pytest.ini`, `tox.ini`, `Makefile`, `run*.sh`,
pastas `campaign*`. **Não há campanhas para classificar.**

### Resultado de `accept_phase1.py`

Sai 1, com dois critérios em falha:

1. **`suite verde`** — pelas 3 falhas abaixo, e só por elas.
2. **`motor em 1.13.0`** — `accept_phase1.py:387` afirma `TOOL_VERSION == "1.13.0"`;
   `library/kernel/tools/dashboard.py:44` define `TOOL_VERSION = "1.14.0"`. **O script de
   aceitação está atrasado face ao motor**, não o inverso. Qual dos lados está certo — o
   script por atualizar, ou um bump de motor sem atualizar a aceitação — **NÃO ESTÁ
   DETERMINADO**. Fica para P1.

### Resultado de `accept_phase1..3.py`

Os três correram contra os quatro engagements reais. Todos saíram 1. Medidos **antes** da
correção de fronteira, por isso `suite verde` reflecte as 3 falhas POSIX, e os critérios
«fase N continua verde (regressão)» são consequência dessa mesma falha, não achados novos.

| Script | Critérios em falha |
|---|---|
| `accept_phase1.py` | `motor em 1.13.0`; `suite verde` |
| `accept_phase2.py` | `docs/FRAMEWORK-NEGOCIO.md: tem SCOPE-STATEMENT v1`; `CONSOLIDATED_PLAN tem errata`; `suite verde`; fase 1 e fase 3 continuam verdes |
| `accept_phase3.py` | `suite verde`; fase 1 continua verde |

Descontando `suite verde` e as regressões que dela derivam, sobram **três** critérios reais,
e dois deles são entradas em falta que só este modo de runner revelou:

1. **`docs/FRAMEWORK-NEGOCIO.md` não existe** (`accept_phase2.py:59`).
2. **`docs/CONSOLIDATED_PLAN.md` não existe** (`accept_phase2.py:172`, que procura `Errata`).
3. **Divergência de versão do motor**, acima.

Nenhum dos três foi inventado nem contornado. Os dois documentos juntam-se à lista de
entradas por fornecer; ao contrário das anteriores, **não bloqueiam nenhum teste do conjunto
principal** — só o critério de aceitação da fase 2.

### Falhas baseline: 17 → 3

Treze fecharam quando as entradas chegaram. Nenhuma por alteração de código:

| Grupo | Testes | Entrada que resolveu |
|---|---:|---|
| A | 12 | `docs/pp-pack-authoring/` (`research/pp/authoring/`, `pilot/step-8b-*`) |
| B | 1 | `docs/runtime-hardening/patches/f16-decision-ref-alias.patch` |
| D | 1 | `projects/` com 4 engagements (havia SU pré-v2.3 para encontrar) |

O patch do grupo B confirma o que a revisão 1 já tinha concluído: a correção **está
instalada no leitor** (`bp_decision_id` normaliza `decision_ref` e `concretizes_decision`);
faltava só o registo em ficheiro.

**Restam 3, todas em `.claude/tests/test_coverage_inventory.py`:**

- `EveryReadCrossesTheBoundary::test_it_is_reported_instead_of_ignored`
- `LinkedMainSourcesAreRefused::test_a_linked_capture_directory_is_refused_and_reported`
- `LinkedMainSourcesAreRefused::test_a_linked_lens_outputs_directory_is_refused`

**Defeito de código real, dependente de plataforma.** Em POSIX, uma ligação para fora do
engagement é **corretamente excluída** do inventário — nenhum conteúdo de fora entra — mas
`build_inventory` **não emite o diagnóstico bloqueante** e `inv["complete"]` fica `True`.
Os testes foram escritos para junções Windows. Em Linux/mac a fuga é silenciosa.

**Não corrigido em P0**, por definição da fase. Corrigido imediatamente a seguir, em
alteração autónoma, com estes três testes como especificação.

- **Casos de aceitação → evidência:** N/A — `cases.json` não atribui casos a P0.
- **Testes não executados e razão:** ver *Runners descobertos*; nenhum ficheiro do conjunto
  principal ficou por correr.
- **Falhas baseline vs regressões novas:** as 3 são baseline. Zero regressões — P0 não
  alterou código.
- **Falhas injetadas, snapshots, recuperação:** N/A — pertencem a P2 (casos K/W).
- **Pilotos/oráculos e sessões reais:** entradas disponíveis (abaixo); oráculos pertencem a P1.

## Resultado e limitações

### Âmbitos bloqueados

**Nenhum bloqueio de entrada permanece.** Os quatro engagements cobrem os dois tipos que
P8 exige:

| Engagement | Entrada | Tipo P8 |
|---|---|---|
| `dpt-galp-jp-pilot-4` | `Dayly_pending_tickets_Anonimo.xlsx` | operacional/tickets |
| `pricing-bunkers-pilot-4` | `PREÇO BANCAS_03_08_26.xlsm` + `.vtt` | Excel com regras e dependências |
| `kam-onboarding-pilot-4` | `.pdf` + `.txt` + perguntas ao sponsor | — |
| `cae-automation-pilot-4` | `.docx` + análise | — |

Os **oráculos continuam por construir**: `ACCEPTANCE.md` exige preenchimento por inspeção
independente da fonte e proíbe gerá-los a partir do candidato. É trabalho de P1, com acesso
à fonte e, quando preciso, confirmação do responsável.

### Limitações e impacto material

- Identidade dos inputs diverge do `SOURCE_MANIFEST.json`; conclusões do pacote sobre o
  alvo não são reutilizáveis sem o diff de P1.
- Divergência de versão do motor por adjudicar (1.13.0 vs 1.14.0).
- O defeito das 3 falhas está na garantia de fronteira de `coverage.py` — o mecanismo de
  que P6 depende.
- `requirements-dev.txt` não declara `pypdf` nem `python-docx`.
- Medido só em Linux. Os próprios testes que falham provam que o comportamento diverge
  entre POSIX e Windows; o baseline **não** cobre Windows.
- `projects/` fica fora do versionamento por decisão explícita: contém dados de cliente.
  Consequência aceite: um clone limpo não reproduz o grupo D sem receber os pilotos.

### Métricas comparáveis

| Métrica | Baseline |
|---|---:|
| Ficheiros tracked (antes das subárvores) | 300 |
| Contratos do kernel | 7 · 2271 linhas |
| Motores (`library/kernel/tools/*.py`) | 5 · 15 954 linhas |
| Packs / Comandos / Skills / Agentes / Regras | 4 / 17 / 24 / 8 / 4 |
| Hooks registados / ficheiros | 9 / 10 · 2289 linhas |
| Ficheiros de teste | 48 |
| Testes (unittest / pytest) | 2009 / 2017 |
| Runners distintos | 3 modos |
| Stores persistentes | 0 (estado em ficheiros por engagement) |
| Engagements disponíveis | 4 (não versionados) |

Latência/tokens: não observados — P0 não executou sessões de agente. Não inventados.

### GO/NO-GO e justificação por critério

| Critério de saída (P0) | Veredicto | Evidência |
|---|---|---|
| Todos os modos de teste descobertos executados | **Cumprido** | 3 modos; os não executados estão nomeados com razão (escrevem, ou são de outro âmbito) |
| Baseline recolhe as suites | **Cumprido** | 2009 / 2017 testes; zero erros de colecção |
| Mecanismos críticos executados | **Cumprido** | coverage nas três etapas, dashboard, hooks, capture, replay, render/blueprint |
| Falhas pré-existentes isoladas e documentadas | **Cumprido** | 3 testes nomeados, causa única, reprodução por ficheiro |
| Falhas não impedem provar trabalho posterior | **Cumprido** | causa única e delimitada; corrigida a seguir, fora de P0 |
| Baseline não corrigido silenciosamente | **Cumprido** | zero ficheiros de produto alterados; instalações declaradas |
| Runners, ambiente, entradas e falhas conhecidos | **Cumprido** | entradas de piloto presentes; oráculos remetidos para P1 |

**GO.** O baseline é reproduzível, cobre os 48 ficheiros em três modos, e tem uma única
falha de causa conhecida. Nenhum âmbito arranca bloqueado por falta de entrada.

### Próxima ação concreta

1. **Antes de P1**, em alteração autónoma: corrigir o defeito de fronteira em POSIX.
   Razão para não deixar para P2/P6: baseline vermelho cega a comparação por ID em todas as
   fases seguintes, e `accept_phase1` trata `suite verde` como critério de aceitação.
2. **P1** — `authority-map.md`, `writer-reader-map.md`, `integration-adr.md`,
   `test-map.json`; fixar identidade face ao `SOURCE_MANIFEST.json`; adjudicar a divergência
   de versão do motor; construir os oráculos dos pilotos por inspeção independente.
