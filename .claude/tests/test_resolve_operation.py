# -*- coding: utf-8 -*-
"""L01-L05 — primeira operacao completa de negocio (P4).

A sequencia que o plano exige: resolver -> persistir -> TERMINAR A SESSAO ->
sessao nova sem historico -> mesmo estado, proveniencia e proximo passo.
A "sessao nova" e um subprocesso: processo novo, zero memoria."""
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

SU = """> Fase actual: Discovery

## Confirmed

| id | lens | claim | evidência | verificado_em | validade | ronda |
|---|---|---|---|---|---|---|
| C-001 | data | Os dados vivem numa base partilhada | inicial | 2026-01-01 | organizacional | R-01 |

## Assumed

| id | lens | claim | base da assumption | verificado_em | validade | ronda |
|---|---|---|---|---|---|---|

## Unknown

| id | lens | pergunta | quem responde | criticidade | custo | swing | ronda |
|---|---|---|---|---|---|---|---|
| U-001 | data | Quem e o dono da base partilhada? | role: dono dos dados | Critical | documento | dimensionante: muda o modelo de dados | R-01 |
| U-002 | operations | Qual o horario de corte? | role: Operacoes | Med | reuniao | so muda detalhe | R-01 |

## Conflicted

| id | lens | conflito | partes | criticidade | ronda |
|---|---|---|---|---|---|

## Risky

| id | lens | risco | impacto | mitigação proposta | ronda |
|---|---|---|---|---|---|
"""


def new_eng(tmp, name="eng"):
    eng = Path(tmp) / name
    eng.mkdir(parents=True, exist_ok=True)
    (eng / "shared-understanding.md").write_text(SU, encoding="utf-8", newline="\n")
    (eng / "answers.md").write_text("# Respostas\n", encoding="utf-8", newline="\n")
    (eng / "_state.json").write_text('{"phase":"discovery","round":"R-01"}\n',
                                     encoding="utf-8", newline="\n")
    return eng


def fresh_session(eng, expr):
    """Um processo NOVO le o engagement. Sem historico, sem memoria."""
    code = ("import runpy,json;"
            "G=runpy.run_path(r'{g}');B=runpy.run_path(r'{b}');R=runpy.run_path(r'{r}');"
            "eng=r'{e}';print(json.dumps({x}))").format(
        g=TOOLS / "graph.py", b=TOOLS / "bootstrap.py", r=TOOLS / "resolve.py",
        e=eng, x=expr)
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=120)
    if out.returncode != 0:
        raise AssertionError("sessao nova falhou: " + out.stderr[-600:])
    return json.loads(out.stdout)


class L01_ResolucaoInferida(unittest.TestCase):
    """Resolver U por inferencia, reiniciar sessao ->
    U permanece resolvido, sucessor Assumed activo, historico preservado."""

    def _resolve(self, eng):
        return R["apply"](eng, row_id="U-001", answer_text="Infiro que e a equipa de dados.",
                          answered_by={"role": "dono dos dados"}, inference=True,
                          today="2026-09-22")

    def test_inference_resolves_to_assumed_never_confirmed(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = self._resolve(new_eng(tmp))
        self.assertEqual(out["state"], "Assumed")
        self.assertIn("inferencia declarada", out["verdict"]["reason"])

    def test_after_a_fresh_session_the_unknown_is_still_resolved(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            out = self._resolve(eng)
            rows = fresh_session(eng, "R['read_su'](eng)[1]")
        u = [r for r in rows if r.get("id") == "U-001"][0]
        # `parse_su` move o marcador da ultima coluna para `resolved`/`resolved_to`
        self.assertEqual(str(u.get("resolved")), "True",
                         "a resolucao nao sobreviveu a sessao nova")
        self.assertIn(out["new_id"], str(u.get("resolved_to", "")))

    def test_the_assumed_successor_is_active_in_a_fresh_session(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            out = self._resolve(eng)
            rows = fresh_session(eng, "R['read_su'](eng)[1]")
        succ = [r for r in rows if r.get("id") == out["new_id"]]
        self.assertEqual(len(succ), 1, "o sucessor nao existe na sessao nova")

    def test_history_is_preserved_the_original_row_is_not_deleted(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            self._resolve(eng)
            md = (eng / "shared-understanding.md").read_text(encoding="utf-8")
        self.assertIn("| U-001 |", md, "a linha original foi apagada")
        self.assertIn("Quem e o dono da base partilhada?", md)

    def test_provenance_survives_in_the_graph(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            out = self._resolve(eng)
            st = fresh_session(eng, "G['read'](eng)")
        node = [n for n in st["nodes"] if n["id"] == out["new_id"]][0]
        self.assertEqual(node["provenance"]["lens"], "data")
        self.assertEqual(node["provenance"]["answered_by"], "dono dos dados")
        edge = [e for e in st["edges"] if e["src"] == out["new_id"]][0]
        self.assertEqual((edge["rel"], edge["dst"]), ("was", "U-001"))


class L02_Confirmacao(unittest.TestCase):
    """Resolver U com fonte valida e autoridade adequada ->
    resposta literal, locator, was/resolved e estado correctos."""

    def _resolve(self, eng):
        return R["apply"](eng, row_id="U-001",
                          answer_text="O dono e a equipa de dados, por delegacao formal.",
                          answered_by={"role": "dono dos dados"},
                          locator="answers.md#U-001", today="2026-09-22")

    def test_state_is_confirmed(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = self._resolve(new_eng(tmp))
        self.assertEqual(out["state"], "Confirmed")
        self.assertTrue(out["verdict"]["authority"]["matched"])

    def test_the_verbatim_answer_is_kept(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            self._resolve(eng)
            ans = (eng / "answers.md").read_text(encoding="utf-8")
        self.assertIn("O dono e a equipa de dados, por delegacao formal.", ans,
                      "a resposta literal perdeu-se")
        self.assertIn("## U-001", ans)

    def test_was_and_locator_are_in_the_evidence_cell(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            out = self._resolve(eng)
            md = (eng / "shared-understanding.md").read_text(encoding="utf-8")
        line = [l for l in md.splitlines() if l.startswith("| " + out["new_id"] + " ")][0]
        self.assertIn("was U-001", line)
        self.assertIn("answers.md#U-001", line)

    def test_the_original_is_marked_resolved(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            out = self._resolve(eng)
            md = (eng / "shared-understanding.md").read_text(encoding="utf-8")
        line = [l for l in md.splitlines() if l.startswith("| U-001 ")][0]
        self.assertIn("resolved", line)
        self.assertIn(out["new_id"], line)

    def test_everything_lands_as_one_operation(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            out = self._resolve(eng)
        published = set(out["receipt"]["published"])
        self.assertEqual(published,
                         {"shared-understanding.md", "answers.md",
                          "_graph/graph.jsonl", "_graph/meta.json"},
                         "a SU, a resposta e o grafo nao foram publicados juntos")
        self.assertTrue(O["gate_open"](Path(tmp) / "eng"))


class L03_Terceiro(unittest.TestCase):
    """Responder com declaracao FORA da autoridade -> sem promocao silenciosa a Confirmed."""

    def test_a_third_party_with_a_locator_is_still_only_assumed(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = R["apply"](new_eng(tmp), row_id="U-001",
                             answer_text="Ouvi dizer que e a equipa de dados.",
                             answered_by={"role": "estagiario de outra equipa"},
                             locator="answers.md#U-001", today="2026-09-22")
        self.assertEqual(out["state"], "Assumed",
                         "um terceiro foi promovido a Confirmed")
        self.assertIn("terceiro", out["verdict"]["reason"])

    def test_the_reason_is_written_not_implied(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = R["apply"](new_eng(tmp), row_id="U-001", answer_text="x",
                             answered_by={"other": "alguem"}, locator="L",
                             today="2026-09-22")
        self.assertFalse(out["verdict"]["authority"]["matched"])
        self.assertIn("nao corresponde", out["verdict"]["authority"]["reason"])

    def test_the_declared_authority_is_read_from_the_row_itself(self):
        with tempfile.TemporaryDirectory() as tmp:
            _md, rows = R["read_su"](new_eng(tmp))
            row = R["find_row"](rows, "U-001")
            decl = R["declared_authority"](row)
        self.assertEqual(decl["role"], ["dono dos dados"])

    def test_a_matching_authority_without_a_locator_is_also_assumed(self):
        """Autoridade certa nao basta: `states.md` exige locator para Confirmed."""
        with tempfile.TemporaryDirectory() as tmp:
            out = R["apply"](new_eng(tmp), row_id="U-001", answer_text="x",
                             answered_by={"role": "dono dos dados"}, today="2026-09-22")
        self.assertEqual(out["state"], "Assumed")
        self.assertIn("sem locator", out["verdict"]["reason"])


class L04_IdempotenciaDeCapture(unittest.TestCase):
    """Reprocessar fonte igual e repetir resolucao recuperada -> sem efeitos duplicados."""

    ARGS = dict(row_id="U-001", answer_text="O dono e a equipa de dados.",
                answered_by={"role": "dono dos dados"}, locator="answers.md#U-001",
                today="2026-09-22")

    def test_repeating_the_same_resolution_is_the_same_operation(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            a = R["apply"](eng, **self.ARGS)
            b = R["apply"](eng, **self.ARGS)
        self.assertEqual(a["operation_id"], b["operation_id"])
        self.assertTrue(b["replayed"], "a repeticao nao foi reconhecida")

    def test_repeating_does_not_add_a_second_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            R["apply"](eng, **self.ARGS)
            md1 = (eng / "shared-understanding.md").read_text(encoding="utf-8")
            R["apply"](eng, **self.ARGS)
            md2 = (eng / "shared-understanding.md").read_text(encoding="utf-8")
        self.assertEqual(md1, md2, "a repeticao mudou a SU")

    def test_repeating_does_not_duplicate_the_answer(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            R["apply"](eng, **self.ARGS)
            R["apply"](eng, **self.ARGS)
            ans = (eng / "answers.md").read_text(encoding="utf-8")
        self.assertEqual(ans.count("## U-001"), 1, "a resposta entrou duas vezes")

    def test_repeating_does_not_multiply_graph_nodes(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            R["apply"](eng, **self.ARGS)
            R["apply"](eng, **self.ARGS)
            st = G["read"](eng)
        ids = [n["id"] for n in st["nodes"]]
        self.assertEqual(len(ids), len(set(ids)), "fonte repetida multiplicou nos")

    def test_a_recovered_operation_replays_to_the_same_result(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            first = R["apply"](eng, **self.ARGS)
            self.assertEqual(O["recover"](eng)["result"], "nothing_pending")
            again = R["apply"](eng, **self.ARGS)
        self.assertEqual(first["receipt"]["revision"], again["receipt"]["revision"])


class L05_FactoVersusAdequacao(unittest.TestCase):
    """Confirmar gateway sem provar adequacao ->
    facto registado; escolha estrutural MANTEM condicao aberta."""

    def test_a_connectivity_answer_leaves_the_structural_choice_open(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = R["apply"](new_eng(tmp), row_id="U-001",
                             answer_text="Existe um gateway que liga aos dois sistemas.",
                             answered_by={"role": "dono dos dados"},
                             locator="answers.md#U-001", settles="fact", today="2026-09-22")
        self.assertEqual(out["state"], "Confirmed", "o facto nao foi registado")
        self.assertTrue(out["structural"]["choice_open"],
                        "um facto de conectividade fechou uma escolha estrutural")
        self.assertIn("nao o mecanismo nem a sua adequacao", out["structural"]["note"])

    def test_the_open_choice_is_visible_in_the_graph(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            out = R["apply"](eng, row_id="U-001", answer_text="Ha gateway.",
                             answered_by={"role": "dono dos dados"},
                             locator="L", settles="fact", today="2026-09-22")
            st = G["read"](eng)
        node = [n for n in st["nodes"] if n["id"] == out["new_id"]][0]
        self.assertTrue(node["props"]["structural_choice_open"])

    def test_an_answer_that_settles_fit_may_close_the_choice(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = R["apply"](new_eng(tmp), row_id="U-001",
                             answer_text="O gateway suporta o requisito de auditoria.",
                             answered_by={"role": "dono dos dados"}, locator="L",
                             settles="fit", today="2026-09-22")
        self.assertFalse(out["structural"]["choice_open"])

    def test_a_non_structural_question_has_no_open_choice(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = R["apply"](new_eng(tmp), row_id="U-002", answer_text="As 18h.",
                             answered_by={"role": "Operacoes"}, locator="L",
                             today="2026-09-22")
        self.assertFalse(out["structural"]["structural"])
        self.assertIn("nao se aplica", out["structural"]["note"])

    def test_the_next_step_names_the_open_choice(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = R["apply"](new_eng(tmp), row_id="U-001", answer_text="Ha gateway.",
                             answered_by={"role": "dono dos dados"}, locator="L",
                             settles="fact", today="2026-09-22")
        self.assertIn("adequacao", out["summary"]["proximo passo"])
        self.assertIn("em aberto", out["summary"]["estado"])


class SequenciaEntreSessoes(unittest.TestCase):
    """O que o P4 exige de ponta a ponta, num processo NOVO sem historico."""

    def test_a_fresh_session_recovers_state_provenance_and_next_step(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            out = R["apply"](eng, row_id="U-001", answer_text="Ha gateway.",
                             answered_by={"role": "dono dos dados"}, locator="answers.md#U-001",
                             settles="fact", today="2026-09-22")
            boot = fresh_session(eng, "B['bootstrap'](eng)")
        self.assertTrue(boot["ready"], "a sessao nova nao arrancou")
        self.assertEqual(boot["graph"]["nodes"], 2)
        ids = {i["id"] for i in boot["context"]["included"]}
        self.assertIn(out["new_id"], ids, "o facto novo nao esta no contexto da sessao nova")
        self.assertIn("U-001", ids, "a pergunta original desapareceu do contexto")

    def test_the_gate_is_open_after_a_clean_operation(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            R["apply"](eng, row_id="U-002", answer_text="As 18h.",
                       answered_by={"role": "Operacoes"}, locator="L", today="2026-09-22")
            boot = fresh_session(eng, "B['bootstrap'](eng)")
        self.assertTrue(boot["ready"])
        self.assertEqual([l for l in boot["limitations"] if l.get("blocking")], [])

    def test_an_operation_is_refused_while_recovery_is_pending(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            O["_atomic_write"](O["pending_path"](eng), json.dumps(
                {"intent_version": 1, "operation_id": "op-x", "after": {"a": "b"}}))
            with self.assertRaises(R["ResolveError"]) as ctx:
                R["apply"](eng, row_id="U-001", answer_text="x",
                           answered_by={"role": "dono dos dados"}, locator="L")
        self.assertEqual(ctx.exception.code, "NOT_READY")


if __name__ == "__main__":
    unittest.main(verbosity=2)
