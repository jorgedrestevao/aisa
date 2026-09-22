# -*- coding: utf-8 -*-
"""B01-B07 — bootstrap técnico universal (P3).

Cada classe é um caso de `validation/cases.json`."""
import hashlib
import json
import os
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "library" / "kernel" / "tools"
B = runpy.run_path(str(TOOLS / "bootstrap.py"))
G = runpy.run_path(str(TOOLS / "graph.py"))
O = runpy.run_path(str(TOOLS / "operation.py"))

N1 = {"id": "C-001", "type": "claim", "props": {"state": "Confirmed", "text": "facto"},
      "provenance": {"lens": "data"}}
U1 = {"id": "U-001", "type": "question", "props": {"state": "Unknown", "text": "pergunta"},
      "provenance": {"lens": "governance"}}


def tree_hash(root: Path) -> str:
    """Hash de TODA a árvore: caminhos + bytes. Muda se o bootstrap escrever o que for."""
    h = hashlib.sha256()
    for p in sorted(Path(root).rglob("*")):
        h.update(str(p.relative_to(root)).encode("utf-8"))
        if p.is_file():
            h.update(p.read_bytes())
            h.update(str(p.stat().st_mtime_ns).encode("utf-8"))
    return h.hexdigest()


def new_eng(tmp, name="eng", nodes=None, edges=None, files=None):
    eng = Path(tmp) / name
    eng.mkdir(parents=True, exist_ok=True)
    for rel, body in (files or {"_state.json": '{"phase":"discovery"}\n'}).items():
        (eng / rel).write_text(body, encoding="utf-8", newline="\n")
    if nodes is not None:
        (eng / "_graph").mkdir(exist_ok=True)
        body, meta = G["serialize"](nodes, edges or [])
        (eng / "_graph" / "graph.jsonl").write_text(body, encoding="utf-8", newline="\n")
        (eng / "_graph" / "meta.json").write_text(meta, encoding="utf-8", newline="\n")
    return eng


class B01_EntradaReal(unittest.TestCase):
    """Comandos/skills sem start e pedido em linguagem natural ->
    bootstrap PRECEDE efeitos; projecto e revisão observáveis."""

    def test_bootstrap_returns_engagement_and_revision(self):
        with tempfile.TemporaryDirectory() as tmp:
            boot = B["bootstrap"](new_eng(tmp, nodes=[N1]))
        self.assertTrue(boot["ready"])
        self.assertEqual(boot["engagement"]["slug"], "eng")
        self.assertTrue(boot["snapshot"]["revision"], "sem revisão observável")
        self.assertTrue(boot["graph"]["revision"], "sem revisão do grafo")

    def test_an_entry_without_start_still_observes_the_project(self):
        """Não há `/start`: chama-se o bootstrap directamente, como uma skill faria."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp, nodes=[N1])
            boot = B["bootstrap"](eng)
        self.assertEqual(boot["engagement"]["resolved"], str(eng.resolve()))

    def test_a_missing_engagement_is_not_ready_and_says_so(self):
        with tempfile.TemporaryDirectory() as tmp:
            boot = B["bootstrap"](Path(tmp) / "nao-existe")
        self.assertFalse(boot["ready"])
        self.assertEqual(boot["limitations"][0]["code"], "ENGAGEMENT_MISSING")

    def test_pending_stops_bootstrap_before_any_content(self):
        """A ordem do B5: a pendência é detectada no passo 2, antes de ler conteúdo."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp, nodes=[N1])
            O["_atomic_write"](O["pending_path"](eng), json.dumps(
                {"intent_version": 1, "operation_id": "op-x", "after": {"a": "b"}}))
            boot = B["bootstrap"](eng)
        self.assertFalse(boot["ready"])
        self.assertEqual(boot["context"], {}, "construiu contexto sobre estado pendente")
        self.assertEqual(boot["limitations"][0]["code"], "PENDING_OPERATION")
        self.assertTrue(boot["limitations"][0]["recovery"], "não diz como recuperar")

    def test_recovery_is_a_separate_action_never_a_side_effect(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp, nodes=[N1])
            O["_atomic_write"](O["pending_path"](eng), json.dumps(
                {"intent_version": 1, "operation_id": "op-x", "after": {"a": "b"}}))
            B["bootstrap"](eng)
            self.assertIsNotNone(O["read_pending"](eng),
                                 "o bootstrap recuperou sozinho — é acção separada")


class B02_Subprocessos(unittest.TestCase):
    """Mutação por shell e leitores directos -> MESMA barreira; não depende de Write/Edit."""

    def test_a_subprocess_reader_sees_the_same_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp, nodes=[N1])
            here = B["bootstrap"](eng)
            code = ("import runpy,json;B=runpy.run_path(r'{}');"
                    "print(json.dumps(B['bootstrap'](r'{}')['snapshot']))").format(
                TOOLS / "bootstrap.py", eng)
            out = subprocess.run([sys.executable, "-c", code],
                                 capture_output=True, text=True, timeout=60)
            self.assertEqual(out.returncode, 0, out.stderr)
            there = json.loads(out.stdout)
        self.assertEqual(here["snapshot"]["revision"], there["revision"],
                         "o subprocesso viu outro snapshot")

    def test_a_shell_mutation_moves_the_snapshot_for_everyone(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp, nodes=[N1])
            before = B["bootstrap"](eng)["snapshot"]["revision"]
            code = ("import runpy;O=runpy.run_path(r'{}');"
                    "O['run'](r'{}','op-shell',{{'answers.md':'novo\\n'}})").format(
                TOOLS / "operation.py", eng)
            out = subprocess.run([sys.executable, "-c", code],
                                 capture_output=True, text=True, timeout=60)
            self.assertEqual(out.returncode, 0, out.stderr)
            after = B["bootstrap"](eng)["snapshot"]["revision"]
        self.assertNotEqual(before, after,
                            "uma mutação por shell não mexeu no snapshot que os leitores usam")

    def test_a_subprocess_pending_blocks_the_parent_reader(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp, nodes=[N1])
            code = ("import runpy,json;O=runpy.run_path(r'{}');"
                    "O['_atomic_write'](O['pending_path'](r'{}'),"
                    "json.dumps({{'intent_version':1,'operation_id':'sp','after':{{'a':'b'}}}}))"
                    ).format(TOOLS / "operation.py", eng)
            subprocess.run([sys.executable, "-c", code], capture_output=True, timeout=60)
            boot = B["bootstrap"](eng)
        self.assertFalse(boot["ready"], "pendência criada por subprocesso não bloqueou o leitor")


class B03_TrocaDeProjeto(unittest.TestCase):
    """Retomar A, trabalhar B, voltar a A -> sem contaminação nem escrita cruzada."""

    def test_switching_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = B["bootstrap"](new_eng(tmp, "A", nodes=[N1]))
            b = B["bootstrap"](new_eng(tmp, "B", nodes=[U1]))
        self.assertTrue(B["switched"](a, b), "a troca de engagement não foi detectada")
        self.assertFalse(B["switched"](a, a))

    def test_contexts_do_not_bleed(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = B["bootstrap"](new_eng(tmp, "A", nodes=[N1]))
            b = B["bootstrap"](new_eng(tmp, "B", nodes=[U1]))
        ids_a = {i["id"] for i in a["context"]["included"]}
        ids_b = {i["id"] for i in b["context"]["included"]}
        self.assertEqual(ids_a, {"C-001"})
        self.assertEqual(ids_b, {"U-001"})
        self.assertEqual(ids_a & ids_b, set(), "contexto de A apareceu em B")

    def test_returning_to_a_gives_a_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng_a = new_eng(tmp, "A", nodes=[N1])
            first = B["bootstrap"](eng_a)
            B["bootstrap"](new_eng(tmp, "B", nodes=[U1]))
            back = B["bootstrap"](eng_a)
        self.assertEqual(first["snapshot"]["revision"], back["snapshot"]["revision"])
        self.assertEqual(first["graph"]["revision"], back["graph"]["revision"])

    def test_each_context_names_its_own_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = B["bootstrap"](new_eng(tmp, "A", nodes=[N1]))
            b = B["bootstrap"](new_eng(tmp, "B", nodes=[U1]))
        self.assertNotEqual(a["engagement"]["resolved"], b["engagement"]["resolved"])


class B04_ReadOnly(unittest.TestCase):
    """Repetir bootstrap válido e em projecto sem grafo ->
    bytes/revisões INALTERADOS; modo legacy DECLARADO."""

    def test_bootstrap_writes_nothing_at_all(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp, nodes=[N1, U1])
            before = tree_hash(eng)
            B["bootstrap"](eng)
            B["bootstrap"](eng)
            after = tree_hash(eng)
        self.assertEqual(before, after, "o bootstrap escreveu (bytes ou mtime mudaram)")

    def test_bootstrap_writes_nothing_on_a_graphless_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            before = tree_hash(eng)
            B["bootstrap"](eng)
            after = tree_hash(eng)
        self.assertEqual(before, after, "criou grafo num projecto sem grafo")

    def test_it_does_not_create_the_graph(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            B["bootstrap"](eng)
            self.assertFalse((eng / "_graph").exists(), "o bootstrap criou `_graph/`")

    def test_legacy_mode_is_declared_not_silent(self):
        with tempfile.TemporaryDirectory() as tmp:
            boot = B["bootstrap"](new_eng(tmp))
        self.assertTrue(boot["ready"])
        self.assertTrue(boot["graph"]["legacy_mode"])
        codes = {l["code"] for l in boot["limitations"]}
        self.assertIn("LEGACY_MODE", codes, "modo legacy não foi declarado")

    def test_legacy_is_not_presented_as_migrated(self):
        with tempfile.TemporaryDirectory() as tmp:
            boot = B["bootstrap"](new_eng(tmp))
        lim = [l for l in boot["limitations"] if l["code"] == "LEGACY_MODE"][0]
        self.assertIn("não apresentado como migrado", lim["detail"])

    def test_repeating_gives_the_same_revisions(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp, nodes=[N1])
            a, b = B["bootstrap"](eng), B["bootstrap"](eng)
        self.assertEqual(a["snapshot"]["revision"], b["snapshot"]["revision"])
        self.assertEqual(a["graph"]["revision"], b["graph"]["revision"])


class B05_Truncagem(unittest.TestCase):
    """Orçamento que omite Unknown crítico antigo ->
    omissão EXPLÍCITA; nenhum gate liberado por excerto."""

    ITEMS = ([{"id": "U-{:03d}".format(i), "criticality": "critical", "text": "x"}
              for i in range(3)]
             + [{"id": "C-{:03d}".format(i), "criticality": "noncritical", "text": "y"}
                for i in range(10)])

    def test_critical_items_come_first(self):
        ctx = B["build_context"](self.ITEMS, budget=3)
        self.assertEqual([i["id"] for i in ctx["included"]], ["U-000", "U-001", "U-002"])

    def test_truncation_is_explicit(self):
        ctx = B["build_context"](self.ITEMS, budget=3)
        self.assertFalse(ctx["complete"])
        self.assertEqual(len(ctx["omitted"]), 10)
        self.assertIn("NÃO permite concluir", ctx["note"])

    def test_an_omitted_critical_is_named(self):
        ctx = B["build_context"](self.ITEMS, budget=1)
        self.assertEqual(ctx["omitted_critical"], ["U-001", "U-002"])

    def test_a_truncated_context_never_opens_a_gate(self):
        boot = {"ready": True, "context": B["build_context"](self.ITEMS, budget=3)}
        self.assertFalse(B["gate_open"](boot), "um excerto abriu um gate")

    def test_a_complete_context_does_open_the_gate(self):
        boot = {"ready": True, "context": B["build_context"](self.ITEMS, budget=99)}
        self.assertTrue(B["gate_open"](boot))

    def test_bootstrap_reports_the_truncation_as_a_limitation(self):
        nodes = [{"id": "U-{:03d}".format(i), "type": "question",
                  "props": {"state": "Unknown", "text": "q"}, "provenance": {}}
                 for i in range(5)]
        with tempfile.TemporaryDirectory() as tmp:
            boot = B["bootstrap"](new_eng(tmp, nodes=nodes), budget=2)
        codes = {l["code"] for l in boot["limitations"]}
        self.assertIn("CONTEXT_TRUNCATED", codes)
        self.assertFalse(B["gate_open"](boot))


class B06_Premissas(unittest.TestCase):
    """Regra cuja premissa/proveniência não cabe ou está quebrada ->
    dependência assinalada; conclusão LIMITADA."""

    def test_a_broken_dependency_is_flagged(self):
        items = [{"id": "R-1", "criticality": "critical", "depends_on": ["NAO-EXISTE"]}]
        ctx = B["build_context"](items)
        self.assertEqual(ctx["included"][0]["premise_broken"], ["NAO-EXISTE"])

    def test_a_broken_dependency_limits_the_conclusion(self):
        items = [{"id": "R-1", "criticality": "critical", "depends_on": ["NAO-EXISTE"]}]
        ctx = B["build_context"](items)
        self.assertIn("limitada", ctx["included"][0]["conclusion"])

    def test_a_dependency_pushed_out_by_the_budget_is_flagged_too(self):
        items = [{"id": "A-1", "criticality": "critical", "depends_on": ["Z-9"]},
                 {"id": "Z-9", "criticality": "noncritical"}]
        ctx = B["build_context"](items, budget=1)
        self.assertEqual(ctx["included"][0]["premise_omitted"], ["Z-9"])
        self.assertIn("fora do orçamento", ctx["included"][0]["conclusion"])

    def test_a_satisfied_dependency_is_not_flagged(self):
        items = [{"id": "A-1", "criticality": "critical", "depends_on": ["Z-9"]},
                 {"id": "Z-9", "criticality": "critical"}]
        ctx = B["build_context"](items, budget=9)
        self.assertNotIn("premise_broken", ctx["included"][0])
        self.assertNotIn("premise_omitted", ctx["included"][0])

    def test_provenance_travels_with_the_item(self):
        items = [{"id": "A-1", "provenance": {"lens": "data", "round": "R-01"}}]
        ctx = B["build_context"](items)
        self.assertEqual(ctx["included"][0]["provenance"], {"lens": "data", "round": "R-01"})


class B07_DerivaVersusCorrupcao(unittest.TestCase):
    """Locator quebrado -> deriva localizada, avisada.
    Estrutura corrompida -> NÃO usada como contexto válido."""

    def test_localised_drift_still_boots_with_a_warning(self):
        """Premissa quebrada é deriva: o contexto serve, a conclusão dependente não."""
        nodes = [dict(N1, props={"state": "Confirmed", "text": "t",
                                 "depends_on": ["SUMIU"]})]
        with tempfile.TemporaryDirectory() as tmp:
            boot = B["bootstrap"](new_eng(tmp, nodes=nodes))
        self.assertTrue(boot["ready"], "deriva localizada bloqueou tudo")
        self.assertIn("PREMISE_BROKEN", {l["code"] for l in boot["limitations"]})

    def test_structural_corruption_is_not_usable_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp, nodes=[N1])
            (eng / "_graph" / "graph.jsonl").write_text("{corrompido\n", encoding="utf-8")
            boot = B["bootstrap"](eng)
        self.assertFalse(boot["ready"])
        self.assertEqual(boot["context"], {}, "construiu contexto sobre grafo corrompido")

    def test_corruption_is_not_legacy_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp, nodes=[N1])
            (eng / "_graph" / "meta.json").unlink()
            boot = B["bootstrap"](eng)
        self.assertFalse(boot["graph"]["legacy_mode"],
                         "um par incoerente passou por modo legacy")
        lim = [l for l in boot["limitations"] if l.get("blocking")][0]
        self.assertIn("NÃO é modo legacy", lim["note"])

    def test_integrity_problems_block_the_context(self):
        bad = [N1, {"id": "E-1", "type": "claim", "props": {}, "provenance": {}}]
        with tempfile.TemporaryDirectory() as tmp:
            eng = Path(tmp) / "eng"
            (eng / "_graph").mkdir(parents=True)
            body, meta = G["serialize"](bad, [{"src": "C-001", "rel": "r", "dst": "FANTASMA"}])
            (eng / "_graph" / "graph.jsonl").write_text(body, encoding="utf-8")
            (eng / "_graph" / "meta.json").write_text(meta, encoding="utf-8")
            boot = B["bootstrap"](eng)
        self.assertFalse(boot["ready"])
        self.assertIn("GRAPH_INTEGRITY", {l["code"] for l in boot["limitations"]})

    def test_the_two_are_distinguishable(self):
        """A afirmação do caso: deriva e corrupção não colapsam no mesmo estado."""
        with tempfile.TemporaryDirectory() as tmp:
            drift = B["bootstrap"](new_eng(tmp, "A", nodes=[
                dict(N1, props={"state": "Confirmed", "depends_on": ["SUMIU"]})]))
            eng_b = new_eng(tmp, "B", nodes=[N1])
            (eng_b / "_graph" / "graph.jsonl").write_text("{x\n", encoding="utf-8")
            corrupt = B["bootstrap"](eng_b)
        self.assertTrue(drift["ready"])
        self.assertFalse(corrupt["ready"])


class B08_LinhaResolvidaNaoGastaOrcamentoComoCritica(unittest.TestCase):
    """`criticality` decide a prioridade no orcamento, e uma linha ja RESOLVIDA nao bloqueia.

    Medido no piloto de tickets depois de migrar: 4 dos 40 lugares de contexto estavam
    ocupados por `CF-001`, `CF-002`, `U-006` e `U-013` — todas resolvidas, todas ordenadas
    como criticas por `items_from_graph` olhar so ao estado. O orcamento gastava-se a
    repetir historia e empurrava para fora perguntas que continuam abertas: `omitted_critical`
    caiu de 19 para 10 quando isto passou a olhar tambem a `resolved`.

    A linha resolvida NAO desaparece — continua no conjunto, como nao-critica. O grafo e
    aditivo por contrato e descarta-la apagava proveniencia."""

    def no(self, nid, state, resolvida):
        return {"id": nid, "type": "claim",
                "props": {"state": state, "text": "t", "resolved": resolvida},
                "provenance": {}}

    def test_a_resolved_open_row_is_not_ranked_critical(self):
        itens = B["items_from_graph"]([self.no("U-001", "Unknown", True)])
        self.assertEqual(itens[0]["criticality"], "noncritical")
        self.assertTrue(itens[0]["resolved"])

    def test_an_unresolved_open_row_stays_critical(self):
        for estado in ("Unknown", "Conflicted", "Risky"):
            itens = B["items_from_graph"]([self.no("U-001", estado, False)])
            self.assertEqual(itens[0]["criticality"], "critical",
                             "{} por resolver continua a bloquear".format(estado))

    def test_the_resolved_row_is_kept_not_dropped(self):
        nodes = [self.no("U-001", "Unknown", True), self.no("U-002", "Unknown", False)]
        itens = B["items_from_graph"](nodes)
        self.assertEqual(sorted(i["id"] for i in itens), ["U-001", "U-002"],
                         "descartar apagava proveniencia; o grafo e aditivo")

    def test_a_closed_row_is_noncritical_whatever_resolved_says(self):
        for resolvida in (True, False):
            itens = B["items_from_graph"]([self.no("C-001", "Confirmed", resolvida)])
            self.assertEqual(itens[0]["criticality"], "noncritical")

    def test_the_budget_goes_to_what_is_still_open(self):
        """O efeito que se quer: com orcamento apertado, o que entra e o que bloqueia."""
        nodes = ([self.no("U-{:03d}".format(i), "Unknown", True) for i in range(1, 6)]
                 + [self.no("U-{:03d}".format(i), "Unknown", False) for i in range(6, 9)])
        ctx = B["build_context"](B["items_from_graph"](nodes), budget=3)
        entraram = {i["id"] for i in ctx["included"]}
        self.assertEqual(entraram, {"U-006", "U-007", "U-008"},
                         "as resolvidas nao podem empurrar as abertas para fora")
        self.assertEqual(ctx["omitted_critical"], [],
                         "nenhuma pergunta aberta ficou de fora")


if __name__ == "__main__":
    unittest.main(verbosity=2)
