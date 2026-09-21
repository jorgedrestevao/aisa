"""Frente E (P-15) — a round in progress is not a completed round; a single lens runs free.

Inverts two reproductions of the 2026-09-08 adversarial review
(`docs/ADVERSARIAL_REVIEW_2026-09-08.md`, `docs/review-evidence/`):

  P-R6  `docs/review-evidence/repro-round-order.py` asserted `[0, 2]`: with the
        round already stamped as completed, the second single-lens `/round`
        dead-ended. The guard now reads `round_in_progress`, so the same
        sequence passes — the assertion here is the inverted one.

  guard engagement resolution (found in operation, two copies of pilot-3 in a
        simultaneous round): the lens invocation declares ``engagement root
        `<path>``` and the guard must check THAT engagement, not the most
        recently touched one.

The contract itself lives in `library/kernel/phases.md` (*Rounds — in progress
vs completed*); `aisa-round` step 3/5a writes it, this hook and `dashboard.py`
read it.

    python .claude/tests/test_round_in_progress.py
"""

import contextlib
import io
import json
import os
import runpy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / ".claude" / "hooks" / "pre-lens-order-check.py"
DASHBOARD = ROOT / "library" / "kernel" / "tools" / "dashboard.py"
ROUND_SKILL = ROOT / ".claude" / "skills" / "aisa-round" / "SKILL.md"
START_SKILL = ROOT / ".claude" / "skills" / "aisa-start" / "SKILL.md"
PHASES = ROOT / "library" / "kernel" / "phases.md"


def load_hook():
    """Fresh module namespace per call — the guard exits via SystemExit."""
    return runpy.run_path(str(HOOK))


def run_guard(lens, engagements_root, args=None):
    """Invoke the real guard on a real on-disk engagement tree.

    Returns (exit_code, stderr). 0 = allowed, 2 = blocked.
    """
    payload = {"tool_name": "Skill", "tool_input": {"skill": f"lens-{lens}"}}
    if args is not None:
        payload["tool_input"]["args"] = args
    stderr = io.StringIO()
    env = dict(os.environ, AISA_ENGAGEMENTS_ROOT=str(engagements_root))
    with patch.dict(os.environ, env, clear=False), \
            patch.object(sys, "stdin", io.StringIO(json.dumps(payload))), \
            contextlib.redirect_stderr(stderr):
        try:
            code = load_hook()["main"]()
        except SystemExit as error:
            code = error.code
    return code, stderr.getvalue()


def make_engagement(base, slug, *, round_done="R-00", in_progress="",
                    lens_outputs=None, phase="discovery", round_lenses=None):
    eng = Path(base) / slug
    (eng / "lens-outputs").mkdir(parents=True, exist_ok=True)
    state = {"engagement": slug, "phase": phase, "round": round_done}
    if in_progress:
        state["round_in_progress"] = in_progress
    if round_lenses is not None:
        state["round_lenses"] = round_lenses
    (eng / "_state.json").write_text(json.dumps(state), encoding="utf-8")
    (eng / "shared-understanding.md").write_text("# SU\n", encoding="utf-8")
    for lens, stamped in (lens_outputs or {}).items():
        (eng / "lens-outputs" / f"{lens}.md").write_text(
            f"## {stamped} - {lens}\nFindings.\n", encoding="utf-8")
    return eng


class SingleLensSequence(unittest.TestCase):
    """P-R6 inverted: `/round business` then `/round operations` must both run."""

    def test_open_round_lets_the_next_lens_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            # business ran inside the open R-01; the round did NOT close, so
            # `round` still says R-00.
            make_engagement(tmp, "eng", round_done="R-00", in_progress="R-01",
                            lens_outputs={"business": "R-01"})
            code, err = run_guard("operations", tmp)
        self.assertEqual(code, 0, f"open round R-01 must not block operations: {err}")

    def test_the_defect_shape_still_blocks_without_an_open_round(self):
        """The old state shape (round closed at R-01, nothing open) is exactly
        the dead end the review found — and the guard must still block there,
        because R-02's business output genuinely does not exist."""
        with tempfile.TemporaryDirectory() as tmp:
            make_engagement(tmp, "eng", round_done="R-01",
                            lens_outputs={"business": "R-01"})
            code, err = run_guard("operations", tmp)
        self.assertEqual(code, 2)
        self.assertIn("R-02", err)

    def test_stale_in_progress_is_ignored(self):
        """`round_in_progress` behind `round` is a leftover, not an open round."""
        with tempfile.TemporaryDirectory() as tmp:
            make_engagement(tmp, "eng", round_done="R-02", in_progress="R-01",
                            lens_outputs={"business": "R-02"})
            code, err = run_guard("operations", tmp)
        self.assertEqual(code, 2)
        self.assertIn("R-03", err, "stale value must not be trusted as the open round")

    def test_missing_previous_lens_still_blocks_in_an_open_round(self):
        """The order rule survives the fix: an open round is not a free pass."""
        with tempfile.TemporaryDirectory() as tmp:
            make_engagement(tmp, "eng", round_done="R-00", in_progress="R-01")
            code, err = run_guard("operations", tmp)
        self.assertEqual(code, 2)
        self.assertIn("lens-business", err)

    def test_business_is_always_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            make_engagement(tmp, "eng", round_done="R-00")
            code, _ = run_guard("business", tmp)
        self.assertEqual(code, 0)


class EngagementResolution(unittest.TestCase):
    """Two copies in a simultaneous round: the declared root decides."""

    def _two_copies(self, tmp):
        # `ready` has business stamped for the open round; `behind` has nothing.
        make_engagement(tmp, "pilot-3-val-opus", round_done="R-00",
                        in_progress="R-01", lens_outputs={"business": "R-01"})
        make_engagement(tmp, "pilot-3-val-sonnet", round_done="R-00",
                        in_progress="R-01")

    def test_declared_root_wins_over_most_recently_touched(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._two_copies(tmp)
            args = (f"Round: R-01 - engagement `pilot-3-val-opus` - "
                    f"engagement root `{Path(tmp) / 'pilot-3-val-opus'}`\n"
                    "Shared Understanding: ...")
            code, err = run_guard("operations", tmp, args=args)
        self.assertEqual(code, 0, f"the declared engagement has business for R-01: {err}")

    def test_declared_root_blocks_when_that_copy_is_behind(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._two_copies(tmp)
            args = ("Round: R-01 - engagement `pilot-3-val-sonnet` - "
                    f"engagement root `{Path(tmp) / 'pilot-3-val-sonnet'}`")
            code, err = run_guard("operations", tmp, args=args)
        self.assertEqual(code, 2)
        self.assertIn("lens-business", err)

    def test_unknown_root_falls_back_instead_of_blocking(self):
        with tempfile.TemporaryDirectory() as tmp:
            make_engagement(tmp, "eng", round_done="R-00", in_progress="R-01",
                            lens_outputs={"business": "R-01"})
            args = "engagement root `Z:/does/not/exist`"
            code, _ = run_guard("operations", tmp, args=args)
        self.assertEqual(code, 0, "a bogus root must not decide anything by itself")

    def test_engagement_outside_discovery_is_not_policed(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make_engagement(tmp, "eng", round_done="F-01", phase="framing")
            code, _ = run_guard("operations", tmp,
                                args=f"engagement root `{eng}`")
        self.assertEqual(code, 0)


class SingleLensIsFree(unittest.TestCase):
    """`/round <lens>` runs any lens alone, in any order (F1 of the 2026-09-09 review).

    The invocation carries ``round mode: single``; the guard stands aside. The
    marker is fail-closed: absent, the full-round order is enforced as before.
    """

    def test_single_mode_runs_any_lens_without_prerequisite(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make_engagement(tmp, "eng", round_done="R-00", in_progress="R-01")
            args = (f"Round: R-01 - engagement `eng` - engagement root `{eng}` - "
                    "round mode: single")
            for lens in ("financial", "data", "governance"):
                code, err = run_guard(lens, tmp, args=args)
                self.assertEqual(code, 0, f"{lens} alone must run: {err}")

    def test_marker_absent_is_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make_engagement(tmp, "eng", round_done="R-00", in_progress="R-01")
            args = f"Round: R-01 - engagement root `{eng}` - round mode: full"
            code, err = run_guard("data", tmp, args=args)
        self.assertEqual(code, 2)
        self.assertIn("lens-business", err)

    def test_full_mode_marker_still_enforces(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make_engagement(tmp, "eng", round_done="R-00", in_progress="R-01",
                                  lens_outputs={"business": "R-01"})
            args = f"engagement root `{eng}` - round mode: full"
            code, _ = run_guard("operations", tmp, args=args)
            self.assertEqual(code, 0)
            code, err = run_guard("user", tmp, args=args)
        self.assertEqual(code, 2)
        self.assertIn("lens-operations", err)


class SingleIsAuthorisedByState(unittest.TestCase):
    """The isolation signal is `_state.json.round_lenses`, not prose.

    Regression for the 2026-09-09 operational failure: `/round data` on
    `pricing-bunkers` R-03 was refused because the invocation text did not
    carry the marker the skill was supposed to type. The record `/round`
    writes in step 3c is machine-set and scoped to the round AND the lens, so
    it authorises exactly one thing and a leftover authorises nothing.
    """

    SINGLE = {"ronda": "R-03", "modo": "single", "lentes": ["data"]}

    def _guard(self, lens, record, *, in_progress="R-03", round_done="R-02"):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make_engagement(tmp, "eng", round_done=round_done,
                                  in_progress=in_progress, round_lenses=record)
            return run_guard(lens, tmp, args="engagement root `%s`" % eng)

    def test_state_alone_authorises_the_named_lens(self):
        code, err = self._guard("data", self.SINGLE)
        self.assertEqual(code, 0, "round_lenses must authorise data: %s" % err)

    def test_record_does_not_authorise_another_lens(self):
        code, err = self._guard("governance", self.SINGLE)
        self.assertEqual(code, 2)
        self.assertIn("lens-business", err)

    def test_record_from_another_round_authorises_nothing(self):
        code, err = self._guard("data", {"ronda": "R-02", "modo": "single",
                                         "lentes": ["data"]})
        self.assertEqual(code, 2)
        self.assertIn("R-03", err)

    def test_full_mode_record_still_enforces_the_order(self):
        code, err = self._guard("data", {"ronda": "R-03", "modo": "full",
                                         "lentes": ["business", "data"]})
        self.assertEqual(code, 2)
        self.assertIn("lens-business", err)

    def test_absent_or_malformed_record_is_fail_closed(self):
        for record in (None, {}, {"ronda": "R-03", "modo": "single"},
                       {"ronda": "R-03", "modo": "single", "lentes": "data"}):
            code, _ = self._guard("data", record)
            self.assertEqual(code, 2, record)

    def test_the_pricing_bunkers_repro(self):
        """R-03 open, nothing stamped, `/round data`: refused before, runs now."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = make_engagement(tmp, "pricing-bunkers", round_done="R-02",
                                  in_progress="R-03",
                                  lens_outputs={"business": "R-02"})
            args = "engagement root `%s`" % eng
            self.assertEqual(run_guard("data", tmp, args=args)[0], 2,
                             "without the record the order is policed")
            state = json.loads((eng / "_state.json").read_text(encoding="utf-8"))
            state["round_lenses"] = {"ronda": "R-03", "modo": "single",
                                     "lentes": ["data"]}
            (eng / "_state.json").write_text(json.dumps(state), encoding="utf-8")
            code, err = run_guard("data", tmp, args=args)
        self.assertEqual(code, 0, "`/round data` must run in R-03: %s" % err)


class OutputIsAHeaderNotASubstring(unittest.TestCase):
    """F4: "wrote for R-02" means a `## R-02 …` heading, never a body mention."""

    def test_body_mention_does_not_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make_engagement(tmp, "eng", round_done="R-01", in_progress="R-02")
            (eng / "lens-outputs" / "business.md").write_text(
                "## R-01 - business\nCompared with what R-02 will need.\n",
                encoding="utf-8")
            code, err = run_guard("operations", tmp)
        self.assertEqual(code, 2)
        self.assertIn("R-02", err)

    def test_legacy_header_shapes_count(self):
        dash = runpy.run_path(str(DASHBOARD))
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "x.md"
            for header in ("## R-02 — business", "## R-02 (2026-05-29)", "## R-02 — 2026-05-28"):
                f.write_text(header + "\n", encoding="utf-8")
                self.assertTrue(dash["lens_wrote_round"](f, "R-02"), header)
            f.write_text("## R-020 — business\n", encoding="utf-8")
            self.assertFalse(dash["lens_wrote_round"](f, "R-02"), "R-020 is not R-02")


class MotorNamesTheMissingLenses(unittest.TestCase):
    """F5: which lenses stamped the open passagem is a fact the motor publishes."""

    def setUp(self):
        self.dash = runpy.run_path(str(DASHBOARD))

    def test_out_of_order_subset(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make_engagement(tmp, "eng", round_done="R-00", in_progress="R-01",
                                  lens_outputs={"financial": "R-01", "data": "R-01"})
            got = self.dash["lenses_for_round"](eng, "R-01")
        self.assertEqual(got["corridas"], ["data", "financial"])
        self.assertEqual(got["em_falta"], ["business", "operations", "user", "governance"])

    def test_all_six_means_nothing_missing(self):
        lenses = ["business", "operations", "user", "data", "governance", "financial"]
        with tempfile.TemporaryDirectory() as tmp:
            eng = make_engagement(tmp, "eng", round_done="R-00", in_progress="R-01",
                                  lens_outputs={l: "R-01" for l in lenses})
            got = self.dash["lenses_for_round"](eng, "R-01")
        self.assertEqual(got["em_falta"], [])

    def test_no_open_round_is_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make_engagement(tmp, "eng", round_done="R-01")
            self.assertEqual(self.dash["lenses_for_round"](eng, ""),
                             {"ronda": "", "corridas": [], "em_falta": []})

    def test_model_publishes_the_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make_engagement(tmp, "eng", round_done="R-00", in_progress="R-01",
                                  lens_outputs={"user": "R-01"})
            (eng / "context.json").write_text("{}", encoding="utf-8")
            from datetime import date
            model = self.dash["build_model"](eng, date(2026, 9, 9))
        self.assertEqual(model["engagement"]["lentes_ronda_aberta"]["corridas"], ["user"])


class MotorReadsTheOpenRound(unittest.TestCase):
    """dashboard.py publishes it, with the same staleness rule as the guard."""

    def setUp(self):
        self.dash = runpy.run_path(str(DASHBOARD))

    def test_open_round_published(self):
        self.assertEqual(
            self.dash["_open_round"]({"round": "R-01", "round_in_progress": "R-02"}),
            "R-02")

    def test_stale_and_absent_are_both_empty(self):
        for state in ({"round": "R-02", "round_in_progress": "R-01"},
                      {"round": "R-02", "round_in_progress": "R-02"},
                      {"round": "R-02"},
                      {"round": "R-02", "round_in_progress": ""}):
            self.assertEqual(self.dash["_open_round"](state), "", state)


class ContractIsWritten(unittest.TestCase):
    """The rule lives in the kernel and the skills that write the state."""

    def test_phases_declares_the_two_fields(self):
        text = PHASES.read_text(encoding="utf-8")
        self.assertIn("round_in_progress", text)
        self.assertIn("A round in progress is not a completed round.", text)

    def test_start_seeds_the_field(self):
        self.assertIn('"round_in_progress": ""',
                      START_SKILL.read_text(encoding="utf-8"))

    def test_round_opens_closes_and_offers_close(self):
        text = ROUND_SKILL.read_text(encoding="utf-8")
        self.assertIn("--close", text)
        self.assertIn("round_in_progress", text)
        self.assertIn("`round_in_progress` = `\"\"`", text)

    def test_round_declares_single_mode_and_asks_before_rerun(self):
        text = ROUND_SKILL.read_text(encoding="utf-8")
        self.assertIn("round mode: <full|single>", text)
        self.assertIn("lentes_ronda_aberta", text)
        self.assertIn("Passagem guard", text)
        self.assertNotIn("last of the order** (`financial`)", text,
                         "closing on `financial` breaks single-lens rounds")

    def test_phases_and_hooks_doc_name_the_state_record(self):
        self.assertIn("round_lenses", PHASES.read_text(encoding="utf-8"))
        hooks = (ROOT / ".claude" / "hooks" / "HOOKS.md").read_text(encoding="utf-8")
        self.assertIn("round_lenses", hooks)

    def test_round_writes_and_clears_the_record(self):
        text = ROUND_SKILL.read_text(encoding="utf-8")
        self.assertIn("round_lenses", text)
        self.assertIn("`round_lenses` = `{}`", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
