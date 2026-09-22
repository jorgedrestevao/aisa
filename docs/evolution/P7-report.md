# P7 — Projecções e UX de todo o workflow

Estado: **GO parcial** — o mecanismo está provado; **a avaliação com operador humano não foi
feita**, e o caso U01 exige-a. Ver *Limitações*.

## Identidade e precondições

- **Data/ambiente:** 2026-09-22 · Linux · Python 3.11.15
- **GO anterior:** P6 **GO** — 55 ficheiros / 2209 testes.
- **Casos:** U01–U05 — 5 dos 61.

## Nota pré-alteração

- **Problema:** `gate_state` avalia os critérios da fase a partir do disco, mas **não sabe de
  pendência de operação nem de drift do espelho**. O plano exige que os gates avaliem o
  snapshot **completo**, não um excerto.
- **Risco:** construir uma segunda projecção. O `dashboard.py` já projecta quase tudo.
- **Reversão:** dois ficheiros novos.

## Alterações realizadas

| Ficheiro | Linhas | Papel |
|---|---:|---|
| `library/kernel/tools/projection.py` | 191 | compõe bootstrap + `build_model` |
| `.claude/tests/test_projection_ux.py` | — | U01–U05, 23 testes |

**Nenhum modelo novo.** `dashboard.build_model` já dá fase, saúde epistémica, agenda,
críticos, tripwires, marco e o gate com o modo de cada critério. Este módulo compõe.

### O que acrescenta, e só isto

1. **O gate consulta o snapshot completo** — critérios de fase **+** operação pendente **+**
   espelho do grafo. Um gate que ignorasse uma recuperação pendente decidiria sobre estado
   misto.
2. **Bloqueio com quatro campos** — o que falta · porque importa · que evidência fecha ·
   que acção tomar. Um bloqueio que só diz «falta X» não é accionável.
3. **Incerteza não bloqueante continua visível** — avançar não é varrer para debaixo do tapete.
4. **Projecção desactualizada é reportada como tal**, e `stale` **não é verdade de gate**.

## Verificação

| Runner | Collected | Passed | Failed | Skipped | Xfail | Errors |
|---|---:|---:|---:|---:|---:|---:|
| `python3 <ficheiro>` × 56 | **2232** | 2215 | **0** | 14 | 3 | **0** |

2209 → 2232 = +23, exactamente os testes novos. Contagem por classe conferida
(5+5+4+4+5 = 23); nada depois do bloco `main`.

### Casos → evidência

| Caso | Afirma |
|---|---|
| U01 | a explicação nomeia fase, bloqueio e próximo passo; **zero vocabulário interno** (`schema_version`, `graph.jsonl`, `sha256`, `fingerprint`, `node`, `edge`); **nenhuma linha começa por um id** (P-13); o bloqueio é o crítico, não o de baixo impacto |
| U02 | gate fechado com crítico aberto; **todos** os bloqueios têm os quatro campos; a acção é um comando executável; **consultar não muda a fase**; pendência fecha o gate antes de ler conteúdo |
| U03 | o Unknown de baixo impacto **não** bloqueia mas **continua visível**, e a visibilidade é declarada, não implícita |
| U04 | os 14 pontos de entrada do mapa P1 existem; **zero percentagens inventadas**; **`/resolve` e `/advance` não foram criados** por existirem no doador; ler a projecção não escreve |
| U05 | projecção ausente é reportada, não adivinhada; **mutação por subprocesso real** marca stale e nomeia a autoridade mais recente; `stale` diz explicitamente que não é verdade de gate; o gate declara as três fontes que consultou |

### O quinto erro de chave, e o pior até agora

`build_model` **não tem** `rows`, nem `gate`, nem `state` ao nível de topo. Tem `su.rows`,
`status.gates`, `status.milestone`, `engagement.phase`.

`model.get("rows") or []` devolve lista vazia **em silêncio**. A projecção estava a ler o
vazio sem se queixar. Os testes apanharam **porque afirmam conteúdo, não ausência de
excepção** — um teste que só verificasse «não rebentou» teria passado.

É a quinta vez nesta linha de trabalho. O módulo leva agora um comentário a dizer que as
chaves foram verificadas contra a saída real.

## Resultado e limitações

### GO/NO-GO por critério

| Critério (P7) | Veredicto |
|---|---|
| Estado operacional e próxima acção de autoridades verificadas | **Cumprido** |
| Gates avaliam snapshot completo, não excerto | **Cumprido** — três fontes declaradas |
| Bloqueio explica o que falta, porquê, evidência e acção | **Cumprido** — quatro campos, testados |
| Unknown não bloqueante continua visível | **Cumprido** — U03 |
| Sem percentagens arbitrárias; sem duplicar `/resolve`/`/advance` | **Cumprido** — U04 |
| Dashboard é projecção; stale indicado; stale ≠ verdade de gate | **Cumprido** — U05, com subprocesso real |
| Cobertura dos pontos de entrada do mapa P1 | **Cumprido** — os 14 existem |
| Regressão completa | **Cumprido** — 56/56, 2232 testes |
| **Operador que não precise de ids: próximo passo em ~2 min, com protocolo e observação registados** | **NÃO CUMPRIDO** |

**GO parcial.** Oito critérios cumpridos, um por cumprir — e é um que exige uma pessoa.

### A limitação central, declarada

O caso U01 pede **«tempo observado registado»**, e a `ACCEPTANCE.md` §7 acrescenta:
«Registar tarefa, tempo observado, dúvidas e resposta; cerca de dois minutos é referência de
usabilidade». **Isso não foi feito.** Não há operador, não há protocolo corrido, não há
tempo medido.

O que está provado é o **mecanismo**: a explicação existe, é legível sem schema, e não deixa
passar vocabulário interno nem ids como sujeito.

Há um teste que guarda contra o próprio relatório —
`test_the_human_timing_is_not_claimed` — que afirma que a projecção **não produz**
`observed_seconds` nem `comprehension_time`. Se alguém tentar preencher isso sem um humano,
o teste falha.

### Outras limitações

1. **Os pontos de entrada existem; não foi verificado que cada um CHAMA o bootstrap.** U04
   prova que os 14 comandos/skills existem. Que cada um passa pela barreira antes dos
   efeitos é trabalho que não foi feito — o P3 provou que o bootstrap funciona quando
   chamado, não que toda a experiência o chama.
2. **A staleness é por `mtime`.** Um sistema de ficheiros com granularidade grosseira, ou
   uma escrita e uma leitura no mesmo instante, podem não a detectar. Suficiente para o
   caso; não é garantia forte.
3. **`drift` é avaliado com autoridade vazia.** O espelho é comparado contra `{}`, o que
   detecta `MIRROR_SOURCE_MISSING` mas não divergência real de valor — a autoridade viva
   viria da SU, e essa ligação é trabalho de integração que fica por fazer.

### Próxima acção concreta

**P8** — ciclo completo entre sessões e pilotos reais. Arranca com **dois bloqueios de
entrada já conhecidos**, nenhum deles resolúvel por engenharia:

- `ACCEPTANCE.md` §6 exige **sessões Claude Code independentes**; processos Python a passar
  não substituem E01/E02.
- O ficheiro autoritativo do piloto de pricing (o `.xlsx`, sha `cf40be3e…`) **não existe
  neste ambiente**.
