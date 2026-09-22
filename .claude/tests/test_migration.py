# -*- coding: utf-8 -*-
"""M01-M06 — migracao explicita de engagements existentes (P5).

As fixtures sao sinteticas DE PROPOSITO: um conjunto que dependesse dos engagements em
`projects/` (gitignored) falharia para sempre num clone limpo — e o baseline do P0 ja
regista um teste assim. O engagement real e exercitado num teste que SALTA se ausente."""
import json
import runpy
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "library" / "kernel" / "tools"
M = runpy.run_path(str(TOOLS / "migrate.py"))
G = runpy.run_path(str(TOOLS / "graph.py"))
O = runpy.run_path(str(TOOLS / "operation.py"))

HEAD = """> Fase actual: Discovery

## Confirmed

| id | lens | claim | evidência | verificado_em | validade | ronda |
|---|---|---|---|---|---|---|
{confirmed}

## Assumed

| id | lens | claim | base da assumption | verificado_em | validade | ronda |
|---|---|---|---|---|---|---|
{assumed}

## Unknown

| id | lens | pergunta | quem responde | criticidade | custo | swing | ronda |
|---|---|---|---|---|---|---|---|
{unknown}

## Conflicted

| id | lens | conflito | partes | criticidade | ronda |
|---|---|---|---|---|---|
{conflicted}

## Risky

| id | lens | risco | impacto | mitigação proposta | ronda |
|---|---|---|---|---|---|
"""

NOVO = HEAD.format(
    confirmed="| C-001 | data | Base partilhada | inicial | 2026-01-01 | organizacional | R-01 |",
    assumed="", conflicted="",
    unknown="| U-001 | data | Quem e o dono? | role: dono dos dados | Critical | documento | dimensionante: muda o modelo | R-01 |")

# historia resolvida: U-001 resolveu em C-002 e A-001; decisao D-002 substitui D-001
RESOLVIDO = HEAD.format(
    confirmed=("| C-001 | data | Base partilhada | inicial | 2026-01-01 | organizacional | R-01 |\n"
               "| C-002 | data | O dono e a equipa de dados | USER_ANSWER 2026-02-01 (was U-001), answers.md#U-001 | 2026-02-01 | organizacional | R-01 |"),
    assumed="| A-001 | data | Ha um processo de acesso informal | inferido (was U-001) | 2026-02-01 | organizacional | R-01 |",
    unknown="| U-001 | data | Quem e o dono? | role: dono dos dados | Critical | documento | dimensionante: muda o modelo | R-01 — resolved -> C-002, A-001 |",
    conflicted="| X-001 | governance | Duas versoes do horario | role: Operacoes / fonte: contrato | Med | R-01 |")

# ambiguidades: `quem responde` sem prefixo; resolvida sem sucessor
AMBIGUO = HEAD.format(
    confirmed="| C-001 | data | Base partilhada | inicial | 2026-01-01 | organizacional | R-01 |",
    assumed="",
    unknown=("| U-001 | data | Quem e o dono? | o Joao da equipa | Critical | documento | dimensionante: muda o modelo | R-01 |\n"
             "| U-002 | ops | Qual o corte? | role: Operacoes | Med | email | so detalhe | R-01 — resolved -> C-999 |"),
    conflicted="")

DECISIONS = """# Decisoes

## D-001 — Primeira escolha

Escolha inicial.

## D-002 — Substitui a anterior

**Supersedes**: D-001

Escolha revista.
"""


def make(tmp, su, name="eng", decisions=DECISIONS):
    eng = Path(tmp) / name
    eng.mkdir(parents=True, exist_ok=True)
    (eng / "shared-understanding.md").write_text(su, encoding="utf-8", newline="\n")
    (eng / "answers.md").write_text("# Respostas\n\n## U-001\n\n> literal\n",
                                    encoding="utf-8", newline="\n")
    (eng / "decisions.md").write_text(decisions, encoding="utf-8", newline="\n")
    (eng / "_state.json").write_text('{"phase":"discovery","round":"R-01"}\n',
                                     encoding="utf-8", newline="\n")
    return eng


def tree(root):
    return {str(p.relative_to(root)): p.read_bytes()
            for p in sorted(Path(root).rglob("*")) if p.is_file()}


class M01_DryRun(unittest.TestCase):
    """Migrar em ensaio -> SEM alteracao do engagement; mapa completo origem/destino."""

    def test_dry_run_changes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make(tmp, RESOLVIDO)
            before = tree(eng)
            M["dry_run"](eng)
            self.assertEqual(before, tree(eng), "o ensaio escreveu no engagement")

    def test_dry_run_creates_no_migration_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make(tmp, RESOLVIDO)
            M["dry_run"](eng)
            self.assertFalse((eng / "_migration").exists(),
                             "o ensaio criou `_migration/` no snapshot")

    def test_the_map_covers_every_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = M["dry_run"](make(tmp, RESOLVIDO))
        self.assertEqual(len(plan["mapping"]), plan["rows"])
        self.assertEqual(sum(plan["counts"].values()), plan["rows"])

    def test_each_entry_names_source_and_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = M["dry_run"](make(tmp, NOVO))
        for m in plan["mapping"]:
            self.assertTrue(m["source"].startswith("shared-understanding.md#"))
            if m["class"] == M["PROJECTABLE"]:
                self.assertTrue(m["destination"].startswith("graph:node:"))

    def test_the_report_lives_outside_the_snapshot(self):
        """C1: o relatorio e devolvido, nao gravado no engagement."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = make(tmp, RESOLVIDO)
            plan = M["dry_run"](eng)
            self.assertIsInstance(plan, dict)
            self.assertEqual([p for p in eng.rglob("*") if "migration" in p.name], [])


class M02_Historico(unittest.TestCase):
    """Projecto com resolved, pressupostos, conflitos e decisao substituida ->
    MESMOS ids, relacoes, estados e decisao ACTIVA."""

    def test_ids_and_states_survive(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make(tmp, RESOLVIDO)
            M["apply"](eng)
            st = G["read"](eng)
        by = {n["id"]: n for n in st["nodes"]}
        for rid, state in (("C-001", "Confirmed"), ("C-002", "Confirmed"),
                           ("A-001", "Assumed"), ("U-001", "Unknown"), ("X-001", "Conflicted")):
            self.assertIn(rid, by, "{} perdeu-se na migracao".format(rid))
            self.assertEqual(by[rid]["props"]["state"], state)

    def test_the_resolution_chain_becomes_edges(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make(tmp, RESOLVIDO)
            M["apply"](eng)
            st = G["read"](eng)
        was = {(e["src"], e["dst"]) for e in st["edges"] if e["rel"] == "was"}
        self.assertIn(("C-002", "U-001"), was)
        self.assertIn(("A-001", "U-001"), was, "a cadeia para o Assumed perdeu-se")

    def test_resolved_rows_are_not_reopened(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make(tmp, RESOLVIDO)
            M["apply"](eng)
            st = G["read"](eng)
        u = [n for n in st["nodes"] if n["id"] == "U-001"][0]
        self.assertTrue(u["props"]["resolved"], "uma linha resolvida foi reaberta")

    def test_the_active_decision_is_the_one_not_superseded(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = M["dry_run"](make(tmp, RESOLVIDO))
        self.assertEqual(plan["decisions"]["active"], "D-002")
        self.assertIn("D-001", plan["decisions"]["superseded"])

    def test_authority_is_preserved_verbatim(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make(tmp, RESOLVIDO)
            M["apply"](eng)
            st = G["read"](eng)
        u = [n for n in st["nodes"] if n["id"] == "U-001"][0]
        self.assertEqual(u["provenance"]["support"], "role: dono dos dados")


class M03_Repeticao(unittest.TestCase):
    """Reexecutar migracao concluida -> no-op, sem duplicacao."""

    def test_second_apply_is_a_no_op(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make(tmp, RESOLVIDO)
            M["apply"](eng)
            again = M["apply"](eng)
        self.assertEqual(again["result"], "no_op")

    def test_nothing_changes_on_the_second_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make(tmp, RESOLVIDO)
            M["apply"](eng)
            snap = tree(eng / "_graph")
            M["apply"](eng)
            self.assertEqual(snap, tree(eng / "_graph"))

    def test_no_duplicate_nodes(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make(tmp, RESOLVIDO)
            M["apply"](eng)
            M["apply"](eng)
            st = G["read"](eng)
        ids = [n["id"] for n in st["nodes"]]
        self.assertEqual(len(ids), len(set(ids)))


class M04_Ambiguidade(unittest.TestCase):
    """Linhas incompativeis ou sem origem verificavel ->
    excepcoes EXPLICITAS, sem confirmacao inventada."""

    def test_an_owner_without_a_prefix_is_ambiguous(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = M["dry_run"](make(tmp, AMBIGUO))
        u1 = [m for m in plan["mapping"] if m["id"] == "U-001"][0]
        self.assertEqual(u1["class"], M["AMBIGUOUS"])
        self.assertIn("sem prefixo", u1["reason"])

    def test_resolved_to_a_successor_that_does_not_exist_is_ambiguous(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = M["dry_run"](make(tmp, AMBIGUO))
            u2 = [m for m in plan["mapping"] if m["id"] == "U-002"][0]
            self.assertEqual(u2["class"], M["AMBIGUOUS"], u2["reason"])
            self.assertIn("C-999", u2["reason"])

    def test_exceptions_are_listed_explicitly(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = M["dry_run"](make(tmp, AMBIGUO))
        self.assertEqual(len(plan["exceptions"]), 2)
        self.assertFalse(plan["complete"])

    def test_an_ambiguous_row_is_not_projected_as_fact(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make(tmp, AMBIGUO)
            M["apply"](eng)
            st = G["read"](eng)
        ids = {n["id"] for n in st["nodes"]}
        self.assertNotIn("U-001", ids, "uma linha ambigua foi projectada na mesma")

    def test_a_migration_with_exceptions_does_not_declare_full_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = M["apply"](make(tmp, AMBIGUO))
        self.assertFalse(out["success_declared"])
        self.assertIn("PARCIAL", out["note"])


class M05_Restore(unittest.TestCase):
    """Reverter na revisao pos-migracao sem trabalho novo ->
    hashes originais restaurados; ficheiros alheios preservados."""

    def test_restore_reproduces_the_original_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make(tmp, RESOLVIDO)
            before = {k: v for k, v in tree(eng).items()}
            M["apply"](eng)
            out = M["restore"](eng)
            self.assertEqual(out["result"], "restored")
            for rel in ("shared-understanding.md", "answers.md", "decisions.md", "_state.json"):
                self.assertEqual(tree(eng)[rel], before[rel], "`{}` nao voltou".format(rel))

    def test_only_new_files_are_removed(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make(tmp, RESOLVIDO)
            alheio = eng / "ficheiro-do-utilizador.md"
            alheio.write_text("nao mexer\n", encoding="utf-8")
            M["apply"](eng)
            M["restore"](eng)
            self.assertTrue(alheio.exists(), "um ficheiro alheio foi removido")
            self.assertEqual(alheio.read_text(encoding="utf-8"), "nao mexer\n")

    def test_the_graph_created_by_the_migration_is_gone(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make(tmp, RESOLVIDO)
            M["apply"](eng)
            M["restore"](eng)
            st = G["read"](eng)
        self.assertEqual(st["status"], G["ABSENT"])

    def test_a_corrupt_backup_refuses_the_restore(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make(tmp, RESOLVIDO)
            M["apply"](eng)
            b = eng / "_migration" / "backup" / "shared-understanding.md"
            b.write_text("corrompido\n", encoding="utf-8")
            with self.assertRaises(M["MigrationError"]) as ctx:
                M["restore"](eng)
        self.assertEqual(ctx.exception.code, "BACKUP_CORRUPT")


class M06_TrabalhoPosterior(unittest.TestCase):
    """Rollback apos nova resposta, e falha a meio ->
    restore cego RECUSADO; trabalho preservado; pendencia recuperavel."""

    def test_blind_restore_is_refused_after_new_work(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make(tmp, RESOLVIDO)
            M["apply"](eng)
            O["run"](eng, "trabalho-novo", {"answers.md": "# Respostas\n\n## U-009\n\n> nova\n"})
            with self.assertRaises(M["MigrationError"]) as ctx:
                M["restore"](eng)
        self.assertEqual(ctx.exception.code, "WORK_AFTER")

    def test_the_new_work_is_preserved_when_the_restore_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make(tmp, RESOLVIDO)
            M["apply"](eng)
            O["run"](eng, "trabalho-novo", {"answers.md": "# Respostas\n\n## U-009\n\n> nova\n"})
            try:
                M["restore"](eng)
            except M["MigrationError"]:
                pass
            self.assertIn("U-009", (eng / "answers.md").read_text(encoding="utf-8"),
                          "o trabalho novo foi perdido")

    def test_the_refusal_names_what_changed(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make(tmp, RESOLVIDO)
            M["apply"](eng)
            O["run"](eng, "t", {"answers.md": "x\n"})
            try:
                M["restore"](eng)
                self.fail("nao recusou")
            except M["MigrationError"] as exc:
                self.assertIn("answers.md", exc.detail["changed"])

    def test_a_stale_plan_is_rejected(self):
        """C1: entrada mudou depois do ensaio -> recalcular, nao aplicar o plano velho."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = make(tmp, RESOLVIDO)
            plan = M["dry_run"](eng)
            O["run"](eng, "mexeu", {"answers.md": "mudou\n"})
            with self.assertRaises(M["MigrationError"]) as ctx:
                M["apply"](eng, plan)
        self.assertEqual(ctx.exception.code, "PLAN_STALE")

    def test_a_pending_operation_is_recoverable_after_a_half_migration(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = make(tmp, RESOLVIDO)
            O["_atomic_write"](O["pending_path"](eng), json.dumps(
                {"intent_version": 1, "operation_id": "meio", "request_hash": "h", "owner": {},
                 "before": {}, "after": {}, "staging": "_ops/staging/meio"}))
            (eng / "_ops" / "staging" / "meio").mkdir(parents=True)
            self.assertFalse(O["gate_open"](eng))
            self.assertEqual(O["recover"](eng)["result"], "rolled_forward")
            self.assertTrue(O["gate_open"](eng))


class EngagementReal(unittest.TestCase):
    """O ensaio contra um engagement verdadeiro, quando existe. SALTA se ausente."""

    ENG = ROOT / "projects" / "pricing-bunkers-pilot-4"

    def test_dry_run_on_a_real_engagement_changes_nothing(self):
        if not (self.ENG / "shared-understanding.md").exists():
            self.skipTest("engagement real ausente (projects/ e gitignored)")
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "real"
            shutil.copytree(self.ENG, copy)
            before = tree(copy)
            plan = M["dry_run"](copy)
            self.assertEqual(before, tree(copy), "o ensaio escreveu num engagement real")
        self.assertGreater(plan["rows"], 0)
        self.assertEqual(sum(plan["counts"].values()), plan["rows"])


class M07_ReAplicarDepoisDeReverter(unittest.TestCase):
    """O defeito que nenhum destes 28 testes apanhava, porque nenhum fazia o ciclo inteiro.

    `apply` -> `restore` -> `apply`. O id da operacao e `migrate-<plan_hash[:16]>`, e o
    `plan_hash` deriva dos digests PRE-migracao. Depois de reverter, o estado volta a ser o
    de antes, o plano volta a dar o mesmo hash, e o coordenador reconhecia o recibo antigo:
    devolvia sucesso sem escrever nada, e `apply` respondia `migrated` sobre um grafo
    AUSENTE. `ACCEPTANCE.md` §2 — «Zero sucesso falso de operacao interrompida/rejeitada».

    Encontrado a correr o ciclo sobre o engagement real, nao por um teste vermelho."""

    def ciclo(self, tmp):
        eng = make(tmp, RESOLVIDO)
        M["apply"](eng)
        return eng

    def test_the_graph_is_really_there_after_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = self.ciclo(tmp)
            st = G["read"](eng)
            self.assertEqual(st["status"], G["OK"])
            self.assertGreater(len(st["nodes"]), 0)

    def test_restore_takes_the_graph_away_and_the_receipt_with_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = self.ciclo(tmp)
            op = M["read_manifest"](eng)["operation_id"]
            self.assertTrue(O["receipt_path"](eng, op).is_file(), "o apply deixa recibo")
            M["restore"](eng)
            self.assertEqual(G["read"](eng)["status"], G["ABSENT"])
            self.assertFalse(O["receipt_path"](eng, op).is_file(),
                             "reverter desfaz a operacao: o recibo dela nao pode sobreviver")

    def test_reapplying_after_a_restore_really_writes_the_graph(self):
        """O caso do defeito. Antes da correccao isto dava `migrated` com grafo ausente."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = self.ciclo(tmp)
            revisao1 = G["read"](eng)["revision"]
            M["restore"](eng)
            r = M["apply"](eng)
            st = G["read"](eng)
        self.assertEqual(r["result"], "migrated")
        self.assertEqual(st["status"], G["OK"], "dizer `migrated` sobre grafo ausente e mentira")
        self.assertGreater(len(st["nodes"]), 0)
        self.assertEqual(st["revision"], revisao1,
                         "a mesma entrada da a mesma revisao — a serializacao e canonica")

    def test_a_receipt_left_behind_makes_apply_refuse_instead_of_lying(self):
        """Defesa em profundidade: se o recibo sobreviver por outra via, `apply` recusa."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = self.ciclo(tmp)
            op = M["read_manifest"](eng)["operation_id"]
            guardado = O["receipt_path"](eng, op).read_text(encoding="utf-8")
            M["restore"](eng)
            # o recibo volta a aparecer sem os ficheiros que ele diz ter publicado
            rp = O["receipt_path"](eng, op)
            rp.parent.mkdir(parents=True, exist_ok=True)
            rp.write_text(guardado, encoding="utf-8")
            with self.assertRaises(M["MigrationError"]) as ctx:
                M["apply"](eng)
        self.assertEqual(ctx.exception.code, "RECEIPT_STALE")
        self.assertIn("restore", str(ctx.exception))

    def test_the_coordinator_reports_whether_the_effects_survived(self):
        """A peca generica: um recibo diz que aconteceu, nao que sobreviveu."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = Path(tmp) / "e"
            eng.mkdir()
            ws = {"x.txt": "conteudo\n"}
            primeiro = O["run"](eng, "op-1", ws)
            self.assertNotIn("replayed", primeiro)

            repetido = O["run"](eng, "op-1", ws)
            self.assertTrue(repetido["replayed"])
            self.assertTrue(repetido["effects_present"], "os ficheiros ainda la estao")

            (eng / "x.txt").unlink()
            depois = O["run"](eng, "op-1", ws)
            self.assertTrue(depois["replayed"])
            self.assertFalse(depois["effects_present"],
                             "o ficheiro desapareceu: o recibo ja nao descreve a realidade")


if __name__ == "__main__":
    unittest.main(verbosity=2)
