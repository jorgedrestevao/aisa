# -*- coding: utf-8 -*-
"""O separador «Memória»: de que pergunta veio cada facto, e se a memória bate certo.

Não é «o grafo no dashboard», e a diferença é o que decide o desenho. Medido nos dois
pilotos antes de escrever uma linha:

    tickets   117 nós ·  9 arestas   (só `was`)
    pricing   108 nós · 25 arestas   (só `was`)

**0,08 arestas por nó.** Um diagrama nó-aresta disto é uma nuvem de pontos soltos, e
desenhá-lo a sério numa página sem bibliotecas custava um algoritmo de layout em SVG à mão.
Pior: os 117 nós espelham as 117 linhas da SU — listá-los duplicava o separador «Registo»
inteiro.

O que é NOVO e não está em lado nenhum:

- as cadeias `was` — `A-006 was U-004` é «este facto veio daquela pergunta». É o histórico
  de respostas, e hoje só existe enterrado na coluna da ronda;
- a saúde do espelho — linhas sem nó, nós que espelham uma linha que já não existe, campos
  divergentes. Zero nos dois pilotos, mas é exactamente o que bloqueia o engagement quando
  acontece;
- a revisão e a última operação — o que foi publicado, e quando.

Por isso o separador chama-se **Memória** e não «grafo»: P-13, o utilizador lê negócio."""
import json
import runpy
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "library" / "kernel" / "tools"
D = runpy.run_path(str(TOOLS / "dashboard.py"))
G = runpy.run_path(str(TOOLS / "graph.py"))
M = runpy.run_path(str(TOOLS / "migrate.py"))
R = runpy.run_path(str(TOOLS / "resolve.py"))
FIX = runpy.run_path(str(ROOT / ".claude" / "tests" / "test_migration.py"))


def eng_com_historia(tmp):
    """Um engagement migrado onde uma pergunta JÁ foi respondida — senão não há história."""
    eng = FIX["make"](tmp, FIX["NOVO"])
    M["apply"](eng)
    R["apply"](eng, row_id="U-001", answer_text="A equipa de dados.",
               answered_by={"role": "dono dos dados"}, locator="answers.md#U-001")
    return eng


def gera(eng):
    p = subprocess.run([sys.executable, str(TOOLS / "dashboard.py"),
                        "--engagement", str(eng), "--quiet", "--force"],
                       capture_output=True, text=True, timeout=300)
    return p, (eng / "dashboard.html").read_text(encoding="utf-8")


def painel(html, chave="memoria"):
    """O painel e nada mais.

    Fatiar um numero fixo de caracteres saia do painel para os seguintes e para o JSON
    embebido no fim da pagina — e um caso que assim afirmasse «isto nao aparece aqui»
    estava a olhar para outro sitio. Corta-se no `</section>` do proprio painel.
    """
    i = html.index('id="panel-{}"'.format(chave))
    return html[i:html.index("</section>", i)]


class M1_OModelo(unittest.TestCase):

    def test_the_model_carries_the_answer_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            modelo = D["build_model"](eng_com_historia(tmp), date.today())
        mem = modelo.get("memory")
        self.assertIsNotNone(mem, "o modelo não carrega a memória do projecto")
        cadeias = mem.get("history", [])
        self.assertTrue(cadeias, "respondeu a uma pergunta e a história ficou vazia")
        primeira = cadeias[0]
        for campo in ("from_id", "to_id", "from_text", "to_text", "to_state"):
            self.assertIn(campo, primeira, "falta `{}` na cadeia".format(campo))
        self.assertEqual(primeira["from_id"], "U-001")

    def test_the_history_carries_the_text_not_only_ids(self):
        """Um id sozinho não diz nada a quem lê (P-13)."""
        with tempfile.TemporaryDirectory() as tmp:
            modelo = D["build_model"](eng_com_historia(tmp), date.today())
        c = modelo["memory"]["history"][0]
        self.assertTrue(c["from_text"].strip(), "a pergunta de origem saiu sem texto")
        self.assertTrue(c["to_text"].strip(), "o facto saiu sem texto")

    def test_a_healthy_engagement_reports_no_problem(self):
        with tempfile.TemporaryDirectory() as tmp:
            modelo = D["build_model"](eng_com_historia(tmp), date.today())
        saude = modelo["memory"]["health"]
        self.assertEqual(saude["rows_without_node"], [])
        self.assertEqual(saude["nodes_without_row"], [])
        self.assertEqual(saude["diverging"], [])

    def test_a_row_with_no_node_is_named(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_com_historia(tmp)
            su = eng / "shared-understanding.md"
            texto = su.read_text(encoding="utf-8").replace(
                "| C-001 | data | Base partilhada | inicial | 2026-01-01 | organizacional | R-01 |",
                "| C-001 | data | Base partilhada | inicial | 2026-01-01 | organizacional | R-01 |\n"
                "| C-777 | data | Linha sem no | fonte: acta | 2026-03-01 | organizacional | R-02 |")
            su.write_text(texto, encoding="utf-8", newline="\n")
            modelo = D["build_model"](eng, date.today())
        self.assertIn("C-777", modelo["memory"]["health"]["rows_without_node"])

    def test_it_says_which_revision_it_is_reporting(self):
        with tempfile.TemporaryDirectory() as tmp:
            modelo = D["build_model"](eng_com_historia(tmp), date.today())
        self.assertTrue(modelo["memory"]["revision"],
                        "não diz sobre que revisão está a reportar")
        self.assertGreater(modelo["memory"]["operations"], 0,
                           "houve operações publicadas e a contagem é zero")

    def test_an_engagement_with_no_memory_is_not_an_error(self):
        """Sem grafo, a secção diz que não há — não rebenta nem inventa."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = FIX["make"](tmp, FIX["NOVO"])          # sem migrar
            modelo = D["build_model"](eng, date.today())
        self.assertEqual(modelo["memory"]["history"], [])
        self.assertFalse(modelo["memory"]["available"])


class M2_ASeparador(unittest.TestCase):

    def test_the_tab_exists_and_is_named_in_business_language(self):
        chaves = [k for k, _l, _t in D["TAB_SPEC"]]
        self.assertIn("memoria", chaves, "não há separador da memória")
        rotulo = [l for k, l, _t in D["TAB_SPEC"] if k == "memoria"][0]
        self.assertNotIn("grafo", rotulo.lower(), "o rótulo usa vocabulário de kernel")

    def test_the_page_shows_where_each_fact_came_from(self):
        with tempfile.TemporaryDirectory() as tmp:
            p, html = gera(eng_com_historia(tmp))
        self.assertEqual(p.returncode, 0)
        corpo = painel(html)
        self.assertIn("U-001", corpo, "a pergunta de origem não aparece")
        self.assertIn("A equipa de dados", corpo, "o facto não aparece")

    def test_the_panel_speaks_business(self):
        with tempfile.TemporaryDirectory() as tmp:
            _p, html = gera(eng_com_historia(tmp))
        corpo = painel(html)
        for termo in ("grafo", "mirror_of", "graph.jsonl", "drift", "provenance"):
            self.assertNotIn(termo, corpo.lower(),
                             "vocabulário de kernel na página: " + termo)

    def test_the_tab_counts_what_it_shows(self):
        with tempfile.TemporaryDirectory() as tmp:
            _p, html = gera(eng_com_historia(tmp))
        i = html.index('id="tab-memoria"')
        botao = html[i:i + 400]
        self.assertIn('class="cnt"', botao,
                      "o separador não diz quantas respostas tem, como os outros")

    def test_it_does_not_duplicate_the_registo_tab(self):
        """Listar os 117 nós era repetir o Registo inteiro noutro sítio."""
        with tempfile.TemporaryDirectory() as tmp:
            _p, html = gera(eng_com_historia(tmp))
        corpo = painel(html)
        # C-001 nunca foi respondida nem tem problema: não tem por que aparecer aqui
        self.assertNotIn("Base partilhada", corpo,
                         "está a listar linhas que não têm história nem problema")


class M3_ContraOsPilotosReais(unittest.TestCase):

    def test_the_real_pilot_has_history_to_show(self):
        eng = ROOT / "projects" / "pricing-bunkers-pilot-4"
        if not (eng / "_graph").is_dir():
            self.skipTest("piloto ausente neste ambiente")
        modelo = D["build_model"](eng, date.today())
        self.assertGreaterEqual(len(modelo["memory"]["history"]), 20,
                                "medido: 25 cadeias `was` neste piloto")
        self.assertEqual(modelo["memory"]["health"]["rows_without_node"], [],
                         "medido: 108/108 espelhadas")


if __name__ == "__main__":
    unittest.main(verbosity=1)
