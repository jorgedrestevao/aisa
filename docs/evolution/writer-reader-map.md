# P1 — Mapa de escritores e leitores

Estado: **parcial**. A camada Python (motores + hooks) está verificada por AST e leitura
de cada linha detectada. A camada das skills está por verificar ficheiro a ficheiro; o que
aqui está marcado `CANDIDATO` vem de varrimento por verbos e **sobre-reporta**.

Método da camada verificada: `ast.walk` sobre cada `.py` à procura de `open(mode=w/a/x/+)`,
`write_text`, `write_bytes`, `mkdir`, `makedirs`, `os.replace`, `rename`, `unlink`,
`shutil.copy*`, `rmtree`; depois inspecção da linha de origem de **cada** ocorrência para
separar `str.replace` de `os.replace`. Sem essa segunda passagem o varrimento dá falsos
escritores — foi o que aconteceu na primeira tentativa, que marcou `dashboard.py` como
escritor da Shared Understanding e `coverage.py` como escritor de `_capture/`.

## 1. Motores — escrita verificada

| Motor | Escreve | Onde | Como |
|---|---|---|---|
| `coverage.py` | **só em `finalize`** | `<engagement>/_coverage/` e mais nada | `cdir.mkdir` (L3594), `md_path.write_text` (L3656), `unlink` de rascunhos (L3629/3648/3659/3660) |
| `dashboard.py` | `dashboard.html` | `<engagement>/` | `atomic_write` (L125-134): `makedirs` → `open(tmp,"w")` → `os.replace`. O nome do tmp leva o **pid**, porque o hook lança destacado e dois geradores podem sobrepor-se |
| `xlsx_extract.py` | artefactos L1/L3 | `_capture/` | 23 chamadas, padrão `makedirs` + `os.replace` |
| `text_extract.py` | artefactos LT | `_capture/` | 14 chamadas, mesmo padrão |
| `fields_draft.py` | rascunho de campos | `_capture/` | 5 chamadas, `write_text` + `replace` |

O contrato do kernel diz que `finalize` é a única operação de escrita do `coverage.py` e que
escreve só em `_coverage/`. **Confirmado no código**, não aceite por declaração.

`dashboard.py` tem ainda um **lock** (`_lock_path`, `unlink` em L7563/7579). É o único
mecanismo de exclusão que o alvo tem hoje. Material directo para P2: um lock de dashboard
**não** exclui escritas à SU nem a `_state.json`, que não passam por ele.

## 2. Hooks — escrita verificada

| Hook | Escreve? | O quê |
|---|---|---|
| `pre-write-guard.py` | **não** | guarda pura; o único `replace` é normalização de string (L60) |
| `pre-lens-order-check.py` | **não** | idem (L179) |
| `phase-gate-check.py` | sim | `gate-log.md` (`write_text`, L125) |
| `su-confirmed-guard.py` | sim | append a log (`open(log,"a")`, L106) |
| `synthesis-validate.py` | sim | ficheiro de verificação de síntese (`write_text`, L81) |
| `render-validate.py` | sim | lacunas de render (`mkdir` L514 + escrita) |
| `blueprint-validate.py` | não detectado | carrega `dashboard.py` por `runpy` (L47) |
| `on-su-change.py` | **não escreve directamente** | lança `dashboard.py` em `subprocess.Popen` destacado (L112) |
| `phase-completeness.py` | não detectado | `Stop` hook |
| `_common.py` | — | biblioteca; carrega `dashboard.py` por `runpy` (L46) |

## 3. O ponto cego dos subprocessos — já documentado no próprio código

`on-su-change.py`, linhas 38-40, em comentário:

> *engine's `finalize` writes with open() + os.replace() in a subprocess, which is
> filesystem I/O and not a tool call, so PostToolUse never fires on it; and the dashboard
> reads `_coverage/` and writes only `dashboard.html`, which is excluded below.*

Os seis hooks de escrita disparam em `Write|Edit`. Uma escrita feita por subprocesso —
`coverage.py finalize`, os extractores, qualquer script via Bash — **não passa por
`PostToolUse`**. Não é inferência deste mapa: está escrito no código.

Consequência para P2/P3: não existe hoje coordenador de operação. O que existe é
(a) escrita atómica por ficheiro, (b) um lock só do dashboard, (c) hooks que só vêem
chamadas de ferramenta. Nada disto dá atomicidade **entre** artefactos relacionados.

## 4. Camada das skills — `CANDIDATO`, por verificar

Varrimento por verbos sobre `.claude/skills/*/SKILL.md`. Conta menções, não operações:
uma skill que *descreve* o que outra escreve entra como escritora. **Não usar como
autoridade.** Serve só para dizer onde procurar.

| Artefacto | Candidatos a escritor | Menções de leitura |
|---|---:|---:|
| `shared-understanding.md` | 7 | 22 |
| `_state.json` | 7 | 19 |
| `decisions.md` | 10 | 11 |
| `story.md` | 11 | 5 |
| `council-log.md` | 14 | 4 |
| `lens-outputs/` | 10 | 12 |
| `answers.md` | 3 | 11 |
| `options.md` | 5 | 17 |
| `frame.md` | 5 | 12 |

Contradição por resolver: o kernel diz que em modo council-independent
`chairman-synthesis` é o **único** escritor da SU, e que a escrita atómica `tmp → mv` de
`_state.json` é princípio inviolável — mas só 4 skills declaram o padrão no texto.
Qual é o comportamento real de cada uma exige ler as 24, uma a uma. É o que falta.

## 5. O que falta para fechar este mapa

1. Ler as 24 skills e registar, por artefacto, a operação declarada (append / substituição /
   transição com `was`), não a menção.
2. Confirmar se os escritores de `_state.json` que não declaram `tmp → mv` o omitem de facto.
3. Ligar cada escritor a uma entrada de mutação, para o coordenador de operações de P2.
