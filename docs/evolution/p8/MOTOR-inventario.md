# Folha `Motor` — inventário

> Fonte: `projects/pricing-bunkers-pilot-4/inputs/PREÇO BANCAS_03_08_26.xlsx`
> sha256 `cf40be3ed65983d51e689d9d34ba1714fdb204794d34e89352be667be1692b52` · 2026-09-22
> Método: leitura directa das células com `openpyxl` (fórmulas **e** valores em cache).
> Nada aqui é inferido. Onde a folha não diz, este documento não diz.

## Porque é que este documento existe

`Motor` **não existe no `.xlsm` substituído**. É uma das três folhas que só aparecem no
ficheiro autoritativo:

| `.xlsm` (18 folhas) | `.xlsx` (19 folhas) |
|---|---|
| `Outputs` | → `Relatório Preços` (renomeada) |
| `Outputs BIOS` | → `Relatório Preços Bios` (renomeada) |
| — | **`Motor`** (nova) |

Foi inventariada antes de o protocolo P8 correr, para que um item de oráculo mal ancorado
apareça agora e não ao fim de 18 reinícios de sessão.

## O que é

Grelha de cálculo declarada `A1:N60`; **conteúdo real em `B1:I53`** (linhas 54–60 e colunas
J–N vazias). A própria folha diz o que é, em `B2`: *«Folha de suporte — não imprimir»*.

Três blocos.

### Bloco 1 — fatores de conversão (`B3:C10`)

| célula | rótulo | conteúdo |
|---|---|---|
| `C5` | Divisor FX | `=IF('Relatório Preços'!$D$5="EUR",'Relatório Preços'!$F$5,1)` |
| `C6` | Densidade VLSFO | `=IF('Relatório Preços'!$E$5="M3",0.953,1)` |
| `C7` | Densidade HSFO | `=IF('Relatório Preços'!$E$5="M3",0.989,1)` |
| `C8` | Densidade MGO/IFO | `=IF('Relatório Preços'!$E$5="M3",0.855,1)` |
| `C9` | Ajuste preço referência | `10` (constante) |
| `C10` | Desconto CT (MGO) | `5` (constante) |

`C9` e `C10` são os `−10` e `−5` que a regra de porto do P-10 usa. Aqui são **constantes
nomeadas na folha**, não números soltos da especificação.

### Bloco 2 — índices diários e médias semanais (`B12:H33`)

Cinco colunas de índice, mais a taxa de câmbio:

| coluna | índice (`linha 13`) |
|---|---|
| `C` | CIF MED DMA 0,1 |
| `D` | CIF MED 3,5 |
| `E` | 0.5% FOB Rdam barge |
| `F` | Diesel 10ppm NWE |
| `G` | CIF NWE DMA 0,1 |
| `H` | USD (FX) |

| linhas | conteúdo |
|---|---|
| `14:18` | dias da **semana N−1** |
| `19:23` | dias da **semana N** |
| `24` | `Média Semana N` = `=IF(SUM(C19:C23)=0,0,AVERAGEIF(C19:C23,"<>0"))` |
| `28` | `Média Semana N−1` = mesma forma sobre `14:18` |
| `25` / `29` | `Prémio (USD/MT)` — `XLOOKUP` sobre `Index_<índice>_Prémio` |
| `26` / `30` | `SLI'S (USD/MT)` — `XLOOKUP` sobre `Index_<índice>_SLI` |
| `27` / `31` | `Tot.Enc. (USD/MT)` = `=+C26+C25` |
| `32` | `Variação usd` = `=+C24-C28` |
| `33` | `Variação euro` = `=IF(OR($H$24=0,$H$28=0),0,+C24/$H$24-C28/$H$28)` |

A âncora de data é `B19`:
`=IF(WEEKDAY(Data_Output,2)=1,Data_Output,Data_Output-WEEKDAY(Data_Output,2)+1)` —
a semana alinha-se pela segunda-feira a partir de `Data_Output`. As restantes datas derivam
por `±1` dia, com `B18 = B19-3` a saltar o fim-de-semana.

Média que ignora zeros (`AVERAGEIF(...,"<>0")`): um dia sem cotação **não puxa a média para
baixo**, é excluído. É regra de negócio, não detalhe de fórmula.

### Bloco 3 — cálculos intermédios de preço (`B35:I53`)

Dois blocos idênticos em forma: **Semana N+1** (`39:45`, FX `=+H24`) e **Semana N**
(`47:53`, FX `=+H28`).

Sete colunas de produto (`linha 39`): `380` · `VLSFO 0,5%` · `MGO` · `FUEL1%` · `IFO180` ·
`GMC Prio/Aveiro (€/M3)` · `GMC Sines (€/M3)`.

| linha | rótulo | fórmula (coluna `C`, produto `380`) |
|---|---|---|
| `40` | Cedência EUR | `=IFERROR(C41/$D$37,0)` |
| `41` | Cedência USD | `=+D24+D27` — média + encargo |
| `42` | Margem Alvo EUR | `=XLOOKUP(Data_Output,Data_Lista,PreçosSpot_380_Margem)` |
| `43` | Margem Alvo USD | `=C42*$D$37` |
| `44` | Preço EUR | `=C40+C42` |
| `45` | Preço USD | `=+C41+C43` |

## O que isto verifica do P-10

O item P-10 do oráculo estava `CLOSED_BY_OPERATOR_SPEC` — fechado pela especificação, não
pelo ficheiro. Quatro das suas regras passam agora a ser verificáveis **na fonte**:

| regra P-10 | célula | fórmula |
|---|---|---|
| `encargo = prémio + SLI` | `Motor!C27` | `=+C26+C25` ✓ |
| `cedência = média(Platts) + encargo` | `Motor!C41` | `=+D24+D27` ✓ |
| `IFO180 = 0,9×VLSFO + 0,1×DMA` | `Motor!G41` | `=+D41*0.9+E41*0.1` ✓ |
| `margem USD = margem EUR × FX` | `Motor!C43` | `=C42*$D$37` ✓ |
| `PREÇO USD = cedência USD + margem USD` | `Motor!C45` | `=+C41+C43` ✓ |

E confirma a resposta do operador sobre a conversão do SLI: `Motor!C26` é
`=XLOOKUP(...Index_CIFMEDDMA_SLI)*$H$24` — o SLI é multiplicado pela média FX. Nas colunas
`E` e `F` (`0.5% FOB Rdam barge`, `Diesel 10ppm NWE`) **não há** `*$H$24`, exactamente como
o P-10 já registava.

## O que o `Motor` NÃO contém

A regra de porto do P-10 — `O03 porto = mínimo(produto/período) + logística do porto − 10`,
com `MGO: mínimo DMA + logística − 5 − 10` — **não está nesta folha**. O `Motor` pára no
preço por produto. As constantes `10` e `5` estão aqui (`C9`, `C10`); a aplicação delas vive
noutro lado, ainda por localizar.

Fica como está: não se afirma onde não foi visto.

## Consequência para o protocolo

Os **dez** itens críticos do oráculo, verificados um a um contra o ficheiro autoritativo:

| item | ancorado em | veredicto |
|---|---|---|
| `P-01` | anexos do `.xlsx` | já re-medido em P1 sobre o autoritativo |
| `P-02` | named ranges | **sem problema** — os 127 nomes de padrão `<Cliente>_<Produto>_<Componente>` são idênticos nas duas versões, alvos incluídos. Só muda o nome da folha do scope |
| `P-03` | `UlyssesQuotes!A1:J525` | **sem problema** — folha idêntica: mesmas dimensões, mesmas 10 colunas, mesmos cabeçalhos `model://` |
| `P-04` | anexos do `.xlsx` | já re-medido em P1 sobre o autoritativo |
| `P-05` | named ranges `Data_*` | **RE-ANCORADO** — era o único a apontar para `Outputs` (ver `remeasurements` no oráculo) |
| `P-06` | `xl/vbaProject.bin` do `.xlsm` | **sem problema** — a proposição já cobre as duas versões («o autoritativo não tem VBA sequer»), e o locator resolve porque o `.xlsm` foi arquivado em `inputs/_superseded/` e não apagado |
| `P-10` | especificação | **reforçado** — cinco das suas regras passam de «fechado pela spec» a verificáveis no ficheiro (tabela acima) |
| `P-12` | especificação | não toca no livro |
| `P-13` | especificação | não toca no livro |
| `P-14` | P-10 × P-12 | não toca no livro |

`P-02`, `P-03` e `P-06` mantêm `source_sha256` do `.xlsm` — o campo está desactualizado, o
conteúdo não. Não foram tocados: re-ancorar um item que verifica seria mexer na referência
independente sem razão.
