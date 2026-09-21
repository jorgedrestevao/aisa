"""Frente E (P-17) — the replay is honest about what it cannot replay.

Inverts the EXCEL_SEMANTICS scenarios of the 2026-09-08 adversarial review (F03):

  `XLOOKUP("key",A2:A3,B2:B3,"",0,-1)` searches last-to-first. With duplicate keys the
  replay matched first-to-last, recomputed the OTHER row and called a correct cached
  value stale. `COUNTIF(A2:A3,"key*")` matches two rows in Excel; the replay compared
  the wildcard literally and recorded "no match". Both fed invented anomalies into the
  evidence surface.

The fix is the one the review asked for and the plan chose: declare the limit. None of
the three pilots carries a formula that needs the semantics implemented (checked
2026-09-08: zero `XLOOKUP` with 5+ arguments, zero wildcard criteria), so implementing
it would be untested machinery. What must never happen is a partial implementation
reporting a finding.

    python .claude/tests/test_replay_scope.py
"""

import runpy
import sys
import unittest
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.dont_write_bytecode = True
X = runpy.run_path(str(ROOT / "library" / "kernel" / "tools" / "xlsx_extract.py"))
TE = runpy.run_path(str(ROOT / "library" / "kernel" / "tools" / "text_extract.py"))

try:
    from openpyxl import Workbook
    HAVE_OPENPYXL = True
except ImportError:  # pragma: no cover - environment without the capture dependency
    HAVE_OPENPYXL = False


def workbook_with_duplicate_keys():
    wb = Workbook()
    sheet = wb.active
    sheet.title = "Data"
    sheet.append(["Key", "Value"])
    sheet.append(["key", "old"])
    sheet.append(["key", "new"])
    return wb


def replay_one(formula, stored):
    """Replay a single cell; returns (replayer, misses, stales)."""
    rep = X["Replayer"](workbook_with_duplicate_keys(), {"sheets": []})
    misses, stales = defaultdict(list), defaultdict(list)
    rep._replay_cell("Data", "D2", formula, stored, False, misses, stales)
    return rep, misses, stales


def declined_reasons(rep):
    return [k.split(":")[0] for k in rep.not_replayable]


@unittest.skipUnless(HAVE_OPENPYXL, "openpyxl required (requirements-dev.txt)")
class DeclinedBeforeAnyFinding(unittest.TestCase):

    def test_reverse_search_mode_is_declined(self):
        rep, misses, stales = replay_one(
            '=XLOOKUP("key",A2:A3,B2:B3,"",0,-1)', "new")
        self.assertIn("unsupported XLOOKUP search_mode", declined_reasons(rep))
        self.assertFalse(stales, "a correct cached value must not be called stale")
        self.assertFalse(misses)
        self.assertFalse(rep.findings)

    def test_binary_search_modes_are_declined(self):
        for mode in ("2", "-2"):
            rep, _, stales = replay_one(
                '=XLOOKUP("key",A2:A3,B2:B3,"",0,{})'.format(mode), "new")
            self.assertIn("unsupported XLOOKUP search_mode", declined_reasons(rep), mode)
            self.assertFalse(stales, mode)

    def test_first_to_last_is_still_replayed(self):
        """The fix must not turn the supported case into a declined one."""
        for call in ('=XLOOKUP("key",A2:A3,B2:B3,"",0,1)',
                     '=XLOOKUP("key",A2:A3,B2:B3,"",0)',
                     '=XLOOKUP("key",A2:A3,B2:B3)'):
            rep, _, stales = replay_one(call, "wrong")
            self.assertFalse(declined_reasons(rep), call)
            self.assertTrue(stales, "a genuinely stale value is still reported: " + call)

    def test_wildcard_countif_is_declined(self):
        rep, misses, _ = replay_one('=COUNTIF(A2:A3,"key*")', 2)
        self.assertIn("wildcard COUNTIF criterion", declined_reasons(rep))
        self.assertFalse(misses)
        self.assertFalse(rep.findings)

    def test_literal_countif_is_still_replayed(self):
        rep, misses, _ = replay_one('=COUNTIF(A2:A3,"absent")', 0)
        self.assertFalse(declined_reasons(rep))
        self.assertTrue(misses, "a real miss is still reported")

    def test_wildcard_lookup_values_are_declined(self):
        for call, reason in (
                ('=XLOOKUP("key*",A2:A3,B2:B3)', "wildcard XLOOKUP lookup value"),
                ('=VLOOKUP("key?",A2:B3,2,FALSE)', "wildcard VLOOKUP lookup value"),
                ('=INDEX(B2:B3,MATCH("ke~y",A2:A3,0))', "wildcard MATCH lookup value")):
            rep, misses, stales = replay_one(call, "x")
            self.assertIn(reason, declined_reasons(rep), call)
            self.assertFalse(rep.findings, call)
            self.assertFalse(misses, call)
            self.assertFalse(stales, call)

    def test_has_wildcards_is_narrow(self):
        for value in ("key*", "a?b", "ke~y"):
            self.assertTrue(X["has_wildcards"](value), value)
        for value in ("key", "", "a-b_c", 12, None, "2026-09-08"):
            self.assertFalse(X["has_wildcards"](value), value)


class DeclinedCountIsVisible(unittest.TestCase):
    """A reader comparing '0 findings' across runs must see what was out of scope."""

    def test_replay_md_states_the_out_of_scope_count(self):
        rep = X["Replayer"](Workbook() if HAVE_OPENPYXL else None, {"sheets": []})
        rep.not_replayable["wildcard COUNTIF criterion: COUNTIF(<ref>,\"k*\")"] = 3
        rep.nr_example["wildcard COUNTIF criterion: COUNTIF(<ref>,\"k*\")"] = "Data!D2"
        out = Path(__file__).with_name("_tmp_replay.md")
        try:
            X["render_replay_md"]({"identity": {"filename": "x.xlsx", "sha256": "0" * 64}},
                                  rep, str(out))
            text = out.read_text(encoding="utf-8")
        finally:
            if out.exists():
                out.unlink()
        self.assertIn("Out of scope: 3 formula call(s) declined as not replayable", text)
        self.assertIn("search_mode", text, "the declared limits belong in the notes")

    def test_evidence_index_reads_that_line(self):
        out = Path(__file__).with_name("_tmp_index_replay.md")
        out.write_text("**Out of scope: 2045 formula call(s) declined as not replayable**\n",
                       encoding="utf-8")
        try:
            self.assertEqual(TE["_declined_calls"](str(out)), 2045)
        finally:
            out.unlink()

    def test_missing_replay_report_contributes_nothing(self):
        self.assertEqual(TE["_declined_calls"]("does-not-exist.md"), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
