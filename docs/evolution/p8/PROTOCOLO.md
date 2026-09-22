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

**`/capture` ainda não correu sobre o `.xlsx`.** Por decisão do operador, corre como **cp1
do protocolo**, dentro de uma sessão real — Capture/Discovery é o primeiro ponto de
reinício de E01, e pré-correr punha parte do ciclo medido fora de uma sessão.

Os artefactos em `_capture/` são do `.xlsm` e são anteriores ao bloco
`capability_boundary`: nunca declararam as 176 chamadas `_xll.Storm`. Serão substituídos
pelo `/capture` de cp1.
