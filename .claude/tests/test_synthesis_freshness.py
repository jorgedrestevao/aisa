"""Frente E (P-18 / F04 + F08) — synthesis freshness per topic; the blueprint version a
deliverable reads is explicit.

The counterexample of the 2026-09-08 adversarial review (F04): five topics synthesised on
7/9, blueprint approved on 8/9 at 10h, `business-story` re-run at 11h. The motor took the
newest date of ANY topic, said "síntese posterior à aprovação" and recommended
`/render --all` while `architecture-story` still projected the pre-approval record.

Freshness is now judged PER TOPIC, against the authorities that topic consumes (the kernel
synthesis templates' `sources:`): the blueprint approval and the identity of the version
the architecture-story stamped, the SU rows a topic reads (day granularity), the decision
blocks. A pack with no log line is `desconhecido` -- never a positive claim.

F08: `blueprint_state` names the latest AUTHORIZED version (what the Architecture
Blueprint deliverable reads) next to the approved one (what the Specification and the
Design Brief read), and `--authority-stamp` prints the stamp aisa-synthesize writes.

    python .claude/tests/test_synthesis_freshness.py
"""

import io
import json
import runpy
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
D = runpy.run_path(str(ROOT / "library" / "kernel" / "tools" / "dashboard.py"))
TODAY = date(2026, 9, 9)
TOPICS = ["business-story", "as-is", "architecture-story", "risks-and-assumptions",
          "financial-story"]

SU_HEAD = """# Shared Understanding — {slug}

**Engagement**: {slug}
**Phase**: decision
**Pack**: pp
**Last updated**: 2026-09-08

"""
SU_COLS = {
    "Confirmed": "| id | lens | claim | evidência | verificado_em | validade | ronda |",
    "Assumed": "| id | lens | claim | base da assumption | verificado_em | validade | ronda |",
    "Unknown": "| id | lens | pergunta | quem responde | criticidade | custo | swing | ronda |",
    "Conflicted": "| id | lens | conflito | partes | criticidade | ronda |",
    "Risky": "| id | lens | risco | impacto | mitigação proposta | ronda |",
}

DECISIONS = """# Decisions

## D-001 — Frame agreed
- **Timestamp**: 2026-09-01T10:00:00Z

## D-002 — Adopt O-001
- **Chosen option**: O-001
- **Timestamp**: 2026-09-02T10:00:00Z

## D-003 — Blueprint bp-v01 aprovado
- **Timestamp**: 2026-09-08T10:00:00Z
"""

# A structurally VALID minimal blueprint: the freshness tests assume an approved
# version, and since 1.13.0 an approval over a version that fails bp_validate is not
# consumable (blueprint-contract.md -> Validação estrutural). Minimal, not empty.
BP_V01 = """version: v01
engagement: fx
decision_ref: decisions.md#D-002
draft: false
architecture:
  scope: whole solution
  authorization: authorized
  authorization_basis: "outcome sentence, verbatim (fixture)"
  architectability_basis: "PP application built from scratch (fixture)"
  experience:
    mode: owned-internal
    primary_surface: "Record-centric app (model-driven)"
  record_authority: []
  compositions: []
  relocated_responsibilities: []
  proof_obligations: []
  open_architecture_choices: []
entities: []
personas:
  - name: Analista
    su_refs: [C-001]
navigation:
  home: {Analista: S1}
screens:
  - name: S1
    type: gallery
    su_refs: [C-001]
excluded_from_ui:
  - field_or_area: "margem interna"
    reason: "sensível"
    su_refs: [C-001]
open_questions: []
validation:
  violations: []
"""


def write(eng, rel, body):
    p = eng / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")


def su_text(slug, sections=None):
    out = [SU_HEAD.format(slug=slug)]
    for name in ("Confirmed", "Assumed", "Unknown", "Conflicted", "Risky"):
        out.append("## " + name + "\n")
        out.append(SU_COLS[name])
        out.append("|" + "|".join(["---"] * (SU_COLS[name].count("|") - 1)) + "|")
        for cells in (sections or {}).get(name, []):
            out.append("| " + " | ".join(str(c) for c in cells) + " |")
        out.append("")
    return "\n".join(out) + "\n"


def log_lines(when, topics=TOPICS, extra=""):
    return "# Synthesis Log\n\n" + "".join(
        "{} — {} — sources: 1\n".format(when, t) for t in topics) + extra


def mk(tmp, slug="fx", files=None, sections=None, decisions=DECISIONS, blueprints=None,
       packs=TOPICS, log=None):
    eng = Path(tmp) / slug
    eng.mkdir(parents=True, exist_ok=True)
    write(eng, "_state.json", json.dumps({
        "engagement": slug, "pack": "pp", "phase": "decision", "round": "D-01",
        "created": "2026-09-01T10:00:00Z"}))
    write(eng, "context.json", json.dumps({"literal_request": "x",
                                           "requester": {"name": "n", "role": "r"}}))
    write(eng, "shared-understanding.md", su_text(slug, sections))
    write(eng, "frame.md", "# Frame\n")
    write(eng, "options.md", "# Options\n")
    write(eng, "decisions.md", decisions)
    for ver, body in (blueprints if blueprints is not None else {"v01": BP_V01}).items():
        write(eng, "_blueprint/ux-blueprint_{}.yaml".format(ver), body)
    for t in packs:
        write(eng, "_synthesis/{}.md".format(t), "# {}\nOld content\n".format(t))
    if log is not None:
        write(eng, "_synthesis/_synthesis-log.md", log)
    for rel, body in (files or {}).items():
        write(eng, rel, body)
    return eng


def model(eng):
    return D["build_model"](eng, TODAY)


class Harness(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = self._tmp.name

    def tearDown(self):
        self._tmp.cleanup()


class F04Counterexample(Harness):
    """The review's scenario, inverted by construction."""

    def _eng(self):
        return mk(self.tmp, log=log_lines("2026-09-07T09:00:00Z") +
                  "2026-09-08T11:00:00Z — business-story — sources: 1\n",
                  files={"_synthesis/business-story.md": "# Business story\nFresh\n"})

    def test_one_fresh_topic_does_not_mask_the_stale_architecture_story(self):
        syn = model(self._eng())["status"]["synthesis"]
        self.assertEqual(syn["topics"]["business-story"]["verdict"], "fresh")
        self.assertEqual(syn["topics"]["architecture-story"]["verdict"], "stale")
        self.assertIn("architecture-story", syn["stale_topics"])
        self.assertTrue(syn["stale_vs_approval"])
        self.assertEqual(syn["verdict"], "stale")

    def test_the_milestone_refuses_the_render_and_names_the_topics(self):
        ms = model(self._eng())["status"]["milestone"]
        self.assertNotEqual(ms["command"], "/render --all")
        self.assertTrue(ms["command"].startswith("/synthesize"))
        self.assertIn("architecture-story", ms["blocking"])
        self.assertIn("architecture-story", ms["text"])

    def test_a_topic_that_consumes_decisions_is_stale_after_a_new_decision_block(self):
        # risks-and-assumptions and financial-story read decisions.md; D-003 (the
        # approval) was appended after their run, so they are stale too -- honestly.
        syn = model(self._eng())["status"]["synthesis"]
        for t in ("risks-and-assumptions", "financial-story"):
            self.assertEqual(syn["topics"][t]["verdict"], "stale", t)
            self.assertTrue(any(r.startswith("decisions") for r in syn["topics"][t]["reasons"]))

    def test_as_is_with_nothing_stamped_after_it_is_fresh_by_absence_of_counterevidence(self):
        syn = model(self._eng())["status"]["synthesis"]
        t = syn["topics"]["as-is"]
        self.assertEqual(t["verdict"], "fresh")
        self.assertEqual(t["comparable"], 0)
        self.assertIn("ausência de contra-evidência", t["julgamento"])


class Release(Harness):

    def test_all_five_fresh_after_the_approval_releases_the_deliverables(self):
        eng = mk(self.tmp, log=log_lines("2026-09-08T12:00:00Z"))
        st = model(eng)["status"]
        self.assertEqual(st["synthesis"]["verdict"], "fresh")
        self.assertEqual(st["synthesis"]["stale_topics"], [])
        self.assertFalse(st["synthesis"]["stale_vs_approval"])
        self.assertEqual(st["milestone"]["command"], "/render --all")

    def test_single_stale_topic_gets_a_targeted_command(self):
        log = log_lines("2026-09-08T12:00:00Z", [t for t in TOPICS if t != "architecture-story"])
        log += "2026-09-07T09:00:00Z — architecture-story — sources: 1\n"
        ms = model(mk(self.tmp, log=log))["status"]["milestone"]
        self.assertEqual(ms["command"], "/synthesize architecture-story")


class UnknownIsNeverPositive(Harness):

    def test_no_log_at_all_is_desconhecido_not_fresh(self):
        st = model(mk(self.tmp, log=None))["status"]
        syn = st["synthesis"]
        self.assertTrue(syn["present"])
        self.assertEqual(syn["verdict"], "desconhecido")
        self.assertEqual(sorted(syn["unknown_topics"]), sorted(TOPICS))
        self.assertIsNone(syn["stale_vs_approval"])
        self.assertNotEqual(st["milestone"]["command"], "/render --all")
        self.assertIn("verificação incompleta", st["milestone"]["marco"])

    def test_a_pack_without_its_own_log_line_is_unknown_even_if_others_are_fresh(self):
        log = log_lines("2026-09-08T12:00:00Z", [t for t in TOPICS if t != "financial-story"])
        syn = model(mk(self.tmp, log=log))["status"]["synthesis"]
        self.assertEqual(syn["topics"]["financial-story"]["verdict"], "desconhecido")
        self.assertEqual(syn["unknown_topics"], ["financial-story"])
        self.assertIn("nada se afirma", syn["topics"]["financial-story"]["julgamento"])

    def test_a_missing_pack_is_missing(self):
        packs = [t for t in TOPICS if t != "as-is"]
        syn = model(mk(self.tmp, packs=packs, log=log_lines("2026-09-08T12:00:00Z")))["status"]["synthesis"]
        self.assertEqual(syn["topics"]["as-is"]["verdict"], "missing")
        self.assertIn("as-is", syn["unknown_topics"])

    def test_no_approval_yet_makes_no_approval_claim(self):
        dec = DECISIONS.split("## D-003")[0]
        syn = model(mk(self.tmp, decisions=dec, log=log_lines("2026-09-08T12:00:00Z")))["status"]["synthesis"]
        self.assertIsNone(syn["stale_vs_approval"])
        self.assertEqual(syn["approval_id"], "")


class Identity(Harness):
    """The architecture-story names the version it projected; a clock cannot hide it."""

    def _two_versions(self):
        v02 = BP_V01.replace("version: v01", "version: v02").replace(
            "  scope: whole solution", "  scope: whole solution\n  note: changed")
        dec = DECISIONS + "\n## D-004 — Blueprint bp-v02 aprovado\n- **Timestamp**: 2026-09-08T10:30:00Z\n"
        return v02, dec

    def test_a_stamp_naming_another_version_is_stale_whatever_the_clock_says(self):
        v02, dec = self._two_versions()
        eng = mk(self.tmp, decisions=dec, blueprints={"v01": BP_V01, "v02": v02},
                 log=log_lines("2026-09-08T12:00:00Z"),
                 files={"_synthesis/architecture-story.md":
                        "# Architecture Story\n<!-- authority: _blueprint/ux-blueprint_v01.yaml"
                        "#architecture -->\nbody\n"})
        syn = model(eng)["status"]["synthesis"]
        t = syn["topics"]["architecture-story"]
        self.assertEqual(t["identity"], "mismatch")
        self.assertEqual(t["verdict"], "stale")
        self.assertTrue(any(r.startswith("identidade") for r in t["reasons"]))
        self.assertTrue(syn["stale_vs_approval"])

    def test_a_matching_stamp_with_the_right_sha_is_fresh(self):
        eng = mk(self.tmp, log=log_lines("2026-09-08T12:00:00Z"))
        sha = D["architecture_block_sha256"](BP_V01)
        write(eng, "_synthesis/architecture-story.md",
              "# Architecture Story\n<!-- authority: _blueprint/ux-blueprint_v01.yaml"
              "#architecture @ sha256:{} -->\nbody\n".format(sha))
        t = model(eng)["status"]["synthesis"]["topics"]["architecture-story"]
        self.assertEqual(t["identity"], "match")
        self.assertEqual(t["verdict"], "fresh")
        self.assertEqual(t["stamp"]["sha256"], sha)

    def test_a_changed_architecture_block_under_the_same_version_is_stale_by_sha(self):
        eng = mk(self.tmp, log=log_lines("2026-09-08T12:00:00Z"))
        old_sha = D["architecture_block_sha256"](BP_V01.replace("owned-internal", "none"))
        write(eng, "_synthesis/architecture-story.md",
              "# Architecture Story\n<!-- authority: _blueprint/ux-blueprint_v01.yaml"
              "#architecture @ sha256:{} -->\nbody\n".format(old_sha))
        t = model(eng)["status"]["synthesis"]["topics"]["architecture-story"]
        self.assertEqual(t["identity"], "mismatch")
        self.assertTrue(any("sha256" in r for r in t["reasons"]))

    def test_the_version_cited_in_the_log_line_is_the_fallback_identity(self):
        v02, dec = self._two_versions()
        log = log_lines("2026-09-08T12:00:00Z", [t for t in TOPICS if t != "architecture-story"])
        log += ("2026-09-08T12:00:00Z — architecture-story (re-síntese, manual) — sources: "
                "_blueprint/ux-blueprint_v01.yaml#architecture (versão APROVADA)\n")
        eng = mk(self.tmp, decisions=dec, blueprints={"v01": BP_V01, "v02": v02}, log=log)
        t = model(eng)["status"]["synthesis"]["topics"]["architecture-story"]
        self.assertEqual(t["runs"], 1, "a topic token with a suffix is still the topic")
        self.assertEqual(t["identity"], "mismatch")

    def test_no_stamp_and_no_citation_is_sem_carimbo_not_a_mismatch(self):
        t = model(mk(self.tmp, log=log_lines("2026-09-08T12:00:00Z")))["status"]["synthesis"]["topics"]["architecture-story"]
        self.assertEqual(t["identity"], "sem carimbo")
        self.assertEqual(t["verdict"], "fresh")


class BlockFingerprint(unittest.TestCase):

    def test_presentation_does_not_change_the_fingerprint(self):
        a = D["architecture_block_sha256"](BP_V01)
        noisy = BP_V01.replace("\n", "\r\n").replace("authorized\r\n", "authorized   \r\n")
        self.assertEqual(D["architecture_block_sha256"](noisy), a)
        self.assertEqual(len(a), 64)

    def test_the_block_stops_at_the_next_top_level_key(self):
        blk = D["architecture_block_text"](BP_V01)
        self.assertIn("authorization: authorized", blk)
        self.assertNotIn("entities", blk)

    def test_words_change_it_and_no_block_is_empty(self):
        self.assertNotEqual(D["architecture_block_sha256"](BP_V01),
                            D["architecture_block_sha256"](BP_V01.replace("authorized", "authorized-bounded")))
        self.assertEqual(D["architecture_block_sha256"]("version: v01\nentities: []\n"), "")


class SuAndLogShapes(Harness):

    def test_a_business_row_verified_after_the_run_makes_business_story_stale(self):
        eng = mk(self.tmp, log=log_lines("2026-09-08T12:00:00Z"), sections={
            "Confirmed": [["C-001", "business", "c", "e", "2026-09-09", "organizacional", "R-01"],
                          ["C-002", "operations", "c", "e", "2026-09-09", "organizacional", "R-01"]]})
        syn = model(eng)["status"]["synthesis"]
        self.assertEqual(syn["topics"]["business-story"]["verdict"], "stale")
        self.assertEqual(syn["topics"]["as-is"]["verdict"], "stale")
        self.assertEqual(syn["topics"]["financial-story"]["verdict"], "fresh",
                         "a row of another lens is not this topic's authority")

    def test_same_day_is_not_stale_the_su_carries_dates_not_times(self):
        eng = mk(self.tmp, log=log_lines("2026-09-08T12:00:00Z"), sections={
            "Confirmed": [["C-001", "business", "c", "e", "2026-09-08", "organizacional", "R-01"]]})
        self.assertEqual(model(eng)["status"]["synthesis"]["topics"]["business-story"]["verdict"], "fresh")

    def test_the_table_shaped_log_of_dpt_galp_jp_is_read(self):
        log = ("# Synthesis Log — x\n\n## Run 1 — 2026-09-08T12:00:00Z\n\n"
               "| topic | sources | SU ids cited | paragraphs | warnings |\n|---|---|---|---|---|\n"
               + "".join("| {} | s | C-001 | 5 | — |\n".format(t) for t in TOPICS))
        syn = model(mk(self.tmp, log=log))["status"]["synthesis"]
        self.assertEqual(len(syn["log_entries"]), 5)
        self.assertEqual(syn["verdict"], "fresh")

    def test_sources_come_from_the_kernel_templates(self):
        for t in TOPICS:
            srcs, basis = D["synthesis_template_sources"](t)
            self.assertEqual(basis, "template", t)
            self.assertTrue(srcs, t)
        arch, _ = D["synthesis_template_sources"]("architecture-story")
        self.assertTrue(any(s.startswith("_blueprint/") for s in arch))
        self.assertEqual(D["synthesis_template_sources"]("no-such-topic"), ([], "fallback"))


class F08LatestAuthorized(Harness):

    def test_latest_authorized_is_named_next_to_the_approved_version(self):
        v02 = BP_V01.replace("version: v01", "version: v02").replace(
            "  open_architecture_choices: []",
            "  open_architecture_choices:\n    - choice: store\n      structural: true\n      su_refs: [U-001]")
        bp = model(mk(self.tmp, blueprints={"v01": BP_V01, "v02": v02},
                      log=log_lines("2026-09-08T12:00:00Z")))["status"]["blueprint"]
        self.assertEqual(bp["approved"]["version"], "v01")
        self.assertEqual(bp["latest_authorized"]["version"], "v02")
        self.assertFalse(bp["latest_authorized"]["approved"])
        self.assertEqual(bp["latest_authorized"]["structural_open_count"], 1)
        self.assertIn("structural choice(s) open", bp["latest_authorized"]["state"])

    def test_drafts_and_unauthorized_versions_are_never_the_latest_authorized(self):
        v02 = BP_V01.replace("version: v01", "version: v02").replace("authorization: authorized",
                                                                    "authorization: not-authorized")
        v03 = BP_V01.replace("version: v01", "version: v03\ndraft: true\noption: O-002")
        bp = model(mk(self.tmp, blueprints={"v01": BP_V01, "v02": v02, "v03": v03},
                      log=log_lines("2026-09-08T12:00:00Z")))["status"]["blueprint"]
        self.assertEqual(bp["latest_authorized"]["version"], "v01")
        self.assertTrue(bp["latest_authorized"]["approved"])
        self.assertTrue(bp["latest_authorized"]["state"].startswith("approved (D-003)"))

    def test_no_blueprint_means_no_latest_authorized(self):
        eng = mk(self.tmp, blueprints={}, log=log_lines("2026-09-08T12:00:00Z"))
        (eng / "_blueprint").mkdir(exist_ok=True)
        self.assertIsNone(model(eng)["status"]["blueprint"]["latest_authorized"])


class AuthorityStampCli(Harness):

    def _run(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            rc = D["main"](list(argv))
        return rc, out.getvalue().strip(), err.getvalue().strip()

    def test_prints_the_stamp_of_the_approved_version(self):
        eng = mk(self.tmp, log=log_lines("2026-09-08T12:00:00Z"))
        rc, out, _ = self._run("--engagement", str(eng), "--authority-stamp", "--quiet")
        self.assertEqual(rc, 0)
        self.assertEqual(out, "authority: _blueprint/ux-blueprint_v01.yaml#architecture @ sha256:"
                         + D["architecture_block_sha256"](BP_V01))
        stamp = D["synthesis_stamp"]("# x\n<!-- " + out + " -->\n")
        self.assertEqual(stamp["version"], "v01")

    def test_an_explicit_version_wins_and_a_missing_one_fails_loud(self):
        v02 = BP_V01.replace("version: v01", "version: v02")
        eng = mk(self.tmp, blueprints={"v01": BP_V01, "v02": v02}, log=log_lines("2026-09-08T12:00:00Z"))
        rc, out, _ = self._run("--engagement", str(eng), "--authority-stamp", "2", "--quiet")
        self.assertEqual(rc, 0)
        self.assertIn("ux-blueprint_v02.yaml", out)
        rc, _, err = self._run("--engagement", str(eng), "--authority-stamp", "v09", "--quiet")
        self.assertEqual(rc, 3)
        self.assertIn("sem bloco architecture", err)


if __name__ == "__main__":
    unittest.main(verbosity=1)
