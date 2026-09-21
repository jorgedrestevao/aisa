# P0 — Estabelecer verdade do repositório

Estado: **GO**

## Identidade e precondições

- **Data/ambiente/runtime:** 2026-09-21 · Linux 6.18.44-fc-v37 x86_64 · Python 3.11.15
- **Commit de entrada e saída:** `e81d50da3cb0b7fdb5736033cb90d9b6ec8fd270` (entrada = saída; P0 não altera comportamento). Worktree limpo à entrada.
- **GO anterior e evidência:** N/A — P0 é a primeira fase.
- **Contratos/casos aplicáveis:** nenhum caso de `validation/cases.json` pertence a P0. P0 produz a base contra a qual K/W/B/L/M/C/U/E/S serão medidos.
- **Inputs do pacote:** `docs/AISA_Evolution_Plan.zip` (commit `e81d50d`), rev. 2, extraído para referência fora do repositório.

### Divergência de identidade face ao `SOURCE_MANIFEST.json`

O manifesto do pacote declara três ZIPs. Nenhum corresponde byte-a-byte ao que este
repositório recebeu. Registado, não resolvido:

| Papel | Manifesto | O que existe aqui |
|---|---|---|
| target | `aisa-rt-fix(1).zip`, 74 371 086 B | conteúdo aplicado a partir de um upload de 5 877 644 B |
| donor | `ai-solution-architect-main 2(2).zip`, 669 489 B | `ai-solution-architect-main.zip`, 2 548 035 B, 877 ficheiros |
| previous_plan | `AISA_Evolution_Plan(1).zip`, 19 198 B | não fornecido; rev. 2 substitui-o integralmente |

O alvo versionado tem 300 ficheiros tracked; o ZIP de 74 MB incluía muito provavelmente
`projects/` e caches, que `.gitignore` exclui. **NÃO VERIFICADO** — sem o ZIP original não
se calcula o diff. P1 tem de fixar a identidade antes de reutilizar qualquer conclusão do
pacote sobre o alvo.

## Nota pré-alteração

- **Problema e hipótese verificável:** não existe baseline reproduzível. Hipótese: o conjunto
  de testes corre integralmente e as falhas existentes são identificáveis e reproduzíveis.
- **Autoridades, leitores e escritores afetados:** nenhum. P0 é inventário e medição.
- **Comportamento esperado e risco:** zero alteração de comportamento. Risco: medir um
  baseline incompleto e tratá-lo como verde.
- **Recuperação/reversão:** os entregáveis são ficheiros novos em `docs/evolution/`;
  remover a pasta reverte P0 na totalidade.

## Alterações realizadas

- **Ficheiros e razão:** apenas entregáveis novos —
  `docs/evolution/P0-report.md`, `baseline-test-inventory.json`, `source-inventory.json`,
  `runtime-map.md`.
- **Comportamentos adicionados/alterados:** nenhum.
- **ADRs/mapeamentos:** nenhum (pertencem a P1).
- **Alterações intencionais de testes e garantia substituta:** nenhuma. Nenhum teste foi
  alterado, saltado ou desativado. O baseline não foi corrigido.

### Alterações de ambiente, declaradas

Instalados antes da medição, **não** presentes em `requirements-dev.txt`:
`pypdf 6.19.0`, `python-docx 1.2.0`, `cffi 2.1.1`, e `pytest 9.1.1` (runner auxiliar).

Sem os três primeiros, `library/kernel/tools/tests/test_text_extract.py` falha
(5 erros + 3 falhas) e o número de ficheiros a falhar seria **5, não 4**. É uma lacuna de
declaração de dependências, não uma correção de código: nenhum ficheiro de produto foi tocado.

## Verificação

| Runner/comando exato | Ambiente | Collected | Passed | Failed | Skipped | Xfail/Xpass | Errors | Duração | Log |
|---|---|---|---|---|---|---|---|---|---|
| `python3 <ficheiro>` para cada um dos 48 ficheiros (unittest, **autoritativo**) | Py 3.11.15 / Linux | 2009 | 1973 | 6 | 16 | 3 / 0 | 11 | ~9 min (timeout 180 s/ficheiro, nenhum atingido) | `baseline-test-inventory.json` + log por ficheiro |
| `python3 -m pytest .claude/tests library/kernel/tools/tests -q -p no:cacheprovider` (auxiliar) | Py 3.11.15 / Linux, pytest 9.1.1 | 2017 | 1975 (+181 subtests) | 17 | 22 | 3 / 0 | — | 195,6 s | output da execução |

Aritmética: unittest 1973 + 6 + 11 + 16 + 3 = 2009; pytest 1975 + 17 + 22 + 3 = 2017.
As contagens de skip diferem (16 vs 22) porque os dois modos classificam subtests e
skips condicionais de forma diferente; nenhum dos modos deixa ficheiro por correr.

Os dois modos foram executados. **Concordam nos mesmos 17 testes a falhar.**
Zero erros de colecção, zero timeouts. A diferença de contagem (2009 vs 2017) é de
contabilização de subtests, não de cobertura: ambos cobrem os 48 ficheiros.

> **Correção a uma leitura intermédia deste P0.** O `.pytest_cache` fornecido pelo operador
> listava 1444 node ids em 32 ficheiros, o que foi primeiro lido como pytest a não colher
> 16 ficheiros. Uma execução nova desmente-o: pytest colhe os 48. O cache estava
> desatualizado. Não existe ponto cego de runner.

### Runners descobertos

- **`python3 <ficheiro>`** — todos os 48 ficheiros têm bloco `if __name__ == "__main__": unittest.main(...)`.
  É o modo que o `requirements-dev.txt` declara («unittest, no pytest needed»).
- **`pytest`** — não declarado em `requirements-dev.txt`, mas usado pelo operador. Funciona.
- **Procurados e inexistentes:** `conftest.py`, `pytest.ini`, `tox.ini`, `Makefile`, scripts
  `run*.sh`, suites de aceitação externas, pastas `campaign*`. **Não há campanhas para classificar.**
- Motores (`coverage.py`, `dashboard.py`, …) têm CLI própria e são exercidos por subprocesso
  dentro dos testes; não constituem runner autónomo.

### Falhas baseline, individualmente

17 testes, 4 ficheiros. Reprodução: correr o ficheiro indicado. Classificadas:

**A — subárvore `docs/pp-pack-authoring/` ausente (12 testes)**
`test_pp_domain_knowledge.py`: `TestAuthoringAnnexes` (8) e `TestRepairIsRecorded` (3);
`test_step8c_semantic_continuity.py`: `Guards::test_step_8b_final_corrections_recorded` (1).
`FileNotFoundError` em `docs/pp-pack-authoring/research/...` e `.../pilot/step-8b-post-pilot-adjudication-report.md`.
**Entrada em falta, não defeito de código.** Os ficheiros nunca existiram neste repositório.

**B — patch de referência ausente (1 teste)**
`test_coverage_inventory.py::F16IsInstalled::test_the_patch_file_is_kept_as_the_record_of_the_change`
espera `docs/runtime-hardening/patches/f16-decision-ref-alias.patch`. Os outros três testes
da mesma classe passam: a correção **está instalada no leitor**; falta só o registo em ficheiro.

**C — defeito real, dependente de plataforma (3 testes)**
`test_coverage_inventory.py::EveryReadCrossesTheBoundary::test_it_is_reported_instead_of_ignored`,
`::LinkedMainSourcesAreRefused::test_a_linked_capture_directory_is_refused_and_reported`,
`::LinkedMainSourcesAreRefused::test_a_linked_lens_outputs_directory_is_refused`.
Em POSIX, uma ligação para fora do engagement é **corretamente excluída** do inventário
(o conteúdo de fora não entra), mas `build_inventory` **não emite o diagnóstico bloqueante**
e `inv["complete"]` fica `True`. Os testes foram escritos para junções Windows.
A fuga é silenciosa em Linux/mac. **Não corrigido em P0** (P0 não altera comportamento).

**D — exige dados de engagement (1 teste)**
`test_state_scaffold.py::TestNoMigration::test_a_pre_v23_su_still_exists_untouched`
varre `projects/` à procura de uma SU pré-v2.3. `projects/*` está em `.gitignore` e o
checkout tem zero engagements, por isso **nunca passa num clone limpo**.

- **Casos de aceitação → testes/evidência:** N/A em P0 — justificação: `cases.json` não
  atribui nenhum caso a P0.
- **Testes não executados e razão:** nenhum. Os 48 ficheiros correram nos dois modos.
- **Falhas baseline reproduzidas vs regressões novas:** todas as 17 são baseline. Zero
  regressões — P0 não alterou código.
- **Falhas injetadas, snapshots e recuperação:** N/A — pertencem a P2 (casos K/W).
- **Pilotos/oráculos e sessões reais:** N/A em P0; ver bloqueio abaixo.

## Resultado e limitações

### Observado vs esperado

Esperado um conjunto que corre por inteiro com falhas identificáveis. Confirmado: corre
por inteiro nos dois modos, sem timeouts nem erros de colecção, e as 17 falhas estão
classificadas por causa e reprodução.

### Âmbitos bloqueados

1. **P8 — pilotos.** `projects/*` está em `.gitignore`; o repositório versionado tem **zero**
   engagements e **zero** entradas de piloto. Os candidatos observados fora do versionamento
   (`PREÇO BANCAS_03_08_26.xlsm`, ~1,5 MB, e uma transcrição `.vtt` de reunião) chegaram num
   upload, não num commit. P8 exige **dois** pilotos distintos com oráculos preenchidos por
   inspeção independente da fonte; a `ACCEPTANCE.md` proíbe gerar o oráculo a partir do
   candidato. **Não desbloqueável por mim.**
2. **12 testes do grupo A + 1 do grupo B** não conseguem validar enquanto as subárvores
   `docs/pp-pack-authoring/` e `docs/runtime-hardening/patches/` não existirem. Ou são
   fornecidas, ou os testes que as exigem estão obsoletos e a decisão é de produto.
3. **1 teste do grupo D** depende do mesmo que (1).

### Limitações e impacto material

- Identidade dos inputs diverge do `SOURCE_MANIFEST.json` (secção 1). Conclusões do pacote
  sobre o alvo não são reutilizáveis sem o diff que P1 tem de produzir.
- O defeito do grupo C está numa garantia de fronteira de `coverage.py` — precisamente o
  mecanismo de que P6 depende. Fica registado como dívida conhecida, não como ruído.
- `requirements-dev.txt` não declara `pypdf` nem `python-docx`, exigidos por `text_extract.py`.
- Medido num só sistema operativo (Linux). Os testes do grupo C provam que o comportamento
  diverge entre POSIX e Windows; o baseline **não** cobre Windows.

### Métricas comparáveis

| Métrica | Valor na baseline |
|---|---:|
| Ficheiros tracked | 300 |
| Contratos do kernel (`library/kernel/*.md`) | 7 · 2271 linhas |
| Motores (`library/kernel/tools/*.py`) | 5 · 15 954 linhas |
| Packs | 4 |
| Comandos | 17 |
| Skills | 24 |
| Agentes | 8 |
| Hooks registados / ficheiros | 9 / 10 · 2289 linhas |
| Regras | 4 |
| Ficheiros de teste | 48 |
| Testes (unittest / pytest) | 2009 / 2017 |
| Stores persistentes | 0 (estado vive em ficheiros por engagement) |
| Engagements no checkout | 0 |

Latência/tokens: não observados — P0 não executou sessões de agente. Não inventados.

### GO/NO-GO e justificação por critério

| Critério de saída (P0) | Veredicto | Evidência |
|---|---|---|
| Todos os modos de teste descobertos executados | **Cumprido** | unittest per-file (48/48) + pytest 9.1.1 (48/48); tabela de verificação |
| Baseline recolhe as suites | **Cumprido** | 2009 / 2017 testes; zero erros de colecção |
| Mecanismos críticos executados | **Cumprido** | coverage (todas as etapas), dashboard, hooks, capture, replay, render/blueprint exercitados pelos 48 ficheiros |
| Falhas pré-existentes isoladas e documentadas | **Cumprido** | 17 testes, 4 grupos de causa, reprodução por ficheiro |
| Falhas não impedem provar trabalho posterior | **Cumprido com ressalva** | A/B/D são entradas em falta, não defeitos; C é defeito real mas isolado a uma garantia, com teste que o demonstra |
| Baseline não corrigido silenciosamente | **Cumprido** | zero ficheiros de produto alterados; instalações de ambiente declaradas |
| Runners, ambiente, entradas e falhas conhecidos | **Cumprido para runners/ambiente/falhas; parcial para entradas** | entradas de piloto ausentes e registadas como bloqueio de P8 |

**GO.** A baseline é reproduzível, completa em cobertura de ficheiros e honesta quanto ao
que falha e porquê. O único âmbito que arranca bloqueado é P8, e o bloqueio é de entrada
externa, não de engenharia — não impede P1 a P7.

### Próxima ação concreta

P1 — ligar contratos ao código: `authority-map.md`, `writer-reader-map.md`,
`integration-adr.md`, `test-map.json`, e fixar a identidade dos inputs face ao
`SOURCE_MANIFEST.json`.

Três pedidos ao operador, nenhum deles bloqueia o arranque de P1:

1. As subárvores `docs/pp-pack-authoring/` e `docs/runtime-hardening/patches/` existem
   noutro checkout? Se não existirem, os 13 testes dos grupos A e B ficam obsoletos e a
   retirada é decisão de produto.
2. Dois pilotos reais + acesso à fonte para construir os oráculos de P8, por inspeção
   independente.
3. Confirmação de que o alvo versionado é o alvo pretendido, apesar da divergência face ao
   `SOURCE_MANIFEST.json`.
