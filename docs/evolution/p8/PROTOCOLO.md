# P8 — protocolo de execução (E01/E02/E03)

> Quem executa: **o operador**, em sessões Claude Code reais.
> Quem julga: **`compare.py`**, por código.
>
> Esta separação não é cerimónia. `ACCEPTANCE.md` §1 proíbe «criar um ficheiro com o mesmo
> nome ou imprimir PASS», e §5 proíbe «gerar a referência a partir das conclusões do
> candidato». Quem construiu o mecanismo não pode ser quem o aprova em prosa.

---

## 0. O que já está fechado sem ti

| Caso | Estado | Onde |
|---|---|---|
| **E03** Referência independente | Fechado em P1 | Oráculos extraídos da fonte e validados pelo dono **antes** de existir candidato |
| **E04** Inspeção completa | Fechado | `.claude/tests/test_graph_inspection.py` (22 testes) + `graph.py inspect\|export` |
| **E05** Limites de extração | Fechado | `.claude/tests/test_extraction_limits.py` (14 testes), incluindo o livro real |

Falta **E01** (sessões reais) e **E02** (dois pilotos contra oráculos). Nenhum dos dois se
fecha sem um humano a abrir e fechar sessões.

**Corridas feitas até agora** (2026-09-23):

| Engagement | Checkpoint | Corrida | Veredicto | Conta? |
|---|---|---|---|---|
| `pricing-bancas-marinha` | `cp1-discovery` | r1 | NO-GO, 5 críticos (`LOST_CRITICAL` A-001..A-005) | **Não** — ver abaixo |

A r1 não mede o kernel, por dois defeitos do harness e do kernel, ambos corrigidos em
`master@073739a`:

1. o formulário do §2.3 não tinha campo para `Assumed` e o juiz exigia-o (`d02f9a3`);
2. o Discovery bloqueava na segunda escrita de uma lente — nada espelhava no grafo o que as
   lentes escrevem pela ferramenta Edit (`073739a`).

**Nenhuma corrida feita antes de `073739a` conta.** `cp1-discovery` repete-se (§2.5).

---

## 1. Antes de começar

```bash
git pull origin master          # o kernel medido tem de ser, no mínimo, 073739a
mkdir -p docs/evolution/p8/runs/<slug>
```

Regra que não se contorna: **cada braço comparável usa um engagement novo** (§6). Não se
reaproveita um engagement já mexido para um segundo braço — o resultado deixa de ser
atribuível. Por isso o slug do braço **não** é o do piloto de origem:

| Piloto de origem (oráculo) | Engagement do braço E01 |
|---|---|
| `pricing-bunkers-pilot-4` | `pricing-bancas-marinha` *(presumido pelo nome — confirmar abaixo)* |
| `dpt-galp-jp-pilot-4` | *por criar* |

Os oráculos ficam com o nome do piloto de **origem** — são da fonte, não do engagement
(§5). **O `compare.py oracle` não verifica que o braço usa a fonte do oráculo**: essa
correspondência confirma-se à mão, antes de E02, comparando o sha do input do braço com
`authoritative_source.sha256` do oráculo:

```bash
python -c "import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" \
  "projects/<slug>/inputs/<ficheiro>"
```

Sha diferente = o braço não mede contra aquele oráculo, e E02 não se corre com ele.

**Windows.** Os comandos abaixo escrevem `python3`; no Windows é `python`. O projecto corre
o Python em modo UTF-8 (`PYTHONUTF8=1` no `env` de `.claude/settings.json`), mas o
`settings.json` só é lido quando a sessão **arranca**: depois de um `git pull` que o
mude, fechar e reabrir o Claude Code. Numa consola fora do Claude Code, definir à mão:
`$env:PYTHONUTF8 = "1"`.

---

## 2. O ciclo, por engagement

Sequência obrigatória (§6), com reinício de sessão **a cada seta**:

```
Capture/Discovery → resolução → Frame → Options → Premortem/Simulation → Decide → Blueprint → Render
```

São **7 pontos de reinício**, um no fim de cada etapa antes do Render. O nome do
checkpoint é **este**, sempre — o `compare.py` agrupa por ele, e um nome que muda de
corrida para corrida (`cp1-capture`, `cp1-disocvery`) parte a comparação sem erro nenhum:

| Checkpoint | Congela-se no fim de |
|---|---|
| `cp1-discovery` | Capture/Discovery |
| `cp2-resolution` | resolução das perguntas |
| `cp3-frame` | `/frame` |
| `cp4-options` | `/options` |
| `cp5-premortem` | `/premortem` · `/simulate` |
| `cp6-decide` | `/decide` |
| `cp7-blueprint` | `/blueprint` |

O Render é a última etapa e não tem reinício depois dele. Em cada checkpoint:

### 2.1 Antes de fechar a sessão — congelar a verdade

```bash
python3 docs/evolution/p8/compare.py truth \
  --engagement <slug> \
  --checkpoint cp<N>-<nome> \
  --out docs/evolution/p8/runs/<slug>/
```

Isto lê os ficheiros do engagement e escreve `cp<N>-<nome>.truth.json`. É o alvo imóvel.
Faz-se **antes** de reabrir, nunca depois — depois já não é verdade, é memória.

### 2.2 Fechar a sessão a sério

Fechar mesmo. Sem `--continue`, sem `--resume`, sem colar um resumo da sessão anterior.
Uma sessão que recebe o resumo não prova recuperação nenhuma.

### 2.3 Reabrir e pedir isto, literalmente

> No engagement `<slug>`, sem que eu te dê qualquer contexto anterior: reconstrói o estado
> usando apenas os mecanismos do projecto. Depois devolve **só** um bloco JSON com estes
> campos, usando os ids reais que encontrares:
>
> ```json
> {
>   "engagement": "<slug>",
>   "checkpoint": "cp<N>-<nome>",
>   "phase": "<fase>",
>   "facts": [{"id": "C-001", "state": "Confirmed"}],
>   "assumptions": [{"id": "A-001", "state": "Assumed"}],
>   "open_questions": [{"id": "U-002", "state": "Unknown"}],
>   "risks": [{"id": "R-003", "state": "Risky"}, {"id": "X-004", "state": "Conflicted"}],
>   "decisions": [{"id": "D-001"}],
>   "coverage": {"status": "<fresh|stale|absent>"},
>   "blockers": [{"id": "U-002"}],
>   "next_step": "/comando args",
>   "recovered_via": ["bootstrap", "graph"]
> }
> ```
>
> Cada linha vai para o campo do seu estado: `Confirmed` → `facts`, `Assumed` →
> `assumptions`, `Unknown` → `open_questions`, `Risky` e `Conflicted` → `risks`. Em
> `blockers` entra o que bloqueia, seja qual for o estado.
>
> Não inventes ids. Se não encontrares algo, deixa a lista vazia — uma lista vazia é uma
> resposta; um id inventado não é.
>
> Em `recovered_via`, diz **por que mecanismos** reconstruíste, com honestidade brutal: se
> leste `shared-understanding.md` directamente, escreve isso. Não escrevas `bootstrap` se
> não o correste.

**Porque é que há um campo por estado.** A primeira corrida real (`cp1-discovery`) deu
NO-GO com 5 críticos — `LOST_CRITICAL` sobre A-001..A-005 — e a sessão não tinha perdido
nada. Este formulário só tinha `facts` e `open_questions`; o `compare.py` exigia recuperar
linhas materiais em cinco estados. A sessão seguiu o formulário à letra e reprovou por isso.
Pior: o juiz não olhava ao campo, só ao id e ao estado, e uma sessão que desobedecesse
(Assumed em `facts`) passava. Agora o juiz lê os quatro campos, e o estado certo na gaveta
errada é `FIELD_MISMATCH` — aviso, não crítico, porque arrumar mal não é perder.

**A correcção que NÃO se faz:** copiar as linhas em falta do `truth.json` para o report.
Isso é preencher o candidato a partir da referência (`ACCEPTANCE.md` §5) e dá GO sem medir
coisa nenhuma. Um report produzido sob um formulário partido não se edita: guarda-se como
corrida N no `.notes.md`, com a causa, e o checkpoint repete-se numa sessão nova contra o
**mesmo** `truth.json` — que continua válido, porque foi congelado antes.

**Porque é que `recovered_via` existe.** Sem ele o comparador mede ids recuperados e dá GO —
mesmo quando a recuperação veio de ler a SU à moda antiga, que é exactamente o que E01
existe para **não** dar por provado. Agora `truth` regista por que caminho o engagement se
reconstrói (`kernel.mode`: `graph` · `legacy` · `blocked`) e o `check` cruza-o com o que a
sessão declara:

| situação | achado | gravidade |
|---|---|---|
| bootstrap em modo legacy | `LEGACY_PATH` | crítico |
| bootstrap não pronto | `KERNEL_BLOCKED` | crítico |
| sessão diz «bootstrap», mas estava legacy | `PROVENANCE_MISMATCH` | crítico |
| `recovered_via` ausente | `PROVENANCE_UNDECLARED` | aviso |
| reconstrução sem mecanismo do kernel | `PROVENANCE_OUTSIDE_KERNEL` | aviso |

> Um engagement criado com o kernel actual nasce com grafo (`migrate.py init`, chamado por
> `/start`) e as escritas das lentes são espelhadas pelo hook `on-su-mirror.py`. `LEGACY_PATH`
> numa corrida nova é, por isso, um defeito a reportar — não o estado esperado.

Gravar como `docs/evolution/p8/runs/<slug>/cp<N>-<nome>.report.json`.

Registar também, num `.notes.md` ao lado: modelo e configuração se acessíveis, **o commit
do kernel medido** (`git rev-parse --short HEAD`), o sistema operativo, e **os campos que
não se conseguiram observar** (§6 exige-o por escrito). Sem o commit não há como saber,
depois, se a corrida mediu um kernel que já tinha o defeito corrigido.

### 2.4 Comparar

```bash
python3 docs/evolution/p8/compare.py check \
  --truth  docs/evolution/p8/runs/<slug>/cp<N>-<nome>.truth.json \
  --report docs/evolution/p8/runs/<slug>/cp<N>-<nome>.report.json \
  --out    docs/evolution/p8/runs/<slug>/cp<N>-<nome>.verdict.json
```

Sai `0` em GO, `1` em NO-GO. O que ele procura:

| Achado | Gravidade | Significa |
|---|---|---|
| `INVENTED` / `INVENTED_DECISION` | crítico | id que não existe em lado nenhum |
| `FALSE_CONFIRMED` | crítico | disse Confirmed onde a SU tem Unknown/Assumed |
| `LOST_CRITICAL` / `LOST_DECISION` | crítico | perdeu linha dimensionante ou decisão tomada |
| `UNDUE_ADVANCE` | crítico | propõe `/frame`, `/decide`… com o gate fechado |
| `PHASE_MISMATCH` | crítico | fase reportada ≠ fase nos ficheiros |
| `REPORT_INCOMPLETE` | crítico | a resposta não traz os campos pedidos |
| `LOST` / `STATE_DRIFT` | aviso | perda ou desvio não material |
| `FIELD_MISMATCH` | aviso | estado certo, campo errado (ex.: Assumed em `facts`) |

### 2.5 Repetir um checkpoint

Quando uma corrida não mede o que devia — defeito do harness ou do kernel, corrigido
depois —, o checkpoint repete-se. Nunca se edita o report.

1. Mover **os ficheiros da corrida** (report, verdict, notes) para
   `runs/<slug>/_superseded/r<N>/`, com uma linha no `.notes.md` a dizer a causa e o
   commit que a corrigiu.
2. **O `truth.json` fica onde está.** Foi congelado antes da sessão, e é por isso que
   continua válido — é o mesmo alvo para a corrida nova.
3. Abrir uma sessão nova, fechada a sério (§2.2), e voltar a §2.3.
4. `compare.py check` com o mesmo `--truth` e o report novo.

O `summary` não conta o que está em `_superseded/`, mas diz quantas são. E uma corrida
substituída **sem** corrida activa do mesmo engagement e checkpoint é crítica
(`superseded_without_rerun`): esconder uma corrida falhada não é repeti-la.

---

## 3. Os dois reinícios extra (§6)

Além dos 7 pontos, a aceitação pede mais dois:

1. **Reinício depois de erro.** Provocar uma falha (fechar a meio de um comando), reabrir,
   pedir o mesmo JSON. Esperado: a sessão vê a operação pendente e **não avança**.
2. **Reinício depois de fonte actualizada.** Trocar o ficheiro de input por uma versão
   diferente, reabrir. Esperado: a sessão reporta a fonte como mudada, não como igual.

---

## 4. Fuga entre engagements

Trabalhar um engagement, fechar, abrir o outro, pedir o JSON. Nenhum id do primeiro pode
aparecer no segundo.

```bash
python3 docs/evolution/p8/compare.py leak \
  --truth-other docs/evolution/p8/runs/<slug-a>/cp7-blueprint.truth.json \
  --report      docs/evolution/p8/runs/<slug-b>/cp1-discovery.report.json \
  --out         docs/evolution/p8/runs/<slug-b>/leak.verdict.json
```

E ao contrário, nos dois sentidos.

---

## 5. E02/E03 — a extração contra o oráculo

O oráculo está congelado e validado. O que falta é a **correspondência**: que linha da SU
responde a cada item do oráculo. Essa correspondência é declarada pelo **candidato**, não
por quem avalia — adivinhá-la aqui seria construir a referência a partir do candidato.

Pedir à sessão:

> Para cada item do oráculo (`T-01`…`T-11` / `P-01`…`P-14`), diz que linha da SU o cobre.
> Formato `{"T-01": "C-004", "T-02": null}`. `null` quando nenhuma linha o cobre — não
> forces uma correspondência.

Gravar como `runs/<slug>/mapping.json` e correr:

```bash
python3 docs/evolution/p8/compare.py oracle \
  --engagement <slug> \
  --oracle  docs/evolution/oracles/<piloto-de-origem>.oracle.json \
  --mapping docs/evolution/p8/runs/<slug>/mapping.json \
  --out     docs/evolution/p8/runs/<slug>/oracle.verdict.json
```

O oráculo tem o nome do piloto de **origem** (§1). O `--engagement` é o braço; o
`--oracle` é a fonte — e que são a mesma fonte confirma-se pelo sha (§1), porque este
comando não o verifica.

Mede os três números que o próprio oráculo declara em `acceptance`:

| Métrica | Limiar | O que reprova |
|---|---|---|
| `critical_recall` | `1.0` | um item crítico sem correspondência |
| `critical_false_confirmed` | `0` | afirmar Confirmed onde o oráculo diz Unknown |
| `improper_gate_advances` | `0` | gate aberto com críticos por resolver |

---

## 6. O agregado

```bash
python3 docs/evolution/p8/compare.py summary --runs docs/evolution/p8/runs/
```

Sem ficheiros em `runs/`, devolve `SEM EXECUÇÃO` — **não** devolve GO. Um P8 sem sessões
reais não é um P8 verde; é um P8 por fazer.

---

## 7. O input de pricing — resolvido, com um passo por fazer

**Resolvido a 2026-09-22.** O ficheiro autoritativo entrou e está verificado:

```
projects/pricing-bunkers-pilot-4/inputs/PREÇO BANCAS_03_08_26.xlsx
sha256 cf40be3ed65983d51e689d9d34ba1714fdb204794d34e89352be667be1692b52
19 folhas · com Motor, Relatório Preços, Relatório Preços Bios · sem VBA
```

Bate campo a campo com `authoritative_source` do oráculo (sha, contagem de folhas,
`has_vba: false`). Os locators da especificação (`Motor!C24:H24`, `Relatorio!B5`) resolvem
aqui — não resolviam no `.xlsm`.

O `.xlsm` substituído (sha `677e7963…`, 18 folhas, com VBA) foi para
`inputs/_superseded/`, com um `README.md` a dizer porquê. Não foi apagado: é a única fonte
**real** com `vbaProject.bin` e é sobre ela que E05 afirma que o motor declara macros sem
as inventar. Está fora de `inputs/` para que `/capture` não processe as duas versões.

> **Facto que sobreviveu à troca:** os dois livros fazem as **mesmas 176 chamadas
> `_xll.Storm`**. O motor de preço depende de código de add-in que não está em nenhum dos
> ficheiros. Isto é fronteira declarada, não omissão, e limita o que se pode afirmar sobre
> o cálculo a partir do livro — em qualquer das versões.

### O passo que falta

O `/capture` sobre o `.xlsx` corre dentro de `cp1-discovery`, numa sessão real — por
decisão do operador: pré-correr punha parte do ciclo medido fora de uma sessão.

A primeira corrida (r1, `pricing-bancas-marinha`) não conta (§0). Repete-se com o kernel
de `073739a` ou posterior, que traz também, na captura: `.srt`/`.txt`/`.md`/`.csv`
(`c7fabf6`), a formatação condicional agrupada por padrão (`bd164c0`, o extraction.json do
livro de pricing desce de 6,3 MB para 1,8 MB) e, no replay, a secção *What to read* que
nomeia os alvos das chamadas recusadas (`22132f6`).
