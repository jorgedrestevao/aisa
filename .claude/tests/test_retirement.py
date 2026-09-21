"""Frente F (P-21) — a question withdrawn for scope: the fourth sanctioned edit.

The owner's ruling (2026-09-09) took four families of question out of the process:
identity of who executes or authorises, third-party paper proof, signatures and
go-live gates, and physical custody of files. On `pricing-bunkers` those were 30 of
95 rows. They needed a way out of the Shared Understanding that is neither a
deletion (the record must survive) nor a closure (nothing was answered).

    - retirada P-21 (<reason>)

What this locks:
  the contract says four sanctioned edits, and names the marker;
  the motor stops counting a withdrawn row as open;
  a withdrawal is NOT a closure -- it lands in no round's balance and never in
  `fechadas`, so a round that withdrew ten questions does not read as convergence;
  only `Unknown` and `Conflicted` may be withdrawn -- a Confirmed/Assumed/Risky row
  asserts something about the world and leaves by transition or not at all.

    python .claude/tests/test_retirement.py
"""

import runpy
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DASHBOARD = ROOT / "library" / "kernel" / "tools" / "dashboard.py"
STATES = (ROOT / "library" / "kernel" / "states.md").read_text(encoding="utf-8")

D = runpy.run_path(str(DASHBOARD))

SU = """# Shared Understanding

## Confirmed

| id | lens | claim | evidência | verificado_em | validade | ronda |
|----|------|-------|-----------|---------------|----------|-------|
| C-001 | data | Um facto qualquer | locator | 2026-09-09 | organizacional | R-01 |
| C-002 | data | Outro facto | locator | 2026-09-09 | organizacional | R-01 — retirada P-21 (nao se aplica a factos) |

## Unknown

| id | lens | pergunta | quem responde | criticidade | custo | swing | ronda |
|----|------|----------|---------------|-------------|-------|-------|-------|
| U-001 | data | Qual e a chave de negocio estavel? | dono de dados | Critical | spike | decisivo: sem chave nao ha idempotencia | O-02 |
| U-002 | governance | Quem assina o fecho do achado? | auditoria | Critical | reuniao | decisivo: nomeia o signatario | O-02 — retirada P-21 (pessoa/papel, fora de ambito) |
| U-003 | governance | A area receptora entrega aceitacao escrita? | dono | Critical | email | decisivo: prova de terceiro | O-02 — retirada P-21 (prova documental de terceiro) |
| U-004 | data | Que plano impoe a permissao? | IT | Critical | spike | decisivo: muda o plano de imposicao | O-01 — resolved → C-001 |

## Conflicted

| id | lens | tensão | partes | criticidade | ronda |
|----|------|--------|--------|-------------|-------|
| X-001 | chair | Duas fontes discordam do prazo | business∧governance | Critical | O-01 |
| X-002 | chair | Quem revê nao pertence a decisao | governance∧operations | Critical | O-02 — retirada P-21 (pessoa, fora de ambito) |

## Risky

| id | lens | risco | impacto | mitigação | ronda |
|----|------|-------|---------|-----------|-------|
| R-001 | data | Base nunca perfilada | lacunas tarde | perfilar antes | O-02 |
"""


class Contract(unittest.TestCase):
    def test_states_declares_six_sanctioned_edits(self):
        self.assertIn("Sanctioned edits to existing rows are exactly six", STATES)
        self.assertNotIn("are exactly three", STATES)
        self.assertNotIn("are exactly four", STATES)
        self.assertNotIn("are exactly five", STATES)

    def test_states_declares_terminology_normalisation(self):
        """P-20's fifth edit: a paraphrased product literal is restored in place."""
        self.assertIn("Terminology normalisation", STATES)
        self.assertIn("the claim asserts the same thing about the same product", STATES)
        self.assertIn("it is not a normalisation", STATES)

    def test_states_declares_the_marker_and_that_it_is_not_a_closure(self):
        self.assertIn("Withdrawal for scope", STATES)
        self.assertIn("retirada P-21", STATES)
        self.assertIn("not** a closure", STATES)

    def test_states_restricts_withdrawal_to_open_questions(self):
        self.assertIn("available for `Unknown` and `Conflicted` rows only", STATES)

    def test_states_keeps_the_row_for_audit_and_reserves_the_call_to_the_owner(self):
        self.assertIn("The row **stays**", STATES)
        self.assertIn("Only the owner's ruling withdraws a question", STATES)


class MarkerDetection(unittest.TestCase):
    def test_the_marker_is_read_with_its_reason(self):
        self.assertEqual(
            D["detect_retirement"](["U-002", "x", "O-02 — retirada P-21 (pessoa/papel)"]),
            (True, "pessoa/papel"),
        )

    def test_a_plain_round_cell_is_not_a_withdrawal(self):
        self.assertEqual(D["detect_retirement"](["U-001", "x", "O-02"]), (False, ""))

    def test_a_reason_may_carry_parentheses_of_its_own(self):
        """A reason naming the replacement row reads better with its own parenthesis;
        capturing to the FIRST `)` truncated 6 of the 13 reasons on pricing-bunkers."""
        self.assertEqual(
            D["detect_retirement"](
                ["U-063", "x", "O-01 — retirada P-21 (pessoa em vez de role — "
                                "substituída por U-096 (perfis e plano de imposição))"]
            ),
            (True, "pessoa em vez de role — substituída por U-096 "
                   "(perfis e plano de imposição)"),
        )

    def test_a_closure_is_not_a_withdrawal_and_a_withdrawal_is_not_a_closure(self):
        closure = ["U-004", "x", "O-01 — resolved → C-001"]
        withdrawal = ["U-002", "x", "O-02 — retirada P-21 (pessoa)"]
        self.assertEqual(D["detect_retirement"](closure), (False, ""))
        self.assertEqual(D["detect_resolution"](withdrawal), (False, []))


class MotorCounting(unittest.TestCase):
    def setUp(self):
        _, self.rows, meta, self.diagnostics = D["parse_su"](SU)
        self.sections = meta["sections"]
        self.by_id = {r["id"]: r for r in self.rows}

    def test_the_su_parses_without_diagnostics(self):
        self.assertEqual(self.diagnostics, [])

    def test_a_withdrawn_question_stops_counting_as_open(self):
        self.assertEqual(self.sections["Unknown"]["open"], 1)  # only U-001
        self.assertEqual(self.sections["Unknown"]["retirada"], 2)

    def test_a_withdrawn_conflict_stops_counting_as_open(self):
        self.assertEqual(self.sections["Conflicted"]["open"], 1)  # only X-001
        self.assertEqual(self.sections["Conflicted"]["retirada"], 1)

    def test_the_reason_travels_with_the_row(self):
        self.assertTrue(self.by_id["U-002"]["retired"])
        self.assertEqual(self.by_id["U-003"]["retired_reason"],
                         "prova documental de terceiro")

    def test_a_confirmed_row_cannot_be_withdrawn(self):
        """C-002 carries the marker; the motor refuses it and the row stays open."""
        self.assertFalse(self.by_id["C-002"]["retired"])
        self.assertFalse(self.by_id["C-002"]["resolved"])
        self.assertEqual(self.sections["Confirmed"]["open"], 2)
        self.assertEqual(self.sections["Confirmed"]["retirada"], 0)

    def test_every_section_carries_the_counter(self):
        for state in ("Confirmed", "Assumed", "Unknown", "Conflicted", "Risky"):
            self.assertIn("retirada", self.sections[state], state)


class RoundBalance(unittest.TestCase):
    """A round that withdrew questions must not read as convergence."""

    def setUp(self):
        _, rows, _, _ = D["parse_su"](SU)
        self.delta = D["round_delta"](rows, {"O-01": ["2026-09-09"], "O-02": ["2026-09-09"]})

    def test_withdrawals_are_counted_apart(self):
        self.assertEqual(self.delta["retiradas"], 2)  # U-002, U-003

    def test_a_withdrawal_closes_no_round(self):
        for entry in self.delta["por_ronda"]:
            self.assertLessEqual(entry.get("fechadas", 0), 1, entry)
        self.assertEqual(sum(e.get("fechadas", 0) for e in self.delta["por_ronda"]), 1)

    def test_a_withdrawal_is_not_an_indeterminate_closure(self):
        """Before P-21 a marker with no target id landed in `indeterminadas`."""
        ids = [e["id"] for e in self.delta["indeterminadas"]]
        self.assertNotIn("U-002", ids)
        self.assertNotIn("U-003", ids)

    def test_open_counts_exclude_withdrawals(self):
        self.assertEqual(self.delta["abertas"], 1)
        self.assertEqual(self.delta["critical_abertas"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
