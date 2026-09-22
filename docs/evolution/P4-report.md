# P4 — Primeira operação completa de negócio

Estado: **GO** — prova esta sequência delimitada, não todo o workflow (o plano di-lo assim).

## Identidade e precondições

- **Data/ambiente:** 2026-09-22 · Linux · Python 3.11.15
- **GO anterior:** P3 **GO** técnico — 51 ficheiros / 2101 testes.
- **Contrato:** `WRITES_AND_RECOVERY.md` (B1–B5), `library/kernel/states.md` → *Transitions*.
- **Casos:** L01–L05 — 5 dos 61.

## Nota pré-alteração

- **Problema:** P2 e P3 deram atomicidade, recuperação e bootstrap, mas **nada de negócio
  passava por eles**. As limitações 1 e 2 do P3 — não lê a SU, nenhum ponto de entrada o
  chama — deixavam de ser aceitáveis aqui.
- **Hipótese verificável:** resolver uma linha da SU pode publicar SU + `answers.md` + grafo
  como **uma** operação, e a resolução sobrevive a uma sessão nova sem histórico.
- **Autoridades afectadas:** `shared-understanding.md`, `answers.md`, o grafo. Primeira vez
  que o coordenador toca artefactos de negócio.
- **Risco:** um segundo parser da SU seria uma segunda verdade.
- **Reversão:** dois ficheiros novos.

## Alterações realizadas

| Ficheiro | Linhas | Papel |
|---|---:|---|
| `library/kernel/tools/resolve.py` | 319 | o motor por trás de `/answer` |
| `.claude/tests/test_resolve_operation.py` | — | L01–L05 + sequência entre sessões, 27 testes |

Zero ficheiros existentes alterados.

### Reutilização, e o que ela ensinou

`resolve.py` lê a SU por `dashboard.parse_su` e a autoridade por `dashboard.split_owner`.
Não há segundo parser.

Assumi os nomes das colunas e **errei**. O schema que `parse_su` devolve é muito mais rico
do que o markdown mostra:

| Assumi | Real |
|---|---|
| `pergunta` | `claim` |
| `quem responde` | `support` |
| regex sobre prosa | **`swing_class: dimensionante`** — já computado |
| — | `resolved`, `resolved_to`, `was`, `retired`, `expired` — já computados |

A minha regex para decidir se a pergunta era estrutural foi substituída pela classificação
do próprio motor. **Duas classificações divergiriam ao primeiro caso estranho.** E o
`RESOLVED_RE` já aceita `→` e `->`, portanto a convenção de marcação não precisou de
invenção nenhuma — precisou de leitura.

## Verificação

| Runner | Collected | Passed | Failed | Skipped | Xfail | Errors |
|---|---:|---:|---:|---:|---:|---:|
| `python3 <ficheiro>` × 52 | **2128** | 2111 | **0** | 14 | 3 | **0** |

2101 → 2128 = +27, exactamente os testes novos. Contagem por classe conferida; nada depois
do bloco `main`.

### Casos → evidência

| Caso | Afirma |
|---|---|
| L01 | inferência resolve para `Assumed`, nunca `Confirmed`; sessão nova mantém resolvido, sucessor activo, linha original **não apagada**; proveniência e aresta `was` intactas |
| L02 | locator + autoridade correspondida → `Confirmed`; resposta **literal** preservada; `was` e âncora na célula de evidência; original marcado; **tudo numa só operação** |
| L03 | terceiro **com** locator continua `Assumed`, com razão escrita; autoridade lida da própria linha; autoridade certa **sem** locator também é `Assumed` |
| L04 | repetir é a mesma operação; sem segunda linha, sem resposta duplicada, sem nós multiplicados |
| L05 | conectividade regista facto e **mantém a escolha estrutural aberta**, visível no grafo; resposta que estabelece adequação pode fechar; pergunta não estrutural não abre escolha |

### As três regras deixam de ser prosa

| Regra | Onde era texto | Agora |
|---|---|---|
| Autoridade não se presume | `states.md` | recusada por código, razão escrita |
| Facto não fecha adequação | `aisa-answer/SKILL.md` §46-48 | `structural_choice_open` calculado |
| Repetir não duplica | — | recibo antes de planear |

### Bug de desenho que o L04 expôs

A segunda chamada de `apply()` replaneava sobre uma SU **já resolvida**, produzindo payload
diferente sob o mesmo `operation_id`. O coordenador recusou — correctamente. O nível que
sabe que a operação já correu é este, porque o id deriva da linha e da resposta, **não do
estado do mundo**. `apply()` passa a ler o recibo antes de planear.

## Resultado e limitações

### GO/NO-GO por critério

| Critério (P4) | Veredicto |
|---|---|
| Capture/SU/`/answer` ligados ao coordenador e ao grafo | **Cumprido** |
| Confirmar só ao nível e autoridade que `states.md` permite | **Cumprido** — L02/L03 |
| Não fechar escolha arquitectural por confirmação de conectividade | **Cumprido** — L05 |
| Sequência sobrevive a sessão nova sem histórico | **Cumprido** — subprocesso real |
| Gate não passa com divergência ou recuperação pendente | **Cumprido** — `NOT_READY` |
| Fontes repetidas não multiplicam nós | **Cumprido** — L04 |
| Output «o que mudou / estado / próximo passo» | **Cumprido** — `summary` |
| L01–L05 + regressão completa | **Cumprido** — 5/5, 52/52 ficheiros |

**GO.**

### Limitações, declaradas

1. **Capture não está ligado.** `resolve.py` cobre `/answer` e o registo na SU. O pipeline de
   captura (`xlsx_extract`, `text_extract`) continua a escrever `_capture/` fora do
   coordenador. L04 testa idempotência **da resolução**, não da captura.
2. **Coverage não é consultado.** O plano pede «verificar Coverage pelo motor»; `resolve.py`
   não invoca `coverage.py`. É integração de P6.
3. **As 24 skills continuam a não chamar isto.** O motor existe e é testado; `aisa-answer`
   ainda não o usa. Ligar os pontos de entrada é P7.
4. **Um só sentido de transição.** Só `Unknown → Confirmed/Assumed`. `Conflicted`, `Risky`,
   revalidação e retirada são P6 (casos L06–L10).

### Próxima acção concreta

**P6** — coerência, fontes e Coverage (L06–L10 + C01–C08, 13 casos). É onde as limitações 2
e 4 se resolvem, e onde `coverage.py` entra de facto.
