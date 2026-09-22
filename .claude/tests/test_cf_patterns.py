# -*- coding: utf-8 -*-
"""Formatacao condicional: 21 982 regras para dizer duas coisas.

Medido no piloto real de pricing, ANTES desta correccao:

    _capture/…xlsm.extraction.json        6 313 KB
      sheets.conditional_formatting        3 359 KB   ← 77% do ficheiro
      sheets.columns                         972 KB

    folha `Inputs`: 21 982 regras de formatacao condicional

O Excel explode uma regra em milhares de instancias quando se copiam linhas. Normalizadas
para R1C1 — **o mesmo `normalize_formula` que o motor ja usa para colapsar fill-downs nas
formulas de coluna** — as 21 982 sao SETE padroes: «hoje» e «fim-de-semana», repetidos
dez mil vezes cada.

Isto nao e um detalhe de tamanho. O passo L2 da captura (`aisa-capture` 5b2) declara um
orcamento de ~200 KB para os JSONs e manda ler todos: a 6,3 MB o passo demora 15+ minutos
e a maior parte do que se le e a mesma regra outra vez.

O que NAO pode perder-se, e por isso esta fixado abaixo: o numero de instancias, os
intervalos, as cores, e uma formula em A1 por padrao — `_cf_thresholds` colhe limiares
delas (`$I5>=30`) e `extract_fills` precisa do conjunto de `fill_rgb`. Agrupar nao e
amostrar."""
import json
import os
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
XLSX_PY = ROOT / "library" / "kernel" / "tools" / "xlsx_extract.py"
X = runpy.run_path(str(XLSX_PY))

try:
    import openpyxl  # noqa: F401
    HAVE = True
except ImportError:
    HAVE = False


def livro_com_cf_repetida(destino, linhas=300):
    """Uma regra por linha, como o Excel escreve depois de copiar — e duas cores."""
    from openpyxl import Workbook
    from openpyxl.formatting.rule import FormulaRule
    from openpyxl.styles import PatternFill

    wb = Workbook(); ws = wb.active; ws.title = "Inputs"
    ws["A1"] = "data"; ws["B1"] = "valor"
    amarelo = PatternFill(start_color="FFFFEB9C", end_color="FFFFEB9C", fill_type="solid")
    for i in range(2, linhas + 2):
        ws.cell(row=i, column=1, value="2026-01-01")
        ws.cell(row=i, column=2, value=i)
        ws.conditional_formatting.add(
            "A{r}:B{r}".format(r=i),
            FormulaRule(formula=["$A{r}=TODAY()".format(r=i)], fill=amarelo))
    # uma regra genuinamente diferente, que NAO pode desaparecer no agrupamento
    ws.conditional_formatting.add("D1:D9", FormulaRule(formula=['$D1>=30'], fill=amarelo))
    # a MESMA formula com outra cor: mesma condicao, outro significado visual
    vermelho = PatternFill(start_color="FFFFC7CE", end_color="FFFFC7CE", fill_type="solid")
    ws.conditional_formatting.add("E1:E9", FormulaRule(formula=['$D1>=30'], fill=vermelho))
    wb.save(str(destino))
    return destino


def extrai(tmp, livro):
    saida = os.path.join(tmp, "out.extraction.json")
    p = subprocess.run([sys.executable, str(XLSX_PY), str(livro), saida, "--force"],
                       capture_output=True, text=True, timeout=600)
    doc = json.loads(Path(saida).read_text(encoding="utf-8")) if os.path.exists(saida) else {}
    return p, doc, saida


def folha(doc, nome="Inputs"):
    return next(s for s in doc["sheets"] if s["name"] == nome)


@unittest.skipUnless(HAVE, "openpyxl ausente")
class C1_OColapso(unittest.TestCase):

    def test_repeated_rules_collapse_to_patterns(self):
        with tempfile.TemporaryDirectory() as tmp:
            _p, doc, _s = extrai(tmp, livro_com_cf_repetida(Path(tmp) / "l.xlsx"))
        cf = folha(doc)["conditional_formatting"]
        self.assertLessEqual(len(cf), 5,
                             "300 copias da mesma regra continuam 300 registos: {}".format(len(cf)))

    def test_the_instance_count_survives(self):
        """Quantas vezes a regra existe e informacao de negocio — nao se deita fora."""
        with tempfile.TemporaryDirectory() as tmp:
            _p, doc, _s = extrai(tmp, livro_com_cf_repetida(Path(tmp) / "l.xlsx"))
        cf = folha(doc)["conditional_formatting"]
        total = sum(r.get("instances", 1) for r in cf)
        self.assertEqual(total, 302, "as instancias nao somam as regras originais")

    def test_each_pattern_says_what_it_is(self):
        with tempfile.TemporaryDirectory() as tmp:
            _p, doc, _s = extrai(tmp, livro_com_cf_repetida(Path(tmp) / "l.xlsx"))
        r = folha(doc)["conditional_formatting"][0]
        for campo in ("range", "type", "formulas", "fill_rgb", "instances", "pattern"):
            self.assertIn(campo, r, "falta `{}` no padrao".format(campo))
        self.assertTrue(r["pattern"], "o padrao R1C1 saiu vazio")

    def test_a_genuinely_different_rule_is_not_absorbed(self):
        """Agrupar por padrao nao pode engolir uma regra que diz outra coisa."""
        with tempfile.TemporaryDirectory() as tmp:
            _p, doc, _s = extrai(tmp, livro_com_cf_repetida(Path(tmp) / "l.xlsx"))
        cf = folha(doc)["conditional_formatting"]
        padroes = [r.get("pattern") for r in cf]
        self.assertTrue(any(">=30" in (p or "") for p in padroes),
                        "a regra de limiar desapareceu no agrupamento")

    def test_two_rules_that_differ_only_in_colour_stay_two(self):
        """A cor entra na chave. A mesma condicao pintada de amarelo e de vermelho diz
        duas coisas; fundi-las apagava metade do significado visual da folha."""
        with tempfile.TemporaryDirectory() as tmp:
            _p, doc, _s = extrai(tmp, livro_com_cf_repetida(Path(tmp) / "l.xlsx"))
        limiar = [r for r in folha(doc)["conditional_formatting"]
                  if ">=30" in (r.get("pattern") or "")]
        self.assertEqual(len(limiar), 2,
                         "as duas cores da mesma condicao foram fundidas numa")
        self.assertEqual(len({r.get("fill_rgb") for r in limiar}), 2)

    def test_an_a1_formula_survives_per_pattern(self):
        """`_cf_thresholds` le limiares das formulas em A1: uma por padrao tem de ficar."""
        with tempfile.TemporaryDirectory() as tmp:
            _p, doc, _s = extrai(tmp, livro_com_cf_repetida(Path(tmp) / "l.xlsx"))
        for r in folha(doc)["conditional_formatting"]:
            self.assertTrue(r.get("formulas"), "padrao sem formula representante")

    def test_the_ranges_are_kept(self):
        """O intervalo diz ONDE a regra se aplica — sem ele o padrao nao tem locator."""
        with tempfile.TemporaryDirectory() as tmp:
            _p, doc, _s = extrai(tmp, livro_com_cf_repetida(Path(tmp) / "l.xlsx"))
        cf = folha(doc)["conditional_formatting"]
        grande = max(cf, key=lambda r: r.get("instances", 1))
        self.assertTrue(grande.get("ranges"), "os intervalos do padrao desapareceram")

    def test_the_file_gets_much_smaller(self):
        with tempfile.TemporaryDirectory() as tmp:
            _p, doc, saida = extrai(tmp, livro_com_cf_repetida(Path(tmp) / "l.xlsx", 300))
            peso = len(json.dumps(folha(doc)["conditional_formatting"], ensure_ascii=False))
        self.assertLess(peso, 6000,
                        "a formatacao condicional ainda pesa {} B".format(peso))


@unittest.skipUnless(HAVE, "openpyxl ausente")
class C2_OQueDependeDisto(unittest.TestCase):
    """Dois consumidores internos leem estas regras. Nenhum pode partir."""

    def test_the_fill_colours_are_still_reachable(self):
        with tempfile.TemporaryDirectory() as tmp:
            _p, doc, _s = extrai(tmp, livro_com_cf_repetida(Path(tmp) / "l.xlsx"))
        cores = {r.get("fill_rgb") for r in folha(doc)["conditional_formatting"]}
        self.assertTrue([c for c in cores if c], "`extract_fills` ficou sem cores de CF")

    def test_the_thresholds_are_still_readable(self):
        """`_cf_thresholds` procura `$COL<n>>=N` nas formulas. Tem de continuar a achar."""
        import re
        with tempfile.TemporaryDirectory() as tmp:
            _p, doc, _s = extrai(tmp, livro_com_cf_repetida(Path(tmp) / "l.xlsx"))
        achou = False
        for r in folha(doc)["conditional_formatting"]:
            for f in r.get("formulas", []):
                if re.search(r"\$?([A-Z]{1,3})\$?\d+\s*[<>]=?\s*(\d+)\b", str(f)):
                    achou = True
        self.assertTrue(achou, "o limiar deixou de ser legivel nas formulas guardadas")

    def test_a_read_failure_is_still_reported(self):
        """O registo de erro nao e uma regra e nao pode ser agrupado nem perdido."""
        agrupado = X["group_cf_rules"]([{"error": "conditional formatting read failed: x"}])
        self.assertEqual(len(agrupado), 1)
        self.assertIn("error", agrupado[0])

    def test_grouping_nothing_returns_nothing(self):
        self.assertEqual(X["group_cf_rules"]([]), [])


@unittest.skipUnless(HAVE, "openpyxl ausente")
class C3_ContraOPilotoReal(unittest.TestCase):

    def test_the_real_workbook_stops_being_a_six_megabyte_file(self):
        livro = ROOT / "projects" / "pricing-bunkers-pilot-4" / "inputs" / \
            "PREÇO BANCAS_03_08_26.xlsx"
        if not livro.exists():
            self.skipTest("piloto ausente neste ambiente")
        with tempfile.TemporaryDirectory() as tmp:
            # medir DENTRO do `with`: fora dele a pasta ja nao existe e o caso falha
            # por um motivo que nao tem nada a ver com o que afirma
            _p, doc, saida = extrai(tmp, livro)
            peso = os.path.getsize(saida) / 1024
        cf = sum(len(s.get("conditional_formatting") or []) for s in doc["sheets"])
        self.assertLess(peso, 3000, "o ficheiro ainda tem {:.0f} KB".format(peso))
        self.assertLess(cf, 100, "ainda ha {} regras de formatacao condicional".format(cf))


if __name__ == "__main__":
    unittest.main(verbosity=1)
