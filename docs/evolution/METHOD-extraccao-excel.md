# Método — extracção independente de um Excel de negócio

Como foi extraído o `PREÇO BANCAS_03_08_26.xlsm` (18 folhas, 13 262 fórmulas, VBA) para o
oráculo de P8, e como repetir noutro ficheiro.

O objectivo **não** é perceber o ficheiro todo. É produzir afirmações que se sustentem, saber
onde param, e dizê-lo. Um oráculo com 8 factos verificados e 2 lacunas declaradas vale mais
do que 20 factos plausíveis.

## Regra zero — de onde se lê

Ler a **fonte**, nunca `_capture/`. O `_capture/` é output do candidato; um oráculo derivado
dele mede o candidato contra ele próprio (`ACCEPTANCE.md` §5). Isto não é formalidade: é a
única coisa que separa uma referência de um eco.

## 1. Resolver o ficheiro antes de o abrir

```bash
python3 -c "
import os
d='projects/<slug>/inputs'
for n in os.listdir(d): print(repr(n), os.path.getsize(os.path.join(d,n)))"
```

`repr()`, não `print()`. O nome real no disco era
`'PRE#U00c7O BANCAS_03_08_26.xlsm'` — o `Ç` vinha mangled da importação. Abrir pelo nome
"correcto" dá `FileNotFoundError` e faz perder tempo a duvidar do caminho. **Os locators do
oráculo têm de usar o nome literal.**

Identidade, sempre, antes de qualquer leitura:

```python
sha = hashlib.sha256(open(f,'rb').read()).hexdigest()
```

## 2. Abrir para ler FÓRMULAS, não valores

```python
wb = openpyxl.load_workbook(f, data_only=False, keep_vba=True)
```

- `data_only=False` — **o essencial**. Com `True` vêm os valores em cache da última vez que
  o Excel gravou, e perde-se a regra inteira. A regra é a fórmula; o valor é um resultado
  datado.
- `keep_vba=True` — preserva e permite detectar macros.

Ler os *warnings* que o openpyxl emite e registá-los como limite de extracção. Neste ficheiro:

```
UserWarning: Data Validation extension is not supported and will be removed
```

Há validação de dados no livro que esta leitura **não vê**. Isso entra em
`extraction_limits`, não se ignora.

## 3. Panorâmica: onde vive a lógica

```python
for ws in wb.worksheets:
    fx = sum(1 for row in ws.iter_rows() for c in row
             if isinstance(c.value, str) and c.value.startswith("="))
    print(ws.title, ws.max_row, ws.max_column, fx)
```

O resultado diz logo onde investir. Aqui: `Inputs` com 7906 fórmulas era o motor, `Capa` com
0 era decoração, `UlyssesQuotes` com 525 linhas e **zero** fórmulas era dados importados —
e "zero fórmulas numa folha grande" é assinatura de *feed externo*, não de cálculo.

## 4. Named ranges — o melhor sinal do ficheiro

```python
names = [n for n in wb.defined_names if not n.startswith("_xl")]
```

Filtrar `_xl*` (internos do Excel). Os 134 restantes eram o modelo de dados explícito, num
padrão `<Cliente>_<Produto>_<Componente>`:

```python
pat = re.compile(r"^(.+?)_(380|IFO18005|MGO|[A-Z0-9]+)_(.+)$")
```

Deu 11 clientes × 22 produtos × 47 componentes, sem abrir uma única fórmula. **Quem nomeia
intervalos está a documentar o seu modelo de domínio.** Guardar os não-parseados e olhá-los:
foi assim que apareceram `Data_Lista`, `Data_Manual`, `Index_TaxaCâmbio`.

Resolver os nomes para o seu alvo é o passo que mais rende:

```python
wb.defined_names.get("Data_Lista").value   # -> Inputs!$B$9:$B$1469
```

`Data_Lista` e `Index_TaxaCâmbio` apontavam ambos para `$9:$1469` — **série temporal de 1461
linhas**. `Data_Output` (`Outputs!$C$6`) e `Data_Manual` (`Outputs!$C$7`), duas células
isoladas, revelaram uma **superfície de intervenção manual** que nenhuma fórmula anunciava.

## 5. Padrões de fórmula, não fórmulas

Normalizar os números de linha e comparar conjuntos:

```python
p = re.sub(r'(?<=[A-Z$])\d+', 'N', c.value)   # A5 -> AN, $Z$3 -> $Z$N
```

103 células com o mesmo padrão são **uma** regra, não 103. Na folha de tickets, 10 colunas
colapsaram em 10 regras legíveis.

**Onde isto falha, e é preciso saber:** nas folhas `Outputs`/`eur_ton`, 676 fórmulas deram
251 padrões do tipo `=$Z$N+AKN-AKN-#`. Sinal baixo — são referências de célula cruas, sem
semântica. Lição: **o padrão rende onde há nomes; onde há só coordenadas, dá pouco.** Não
insistir; declarar a lacuna (foi o que originou `P-10`).

## 6. Comparar folhas irmãs — o achado mais valioso

Quatro folhas pareciam quatro cálculos:

```python
sig = {s: {re.sub(r'\d+','#', c.value) for row in wb[s].iter_rows() for c in row
           if isinstance(c.value,str) and c.value.startswith("=")}
       for s in ("usd_ton","eur_ton","usd_m3","eur_m3")}
# interseção == união  ->  249/249
```

**249 de 249 padrões partilhados, mesmas dimensões 80×104.** Um cálculo em quatro
apresentações (moeda × unidade), não quatro regras.

Este é o tipo de facto que muda a estimativa por um factor de 4. Vale sempre a pena procurar
folhas gémeas antes de estimar seja o que for.

## 7. Uma folha é inerte? Varrer o livro inteiro

```python
for s in wb.worksheets:
    for row in s.iter_rows():
        for c in row:
            if isinstance(c.value,str) and "<NomeDaFolha>" in c.value: ...
```

No ficheiro de tickets, `Dayly_extraction_closed` — 158 linhas — **não era referenciada por
nenhuma fórmula**. Está no livro, é carregada, e é inerte na lógica. Afirmar que os tickets
fechados alimentam a priorização seria facto falso; só se soube por varrimento exaustivo.

## 8. VBA: detectar mesmo sem ler

```python
vba = [n for n in zipfile.ZipFile(f).namelist() if "vba" in n.lower()]
# -> ['xl/vbaProject.bin']
```

Um `.xlsm` é um zip. Detectar é barato; descompilar não. **Detectar e declarar como âmbito
não medido** é honesto e é o que foi feito (`P-06`). Estimar um processo só pelas fórmulas,
havendo VBA, subestima-o — e isso tem de constar do oráculo.

## 9. Armadilhas encontradas

| Armadilha | Sintoma | Resposta |
|---|---|---|
| Nome mangled no disco | `FileNotFoundError` num caminho "certo" | `repr()` do `listdir`; locators com o nome literal |
| `data_only=True` | Vêm números, some a regra | Sempre `data_only=False` |
| `ArrayFormula` | Imprime `<openpyxl...ArrayFormula object>`, não bate em `startswith("=")` | Tratar à parte; declarar se não foi expandida |
| Offset de cabeçalho | 91 linhas mas 89 fórmulas | Confirmar a linha de cabeçalho antes de contar |
| Padrão em folhas sem nomes | Muitos padrões, pouco sentido | Não insistir; declarar lacuna |
| Warning do openpyxl | Silencioso se não se ler | Ler o stderr e registar em `extraction_limits` |

## 10. Contar o que não existe

O que a fonte **não** diz é material e entra como `Unknown`, com locator da ausência:

- tickets: 60 High, 29 Medium, **0 Low** — o cabeçalho declara `High/Medium/Low`. Vocabulário
  declarado maior do que o usado. Não inferir que `Low` está proibido.
- tickets: `Exec. Order` preenchida em **37 de 89**. A ordenação fina aplica-se a um
  subconjunto.
- pricing: quais dos 11×22 pares estão activos — os named ranges não distinguem activo de
  legado.

## 11. Saber parar

O critério de paragem foi explícito: **estrutura traçada exaustivamente, aritmética não.**

Traçado: named ranges, simetria entre folhas, dimensões, contagens, referências cruzadas,
presença de VBA. Não traçado: que componente entra em que preço, com que sinal e em que
ordem, através de 13 262 fórmulas.

Isso foi escrito como `P-10`, `Unknown` **crítico**, com o custo de o fechar declarado
(traçar `Inputs` célula a célula, ou dez minutos do responsável). **A alternativa — escrever
uma ordem plausível dos componentes — teria produzido um oráculo que parece completo e está
errado**, e P8 mediria o candidato contra ficção.

Um oráculo com lacunas declaradas é utilizável. Um oráculo com lacunas preenchidas por
plausibilidade é pior do que nenhum, porque ninguém sabe quais das linhas confiar.

## 12. Limite que o método não resolve

Tudo isto cumpre a letra da `ACCEPTANCE.md` — a fonte foi lida directamente, nunca o output
do candidato. Mas o autor do oráculo e o operador do candidato continuam a ser **o mesmo
agente**. Nenhum rigor de extracção fecha esse buraco.

Por isso os 13 itens críticos ficam `PENDING_OWNER`: só contam como referência de P8 depois
de o responsável do processo os confirmar ou corrigir.
