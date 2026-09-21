"""Captura de cálculo — Fase 3 (P3d): orçamento de travessia declarado, nenhum candidato sem destino.

O fecho da Fase 2 cortou 136 candidatos num contador do JSON. Este teste fixa o contrário:
`rendered + grouped + absorbed + to_read == candidates`, com qualquer orçamento; blocos com o mesmo
padrão normalizado (nome colapsado, linha absoluta colapsada) saem agrupados com os membros
enumerados; um run rotulado, uma família de nomes, um grupo de clones e um par de janelas de
agregação são **dimensões declaradas** com membros e locators (P3d-3).

    python .claude/tests/test_calc_budget.py
"""
from __future__ import annotations

import json
import runpy
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.dont_write_bytecode = True
X = runpy.run_path(str(ROOT / "library" / "kernel" / "tools" / "xlsx_extract.py"))
FIXTURE = ROOT / ".claude" / "tests" / "fixtures" / "calc-capture" / "fx-calc-bancas" / "inputs" / "precos-bancas-reduzido.xlsx"

try:
    from openpyxl import load_workbook
    HAVE_OPENPYXL = True
except Exception:  # pragma: no cover
    HAVE_OPENPYXL = False


def _chain(budget=None):
    tmp = Path(tempfile.mkdtemp(prefix="calc-budget-"))
    out = tmp / "x.extraction.json"
    assert X["extract"](str(FIXTURE), str(out), True, None) == 0
    extraction = json.loads(out.read_text(encoding="utf-8"))
    wb = load_workbook(str(FIXTURE), data_only=False)
    return X["CalcChain"](wb, extraction, budget=budget).run()


@unittest.skipUnless(HAVE_OPENPYXL, "openpyxl not installed")
class TestBudgetInvariant(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.full = _chain()
        cls.tight = _chain({"max_blocks": 2})

    def _sum_ok(self, chain):
        t = chain["totals"]
        self.assertEqual(t["rendered"] + t["grouped"] + t["absorbed"] + t["to_read"], t["candidates"], t)

    def test_sum_holds_with_default_budget(self):
        self._sum_ok(self.full)
        self.assertEqual(self.full["totals"]["to_read"], 0, "com o orçamento por defeito a fixture cabe inteira")
        self.assertEqual(self.full["budget"]["max_blocks"], X["CHAIN_BUDGET"]["max_blocks"])

    def test_sum_holds_when_budget_is_tight_and_nothing_disappears(self):
        self._sum_ok(self.tight)
        self.assertEqual(len(self.tight["blocks"]), 2)
        self.assertGreater(self.tight["totals"]["to_read"], 0, "acima do tecto → TO-READ, nunca silêncio")
        over = next(e for e in self.tight["to_read"] if e["prefix"].startswith("<acima do orçamento"))
        self.assertGreaterEqual(len(over["cells"]), self.tight["totals"]["to_read"])
        self.assertIn("max_blocks=2", over["reason"])

    def test_declared_budget_is_written_to_the_result(self):
        for key in ("max_blocks", "max_depth", "max_nodes"):
            self.assertIn(key, self.full["budget"])
        self.assertIn("totals", self.full)
        self.assertIn("coverage", self.full)


@unittest.skipUnless(HAVE_OPENPYXL, "openpyxl not installed")
class TestGroupingAndDimensions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chain = _chain()

    def test_blocks_carry_terminal_classes_and_validity(self):
        for b in self.chain["blocks"]:
            self.assertIn("valid", b)
            self.assertIn("terminals", b)
            for k in b["terminals"]:
                self.assertIn(k, X["TERMINAL_CLASSES"] + ("invalid",), f"{b['id']}: classe de terminal desconhecida {k!r}")
        self.assertTrue(all(b["valid"] for b in self.chain["blocks"]), [b["invalid_reasons"] for b in self.chain["blocks"] if not b["valid"]])

    def test_labelled_run_becomes_a_declared_dimension(self):
        runs = [d for d in self.chain["dimensions"] if d["basis"].startswith("linhas rotuladas")]
        self.assertTrue(runs, self.chain["dimensions"])
        members = {m for d in runs for m in d["members"]}
        self.assertIn("PORTO NORTE", members)
        self.assertIn("PORTO SUL", members)
        self.assertTrue(all(d["locators"] for d in runs))

    def test_indirect_name_family_becomes_a_declared_dimension(self):
        fam = [d for d in self.chain["dimensions"] if "CustosLogísticos_FUEL" in d["basis"] or "CustosLogísticos_MGO" in d["basis"]]
        self.assertTrue(fam, [d["basis"] for d in self.chain["dimensions"]])
        self.assertEqual(sorted(fam[0]["members"]), ["PortoNorte", "PortoSul"])

    def test_clone_group_and_aggregation_windows_are_dimensions(self):
        bases = [d["basis"] for d in self.chain["dimensions"]]
        self.assertTrue(any(b.startswith("folhas-clone") for b in bases), bases)
        win = [d for d in self.chain["dimensions"] if d["basis"].startswith("janelas de agregação")]
        self.assertTrue(win, bases)
        rngs = {r for d in win for r in d["members"]}
        self.assertTrue(any("19:" in r for r in rngs) and any("14:" in r for r in rngs), rngs)

    def test_section_4bis_opens_with_boundary_coverage_and_lists_dimensions(self):
        md = X["render_calc_chain_md"](self.chain)
        i_b, i_c, i_t = md.index("Fronteira de capacidade"), md.index("Cobertura declarada"), md.index("| output |")
        self.assertLess(i_b, i_c)
        self.assertLess(i_c, i_t)
        self.assertIn("Dimensões da saída", md)
        self.assertIn("PORTO NORTE", md)
        self.assertIn("orçamento", md)


if __name__ == "__main__":
    unittest.main(verbosity=1)
