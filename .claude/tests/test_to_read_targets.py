# -*- coding: utf-8 -*-
"""Uma chamada recusada diz onde ESTA. Nao dizia o que ha a LER.

Medido no piloto real de pricing: 10 262 chamadas recusadas pelo replay. O relatorio ja
as colapsava — 10 intervalos de celulas — mas listava a FORMULA, e a formula repete-se.
Quem lia via dez mil e nao sabia por onde comecar.

As 10 262 sao tres alvos:

    INDEX('Market View'!$1:$1048576, MATCH(...), MATCH(...))   7 286   folha, no ficheiro
    INDIRECT("Galp_Marinha_v2["&...&"]")                       2 698   tabela A1:J525
    INDIRECT("CustosLogisticos_"&canal&"_"&porto)                110   82 nomes -> Inputs

Nenhum e externo. 289 dos 291 intervalos nomeados apontam para dentro do ficheiro; os dois
que apontam para fora sao do canal Apttus/X-Author e NAO fazem parte destas chamadas.

Este ficheiro fixa a distincao que faltava: a celula recusada e onde o problema esta; o
alvo e o que resolve o padrao inteiro. Ler UM `CustosLogisticos_*` resolve os 82.

O que isto NAO faz: computar. A recusa mantem-se, o `no check = no claim` mantem-se, e um
alvo nomeado nunca vira uma verificacao limpa."""
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

WB = {
    "named_ranges": [
        {"name": "CustosLogisticos_FUEL_Sines", "target": "Inputs!$AV$9:$AV$1469"},
        {"name": "CustosLogisticos_FUEL_Aveiro", "target": "Inputs!$AP$9:$AP$1469"},
        {"name": "CustosLogisticos_GMC_Gaia", "target": "Inputs!$BA$9:$BA$1469"},
        {"name": "Data_Lista", "target": "Inputs!$B$9:$B$1469"},
        {"name": "XAE_Invalid_PLData", "target": "[1]apttusmetadata!$B$1"},
    ],
    "tables": [{"name": "Galp_Marinha_v2", "sheet": "UlyssesQuotes", "ref": "A1:J525"}],
}
FOLHAS = ("Inputs", "Market View", "UlyssesQuotes", "Motor")


def alvos(formula):
    return X["read_targets"](formula, WB, FOLHAS)


class A1_OAlvoDeCadaForma(unittest.TestCase):

    def test_an_indirect_prefix_names_the_family(self):
        a = alvos('INDIRECT("CustosLogisticos_"&$A5&"_"&$B5)')
        fam = [t for t in a if t["kind"] == "named-family"]
        self.assertTrue(fam, "o prefixo do INDIRECT nao virou familia de nomes")
        self.assertEqual(fam[0]["count"], 3, "contou mal os nomes com este prefixo")
        self.assertIn("Inputs!", fam[0]["where"], "a familia nao diz para onde aponta")

    def test_a_structured_table_reference_names_the_table(self):
        a = alvos('IF(INDEX(INDIRECT("Galp_Marinha_v2["&$C5&"]"),MATCH($B5,Galp_Marinha_v2[quotation_dt],0)),1,0)')
        tab = [t for t in a if t["kind"] == "table"]
        self.assertTrue(tab, "a tabela nao foi identificada")
        self.assertEqual(tab[0]["name"], "Galp_Marinha_v2")
        self.assertIn("A1:J525", tab[0]["where"], "a tabela saiu sem o seu intervalo")

    def test_a_sheet_reference_names_the_sheet(self):
        a = alvos("INDEX('Market View'!$1:$1048576,MATCH($A5,'Market View'!$A:$A,0),MATCH($B4,'Market View'!$1:$1,0))")
        fol = [t for t in a if t["kind"] == "sheet"]
        self.assertTrue(fol, "a folha referida nao foi identificada")
        self.assertEqual(fol[0]["name"], "Market View")

    def test_a_structured_reference_without_indirect_still_names_the_table(self):
        """A regra 2 sozinha. O caso anterior levava a tabela DENTRO de um `INDIRECT`, e
        a regra 1 apanhava-a primeiro — apagar a regra 2 nao mudava nada e o mutante
        sobrevivia. Aqui nao ha `INDIRECT` nenhum."""
        a = alvos("SUMIFS(Galp_Marinha_v2[valor],Galp_Marinha_v2[quotation_dt],$B5)")
        tab = [t for t in a if t["kind"] == "table"]
        self.assertTrue(tab, "uma referencia estruturada sem INDIRECT nao deu a tabela")
        self.assertEqual(tab[0]["name"], "Galp_Marinha_v2")

    def test_a_sheet_named_inside_a_string_is_not_a_target(self):
        """Texto dentro de aspas e conteudo, nao referencia.

        A primeira versao deste caso usava `Market View!A1` — nome com espaco, que a
        regex de referencia nunca casaria com ou sem aspas. O mutante que removia a
        limpeza das strings sobrevivia a ele. Usa-se um nome de folha que ELA casa."""
        a = alvos('IF($A5="ver Inputs!A1 para a fonte","sem fonte","ok")')
        self.assertEqual([t for t in a if t["kind"] == "sheet"], [],
                         "leu uma folha a partir de texto entre aspas")

    def test_an_exact_named_range_resolves_to_its_target(self):
        a = alvos("MATCH(Data_Output,Data_Lista,0)")
        nom = [t for t in a if t["kind"] == "named" and t["name"] == "Data_Lista"]
        self.assertTrue(nom, "o intervalo nomeado nao foi resolvido")
        self.assertEqual(nom[0]["where"], "Inputs!$B$9:$B$1469")

    def test_a_target_outside_the_file_is_said_to_be_outside(self):
        """`[1]apttusmetadata!` e outro ficheiro. Ler o Excel nao resolve isso, e o
        relatorio nao pode sugerir que sim."""
        a = alvos("IF(XAE_Invalid_PLData=1,0,1)")
        nom = [t for t in a if t["name"] == "XAE_Invalid_PLData"]
        self.assertTrue(nom)
        self.assertTrue(nom[0].get("external"),
                        "um alvo noutro ficheiro aparece como se fosse leitura local")


class A2_OQueNaoPodeAcontecer(unittest.TestCase):

    def test_an_unknown_name_is_not_invented(self):
        a = alvos('INDIRECT("NaoExisteNada_"&$A5)')
        self.assertEqual([t for t in a if t["kind"] in ("named", "named-family")], [],
                         "inventou um alvo para um prefixo que nao casa com nada")

    def test_a_formula_with_no_target_returns_nothing(self):
        self.assertEqual(alvos("=A1+B1*2"), [])

    def test_targets_are_deduplicated(self):
        a = alvos("INDEX('Market View'!$A:$A,MATCH($A5,'Market View'!$B:$B,0))")
        folhas = [t for t in a if t["kind"] == "sheet"]
        self.assertEqual(len(folhas), 1, "a mesma folha aparece duas vezes")

    def test_the_order_is_deterministic(self):
        f = 'INDEX(INDIRECT("CustosLogisticos_"&$A5&"_"&$B5),MATCH(Data_Lista,\'Market View\'!$A:$A,0))'
        self.assertEqual(alvos(f), alvos(f))


@unittest.skipUnless(HAVE, "openpyxl ausente")
class A3_AsTabelasEntramNaExtraccao(unittest.TestCase):

    def test_the_extraction_carries_the_tables(self):
        from openpyxl import Workbook
        from openpyxl.worksheet.table import Table
        with tempfile.TemporaryDirectory() as tmp:
            livro = Path(tmp) / "l.xlsx"
            wb = Workbook(); ws = wb.active; ws.title = "Dados"
            ws.append(["id", "valor"]); ws.append([1, 10]); ws.append([2, 20])
            ws.add_table(Table(displayName="Cotacoes", ref="A1:B3"))
            wb.save(str(livro))
            saida = os.path.join(tmp, "o.json")
            subprocess.run([sys.executable, str(XLSX_PY), str(livro), saida, "--force"],
                           capture_output=True, text=True, timeout=300)
            doc = json.loads(Path(saida).read_text(encoding="utf-8"))
        tabelas = doc["workbook"].get("tables")
        self.assertTrue(tabelas, "a extraccao nao regista tabelas nenhumas")
        self.assertEqual(tabelas[0]["name"], "Cotacoes")
        self.assertEqual(tabelas[0]["ref"], "A1:B3")
        self.assertEqual(tabelas[0]["sheet"], "Dados")


@unittest.skipUnless(HAVE, "openpyxl ausente")
class A4_ContraOPilotoReal(unittest.TestCase):

    def test_the_replay_report_names_what_to_read(self):
        livro = ROOT / "projects" / "pricing-bunkers-pilot-4" / "inputs" / \
            "PREÇO BANCAS_03_08_26.xlsx"
        if not livro.exists():
            self.skipTest("piloto ausente neste ambiente")
        with tempfile.TemporaryDirectory() as tmp:
            ext = os.path.join(tmp, "e.json")
            rep = os.path.join(tmp, "r.replay.md")
            subprocess.run([sys.executable, str(XLSX_PY), str(livro), ext, "--force"],
                           capture_output=True, text=True, timeout=900)
            subprocess.run([sys.executable, str(XLSX_PY), "--replay", str(livro), ext, rep],
                           capture_output=True, text=True, timeout=900)
            corpo = Path(rep).read_text(encoding="utf-8")
        self.assertIn("**What to read**", corpo,
                      "o relatorio perdeu o bloco que diz por onde comecar")
        self.assertIn("| target | kind | where | calls |", corpo,
                      "o bloco existe mas nao lista os alvos")
        self.assertIn("Galp_Marinha_v2", corpo, "a tabela nao aparece no relatorio")
        self.assertIn("A1:J525", corpo, "a tabela aparece sem o intervalo a ler")
        self.assertIn("Market View", corpo)
        self.assertIn("CustosLog", corpo, "a familia de intervalos nomeados nao aparece")


if __name__ == "__main__":
    unittest.main(verbosity=1)
