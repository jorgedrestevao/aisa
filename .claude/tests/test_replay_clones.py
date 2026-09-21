"""Captura de cálculo — Fase 3 (P6): folhas-clone deduplicadas antes do replay, divergência entre clones é `high`.

Escrito **vermelho** na Fase 1. O que fixa: no engagement real, 14 achados distintos × 6
folhas estruturalmente idênticas deram 101 findings `medium` — e a única coisa valiosa nessa
massa, as células que **divergem** entre clones (`CN23` 42/37/39, `AK31` 5/8, `W27` com e sem
`-10`), saía diluída ou não saía. A fixture tem dois clones (`Outputs`, `Simulador`) com duas
divergências plantadas: `W27` (sem `-10` no Simulador) e `CN23`/`CO23` (42/45 vs 37/40).

    python .claude/tests/test_replay_clones.py
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


def _replay():
    tmp = Path(tempfile.mkdtemp(prefix="calc-clones-"))
    out = tmp / "x.extraction.json"
    assert X["extract"](str(FIXTURE), str(out), True, None) == 0
    extraction = json.loads(out.read_text(encoding="utf-8"))
    rep = X["Replayer"](load_workbook(str(FIXTURE), data_only=True), extraction)
    rep._fwb = load_workbook(str(FIXTURE), data_only=False)
    rep.run()
    return rep


@unittest.skipUnless(HAVE_OPENPYXL, "openpyxl not installed")
class TestCloneGroups(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rep = _replay()

    def test_replayer_groups_clones(self):
        self.assertTrue(hasattr(self.rep, "_clone_groups"), "Fase 3: `Replayer._clone_groups()` por assinatura estrutural")
        groups = self.rep._clone_groups()
        self.assertIn("Outputs", groups, groups)
        self.assertIn("Simulador", groups["Outputs"])

    def test_clone_divergence_is_a_high_finding(self):
        div = [f for f in self.rep.findings if f.check == "clone divergence"]
        self.assertTrue(div, "nenhum finding `clone divergence` — a check não existe ou não disparou")
        self.assertTrue(all(f.severity == "high" for f in div), [f.severity for f in div])
        locs = " | ".join(f.location for f in div)
        self.assertIn("CN23", locs, locs)
        self.assertIn("W27", locs, locs)

    def test_divergence_names_both_values(self):
        cn = next(f for f in self.rep.findings if f.check == "clone divergence" and "CN23" in f.location)
        text = f"{cn.expected} {cn.found}"
        self.assertIn("42", text)
        self.assertIn("37", text)

    def test_pattern_exceptions_are_policed_once_per_group(self):
        pe = [f for f in self.rep.findings if f.check == "pattern exceptions"]
        on_clone = [f.location for f in pe if f.location.startswith("Simulador!") or f.location.startswith("Simulador ")]
        self.assertEqual(on_clone, [], f"o clone não é policiado à parte: {on_clone}")
        tagged = [f.location for f in pe if f.location.startswith("Outputs") and "clone" in f.location]
        self.assertTrue(tagged, "o representante diz quantos clones replica (`(+1 clone: Simulador)`)")


if __name__ == "__main__":
    unittest.main(verbosity=1)
