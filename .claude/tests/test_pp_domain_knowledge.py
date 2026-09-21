"""Step 4B — PP domain-knowledge runtime layer.

Mechanical/structural assertions only. These prove IMPLEMENTATION FIDELITY against the
approved Step 4A design (taxonomy, unit contract, stable/volatile boundary, CRAFT boundary,
consumer paths). They do NOT prove retrieval or depth behaviour — that is a Step 4C
semantic/pull gate, deliberately not implemented here.

    python .claude/tests/test_pp_domain_knowledge.py
"""

import os
import re
import unittest

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PACK_DIR = os.path.join(ROOT, "library", "packs", "pp")
DK_DIR = os.path.join(PACK_DIR, "domain-knowledge")
DM_DIR = os.path.join(PACK_DIR, "decision-model")

# ---------------------------------------------------------------- approved taxonomy

RESEARCH_UNITS = [
    "application/application-surfaces.md",
    "data/store-boundaries.md",
    "data/dataverse.md",
    "data/sharepoint.md",
    "data/azure-sql.md",
    "data/query-and-delegation.md",
    "automation/automation-mechanisms.md",
    "integration/integration-mechanisms.md",
    "security/security-controls.md",
    "governance/governance-and-environments.md",
    "alm/release-and-lifecycle.md",
    "performance/performance-and-scale.md",
    "economics/licensing-and-cost-drivers.md",
    "operations/operability-and-support.md",
    "architecture/patterns.md",
]

CRAFT_UNITS = [
    "craft/powerfx.md",
    "craft/screen-patterns.md",
    "craft/screen-consolidation-rules.md",
    "craft/excel-translation.md",
    "craft/flow-craft.md",
    "craft/security-craft.md",
    "craft/sql-delivery-conventions.md",
    "craft/anonymization.md",
    "craft/estimation-model.md",
    "craft/delivery-conventions.md",
]

EXPECTED_FILES = ["README.md"] + RESEARCH_UNITS + CRAFT_UNITS

# The 13 files the layer had before Step 4B. None may survive at the old flat path.
RETIRED_FLAT_FILES = [
    "powerfx-patterns.md",
    "screen-patterns.md",
    "security-patterns.md",
    "delegation-matrix.md",
    "excel-patterns.md",
    "dataverse-reference.md",
    "azure-sql-reference.md",
    "sharepoint-reference.md",
    "anonymization.md",
    "flows-patterns.md",
    "estimation-model.md",
    "screen-consolidation-rules.md",
    "delivery-conventions.md",
]

# ---------------------------------------------------------------- helpers


def read(rel, base=DK_DIR):
    with open(os.path.join(base, rel), encoding="utf-8") as fh:
        return fh.read()


def flat(text):
    """Collapse whitespace so a wrapped sentence still matches as one string."""
    return re.sub(r"\s+", " ", text)


def prose(text):
    """Drop fenced code blocks — sample code is not a platform or commercial claim."""
    return re.sub(r"```.*?```", "", text, flags=re.S)


def all_dk_files():
    out = []
    for dirpath, _dirs, files in os.walk(DK_DIR):
        for name in files:
            if name.endswith(".md"):
                rel = os.path.relpath(os.path.join(dirpath, name), DK_DIR)
                out.append(rel.replace(os.sep, "/"))
    return sorted(out)


PACK = yaml.safe_load(read("pack.yaml", base=PACK_DIR))
VOLATILITY = read("volatility-register.md", base=DM_DIR)

# Rows that actually exist in the runtime volatility register.
EXISTING_ROWS = set(re.findall(r"\b(?:VC-\d{2}|VS-\d{2}|TW-V\d)\b", VOLATILITY))

# Canonical research id shapes that must never reach a runtime domain file.
RESEARCH_ID_PATTERNS = [
    r"\bDC-D-\d{3}\b",
    r"\bAP-D-\d{3}\b",
    r"\bALT-\d{3}\b",
    r"\bDA-\d{2}\b",
    r"\bAT2-\d{2}\b",
    r"\bIA-[CU]?-?\d{2}\b",
    r"\bPS-\d{2}\b",
    r"\bPF-[UC]?-?\d{2}\b",
    r"\bSQ2?-\d{2}\b",
    r"\bSP:S-\d{2}\b",
    r"\bDV:S\d{2}\b",
    r"\bVT-\d{2}\b",
    r"\bSY-\d{2}\b",
    r"\bSC-\d{2}\b",
    r"\bDQ-\d{2}\b",
    r"\bNB-\d{2}\b",
    r"Research basis:",
]

# Currency / price shapes. Deliberately narrow enough not to fire on ordinary prose.
PRICE_PATTERNS = [
    r"[$€£]\s?\d",
    r"\b\d+(?:[.,]\d+)?\s?(?:USD|EUR|GBP)\b",
    r"\bper[- ]user\s+price\b",
    r"\bprice\s+per\b",
    r"/GB/month",
    r"\bper\s+GB\s+per\s+month\b",
]

OBSOLETE_BRANCH_VOCAB = ["sharepoint-first", "dataverse-first", "azure-sql-first"]

# Router / load-order semantics the design forbids introducing.
ROUTER_VOCAB = [
    "routing table",
    "load order",
    "preload map",
    "concern-to-file map",
    "retrieval engine",
]


# ---------------------------------------------------------------- taxonomy


class TestTaxonomy(unittest.TestCase):
    def test_exactly_the_expected_files_exist(self):
        self.assertEqual(all_dk_files(), sorted(EXPECTED_FILES))

    def test_counts_match_the_approved_design(self):
        found = all_dk_files()
        self.assertEqual(len(found), 26, "26 files = 15 RESEARCH + 10 CRAFT + 1 README")
        self.assertEqual(len(RESEARCH_UNITS), 15)
        self.assertEqual(len(CRAFT_UNITS), 10)

    def test_no_retired_flat_file_survives(self):
        for name in RETIRED_FLAT_FILES:
            self.assertFalse(
                os.path.exists(os.path.join(DK_DIR, name)),
                "retired flat file still present: %s" % name,
            )


# ---------------------------------------------------------------- RESEARCH contract


class TestResearchUnitContract(unittest.TestCase):
    def test_runtime_header_present_and_classed_research(self):
        for rel in RESEARCH_UNITS:
            body = read(rel)
            self.assertIn("provenance: RUNTIME (domain knowledge) · class: RESEARCH", body, rel)
            self.assertIn("design authority: Step 4A", body, rel)
            self.assertIn("Never preloaded.", body, rel)
            self.assertIn("decision-tree.md §9", body, rel)

    def test_section_zero_pull_questions_present(self):
        for rel in RESEARCH_UNITS:
            body = read(rel)
            self.assertIn("## 0. When to pull this file", body, rel)
            head = body.split("## 0.", 1)[1].split("\n## ", 1)[0]
            # Pull questions are italicised concrete questions; the design asks for 2-4.
            questions = re.findall(r"^- \*.+\?\*$", head, flags=re.M)
            self.assertGreaterEqual(len(questions), 2, "%s: %d pull questions" % (rel, len(questions)))
            self.assertLessEqual(len(questions), 5, "%s: %d pull questions" % (rel, len(questions)))

    def test_boundary_line_present(self):
        for rel in RESEARCH_UNITS:
            body = read(rel)
            head = flat(body.split("## 0.", 1)[1].split("\n## ", 1)[0])
            self.assertIn("This file states", head, "%s: no boundary line in §0" % rel)
            self.assertIn("does not decide", head, "%s: no boundary line in §0" % rel)
            self.assertIn("decision-tree.md", head, rel)

    def test_decision_grade_section_comes_first(self):
        for rel in RESEARCH_UNITS:
            body = read(rel)
            grades = re.findall(r"`(decision|architecture|implementation)-grade`", body)
            self.assertTrue(grades, "%s: no grade markers" % rel)
            self.assertEqual(grades[0], "decision", "%s: first graded section is %s" % (rel, grades[0]))

    def test_alternatives_symmetry_statement_present(self):
        for rel in RESEARCH_UNITS:
            body = flat(read(rel).lower())
            self.assertIn("not evidence that another option class", body,
                          "%s: missing the alternatives-symmetry statement" % rel)


# ---------------------------------------------------------------- CRAFT contract


class TestCraftUnitContract(unittest.TestCase):
    def test_craft_header_and_class(self):
        for rel in CRAFT_UNITS:
            body = read(rel)
            self.assertIn("provenance: RUNTIME (domain knowledge) · class: CRAFT", body, rel)
            self.assertIn("Not an Options D3 pull target.", body, rel)

    def test_craft_states_its_non_authority(self):
        """The boundary statement is mandatory; its LANGUAGE follows the file's consumers.

        Step 4A keeps each craft file in the language its consumers use, so the statement is
        matched in English or Portuguese rather than forced into one.
        """
        pairs = [
            ("no independent research authority", "sem autoridade própria de investigação"),
            ("must not state a platform limit", "não pode afirmar como facto um limite de plataforma"),
        ]
        for rel in CRAFT_UNITS:
            body = flat(read(rel).lower())
            for en, pt in pairs:
                self.assertTrue(en in body or pt in body,
                                "%s: missing the craft boundary statement (%r)" % (rel, en))

    def test_craft_does_not_state_platform_limits_independently(self):
        """A CRAFT file may not present a service limit or threshold as fact.

        Proxy check: no volatility stamp (those belong to RESEARCH units, which own the
        figures) and no delegation ceiling restated in the Power Fx craft file.
        """
        for rel in CRAFT_UNITS:
            body = read(rel)
            self.assertNotIn("Documented reading · read", body,
                             "%s: CRAFT file carries a volatility stamp" % rel)
        # The word "delegable" is legitimate in craft ("once the owner says it is not
        # delegable, write this pattern"). A delegation FIGURE is not.
        powerfx = flat(prose(read("craft/powerfx.md")))
        for pat in (r"500", r"2[,.]?000", r"record limit of \d", r"up to \d+ records"):
            hit = re.search(pat, powerfx)
            self.assertIsNone(hit, "craft/powerfx.md carries a delegation figure -> %r"
                              % (hit and hit.group(0)))
        self.assertIn("query-and-delegation.md", powerfx,
                      "craft/powerfx.md must defer to the RESEARCH owner")

    def test_estimation_model_states_the_comparative_economics_bar(self):
        body = flat(read("craft/estimation-model.md").lower())
        self.assertIn("comparator", body)
        self.assertTrue(
            "not valid as" in body or "barred" in body,
            "craft/estimation-model.md must state it is not valid as comparative economics",
        )

    def test_screen_consolidation_rules_keeps_its_contract(self):
        body = read("craft/screen-consolidation-rules.md")
        low = flat(body.lower())
        for token in ("screen", "field"):
            self.assertIn(token, low)
        self.assertTrue(
            "cap" in low or "limite" in low,
            "the hard caps must survive the move",
        )


# ---------------------------------------------------------------- hygiene, all files


class TestRuntimeHygiene(unittest.TestCase):
    def test_no_prices_anywhere(self):
        for rel in all_dk_files():
            body = prose(read(rel))
            for pat in PRICE_PATTERNS:
                hit = re.search(pat, body, flags=re.I)
                self.assertIsNone(hit, "%s: price token %r -> %r" % (rel, pat, hit and hit.group(0)))

    def test_no_canonical_research_ids_anywhere(self):
        for rel in all_dk_files():
            body = read(rel)
            for pat in RESEARCH_ID_PATTERNS:
                hit = re.search(pat, body)
                self.assertIsNone(hit, "%s: research id %r -> %r" % (rel, pat, hit and hit.group(0)))

    def test_no_obsolete_branch_vocabulary(self):
        for rel in all_dk_files():
            body = flat(read(rel).lower())
            for token in OBSOLETE_BRANCH_VOCAB:
                self.assertNotIn(token, body, "%s: obsolete branch vocabulary %r" % (rel, token))

    def test_no_router_or_load_order_semantics(self):
        for rel in all_dk_files():
            body = flat(read(rel).lower())
            for token in ROUTER_VOCAB:
                if token in body:
                    # Permitted only as an explicit negation of the construct.
                    idx = body.index(token)
                    window = body[max(0, idx - 90): idx + len(token) + 20]
                    self.assertTrue(
                        any(neg in window for neg in ("no ", "not ", "never", "não ", "forbidden")),
                        "%s: router/load-order semantics introduced (%r)" % (rel, token),
                    )

    def test_no_deleted_r0_thresholds_restated(self):
        """The deleted disqualification gates and their invented numbers must not survive."""
        banned = [
            r"30[,.]?000\s+rows",
            r"formula_count",
            r"disqualification gate",
        ]
        for rel in all_dk_files():
            body = read(rel)
            for pat in banned:
                hit = re.search(pat, body, flags=re.I)
                self.assertIsNone(hit, "%s: deleted R0 threshold %r -> %r"
                                  % (rel, pat, hit and hit.group(0)))

    def test_no_selection_verdict_language(self):
        """A capability absence is domain knowledge; 'therefore inappropriate' is selection.

        The banned phrases may appear when a unit *names them as forbidden* — that is the
        prohibition doing its job. They may not appear as assertions, so a hit is a failure
        unless the surrounding window marks it as quoted or negated.
        """
        banned = [
            "therefore inappropriate",
            "makes sharepoint inappropriate",
            "is the best choice",
            "is the recommended option",
            "wins on",
        ]
        markers = (
            "selection verdict", "forbidden", "never", "not ", "no ",
            "belongs to", "is not", "prohibit", "must not", "— that",
        )
        for rel in all_dk_files():
            body = flat(read(rel).lower())
            for token in banned:
                start = 0
                while True:
                    idx = body.find(token, start)
                    if idx == -1:
                        break
                    start = idx + len(token)
                    window = body[max(0, idx - 160): idx + len(token) + 160]
                    self.assertTrue(
                        any(m in window for m in markers),
                        "%s: selection verdict asserted (%r)" % (rel, token),
                    )


# ---------------------------------------------------------------- stable / volatile


class TestVolatilityStamping(unittest.TestCase):
    STAMP = re.compile(r"Documented reading · read (\d{4}-\d{2}-\d{2}) · re-verify: ([^\s(]+)")

    def test_every_stamp_names_an_existing_register_row(self):
        seen = 0
        for rel in RESEARCH_UNITS:
            for _date, row in self.STAMP.findall(read(rel)):
                seen += 1
                self.assertIn(row, EXISTING_ROWS,
                              "%s: stamp names %r, which is not a row in volatility-register.md"
                              % (rel, row))
        self.assertGreater(seen, 0, "no volatile figure is stamped anywhere")

    def test_every_referenced_register_row_exists(self):
        for rel in RESEARCH_UNITS:
            for row in re.findall(r"`(VC-\d{2}|VS-\d{2}|TW-V\d)`", read(rel)):
                self.assertIn(row, EXISTING_ROWS,
                              "%s: references non-existent register row %s" % (rel, row))

    def test_conflicted_ceiling_is_not_carried_numerically(self):
        """The one live quantitative conflict is rendered as the conflict, never as a value."""
        for rel in ("integration/integration-mechanisms.md", "performance/performance-and-scale.md"):
            body = read(rel)
            self.assertIn("CONFLICTED", body.upper(), rel)
            low = flat(body.lower())
            self.assertTrue(
                "until measured" in low or "decision-blocked" in low,
                "%s: the conflict must carry its measurement obligation" % rel,
            )
            # Neither side of the disputed per-minute ceiling may appear.
            for pat in (r"\b500\s*(?:requests?|calls?)\s*/?\s*min",
                        r"\b10[,.]?000\s*(?:requests?|calls?)\s*/?\s*min"):
                hit = re.search(pat, body, flags=re.I)
                self.assertIsNone(hit, "%s: conflicted figure carried -> %r"
                                  % (rel, hit and hit.group(0)))

    def test_register_is_not_copied_wholesale(self):
        """Domain knowledge must not become a current-facts database.

        NAMING many rows in a "what must be verified" table is the sanctioned pattern — the
        performance unit legitimately touches most of the meters. What has to stay scarce is
        the number of FIGURES carried, so the bound is on stamped readings rather than on row
        references.
        """
        for rel in RESEARCH_UNITS:
            stamps = self.STAMP.findall(read(rel))
            self.assertLess(len(stamps), 12,
                            "%s: carries %d stamped figures - reads as a current-facts database"
                            % (rel, len(stamps)))


# ---------------------------------------------------------------- manifest


class TestPackManifest(unittest.TestCase):
    def test_declared_paths_all_exist(self):
        declared = PACK.get("domain_knowledge") or []
        self.assertTrue(declared, "pack.yaml declares no domain_knowledge")
        for rel in declared:
            self.assertTrue(rel.startswith("domain-knowledge/"), rel)
            self.assertTrue(os.path.exists(os.path.join(PACK_DIR, rel)),
                            "pack.yaml declares a missing path: %s" % rel)

    def test_every_unit_is_declared_and_vice_versa(self):
        declared = sorted(r[len("domain-knowledge/"):] for r in (PACK.get("domain_knowledge") or []))
        self.assertEqual(declared, sorted(EXPECTED_FILES),
                         "pack.yaml manifest and the authored taxonomy disagree")

    def test_no_research_ids_in_pack_yaml(self):
        raw = read("pack.yaml", base=PACK_DIR)
        for pat in RESEARCH_ID_PATTERNS:
            hit = re.search(pat, raw)
            self.assertIsNone(hit, "pack.yaml carries a research id %r -> %r"
                              % (pat, hit and hit.group(0)))

    def test_manifest_carries_no_routing_semantics(self):
        raw = read("pack.yaml", base=PACK_DIR)
        block = raw.split("domain_knowledge:", 1)[1].split("\nquestion_bank:", 1)[0]
        # The comments explain what the manifest is NOT; only the data lines are under test.
        block = "\n".join(l for l in block.splitlines()
                          if not l.strip().startswith("#")).lower()
        for token in ("priority", "order:", "stage:", "concern"):
            self.assertNotIn(token, block,
                             "pack.yaml.domain_knowledge must stay a manifest (%r)" % token)

    def test_pack_version_bumped(self):
        version = str(PACK.get("pack_version", ""))
        parts = version.split(".")
        self.assertEqual(len(parts), 3, "pack_version is not semver: %r" % version)
        self.assertGreaterEqual((int(parts[0]), int(parts[1])), (1, 6),
                                "pack_version must be bumped past the Step 3 line: %r" % version)


# ---------------------------------------------------------------- consumers


class TestConsumerPaths(unittest.TestCase):
    CONSUMERS = [
        ".claude/skills/aisa-blueprint/SKILL.md",
        ".claude/skills/aisa-simulate/SKILL.md",
        ".claude/agent-memory/_universal/solution-architect/anti-patterns.md",
        ".claude/agent-memory/_universal/compliance-officer/anti-patterns.md",
        "library/packs/pp/deliverable-templates/claude-design-brief.template.md",
        "library/kernel/blueprint-contract.md",
        "docs/ARCHITECTURE.md",
        "docs/PACK_AUTHORING.md",
        "docs/ONBOARDING.md",
    ]

    def _text(self, rel):
        with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
            return fh.read()

    def test_no_consumer_references_a_retired_flat_path(self):
        """No dead path may stand alone.

        A retired flat path is allowed only on a line that also names its live replacement —
        which is how a historical v1 to v2 migration record stays truthful without pointing a
        reader at a file that no longer exists. Anywhere else it is a stale reference.
        """
        live = re.compile(
            r"domain-knowledge/(?:craft|application|data|automation|integration|security"
            r"|governance|alm|performance|economics|operations|architecture)/"
        )
        for rel in self.CONSUMERS:
            for n, line in enumerate(self._text(rel).splitlines(), 1):
                for name in RETIRED_FLAT_FILES:
                    if "domain-knowledge/" + name in line:
                        self.assertRegex(
                            line, live,
                            "%s:%d stale flat domain-knowledge path %s with no live "
                            "replacement on the same line" % (rel, n, name),
                        )

    def test_blueprint_hard_contract_path_is_valid(self):
        body = self._text(".claude/skills/aisa-blueprint/SKILL.md")
        self.assertIn("domain-knowledge/craft/screen-consolidation-rules.md", body)
        self.assertTrue(
            os.path.exists(os.path.join(DK_DIR, "craft", "screen-consolidation-rules.md")),
            "the named hard contract must exist at its new path",
        )

    def test_solution_architect_memory_no_longer_restates_a_threshold(self):
        body = self._text(".claude/agent-memory/_universal/solution-architect/anti-patterns.md")
        self.assertNotIn(">2000 records", body)
        self.assertIn("data/query-and-delegation.md", body)

    def test_design_brief_cross_references_resolve(self):
        body = self._text("library/packs/pp/deliverable-templates/claude-design-brief.template.md")
        for rel in re.findall(r"library/packs/pp/domain-knowledge/([A-Za-z0-9_./-]+\.md)", body):
            self.assertTrue(os.path.exists(os.path.join(DK_DIR, rel)),
                            "design brief cites a missing unit: %s" % rel)


# ---------------------------------------------------------------- README contract


class TestReadmeContract(unittest.TestCase):
    def test_readme_states_the_pull_rule_and_boundaries(self):
        body = read("README.md")
        low = flat(body.lower())
        for token in ("pull", "decision-grade", "architecture-grade", "implementation-grade"):
            self.assertIn(token, low, token)
        self.assertIn("D3", body)
        self.assertTrue("never preloaded" in low or "never preloaded." in low)
        self.assertIn("craft", low)
        self.assertTrue(
            "never chooses the winning option" in low or "never decides which option" in low,
            "README must carry the prohibition",
        )

    def test_readme_is_not_a_router(self):
        low = flat(read("README.md").lower())
        self.assertIn("no router", low)


# ======================================================================
# Step 4B pre-4C bounded repair
# ======================================================================

REGISTER = read("volatility-register.md", base=DM_DIR)

# The five decision-model registers. The repair may amend volatility OWNERSHIP only; the
# other four and the spine carry decision semantics and must be untouched by it.
DECISION_SEMANTIC_FILES = [
    os.path.join(PACK_DIR, "decision-tree.md"),
    os.path.join(DM_DIR, "alternatives-register.md"),
    os.path.join(DM_DIR, "blocking-set.md"),
    os.path.join(DM_DIR, "composed-disqualifiers.md"),
    os.path.join(DM_DIR, "outcome-classes.md"),
]

ANNEXES = {
    "step-4b-runtime-provenance.md": "provenance",
    "step-4b-number-adjudication.md": "number adjudication",
    "step-4b-research-gaps.md": "research gaps",
}
AUTHORING_DIR = os.path.join(
    ROOT, "docs", "pp-pack-authoring", "research", "pp", "authoring"
)


def annex(name):
    with open(os.path.join(AUTHORING_DIR, name), encoding="utf-8") as fh:
        return fh.read()


def register_rows():
    return set(re.findall(r"\*\*(VC-\d{2}|VS-\d{2}|TW-V\d)\*\*", REGISTER))


def rows_used_by_runtime():
    used = set()
    for rel in all_dk_files():
        used |= set(re.findall(r"\b(VC-\d{2}|VS-\d{2}|TW-V\d)\b", read(rel)))
    return used


class TestVolatilityOwnershipRepair(unittest.TestCase):
    """1. Every volatile documented reading has an existing owner — and vice versa."""

    def test_every_reading_has_an_existing_owner(self):
        stamp = re.compile(r"re-verify: ([A-Z]{2}-[A-Z0-9]{1,3})")
        rows = register_rows()
        seen = 0
        for rel in RESEARCH_UNITS:
            for row in stamp.findall(read(rel)):
                seen += 1
                self.assertIn(row, rows, "%s: reading owned by %r, absent from the register"
                              % (rel, row))
        self.assertGreater(seen, 0)

    def test_no_orphan_row_reference_and_no_unowned_row(self):
        rows, used = register_rows(), rows_used_by_runtime()
        self.assertEqual(sorted(used - rows), [],
                         "runtime references rows that do not exist")
        self.assertEqual(sorted(rows - used), [],
                         "register rows nothing references — dead ownership")

    def test_the_amendment_is_present_and_scoped(self):
        self.assertIn("2A. Ownership amendment", REGISTER)
        low = flat(REGISTER.lower())
        # It must say what it did NOT change.
        for token in ("stage", "concern", "blocking", "option class",
                      "outcome", "composed row", "comparator"):
            self.assertIn(token, low, "the amendment must state it changed no %r" % token)
        self.assertIn("no figures", low)

    def test_register_still_supplies_no_figures(self):
        """The register names what is volatile; the reading is taken at the decision date."""
        body = prose(REGISTER)
        # A service-limit-shaped figure would be a value, not an ownership statement.
        for pat in (r"\b\d{3,}\s*(?:calls?|requests?|rows?|items?|actions?)\b",
                    r"\b\d+\s*(?:MB|GB)\b"):
            hit = re.search(pat, body, flags=re.I)
            self.assertIsNone(hit, "volatility-register carries a figure -> %r"
                              % (hit and hit.group(0)))


class TestOwnershipGranularity(unittest.TestCase):
    """2. No new row groups unrelated facts under one owner."""

    def test_v1_is_split_propagation_from_revocation(self):
        self.assertIn("**VS-21**", REGISTER)
        self.assertIn("**VS-22**", REGISTER)
        low = flat(REGISTER.lower())
        self.assertIn("propagation", low)
        self.assertIn("revocation", low)

    def test_v3_is_split_by_service_family(self):
        for row in ("**VS-24**", "**VS-25**", "**VS-26**"):
            self.assertIn(row, REGISTER, "V3 must not collapse into one row (%s)" % row)

    def test_v4_excludes_the_conflicted_ceiling(self):
        block = REGISTER.split("**VS-27**", 1)[1].split("\n|", 1)[0]
        low = flat(block.lower())
        self.assertIn("exclud", low,
                      "VS-27 must explicitly exclude the conflicted custom-connector ceiling")
        self.assertTrue("vc-01" in low or "vs-08" in low,
                        "VS-27 must name where the conflicted ceiling stays")

    def test_every_new_row_states_why_the_family_holds_together(self):
        """Each amendment row carries a 'why these belong together' justification."""
        section = REGISTER.split("2A. Ownership amendment", 1)[1].split("\n## ", 1)[0]
        rows = [l for l in section.splitlines()
                if re.match(r"^\| \*\*VS-\d{2}\*\*", l)]
        self.assertEqual(len(rows), 19, "expected 19 amendment rows, found %d" % len(rows))
        for l in rows:
            cells = [c.strip() for c in l.strip().strip("|").split("|")]
            self.assertGreaterEqual(len(cells), 4, "row is missing columns: %s" % l[:60])
            # cells = [id, family, why-together, re-verify-at]
            self.assertGreater(len(cells[2]), 40,
                               "row %s has no substantive grouping rationale" % cells[0])

    def test_grouping_rule_is_stated(self):
        low = flat(REGISTER.lower())
        for token in ("factual subject", "volatility mechanism",
                      "re-verification trigger", "decision consequence"):
            self.assertIn(token, low, "the four-way grouping rule must be stated (%r)" % token)


class TestVs04Split(unittest.TestCase):
    """3. VS-04's two former responsibilities are separated."""

    def test_vs04_is_narrowed_to_the_access_path(self):
        row = [l for l in REGISTER.splitlines() if l.startswith("| **VS-04**")]
        self.assertEqual(len(row), 1)
        low = row[0].lower()
        self.assertTrue("view" in low or "query" in low or "access-path" in low)
        self.assertIn("vs-29", low, "VS-04 must point at the row that took the other half")

    def test_vs29_owns_the_authorization_scope(self):
        row = [l for l in REGISTER.splitlines() if l.startswith("| **VS-29**")]
        self.assertEqual(len(row), 1)
        low = row[0].lower()
        self.assertIn("permission", low)
        self.assertIn("split", low)

    def test_the_authorization_use_migrated_off_vs04(self):
        sec = flat(read("security/security-controls.md"))
        self.assertIn("VS-29", sec,
                      "the security unit's permission-scope fact must now cite VS-29")
        table = sec.split("| Fact | Register row |", 1)[1]
        self.assertNotIn("scale threshold used as the access-granularity boundary | `VS-04`",
                         table, "the security unit still carries the old combined row")

    def test_no_unit_still_conflates_the_two_facts(self):
        for rel in RESEARCH_UNITS:
            body = flat(read(rel))
            for line in read(rel).splitlines():
                if "VS-04" in line and "permission" in line.lower():
                    self.fail("%s conflates the access-path and authorization facts: %s"
                              % (rel, line[:90]))


class TestConflictedStillUnsettled(unittest.TestCase):
    """4. Conflicted figures remain unsettled after the repair."""

    def test_the_live_conflict_is_still_a_conflict(self):
        self.assertIn("CONFLICTED", REGISTER.upper())
        low = flat(REGISTER.lower())
        self.assertIn("encode neither", low)

    def test_no_unit_settled_a_conflicted_fact(self):
        for rel in RESEARCH_UNITS:
            body = prose(read(rel))
            for pat in (r"\b500\s*(?:requests?|calls?)\s*/?\s*min",
                        r"\b10[,.]?000\s*(?:requests?|calls?)\s*/?\s*min"):
                hit = re.search(pat, body, flags=re.I)
                self.assertIsNone(hit, "%s: conflicted figure now carried -> %r"
                                  % (rel, hit and hit.group(0)))

    def test_elastic_maturity_row_owns_reverification_not_an_answer(self):
        row = [l for l in REGISTER.splitlines() if l.startswith("| **VS-32**")]
        self.assertEqual(len(row), 1)
        low = row[0].lower()
        self.assertTrue("contradict" in low or "conflict" in low)
        self.assertTrue("never a settled" in low or "re-verification" in low)


class TestDecisionSemanticsUntouched(unittest.TestCase):
    """7. No decision semantics changed by the repair."""

    def test_spine_and_four_registers_carry_no_amendment(self):
        for path in DECISION_SEMANTIC_FILES:
            with open(path, encoding="utf-8") as fh:
                body = fh.read()
            self.assertNotIn("Ownership amendment", body,
                             "%s was touched by the volatility repair" % path)
            self.assertNotIn("pre-4C", body, "%s was touched by the repair" % path)

    def test_spine_still_carries_no_platform_figure(self):
        with open(os.path.join(PACK_DIR, "decision-tree.md"), encoding="utf-8") as fh:
            spine = fh.read()
        self.assertIn("This file contains no platform figure", spine)

    def test_amendment_lives_only_in_the_volatility_register(self):
        self.assertIn("Ownership amendment", REGISTER)


class TestAuthoringAnnexes(unittest.TestCase):
    """9-12. The three annexes exist, and they actually cover what they claim."""

    def test_the_three_annexes_exist(self):
        for name, what in ANNEXES.items():
            path = os.path.join(AUTHORING_DIR, name)
            self.assertTrue(os.path.exists(path), "missing %s annex: %s" % (what, name))
            self.assertGreater(len(annex(name)), 4000, "%s annex is a stub" % what)

    def test_annexes_are_authoring_side_only(self):
        for name in ANNEXES:
            low = flat(annex(name).lower())
            self.assertIn("authoring-side only", low,
                          "%s must declare itself authoring-side" % name)
        # And none of them leaked into the pack.
        for rel in all_dk_files():
            for name in ANNEXES:
                self.assertNotIn(name, read(rel),
                                 "%s references the %s annex" % (rel, name))

    def test_provenance_annex_covers_every_research_unit(self):
        body = annex("step-4b-runtime-provenance.md")
        for rel in RESEARCH_UNITS:
            self.assertIn("`%s`" % rel, body,
                          "provenance annex does not cover %s" % rel)
        sections = re.findall(r"^## \d+\. `(.+?)`", body, flags=re.M)
        self.assertEqual(len(sections), 15,
                         "expected one provenance section per RESEARCH unit, found %d"
                         % len(sections))

    def test_provenance_annex_row_count_matches_its_own_claim(self):
        body = annex("step-4b-runtime-provenance.md")
        claimed = int(re.search(r"\| \*\*Total\*\* \| \*\*(\d+)\*\* \|", body).group(1))
        counted, cur = 0, None
        for line in body.splitlines():
            if re.match(r"^## \d+\. `", line):
                cur = True
                continue
            if cur and line.startswith("| ") and not line.startswith("| Rule") \
                    and not line.startswith("|---"):
                counted += 1
        self.assertEqual(claimed, counted,
                         "provenance annex claims %d rows but carries %d" % (claimed, counted))

    def test_all_research_gaps_are_persisted_and_contiguous(self):
        body = annex("step-4b-research-gaps.md")
        ids = sorted({int(m) for m in re.findall(r"`G-(\d{3})`", body)})
        self.assertEqual(ids, list(range(1, len(ids) + 1)),
                         "gap ids are not contiguous — an entry was lost")
        claimed = int(re.search(r"`RESEARCH GAPS PERSISTED: (\d+)`", body).group(1))
        self.assertEqual(claimed, len(ids),
                         "gap annex claims %d gaps but carries %d" % (claimed, len(ids)))
        self.assertGreaterEqual(len(ids), 63,
                                "the annex must persist at least the reported 63 gaps")

    def test_gap_annex_records_the_count_correction(self):
        low = flat(annex("step-4b-research-gaps.md").lower())
        self.assertIn("report figure corrected", low)

    def test_number_adjudication_covers_every_source_file_and_class(self):
        body = annex("step-4b-number-adjudication.md")
        for name in RETIRED_FLAT_FILES:
            self.assertIn(name, body,
                          "number-adjudication annex omits source file %s" % name)
        for cls in ("stable-retain", "volatile-retain-stamped", "register-owned",
                    "implementation-trivia", "unsupported-remove", "conflicted"):
            self.assertIn(cls, body, "adjudication class %r is missing" % cls)

    def test_number_adjudication_reflects_the_repair(self):
        low = flat(annex("step-4b-number-adjudication.md").lower())
        for token in ("bounded volatility repair", "restored to runtime",
                      "survival test", "measurement-owned"):
            self.assertIn(token, low, "annex does not reflect the repair (%r)" % token)


class TestRepairIsRecorded(unittest.TestCase):
    """14. The report carries the bounded-repair note and the corrections."""

    REPORT = "step-4b-domain-knowledge-implementation-report.md"

    def _report(self):
        return annex(self.REPORT)

    def test_repair_note_appended(self):
        body = self._report()
        self.assertIn("Bounded pre-4C repair", body)
        low = flat(body.lower())
        for token in ("rows added", "rows split", "restored",
                      "deliberately left out", "provenance annex",
                      "number-adjudication annex", "research-gap annex",
                      "no new research"):
            self.assertIn(token, low, "repair note is missing %r" % token)

    def test_half_life_is_deferred_not_open(self):
        low = flat(self._report().lower())
        self.assertIn("deferred to pilot", low)
        self.assertIn("non-blocking for step 4c", low)
        pack_raw = read("pack.yaml", base=PACK_DIR)
        self.assertIn("half_lives_override: {}", pack_raw)
        self.assertIn("trigger", pack_raw.lower())

    def test_the_report_count_is_corrected(self):
        body = self._report()
        self.assertIn("New units with no migration source (11)", body)
        self.assertNotIn("New units with no migration source (7)", body)


if __name__ == "__main__":
    unittest.main(verbosity=2)
