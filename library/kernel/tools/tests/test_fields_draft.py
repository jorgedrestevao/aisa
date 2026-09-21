#!/usr/bin/env python3
"""test_fields_draft.py — P-6 motor acceptance (frente D, onda 1).

Run:  python library/kernel/tools/tests/test_fields_draft.py

What the motor promises (docs/pp-pack-authoring/pilot/step-9a-onda-0-desenho-a5.md §3, §8):
name by `named_range → formula_ref → header → none`; type vocabulary with `unknown` for
mixed/empty; a validation list makes a `choice`; `required` from nulls; `default` never
inferred; role from the L1 class; items per column with aliases; dictionary entries that
point at columns without data listed apart; `disposition` left to the skill; idempotent
by source sha256; never touches a blueprint.

Synthetic fixtures are built in a temp dir. The two real-engagement classes run only
where the repo carries the engagement (validation copies come and go) — they pin the
acceptance numbers of §8.1 / §8.2 against the motor, never against a hand count.
"""

from __future__ import annotations

import json
import os
import runpy
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
REPO = Path(os.environ.get("AISA_TEST_REPO") or TOOLS.parents[2])
M = runpy.run_path(str(TOOLS / "fields_draft.py"))


def col(letter, header=None, klass="manual", itype="number", nonempty=10, nulls=0,
        distinct=10, key_like=False, formula=None, reads=None):
    c = {"column": letter, "header": header, "inferred_type": itype,
         "rows_nonempty": nonempty, "nulls": nulls, "distinct": distinct,
         "top_values": [], "formula_count": 1 if formula else 0,
         "typed_count": 0 if formula else nonempty, "formula": None,
         "class": klass, "class_basis": "fixture", "key_like": key_like}
    if formula:
        c["formula"] = {"count": nonempty, "dominant_pattern": formula,
                        "patterns": [{"pattern": formula, "count": nonempty}]}
    if reads:
        c["reads"] = reads
    return c


def extraction(sheets, named_ranges=(), sha="ab" * 32, status="ok"):
    return {
        "artefact": "aisa.capture.extraction",
        "tool": {"name": "xlsx_extract.py", "version": "1.2.0"},
        "extracted_at": "2026-09-09T10:00:00",
        "identity": {"filename": "fx.xlsx", "sha256": sha},
        "status": status,
        "workbook": {"named_ranges": list(named_ranges), "flags": {}},
        "sheets": [dict({"state": "visible", "dimensions": "A1:Z9", "header_row": 1,
                         "data_start_row": 2, "data_end_row": 9, "header_basis": "string-density",
                         "validations": [], "anomalies": {}}, **s) for s in sheets],
    }


def draft(ex):
    return M["build_draft"](ex, "fx.xlsx.extraction.json", "fx.xlsx.fields-draft.json",
                            generated_at="2026-09-09T10:00:00")


def columns(d, sheet):
    return {c["column"]: c for s in d["sheets"] if s["name"] == sheet for c in s["columns"]}


REGISTER = {
    "name": "Inputs", "header_row": 1119, "header_basis": "frozen-pane",
    "columns": [
        col("B", header="2026-01-15 00:00:00", itype="datetime", nonempty=350, distinct=350),
        col("F", header="652.75", klass="derived", nonempty=11, nulls=340,
            formula="=IFERROR(INDEX('Market View'!R1:R1048576,MATCH(RC2,'Market View'!C1:C1,0)),\"\")",
            reads=["$B1120", "Market View!A1"]),
        col("G", header="-2.5", nonempty=11, nulls=340, distinct=11),
        col("H", header="9", nonempty=11, nulls=340, distinct=5),
    ],
}
REPORT = {
    "name": "Outputs", "header_row": 6,
    "validations": [{"range": "AF14", "type": "list", "operator": None,
                     "formula1": "\"USD,EUR\"", "formula2": None, "allow_blank": True}],
    "columns": [
        col("C", header="2026-08-04 00:00:00", klass="derived", itype="mixed(number,str)",
            nonempty=33, nulls=41, distinct=20,
            formula="=IF(R6C3>=RC2,INDEX(Index_CIFMEDDMA_Preço,MATCH(RC2,Data_Lista,0)),\"\")"),
        col("L", header=None, klass="derived", nonempty=16, nulls=58, distinct=16,
            formula="=R[-4]C+R[-2]C"),
        col("AF", header=None, klass="manual", itype="str", nonempty=14, nulls=60, distinct=2),
        col("AI", header=None, klass="manual", itype="str", nonempty=15, nulls=59, distinct=15,
            key_like=True),
    ],
}
NAMES = [
    {"name": "Data_Lista", "target": "Inputs!$B$9:$B$1469", "scope": "workbook"},
    {"name": "Data_Lista", "target": "Inputs!$B$9:$B$1469", "scope": "Outputs"},   # repeated
    {"name": "Index_Diesel_Prémio", "target": "Inputs!$G$9:$G$1469", "scope": "workbook"},
    {"name": "GS_Diesel_Prémio", "target": "Inputs!$G$9:$G$1469", "scope": "workbook"},  # alias
    {"name": "CustosLogísticos_MGO_Aveiro", "target": "Inputs!$CX$9:$CX$1469", "scope": "workbook"},
    {"name": "Data_Output", "target": "Outputs!$C$6", "scope": "workbook"},
    {"name": "DF_GRID_1", "target": "#REF!", "scope": "workbook"},
    {"name": "ExternalData_1", "target": "UlyssesQuotes!$A$1:$J$525", "scope": "workbook"},
]


class NameResolution(unittest.TestCase):

    def setUp(self):
        self.d = draft(extraction([REGISTER, REPORT], NAMES))
        self.inp = columns(self.d, "Inputs")
        self.out = columns(self.d, "Outputs")

    def test_a_named_range_beats_a_header_that_is_a_value(self):
        self.assertEqual(self.inp["B"]["name"], "Data_Lista")
        self.assertEqual(self.inp["B"]["name_basis"], "named_range")
        self.assertEqual(self.inp["B"]["header"], "2026-01-15 00:00:00")

    def test_aliases_are_per_column_and_deduplicated(self):
        g = self.inp["G"]
        self.assertEqual(sorted(g["aliases"]), ["GS_Diesel_Prémio", "Index_Diesel_Prémio"])
        self.assertEqual(g["name"], "GS_Diesel_Prémio", "shortest alias first, deterministic")
        self.assertEqual(self.d["dictionary"]["max_aliases_per_column"], 2)
        self.assertEqual(self.d["dictionary"]["distinct_name_target_pairs"], 7,
                         "the same name repeated across scopes counts once")

    def test_a_derived_column_takes_its_name_from_the_named_reference(self):
        c = self.out["C"]
        self.assertEqual(c["name"], "Index_CIFMEDDMA_Preço")
        self.assertEqual(c["name_basis"], "formula_ref")
        self.assertEqual(c["lineage"][:2], ["Index_CIFMEDDMA_Preço", "Data_Lista"])

    def test_a_value_header_is_never_a_name(self):
        for letter in ("F", "H"):
            self.assertEqual(self.inp[letter]["name_basis"], "none", letter)
            self.assertEqual(self.inp[letter]["name"], "Inputs!" + letter)
            self.assertEqual(self.inp[letter]["state"], "Unknown")

    def test_a_derived_column_without_named_reference_or_header_is_unnamed(self):
        self.assertEqual(self.out["L"]["name_basis"], "none")
        self.assertEqual(self.out["L"]["role"], "computed")

    def test_sheet_names_and_functions_are_not_named_ranges(self):
        self.assertEqual(M["named_refs"](
            '=IF(COUNTIF(Dayly_extraction!C1,RC[-7])>0,"Active","Closed")', {"Dayly_extraction"}), [])
        self.assertEqual(M["named_refs"]("=+_xlfn.XLOOKUP(RC[-1],Outputs!R14C2:R23C2,Outputs!R14C8:R23C8)"), [])
        # an INDIRECT-built name is a string fragment, not a reference (PM-005)
        self.assertEqual(M["named_refs"](
            '=INDEX(INDIRECT("CustosLogísticos_"&LEFT(RC,3)&"_"&R5C),MATCH(RC2,Data_Lista,0))'),
            ["Data_Lista"])


class TypesAndRules(unittest.TestCase):

    def setUp(self):
        self.d = draft(extraction([REGISTER, REPORT], NAMES))
        self.inp = columns(self.d, "Inputs")
        self.out = columns(self.d, "Outputs")

    def test_type_vocabulary(self):
        self.assertEqual(self.inp["B"]["type"], "datetime")
        self.assertEqual(self.inp["G"]["type"], "number")
        self.assertEqual(self.out["C"]["type"], "unknown")
        self.assertIn("tipos mistos", self.out["C"]["type_basis"])
        self.assertTrue(any("tipos mistos" in r for r in self.out["C"]["rules"]))

    def test_a_validation_list_makes_a_choice_with_its_values_and_range(self):
        af = self.out["AF"]
        self.assertEqual(af["type"], "choice")
        self.assertEqual(af["values"], ["USD", "EUR"])
        self.assertEqual(af["rules"], ["lista (AF14): USD, EUR"])

    def test_key_like_is_identifier_and_index_candidate_or_primary(self):
        ai = self.out["AI"]
        self.assertEqual(ai["type"], "identifier")
        self.assertEqual(ai["index"], "candidate", "nulls > 0 → not primary")
        prim = draft(extraction([{"name": "S", "columns": [
            col("A", header="ID", itype="str", nonempty=72, nulls=0, distinct=72, key_like=True)]}]))
        self.assertEqual(columns(prim, "S")["A"]["index"], "primary")

    def test_required_from_nulls_and_default_never_inferred(self):
        self.assertTrue(self.inp["B"]["required"])
        self.assertFalse(self.inp["G"]["required"])
        for c in list(self.inp.values()) + list(self.out.values()):
            self.assertIsNone(c["default"])
            self.assertIsNone(c["disposition"])

    def test_role_follows_the_l1_class(self):
        self.assertEqual(self.inp["G"]["role"], "write")
        self.assertEqual(self.inp["F"]["role"], "computed")
        self.assertTrue(self.inp["F"]["computed"])
        empty = draft(extraction([{"name": "S", "columns": [
            col("I", header="VIP", klass="empty", itype="empty", nonempty=0, nulls=72, distinct=0)]}]))
        c = columns(empty, "S")["I"]
        self.assertEqual((c["role"], c["type"], c["state"]), ("no-data", "unknown", "Unknown"))
        self.assertIn("header only", c["type_basis"])

    def test_every_line_carries_state_source_and_locator(self):
        for s in self.d["sheets"]:
            for c in s["columns"]:
                self.assertIn(c["state"], ("Assumed", "Unknown"))
                self.assertTrue(c["source"].startswith("_capture/fx.xlsx.fields-draft.json#"))
                self.assertTrue(c["locator"].startswith("fx.xlsx.extraction.json#sheets["))


class Dictionary(unittest.TestCase):

    def setUp(self):
        self.d = draft(extraction([REGISTER, REPORT], NAMES))
        self.dic = self.d["dictionary"]

    def test_entries_without_data_are_listed_apart_never_as_writes(self):
        self.assertEqual([e["name"] for e in self.dic["entries_without_data"]],
                         ["CustosLogísticos_MGO_Aveiro"])
        self.assertNotIn("CX", columns(self.d, "Inputs"))

    def test_non_column_targets_are_classified(self):
        kinds = {x["name"]: x["kind"] for x in self.dic["non_column_targets"]}
        self.assertEqual(kinds["Data_Output"], "cell")
        self.assertEqual(kinds["DF_GRID_1"], "broken")
        self.assertEqual(kinds["ExternalData_1"], "range", "a table, not a column — never a field")
        self.assertNotIn("DF", [v for x in self.dic["dimensions"] for v in x["values"]],
                         "a broken target invents no dimension")

    def test_three_segment_names_yield_dimensions_with_cardinality(self):
        dims = {x["position"]: x for x in self.dic["dimensions"]}
        self.assertEqual(dims[1]["values"], ["CustosLogísticos", "GS", "Index"])
        self.assertEqual(dims[3]["cardinality"], 2)          # Prémio, Aveiro

    def test_key_candidates_are_the_most_referenced_names(self):
        self.assertEqual(self.dic["key_candidates"][0]["name"], "Data_Lista")

    def test_shape_hint_is_a_hint_not_the_sheet_role(self):
        hints = {s["name"]: s["shape_hint"] for s in self.d["sheets"]}
        self.assertEqual(hints["Inputs"], "register")
        self.assertIn("julgamento do process-model.md", self.d["sheets"][0]["shape_hint_basis"])


class InputContract(unittest.TestCase):

    def test_refuses_anything_that_is_not_an_l1_extraction(self):
        with self.assertRaises(ValueError):
            draft({"artefact": "something-else"})

    def test_cli_is_idempotent_by_sha_and_force_rewrites(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "fx.xlsx.extraction.json"
            dst = Path(tmp) / "fx.xlsx.fields-draft.json"
            src.write_text(json.dumps(extraction([REGISTER], NAMES)), encoding="utf-8")
            code, msg = M["draft_one"](src, dst)
            self.assertEqual(code, 0)
            self.assertTrue(dst.is_file())
            first = dst.read_text(encoding="utf-8")
            code, msg = M["draft_one"](src, dst)
            self.assertIn("unchanged", msg)
            self.assertEqual(dst.read_text(encoding="utf-8"), first)
            code, msg = M["draft_one"](src, dst, force=True)
            self.assertEqual(code, 0)
            self.assertNotIn("unchanged", msg)
            self.assertFalse(list(Path(tmp).glob("*.tmp")), "atomic write leaves no tmp")

    def test_a_failed_extraction_produces_no_draft(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "fx.xlsx.extraction.json"
            dst = Path(tmp) / "fx.xlsx.fields-draft.json"
            src.write_text(json.dumps(extraction([REGISTER], status="failed")), encoding="utf-8")
            code, msg = M["draft_one"](src, dst)
            self.assertEqual(code, 2)
            self.assertFalse(dst.exists())

    def test_engagement_mode_writes_next_to_the_extraction_and_logs(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = Path(tmp) / "eng"
            cap = eng / "_capture"
            cap.mkdir(parents=True)
            (cap / "fx.xlsx.extraction.json").write_text(json.dumps(extraction([REGISTER], NAMES)),
                                                          encoding="utf-8")
            (cap / "doc.docx.extraction.json").write_text("{}", encoding="utf-8")
            import io
            from contextlib import redirect_stdout
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = M["main"](["--engagement", str(eng), "--log"])
            self.assertEqual(rc, 0)
            self.assertIn("fx.xlsx.fields-draft.json:", buf.getvalue())
            self.assertTrue((cap / "fx.xlsx.fields-draft.json").is_file())
            self.assertFalse((cap / "doc.docx.fields-draft.json").exists(), "text tier untouched")
            log = (cap / "_capture-log.md").read_text(encoding="utf-8")
            self.assertIn("| L1b | fx.xlsx | fields-draft |", log)
            self.assertFalse((eng / "_blueprint").exists(), "the motor never touches a blueprint")


def real_draft(slug, workbook):
    p = REPO / "projects" / slug / "_capture" / (workbook + ".extraction.json")
    if not p.is_file():
        return None
    ex = json.loads(p.read_text(encoding="utf-8"))
    return M["build_draft"](ex, p.name, workbook + ".fields-draft.json")


class RealPilot1(unittest.TestCase):
    """Design §8.1 numbers, measured by the motor over the L1 of pricing-marinha-pilot-1."""

    @classmethod
    def setUpClass(cls):
        cls.d = real_draft("pricing-marinha-pilot-1", "PREÇO BANCAS_30_01_26.xlsx")
        if cls.d is None:
            raise unittest.SkipTest("pilot-1 not mounted")

    def test_inputs_named_by_the_dictionary_not_by_the_header_row(self):
        inp = columns(self.d, "Inputs")
        self.assertEqual(len(inp), 91)
        basis = [c["name_basis"] for c in inp.values()]
        self.assertEqual(basis.count("named_range"), 83)
        self.assertEqual(basis.count("header"), 0, "row 1119 holds values, not names (C-017)")
        self.assertEqual([k for k, c in inp.items() if c["name_basis"] == "none"],
                         ["F", "H", "Y", "Z", "AA", "AB", "AL", "CX"])
        self.assertEqual(sum(c["role"] == "write" for c in inp.values()), 85)
        self.assertEqual(sum(c["role"] == "computed" for c in inp.values()), 6)
        self.assertEqual(inp["B"]["name"], "Data_Lista")

    def test_outputs_are_computed_with_lineage(self):
        out = columns(self.d, "Outputs")
        self.assertEqual(sum(c["role"] == "computed" for c in out.values()), 59)
        self.assertEqual(sum(c["role"] == "write" for c in out.values()), 17)
        named = [c for c in out.values() if c["name_basis"] == "formula_ref"]
        self.assertTrue(all(c["lineage"] for c in named))

    def test_dictionary_numbers(self):
        dic = self.d["dictionary"]
        self.assertEqual(dic["named_ranges"], 291)
        self.assertEqual(dic["columns_covered"], 83)
        self.assertEqual(len(dic["entries_without_data"]), 42)
        self.assertEqual(dic["key_candidates"][0]["name"], "Data_Lista")
        # the design's §2.1 measurement, now reproduced by the motor: contraparte × combustível × métrica/porto
        self.assertEqual([(x["position"], x["cardinality"]) for x in dic["dimensions"]],
                         [(1, 10), (2, 22), (3, 46)])


class RealDptGalpJp(unittest.TestCase):
    """Design §8.2: what must come out of the motor WITHOUT judgement."""

    @classmethod
    def setUpClass(cls):
        cls.d = real_draft("dpt-galp-jp", "Dayly_pending_tickets_Anonimo.xlsx")
        if cls.d is None:
            raise unittest.SkipTest("dpt-galp-jp not mounted")

    def test_prioridade_is_a_deterministic_choice(self):
        e = columns(self.d, "Priority_Store")["E"]
        self.assertEqual(e["type"], "choice")
        self.assertEqual(e["values"], ["High", "Medium", "Low"])

    def test_exec_order_is_not_required_and_ticket_id_is_the_key(self):
        ps = columns(self.d, "Priority_Store")
        self.assertFalse(ps["F"]["required"])
        self.assertEqual(ps["F"]["type"], "number")
        self.assertEqual(columns(self.d, "Dayly_extraction")["A"]["index"], "primary")

    def test_live_status_takes_its_header_not_the_sheet_name_in_its_formula(self):
        h = columns(self.d, "Priority_Store")["H"]
        self.assertEqual((h["name"], h["name_basis"], h["role"]), ("Live Status", "header", "computed"))

    def test_empty_columns_are_header_only_unknowns_never_dropped(self):
        de = columns(self.d, "Dayly_extraction")
        for letter in ("D", "I", "J", "K", "M"):
            self.assertEqual(de[letter]["role"], "no-data", letter)
            self.assertEqual(de[letter]["state"], "Unknown", letter)
        self.assertEqual(de["I"]["name"], "VIP")

    def test_sheet_hints(self):
        hints = {s["name"]: s["shape_hint"] for s in self.d["sheets"]}
        self.assertEqual(hints["Priority_Store"], "register")
        self.assertEqual(hints["Prioritized_View"], "report")
        self.assertEqual(hints["Dayly_extraction"], "input-extract")


if __name__ == "__main__":
    unittest.main(verbosity=1)
