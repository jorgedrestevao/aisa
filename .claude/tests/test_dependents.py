# -*- coding: utf-8 -*-
"""W6 — quem cita o que, calculado do que já está escrito (P7.5).

O projecto decidiu **não** ter registo de dependências: `aisa-answer` passo 7 remata «No
dependency graph, no registry» e manda encontrar os dependentes por grep dos ids nos
artefactos derivados. Medido nos dois pilotos, esse método tem muito que encontrar — 100 de
117 linhas citadas em 17 ficheiros no piloto de tickets, 89 delas em mais do que um.

Então isto não constrói registo nenhum: constrói o índice inverso que o grep já implicava,
calculado a pedido e guardado em lado nenhum. O que muda é deixar de depender de o agente
se lembrar de seis padrões de ficheiro.

O que **não** faz, e não pode: dizer que o artefacto está errado. Citar uma linha que mudou
é suspeita, não prova de anterioridade — nenhum derivado regista contra que valores foi
escrito. O motor produz candidatos; o julgamento fica onde o projecto o põe.

Mutantes escritos antes destes testes, como no W5."""
import runpy
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "library" / "kernel" / "tools"
R = runpy.run_path(str(TOOLS / "resolve.py"))
G = runpy.run_path(str(TOOLS / "graph.py"))

SU = """> Fase actual: Options

## Confirmed

| id | lens | claim | evidência | verificado_em | validade | ronda |
|---|---|---|---|---|---|---|
| C-001 | data | facto um | fonte: x | 2026-01-01 | organizacional | R-01 |
| C-010 | data | facto dez | fonte: x | 2026-01-01 | organizacional | R-01 |

## Assumed

| id | lens | claim | base da assumption | verificado_em | validade | ronda |
|---|---|---|---|---|---|---|
| A-002 | user | suposicao | base: y | 2026-01-01 | organizacional | R-01 |

## Unknown

| id | lens | pergunta | quem responde | criticidade | custo | swing | ronda |
|---|---|---|---|---|---|---|---|
| U-007 | data | pergunta aberta | role: dono | Critical | reuniao | dimensionante: muda o modelo | R-01 |

## Conflicted

| id | lens | conflito | partes | criticidade | ronda |
|---|---|---|---|---|---|

## Risky

| id | lens | risco | impacto | mitigação proposta | ronda |
|---|---|---|---|---|---|
"""


def eng_com(tmp, **ficheiros):
    eng = Path(tmp) / "eng"
    eng.mkdir(parents=True, exist_ok=True)
    (eng / "shared-understanding.md").write_text(SU, encoding="utf-8", newline="\n")
    (eng / "_state.json").write_text('{"phase":"options","round":"O-01"}\n',
                                     encoding="utf-8", newline="\n")
    for rel, texto in ficheiros.items():
        alvo = eng / rel
        alvo.parent.mkdir(parents=True, exist_ok=True)
        alvo.write_text(texto, encoding="utf-8", newline="\n")
    return eng


class W6a_OIndiceInverso(unittest.TestCase):
    """`cited_by` lê o que está escrito; não inventa nem esquece."""

    def test_a_row_cited_in_one_file_is_found_there(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_com(tmp, **{"frame.md": "o enquadramento assenta em C-001.\n"})
            idx = R["cited_by"](eng)
        self.assertEqual(idx["C-001"], ["frame.md"])

    def test_a_row_cited_nowhere_maps_to_an_empty_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_com(tmp, **{"frame.md": "so cita C-001.\n"})
            idx = R["cited_by"](eng)
        self.assertEqual(idx["U-007"], [],
                         "um id sem citações não pode ganhar uma")

    def test_every_derived_family_is_walked(self):
        """Guarda contra encolher `DERIVED_GLOBS` sem ninguém dar por isso."""
        familias = {
            "frame.md": "C-001", "options.md": "C-001", "decisions.md": "C-001",
            "story.md": "C-001", "_synthesis/as-is.md": "C-001",
            "_blueprint/ux-blueprint_v01.yaml": "su_refs: [C-001]",
            "_simulation/counterfactuals/O-001.md": "C-001",
            "_render/eng_estimate_v01.md": "C-001",
        }
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_com(tmp, **familias)
            idx = R["cited_by"](eng)
        self.assertEqual(sorted(idx["C-001"]), sorted(familias),
                         "uma família de derivados deixou de ser percorrida")

    def test_the_su_itself_is_never_a_citation(self):
        """A linha cita-se a si própria na SU. Isso não é dependência."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_com(tmp)                       # sem nenhum derivado
            idx = R["cited_by"](eng)
        self.assertEqual({i: fs for i, fs in idx.items() if fs}, {},
                         "a SU entrou como derivado e deu cobertura falsa")
        self.assertNotIn("shared-understanding.md", R["DERIVED_GLOBS"])

    def test_an_id_does_not_match_inside_a_longer_token(self):
        """A fronteira, com o par que a exerce mesmo.

        A primeira versão deste caso usava `C-001` contra `C-010` — e nenhum dos dois cabe
        dentro do outro, por isso não distinguia nada e deixou passar o mutante que remove
        a fronteira. Com ids de três dígitos, quem colide é um token MAIS LONGO que contém
        o id: `C-001-bis`, `C-001a`, `xC-001`."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_com(tmp, **{
                "frame.md": "revisto como C-001-bis; ver tambem C-001a e xC-001.\n",
                "options.md": "aqui sim, C-001 sozinho.\n"})
            idx = R["cited_by"](eng)
        self.assertEqual(idx["C-001"], ["options.md"],
                         "`C-001` casou dentro de um token mais longo")

    def test_a_shorter_and_a_longer_id_do_not_mix(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_com(tmp, **{"frame.md": "isto fala de C-010 e de mais nada.\n"})
            idx = R["cited_by"](eng)
        self.assertEqual(idx["C-010"], ["frame.md"])
        self.assertEqual(idx["C-001"], [])

    def test_punctuation_around_the_id_does_not_hide_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_com(tmp, **{
                "options.md": "a razão (C-001), o risco [A-002] e `U-007`.\n"})
            idx = R["cited_by"](eng)
        for rid in ("C-001", "A-002", "U-007"):
            self.assertEqual(idx[rid], ["options.md"], rid + " ficou escondido")

    def test_the_index_is_computed_and_never_written(self):
        """«No registry» — nada é persistido."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_com(tmp, **{"frame.md": "C-001\n"})
            antes = sorted(p.name for p in eng.rglob("*") if p.is_file())
            R["cited_by"](eng)
            depois = sorted(p.name for p in eng.rglob("*") if p.is_file())
        self.assertEqual(antes, depois, "o índice escreveu alguma coisa")


class W6b_OImpactoDeUmaAlteracao(unittest.TestCase):

    FICHEIROS = {"frame.md": "assenta em C-001 e A-002.\n",
                 "options.md": "a opção cita A-002.\n",
                 "_render/eng_estimate_v01.md": "estimativa sobre C-001.\n"}

    def test_it_names_the_files_that_cite_what_changed(self):
        with tempfile.TemporaryDirectory() as tmp:
            imp = R["impact_of"](eng_com(tmp, **self.FICHEIROS), ["A-002"])
        self.assertEqual(imp["cited_by"], {"A-002": ["frame.md", "options.md"]})
        self.assertEqual(imp["files"], ["frame.md", "options.md"])

    def test_it_says_when_what_changed_is_cited_nowhere(self):
        with tempfile.TemporaryDirectory() as tmp:
            imp = R["impact_of"](eng_com(tmp, **self.FICHEIROS), ["U-007"])
        self.assertEqual(imp["not_cited"], ["U-007"])
        self.assertEqual(imp["files"], [])

    def test_it_reports_only_what_changed_not_the_whole_su(self):
        """Revalidar tudo seria o mesmo que não revalidar nada."""
        with tempfile.TemporaryDirectory() as tmp:
            imp = R["impact_of"](eng_com(tmp, **self.FICHEIROS), ["A-002"])
        self.assertEqual(imp["changed"], ["A-002"])
        self.assertNotIn("C-001", imp["cited_by"],
                         "devolveu linhas que não mudaram")

    def test_it_carries_the_graph_successors_too(self):
        """A outra metade do impacto, que já existia em `dependents_of`."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_com(tmp, **self.FICHEIROS)
            nodes = [{"id": "A-002", "type": "su-row", "props": {}, "provenance": {}},
                     {"id": "C-050", "type": "su-row", "props": {}, "provenance": {}}]
            edges = [{"src": "C-050", "rel": "was", "dst": "A-002", "props": {},
                      "provenance": {}}]
            body, meta = G["serialize"](nodes, edges)
            (eng / "_graph").mkdir()
            (eng / "_graph" / "graph.jsonl").write_text(body, encoding="utf-8", newline="\n")
            (eng / "_graph" / "meta.json").write_text(meta, encoding="utf-8", newline="\n")
            imp = R["impact_of"](eng, ["A-002"])
        self.assertEqual(imp["successors"], ["C-050"],
                         "o sucessor no grafo não entrou no impacto")

    def test_an_absent_graph_is_not_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            imp = R["impact_of"](eng_com(tmp, **self.FICHEIROS), ["A-002"])
        self.assertEqual(imp["successors"], [])

    def test_the_verdict_says_it_is_a_suspicion_not_a_proof(self):
        """O limite honesto: nenhum derivado regista contra que valores foi escrito."""
        with tempfile.TemporaryDirectory() as tmp:
            imp = R["impact_of"](eng_com(tmp, **self.FICHEIROS), ["A-002"])
        self.assertIn("candidatos", imp["verdict"])
        self.assertIn("nao prova anterioridade", imp["verdict"])


class W6c_ContraOsPilotosReais(unittest.TestCase):
    """Medido: 100 de 117 linhas citadas no piloto de tickets, 89 em mais de um ficheiro."""

    def test_the_ticket_pilot_has_the_cross_references_the_method_needs(self):
        eng = ROOT / "projects" / "dpt-galp-jp-pilot-4"
        if not (eng / "shared-understanding.md").is_file():
            self.skipTest("engagement ausente neste ambiente")
        idx = R["cited_by"](eng)
        citadas = {i: fs for i, fs in idx.items() if fs}
        self.assertGreater(len(citadas), 50,
                           "quase nenhuma linha citada: ou o índice partiu, ou os "
                           "derivados desapareceram")
        multi = [i for i, fs in citadas.items() if len(fs) > 1]
        self.assertGreater(len(multi), 20,
                           "sem linhas citadas em vários ficheiros não há o que revalidar")

    def test_an_open_question_is_typically_cited_nowhere(self):
        """Uma pergunta por responder ainda não foi usada a jusante — e isso é informação."""
        eng = ROOT / "projects" / "dpt-galp-jp-pilot-4"
        if not (eng / "shared-understanding.md").is_file():
            self.skipTest("engagement ausente neste ambiente")
        imp = R["impact_of"](eng, ["U-001"])
        self.assertEqual(imp["cited_by"], {})
        self.assertEqual(imp["not_cited"], ["U-001"])


if __name__ == "__main__":
    unittest.main(verbosity=1)
