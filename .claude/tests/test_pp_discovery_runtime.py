"""Phase G — PP Discovery runtime artifacts.

Asserts the properties the cleanup is supposed to hold, not their sizes:
the six Discovery lenses still get cues, the cues stay neutral tokens, every
probe states a trigger, the question bank stays consumable by `aisa-status`,
and no canonical research id leaks into the runtime pack.

    python .claude/tests/test_pp_discovery_runtime.py
"""

import os
import re
import unittest

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PACK_DIR = os.path.join(ROOT, "library", "packs", "pp")

DISCOVERY = ["business", "operations", "user", "data", "governance", "financial"]

# Canonical research namespaces from the PP corpus. `Q-GOV-NN`/`P-GOV-NN` are
# question ids, not research ids, so `GOV-` is matched only when not preceded by one.
CANONICAL_ID = re.compile(
    r"\b(?:DC-D-\d+|AP-D-\d+|PS-\d+|LC-\d+|OP-\d+|SC-\d+|DQ-\d+|NB-\d+|AA-\d+"
    r"|DA-\d+|AT2-\d+|IA-\d+|ALT-\d+|PF-\d+|SY-\d+|VT-\d+|SQ2-\d+)\b"
)
GOV_RESEARCH_ID = re.compile(r"(?<![QP]-)\bGOV-\d+\b")

VENDOR_TERMS = [
    "power platform", "power apps", "power automate", "power fx", "power pages",
    "dataverse", "sharepoint", "canvas", "model-driven", "copilot",
    "microsoft", "azure", "premium connector", "managed solution",
]


def read(name):
    with open(os.path.join(PACK_DIR, name), encoding="utf-8") as fh:
        return fh.read()


PACK_TEXT = read("pack.yaml")
PACK = yaml.safe_load(PACK_TEXT)
QBANK = read("question-bank.md")
GLOSSARY = read("glossary.md")


class TestDiscoveryCues(unittest.TestCase):
    def test_all_six_discovery_lenses_receive_cues(self):
        cfg = PACK["lenses_config"]
        for lens in DISCOVERY:
            self.assertIn(lens, cfg, "%s missing from lenses_config" % lens)
            signals = cfg[lens].get("extra_signals")
            self.assertTrue(signals, "%s has no extra_signals to inject" % lens)

    def test_cue_count_is_within_the_soft_heuristic(self):
        # Soft authoring guardrail (plan §9): preferably 5-8 per Discovery lens.
        for lens in DISCOVERY:
            n = len(PACK["lenses_config"][lens]["extra_signals"])
            self.assertLessEqual(n, 8, "%s injects %d cues — over the heuristic" % (lens, n))
            self.assertGreaterEqual(n, 3, "%s injects only %d cues" % (lens, n))

    def test_cues_are_neutral_tokens(self):
        for lens in DISCOVERY:
            for signal in PACK["lenses_config"][lens]["extra_signals"]:
                self.assertRegex(signal, r"^[a-z][a-z0-9_]+$", "not a token: %r" % signal)
                for term in VENDOR_TERMS:
                    self.assertNotIn(term, signal.lower(), "%s names a product" % signal)

    def test_cues_are_not_duplicated_across_lenses(self):
        seen = {}
        for lens in DISCOVERY:
            for signal in PACK["lenses_config"][lens]["extra_signals"]:
                self.assertNotIn(
                    signal, seen, "%s duplicated in %s and %s" % (signal, seen.get(signal), lens)
                )
                seen[signal] = lens

    def test_technology_lens_keeps_its_options_only_config(self):
        tech = PACK["lenses_config"]["technology"]
        self.assertNotIn("extra_signals", tech, "technology must not join the Discovery loop")
        self.assertTrue(tech["constraints_to_check"])

    def test_no_mandatory_coverage_semantics_in_the_pack(self):
        for text, name in ((PACK_TEXT, "pack.yaml"), (QBANK, "question-bank.md")):
            low = text.lower()
            for phrase in ("must cover", "coverage requirement", "every signal must",
                           "all signals", "mandatory question"):
                self.assertNotIn(phrase, low, "%s encodes coverage: %r" % (name, phrase))


class TestQuestionBank(unittest.TestCase):
    def test_status_is_the_declared_consumer_and_can_resolve_it(self):
        self.assertEqual(PACK["question_bank"], "question-bank.md")
        self.assertTrue(os.path.exists(os.path.join(PACK_DIR, PACK["question_bank"])))
        with open(os.path.join(ROOT, ".claude", "skills", "aisa-status", "SKILL.md"),
                  encoding="utf-8") as fh:
            status = fh.read()
        self.assertIn("question_bank", status)
        # the two id shapes `aisa-status` step 6d names must exist in the bank
        self.assertTrue(re.search(r"\*\*Q-[A-Z]{3}-\d\d\*\*", QBANK))
        self.assertTrue(re.search(r"\*\*P-[A-Z]{3}-\d\d\*\*", QBANK))

    def test_core_patterns_per_lens_within_range(self):
        counts = {}
        for lens_code in re.findall(r"\*\*Q-([A-Z]{3})-\d\d\*\*", QBANK):
            counts[lens_code] = counts.get(lens_code, 0) + 1
        self.assertEqual(len(counts), 6, "expected core patterns for six lenses: %r" % counts)
        for code, n in counts.items():
            self.assertTrue(4 <= n <= 8, "%s has %d core patterns" % (code, n))

    def test_every_probe_states_a_trigger(self):
        probes = re.findall(r"\*\*P-[A-Z]{3}-\d\d\*\*(.{0,120})", QBANK, re.S)
        self.assertTrue(probes)
        for tail in probes:
            self.assertIn("Trigger:", tail, "probe without a trigger: %r" % tail[:60])

    def test_no_trigger_depends_on_a_judgement_the_su_cannot_hold(self):
        # A trigger must point at something observable, never at a computed verdict.
        triggers = re.findall(r"\*Trigger: (.+?)\*", QBANK)
        self.assertTrue(triggers)
        for trig in triggers:
            low = trig.lower()
            for banned in ("complexity is high", "is complex", "fit is", "score",
                           "is suitable", "is unsuitable"):
                self.assertNotIn(banned, low, "unobservable trigger: %r" % trig)

    def test_no_solution_is_named_or_implied(self):
        body = QBANK.split("\n", 1)[1].lower()  # the title carries the pack's own name
        for term in VENDOR_TERMS:
            self.assertNotIn(term, body, "question bank names %r" % term)

    def test_outcome_reachability_guard_survived(self):
        for phrase in ("another kind of technology is preferable",
                       "process change without new technology",
                       "doing nothing"):
            self.assertIn(phrase, QBANK.lower(), "missing reachable outcome: %r" % phrase)

    def test_no_question_economics_encoded_per_question(self):
        for token in ("custo:", "swing:", "criticidade:"):
            self.assertNotIn(token, QBANK, "%s duplicates SU/state reasoning" % token)


class TestGlossary(unittest.TestCase):
    def test_resolvable_and_split_in_two_parts(self):
        self.assertEqual(PACK["glossary"], "glossary.md")
        self.assertIn("# Part A", GLOSSARY)
        self.assertIn("# Part B", GLOSSARY)

    def test_part_a_is_technology_neutral(self):
        part_a = GLOSSARY.split("# Part A", 1)[1].split("# Part B", 1)[0].lower()
        for term in VENDOR_TERMS:
            self.assertNotIn(term, part_a, "Part A names %r" % term)

    def test_part_b_stays_quarantined(self):
        part_b = GLOSSARY.split("# Part B", 1)[1]
        self.assertIn("options+", part_b.lower())
        self.assertIn("NOT Discovery reasoning vocabulary", part_b)

    def test_definitions_carry_no_platform_number(self):
        part_a = GLOSSARY.split("# Part A", 1)[1].split("# Part B", 1)[0]
        # only word-numbers ("four shapes") are allowed; digits would be a platform figure
        self.assertNotRegex(part_a, r"\d[\d,.]*\s?(?:GB|MB|rows|records|items|seconds|s\b)")


class TestNoCanonicalIdsInRuntime(unittest.TestCase):
    def test_pack_runtime_files_carry_no_research_ids(self):
        for text, name in ((PACK_TEXT, "pack.yaml"), (QBANK, "question-bank.md"),
                           (GLOSSARY, "glossary.md")):
            self.assertEqual([], CANONICAL_ID.findall(text), "%s leaks research ids" % name)
            self.assertEqual([], GOV_RESEARCH_ID.findall(text), "%s leaks research ids" % name)

    def test_no_research_basis_lines(self):
        for text, name in ((PACK_TEXT, "pack.yaml"), (QBANK, "question-bank.md"),
                           (GLOSSARY, "glossary.md")):
            self.assertNotIn("Research basis", text, "%s carries research citations" % name)


class TestDegradation(unittest.TestCase):
    """Missing or empty cue/bank config must stay a no-op, not a round failure."""

    def test_round_and_council_state_the_degradation(self):
        for skill in ("aisa-round", "aisa-frame"):
            with open(os.path.join(ROOT, ".claude", "skills", skill, "SKILL.md"),
                      encoding="utf-8") as fh:
                text = fh.read()
            self.assertIn("extra_signals", text)
            self.assertIn("empty list", text, "%s does not state empty-signal degradation" % skill)
        # `aisa-options` inherits the resolution/degradation from `aisa-frame` step 4b.
        with open(os.path.join(ROOT, ".claude", "skills", "aisa-options", "SKILL.md"),
                  encoding="utf-8") as fh:
            options = fh.read()
        self.assertIn("extra_signals", options)
        self.assertIn("Identical to `aisa-frame` step 4b", options)

    def test_status_degrades_without_a_question_bank(self):
        with open(os.path.join(ROOT, ".claude", "skills", "aisa-status", "SKILL.md"),
                  encoding="utf-8") as fh:
            status = fh.read()
        self.assertIn("Degrade gracefully", status)

    def test_a_pack_with_no_lenses_config_injects_nothing(self):
        others = []
        packs_root = os.path.join(ROOT, "library", "packs")
        for name in sorted(os.listdir(packs_root)):
            manifest = os.path.join(packs_root, name, "pack.yaml")
            if name == "pp" or not os.path.exists(manifest):
                continue
            with open(manifest, encoding="utf-8") as fh:
                others.append((name, yaml.safe_load(fh) or {}))
        for name, doc in others:
            cfg = doc.get("lenses_config") or {}
            for lens in DISCOVERY:
                signals = (cfg.get(lens) or {}).get("extra_signals")
                self.assertTrue(
                    signals is None or isinstance(signals, list),
                    "%s.%s has a malformed extra_signals" % (name, lens),
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
