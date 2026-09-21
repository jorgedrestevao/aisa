"""Captura de cálculo — Fase 2 (P3, P9): a cadeia de cálculo do output principal sai do motor.

Escrito **vermelho** na Fase 1 (`docs/CALC_CAPTURE_IMPLEMENTATION_PLAN.md` §5-§6). Fica verde
quando `xlsx_extract.py` expuser `CalcChain` e `render_calc_chain_md` com o contrato mínimo
abaixo. O contrato é deliberadamente pequeno para a Fase 2 ter liberdade de forma; o que
ele fixa é o que o engagement `pricing-bunkers-v2` não conseguiu produzir:

  - blocos de saída (`CALC-NNN`) com passos citados por célula;
  - a regra de selecção entre janelas (`MIN` na tabela de carga, `MAX` na folha de rosto);
  - a agregação semanal com `AVERAGEIF(...,"<>0")`;
  - a cedência como soma de média + encargos (`L19 = D24 + D27`);
  - factores de conversão (densidades) e constantes sem rótulo (`+10`, `-10`, `+8`);
  - `INDIRECT` dinâmico como alvo de leitura (`TO-READ`), não como buraco.

    python .claude/tests/test_calc_chain.py
"""
from __future__ import annotations

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


def _chain():
    """Extrai a fixture e devolve (extraction, chain_dict)."""
    tmp = Path(tempfile.mkdtemp(prefix="calc-chain-"))
    out = tmp / "x.extraction.json"
    rc = X["extract"](str(FIXTURE), str(out), True, None)
    assert rc == 0, f"extract rc={rc}"
    import json
    extraction = json.loads(out.read_text(encoding="utf-8"))
    wb_formula = load_workbook(str(FIXTURE), data_only=False)
    chain = X["CalcChain"](wb_formula, extraction).run()
    return extraction, chain


def _steps(chain):
    for block in chain["blocks"]:
        for step in block["steps"]:
            yield block, step


def _step(chain, sheet, cell):
    for block, step in _steps(chain):
        if step["sheet"] == sheet and step["cell"] == cell:
            return block, step
    return None, None


@unittest.skipUnless(HAVE_OPENPYXL, "openpyxl not installed")
class TestMotorExposesCalcChain(unittest.TestCase):
    def test_fixture_exists(self):
        self.assertTrue(FIXTURE.exists(), f"fixture em falta: {FIXTURE} — correr docs/calc-capture/make_fixture.py")

    def test_calc_chain_class_exists(self):
        self.assertIn("CalcChain", X, "Fase 2: `CalcChain(wb_formula, extraction).run()` em xlsx_extract.py")

    def test_renderer_exists(self):
        self.assertIn("render_calc_chain_md", X, "Fase 2: `render_calc_chain_md(chain) -> str` (§4bis)")


@unittest.skipUnless(HAVE_OPENPYXL, "openpyxl not installed")
class TestChainContent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if "CalcChain" not in X:
            raise unittest.SkipTest("CalcChain ainda não existe — ver TestMotorExposesCalcChain")
        cls.extraction, cls.chain = _chain()

    def test_blocks_have_stable_ids_and_anchors(self):
        blocks = self.chain["blocks"]
        self.assertGreaterEqual(len(blocks), 4, "≥ 4 blocos de saída: folha de rosto, tabela de carga, BIOS, custos por porto")
        ids = [b["id"] for b in blocks]
        self.assertEqual(len(ids), len(set(ids)))
        for b in blocks:
            self.assertRegex(b["id"], r"^CALC-\d{3}$")
            self.assertIn("sheet", b)
            self.assertIn("anchor", b)
            self.assertNotEqual(b.get("label", ""), "", f"{b['id']} sem rótulo")

    def test_min_on_loading_table_and_max_on_front_sheet_are_two_rules(self):
        _, d38 = _step(self.chain, "Outputs", "D38")
        self.assertIsNotNone(d38, "Outputs!D38 (MIN entre janelas) tem de estar num bloco")
        self.assertEqual(d38["kind"], "selection")
        self.assertIn("MIN", d38["formula"])
        _, w14 = _step(self.chain, "Outputs", "W14")
        self.assertIsNotNone(w14, "Outputs!W14 (MAX entre janelas) tem de estar num bloco")
        self.assertEqual(w14["kind"], "selection")
        self.assertIn("MAX", w14["formula"])

    def test_weekly_windows_are_aggregations_that_skip_zeros(self):
        _, d24 = _step(self.chain, "Outputs", "D24")
        self.assertIsNotNone(d24)
        self.assertEqual(d24["kind"], "aggregation")
        self.assertIn('"<>0"', d24["formula"])
        _, d29 = _step(self.chain, "Outputs", "D29")
        self.assertIsNotNone(d29, "a janela N-1 é um passo distinto da janela N")

    def test_cedencia_is_average_plus_charges(self):
        _, l19 = _step(self.chain, "Outputs", "L19")
        self.assertIsNotNone(l19, "Outputs!L19 (cedência USD) tem de estar na cadeia")
        refs = set(l19["refs"])
        self.assertIn("Outputs!D24", refs)
        self.assertIn("Outputs!D27", refs)

    def test_densities_are_conversions_and_offsets_are_unlabelled_constants(self):
        block, _ = _step(self.chain, "Outputs", "W14")
        conv = [round(c["value"], 3) for c in block["conversions"]]
        self.assertIn(0.953, conv, "a densidade em W14 é um factor de conversão")
        consts = {(c["cell"], c["value"]) for c in block["unlabelled_constants"]}
        self.assertIn(("W14", 10), consts, "o +10 de W14 não tem rótulo — vai para *por confirmar*")
        block27, _ = _step(self.chain, "Outputs", "W27")
        consts27 = {(c["cell"], c["value"]) for c in block27["unlabelled_constants"]}
        self.assertIn(("W27", -10), consts27)
        bios, _ = _step(self.chain, "Outputs BIOS", "D6")
        self.assertIsNotNone(bios)
        self.assertIn(("D6", 8), {(c["cell"], c["value"]) for c in bios["unlabelled_constants"]})

    def test_dynamic_indirect_becomes_a_read_target_not_a_hole(self):
        to_read = self.chain["to_read"]
        prefixes = [t["prefix"] for t in to_read]
        self.assertTrue(any(p.startswith("CustosLogísticos_") for p in prefixes), prefixes)
        hit = next(t for t in to_read if t["prefix"].startswith("CustosLogísticos_"))
        self.assertGreaterEqual(len(hit["cells"]), 2)
        self.assertLessEqual(len(to_read), 20, "ranges a ler, não chamadas: o número tem de ser finito")

    def test_dead_index_column_is_reported_as_feeding_zero(self):
        _, c25 = _step(self.chain, "Outputs", "C25")
        self.assertIsNotNone(c25, "o indexante morto é consumido em C25 e tem de aparecer")
        self.assertTrue(c25.get("source_empty"), "Inputs!C está vazia — o passo declara-o")

    def test_section_4bis_renders_with_locators_and_por_confirmar(self):
        md = X["render_calc_chain_md"](self.chain)
        self.assertIn("## 4bis", md)
        self.assertIn("por confirmar", md)
        self.assertIn("Outputs!D38", md)
        self.assertIn("Outputs!W14", md)
        self.assertIn("CALC-001", md)


if __name__ == "__main__":
    unittest.main(verbosity=1)
