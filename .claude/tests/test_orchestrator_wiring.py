"""Phase D — orchestrator wiring checks.

Asserts the contract the round/status skills declare, plus the one functional
mechanism they rely on (capture freshness by SHA-256). Deliberately small: no
orchestration test framework, no runtime driver, no fixture engagement beyond a
temp dir for the freshness check.

    python .claude/tests/test_orchestrator_wiring.py
"""

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DISCOVERY_LENSES = ("business", "operations", "user", "data", "governance", "financial")
TEXT_EXTRACT = os.path.join(ROOT, "library", "kernel", "tools", "text_extract.py")


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as fh:
        return fh.read()


ROUND = read(".claude", "skills", "aisa-round", "SKILL.md")
STATUS = read(".claude", "skills", "aisa-status", "SKILL.md")


class TestSharedEvidence(unittest.TestCase):
    """A round invocation can resolve the shared evidence index."""

    def test_round_carries_the_index_path(self):
        self.assertIn("_capture/evidence-index.md", ROUND)
        self.assertIn("Shared evidence:", ROUND)

    def test_index_absence_is_stated_never_assumed(self):
        self.assertIn("raw `inputs/` is the evidence surface", ROUND)

    def test_orchestrator_does_not_decide_relevance(self):
        self.assertIn("rank, assign, summarize or bundle sources", ROUND)
        self.assertIn("which of it matters is the lens's judgement", ROUND)

    def test_index_builder_exists_and_is_the_one_producer(self):
        self.assertTrue(os.path.isfile(TEXT_EXTRACT))
        capture = read(".claude", "skills", "aisa-capture", "SKILL.md")
        self.assertIn("--index", capture)


class TestPackSignalInjection(unittest.TestCase):
    """A Discovery lens receives the active pack's configured extra_signals."""

    @classmethod
    def setUpClass(cls):
        import yaml
        with open(os.path.join(ROOT, "library", "packs", "pp", "pack.yaml"), encoding="utf-8") as fh:
            cls.pack = yaml.safe_load(fh)

    def test_round_resolves_the_manifest_key(self):
        self.assertIn("lenses_config.<lens>.extra_signals", ROUND)
        self.assertIn("_state.json.pack", ROUND)

    def test_active_pack_declares_signals_for_every_discovery_lens(self):
        cfg = self.pack["lenses_config"]
        for lens in DISCOVERY_LENSES:
            signals = cfg[lens]["extra_signals"]
            self.assertTrue(signals, "%s has no extra_signals to inject" % lens)
            for token in signals:
                self.assertIsInstance(token, str)

    def test_injection_is_verbatim_no_scoring(self):
        self.assertIn("no scoring, no ranking, no filtering", ROUND)
        self.assertIn("no rewriting into questions", ROUND)

    def test_cues_are_not_coverage(self):
        self.assertIn("cues, not a checklist", ROUND)
        self.assertIn("an uncovered cue is not a gap and never becomes an `Unknown`", ROUND)

    def test_empty_or_absent_signals_degrade_gracefully(self):
        self.assertIn("inject nothing for that lens and continue", ROUND)
        self.assertIn("a lens works on its universal perspective without them", ROUND)
        self.assertIn("Omit the cue line entirely", ROUND)

    def test_technology_is_not_in_the_discovery_loop(self):
        self.assertIn("`lens-technology` is never invoked here", ROUND)
        self.assertIn("constraints_to_check", self.pack["lenses_config"]["technology"])


class TestDiscoveryPackBoundary(unittest.TestCase):
    """The Discovery lens itself still does not resolve pack.yaml."""

    def test_no_discovery_lens_reads_the_manifest(self):
        for lens in DISCOVERY_LENSES:
            body = read(".claude", "skills", "lens-" + lens, "SKILL.md")
            self.assertNotIn("pack.yaml", body, "lens-%s resolves the pack manifest" % lens)
            self.assertNotIn("library/packs/", body, "lens-%s reaches into the pack" % lens)

    def test_no_discovery_lens_loads_the_question_bank(self):
        for lens in DISCOVERY_LENSES:
            body = read(".claude", "skills", "lens-" + lens, "SKILL.md")
            self.assertNotIn("question-bank", body)
            self.assertNotIn("question_bank", body)


class TestQuestionBankConsumer(unittest.TestCase):
    """Exactly one selective consumer; never lens context."""

    def _resolvers(self):
        """Files that resolve the manifest key — i.e. actual consumers."""
        hits = set()
        for dirpath, _dirnames, filenames in os.walk(os.path.join(ROOT, ".claude")):
            if os.sep + "tests" in dirpath or "__pycache__" in dirpath:
                continue
            for name in filenames:
                if not name.endswith((".md", ".py", ".json")):
                    continue
                path = os.path.join(dirpath, name)
                with open(path, encoding="utf-8", errors="replace") as fh:
                    body = fh.read()
                if "question_bank" in body:
                    hits.add(os.path.relpath(path, ROOT).replace(os.sep, "/"))
        return hits

    def test_single_consumer(self):
        hits = self._resolvers()
        self.assertEqual(hits, {".claude/skills/aisa-status/SKILL.md"},
                         "unexpected question_bank resolvers: %s" % sorted(hits))

    def test_round_forbids_it_as_lens_context(self):
        # aisa-round names the bank only to keep it out of the launch context.
        self.assertIn("The pack's question bank is not lens context.", ROUND)
        self.assertIn("never enters a lens invocation", ROUND)
        self.assertNotIn("question_bank", ROUND)

    def test_consult_is_selective_and_not_coverage(self):
        self.assertIn("Selective, never exhaustive.", STATUS)
        self.assertIn("do not produce one question per Unknown", STATUS)
        self.assertIn("No scoring formula, no ranking engine.", STATUS)

    def test_consult_degrades_when_absent(self):
        self.assertIn("Degrade gracefully", STATUS)
        self.assertIn("build the agenda from the SU rows alone", STATUS)

    def test_bank_file_exists_for_the_active_pack(self):
        self.assertTrue(os.path.isfile(os.path.join(ROOT, "library", "packs", "pp", "question-bank.md")))


class TestFreshness(unittest.TestCase):
    """Changed .docx/.pdf/.vtt is detected by the existing capture mechanism."""

    def _sha256(self, path):
        with open(path, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()

    def _extract(self, src, out_md, out_json):
        cmd = [sys.executable, TEXT_EXTRACT, src, out_md, out_json]
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        return subprocess.run(cmd, capture_output=True, text=True, env=env)

    def test_round_covers_both_capture_tiers(self):
        self.assertIn("`.xlsx`/`.xlsm`", ROUND)
        self.assertIn("`.docx`/`.pdf`/`.vtt`", ROUND)
        self.assertIn("identity.sha256", ROUND)
        self.assertIn("hash/status only", ROUND)
        self.assertIn("never a semantic diff", ROUND)

    def test_changed_text_source_is_detected_by_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "notes.vtt")
            out_md = os.path.join(tmp, "notes.vtt.text.md")
            out_json = os.path.join(tmp, "notes.vtt.extraction.json")
            with open(src, "w", encoding="utf-8") as fh:
                fh.write("WEBVTT\n\n00:00:01.000 --> 00:00:03.000\n<v Ana>first version\n")
            self.assertEqual(self._extract(src, out_md, out_json).returncode, 0)

            with open(out_json, encoding="utf-8") as fh:
                identity = json.load(fh)["identity"]
            # fresh: the round's rule sees no drift
            self.assertEqual(identity["sha256"], self._sha256(src))

            with open(src, "a", encoding="utf-8") as fh:
                fh.write("\n00:00:04.000 --> 00:00:06.000\n<v Ana>a second passage\n")
            with open(out_json, encoding="utf-8") as fh:
                stale = json.load(fh)["identity"]["sha256"]
            # stale: the round's rule fires and re-capture is triggered
            self.assertNotEqual(stale, self._sha256(src))

            self.assertEqual(self._extract(src, out_md, out_json).returncode, 0)
            with open(out_json, encoding="utf-8") as fh:
                refreshed = json.load(fh)["identity"]["sha256"]
            self.assertEqual(refreshed, self._sha256(src))
            with open(out_md, encoding="utf-8") as fh:
                self.assertIn("a second passage", fh.read())

    def test_both_tiers_expose_the_same_identity_key(self):
        # one freshness rule covers both tiers only because the key matches
        for tool in ("xlsx_extract.py", "text_extract.py"):
            body = read("library", "kernel", "tools", tool)
            self.assertIn('"sha256"', body)


class TestInvocationCompactness(unittest.TestCase):
    """The launch context is pointers, not dumps."""

    def test_no_dump_rule_present(self):
        self.assertIn("**Do not dump.**", ROUND)
        tail = ROUND.split("**Do not dump.**", 1)[1][:600]
        for forbidden in ("`pack.yaml`", "`question-bank.md`", "domain-knowledge"):
            self.assertIn(forbidden, tail)

    def test_payload_names_the_required_context(self):
        block = re.search(r"Round: <R-NN>.*?```", ROUND, re.S)
        self.assertIsNotNone(block, "round context block missing")
        payload = block.group(0)
        for needed in ("shared-understanding.md", "next free ids", "context.json",
                       "Prior lens outputs", "evidence-index.md", "agent-memory",
                       "Pack attention cues"):
            self.assertIn(needed, payload)

    def test_orchestrator_does_no_domain_reasoning(self):
        self.assertIn("never what to conclude, which evidence matters, which cue is relevant, "
                      "or which state a finding should get", ROUND)


if __name__ == "__main__":
    unittest.main(verbosity=2)
