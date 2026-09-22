# P2 — Fundação de persistência e recuperação

Estado: **GO** — técnico. Não se declara continuidade de negócio (o plano proíbe-o nesta fase).

## Identidade e precondições

- **Data/ambiente:** 2026-09-22 · Linux 6.18.44-fc-v37 · Python 3.11.15
- **GO anterior:** P0 **GO**. P1 `IN_PROGRESS` — os cinco entregáveis estão produzidos; falta
  validação de 13 itens críticos dos oráculos, que é evidência de **P8** e não entrada de P2.
  O operador autorizou explicitamente correr P2 em paralelo.
- **Contratos aplicáveis:** `WRITES_AND_RECOVERY.md` (B1–B6), `AUTHORITY_AND_KNOWLEDGE.md`.
- **Casos:** K01–K08, W01–W08 — 16 dos 61.

## Nota pré-alteração

- **Problema:** o alvo tem garantias **por artefacto** (escrita atómica, uma porta de escrita
  no `coverage.py`, lock do dashboard) e nenhuma **entre** artefactos. Uma operação que toca
  SU + `_state.json` + `answers.md` é atómica ficheiro a ficheiro e não como conjunto.
  Medido em `authority-map.md`, não suposto.
- **Hipótese verificável:** é possível dar atomicidade observável pelos leitores suportados
  sem serviço, sem base de dados e sem framework transaccional — só com stdlib.
- **Autoridades afectadas:** nenhuma, ainda. P2 constrói a fundação; **nenhum escritor de
  negócio foi movido para cima dela**. O plano exige esta ordem.
- **Risco:** acrescentar dois motores ao kernel e partir testes que os enumeram.
- **Reversão:** dois ficheiros novos em `library/kernel/tools/` e dois de teste. Nada
  existente foi alterado; remover os quatro reverte P2 por inteiro.

## Alterações realizadas

| Ficheiro | Linhas | Papel |
|---|---:|---|
| `library/kernel/tools/graph.py` | 360 | store aditivo, integridade, autoridade, isolamento |
| `library/kernel/tools/operation.py` | 445 | coordenador, exclusão, recuperação |
| `.claude/tests/test_graph_store.py` | — | K01–K08 + a costura grafo↔coordenador |
| `.claude/tests/test_operation_recovery.py` | — | W01–W08 |

Zero ficheiros existentes alterados. Zero testes existentes alterados, saltados ou desactivados.

### Decisões de formato (o que P1 deixou para fixar aqui)

**`<engagement>/_graph/graph.jsonl` + `meta.json`.** JSONL porque o grafo é aditivo e uma
linha por registo mantém a serialização estável e o diff legível. `meta.json` separado porque
a revisão tem de ser lida **sem** ler o grafo inteiro — os gates fazem-no a cada operação.

**Ordem canónica:** nós por `(type, id)`, arestas por `(src, rel, dst)`, chaves na ordem do
contrato e as desconhecidas no fim, nunca apagadas. Entrada reordenada dá bytes iguais.

**`<engagement>/_ops/`** para pendência, staging e recibos — tem de sobreviver a tudo.
**Lock em `$TMP`**, fora do engagement, pela razão que o `dashboard.py` já documenta: a pasta
do engagement é material de cliente e um ficheiro de runtime não se versiona com ela.

### Reutilização do que já existia

O contrato manda reutilizar atomicidade e locks existentes «quando suficiente». Foi examinado:

- **`atomic_write` do `dashboard.py`** — o padrão foi reutilizado (tmp com pid → `os.replace`),
  com `fsync` acrescentado antes do rename.
- **Lock do `dashboard.py`** — **não** reutilizável: é lock de *servidor* (porta, pid, sonda
  HTTP), específico do `--serve`. O que se reutilizou foi a **disciplina de identidade**
  (pid + instante de arranque, nunca existência de ficheiro, nunca remoção por timeout cego),
  que é exactamente o que B2.2 exige. O código não serve; o critério serve.

## Verificação

| Runner | Collected | Passed | Failed | Skipped | Xfail | Errors |
|---|---:|---:|---:|---:|---:|---:|
| `python3 <ficheiro>` × 50 (per-file unittest) | **2064** | 2047 | **0** | 14 | 3 | **0** |

Antes de P2: 48 ficheiros / 2009 testes. Depois: 50 / 2064. A diferença são exactamente os
55 testes novos (+3 da costura = 58 no total dos dois ficheiros). Zero regressões.

Verificado antes de committar que nenhum teste existente enumera os motores por glob — são
agora sete onde eram cinco. Referenciam-nos por nome. `test_motor_identity`,
`test_hook_invocation`, `test_orchestrator_wiring` e `test_pp_pack_integrity` passam.

### Casos → evidência

| Caso | Onde | Afirma |
|---|---|---|
| K01 | `K01_StoreVazio` | store vazio é `ok` e **distinto** de ausente |
| K02 | `K02_Persistencia` | reler em **processo novo** preserva ids, props, relações e proveniência |
| K03 | `K03_Determinismo` | reordenar entrada não muda bytes nem revisão |
| K04 | `K04_Integridade` | id duplicado, relação sem `rel`, ponta inexistente → erro; **nada escrito** |
| K05 | `K05_Autoridade` | drift detectado; o grafo **não prevalece** nem se auto-corrige |
| K06 | `K06_Schema` | schema não suportado é explicado; campo desconhecido **sobrevive** à regravação |
| K07 | `K07_AusenteVersusIlegivel` | meta removido, grafo corrompido, revisão que não bate, permissão negada — **nenhum** vira ausência |
| K08 | `K08_IsolamentoDeCaminhos` | escape por `..`, por caminho absoluto e por **symlink** recusado |
| W01 | `W01_CrashAntesDaIntencao` | base recusada não toca em artefactos nem deixa pendência |
| W02 | `W02_CrashEntreEscritas` | processo morto a meio da publicação → pendência visível, **sem recibo**, recuperação completa |
| W03 | `W03_CrashAposCommit` | repetir o `operation_id` devolve o mesmo recibo e **não reescreve** |
| W04 | `W04_Concorrencia` | segundo escritor sobre base velha é recusado; a escrita do primeiro sobrevive |
| W05 | `W05_LeitorConcorrente` | leitor durante pendência recebe recusa explícita **com a acção de recuperação** |
| W06 | `W06_Locks` | lock vivo não é roubado, abandonado é tomado **com registo**, ilegível não é removido |
| W07 | `W07_FalhaDeIO` | staging danificado recusa sem inventar; a pendência **sobrevive** à recuperação falhada |
| W08 | `W08_ConflitoExterno` | bytes de terceiro **não** sobrescritos; conflito com os três hashes |

As interrupções de W02 são reais: `os._exit(9)` a meio da publicação, em subprocesso, não uma
flag.

### Três falsos verdes apanhados, e como

Registados porque o modo de falha importa mais do que a correcção:

1. **`runpy.run_path` devolve uma CÓPIA do namespace.** Substituir `O["_publish"]` nunca
   chegava ao `__globals__` da função a correr: a sabotagem não disparava, o processo saía
   com 0 e **o teste de crash passava sem testar nada**. Corrigido com patch em
   `run.__globals__`.
2. **Asserção fora do bloco `with tempfile.TemporaryDirectory()`.** O «gate está aberto» era
   só o directório já ter sido apagado.
3. **Classe de teste acrescentada depois do `if __name__ == "__main__"`.** Três testes
   existiam no ficheiro e **não corriam**. Apanhado pela contagem: 30 quando deviam ser 33.

Nenhum foi detectado por o teste falhar. Todos por o número não bater. A contagem é evidência.

## Resultado e limitações

### GO/NO-GO por critério

| Critério de saída (P2) | Veredicto | Evidência |
|---|---|---|
| Nenhuma escrita rejeitada altera a verdade | **Cumprido** | W01: base recusada deixa bytes e gate intactos |
| Interrupção é recuperável | **Cumprido** | W02: morte real a meio, recuperação completa o conjunto |
| Duas sessões não perdem actualizações | **Cumprido** | W04: o segundo é recusado, o primeiro sobrevive, e passa depois de reler a base |
| Leitores não declaram sucesso sobre estado misto | **Cumprido** | W02/W05: pendência visível bloqueia gate; sem recibo antes da verificação |
| Casos K01–K08 e W01–W08 | **Cumprido** | 16/16 com teste que afirma o `expected` do caso |
| Regressão completa | **Cumprido** | 50/50 ficheiros, 2064 testes, 0 falhas |
| Sem serviço, BD, fila ou dependência nova | **Cumprido** | stdlib apenas; `pip freeze` inalterado |

**GO técnico.**

### Limitações, declaradas

1. **Nada está ligado.** `graph.py` e `operation.py` existem e são testados; **nenhum escritor
   de negócio os usa**. É a ordem que o plano impõe — ligar é P4. Até lá, o grafo não contém
   conhecimento real e K02 é testado com nós sintéticos.
2. **Leitores externos ficam fora da garantia**, como B3 permite. O que se faz é **detectar**
   que mexeram (W08), não impedi-los.
3. **Escritas por subprocesso continuam invisíveis aos hooks.** P2 não resolve isto —
   resolve-o quem passar a usar o coordenador. O ponto cego está em `on-su-change.py:38-40`,
   no próprio código, e continua lá.
4. **Durabilidade contra falha de energia não é afirmada.** Há `fsync` antes do rename; o
   comportamento do sistema de ficheiros por baixo **não foi testado** e B2.5 só exige a
   afirmação quando testada. Não é afirmada.
5. **Um só sistema operativo.** Medido em Linux. `_proc_started()` lê `/proc` e devolve `""`
   onde não existe; nesse caso a posse fica *indeterminada* e o lock **não** é tomado — falha
   segura, mas não testada noutro SO.

### Métricas

| | antes de P2 | depois |
|---|---:|---:|
| Motores em `library/kernel/tools/` | 5 · 15 954 linhas | 7 · 16 759 |
| Ficheiros de teste | 48 | 50 |
| Testes | 2009 | 2064 |
| Stores persistentes | 0 | 1 (`_graph/`, ainda vazio em uso real) |
| Dependências de runtime | stdlib | stdlib |

### Próxima acção concreta

**P3 — bootstrap técnico universal** (casos B01–B07). Integrar a ordem que B5 exige:
identidade do engagement → detecção de pendência → recuperação autorizada → snapshot →
autoridades → contexto → operação. O `status()` e o `gate_open()` deste P2 são as peças que
P3 põe a correr **antes** dos efeitos, em todos os pontos de entrada — incluindo os que não
passam por `/start` e os que correm por subprocesso.
