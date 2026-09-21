"""Frente E (P-18 / F07) — a tripwire that fires must have somewhere to go.

`/revisit` recommended `/options` when the verdict was REABRIR, and `/options` refused
`phase=decision` — so the published command path dead-ended (2026-09-08 review). Two
things make the transition possible without losing history:

  * the verdict is read from a fixed header in `_simulation/revisit_*.md`, never
    inferred from prose (`revisit_state`);
  * the next Options round comes from HISTORY, not from `_state.json` — after a
    decision the state holds `D-01`, and deriving `O-01` from it would overwrite the
    round that produced the very decision being revisited (`options_round_history`).

The previous decision is never edited: the new one carries `Supersedes`, and the motor
derives the reverse pointer and stops treating the old one as the decision in force.

    python .claude/tests/test_reopen_transition.py
"""

import json
import runpy
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
D = runpy.run_path(str(ROOT / "library" / "kernel" / "tools" / "dashboard.py"))

REVISIT_HEADER = """# Revisit — eng — TW-1

- **Decision**: D-002
- **Target**: TW-1
- **Counterfactual**: _simulation/counterfactuals/O-003.md
- **Fired**: yes
- **Recomendação**: REABRIR
- **Timestamp**: 2026-09-10T09:00:00Z

## Disparou mesmo?

Sim — o volume confirmado caiu (C-042).
"""

SOLUTION = """
## D-002 — Adopt O-001 — plataforma interna

- **Chosen option**: O-001
- **Revision conditions / Tripwires (estruturados)**:
  - TW-1: se o volume confirmado cair abaixo de 20/mês (C-042) → comparar com `_simulation/counterfactuals/O-003.md`
- **Decided in round**: D-01
- **Timestamp**: 2026-06-01T10:00:00Z
"""

REOPENED = """
## D-005 — Adopt O-003 — serviço externo

- **Chosen option**: O-003
- **Revision conditions / Tripwires (estruturados)**:
  - TW-1: se o custo por unidade subir acima de X (C-051) → rever
- **Supersedes**: D-002 — reaberta em O-02 por TW-1 (_simulation/revisit_2026-09-10_TW-1.md)
- **Decided in round**: D-02
- **Timestamp**: 2026-09-11T10:00:00Z
"""


def make_engagement(base, *, phase="decision", round_id="D-01", decisions=SOLUTION,
                    revisit=None, synthesis_rounds=("O-01",)):
    eng = Path(base) / "eng"
    (eng / "lens-outputs").mkdir(parents=True, exist_ok=True)
    (eng / "_simulation").mkdir(exist_ok=True)
    (eng / "_state.json").write_text(
        json.dumps({"engagement": "eng", "phase": phase, "round": round_id}), encoding="utf-8")
    (eng / "decisions.md").write_text("# Decisions\n" + decisions, encoding="utf-8")
    (eng / "shared-understanding.md").write_text("# Shared Understanding\n", encoding="utf-8")
    for r in synthesis_rounds:
        (eng / "lens-outputs" / f"chairman-synthesis-{r}.md").write_text(
            f"# {r}\n", encoding="utf-8")
    if revisit is not None:
        (eng / "_simulation" / "revisit_2026-09-10_TW-1.md").write_text(revisit, encoding="utf-8")
    return eng


class RevisitVerdictIsRead(unittest.TestCase):

    def test_header_verdict(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make_engagement(tmp, revisit=REVISIT_HEADER)
            st = D["revisit_state"](eng)
        self.assertEqual(st["verdict"], "REABRIR")
        self.assertEqual(st["decision"], "D-002")
        self.assertEqual(st["target"], "TW-1")
        self.assertTrue(st["present"])

    def test_prose_without_a_header_is_unknown_never_guessed(self):
        prose = ("# Revisit\n\nA recomendação é reabrir as alternativas, sem dúvida — "
                 "REABRIR já.\n")
        with tempfile.TemporaryDirectory() as tmp:
            eng = make_engagement(tmp, revisit=prose)
            st = D["revisit_state"](eng)
        self.assertEqual(st["verdict"], "unknown",
                         "a verdict inferred from prose would be the motor judging")

    def test_no_revisit_at_all(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make_engagement(tmp)
            st = D["revisit_state"](eng)
        self.assertFalse(st["present"])
        self.assertEqual(st["verdict"], "")

    def test_latest_by_timestamp_wins(self):
        older = REVISIT_HEADER.replace("REABRIR", "MANTER").replace(
            "2026-09-10T09:00:00Z", "2026-09-01T09:00:00Z")
        with tempfile.TemporaryDirectory() as tmp:
            eng = make_engagement(tmp, revisit=REVISIT_HEADER)
            (eng / "_simulation" / "revisit_2026-09-01_TW-1.md").write_text(older, encoding="utf-8")
            st = D["revisit_state"](eng)
        self.assertEqual(st["verdict"], "REABRIR")


class OptionsCounterComesFromHistory(unittest.TestCase):

    def test_state_says_D01_but_history_says_O02(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make_engagement(tmp)
            state = json.loads((eng / "_state.json").read_text(encoding="utf-8"))
            hist = D["options_round_history"](eng, state)
        self.assertEqual(hist["max"], "O-01")
        self.assertEqual(hist["next"], "O-02",
                         "restarting at O-01 would overwrite the round under revision")

    def test_council_log_headings_count_too(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make_engagement(tmp, synthesis_rounds=())
            (eng / "council-log.md").write_text("## O-01 — opções\n## O-02 — opções\n",
                                                encoding="utf-8")
            hist = D["options_round_history"](eng, {"round": "D-01"})
        self.assertEqual(hist["next"], "O-03")

    def test_first_options_round_when_there_is_no_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make_engagement(tmp, phase="framing", round_id="F-01", synthesis_rounds=())
            hist = D["options_round_history"](eng, {"round": "F-01"})
        self.assertEqual(hist["max"], "")
        self.assertEqual(hist["next"], "O-01")


class SupersededDecisionLeavesTheStage(unittest.TestCase):

    def test_tripwires_follow_the_decision_in_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make_engagement(tmp, decisions=SOLUTION)
            before = D["classify_decisions"]((eng / "decisions.md").read_text(encoding="utf-8"))
            self.assertEqual(D["solution_decision"](before)["id"], "D-002")

            # /decide after the reopening appends; it never edits the old block.
            (eng / "decisions.md").write_text(
                "# Decisions\n" + SOLUTION + REOPENED, encoding="utf-8")
            after = D["classify_decisions"]((eng / "decisions.md").read_text(encoding="utf-8"))
        index = {b["id"]: b for b in after}
        self.assertEqual(D["solution_decision"](after)["id"], "D-005")
        self.assertEqual(index["D-002"]["superseded_by"], "D-005")
        self.assertEqual(index["D-005"]["supersedes"], "D-002")
        self.assertTrue(index["D-002"]["tripwires"],
                        "the superseded decision keeps its record, it is just not in force")
        facts = D["tripwire_facts"](after, [])
        self.assertEqual(facts["source_decision"], "D-005")

    def test_a_decision_cannot_supersede_itself(self):
        self_ref = SOLUTION.replace("- **Decided in round**: D-01",
                                    "- **Supersedes**: D-002\n- **Decided in round**: D-01")
        blocks = D["classify_decisions"]("# Decisions\n" + self_ref)
        self.assertEqual(blocks[0]["superseded_by"], "")
        self.assertEqual(D["solution_decision"](blocks)["id"], "D-002")


class RealEngagementUnaffected(unittest.TestCase):
    """A copy of a real engagement: nothing about it changes until a reopen happens."""

    def test_pilot_1_still_reports_its_decision(self):
        src = ROOT / "projects" / "pricing-marinha-pilot-1"
        if not (src / "decisions.md").is_file():
            self.skipTest("engagement not mounted")
        with tempfile.TemporaryDirectory() as tmp:
            eng = Path(tmp) / "pilot"
            shutil.copytree(src, eng)
            blocks = D["classify_decisions"]((eng / "decisions.md").read_text(encoding="utf-8"))
            state = json.loads((eng / "_state.json").read_text(encoding="utf-8"))
            self.assertEqual(D["solution_decision"](blocks)["id"], "D-002")
            self.assertTrue(all(not b["superseded_by"] for b in blocks))
            self.assertEqual(D["options_round_history"](eng, state)["next"], "O-02")
            self.assertFalse(D["revisit_state"](eng)["present"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
