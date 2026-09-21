"""Phase F — state scaffold checks.

Asserts that the SU skeleton `aisa-start` writes matches the authoritative
column contract in `library/kernel/states.md`, that `_capture/` is visible in
the scaffold listing, and that the dashboard parser still reads pre-v2.3 SUs
(no migration). Deliberately small: no scaffold driver, no fixture engagement.

    python .claude/tests/test_state_scaffold.py
"""

import importlib.util
import io
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def read(*parts):
    with io.open(os.path.join(ROOT, *parts), encoding="utf-8") as fh:
        return fh.read()


def slurp(path):
    with io.open(path, encoding="utf-8") as fh:
        return fh.read()


START = read(".claude", "skills", "aisa-start", "SKILL.md")
STATES = read("library", "kernel", "states.md")


def load_dashboard():
    path = os.path.join(ROOT, "library", "kernel", "tools", "dashboard.py")
    spec = importlib.util.spec_from_file_location("aisa_dashboard", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def cells(row):
    return [c.strip() for c in row.strip().strip("|").split("|")]


def contract_columns(state):
    """The authoritative column list for a state, from states.md §Schema."""
    m = re.search(r"^\| `## %s` \| (.+) \|$" % state, STATES, re.M)
    assert m, state
    out = []
    for c in m.group(1).split(r"\|"):
        c = c.strip().strip("`").strip()
        out.append(re.sub(r"\s*\(.*\)$", "", c))
    return out


def scaffold_columns(state):
    """The header `aisa-start` step 8 writes for a state."""
    m = re.search(r"^\s*## %s\s*$\n\s*\n(\s*\|.+\|)\s*$" % state, START, re.M)
    assert m, state
    return cells(m.group(1))


class TestScaffoldMatchesContract(unittest.TestCase):
    """The skeleton can hold what the lenses are mandated to stamp."""

    STATES = ("Confirmed", "Assumed", "Unknown", "Conflicted", "Risky")

    def test_every_state_header_matches_states_md(self):
        for state in self.STATES:
            self.assertEqual(scaffold_columns(state), contract_columns(state), state)

    def test_unknown_carries_custo_and_swing(self):
        cols = scaffold_columns("Unknown")
        self.assertIn("custo", cols)
        self.assertIn("swing", cols)

    def test_unknown_column_order_is_the_contract_order(self):
        self.assertEqual(
            scaffold_columns("Unknown"),
            ["id", "lens", "pergunta", "quem responde", "criticidade", "custo", "swing", "ronda"])

    def test_separator_row_width_matches_the_header(self):
        for state in self.STATES:
            m = re.search(r"^\s*## %s\s*$\n\s*\n(\s*\|.+\|)\s*\n(\s*\|[-|]+\|)\s*$" % state,
                          START, re.M)
            self.assertIsNotNone(m, state)
            self.assertEqual(len(cells(m.group(1))), len(cells(m.group(2))), state)

    def test_skeleton_points_at_the_owning_kernel_sections(self):
        self.assertIn("library/kernel/states.md", START)
        self.assertIn("Question economics", START)
        self.assertIn("Epistemic half-lives", START)

    def test_no_state_invented_by_the_scaffold(self):
        headings = re.findall(r"^\s{3}## (\w+)\s*$", START, re.M)
        self.assertEqual(headings, list(self.STATES))


class TestCaptureVisibleInScaffold(unittest.TestCase):
    """`_capture/` is the shared deterministic evidence surface, next to inputs/."""

    def test_capture_is_in_the_directory_listing(self):
        listing = re.search(r"5\. \*\*Create the folder structure\*\*:\n   ```\n(.+?)   ```",
                            START, re.S).group(1)
        self.assertIn("_capture/", listing)
        self.assertIn("inputs/", listing)
        self.assertIn("evidence", listing)

    def test_raw_inputs_are_not_replaced(self):
        listing = re.search(r"5\. \*\*Create the folder structure\*\*:\n   ```\n(.+?)   ```",
                            START, re.S).group(1)
        self.assertIn("raw source material", listing)
        self.assertIn("authoritative", listing)

    def test_no_second_evidence_directory(self):
        listing = re.search(r"5\. \*\*Create the folder structure\*\*:\n   ```\n(.+?)   ```",
                            START, re.S).group(1)
        self.assertEqual(re.findall(r"_(?:capture|evidence|extract)\w*/", listing), ["_capture/"])

    def test_capture_producer_is_still_the_capture_skill(self):
        self.assertIn("aisa-capture", START)
        self.assertIn("_capture/evidence-index.md", START)


class TestNoMigration(unittest.TestCase):
    """Existing engagements are not rewritten; older SUs stay readable."""

    @classmethod
    def setUpClass(cls):
        cls.dash = load_dashboard()
        cls.sus = sorted(
            p for p in (os.path.join(ROOT, "projects", d, "shared-understanding.md")
                        for d in os.listdir(os.path.join(ROOT, "projects"))
                        if os.path.isdir(os.path.join(ROOT, "projects", d)))
            if os.path.isfile(p))

    def test_no_migration_machinery_in_the_start_skill(self):
        for token in ("migrat", "backfill", "rewrite the existing", "upgrade the SU"):
            self.assertNotIn(token, START.lower())

    def test_a_pre_v23_su_still_exists_untouched(self):
        legacy = [p for p in self.sus
                  if "| custo |" not in re.search(r"## Unknown\n\n(\|.+\|)\n",
                                                  io.open(p, encoding="utf-8").read()).group(1)]
        self.assertTrue(legacy, "no pre-v2.3 SU left to prove tolerance against")

    def test_parser_reads_every_existing_su_and_infers_absent_columns(self):
        for path in self.sus:
            md = slurp(path)
            _hdr, rows, meta, _diag = self.dash.parse_su(md)
            self.assertIn(meta["schema_flavour"], ("legacy", "v2.3"), path)
            for row in [r for r in rows if r["state"] == "Unknown"]:
                self.assertTrue(row["custo"], path)
                self.assertTrue(row["swing_class"], path)

    def test_compatibility_defaults_are_the_kernel_ones(self):
        self.assertEqual(self.dash.DEFAULT_CUSTO, "email")
        self.assertEqual(self.dash.DEFAULT_SWING, "dimensionante")
        self.assertIn("`custo = email`, `swing = dimensionante`", STATES)
        self.assertIn("applied on read, never migrated", STATES)

    def test_a_new_scaffold_su_parses_as_v23(self):
        skeleton = re.search(r"8\. \*\*Write the `shared-understanding\.md` skeleton\*\*.*?"
                             r"```markdown\n(.+?)\n   ```", START, re.S).group(1)
        md = "\n".join(l[3:] if l.startswith("   ") else l for l in skeleton.splitlines())
        _hdr, rows, meta, diag = self.dash.parse_su(md)
        self.assertEqual(meta["schema_flavour"], "v2.3")
        self.assertEqual(rows, [])
        self.assertEqual(diag, [])
        self.assertEqual(meta["sections"]["Unknown"]["columns"],
                         ["id", "lens", "pergunta", "quem responde", "criticidade",
                          "custo", "swing", "ronda"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
