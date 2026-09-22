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

---

## 1. Antes de começar

```bash
mkdir -p docs/evolution/p8/runs/{dpt-galp-jp-pilot-4,pricing-bunkers-pilot-4}
```

Regra que não se contorna: **cada braço comparável usa um engagement novo** (§6). Não se
reaproveita um engagement já mexido para um segundo braço — o resultado deixa de ser
atribuível.

---

## 2. O ciclo, por engagement

Sequência obrigatória (§6), com reinício de sessão **a cada seta**:

```
Capture/Discovery → resolução → Frame → Options → Premortem/Simulation → Decide → Blueprint → Render
```

São **7 pontos de reinício**. Em cada um:

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
>   "open_questions": [{"id": "U-002", "state": "Unknown"}],
>   "decisions": [{"id": "D-001"}],
>   "coverage": {"status": "<fresh|stale|absent>"},
>   "blockers": [{"id": "U-002"}],
>   "next_step": "/comando args"
> }
> ```
>
> Não inventes ids. Se não encontrares algo, deixa a lista vazia — uma lista vazia é uma
> resposta; um id inventado não é.

Gravar como `docs/evolution/p8/runs/<slug>/cp<N>-<nome>.report.json`.

Registar também, num `.notes.md` ao lado: modelo e configuração se acessíveis, e **os
campos que não se conseguiram observar** (§6 exige-o por escrito).

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

---

## 3. Os dois reinícios extra (§6)

Além dos 7 pontos, a aceitação pede mais dois:

1. **Reinício depois de erro.** Provocar uma falha (fechar a meio de um comando), reabrir,
   pedir o mesmo JSON. Esperado: a sessão vê a operação pendente e **não avança**.
2. **Reinício depois de fonte actualizada.** Trocar o ficheiro de input por uma versão
   diferente, reabrir. Esperado: a sessão reporta a fonte como mudada, não como igual.

---

## 4. Fuga entre engagements

Trabalhar `dpt-galp-jp-pilot-4`, fechar, abrir `pricing-bunkers-pilot-4`, pedir o JSON.
Nenhum id do primeiro pode aparecer no segundo.

```bash
python3 docs/evolution/p8/compare.py leak \
  --truth-other docs/evolution/p8/runs/dpt-galp-jp-pilot-4/cp7-render.truth.json \
  --report      docs/evolution/p8/runs/pricing-bunkers-pilot-4/cp1-capture.report.json \
  --out         docs/evolution/p8/runs/pricing-bunkers-pilot-4/leak.verdict.json
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
  --oracle  docs/evolution/oracles/<slug>.oracle.json \
  --mapping docs/evolution/p8/runs/<slug>/mapping.json \
  --out     docs/evolution/p8/runs/<slug>/oracle.verdict.json
```

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

## 7. Bloqueio conhecido, por resolver

O piloto de pricing corre contra o ficheiro **errado**. O autoritativo é o `.xlsx`
(sha `cf40be3e…`, 19 folhas, com `Motor` e `Relatório Preços`); o que está em
`projects/pricing-bunkers-pilot-4/inputs/` é o `.xlsm` (sha `677e7963…`, 18 folhas, com
VBA). O oráculo `pricing-bunkers-pilot-4.oracle.json` foi extraído do `.xlsx`.

Enquanto o `.xlsx` não entrar, o braço de pricing de **E02 não fecha** — e o que se medir
contra o `.xlsm` mede outra coisa. O `.xlsm` continua a servir E05, que é sobre limites de
extração e não sobre correcção.

Substituir o input e recapturar (`/capture`) antes de correr E02 em pricing. A captura
guardada é anterior ao bloco `capability_boundary` e não declara as 176 chamadas
`_xll.Storm` que o motor de preço faz.
