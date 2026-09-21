# excel-patterns — Excel to Power Fx / T-SQL Translation Catalogue

**Source:** transplanted 2026-05-28 from the previous-aisa references.
**Consulted by:** `lens-technology`, `solution-architect`, the `implementation-spec` and `claude-design-brief` deliverable templates (Options / Decision phase).
**Phase eligibility:** Options + Decision only (this file names vendors and products — never consulted from Discovery lenses).

The catalogue is exhaustive for the patterns that appear in most Power Platform discovery datasets. It is the bridge between the **as-is** in Excel (which the operations + data lenses surface in Discovery) and the **to-be** in Power Fx or T-SQL (which the solution-architect proposes in Options).

---

## ARITHMETIC

| Excel | Power Fx | T-SQL | Notes |
|---|---|---|---|
| `=A*B` | `colA * colB` | `[colA] * [colB]` | Direct |
| `=A+B` | `colA + colB` | `[colA] + [colB]` | Direct |
| `=A-B` | `colA - colB` | `[colA] - [colB]` | Direct |
| `=A/B` | `If(colB<>0, colA/colB, 0)` | `CASE WHEN [colB]<>0 THEN [colA]/[colB] ELSE 0 END` | ALWAYS zero-guard |
| `=ROUND(A,2)` | `Round(colA, 2)` | `ROUND([colA], 2)` | Direct |
| `=ROUNDUP(A,0)` | `RoundUp(colA, 0)` | `CEILING([colA], 1)` | |
| `=ROUNDDOWN(A,0)` | `RoundDown(colA, 0)` | `FLOOR([colA], 1)` | |
| `=ABS(A)` | `Abs(colA)` | `ABS([colA])` | Direct |
| `=MOD(A,B)` | `Mod(colA, colB)` | `[colA] % [colB]` | |
| `=INT(A)` | `Int(colA)` | `FLOOR([colA], 1)` | |
| `=POWER(A,B)` | `Power(colA, colB)` | `POWER([colA], [colB])` | |
| `=SQRT(A)` | `Sqrt(colA)` | `SQRT([colA])` | |

---

## CONDITIONAL

| Excel | Power Fx | T-SQL | Notes |
|---|---|---|---|
| `=IF(A>0,"Y","N")` | `If(colA>0,"Y","N")` | `CASE WHEN [colA]>0 THEN 'Y' ELSE 'N' END` | |
| `=IF(ISBLANK(A),"",A)` | `If(IsBlank(colA),"",colA)` | `COALESCE([colA],'')` | |
| `=IF(AND(A,B),1,0)` | `If(colA && colB,1,0)` | `CASE WHEN [colA]=1 AND [colB]=1 THEN 1 ELSE 0 END` | |
| `=IF(OR(A,B),1,0)` | `If(colA \|\| colB,1,0)` | `CASE WHEN [colA]=1 OR [colB]=1 THEN 1 ELSE 0 END` | |
| `=IFS(A=1,"L",A=2,"M",A=3,"H")` | `Switch(colA,1,"L",2,"M",3,"H")` | `CASE [colA] WHEN 1 THEN 'L' WHEN 2 THEN 'M' ELSE 'H' END` | |
| `=IFERROR(A/B,0)` | `IfError(colA/colB,0)` | `TRY_CAST([colA]/NULLIF([colB],0) AS DECIMAL(18,4))` | Prefer explicit zero-guard |
| Nested IF (3+ levels) | `Switch` or flatten | `CASE...WHEN...END` | Use Switch in PFx |

---

## LOOKUP

| Excel | Power Fx | Delegation | Notes |
|---|---|---|---|
| `=VLOOKUP(k,T,n,0)` | `LookUp(Table, KeyCol=k, ResultCol)` | OK if KeyCol indexed | Most common pattern |
| `=INDEX(MATCH(...))` | `LookUp(Table, KeyCol=k, ResultCol)` | OK if KeyCol indexed | Same as VLOOKUP |
| `=XLOOKUP(k,arr,ret)` | `LookUp(Table, KeyCol=k, ResultCol)` | OK if KeyCol indexed | |
| Lookup on non-PK | `LookUp(Table, Col=k, Result)` | WARN — check if searchable | Add delegation warning |
| Lookup with calculation | `LookUp(Table, Col=k, ColA * ColB)` | WARN — non-delegable calc | Use collection workaround |

**Safe LookUp pattern:**
```powerfx
With(
 {varResult: LookUp(cr_products, cr_productid = ddProduct.Selected.cr_productid, cr_unitprice)},
 If(IsBlank(varResult), 0, varResult)
)
```

**T-SQL equivalent:**
```sql
SELECT p.[unit_price]
FROM [dbo].[slv_product] p
WHERE p.[id] = @product_id
```

---

## AGGREGATION

| Excel | Power Fx | Delegation (Dataverse) | T-SQL |
|---|---|---|---|
| `=SUM(col)` | `Sum(Table, Column)` | OK | `SUM([col])` |
| `=COUNT(col)` | `CountRows(Table)` | OK | `COUNT(*)` |
| `=AVERAGE(col)` | `Average(Table, Column)` | OK | `AVG([col])` |
| `=MAX(col)` | `Max(Table, Column)` | OK | `MAX([col])` |
| `=MIN(col)` | `Min(Table, Column)` | OK | `MIN([col])` |
| `=SUMIF(r,c,s)` | `Sum(Filter(T,Cond),Col)` | WARN — only if Cond delegable | `SUM(CASE WHEN [c] THEN [s] END)` |
| `=COUNTIF(r,c)` | `CountIf(Table,Cond)` | WARN — only if Cond delegable | `COUNT(CASE WHEN [c] THEN 1 END)` |
| `=AVERAGEIF(r,c,a)` | `Average(Filter(T,C),Col)` | WARN | `AVG(CASE WHEN [c] THEN [a] END)` |
| `=SUMPRODUCT(A,B)` | NEVER — use Power Automate | N/A | `SUM([a]*[b])` in SQL |

**SUMPRODUCT Power Automate pattern:**
```
Initialize: weighted_sum = 0, total_weight = 0
Apply to Each record:
 weighted_sum += record.[quantity] * record.[value]
 total_weight += record.[quantity]
Result: IF total_weight > 0 THEN weighted_sum / total_weight ELSE 0
```

**Collection workaround for non-delegable aggregation:**
```powerfx
// OnVisible of screen — preload with delegable filter first
ClearCollect(colFilteredQuotes,
 Filter(cr_quote, cr_status = "Active") // delegable condition
);
// Then aggregate locally (no delegation limit on collections)
Sum(colFilteredQuotes, cr_totalvalue)
```

---

## TEXT

| Excel | Power Fx | T-SQL | Notes |
|---|---|---|---|
| `=A&" "&B` | `colA & " " & colB` | `[colA] + ' ' + [colB]` | |
| `=CONCATENATE(A,B)` | `colA & colB` | `CONCAT([colA],[colB])` | |
| `=LEFT(A,3)` | `Left(colA,3)` | `LEFT([colA],3)` | |
| `=RIGHT(A,3)` | `Right(colA,3)` | `RIGHT([colA],3)` | |
| `=MID(A,2,5)` | `Mid(colA,2,5)` | `SUBSTRING([colA],2,5)` | |
| `=LEN(A)` | `Len(colA)` | `LEN([colA])` | |
| `=UPPER(A)` | `Upper(colA)` | `UPPER([colA])` | |
| `=LOWER(A)` | `Lower(colA)` | `LOWER([colA])` | |
| `=TRIM(A)` | `Trim(colA)` | `TRIM([colA])` | |
| `=SUBSTITUTE(A,"x","y")` | `Substitute(colA,"x","y")` | `REPLACE([colA],'x','y')` | |
| `=TEXT(A,"dd/mm/yyyy")` | `Text(colA,"dd/mm/yyyy")` | `FORMAT([colA],'dd/MM/yyyy')` | |
| `=TEXT(A,"#,##0.00")` | `Text(colA,"[$-pt-PT]#,##0.00")` | `FORMAT([colA],'N2')` | |

---

## DATE / TIME

| Excel | Power Fx | T-SQL | Notes |
|---|---|---|---|
| `=TODAY` | `Today` | `CAST(SYSUTCDATETIME AS DATE)` | |
| `=NOW` | `Now` | `SYSUTCDATETIME` | |
| `=YEAR(A)` | `Year(colA)` | `YEAR([colA])` | |
| `=MONTH(A)` | `Month(colA)` | `MONTH([colA])` | |
| `=DAY(A)` | `Day(colA)` | `DAY([colA])` | |
| `=DATE(y,m,d)` | `Date(y,m,d)` | `DATEFROMPARTS([y],[m],[d])` | |
| `=DATEDIF(A,B,"D")` | `DateDiff(colA,colB,TimeUnit.Days)` | `DATEDIFF(DAY,[colA],[colB])` | |
| `=DATEDIF(A,B,"M")` | `DateDiff(colA,colB,TimeUnit.Months)` | `DATEDIFF(MONTH,[colA],[colB])` | |
| `=EDATE(A,3)` | `DateAdd(colA,3,TimeUnit.Months)` | `DATEADD(MONTH,3,[colA])` | |
| `=EOMONTH(A,0)` | `DateAdd(Date(Year(colA),Month(colA)+1,1),-1,TimeUnit.Days)` | `EOMONTH([colA],0)` | No native in PFx |
| `=WORKDAY(A,5)` | WARN — approximation only (see trap) | `[custom SP with holiday table]` | |
| `=NETWORKDAYS(A,B)` | WARN — no native (see trap) | `[custom SP with holiday table]` | |

**WORKDAY Power Fx approximation (Mon-Fri, no holidays):**
```powerfx
// WARNING: approximation — does NOT account for public holidays.
// For accurate results: implement via Power Automate with a cr_holidays table.
DateAdd(
 startDate,
 days + (RoundDown(days/5,0) * 2) +
 If(Weekday(startDate,StartOfWeek.Monday) + Mod(days,5) > 5, 2,
 If(Weekday(startDate,StartOfWeek.Monday) + Mod(days,5) > 6, 1, 0)
 ),
 TimeUnit.Days
)
```

---

## FINANCIAL — NEVER IN POWER FX

All financial functions require Power Automate or T-SQL implementation.

| Excel | Power Fx | Implementation |
|---|---|---|
| `=PMT(r,n,pv)` | NEVER | PA: `pv * r / (1 - POWER(1+r, -n))` |
| `=NPV(r,vals)` | NEVER | PA: iterate cashflows, discount each, sum |
| `=IRR(vals)` | NEVER | PA: Newton-Raphson iteration (max 100 iter) |
| `=XNPV(r,v,d)` | NEVER | PA: date-weighted NPV |
| `=XIRR(v,d)` | NEVER | PA: date-weighted IRR with Newton-Raphson |
| `=FV(r,n,pmt)` | NEVER | PA: `pmt * ((POWER(1+r,n)-1)/r)` |

**PMT Power Automate pseudocode:**
```
INPUTS: @rate (decimal per period), @nper (int), @pv (decimal)
IF @rate = 0:
 result = @pv / @nper
ELSE:
 result = @pv * @rate / (1 - POWER(1 + @rate, -@nper))
OUTPUT: Write result to [entity].[column]
```

**IRR Newton-Raphson pseudocode:**
```
INPUTS: @cashflows (array of decimals, period 0 is negative investment)
Initialize: irr = 0.1 (10% guess), iteration = 0, max_iter = 100
WHILE ABS(npv) > 0.0001 AND iteration < max_iter:
 npv = SUM(cashflow[t] / POWER(1+irr, t)) for each period t
 npv_prime = SUM(-t * cashflow[t] / POWER(1+irr, t+1)) for each period t
 irr = irr - npv / npv_prime
 iteration++
OUTPUT: irr (as decimal, e.g., 0.1234 = 12.34%)
```

---

## ARRAY / DYNAMIC (Excel 365)

| Excel | Power Fx | Notes |
|---|---|---|
| `=FILTER(range,cond)` | `Filter(Table,Cond)` | Delegation check required |
| `=UNIQUE(range)` | `Distinct(Table,Column)` | Delegable |
| `=SORT(range,col)` | `Sort(Table,Column,SortOrder.Ascending)` | Delegable |
| `=SEQUENCE(n)` | `Sequence(n)` | Local only |
| `=XLOOKUP(...)` | `LookUp(Table,Cond,Result)` | Delegation check |
