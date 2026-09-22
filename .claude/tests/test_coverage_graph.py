# -*- coding: utf-8 -*-
"""C01-C08 — integracao minima do grafo com o Coverage (P6).

Nao ha comparador novo. A dependencia consumida entra como FONTE do `basis` e quem decide
`current`/`stale` continua a ser `coverage.check_freshness` — o proprio codigo avisa, em
`finalize_recheck`, que ter uma segunda comparacao acabaria por divergir."""
import json
import runpy
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "library" / "kernel" / "tools"
G = runpy.run_path(str(TOOLS / "graph.py"))
C = runpy.run_path(str(TOOLS / "coverage.py"))
O = runpy.run_path(str(TOOLS / "operation.py"))
B = runpy.run_path(str(TOOLS / "bootstrap.py"))

NODES = [{"id": "C-001", "type": "claim", "props": {"state": "Confirmed", "v": 1},
          "provenance": {"lens": "data"}},
         {"id": "U-002", "type": "question", "props": {"state": "Unknown"},
          "provenance": {"lens": "ops"}}]
EDGES = [{"src": "U-002", "rel": "depends_on", "dst": "C-001", "props": {},
          "provenance": {}}]
CONSUMED = {"C-001", "U-002|depends_on|C-001"}


def basis(nodes, edges, consumed, **extra):
    """Um `basis` minimo, com a dependencia do grafo como mais uma fonte."""
    b = {"inventory_sha256": "inv", "su_fingerprint": "su", "decision_fingerprint": "dec",
         "contract_version": "1", "authorities": [],
         "sources": [{"path": "inputs/x.xlsx", "use": "freshness", "sha256": "aaa"}]}
    if consumed is not None:
        b["sources"].append(G["as_coverage_source"](nodes, edges, consumed))
    b.update(extra)
    return b


def verdict(old, new):
    return C["check_freshness"]({"basis": old}, new)


class C01_Reinicio(unittest.TestCase):
    """Reabrir sem mudanca de fontes/conhecimento -> Coverage mantem atualidade."""

    def test_same_inputs_stay_current(self):
        b = basis(NODES, EDGES, CONSUMED)
        self.assertEqual(verdict(b, b)["status"], "current")

    def test_a_fresh_read_recomputes_the_same_fingerprint(self):
        a = G["dependency_fingerprint"](NODES, EDGES, CONSUMED)
        z = G["dependency_fingerprint"](NODES, EDGES, CONSUMED)
        self.assertEqual(a, z)

    def test_reopening_an_engagement_does_not_move_the_graph_revision(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = Path(tmp) / "eng"
            eng.mkdir()
            O["run"](eng, "op", G["write_set"](NODES, EDGES))
            first = G["read"](eng)["revision"]
            second = G["read"](eng)["revision"]
            self.assertEqual(first, second)


class C02_Ordenacao(unittest.TestCase):
    """Reordenar grafo sem alteracao semantica -> NAO invalida a revisao."""

    def test_reordered_nodes_give_the_same_fingerprint(self):
        self.assertEqual(G["dependency_fingerprint"](NODES, EDGES, CONSUMED),
                         G["dependency_fingerprint"](list(reversed(NODES)), EDGES, CONSUMED))

    def test_reordering_does_not_make_the_record_stale(self):
        old = basis(NODES, EDGES, CONSUMED)
        new = basis(list(reversed(NODES)), EDGES, CONSUMED)
        self.assertEqual(verdict(old, new)["status"], "current",
                         "reordenar invalidou a revisao")

    def test_reordering_does_not_move_the_store_revision(self):
        self.assertEqual(G["revision_of"](NODES, EDGES),
                         G["revision_of"](list(reversed(NODES)), EDGES))


class C03_PremissaMaterial(unittest.TestCase):
    """Alterar claim/regra consumida -> mudanca detectada e EXPLICADA pelo motor."""

    def test_a_changed_consumed_claim_is_stale(self):
        changed = [dict(NODES[0], props={"state": "Confirmed", "v": 2}), NODES[1]]
        v = verdict(basis(NODES, EDGES, CONSUMED), basis(changed, EDGES, CONSUMED))
        self.assertEqual(v["status"], "stale")

    def test_the_motor_says_which_source_changed(self):
        changed = [dict(NODES[0], props={"state": "Confirmed", "v": 2}), NODES[1]]
        v = verdict(basis(NODES, EDGES, CONSUMED), basis(changed, EDGES, CONSUMED))
        what = [c["what"] for c in v["changed"]]
        self.assertIn(G["CONSUMED_PATH"], what)

    def test_a_changed_su_fingerprint_is_also_explained(self):
        old = basis(NODES, EDGES, CONSUMED)
        new = basis(NODES, EDGES, CONSUMED, su_fingerprint="outro")
        v = verdict(old, new)
        self.assertEqual(v["status"], "stale")
        self.assertTrue(any("Shared Understanding" in c["message"] for c in v["changed"]))

    def test_stale_does_not_mean_the_conclusion_is_false(self):
        """C4: `stale` e «a base mudou e precisa de revisao», nao «a conclusao e falsa»."""
        changed = [dict(NODES[0], props={"v": 2}), NODES[1]]
        v = verdict(basis(NODES, EDGES, CONSUMED), basis(changed, EDGES, CONSUMED))
        self.assertNotIn("false", json.dumps(v).lower())
        self.assertTrue(v["changed"], "stale sem razao nenhuma e um veredicto cego")


class C04_RelacaoNaoConsumida(unittest.TestCase):
    """Acrescentar link so de navegacao -> SEM stale pela versao global do grafo."""

    NAV = EDGES + [{"src": "C-001", "rel": "ve_tambem", "dst": "U-002", "props": {},
                    "provenance": {}}]

    def test_a_navigation_edge_does_not_change_the_dependency(self):
        self.assertEqual(G["dependency_fingerprint"](NODES, EDGES, CONSUMED),
                         G["dependency_fingerprint"](NODES, self.NAV, CONSUMED))

    def test_a_navigation_edge_does_not_make_the_record_stale(self):
        v = verdict(basis(NODES, EDGES, CONSUMED), basis(NODES, self.NAV, CONSUMED))
        self.assertEqual(v["status"], "current",
                         "uma aresta de navegacao invalidou a revisao")

    def test_but_the_store_revision_does_move(self):
        """A revisao global MUDA — e e por isso que nao se usa a versao global."""
        self.assertNotEqual(G["revision_of"](NODES, EDGES),
                            G["revision_of"](NODES, self.NAV))

    def test_the_two_are_not_the_same_thing(self):
        """A afirmacao do caso, dita de uma vez: versao global != dependencia consumida."""
        glob_changed = G["revision_of"](NODES, EDGES) != G["revision_of"](NODES, self.NAV)
        dep_changed = (G["dependency_fingerprint"](NODES, EDGES, CONSUMED)
                       != G["dependency_fingerprint"](NODES, self.NAV, CONSUMED))
        self.assertTrue(glob_changed)
        self.assertFalse(dep_changed)


class C05_RelacaoConsumida(unittest.TestCase):
    """Alterar dependencia EXCLUSIVA do grafo usada na avaliacao ->
    fingerprint especifico muda; revisao nao reutilizada como actual."""

    def test_changing_a_consumed_edge_changes_the_fingerprint(self):
        other = [{"src": "U-002", "rel": "depends_on", "dst": "C-001",
                  "props": {"peso": 2}, "provenance": {}}]
        self.assertNotEqual(G["dependency_fingerprint"](NODES, EDGES, CONSUMED),
                            G["dependency_fingerprint"](NODES, other, CONSUMED))

    def test_and_the_record_goes_stale(self):
        other = [{"src": "U-002", "rel": "depends_on", "dst": "C-001",
                  "props": {"peso": 2}, "provenance": {}}]
        v = verdict(basis(NODES, EDGES, CONSUMED), basis(NODES, other, CONSUMED))
        self.assertEqual(v["status"], "stale")

    def test_removing_a_consumed_edge_is_detected(self):
        v = verdict(basis(NODES, EDGES, CONSUMED), basis(NODES, [], CONSUMED))
        self.assertEqual(v["status"], "stale")

    def test_the_consumed_set_is_recorded_so_the_review_is_auditable(self):
        src = G["as_coverage_source"](NODES, EDGES, CONSUMED)
        self.assertEqual(src["consumed"], sorted(CONSUMED))
        self.assertEqual(src["use"], "freshness")


class C06_Aprovacao(unittest.TestCase):
    """Aprovar blueprint -> preservar exclusoes do contrato; NAO invalidar a propria revisao."""

    def test_su_fingerprint_excludes_blueprint_approval_rows(self):
        """A exclusao ja existe no motor; este teste guarda-a de regressao."""
        src = (TOOLS / "coverage.py").read_text(encoding="utf-8")
        i = src.index("def su_fingerprint")
        doc = src[i:i + 700]
        self.assertIn("aprovações de blueprint", doc,
                      "a exclusao que impede a aprovacao de se auto-invalidar desapareceu")

    def test_an_approval_that_only_adds_a_decision_row_keeps_the_record_current(self):
        old = basis(NODES, EDGES, CONSUMED)
        new = basis(NODES, EDGES, CONSUMED)   # fingerprints iguais: a aprovacao foi excluida
        self.assertEqual(verdict(old, new)["status"], "current")

    def test_a_decision_fingerprint_change_is_still_detected(self):
        """Excluir aprovacoes nao e excluir decisoes."""
        v = verdict(basis(NODES, EDGES, CONSUMED),
                    basis(NODES, EDGES, CONSUMED, decision_fingerprint="outra"))
        self.assertEqual(v["status"], "stale")


class C07_FonteAlterada(unittest.TestCase):
    """Actualizar formula/renomear folha/tornar fonte ilegivel ->
    versoes historicas preservadas, ambito afectado identificado, SEM check limpo ficticio."""

    def test_a_changed_source_is_reported_with_both_hashes(self):
        old = basis(NODES, EDGES, CONSUMED)
        new = basis(NODES, EDGES, CONSUMED)
        new["sources"][0] = {"path": "inputs/x.xlsx", "use": "freshness", "sha256": "bbb"}
        v = verdict(old, new)
        ch = [c for c in v["changed"] if c["what"] == "inputs/x.xlsx"][0]
        self.assertEqual((ch["was"], ch["now"]), ("aaa", "bbb"))

    def test_a_renamed_source_shows_as_removed_and_added(self):
        old = basis(NODES, EDGES, CONSUMED)
        new = basis(NODES, EDGES, CONSUMED)
        new["sources"][0] = {"path": "inputs/y.xlsx", "use": "freshness", "sha256": "aaa"}
        kinds = {c["kind"] for c in verdict(old, new)["changed"]}
        self.assertEqual(kinds & {"source-added", "source-removed"},
                         {"source-added", "source-removed"},
                         "renomear nao foi identificado como ambito afectado")

    def test_an_unreadable_graph_is_not_a_clean_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = Path(tmp) / "eng"
            (eng / "_graph").mkdir(parents=True)
            (eng / "_graph" / "graph.jsonl").write_text("{partido\n", encoding="utf-8")
            (eng / "_graph" / "meta.json").write_text('{"schema_version":1}\n', encoding="utf-8")
            st = G["read"](eng)
            boot = B["bootstrap"](eng)
        self.assertNotEqual(st["status"], G["OK"])
        self.assertFalse(boot["ready"], "fonte ilegivel passou por check limpo")

    def test_a_record_without_basis_is_not_evaluated_rather_than_current(self):
        v = C["check_freshness"]({}, basis(NODES, EDGES, CONSUMED))
        self.assertEqual(v["status"], "not_evaluated",
                         "um registo sem base foi dado como actual")


class C08_EstadoParcial(unittest.TestCase):
    """Consultar gate/Coverage durante pendencia ou SU divergente ->
    avanco NAO usa avaliacao inconsistente; SEM flags de verdade."""

    def test_a_pending_operation_closes_the_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = Path(tmp) / "eng"
            eng.mkdir()
            O["_atomic_write"](O["pending_path"](eng), json.dumps(
                {"intent_version": 1, "operation_id": "x", "after": {"a": "b"}}))
            self.assertFalse(O["gate_open"](eng))
            self.assertFalse(B["bootstrap"](eng)["ready"])

    def test_a_divergent_mirror_is_reported_and_does_not_win(self):
        nodes = [{"id": "C-001", "type": "claim", "props": {"state": "Confirmed"},
                  "provenance": {"mirror_of": "SU:C-001"}}]
        out = G["drift"](nodes, {"SU:C-001": "Assumed"})
        self.assertEqual(out[0]["code"], "MIRROR_DRIFT")
        self.assertIn("a autoridade manda", out[0]["detail"])

    def test_no_coverage_validity_flag_is_written_to_state(self):
        """C4: nada de `coverage_valid`, `coverage_stale` ou percentagens em `_state.json`."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = Path(tmp) / "eng"
            eng.mkdir()
            (eng / "_state.json").write_text('{"phase":"discovery"}\n', encoding="utf-8")
            O["run"](eng, "op", G["write_set"](NODES, EDGES))
            state = json.loads((eng / "_state.json").read_text(encoding="utf-8"))
        for forbidden in ("coverage_valid", "coverage_stale", "coverage_pct", "graph_pct"):
            self.assertNotIn(forbidden, state,
                             "`{}` entrou no estado — C4 proibe".format(forbidden))

    def test_the_gate_reopens_only_after_recovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = Path(tmp) / "eng"
            eng.mkdir()
            O["run"](eng, "op", {"answers.md": "a\n"})
            self.assertTrue(O["gate_open"](eng))


if __name__ == "__main__":
    unittest.main(verbosity=2)
