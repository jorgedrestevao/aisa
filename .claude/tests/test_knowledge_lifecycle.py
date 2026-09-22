# -*- coding: utf-8 -*-
"""L06-L10 — coerencia do conhecimento (P6).

As transicoes que NAO partem de `Unknown`. Todas contra `library/kernel/states.md`."""
import json
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "library" / "kernel" / "tools"
R = runpy.run_path(str(TOOLS / "resolve.py"))
G = runpy.run_path(str(TOOLS / "graph.py"))
O = runpy.run_path(str(TOOLS / "operation.py"))


def fresh(eng, expr):
    code = ("import runpy,json;G=runpy.run_path(r'{g}');R=runpy.run_path(r'{r}');"
            "eng=r'{e}';print(json.dumps({x}))").format(
        g=TOOLS / "graph.py", r=TOOLS / "resolve.py", e=eng, x=expr)
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=120)
    if out.returncode != 0:
        raise AssertionError(out.stderr[-500:])
    return json.loads(out.stdout)


class L06_Finding(unittest.TestCase):
    """Finding de comportamento manual, dispor/reabrir ->
    distincao, evidencia, criticidade e accao SOBREVIVEM ao reinicio."""

    F = dict(fid="F-001", behaviour="O operador reintroduz o preco a mao todas as sextas",
             evidence="_capture/process-model.md#PM-004", criticality="Critical",
             action="automatizar ou registar como excepcao aceite")

    def test_a_finding_needs_all_four_fields(self):
        for drop in ("behaviour", "evidence", "criticality", "action"):
            kw = dict(self.F); kw[drop] = ""
            with self.assertRaises(R["ResolveError"], msg=drop) as ctx:
                R["finding"](**kw)
            self.assertEqual(ctx.exception.code, "INCOMPLETE_FINDING")

    def test_the_four_fields_survive_a_restart(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = Path(tmp) / "eng"; eng.mkdir()
            n = R["finding"](**self.F)
            O["run"](eng, "op-f", G["write_set"]([n], []))
            st = fresh(eng, "G['read'](eng)")
        got = [x for x in st["nodes"] if x["id"] == "F-001"][0]["props"]
        for k in ("behaviour", "evidence", "criticality", "action"):
            self.assertEqual(got[k], self.F[k if k != "behaviour" else "behaviour"],
                             "`{}` nao sobreviveu".format(k))

    def test_disposing_keeps_the_history(self):
        n = R["finding"](**self.F)
        d = R["dispose_finding"](n, "disposed", "aceite como excepcao pelo dono")
        self.assertTrue(d["props"]["disposed"])
        self.assertEqual(len(d["props"]["history"]), 1)

    def test_reopening_appends_rather_than_replaces(self):
        n = R["dispose_finding"](R["finding"](**self.F), "disposed", "b1")
        r = R["dispose_finding"](n, "reopened", "b2")
        self.assertFalse(r["props"]["disposed"])
        self.assertEqual([h["disposition"] for h in r["props"]["history"]],
                         ["disposed", "reopened"], "a historia foi substituida")

    def test_disposing_without_a_basis_is_refused(self):
        with self.assertRaises(R["ResolveError"]) as ctx:
            R["dispose_finding"](R["finding"](**self.F), "disposed", "")
        self.assertEqual(ctx.exception.code, "NO_BASIS")


class L07_Contradicao(unittest.TestCase):
    """Fontes opostas -> dois lados e historia preservados, SEM escolher por recencia."""

    ROW = {"id": "X-001", "state": "Conflicted"}
    SIDES = ["fonte: contrato SAP diz 18h", "role: Operacoes diz 20h"]

    def test_an_owner_decision_gives_n_confirmed(self):
        out = R["resolve_conflict"](self.ROW, self.SIDES, by_owner=True)
        self.assertEqual(out["state"], "Confirmed")
        self.assertEqual(out["successors"], 2)

    def test_without_the_owner_it_is_assumed_not_confirmed(self):
        out = R["resolve_conflict"](self.ROW, self.SIDES, by_owner=False)
        self.assertEqual(out["state"], "Assumed",
                         "resolveu um conflito para Confirmed sem o dono")

    def test_both_sides_are_preserved_either_way(self):
        for by_owner in (True, False):
            out = R["resolve_conflict"](self.ROW, self.SIDES, by_owner=by_owner)
            self.assertEqual(out["sides_preserved"], self.SIDES,
                             "um lado desapareceu (by_owner={})".format(by_owner))

    def test_recency_is_never_the_criterion(self):
        out = R["resolve_conflict"](self.ROW, self.SIDES, by_owner=False)
        self.assertFalse(out["chose_by_recency"])
        # inverter a ordem nao muda o veredicto
        rev = R["resolve_conflict"](self.ROW, list(reversed(self.SIDES)), by_owner=False)
        self.assertEqual(out["state"], rev["state"])

    def test_a_conflict_needs_two_sides(self):
        with self.assertRaises(R["ResolveError"]) as ctx:
            R["resolve_conflict"](self.ROW, ["um lado so"], by_owner=True)
        self.assertEqual(ctx.exception.code, "TOO_FEW_SIDES")


class L08_NaAndRisco(unittest.TestCase):
    """Retirar por ambito ou aceitar risco ->
    base EXIGIDA registada; SEM converter em facto nem apagar historia."""

    def test_withdrawal_is_only_a_marker(self):
        out = R["withdraw"]({"id": "U-009"}, "fora dos eixos tecnicos")
        self.assertTrue(out["marker"].startswith(R["RETIRADA_MARK"]))
        self.assertFalse(out["creates_row"])
        self.assertFalse(out["becomes_fact"], "uma retirada virou facto")

    def test_withdrawal_requires_a_reason(self):
        with self.assertRaises(R["ResolveError"]) as ctx:
            R["withdraw"]({"id": "U-009"}, "   ")
        self.assertEqual(ctx.exception.code, "NO_BASIS")

    def test_the_reason_travels_in_the_marker(self):
        out = R["withdraw"]({"id": "U-009"}, "a organizacao nao saber nao e trabalho do projecto")
        self.assertIn("nao e trabalho do projecto", out["marker"])

    def test_accepting_a_risk_records_the_basis_and_stays_risky(self):
        out = R["accept_risk"]({"id": "R-003"}, "custo de mitigar excede o impacto estimado")
        self.assertFalse(out["becomes_fact"], "um risco aceite virou Confirmed")
        self.assertIn("custo de mitigar", out["basis"])

    def test_accepting_a_risk_without_a_basis_is_refused(self):
        with self.assertRaises(R["ResolveError"]) as ctx:
            R["accept_risk"]({"id": "R-003"}, "")
        self.assertEqual(ctx.exception.code, "NO_BASIS")


class L09_Validade(unittest.TestCase):
    """Expirar/revalidar/corrigir ->
    revalidacao SEM claim nova so quando inalterada; correccao usa transicao."""

    ROW = {"id": "C-014", "state": "Confirmed"}

    def test_an_unchanged_fact_is_a_sanctioned_edit_with_no_new_row(self):
        out = R["revalidate"](self.ROW, still_holds=True, today="2026-09-22")
        self.assertEqual(out["mode"], "sanctioned_edit")
        self.assertFalse(out["creates_row"], "revalidar criou linha nova")
        self.assertEqual(out["verificado_em"], "2026-09-22")

    def test_a_changed_fact_falls_back_to_the_normal_transition(self):
        out = R["revalidate"](self.ROW, still_holds=False)
        self.assertEqual(out["mode"], "transition")
        self.assertTrue(out["creates_row"])
        self.assertIn("was C-014", out["reason"])

    def test_a_changed_fact_is_never_renewed(self):
        out = R["revalidate"](self.ROW, still_holds=False)
        self.assertNotIn("verificado_em", out,
                         "renovou `verificado_em` de um facto que mudou")

    def test_the_two_modes_are_distinguishable(self):
        a = R["revalidate"](self.ROW, still_holds=True)
        b = R["revalidate"](self.ROW, still_holds=False)
        self.assertNotEqual(a["mode"], b["mode"])
        self.assertNotEqual(a["creates_row"], b["creates_row"])


class L10_Dependencias(unittest.TestCase):
    """Alterar premissa de decisao/blueprint e outra nao relacionada ->
    revalidacao DIRECCIONADA; decisao NAO reescrita por answer."""

    NODES = [{"id": "C-001", "type": "claim", "props": {}, "provenance": {}},
             {"id": "C-002", "type": "claim", "props": {}, "provenance": {}},
             {"id": "B-001", "type": "blueprint", "props": {}, "provenance": {}},
             {"id": "Z-999", "type": "claim", "props": {}, "provenance": {}}]
    EDGES = [{"src": "B-001", "rel": "depends_on", "dst": "C-001", "props": {}, "provenance": {}},
             {"src": "C-002", "rel": "depends_on", "dst": "B-001", "props": {}, "provenance": {}}]

    def test_only_the_dependent_chain_is_revalidated(self):
        got = R["dependents_of"](self.NODES, self.EDGES, ["C-001"])
        self.assertEqual(got, ["B-001", "C-002"])

    def test_an_unrelated_change_touches_nothing(self):
        self.assertEqual(R["dependents_of"](self.NODES, self.EDGES, ["Z-999"]), [])

    def test_revalidating_everything_would_be_the_same_as_nothing(self):
        """A afirmacao do caso: direccionada quer dizer que sobra alguem de fora."""
        got = set(R["dependents_of"](self.NODES, self.EDGES, ["C-001"]))
        allids = {n["id"] for n in self.NODES}
        self.assertTrue(allids - got - {"C-001"}, "revalidou tudo — nao e direccionada")

    def test_an_answer_never_rewrites_a_decision(self):
        out = R["decision_rewritten_by"](["U-001", "D-002"], ["D-001", "D-002"])
        self.assertTrue(out["would_rewrite"])
        self.assertEqual(out["decisions"], ["D-002"])
        self.assertIn("`/decide`", out["reason"])

    def test_an_answer_that_touches_no_decision_is_clean(self):
        out = R["decision_rewritten_by"](["U-001", "C-003"], ["D-001"])
        self.assertFalse(out["would_rewrite"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
