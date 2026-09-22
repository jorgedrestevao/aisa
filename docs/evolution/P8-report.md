# P8 — ciclo completo entre sessões e pilotos reais

**Veredicto: GO parcial.** Três dos cinco casos fechados com evidência. Dois por executar,
por razões que não são de engenharia e que estão nomeadas abaixo.

---

## 1. Casos

| Caso | Estado | Evidência |
|---|---|---|
| **E01** Sessões reais | **NÃO EXECUTADO** | Exige sessões Claude Code independentes. Ver §4.1. |
| **E02** Dois pilotos vs oráculos | **NÃO EXECUTADO** | Depende das sessões de E01. O ficheiro autoritativo de pricing entrou e verifica (§4.2); falta correr. |
| **E03** Referência independente | **CUMPRIDO** | Oráculos extraídos da fonte em P1 e validados pelo dono **antes** de existir candidato (`docs/evolution/oracles/`). A referência precede o candidato, como `ACCEPTANCE.md` §5 exige. |
| **E04** Inspeção completa | **CUMPRIDO** | `graph.py` ganhou `traverse`/`components`/`provenance`/`export`/`inspect` + CLI `inspect\|export`. 22 testes em `.claude/tests/test_graph_inspection.py`. |
| **E05** Limites de extração | **CUMPRIDO** | 14 testes em `.claude/tests/test_extraction_limits.py`, sobre fonte construída **e** sobre o livro real do piloto. |

---

## 2. O que E04 prova

`ACCEPTANCE.md` §7 diz três coisas sobre o grafo, e cada uma tem um teste:

1. **«relações completas recuperáveis»** — `traverse` navega nos dois sentidos (a relação
   `was` aponta do novo para o antigo; navegar só a favor perderia metade da história) e
   devolve exactamente o alcançável.
2. **«componentes desconectados reais»** — duas ilhas ficam duas. Um nó sem arestas é um
   componente, não uma falha. Nenhuma função desta secção cria uma aresta ou uma raiz para
   o grafo ficar bonito.
3. **«contexto pode ser parcial; export/traversal permite acesso ao restante»** —
   `traverse(depth=N)` declara `truncated` e devolve a `frontier` exacta; `export` dá o
   resto, byte a byte igual ao publicado.

Mais duas afirmações que a aceitação não pede e que valem na mesma:

- Uma ponta pendente (`EDGE_END_UNKNOWN`) é **reportada**, nunca materializada como nó.
- Um store ilegível **não se resume**: declara o estado e cala-se.

**Sabotagem.** Quatro mutantes correram contra a suite de E04. Todos apanhados:

| Mutante | Resultado |
|---|---|
| componentes coalescem tudo num só | apanhado (2 testes vermelhos) |
| ponta pendente vira nó alcançado | apanhado (1) |
| contexto parcial não declara fronteira | apanhado (1) |
| proveniência ausente é preenchida | apanhado (1) |

Limite honesto do harness: patcha a cópia do namespace que `runpy` devolve, logo mede as
asserções directas, não o interior de `inspect`. O interior é coberto pelos quatro testes
de subprocesso da classe `E04g`, que correm o ficheiro real.

---

## 3. O que E05 prova

A fonte é construída com conteúdo não suportado **material**: macros (`vbaProject.bin`),
funções de add-in (`_xll.Storm.Quote`), Power Query e um livro externo. O `PRECO` depende
da função de add-in, logo **não é calculável a partir do ficheiro**.

O que se afirma é o contrário do habitual — não que o motor leia tudo, mas que:

- declare cada mecanismo presente, com **onde** está (`xl/vbaProject.bin`) e que **não o leu**
  (`modules not decompiled`);
- **conte** as chamadas que viu em vez de estimar;
- não eco do conteúdo do binário como se fosse regra;
- não escreva nenhum número onde não há valor;
- mantenha os mecanismos ausentes ausentes — declarar presença seria inferir;
- continue a extrair o que é legível: a limitação não é desculpa.

E que a consequência chegue a quem lê: §4bis declara a fronteira **antes** da cadeia, com
`TO-READ manual` para a macro e `feed externo` para o add-in.

### 3.1 Achado sobre o piloto real

O livro real de pricing declara hoje:

| mecanismo | presente | detalhe |
|---|---|---|
| `vba` | sim | `vbaProject.bin present (modules not decompiled)` |
| `addin_functions` | sim | **`_xll.Storm ×176`** |
| `power_query` | sim | `DataMashup in customXml/itemProps3.xml` |
| `external_links` | sim | livro `CEntriC - Marine Bunkers PT-Runtime.xlsx` numa pasta `Temp` local |

**176 chamadas a uma função de add-in.** O motor de preço depende de código que não está no
ficheiro. Isto é fronteira declarada, não omissão — mas muda o que se pode afirmar sobre o
cálculo a partir do livro.

**A captura guardada do piloto é anterior a este bloco.** O artefacto em
`_capture/*.extraction.json` não tem `capability_boundary`; só tem `workbook.flags.vba_present`.
As 176 chamadas nunca foram declaradas no material que alimentou o trabalho de oráculo.
Recapturar antes de E02.

---

## 4. Porque E01 e E02 não fecham

Dois bloqueios. Nenhum se resolve escrevendo código.

### 4.1 Sessões Claude Code independentes (E01, e E02 por dependência)

`ACCEPTANCE.md` §2, última linha: *«Continuidade do agente provada em sessões Claude Code
independentes; subprocessos comprovam storage mas não a recuperação de raciocínio do
agente.»* E §6: *«Se não houver execução Claude Code disponível, documentar impedimento e
não marcar E01/E02 como concluídos apenas porque processos Python/Node passaram.»*

P2, P4, P6 e P7 correram subprocessos reais e provam persistência. Isso **não** é o que E01
pede. Uma sessão de agente fechada e reaberta sem histórico não se fabrica de dentro desta
sessão.

**Alternativa avaliada e descartada:** criar sessões remotas. Seriam genuinamente
independentes, mas clonam o repositório do GitHub, e `projects/` está fora do git por
decisão do dono — os dados dos pilotos não chegariam lá. Só funcionaria commitando dados de
cliente.

### 4.2 O ficheiro autoritativo de pricing — **resolvido**

Era o segundo bloqueio. Deixou de ser a 2026-09-22: o dono enviou o `.xlsx` e ele verifica.

| campo | oráculo (`authoritative_source`) | ficheiro recebido |
|---|---|---|
| sha256 | `cf40be3ed6…1692b52` | `cf40be3ed6…1692b52` ✓ |
| folhas | 19 | 19 ✓ |
| `has_vba` | `false` | sem `vbaProject.bin` ✓ |
| folhas-chave | `Motor`, `Relatório Preços` | presentes ✓ |

Instalado em `projects/pricing-bunkers-pilot-4/inputs/PREÇO BANCAS_03_08_26.xlsx`. O
`.xlsm` substituído foi para `inputs/_superseded/` — não apagado, porque é a única fonte
real com macros e é sobre ela que E05 afirma que o motor as declara sem as inventar; e fora
de `inputs/` para que `/capture` não leia as duas versões.

**Facto que sobreviveu à troca:** ambos os livros fazem as **mesmas 176 chamadas
`_xll.Storm`**. A dependência de add-in não é um artefacto da versão desactualizada — é
propriedade do motor de preço.

**O que isto ainda não destrava sozinho.** `/capture` não correu sobre o `.xlsx`. Por
decisão do operador corre como **cp1 do protocolo**, dentro de uma sessão real: Capture é o
primeiro ponto de reinício de E01, e pré-correr punha parte do ciclo medido fora de uma
sessão. Portanto E02 continua **NÃO EXECUTADO** — mas agora por falta de execução, não por
falta de ficheiro.

### 4.3 A troca destapou um defeito na referência — corrigido antes de custar 18 sessões

O `.xlsx` não é outro livro: é o mesmo com `Outputs` → `Relatório Preços`,
`Outputs BIOS` → `Relatório Preços Bios`, e uma folha nova, `Motor`.

O rename partiu um item **crítico** do oráculo. `P-05` ancorava em `Outputs!$C$6`/`$C$7`,
coordenadas que não resolvem no ficheiro autoritativo. Se o protocolo tivesse corrido
assim, a sessão não encontraria o item, `critical_recall` caía abaixo de `1.0` e o
resultado era **NO-GO por defeito da referência, não do candidato** — descoberto ao fim de
~18 reinícios.

Os dez itens críticos foram verificados um a um contra o ficheiro autoritativo antes de
qualquer sessão correr. Só `P-05` estava partido; está **re-ancorado**, medido da fonte e
registado em `remeasurements` no oráculo, com a substância intacta (a proposição não
mudou — só as coordenadas). `P-02`, `P-03` e `P-06` verificam: os 127 named ranges de
negócio são idênticos nas duas versões, `UlyssesQuotes` é idêntica, e a proposição de `P-06`
já cobria os dois ficheiros. Detalhe em `docs/evolution/p8/MOTOR-inventario.md`.

Nota de método: a nota de revisão de `P-05` **já registava** a correcção, vinda da
especificação. O que estava por corrigir era o campo `source_locator`. A medição directa
confirmou-a de forma independente, em vez de a repetir de ouvido.

### 4.4 A folha `Motor` verifica o P-10 contra o ficheiro

`Motor` é o motor de preço explícito e legível, e não existe no `.xlsm`. Cinco regras do
`P-10` — que estava `CLOSED_BY_OPERATOR_SPEC`, fechado pela especificação e não pelo
ficheiro — passam a ser verificáveis na fonte:

| regra | célula | fórmula |
|---|---|---|
| `encargo = prémio + SLI` | `Motor!C27` | `=+C26+C25` |
| `cedência = média(Platts) + encargo` | `Motor!C41` | `=+D24+D27` |
| `IFO180 = 0,9×VLSFO + 0,1×DMA` | `Motor!G41` | `=+D41*0.9+E41*0.1` |
| `margem USD = margem EUR × FX` | `Motor!C43` | `=C42*$D$37` |
| `PREÇO USD = cedência USD + margem USD` | `Motor!C45` | `=+C41+C43` |

E confirma a resposta do operador sobre o SLI: `Motor!C26` multiplica por `$H$24` (média
FX) nas colunas CIF MED, e **não** multiplica nas colunas `0.5% FOB Rdam barge` e
`Diesel 10ppm NWE` — exactamente como o `P-10` já registava.

O que o `Motor` **não** contém: a regra de porto (`mínimo + logística − 10`, MGO `−5 −10`).
As constantes `10` e `5` estão lá (`C9`, `C10`); a aplicação delas vive noutro lado, por
localizar. Fica por afirmar.

**Não promovi `P-10`** de `CLOSED_BY_OPERATOR_SPEC` a re-medido: mexer na validação de um
item que não está partido é decisão do operador, não minha.

---

## 5. O que foi entregue para que E01/E02 possam correr

Decidido com o dono: **o operador executa, o código valida.**

| Entregável | O que é |
|---|---|
| `docs/evolution/p8/PROTOCOLO.md` | Os 7 pontos de reinício, o prompt literal a colar, os dois reinícios extra (erro / fonte actualizada), a verificação de fuga entre engagements, e o procedimento do oráculo |
| `docs/evolution/p8/compare.py` | O comparador determinístico: `truth`, `check`, `leak`, `oracle`, `summary` |
| `.claude/tests/test_p8_comparator.py` | 30 testes sobre o comparador — ele próprio não é de confiar por decreto |

O comparador compara **proposições, estados e locators por id**, nunca igualdade de texto
(§6). Emite números, não opinião:

| Achado | Gravidade |
|---|---|
| `INVENTED`, `INVENTED_DECISION` | crítico |
| `FALSE_CONFIRMED` | crítico |
| `LOST_CRITICAL`, `LOST_DECISION` | crítico |
| `UNDUE_ADVANCE` | crítico |
| `PHASE_MISMATCH`, `REPORT_INCOMPLETE` | crítico |
| `LOST`, `STATE_DRIFT` | aviso |

Contra o oráculo mede os três limiares que o próprio oráculo declara: `critical_recall ≥ 1.0`,
`critical_false_confirmed ≤ 0`, `improper_gate_advances ≤ 0`.

**`summary` sobre um `runs/` vazio devolve `SEM EXECUÇÃO`, nunca GO.** Um P8 sem sessões
reais não é um P8 verde; é um P8 por fazer.

E há uma guarda contra este relatório: `GuardaContraOProprioRelatorio` falha se as linhas de
E01/E02 deixarem de dizer `NÃO EXECUTADO` sem existir um veredicto em `runs/`.

---

## 6. Defeitos corrigidos por caminho

### 6.1 Verde falso em `test_scan_limits.py`

`test_failure_handler_survives_an_unwritable_target` usava `Z:/inexistente/sem-permissao/x.json`
como alvo «inescrevível». Em Windows é uma drive que não existe; **em POSIX é um caminho
relativo**. E `_write_json` cria os directórios — portanto o teste escrevia mesmo o ficheiro,
na raiz do repositório, passava com `rc=0` pelo motivo errado, e nunca tocou no ramo que diz
testar.

Corrigido: o alvo passa a ter como pai um ficheiro regular (`ENOTDIR` em POSIX e em Windows,
sem depender de permissões), com asserção de que nada ficou escrito. O `Z:/` que a suite
deixava na raiz desapareceu.

### 6.2 Leitura silenciosa do vazio, sexta ocorrência

A captura de verdade lia `model["decisions"]`. A chave real é `model["status"]["decisions"]`.
Resultado: `decisions: []` num piloto com `D-001` e `D-002` escritas — zero que se lê como
«não há decisões», sem uma queixa.

Apanhado por os números não baterem, não por um teste vermelho. Corrigido, e com guarda:
`GuardaContraALeituraSilenciosaDoVazio` corre contra o engagement real e compara as decisões
capturadas com as que estão escritas em `decisions.md`.

### 6.3 O mesmo mecanismo do P2, outra vez

O helper `eng_falso` substituía `C_local["truth"]`. `runpy.run_path` devolve uma **cópia** do
namespace, logo `oracle` continuava a chamar o `truth` real sobre um tmpdir vazio — quatro
testes passavam a medir nada. Corrigido com `__globals__`, e a razão ficou escrita na
docstring para não voltar.

---

## 7. Defeito observado e não corrigido

`library/kernel/tools/xlsx_extract.py:2859` — `DeprecationWarning: invalid escape sequence '\|'`.

```python
ftxt = short(head_step["formula"], 64).replace("|", "\|") if head_step else ""
```

Pré-existente, fora do âmbito de P8, e será erro em versões futuras de Python. Não foi
tocado. Fica registado.

---

## 8. Regressão

| Fase | Ficheiros | Testes | Falhas | Erros | Skips | xfail |
|---|---|---|---|---|---|---|
| P7 | 56 | 2232 | 0 | 0 | 14 | 3 |
| **P8** | **59** | **2300** | **0** | **0** | **14** | **3** |

Três ficheiros novos, 68 testes novos (22 + 16 + 30), zero regressões. Duas corridas
independentes deram o mesmo número.

Os testes de E05 sobre o ficheiro real desdobraram-se de dois para três quando o `.xlsx`
entrou: o autoritativo **não tem macros**, logo afirmar VBA sobre ele seria afirmar o que lá
não está. Agora o add-in afirma-se sobre o livro activo, as macros sobre o livro que as tem
(arquivado em `_superseded/`), e um terceiro teste afirma que a **ausência** de VBA no
autoritativo é facto sobre ele, não falha a corrigir.

---

## 9. Próxima acção concreta

**Não é P9.** `IMPLEMENTATION_PLAN.md` é explícito: *«Checkpoint: E01–E05 e todos os testes
novos/antigos. GO obrigatório antes de simplificar.»* E §7: cada remoção de P9 obriga a
*«repetir pilotos afetados»* — sem pilotos corridos não há baseline contra o qual repetir.

Por ordem:

1. ~~O dono envia o `.xlsx` autoritativo (sha `cf40be3e…`).~~ **Feito a 2026-09-22, verificado.**
2. ~~Substituir o input do piloto de pricing.~~ **Feito**; `.xlsm` arquivado em `_superseded/`.
3. Executar `docs/evolution/p8/PROTOCOLO.md` nos dois engagements. O `/capture` sobre o
   `.xlsx` é o cp1 do braço de pricing — corre dentro da sessão real, não antes dela.
4. `compare.py summary --runs docs/evolution/p8/runs/` → GO ou NO-GO por código.
5. Só então P9.

Resta **um** bloqueio, e é o mesmo desde o início: sessões Claude Code independentes exigem
uma pessoa a abri-las e fechá-las.
