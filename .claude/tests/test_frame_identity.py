"""Frente E (P-18 / F05) — an approval approves a sentence, not a file.

The static counterexample of the 2026-09-08 adversarial review: F-01 is approved as
D-001; F-02 rewrites the sentence and is never approved; the session dies; `/options`
finds the old approval and proceeds on a sentence nobody approved. The gate could not
see it, because it only asked whether a `D-001` line existed.

The approval now carries `Frame sha256` — the fingerprint of the sentence it approved —
and `frame_identity` compares it with the sentence on file. The counterexample becomes
`verdict == "mismatch"` by construction.

Normalisation is part of the contract: quote markers, bold wrappers, horizontal rules,
CRLF and repeated whitespace are presentation and must not change the identity; the
words must. Three real heading shapes exist across the engagements, and the reader
handles all three — reading only the kernel's own would call a framed engagement
"no frame" and leave its approval unverifiable.

    python .claude/tests/test_frame_identity.py
"""

import runpy
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
D = runpy.run_path(str(ROOT / "library" / "kernel" / "tools" / "dashboard.py"))

SENTENCE = ("O problema é que o pricing corre num único ficheiro Excel, mantido por uma "
            "só pessoa, sem prova auditável do preço que sai.")
OTHER = ("O problema é que o pricing corre sem prova auditável do preço que sai, e "
         "depende de uma só pessoa para o reparar.")


def frame_md(sentence, heading="## Single problem sentence", style="quote", round_id="F-01"):
    body = {"quote": "> " + sentence,
            "bold": "**" + sentence + "**",
            "plain": sentence}[style]
    return ("# Frame — eng\n## Round: {}  | Phase: Framing\n\n{}\n\n{}\n\n"
            "## Anchors\n\n- cláusula → C-001\n").format(round_id, heading, body)


def approval(did, round_id, sha, supersedes=""):
    sup = supersedes or "—"
    return ("\n## {} — Frame agreed ({})\n\n"
            "- **Frame sentence**: uma frase qualquer escrita à mão no bloco\n"
            "- **Agreed in round**: {}\n"
            "- **Frame sha256**: {}\n"
            "- **Supersedes**: {}\n"
            "- **Validated by**: owner (dono do processo, via AskUserQuestion)\n"
            "- **Timestamp**: 2026-09-08T10:00:00Z\n").format(did, round_id, round_id, sha, sup)


LEGACY_APPROVAL = ("\n## D-001 — Frame agreed\n\n"
                   "- **Frame sentence**: a frase, em português, escrita no bloco\n"
                   "- **Agreed in round**: F-01\n"
                   "- **Timestamp**: 2026-05-29T09:00:00Z\n")


class Normalisation(unittest.TestCase):
    """Same words, different presentation -> same fingerprint."""

    def test_quote_bold_and_plain_are_the_same_sentence(self):
        shas = {style: D["frame_sha256"](D["frame_sentence"](frame_md(SENTENCE, style=style)))
                for style in ("quote", "bold", "plain")}
        self.assertEqual(len(set(shas.values())), 1, shas)
        self.assertTrue(all(len(v) == 64 for v in shas.values()))

    def test_crlf_extra_spaces_and_rules_do_not_change_it(self):
        base = D["frame_sha256"](D["frame_sentence"](frame_md(SENTENCE)))
        noisy = frame_md(SENTENCE).replace("\n", "\r\n").replace("> ", ">   ")
        noisy = noisy.replace("## Anchors", "---\n\n## Anchors")
        self.assertEqual(D["frame_sha256"](D["frame_sentence"](noisy)), base)

    def test_all_three_real_headings_are_read(self):
        for heading in ("## Single problem sentence", "### Frame sentence"):
            got = D["frame_sentence"](frame_md(SENTENCE, heading=heading))
            self.assertEqual(got, SENTENCE, heading)

    def test_different_words_are_a_different_sentence(self):
        a = D["frame_sha256"](D["frame_sentence"](frame_md(SENTENCE)))
        b = D["frame_sha256"](D["frame_sentence"](frame_md(OTHER)))
        self.assertNotEqual(a, b)

    def test_no_sentence_is_empty_not_the_hash_of_empty(self):
        self.assertEqual(D["frame_sentence"]("# Frame\n\n## Anchors\n"), "")
        self.assertEqual(D["frame_sha256"](""), "",
                         "an empty fingerprint must never be able to match an approval")


class Verdicts(unittest.TestCase):

    def _identity(self, frame_text, decisions_text):
        with tempfile.TemporaryDirectory() as tmp:
            eng = Path(tmp) / "eng"
            eng.mkdir()
            if frame_text is not None:
                (eng / "frame.md").write_text(frame_text, encoding="utf-8")
            (eng / "decisions.md").write_text(decisions_text, encoding="utf-8")
            blocks = D["classify_decisions"](decisions_text)
            return D["frame_identity"](eng, blocks), blocks

    def test_no_frame(self):
        ident, _ = self._identity(None, "")
        self.assertEqual(ident["verdict"], "no-frame")

    def test_none_when_nobody_approved(self):
        ident, _ = self._identity(frame_md(SENTENCE), "# Decisions\n")
        self.assertEqual(ident["verdict"], "none")
        self.assertIsNone(ident["latest"])

    def test_legacy_when_the_approval_predates_the_rule(self):
        ident, blocks = self._identity(frame_md(SENTENCE), LEGACY_APPROVAL)
        self.assertEqual(ident["verdict"], "legacy")
        self.assertTrue(blocks[0]["legacy"])

    def test_match(self):
        sha = D["frame_sha256"](SENTENCE)
        ident, _ = self._identity(frame_md(SENTENCE), approval("D-001", "F-01", sha))
        self.assertEqual(ident["verdict"], "match")

    def test_match_other_round_when_only_the_anchors_were_redone(self):
        sha = D["frame_sha256"](SENTENCE)
        ident, _ = self._identity(frame_md(SENTENCE, round_id="F-02"),
                                  approval("D-001", "F-01", sha))
        self.assertEqual(ident["verdict"], "match-other-round")

    def test_the_f05_counterexample_is_a_mismatch_by_construction(self):
        """F-01 approved; F-02 rewrote the sentence; the old approval must not cover it."""
        sha_f01 = D["frame_sha256"](SENTENCE)
        ident, _ = self._identity(frame_md(OTHER, round_id="F-02"),
                                  approval("D-001", "F-01", sha_f01))
        self.assertEqual(ident["verdict"], "mismatch")
        self.assertEqual(ident["latest"]["id"], "D-001")

    def test_approving_the_new_sentence_closes_it(self):
        sha_f01, sha_f02 = D["frame_sha256"](SENTENCE), D["frame_sha256"](OTHER)
        decisions = (approval("D-001", "F-01", sha_f01)
                     + approval("D-002", "F-02", sha_f02, supersedes="D-001 (frame F-01)"))
        ident, blocks = self._identity(frame_md(OTHER, round_id="F-02"), decisions)
        self.assertEqual(ident["verdict"], "match")
        self.assertEqual(ident["latest"]["id"], "D-002")
        index = {b["id"]: b for b in blocks}
        self.assertEqual(index["D-001"]["superseded_by"], "D-002",
                         "the reverse pointer is derived, never written into the file")
        self.assertEqual(index["D-002"]["supersedes"], "D-001")
        self.assertEqual(index["D-001"]["title"].count("Frame agreed"), 1,
                         "the superseded block is never edited")


class RealEngagementsStillParse(unittest.TestCase):
    """The four engagements with decisions predate the rule and must stay readable."""

    def test_existing_approvals_are_legacy_not_broken(self):
        projects = ROOT / "projects"
        seen = 0
        for slug in ("pricing-marinha-pilot-1", "kam-onboarding", "cae-automation",
                     "dpt-galp-jp"):
            eng = projects / slug
            if not (eng / "decisions.md").is_file():
                continue
            seen += 1
            blocks = D["classify_decisions"]((eng / "decisions.md").read_text(encoding="utf-8"))
            ident = D["frame_identity"](eng, blocks)
            self.assertEqual(ident["verdict"], "legacy", slug)
            self.assertTrue(ident["sentence"], slug + ": the sentence must be readable")
            self.assertEqual(len(ident["sha256"]), 64, slug)
        if seen == 0:
            self.skipTest("no engagements mounted")


if __name__ == "__main__":
    unittest.main(verbosity=2)
