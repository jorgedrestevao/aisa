# -*- coding: utf-8 -*-
"""O comparador de P8, ele próprio sob teste.

O comparador é quem emite o veredicto de E01/E02/E03. Se ele estiver errado, P8 fecha com
um número bonito e nada provado. Por isso: cada achado que ele sabe emitir tem aqui um caso
que o provoca, e um caso que prova que ele NÃO o emite quando não deve.

A última classe é a guarda contra o erro que já aconteceu cinco vezes nesta implementação —
ler uma chave que não existe e receber lista vazia em silêncio."""
import json
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMPARE_PY = ROOT / "docs" / "evolution" / "p8" / "compare.py"
C = runpy.run_path(str(COMPARE_PY))


def verdade(**kw):
    base = {
        "engagement": "eng-a", "phase": "discovery", "ready": True,
        "gate": {"open": False, "transition": ""},
        "by_state": {
            "Confirmed": [{"id": "C-001", "state": "Confirmed", "criticidade": "critical",
                           "swing_class": "dimensionante", "resolved": False,
                           "resolved_to": [], "support": "folha Motor!B12"}],
            "Unknown": [{"id": "U-002", "state": "Unknown", "criticidade": "critical",
                         "swing_class": "dimensionante", "resolved": False,
                         "resolved_to": [], "support": ""},
                        {"id": "U-003", "state": "Unknown", "criticidade": "noncritical",
                         "swing_class": "cosmetico", "resolved": False,
                         "resolved_to": [], "support": ""}],
        },
        "all_ids": ["C-001", "U-002", "U-003"],
        "critical_open": [], "decisions": ["D-001"],
        "next_action": {"text": "", "command": "/answer U-002"},
    }
    base.update(kw)
    return base


def relatorio(**kw):
    base = {
        "engagement": "eng-a", "checkpoint": "cp1", "phase": "discovery",
        "facts": [{"id": "C-001", "state": "Confirmed"}],
        "open_questions": [{"id": "U-002", "state": "Unknown"},
                           {"id": "U-003", "state": "Unknown"}],
        "decisions": [{"id": "D-001"}],
        "coverage": {"status": "fresh"},
        "blockers": [],
        "next_step": "/answer U-002",
    }
    base.update(kw)
    return base


def codigos(v):
    return sorted(a["code"] for a in v["findings"])


class UmaRecuperacaoFielPassa(unittest.TestCase):
    """Se nada se perdeu e nada se inventou, o veredicto é GO. Sem isto, tudo o resto é ruído."""

    def test_a_faithful_report_is_go(self):
        v = C["check"](verdade(), relatorio())
        self.assertEqual(v["findings"], [], "nenhum achado num relatório fiel")
        self.assertEqual(v["verdict"], "GO")

    def test_extra_fields_in_the_report_do_not_upset_it(self):
        v = C["check"](verdade(), relatorio(notes="a sessão escreveu uma nota"))
        self.assertEqual(v["verdict"], "GO")


class InventarEsempreCritico(unittest.TestCase):
    """«Zero factos confirmados indevidamente» — e um id que não existe é pior do que isso."""

    def test_an_id_that_does_not_exist_is_critical(self):
        v = C["check"](verdade(), relatorio(
            facts=[{"id": "C-001", "state": "Confirmed"}, {"id": "C-999", "state": "Confirmed"}]))
        self.assertIn("INVENTED", codigos(v))
        self.assertEqual(v["verdict"], "NO-GO")

    def test_a_decision_that_was_never_taken_is_critical(self):
        v = C["check"](verdade(), relatorio(decisions=[{"id": "D-001"}, {"id": "D-777"}]))
        self.assertIn("INVENTED_DECISION", codigos(v))
        self.assertEqual(v["verdict"], "NO-GO")


class PromoverEstadoEFalsoConfirmado(unittest.TestCase):
    """Dizer Confirmed sobre o que a SU tem como Unknown é o falso Confirmed de `ACCEPTANCE` §2."""

    def test_unknown_reported_as_confirmed_is_critical(self):
        v = C["check"](verdade(), relatorio(
            open_questions=[{"id": "U-002", "state": "Confirmed"},
                            {"id": "U-003", "state": "Unknown"}]))
        self.assertIn("FALSE_CONFIRMED", codigos(v))
        self.assertEqual(v["verdict"], "NO-GO")

    def test_the_other_direction_is_a_warning_not_a_failure(self):
        """Dizer Unknown sobre o que é Confirmed perde informação, mas não afirma falsidade."""
        v = C["check"](verdade(), relatorio(facts=[{"id": "C-001", "state": "Unknown"}]))
        self.assertIn("STATE_DRIFT", codigos(v))
        self.assertEqual(v["critical"], 0)
        self.assertEqual(v["verdict"], "GO")


class PerderDistingueMaterialDeCosmetico(unittest.TestCase):
    """Perder uma linha dimensionante fecha o gate; perder uma cosmética é aviso."""

    def test_losing_a_material_line_is_critical(self):
        v = C["check"](verdade(), relatorio(
            open_questions=[{"id": "U-003", "state": "Unknown"}]))
        perdidos = [a for a in v["findings"] if a["code"] == "LOST_CRITICAL"]
        self.assertEqual([a["id"] for a in perdidos], ["U-002"])
        self.assertEqual(v["verdict"], "NO-GO")

    def test_losing_a_cosmetic_line_is_a_warning(self):
        v = C["check"](verdade(), relatorio(
            open_questions=[{"id": "U-002", "state": "Unknown"}]))
        self.assertEqual(codigos(v), ["LOST"])
        self.assertEqual(v["verdict"], "GO")

    def test_losing_a_decision_is_critical(self):
        v = C["check"](verdade(), relatorio(decisions=[]))
        self.assertIn("LOST_DECISION", codigos(v))
        self.assertEqual(v["verdict"], "NO-GO")

    def test_a_resolved_row_is_not_counted_as_lost(self):
        t = verdade()
        t["by_state"]["Unknown"][0]["resolved"] = True
        v = C["check"](t, relatorio(open_questions=[{"id": "U-003", "state": "Unknown"}]))
        self.assertNotIn("LOST_CRITICAL", codigos(v),
                         "uma linha já resolvida não tem de voltar como pergunta aberta")


class AvancarComOGateFechado(unittest.TestCase):
    """«Zero avanço indevido nos cenários de bloqueio»."""

    def test_proposing_a_phase_command_with_a_closed_gate_is_critical(self):
        v = C["check"](verdade(), relatorio(next_step="/decide"))
        self.assertIn("UNDUE_ADVANCE", codigos(v))
        self.assertEqual(v["verdict"], "NO-GO")

    def test_the_same_command_with_an_open_gate_is_fine(self):
        v = C["check"](verdade(gate={"open": True, "transition": "discovery->framing"}),
                       relatorio(next_step="/frame"))
        self.assertNotIn("UNDUE_ADVANCE", codigos(v))

    def test_answering_a_question_is_never_an_advance(self):
        v = C["check"](verdade(), relatorio(next_step='/answer U-002 "..."'))
        self.assertNotIn("UNDUE_ADVANCE", codigos(v))


class AFaseEAFormaDaResposta(unittest.TestCase):

    def test_a_wrong_phase_is_critical(self):
        v = C["check"](verdade(), relatorio(phase="options"))
        self.assertIn("PHASE_MISMATCH", codigos(v))

    def test_a_report_missing_the_asked_fields_is_critical(self):
        parcial = relatorio()
        del parcial["decisions"]
        del parcial["coverage"]
        v = C["check"](verdade(), parcial)
        achado = next(a for a in v["findings"] if a["code"] == "REPORT_INCOMPLETE")
        self.assertEqual(sorted(achado["missing"]), ["coverage", "decisions"])


class FugaEntreEngagements(unittest.TestCase):
    """§6: trocar entre dois engagements e verificar que o primeiro não entra no segundo."""

    def test_an_id_from_the_other_engagement_is_critical(self):
        outro = verdade(engagement="eng-b")
        outro["by_state"]["Confirmed"][0]["id"] = "C-500"
        outro["decisions"] = ["D-900"]
        v = C["leak"](outro, relatorio(engagement="eng-b-alvo",
                                       facts=[{"id": "C-500", "state": "Confirmed"}]))
        self.assertIn("LEAK", codigos(v))
        self.assertEqual(v["verdict"], "NO-GO")

    def test_a_clean_report_shows_no_leak(self):
        outro = verdade(engagement="eng-b")
        outro["by_state"] = {"Confirmed": [{"id": "C-500", "state": "Confirmed"}]}
        outro["decisions"] = ["D-900"]
        v = C["leak"](outro, relatorio())
        self.assertEqual(v["findings"], [])
        self.assertEqual(v["verdict"], "GO")


class ContraOOraculo(unittest.TestCase):
    """E02/E03 — os três números que o oráculo declara, medidos e não narrados."""

    ORACULO = {
        "acceptance": {"critical_recall": 1.0, "critical_false_confirmed": 0,
                       "improper_gate_advances": 0},
        "items": [
            {"id": "T-01", "epistemic_state": "Confirmed", "criticality": "critical"},
            {"id": "T-02", "epistemic_state": "Unknown", "criticality": "critical"},
            {"id": "T-09", "epistemic_state": "Confirmed", "criticality": "noncritical"},
        ],
    }

    def eng_falso(self, tmp, t):
        """O comparador lê o engagement por `truth()`; aqui injecta-se a verdade directamente.

        `runpy.run_path` devolve uma CÓPIA do namespace: escrever em `C_local["truth"]` não
        chega ao `truth` que `oracle` resolve em tempo de execução. O que a função vê é o
        seu próprio `__globals__` — é lá que a substituição tem de ser feita, ou o teste
        mede o engagement vazio do tmpdir e passa a dizer coisas que não verificou.
        """
        C_local = runpy.run_path(str(COMPARE_PY))
        C_local["oracle"].__globals__["truth"] = lambda _p: t
        return C_local

    def test_full_recall_with_no_false_confirmed_meets_the_thresholds(self):
        t = verdade(by_state={
            "Confirmed": [{"id": "C-001", "state": "Confirmed"}],
            "Unknown": [{"id": "U-002", "state": "Unknown"}]},
            all_ids=["C-001", "U-002"], critical_open=[], decisions=[])
        with tempfile.TemporaryDirectory() as tmp:
            Cl = self.eng_falso(tmp, t)
            v = Cl["oracle"](Path(tmp), self.ORACULO, {"T-01": "C-001", "T-02": "U-002"})
        self.assertEqual(v["measured"]["critical_recall"], 1.0)
        self.assertEqual(v["measured"]["critical_false_confirmed"], 0)
        self.assertTrue(v["meets_thresholds"])

    def test_a_critical_item_with_no_match_breaks_recall(self):
        t = verdade(by_state={"Confirmed": [{"id": "C-001", "state": "Confirmed"}]},
                    all_ids=["C-001"], critical_open=[], decisions=[])
        with tempfile.TemporaryDirectory() as tmp:
            Cl = self.eng_falso(tmp, t)
            v = Cl["oracle"](Path(tmp), self.ORACULO, {"T-01": "C-001", "T-02": None})
        self.assertIn("CRITICAL_MISS", codigos(v))
        self.assertEqual(v["measured"]["critical_recall"], 0.5)
        self.assertFalse(v["meets_thresholds"])
        self.assertEqual(v["verdict"], "NO-GO")

    def test_claiming_confirmed_where_the_oracle_says_unknown_is_counted(self):
        t = verdade(by_state={"Confirmed": [{"id": "C-001", "state": "Confirmed"},
                                            {"id": "C-002", "state": "Confirmed"}]},
                    all_ids=["C-001", "C-002"], critical_open=[], decisions=[])
        with tempfile.TemporaryDirectory() as tmp:
            Cl = self.eng_falso(tmp, t)
            v = Cl["oracle"](Path(tmp), self.ORACULO, {"T-01": "C-001", "T-02": "C-002"})
        self.assertEqual(v["measured"]["critical_false_confirmed"], 1)
        self.assertFalse(v["meets_thresholds"])

    def test_a_mapping_to_a_row_that_does_not_exist_is_critical(self):
        t = verdade(by_state={"Confirmed": [{"id": "C-001", "state": "Confirmed"}]},
                    all_ids=["C-001"], critical_open=[], decisions=[])
        with tempfile.TemporaryDirectory() as tmp:
            Cl = self.eng_falso(tmp, t)
            v = Cl["oracle"](Path(tmp), self.ORACULO, {"T-01": "C-001", "T-02": "C-404"})
        self.assertIn("MAPPED_TO_NOTHING", codigos(v))

    def test_an_open_gate_over_open_criticals_is_an_improper_advance(self):
        t = verdade(by_state={"Confirmed": [{"id": "C-001", "state": "Confirmed"}],
                              "Unknown": [{"id": "U-002", "state": "Unknown"}]},
                    all_ids=["C-001", "U-002"],
                    gate={"open": True, "transition": "x"},
                    critical_open=[{"kind": "CRITICAL_OPEN", "what": "U-002"}], decisions=[])
        with tempfile.TemporaryDirectory() as tmp:
            Cl = self.eng_falso(tmp, t)
            v = Cl["oracle"](Path(tmp), self.ORACULO, {"T-01": "C-001", "T-02": "U-002"})
        self.assertEqual(v["measured"]["improper_gate_advances"], 1)
        self.assertFalse(v["meets_thresholds"])


class NaoSeConcluiDoVazio(unittest.TestCase):
    """Sem execução não há veredicto. É o contrário de imprimir PASS (§1)."""

    def test_an_empty_runs_directory_is_not_a_go(self):
        with tempfile.TemporaryDirectory() as tmp:
            s = C["summary"](Path(tmp))
            self.assertEqual(s["verdict"], "SEM EXECUÇÃO")
            self.assertEqual(s["runs"], 0)
            self.assertNotEqual(s["verdict"], "GO")

    def test_one_no_go_run_makes_the_whole_summary_no_go(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "a.verdict.json").write_text(json.dumps(
                {"engagement": "eng-a", "checkpoint": "cp1", "case": "E01",
                 "critical": 0, "warnings": 1, "verdict": "GO"}), encoding="utf-8")
            (d / "b.verdict.json").write_text(json.dumps(
                {"engagement": "eng-b", "checkpoint": "cp2", "case": "E01",
                 "critical": 2, "warnings": 0, "verdict": "NO-GO"}), encoding="utf-8")
            s = C["summary"](d)
        self.assertEqual(s["runs"], 2)
        self.assertEqual(s["verdict"], "NO-GO")
        self.assertEqual(s["no_go"], ["eng-b/cp2"])


class ExitCodeEProcessoReal(unittest.TestCase):
    """Quem corre isto lê o código de saída. Um NO-GO tem de sair diferente de zero."""

    def corre(self, *args):
        return subprocess.run([sys.executable, str(COMPARE_PY), *args],
                              capture_output=True, text=True)

    def test_a_no_go_exits_nonzero(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp) / "t.json"
            r = Path(tmp) / "r.json"
            t.write_text(json.dumps(verdade()), encoding="utf-8")
            r.write_text(json.dumps(relatorio(
                facts=[{"id": "C-001", "state": "Confirmed"}, {"id": "C-999", "state": "Confirmed"}])),
                encoding="utf-8")
            p = self.corre("check", "--truth", str(t), "--report", str(r))
        self.assertEqual(p.returncode, 1)
        self.assertIn("INVENTED", p.stdout)

    def test_a_go_exits_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp) / "t.json"
            r = Path(tmp) / "r.json"
            t.write_text(json.dumps(verdade()), encoding="utf-8")
            r.write_text(json.dumps(relatorio()), encoding="utf-8")
            p = self.corre("check", "--truth", str(t), "--report", str(r))
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)


class GuardaContraALeituraSilenciosaDoVazio(unittest.TestCase):
    """As decisões vivem em `status.decisions`. Ler `model["decisions"]` devolve [] calado.

    Este teste corre contra o engagement real porque é lá que o erro apareceu: a captura
    dizia zero decisões num piloto com D-001 e D-002 escritas, e nada se queixou."""

    ENG = ROOT / "projects" / "dpt-galp-jp-pilot-4"

    def test_the_real_engagement_yields_the_decisions_that_are_written(self):
        if not (self.ENG / "decisions.md").is_file():
            self.skipTest("engagement do piloto ausente neste ambiente")
        escritas = set()
        for linha in (self.ENG / "decisions.md").read_text(encoding="utf-8").splitlines():
            if linha.startswith("## D-"):
                escritas.add(linha[3:].split(" ")[0].strip())
        t = C["truth"](self.ENG)
        self.assertTrue(escritas, "o ficheiro tem decisões escritas")
        self.assertTrue(set(t["decisions"]) >= escritas,
                        "a captura perdeu decisões que estão no ficheiro: {} vs {}".format(
                            sorted(t["decisions"]), sorted(escritas)))

    def test_the_real_engagement_yields_rows(self):
        if not (self.ENG / "shared-understanding.md").is_file():
            self.skipTest("engagement do piloto ausente neste ambiente")
        t = C["truth"](self.ENG)
        self.assertGreater(len(t["all_ids"]), 0,
                           "zero linhas num engagement com SU escrita é leitura do vazio")
        self.assertTrue(t["by_state"], "os estados não podem vir todos vazios")


class GuardaContraOProprioRelatorio(unittest.TestCase):
    """O relatório de P8 não pode declarar E01/E02 cumpridos sem execução em `runs/`.

    O P7 levou uma guarda destas porque um relatório é texto e texto alega o que quiser.
    Aqui a guarda é dupla: ou existem veredictos em `runs/`, ou o relatório diz NÃO
    EXECUTADO. As duas coisas ao mesmo tempo é que não podem ser."""

    RELATORIO = ROOT / "docs" / "evolution" / "P8-report.md"
    RUNS = ROOT / "docs" / "evolution" / "p8" / "runs"

    def test_the_report_claims_e01_e02_only_if_runs_exist(self):
        if not self.RELATORIO.is_file():
            self.skipTest("relatório de P8 ainda não escrito")
        texto = self.RELATORIO.read_text(encoding="utf-8")
        veredictos = list(self.RUNS.rglob("*.verdict.json")) if self.RUNS.is_dir() else []
        if veredictos:
            return          # há execução: o relatório pode falar dela
        for caso in ("E01", "E02"):
            linhas = [l for l in texto.splitlines() if l.strip().startswith("| **" + caso)]
            self.assertTrue(linhas, "o relatório tem de ter uma linha para " + caso)
            self.assertTrue(
                any("NÃO EXECUTADO" in l or "NAO EXECUTADO" in l for l in linhas),
                "{} não pode aparecer como cumprido sem um veredicto em runs/: {!r}".format(
                    caso, linhas))

    def test_the_summary_over_the_real_runs_matches_what_is_there(self):
        """O agregado não pode dizer GO sobre um directório sem veredictos."""
        if not self.RUNS.is_dir():
            self.skipTest("runs/ ainda não existe")
        s = C["summary"](self.RUNS)
        veredictos = list(self.RUNS.rglob("*.verdict.json"))
        if not veredictos:
            self.assertEqual(s["verdict"], "SEM EXECUÇÃO")
        else:
            self.assertEqual(s["runs"], len(veredictos))


if __name__ == "__main__":
    unittest.main(verbosity=1)
