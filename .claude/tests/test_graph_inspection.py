# -*- coding: utf-8 -*-
"""E04 — inspecção completa do grafo (P8).

Caso: «Percorrer/exportar relações do projeto e abrir proveniência».
Esperado: «Acesso coerente às relações, sem links inventados para conectar componentes».

`ACCEPTANCE.md` §7 é mais explícita e é ela que estes testes afirmam: a inspecção mostra
relações recuperáveis, ligações a fontes e **componentes desconectados reais**; não se exige
que tudo seja um único componente nem se criam links fictícios; o contexto pode ser parcial
desde que export/traversal dêem acesso ao restante.

Cada classe afirma uma dessas frases. Nenhuma afirma o que o código faz."""
import json
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GRAPH_PY = ROOT / "library" / "kernel" / "tools" / "graph.py"
G = runpy.run_path(str(GRAPH_PY))


def eng_with(tmp, nodes=(), edges=()):
    eng = Path(tmp) / "eng"
    (eng / "_graph").mkdir(parents=True)
    body, meta = G["serialize"](list(nodes), list(edges))
    (eng / "_graph" / "graph.jsonl").write_text(body, encoding="utf-8", newline="\n")
    (eng / "_graph" / "meta.json").write_text(meta, encoding="utf-8", newline="\n")
    return eng


def no(nid, tipo="claim", **prov):
    return {"id": nid, "type": tipo, "props": {"state": "Confirmed"}, "provenance": dict(prov)}


def ar(src, rel, dst):
    return {"src": src, "rel": rel, "dst": dst, "props": {}, "provenance": {"ronda": "R-01"}}


# Duas ilhas REAIS: nada liga a cadeia de pricing à cadeia de acessos. É assim que o
# engagement está, e é assim que a inspecção o tem de mostrar.
ILHA_A = [no("C-001", provenance_lens="data"), no("U-002", "question"), no("C-003")]
ILHA_B = [no("C-010"), no("C-011")]
ARESTAS_A = [ar("C-003", "was", "U-002"), ar("U-002", "depends_on", "C-001")]
ARESTAS_B = [ar("C-011", "was", "C-010")]


class E04a_PercorrerRelacoes(unittest.TestCase):
    """Percorrer a partir de um nó devolve exactamente o que é alcançável — nem mais."""

    def test_traversal_reaches_the_real_neighbourhood(self):
        t = G["traverse"](ILHA_A + ILHA_B, ARESTAS_A + ARESTAS_B, "C-003")
        self.assertTrue(t["found"])
        self.assertEqual(t["reached"], ["C-001", "C-003", "U-002"],
                         "alcança a ilha inteira a partir de qualquer ponto dela")
        self.assertNotIn("C-010", t["reached"],
                         "a outra ilha NÃO é alcançável: percorrer não é inventar caminho")

    def test_traversal_walks_both_directions(self):
        """A relação `was` aponta do novo para o antigo; navegar só a favor perderia metade."""
        t = G["traverse"](ILHA_A, ARESTAS_A, "C-001")
        self.assertEqual(t["reached"], ["C-001", "C-003", "U-002"])

    def test_a_node_that_does_not_exist_is_not_invented(self):
        t = G["traverse"](ILHA_A, ARESTAS_A, "C-999")
        self.assertFalse(t["found"])
        self.assertEqual(t["reached"], [])
        self.assertIn("não se inventa", t["detail"])

    def test_a_relation_filter_narrows_without_inventing(self):
        t = G["traverse"](ILHA_A, ARESTAS_A, "C-003", rels=("was",))
        self.assertEqual(t["reached"], ["C-003", "U-002"],
                         "só a aresta `was` é seguida; `depends_on` fica por seguir")


class E04b_ComponentesDesconectadosSaoReais(unittest.TestCase):
    """«Não exigir que tudo seja um único componente nem criar links fictícios» (§7)."""

    def test_two_islands_are_reported_as_two(self):
        c = G["components"](ILHA_A + ILHA_B, ARESTAS_A + ARESTAS_B)
        self.assertEqual(len(c), 2, "dois componentes reais ficam dois")
        self.assertEqual(c[0], ["C-001", "C-003", "U-002"], "o maior primeiro, ordenado")
        self.assertEqual(c[1], ["C-010", "C-011"])

    def test_an_isolated_node_is_its_own_component_not_an_error(self):
        solto = no("C-020")
        c = G["components"](ILHA_A + [solto], ARESTAS_A)
        self.assertIn(["C-020"], c, "um nó sem arestas é um componente, não uma falha")

    def test_inspection_never_adds_an_edge_to_join_islands(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_with(tmp, ILHA_A + ILHA_B, ARESTAS_A + ARESTAS_B)
            antes = G["read"](eng)["revision"]
            vista = G["inspect"](eng)
            depois = G["read"](eng)["revision"]
        self.assertEqual(vista["component_count"], 2)
        self.assertEqual(vista["edges"], len(ARESTAS_A + ARESTAS_B),
                         "inspeccionar não acrescenta arestas")
        self.assertEqual(antes, depois, "a inspecção é read-only: a revisão não mexe")


class E04c_ContextoParcialDeclaraAFronteira(unittest.TestCase):
    """«Contexto pode ser parcial; export/traversal de debug permite acesso ao restante»."""

    def test_depth_limited_traversal_declares_what_is_left(self):
        t = G["traverse"](ILHA_A, ARESTAS_A, "C-003", depth=1)
        self.assertEqual(t["reached"], ["C-003", "U-002"])
        self.assertTrue(t["truncated"], "parar a meio declara-se")
        self.assertEqual(t["frontier"], ["U-002"], "e diz exactamente por onde continuar")
        self.assertIn("export", t["detail"])

    def test_a_complete_traversal_does_not_claim_truncation(self):
        t = G["traverse"](ILHA_A, ARESTAS_A, "C-003")
        self.assertFalse(t["truncated"])
        self.assertEqual(t["frontier"], [])

    def test_export_gives_access_to_the_rest_and_round_trips(self):
        nodes, edges = ILHA_A + ILHA_B, ARESTAS_A + ARESTAS_B
        e = G["export"](nodes, edges)
        self.assertEqual(e["nodes"], len(nodes))
        self.assertEqual(e["revision"], G["revision_of"](nodes, edges))
        voltou_n = [json.loads(l) for l in e["lines"] if json.loads(l)["kind"] == "node"]
        voltou_e = [json.loads(l) for l in e["lines"] if json.loads(l)["kind"] == "edge"]
        self.assertEqual(G["revision_of"](voltou_n, voltou_e), e["revision"],
                         "o que sai do export volta a dar a mesma revisão")


class E04d_AbrirProveniencia(unittest.TestCase):
    """«abrir proveniência» — e a ausência dela ser dita, não preenchida."""

    def test_provenance_opens_the_link_to_the_authority(self):
        n = no("C-100", answered_by="dono do processo", locator="folha Motor!B12",
               mirror_of="SU:C-100")
        p = G["provenance"]([n], [], "C-100")
        self.assertTrue(p["has_provenance"])
        self.assertEqual(p["authority"], "SU:C-100", "o espelho aponta à autoridade, que manda")
        chaves = [s["key"] for s in p["sources"]]
        self.assertEqual(chaves, ["mirror_of", "locator", "answered_by"],
                         "as ligações à fonte saem pela ordem do contrato")

    def test_a_node_without_provenance_says_so(self):
        p = G["provenance"]([no("C-101")], [], "C-101")
        self.assertFalse(p["has_provenance"])
        self.assertEqual(p["sources"], [], "sem fonte declarada não se fabrica uma")
        self.assertIn("sem proveniência", p["detail"])

    def test_provenance_of_an_absent_node_is_not_fabricated(self):
        p = G["provenance"](ILHA_A, ARESTAS_A, "C-999")
        self.assertFalse(p["found"])
        self.assertNotIn("provenance", p)


class E04e_PontaPendenteNaoViraNo(unittest.TestCase):
    """Uma aresta que aponta a um id inexistente é reportada, nunca materializada."""

    def test_dangling_end_is_reported_not_created(self):
        arestas = ARESTAS_A + [ar("C-001", "depends_on", "C-FANTASMA")]
        t = G["traverse"](ILHA_A, arestas, "C-001")
        self.assertEqual(t["dangling"], ["C-FANTASMA"])
        self.assertNotIn("C-FANTASMA", t["reached"],
                         "a ponta pendente não entra no alcançado como se fosse um nó")

    def test_integrity_and_inspection_agree_about_the_dangling_end(self):
        arestas = ARESTAS_A + [ar("C-001", "depends_on", "C-FANTASMA")]
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_with(tmp, ILHA_A, arestas)
            vista = G["inspect"](eng)
        codigos = [p["code"] for p in vista["integrity"]]
        self.assertIn("EDGE_END_UNKNOWN", codigos,
                      "a inspecção mostra a incoerência em vez de a coser")


class E04f_GrafoIlegivelNaoSeResume(unittest.TestCase):
    """Um store que não se lê declara-se; não se inspecciona por cima."""

    def test_absent_store_is_not_inspectable(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = Path(tmp) / "eng"
            eng.mkdir()
            vista = G["inspect"](eng)
        self.assertFalse(vista["inspectable"])
        self.assertEqual(vista["status"], G["ABSENT"])
        self.assertNotIn("components", vista, "não se listam componentes de um grafo que não há")

    def test_corrupt_store_reports_the_reason_and_nothing_else(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_with(tmp, ILHA_A, ARESTAS_A)
            (eng / "_graph" / "graph.jsonl").write_text("{ isto não é json\n", encoding="utf-8")
            vista = G["inspect"](eng)
        self.assertFalse(vista["inspectable"])
        self.assertEqual(vista["status"], G["INVALID_FORMAT"])
        self.assertTrue(vista["detail"], "a razão exacta sai; um grafo ilegível não se resume")


class E04g_PercorrivelSemEscreverPython(unittest.TestCase):
    """E04 é «percorrer/exportar» — tem de dar para fazer pela CLI, em processo real."""

    def corre(self, eng, *args):
        return subprocess.run([sys.executable, str(GRAPH_PY), *args,
                               "--engagement", str(eng)],
                              capture_output=True, text=True)

    def test_inspect_prints_the_components_as_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_with(tmp, ILHA_A + ILHA_B, ARESTAS_A + ARESTAS_B)
            p = self.corre(eng, "inspect", "--json")
            self.assertEqual(p.returncode, 0, p.stderr)
            out = json.loads(p.stdout)
        self.assertEqual(out["component_count"], 2)
        self.assertEqual(sorted(out["types"]), ["claim", "question"])
        self.assertEqual(out["relations"], ["depends_on", "was"])

    def test_inspect_from_a_node_carries_traversal_and_provenance(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_with(tmp, ILHA_A, ARESTAS_A)
            p = self.corre(eng, "inspect", "--json", "--start", "C-003", "--depth", "1")
            self.assertEqual(p.returncode, 0, p.stderr)
            out = json.loads(p.stdout)
        self.assertTrue(out["traversal"]["truncated"])
        self.assertEqual(out["traversal"]["frontier"], ["U-002"])
        self.assertTrue(out["provenance"]["found"])

    def test_export_emits_the_canonical_body_on_stdout(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_with(tmp, ILHA_A, ARESTAS_A)
            p = self.corre(eng, "export")
            self.assertEqual(p.returncode, 0, p.stderr)
            corpo = (eng / "_graph" / "graph.jsonl").read_text(encoding="utf-8")
        self.assertEqual(p.stdout, corpo, "o export é byte a byte o que está publicado")

    def test_export_of_an_unreadable_store_fails_loudly(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_with(tmp, ILHA_A, ARESTAS_A)
            (eng / "_graph" / "graph.jsonl").write_text("lixo\n", encoding="utf-8")
            p = self.corre(eng, "export")
        self.assertEqual(p.returncode, 1)
        self.assertEqual(p.stdout, "", "não sai meio grafo")
        self.assertIn("ilegivel", p.stderr)


class E04h_InspeccaoSobreOEngagementRealDoPiloto(unittest.TestCase):
    """O piloto real ainda não tem grafo — e a inspecção diz isso em vez de fingir."""

    def test_the_real_pilot_reports_legacy_mode_not_an_empty_graph(self):
        eng = ROOT / "projects" / "dpt-galp-jp-pilot-4"
        if not eng.is_dir():
            self.skipTest("engagement do piloto ausente neste ambiente")
        vista = G["inspect"](eng)
        self.assertIn(vista["status"], (G["ABSENT"], G["OK"]))
        if vista["status"] == G["ABSENT"]:
            self.assertFalse(vista["inspectable"])
            self.assertNotIn("component_count", vista,
                             "ausência de grafo não se apresenta como grafo de zero componentes")


if __name__ == "__main__":
    unittest.main(verbosity=1)
