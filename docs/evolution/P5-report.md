# P5 — Migração explícita de engagements existentes

Estado: **GO**

## Identidade e precondições

- **Data/ambiente:** 2026-09-22 · Linux · Python 3.11.15
- **GO anterior:** P4 **GO** — 52 ficheiros / 2128 testes.
- **Contrato:** `MIGRATION_AND_COVERAGE.md` §C1 (migração) e §C2 (reversão).
- **Casos:** M01–M06 — 6 dos 61.

## Nota pré-alteração

- **Problema:** os engagements existentes não têm grafo. Migrá-los sem protocolo perde
  história, reinterpreta terceiros como donos, ou reabre linhas resolvidas.
- **Hipótese verificável:** um ensaio pode produzir o mapa completo origem→destino **sem
  escrever um byte**, e a reversão pode provar-se por igualdade de hashes.
- **Risco maior:** preencher ambiguidade com plausibilidade. O contrato é explícito —
  «sem confirmação inventada».
- **Reversão:** dois ficheiros novos.

## Alterações realizadas

| Ficheiro | Linhas | Papel |
|---|---:|---|
| `library/kernel/tools/migrate.py` | 379 | dry-run, apply, restore |
| `.claude/tests/test_migration.py` | — | M01–M06 + engagement real, 28 testes |

### Cinco classes, e nenhuma é «mais ou menos»

| Classe | Quando |
|---|---|
| `projectable` | projecta sem ambiguidade |
| `already_represented` | já existe no grafo com o mesmo id |
| `ambiguous` | `quem responde` sem prefixo `role:`/`fonte:`; resolvida para sucessor inexistente |
| `invalid` | o parser marcou `malformed` |
| `unsupported` | fora do que este porte trata |

**Ambíguo não vira confirmado.** Uma linha ambígua **não é projectada** — há teste que o
afirma. Migração com excepções **não declara sucesso total**.

### Fixtures sintéticas, de propósito

Um conjunto que dependesse dos engagements em `projects/` (gitignored) falharia para sempre
num clone limpo — e o baseline do P0 já regista um teste assim (`test_state_scaffold`). As
fixtures cobrem as três formas que o plano pede: projecto novo, projecto com história
resolvida, projecto com ambiguidades. O engagement real é exercitado num teste que **salta**
se ausente.

## Verificação

| Runner | Collected | Passed | Failed | Skipped | Xfail | Errors |
|---|---:|---:|---:|---:|---:|---:|
| `python3 <ficheiro>` × 53 | **2156** | 2139 | **0** | 14 | 3 | **0** |

2128 → 2156 = +28, exactamente os testes novos. Zero regressões. Contagem por classe
conferida (5+5+3+5+4+5+1 = 28); nada depois do bloco `main`.

### Casos → evidência

| Caso | Afirma |
|---|---|
| M01 | o ensaio **não escreve**: árvore idêntica antes/depois, sem `_migration/`; mapa cobre todas as linhas; relatório devolvido, **fora** do snapshot |
| M02 | ids, estados e autoridade sobrevivem; cadeia `resolved` vira arestas `was`; linhas resolvidas **não reabrem**; decisão activa é a não substituída |
| M03 | segundo `apply` é no-op; nada muda; sem nós duplicados |
| M04 | dono sem prefixo → ambíguo; sucessor inexistente → ambíguo; excepções listadas; ambígua **não projectada**; sucesso **parcial** declarado |
| M05 | hashes originais reproduzidos; ficheiro alheio **preservado**; grafo criado pela migração removido; backup corrompido **recusa** o restore |
| M06 | restore cego **recusado** após trabalho novo; trabalho preservado; recusa nomeia o que mudou; plano velho rejeitado; pendência recuperável |

### Quatro defeitos, e de quem eram

1. **`active_decision` reescrevia o motor.** `classify_decisions` já lê `**Supersedes**` e
   retro-liga `superseded_by`. Passou a usar o que ele computa.
2. **Fixture testava um caso inexistente.** `parse_su` não trata `resolved ->` com alvo vazio
   como resolvido — `RESOLVED_RE` exige `(.+)$`. O caso ambíguo real é resolver para um
   sucessor que **não existe**.
3. **No-op comparava a coisa errada.** `plan_hash` deriva dos digests **pré**-migração, que
   mudam assim que se migra. Passou a comparar o estado actual com o `after` do manifesto.
4. **Asserções fora do bloco `tempfile`** — outra vez, o mesmo bug do W05 em P2.

Os dois primeiros são a mesma lição, a terceira vez nesta linha de trabalho: **antes de
escrever uma segunda leitura, verificar o que o `dashboard.py` já computa.**

## Resultado e limitações

### GO/NO-GO por critério

| Critério (P5) | Veredicto |
|---|---|
| Dry-run primeiro, sem escrita | **Cumprido** — M01, por hash da árvore |
| Bytes originais em snapshot recuperável | **Cumprido** — backup verificado por hash antes de publicar |
| IDs e locators preservados | **Cumprido** — M02 |
| Relatório discrimina 5 classes | **Cumprido** — M04 |
| Não reinterpretar terceiros como owner | **Cumprido** — ambíguo, não projectado |
| Não reabrir linhas resolvidas | **Cumprido** — M02 |
| Migração repetível, sem duplicação | **Cumprido** — M03 |
| Reversão testada | **Cumprido** — M05, M06 |
| Zero perda material não declarada | **Cumprido** — excepções explícitas; sucesso parcial |

**GO.**

### Limitações, declaradas

1. **Grafo sem conhecimento não é migração bem-sucedida de projecto avançado.** O plano
   di-lo e o motor respeita-o: excepções bloqueiam a declaração de sucesso total. Mas o que
   se projecta são **linhas da SU**, não findings, capture nem outputs — esses ficam para P6.
2. **`decisions.md` é lido, não migrado.** A decisão activa é identificada e reportada; não
   há nós de decisão no grafo. P6.
3. **O engagement real só é exercitado em dry-run.** Um `apply` real sobre dados de cliente
   exigiria decisão do operador, e o teste salta se `projects/` estiver ausente.
4. **Downgrade não é prometido.** C2 exige documentar limites; este porte não afirma
   reversão para uma versão anterior do runtime depois de alterações novas.

### Próxima acção concreta

**P6** — coerência, fontes e Coverage: 13 casos (L06–L10, C01–C08), o maior bloco depois de
P2. É onde `coverage.py` entra de facto e onde as limitações 1 e 2 se fecham.
