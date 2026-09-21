"""Captura de cálculo — Fase 3 (P3b): a fronteira de capacidade é declarada por presença, e toda a
folha terminal de um `CALC` cai numa de cinco classes.

Fixture `fx-calc-boundary`: um feed de add-in (`_xll.`), um link a livro externo ausente, um
`INDIRECT` sem literal, células fundidas — e uma saída rotulada cujos ramos morrem nesses pontos.
Power Query não está na fixture (o openpyxl não escreve `DataMashup`, D-8): o motor tem de dizer
`presente: não` e o teste PQ fica **inconclusivo** (skip com razão), nunca verde.

    python .claude/tests/test_capability_boundary.py
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
FIXTURE = ROOT / ".claude" / "tests" / "fixtures" / "calc-capture" / "fx-calc-boundary" / "inputs" / "fronteira.xlsx"
PQ_FIXTURE = ROOT / ".claude" / "tests" / "fixtures" / "calc-capture" / "fx-arch-pq" / "inputs" / "power-query.xlsx"

try:
    from openpyxl import load_workbook
    HAVE_OPENPYXL = True
except Exception:  # pragma: no cover
    HAVE_OPENPYXL = False


def _run(path: Path):
    tmp = Path(tempfile.mkdtemp(prefix="calc-boundary-"))
    out = tmp / "x.extraction.json"
    assert X["extract"](str(path), str(out), True, None) == 0
    extraction = json.loads(out.read_text(encoding="utf-8"))
    wb = load_workbook(str(path), data_only=False)
    boundary = X["capability_boundary"](str(path), wb, extraction)
    chain = X["CalcChain"](wb, extraction, boundary=boundary).run()
    return extraction, boundary, chain


@unittest.skipUnless(HAVE_OPENPYXL, "openpyxl not installed")
class TestBoundaryDeclaredByPresence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not FIXTURE.exists():
            raise unittest.SkipTest(f"fixture em falta: {FIXTURE} — correr docs/calc-capture/make_boundary_fixture.py")
        cls.extraction, cls.boundary, cls.chain = _run(FIXTURE)

    def test_extraction_persists_the_boundary_as_an_additive_key(self):
        self.assertIn("capability_boundary", self.extraction)
        for k in ("power_query", "data_model", "vba", "addin_functions", "external_links", "rtd",
                  "dynamic_names", "iterative", "merged_scan_fail", "pivot_caches", "modern_functions"):
            self.assertIn(k, self.extraction["capability_boundary"])
            self.assertIn("present", self.extraction["capability_boundary"][k])

    def test_present_mechanisms_are_the_planted_ones(self):
        b = self.boundary
        self.assertTrue(b["addin_functions"]["present"], b["addin_functions"])
        self.assertIn("_xll.Feed", b["addin_functions"]["detail"])
        self.assertTrue(b["external_links"]["present"], b["external_links"])
        self.assertTrue(b["dynamic_names"]["present"], b["dynamic_names"])
        self.assertEqual(b["dynamic_names"]["locator"], "Calc!B5")

    def test_absent_mechanisms_are_absent_not_inferred(self):
        b = self.boundary
        for k in ("power_query", "data_model", "vba", "iterative", "pivot_caches", "rtd", "modern_functions"):
            self.assertFalse(b[k]["present"], f"{k}: {b[k]}")

    def test_every_valid_block_ends_in_the_five_classes(self):
        self.assertTrue(self.chain["blocks"], "a saída rotulada `PREÇO DE SAÍDA` tem de virar bloco")
        for blk in self.chain["blocks"]:
            for k in blk["terminals"]:
                self.assertIn(k, X["TERMINAL_CLASSES"] + ("invalid",))
            if blk["valid"]:
                self.assertNotIn("invalid", blk["terminals"])

    def test_output_block_reaches_feed_boundary_and_to_read(self):
        # B7 é consumido por Layout!B3 (rótulo «Produto A»), logo é absorvido como passo desse bloco —
        # o que interessa é o bloco que o contém, não a âncora
        out = next(b for b in self.chain["blocks"] if any(s["sheet"] == "Calc" and s["cell"] == "B7" for s in b["steps"]))
        t = out["terminals"]
        self.assertGreaterEqual(t.get("feed", 0), 1, t)
        self.assertGreaterEqual(t.get("boundary", 0), 1, t)
        self.assertGreaterEqual(t.get("to_read", 0), 1, t)
        self.assertTrue(out["valid"], out["invalid_reasons"])
        self.assertIn(("B7", 8.0), {(c["cell"], c["value"]) for c in out["unlabelled_constants"]})
        dyn = next(e for e in self.chain["to_read"] if e["prefix"] == "<dynamic>")
        self.assertIn("Calc!B5", dyn["cells"])

    def test_section_4bis_declares_the_boundary_first(self):
        md = X["render_calc_chain_md"](self.chain)
        self.assertLess(md.index("Fronteira de capacidade"), md.index("| output |"))
        self.assertIn("`addin_functions` | **sim**", md)
        self.assertIn("`power_query` | não", md)


class TestPowerQueryArchetype(unittest.TestCase):
    def test_power_query_fixture_or_inconclusive(self):
        if not PQ_FIXTURE.exists():
            self.skipTest("INCONCLUSIVO — fx-arch-pq não existe: openpyxl não escreve DataMashup; "
                          "o dono gera a fixture em Excel (plano D-8). Não é verde.")
        _, boundary, chain = _run(PQ_FIXTURE)
        self.assertTrue(boundary["power_query"]["present"])
        dead = [b for b in chain["blocks"] if b["terminals"].get("boundary")]
        self.assertTrue(dead, "um ramo que morre na tabela carregada tem de terminar em fronteira")


if __name__ == "__main__":
    unittest.main(verbosity=1)
