# -*- coding: utf-8 -*-
"""W8 — o engagement nasce com grafo, e a ausência passa a bloquear (P7.5 §2).

A decisão de §2 tem duas metades e só valia metade: *«`LEGACY_MODE` desaparece como caminho
legítimo em runtime»*. A metade que faltava não é o bloqueio — é o que o bloqueio implica.
Medido a 2026-09-22: **nada fora de `graph.py` e `migrate.py` toca `_graph/`**. O `/start`
não criava grafo nenhum. Bloquear sobre ausência, sozinho, bloqueava todo o engagement novo
por um trabalho de migração que não existe — não há nada para migrar num engagement que
acabou de nascer.

Por isso são dois casos e não um: **nasce com grafo** (`migrate.init`) e **ausência bloqueia**
(`bootstrap`). Cada um sem o outro é uma armadilha.

`init` vive em `migrate.py`, não em `graph.py`: publicar é da camada de cima — `graph.py`
prepara bytes e não conhece o coordenador (contrato B2.4). E não é motor novo: é o caso
degenerado do que `migrate` já faz, migrar um engagement sem nada para migrar.

Mutantes escritos antes destes testes, como no W5, W6 e W7."""
import json
import runpy
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "library" / "kernel" / "tools"
M = runpy.run_path(str(TOOLS / "migrate.py"))
B = runpy.run_path(str(TOOLS / "bootstrap.py"))
G = runpy.run_path(str(TOOLS / "graph.py"))

SU = """# Shared Understanding — eng

> Fase actual: Discovery

## Confirmed

| id | lens | claim | evidência | verificado_em | validade | ronda |
|---|---|---|---|---|---|---|

## Assumed

| id | lens | claim | base da assumption | verificado_em | validade | ronda |
|---|---|---|---|---|---|---|

## Unknown

| id | lens | pergunta | quem responde | criticidade | custo | swing | ronda |
|---|---|---|---|---|---|---|---|

## Conflicted

| id | lens | conflito | partes | criticidade | ronda |
|---|---|---|---|---|---|

## Risky

| id | lens | risco | impacto | mitigação proposta | ronda |
|---|---|---|---|---|---|
"""


def novo_eng(tmp):
    """Um engagement como o `/start` o deixa **antes** do passo 9c: sem grafo."""
    eng = Path(tmp) / "eng"
    eng.mkdir(parents=True, exist_ok=True)
    (eng / "shared-understanding.md").write_text(SU, encoding="utf-8", newline="\n")
    (eng / "_state.json").write_text('{"phase":"discovery","round":"R-00"}\n',
                                     encoding="utf-8", newline="\n")
    return eng


class W8a_AAusenciaDeGrafoBloqueia(unittest.TestCase):
    """O que a §2 decidiu e não estava feito: deixar de ser um caminho."""

    def test_an_engagement_without_a_graph_is_not_ready(self):
        with tempfile.TemporaryDirectory() as tmp:
            boot = B["bootstrap"](novo_eng(tmp))
        self.assertFalse(boot["ready"],
                         "ausência de grafo continua a deixar avançar — a §2 dizia o contrário")

    def test_the_gate_never_opens_without_a_graph(self):
        with tempfile.TemporaryDirectory() as tmp:
            boot = B["bootstrap"](novo_eng(tmp))
        self.assertFalse(B["gate_open"](boot))

    def test_the_limitation_is_still_declared_by_name(self):
        """Bloquear não substitui declarar: quem lê tem de saber **o quê**."""
        with tempfile.TemporaryDirectory() as tmp:
            boot = B["bootstrap"](novo_eng(tmp))
        codigos = {l["code"] for l in boot["limitations"]}
        self.assertIn("LEGACY_MODE", codigos)

    def test_it_is_still_not_presented_as_migrated(self):
        with tempfile.TemporaryDirectory() as tmp:
            boot = B["bootstrap"](novo_eng(tmp))
        lim = [l for l in boot["limitations"] if l["code"] == "LEGACY_MODE"][0]
        self.assertIn("não apresentado como migrado", lim["detail"])
        self.assertTrue(lim.get("blocking"))

    def test_the_block_names_the_action_that_clears_it(self):
        """Um bloqueio sem acção nomeada é um beco. A §2 pedia «bloqueio com acção nomeada»."""
        with tempfile.TemporaryDirectory() as tmp:
            boot = B["bootstrap"](novo_eng(tmp))
        lim = [l for l in boot["limitations"] if l["code"] == "LEGACY_MODE"][0]
        self.assertIn("migrate.py", lim.get("recovery", ""),
                      "bloqueia e não diz o que fazer a seguir")

    def test_absence_is_not_reported_as_corruption_either(self):
        """B07 vale nas duas direcções. Ausência bloqueia — mas não vira avaria, senão a
        acção nomeada passa a ser a errada: `migrate` resolve legado, não um ficheiro
        partido."""
        with tempfile.TemporaryDirectory() as tmp:
            boot = B["bootstrap"](novo_eng(tmp))
        codigos = [l["code"] for l in boot["limitations"]]
        self.assertEqual(codigos, ["LEGACY_MODE"],
                         "a ausência arrastou outra limitação atrás: " + str(codigos))
        self.assertNotIn("inutilizável", json.dumps(boot["limitations"], ensure_ascii=False),
                         "ausência apresentada como grafo inutilizável")

    def test_corruption_still_says_something_else(self):
        """B07 intacto: partido não é ausente, e `migrate` não é a acção que o resolve."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = novo_eng(tmp)
            (eng / "_graph").mkdir()
            (eng / "_graph" / "graph.jsonl").write_text("{", encoding="utf-8")
            boot = B["bootstrap"](eng)
        codigos = {l["code"] for l in boot["limitations"]}
        self.assertFalse(boot["ready"])
        self.assertNotIn("LEGACY_MODE", codigos,
                         "um grafo partido foi apresentado como ausência")


class W8b_ONascimento(unittest.TestCase):
    """`migrate.init` — o grafo com que um engagement nasce."""

    def test_a_new_engagement_becomes_ready_after_init(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = novo_eng(tmp)
            self.assertFalse(B["bootstrap"](eng)["ready"])
            M["init"](eng)
            boot = B["bootstrap"](eng)
        self.assertTrue(boot["ready"], "nasceu com grafo e continua bloqueado")
        self.assertTrue(B["gate_open"](boot))
        self.assertEqual([l["code"] for l in boot["limitations"]], [])

    def test_the_graph_it_creates_is_valid_and_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = novo_eng(tmp)
            M["init"](eng)
            st = G["read"](eng)
        self.assertEqual(st["status"], G["OK"])
        self.assertEqual((len(st["nodes"]), len(st["edges"])), (0, 0))
        self.assertEqual(G["validate"](st["nodes"], st["edges"]), [])

    def test_it_goes_through_the_coordinator_and_leaves_a_receipt(self):
        """Nascer é uma operação como as outras — não uma escrita à margem."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = novo_eng(tmp)
            out = M["init"](eng)
            recibo = eng / "_ops" / "receipts" / "graph-init.json"
            self.assertTrue(recibo.is_file(), "publicou o grafo sem passar pelo coordenador")
            corpo = json.loads(recibo.read_text(encoding="utf-8"))
        self.assertEqual(out["operation_id"], "graph-init")
        self.assertEqual(corpo["result"], "committed")
        self.assertEqual(sorted(corpo["revision"]),
                         ["_graph/graph.jsonl", "_graph/meta.json"])

    def test_running_it_twice_changes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = novo_eng(tmp)
            a = M["init"](eng)
            rev_a = G["read"](eng).get("revision", "")
            b = M["init"](eng)
            rev_b = G["read"](eng).get("revision", "")
        self.assertEqual(a["result"], "created")
        self.assertEqual(b["result"], "already")
        self.assertEqual(rev_a, rev_b)

    def test_an_engagement_that_already_has_knowledge_is_not_emptied(self):
        """O caso que mataria um piloto migrado: `init` sobre um grafo com conteúdo."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = novo_eng(tmp)
            nodes = [{"kind": "node", "id": "C-001", "type": "su-row",
                      "props": {"state": "Confirmed"}, "provenance": {}}]
            corpo, meta = G["serialize"](nodes, [])
            (eng / "_graph").mkdir()
            (eng / "_graph" / "graph.jsonl").write_text(corpo, encoding="utf-8", newline="\n")
            (eng / "_graph" / "meta.json").write_text(meta, encoding="utf-8", newline="\n")
            out = M["init"](eng)
            st = G["read"](eng)
        self.assertEqual(out["result"], "already")
        self.assertEqual(len(st["nodes"]), 1, "apagou o grafo de um engagement migrado")

    def test_a_broken_graph_is_never_replaced_by_an_empty_one(self):
        """Substituir uma avaria por um vazio apagava a avaria — e o material com ela."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = novo_eng(tmp)
            (eng / "_graph").mkdir()
            (eng / "_graph" / "graph.jsonl").write_text("nao e json\n", encoding="utf-8")
            (eng / "_graph" / "meta.json").write_text('{"schema_version": 1}\n',
                                                      encoding="utf-8")
            with self.assertRaises(M["MigrationError"]) as ctx:
                M["init"](eng)
            restos = (eng / "_graph" / "graph.jsonl").read_text(encoding="utf-8")
        self.assertEqual(ctx.exception.code, "NOT_ABSENT")
        self.assertEqual(restos, "nao e json\n", "sobrescreveu o grafo partido")

    def test_an_incoherent_pair_is_refused_too(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = novo_eng(tmp)
            (eng / "_graph").mkdir()
            (eng / "_graph" / "meta.json").write_text('{"schema_version": 1}\n',
                                                      encoding="utf-8")
            with self.assertRaises(M["MigrationError"]) as ctx:
                M["init"](eng)
        self.assertEqual(ctx.exception.code, "NOT_ABSENT")


class W8c_OQueOStartTemDeFazer(unittest.TestCase):
    """O passo só é enforçável porque o bloqueio existe: um engagement nascido sem grafo não
    avança. O texto da skill é a instrução; o bloqueio é a garantia."""

    SKILL = ROOT / ".claude" / "skills" / "aisa-start" / "SKILL.md"

    def test_start_is_told_to_create_the_graph(self):
        texto = self.SKILL.read_text(encoding="utf-8")
        self.assertIn("migrate.py init", texto,
                      "o /start não manda criar o grafo — o engagement nasce bloqueado")

    def test_the_instruction_says_it_is_not_optional(self):
        texto = self.SKILL.read_text(encoding="utf-8")
        bloco = texto[texto.index("migrate.py init") - 900:texto.index("migrate.py init") + 900]
        self.assertIn("Não é opcional", bloco)

    def test_an_engagement_born_without_the_step_cannot_proceed(self):
        """A garantia que não depende de texto nenhum."""
        with tempfile.TemporaryDirectory() as tmp:
            self.assertFalse(B["gate_open"](B["bootstrap"](novo_eng(tmp))))


if __name__ == "__main__":
    unittest.main(verbosity=1)
