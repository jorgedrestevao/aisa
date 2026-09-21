"""Endurecimento do runtime, bloco C — a validação da síntese avalia, e não contamina a frescura.

O defeito que este ficheiro existe para impedir (revisão do plano, ponto 1): a proposta
inicial escrevia a validação em `_synthesis-log.md`. `synthesis_entries()` casa qualquer
linha `<ISO> — <token>` e `synthesis_state()` toma a mais recente como o momento em que o
tópico foi sintetizado — logo uma validação datada de hoje faria um pack velho parecer
fresco. `test_validating_a_stale_pack_keeps_it_stale` é essa prova.

O segundo (ponto 2 da mesma revisão): três dos seis testes dependem de fontes FORA do texto
— a SU e `decisions.md` para os ids, o pacote para os termos, o desenho aprovado para o
carimbo. Um sha do texto não chega: o texto pode ficar igual e a resposta mudar. Por isso o
veredicto recalcula-se na consulta e o log é história.

    python .claude/tests/test_synthesis_checks.py
"""

import json
import runpy
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
D = runpy.run_path(str(ROOT / "library" / "kernel" / "tools" / "dashboard.py"))
HOOK = ROOT / ".claude" / "hooks" / "synthesis-validate.py"
TODAY = date(2026, 9, 10)

SU = """# Shared Understanding — fx

**Engagement**: fx
**Phase**: decision
**Pack**: pp
**Last updated**: 2026-09-08

## Confirmed

| id | lens | claim | evidência | verificado_em | validade | ronda |
|---|---|---|---|---|---|---|
| C-001 | business | o processo corre em Excel | inputs/x.xlsx#S!A1 | 2026-09-01 | organizacional | R-01 |
| C-002 | data | o histórico vive numa base partilhada | inputs/x.xlsx#S!A2 | 2026-09-01 | organizacional | R-01 |

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

DECISIONS = """# Decisions

## D-002 — Adopt O-001
- **Chosen option**: O-001
- **Timestamp**: 2026-09-02T10:00:00Z
"""

GOOD = """# As-is

O processo corre hoje num único ficheiro (C-001), mantido à mão por uma pessoa.

O histórico dos valores vive numa base partilhada (C-002), fora do ficheiro.

Nenhuma das duas peças tem hoje um dono declarado para a mudança (C-001).
"""


def mk(tmp, slug="fx", *, packs=None, decisions=DECISIONS, su=SU, blueprints=None,
       log=None, checks=None, phase="decision"):
    eng = Path(tmp) / slug
    (eng / "_synthesis").mkdir(parents=True, exist_ok=True)
    (eng / "_state.json").write_text(json.dumps(
        {"engagement": slug, "pack": "pp", "phase": phase, "round": "D-01"}), encoding="utf-8")
    (eng / "shared-understanding.md").write_text(su, encoding="utf-8")
    (eng / "decisions.md").write_text(decisions, encoding="utf-8")
    for name, body in (packs or {"as-is": GOOD}).items():
        (eng / "_synthesis" / (name + ".md")).write_text(body, encoding="utf-8")
    for ver, body in (blueprints or {}).items():
        d = eng / "_blueprint"
        d.mkdir(exist_ok=True)
        (d / "ux-blueprint_{}.yaml".format(ver)).write_text(body, encoding="utf-8")
    if log is not None:
        (eng / "_synthesis" / "_synthesis-log.md").write_text(log, encoding="utf-8")
    if checks is not None:
        (eng / "_synthesis" / "_synthesis-checks.md").write_text(checks, encoding="utf-8")
    return eng


def codes(eng, topic):
    return sorted(c["code"] for c in D["synthesis_check"](eng, topic)["codes"])


def run_hook(path):
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps({"tool_name": "Write", "tool_input": {"file_path": str(path)}}),
        text=True, capture_output=True, encoding="utf-8", errors="replace", cwd=str(ROOT))


class Codes(unittest.TestCase):
    """Cada código com a fixture que o dispara e a que não o dispara."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def test_a_good_pack_is_clean(self):
        eng = mk(self.tmp.name)
        self.assertEqual(codes(eng, "as-is"), [])

    def test_two_paragraphs_fire_paras(self):
        body = "# As-is\n\nUm parágrafo (C-001).\n\nOutro (C-002).\n"
        eng = mk(self.tmp.name, packs={"as-is": body})
        self.assertIn("SYN-PARAS", codes(eng, "as-is"))

    def test_no_ids_fires(self):
        body = "# As-is\n\nUm.\n\nDois.\n\nTrês.\n"
        eng = mk(self.tmp.name, packs={"as-is": body})
        self.assertIn("SYN-NO-IDS", codes(eng, "as-is"))

    def test_a_dead_id_is_not_a_citation(self):
        eng = mk(self.tmp.name, packs={"as-is": GOOD.replace("C-002", "C-999")})
        self.assertIn("SYN-DEAD-ID", codes(eng, "as-is"))

    def test_a_decision_id_counts_as_known(self):
        eng = mk(self.tmp.name, packs={"as-is": GOOD.replace("C-002", "D-002")})
        self.assertNotIn("SYN-DEAD-ID", codes(eng, "as-is"))

    def test_a_solution_term_in_a_neutral_topic_fires(self):
        eng = mk(self.tmp.name, packs={"as-is": GOOD + "\nSeria feito em Power Apps (C-001).\n"})
        self.assertIn("SYN-VENDOR", codes(eng, "as-is"))

    def test_a_current_state_term_does_not_fire(self):
        """`sharepoint` nomeia o estado actual e é legítimo num as-is — a lista de
        Discovery inclui-o, a lista de solução não. Confundi-las produz falsos positivos."""
        eng = mk(self.tmp.name,
                 packs={"as-is": GOOD + "\nOs ficheiros vivem hoje no SharePoint (C-002).\n"})
        self.assertNotIn("SYN-VENDOR", codes(eng, "as-is"))
        self.assertNotIn("sharepoint", [t.lower() for t in D["pack_vendor_terms"]("pp")])

    def test_a_pack_without_the_list_makes_vendor_not_evaluated(self):
        eng = mk(self.tmp.name, packs={"as-is": GOOD})
        res = D["synthesis_check"](eng, "as-is", pack="generic")
        self.assertTrue(any("SYN-VENDOR" in n for n in res["not_evaluated"]))

    def test_a_topic_outside_the_five_fires_template(self):
        eng = mk(self.tmp.name, packs={"outra-coisa": GOOD})
        self.assertIn("SYN-TEMPLATE", codes(eng, "outra-coisa"))


class ArchitectureStory(unittest.TestCase):
    """A neutralidade deste tópico é CONDICIONAL à autorização de arquitectura."""

    BP = (ROOT / ".claude" / "tests" / "fixtures" / "blueprints" / "valid_min_v01.yaml")

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.valid = self.BP.read_text(encoding="utf-8") if self.BP.is_file() else ""
        if not self.valid:
            self.skipTest("fixture de blueprint ausente")
        self.approved = DECISIONS + "\n## D-003 — Blueprint bp-v01 aprovado\n- **Timestamp**: 2026-09-08T10:00:00Z\n"

    def _story(self, extra=""):
        return ("# Architecture Story\n"
                "<!-- authority: _blueprint/ux-blueprint_v01.yaml#architecture @ sha256:{} -->\n\n"
                "A solução assenta na base já operada (C-002).\n\n"
                "O desenho mantém o histórico onde está (C-002).\n\n"
                "Os utilizadores continuam internos (C-001).\n" + extra)

    def test_a_vendor_term_with_authorization_does_not_fire(self):
        eng = mk(self.tmp.name, packs={"architecture-story": "x"}, decisions=self.approved,
                 blueprints={"v01": self.valid})
        sha = D["architecture_block_sha256"](self.valid)
        body = self._story("\nA app é model-driven sobre Dataverse (C-001).\n").format(sha)
        (eng / "_synthesis" / "architecture-story.md").write_text(body, encoding="utf-8")
        self.assertNotIn("SYN-VENDOR", codes(eng, "architecture-story"))

    def test_a_vendor_term_without_authorization_fires(self):
        not_auth = self.valid.replace("authorization: authorized", "authorization: not-authorized")
        eng = mk(self.tmp.name, packs={"architecture-story": "x"}, decisions=self.approved,
                 blueprints={"v01": not_auth})
        sha = D["architecture_block_sha256"](not_auth)
        body = self._story("\nSeria model-driven sobre Dataverse (C-001).\n").format(sha)
        (eng / "_synthesis" / "architecture-story.md").write_text(body, encoding="utf-8")
        self.assertIn("SYN-VENDOR", codes(eng, "architecture-story"))

    def test_no_stamp_fires(self):
        eng = mk(self.tmp.name,
                 packs={"architecture-story": "# Architecture Story\n\nUm (C-001).\n\nDois (C-002).\n\nTrês (C-001).\n"},
                 decisions=self.approved, blueprints={"v01": self.valid})
        self.assertIn("SYN-STAMP", codes(eng, "architecture-story"))

    def test_authority_none_is_the_legitimate_case(self):
        """Sem arquitectura autorizada não há versão para carimbar — e isso diz-se,
        não se reporta como carimbo em falta."""
        body = ("# Architecture Story\n"
                "<!-- authority: none — outcome-forbade -->\n\n"
                "A escolha não autoriza arquitectura (C-001).\n\n"
                "O âmbito é de mudança de processo (C-002).\n\n"
                "Nada se constrói nesta fase (C-001).\n")
        eng = mk(self.tmp.name, packs={"architecture-story": body})
        self.assertNotIn("SYN-STAMP", codes(eng, "architecture-story"))

    def test_a_stamp_naming_a_structurally_invalid_version_fires(self):
        broken = self.valid.replace("      structural: false\n", "")
        eng = mk(self.tmp.name, packs={"architecture-story": "x"}, decisions=self.approved,
                 blueprints={"v01": broken})
        sha = D["architecture_block_sha256"](broken)
        (eng / "_synthesis" / "architecture-story.md").write_text(
            self._story().format(sha), encoding="utf-8")
        self.assertIn("SYN-STAMP", codes(eng, "architecture-story"))


class StampHasToBeSupported(unittest.TestCase):
    """Reconhecer a FORMA de um carimbo nao e verifica-lo.

    Defeito real (revisao da fase 3, 2026-09-10): um carimbo para `ux-blueprint_v99.yaml`,
    que nao existe, e um `authority: none` num engagement COM arquitectura autorizada
    passavam ambos sem aviso. O topico ficava com uma proveniencia que ninguem consegue
    seguir.
    """

    BP = ROOT / ".claude" / "tests" / "fixtures" / "blueprints" / "valid_min_v01.yaml"

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        if not self.BP.is_file():
            self.skipTest("fixture de blueprint ausente")
        self.valid = self.BP.read_text(encoding="utf-8")
        self.approved = (DECISIONS + "\n## D-003 - Blueprint bp-v01 aprovado\n"
                         "- **Timestamp**: 2026-09-08T10:00:00Z\n")
        self._n = 0

    def _story(self, stamp):
        return ("# Architecture Story\n" + stamp + "\n\nUm (C-001).\n\n"
                "Dois (C-002).\n\nTres (C-001).\n")

    def _stamp(self, ver, sha):
        return ("<!-- authority: _blueprint/ux-blueprint_" + ver +
                ".yaml#architecture @ sha256:" + sha + " -->")

    def _codes(self, body, blueprints=None, decisions=None):
        self._n += 1
        eng = mk(self.tmp.name, slug="s%d" % self._n,
                 packs={"architecture-story": body}, blueprints=blueprints or {},
                 decisions=decisions or DECISIONS)
        return D["synthesis_check"](eng, "architecture-story")["codes"]

    def test_a_stamp_naming_a_version_that_does_not_exist_fires(self):
        got = self._codes(self._story(self._stamp("v99", "0" * 64)))
        self.assertEqual([c["code"] for c in got], ["SYN-STAMP"])
        self.assertIn("nao existe", got[0]["detail"])

    def test_a_truncated_sha_is_not_a_missing_sha(self):
        got = self._codes(self._story(self._stamp("v01", "deadbeef")),
                          {"v01": self.valid}, self.approved)
        self.assertEqual([c["code"] for c in got], ["SYN-STAMP"])
        self.assertIn("64 hex", got[0]["detail"])

    def test_a_wrong_sha_fires(self):
        got = self._codes(self._story(self._stamp("v01", "f" * 64)),
                          {"v01": self.valid}, self.approved)
        self.assertTrue(any("sha256 difere" in c["detail"] for c in got))

    def test_a_stamp_of_an_unauthorized_version_fires(self):
        not_auth = self.valid.replace("authorization: authorized",
                                      "authorization: not-authorized")
        sha = D["architecture_block_sha256"](not_auth)
        got = self._codes(self._story(self._stamp("v01", sha)), {"v01": not_auth})
        self.assertTrue(any("nao autorizada" in c["detail"] for c in got), got)

    def test_a_stamp_of_the_wrong_version_fires(self):
        v02 = self.valid.replace("version: 1", "version: 2")
        sha = D["architecture_block_sha256"](self.valid)
        got = self._codes(self._story(self._stamp("v01", sha)),
                          {"v01": self.valid, "v02": v02},
                          DECISIONS + "\n## D-004 - Blueprint bp-v02 aprovado\n"
                          "- **Timestamp**: 2026-09-09T10:00:00Z\n")
        self.assertTrue(any("autoridade deste engagement" in c["detail"] for c in got), got)

    def test_authority_none_with_an_authorized_version_on_disk_fires(self):
        got = self._codes(self._story("<!-- authority: none - outcome-forbade -->"),
                          {"v01": self.valid}, self.approved)
        self.assertEqual([c["code"] for c in got], ["SYN-STAMP"])
        self.assertIn("nao se sustenta", got[0]["detail"])

    def test_an_unrecognised_reason_fires(self):
        got = self._codes(self._story("<!-- authority: none - porque -->"))
        self.assertEqual([c["code"] for c in got], ["SYN-STAMP"])
        self.assertIn("razao reconhecida", got[0]["detail"])

    # --- `authority: none` contra os pares (scope, outcome) --------------------
    # Alcance ESTRUTURAL (2026-09-11), depois de medir que 2 de 23 engagements os
    # persistem: falta de informacao historica e uma coisa, inconsistencia verificavel e
    # outra, e o motor nao as junta. O SIGNIFICADO da razao fica por avaliar em ambos os
    # casos, e diz-se -- separa-la exigiria a fronteira de architectabilidade do pacote
    # legivel pelo motor (evolucao separada).

    PAIRS_TAIL = ("\n- **Selected solution / composition**: mudar o processo, construir nada"
                  "\n- **(Scope, outcome) pairs - UNCOLLAPSED**:"
                  "\n  - whole solution - \"nenhuma alternativa de construcao e viavel\"\n")

    def _res(self, body, blueprints=None, decisions=None):
        self._n += 1
        eng = mk(self.tmp.name, slug="r%d" % self._n,
                 packs={"architecture-story": body}, blueprints=blueprints or {},
                 decisions=decisions or DECISIONS)
        return D["synthesis_check"](eng, "architecture-story")

    def _none(self, reason="outcome-forbade"):
        return self._story("<!-- authority: none - " + reason + " -->")

    def test_no_decision_at_all_is_not_evaluated_not_clean(self):
        """A lacuna de 2026-09-11: com `decisions.md` vazio as duas razoes passavam
        limpas. Nao viram falha -- viram ausencia, e ausencia nao se afirma."""
        for reason in ("outcome-forbade", "outside-pack-authority"):
            res = self._res(self._none(reason), decisions="# Decisions\n")
            self.assertEqual(res["codes"], [], reason)
            self.assertTrue(any("SYN-STAMP" in n for n in res["not_evaluated"]), reason)
            self.assertTrue(any("nao foi verificada" in n for n in res["not_evaluated"]))
            self.assertEqual(res["notes"], [], reason)

    def test_a_generic_decision_without_pairs_is_not_evaluated(self):
        """A lacuna de 2026-09-11 (segunda volta): bastava existir `Adopt O-001` para as
        duas razoes passarem. A base documental sao os PARES, nao a existencia do bloco."""
        for reason in ("outcome-forbade", "outside-pack-authority"):
            res = self._res(self._none(reason))          # DECISIONS: Adopt O-001, sem pares
            self.assertEqual(res["codes"], [], reason)
            self.assertTrue(any("nao regista pares" in n for n in res["not_evaluated"]),
                            reason)

    def test_a_frame_decision_alone_is_not_evaluated(self):
        """Aprovar a frase do problema nao emite outcome nenhum: so a decisao de solucao
        o faz."""
        frame_only = ("# Decisions\n\n## D-001 - Frame agreed\n"
                      "- **Timestamp**: 2026-09-02T10:00:00Z\n")
        res = self._res(self._none(), decisions=frame_only)
        self.assertEqual(res["codes"], [])
        self.assertTrue(any("decisao de solucao" in n for n in res["not_evaluated"]))

    def test_complete_pairs_pass_structurally_and_say_what_was_not_judged(self):
        """Estrutura satisfeita: a base documental existe, e a nota diz com todas as
        letras que o SIGNIFICADO da razao nao foi avaliado."""
        res = self._res(self._none(), decisions=DECISIONS + self.PAIRS_TAIL)
        self.assertEqual(res["codes"], [])
        self.assertEqual(res["not_evaluated"], [])
        self.assertTrue(res["notes"])
        self.assertIn("base documental existe", res["notes"][0])
        self.assertIn("SIGNIFICADO", res["notes"][0])

    def test_outside_pack_authority_needs_the_selected_solution(self):
        """Essa razao fala da solucao seleccionada; sem ela a estrutura nao esta completa,
        e isso e falha, nao ausencia."""
        no_sel = (DECISIONS + "\n- **(Scope, outcome) pairs - UNCOLLAPSED**:"
                  "\n  - whole solution - \"nao ha alternativa de construcao\"\n")
        res = self._res(self._none("outside-pack-authority"), decisions=no_sel)
        self.assertEqual([c["code"] for c in res["codes"]], ["SYN-STAMP"])
        self.assertIn("solucao seleccionada", res["codes"][0]["detail"])
        # a mesma decisao serve `outcome-forbade`, que nao fala da solucao
        ok = self._res(self._none("outcome-forbade"), decisions=no_sel)
        self.assertEqual(ok["codes"], [])

    def test_malformed_pairs_are_a_failure_not_an_absence(self):
        """Dados malformados nao se convertem em `nao avaliado`."""
        bad = (DECISIONS + "\n- **(Scope, outcome) pairs - UNCOLLAPSED**:"
               "\n  - whole solution\n")
        res = self._res(self._none(), decisions=bad)
        self.assertEqual([c["code"] for c in res["codes"]], ["SYN-STAMP"])
        self.assertIn("malformados, nao ausentes", res["codes"][0]["detail"])
        self.assertEqual(res["not_evaluated"], [])

    def test_a_contradiction_wins_over_the_documentary_basis(self):
        """Ha pares E ha arquitectura autorizada: a contradicao e verificavel e dispara,
        sem passar por `nao avaliado`."""
        res = self._res(self._none(), {"v01": self.valid},
                        self.approved + self.PAIRS_TAIL)
        self.assertEqual([c["code"] for c in res["codes"]], ["SYN-STAMP"])
        self.assertIn("nao se sustenta", res["codes"][0]["detail"])
        self.assertEqual(res["not_evaluated"], [])

    def test_an_unrecognised_reason_is_a_failure_of_its_own(self):
        """A razao invalida e um defeito da forma do carimbo; a ausencia de pares e outro.
        Um nao esconde o outro."""
        res = self._res(self._story("<!-- authority: none - porque -->"),
                        decisions="# Decisions\n")
        self.assertIn("razao reconhecida", res["codes"][0]["detail"])
        self.assertTrue(res["not_evaluated"])

    def test_the_pair_reader_reads_shape_never_meaning(self):
        pairs = D["decision_scope_outcome_pairs"](DECISIONS + self.PAIRS_TAIL)
        self.assertTrue(pairs["present"])
        self.assertEqual(len(pairs["pairs"]), 1)
        self.assertEqual(pairs["pairs"][0]["scope"], "whole solution")
        self.assertIn("nenhuma alternativa", pairs["pairs"][0]["outcome"])
        self.assertEqual(pairs["malformed"], [])
        self.assertTrue(pairs["selected_solution"])

    def test_a_superseded_decision_never_supplies_the_evidence(self):
        """Defeito reproduzido em 2026-09-11: o leitor procurava os primeiros pares e a
        primeira solucao no FICHEIRO inteiro. Com `D-003` a substituir `D-002` e pares
        malformados, os dados antigos de `D-002` eram aceites e a base dava-se por
        existente -- uma validacao contra uma escolha que ninguem esta a fazer."""
        superseded = (DECISIONS + self.PAIRS_TAIL +
                      "\n## D-003 - Adopt O-004 (supersedes D-002)"
                      "\n- **Chosen option**: O-004"
                      "\n- **(Scope, outcome) pairs - UNCOLLAPSED**:"
                      "\n  - whole solution"
                      "\n- **Timestamp**: 2026-09-06T10:00:00Z\n")
        pairs = D["decision_scope_outcome_pairs"](superseded)
        self.assertEqual(pairs["decision"], "D-003")
        self.assertEqual(pairs["pairs"], [])
        self.assertEqual(len(pairs["malformed"]), 1)
        res = self._res(self._none(), decisions=superseded)
        self.assertEqual([c["code"] for c in res["codes"]], ["SYN-STAMP"])
        self.assertIn("malformados", res["codes"][0]["detail"])

    def test_the_selected_solution_comes_from_the_live_block_too(self):
        """Ambos os campos do mesmo bloco: a solucao seleccionada de uma decisao
        substituida nao satisfaz `outside-pack-authority` da decisao em vigor."""
        superseded = (DECISIONS + self.PAIRS_TAIL +
                      "\n## D-003 - Adopt O-004 (supersedes D-002)"
                      "\n- **Chosen option**: O-004"
                      "\n- **(Scope, outcome) pairs - UNCOLLAPSED**:"
                      "\n  - whole solution - \"nao ha alternativa de construcao\""
                      "\n- **Timestamp**: 2026-09-06T10:00:00Z\n")
        pairs = D["decision_scope_outcome_pairs"](superseded)
        self.assertEqual(pairs["decision"], "D-003")
        self.assertEqual(len(pairs["pairs"]), 1)
        self.assertEqual(pairs["selected_solution"], "")
        res = self._res(self._none("outside-pack-authority"), decisions=superseded)
        self.assertEqual([c["code"] for c in res["codes"]], ["SYN-STAMP"])
        self.assertIn("solucao seleccionada", res["codes"][0]["detail"])

    def test_the_real_engagement_that_persists_pairs_is_read(self):
        """Contra a copia real, nao so contra fixtures."""
        eng = ROOT / "projects" / "pricing-marinha-pilot-1"
        if not (eng / "decisions.md").is_file():
            self.skipTest("engagement nao montado")
        pairs = D["decision_scope_outcome_pairs"](
            (eng / "decisions.md").read_text(encoding="utf-8"))
        self.assertTrue(pairs["present"])
        self.assertGreaterEqual(len(pairs["pairs"]), 1)
        self.assertTrue(pairs["selected_solution"])

    def test_a_correct_stamp_is_clean(self):
        sha = D["architecture_block_sha256"](self.valid)
        got = self._codes(self._story(self._stamp("v01", sha)),
                          {"v01": self.valid}, self.approved)
        self.assertEqual(got, [])


class FreshnessIsUntouched(unittest.TestCase):
    """A prova central: validar não é sintetizar."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def _stale(self):
        """`as-is` lê as linhas da SU com lens IN operations,user. Uma linha verificada em
        07/09 é autoridade posterior a uma síntese de 03/09 — é isso que o motor chama
        stale, e é a pré-condição que estes testes precisam de ter a sério."""
        su = SU.replace(
            "| C-002 | data | o histórico vive numa base partilhada | inputs/x.xlsx#S!A2 "
            "| 2026-09-01 | organizacional | R-01 |",
            "| C-002 | operations | o histórico vive numa base partilhada | "
            "inputs/x.xlsx#S!A2 | 2026-09-07 | organizacional | R-01 |")
        log = "# Synthesis Log\n\n2026-09-03T10:00:00Z — as-is — sources: 1\n"
        return mk(self.tmp.name, su=su, log=log)

    def test_the_fixture_really_is_stale(self):
        eng = self._stale()
        st = D["build_model"](eng, TODAY)["status"]["synthesis"]
        self.assertEqual(st["topics"]["as-is"]["verdict"], "stale")

    def test_validating_a_stale_pack_keeps_it_stale(self):
        eng = self._stale()
        before = (eng / "_synthesis" / "_synthesis-log.md").read_bytes()
        r = run_hook(eng / "_synthesis" / "as-is.md")
        self.assertEqual(r.returncode, 0)
        after = (eng / "_synthesis" / "_synthesis-log.md").read_bytes()
        self.assertEqual(before, after, "_synthesis-log.md foi tocado")
        st = D["build_model"](eng, TODAY)["status"]["synthesis"]
        self.assertEqual(st["topics"]["as-is"]["verdict"], "stale")

    def test_the_check_file_is_not_read_as_a_synthesis_run(self):
        eng = self._stale()
        run_hook(eng / "_synthesis" / "as-is.md")
        checks = (eng / "_synthesis" / "_synthesis-checks.md").read_text(encoding="utf-8")
        self.assertTrue(checks.strip())
        entries = D["synthesis_entries"](checks)
        self.assertEqual(entries, [], "as linhas de check leem-se como corridas de síntese")

    def test_the_hook_never_validates_the_log_files(self):
        eng = self._stale()
        for name in ("_synthesis-log.md", "_synthesis-checks.md"):
            r = run_hook(eng / "_synthesis" / name)
            self.assertEqual(r.returncode, 0)
        checks = (eng / "_synthesis" / "_synthesis-checks.md")
        if checks.is_file():
            self.assertNotIn("_synthesis-log", checks.read_text(encoding="utf-8"))


class RecomputedOnRead(unittest.TestCase):
    """O log é história; o veredicto é de agora."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def test_a_clean_pack_records_ok(self):
        eng = mk(self.tmp.name)
        run_hook(eng / "_synthesis" / "as-is.md")
        rec = D["synthesis_check_log"](eng)["as-is"]
        self.assertEqual(rec["result"], "ok")
        self.assertEqual(D["synthesis_checks"](eng)["topics"]["as-is"]["verdict"], "ok")

    def test_changing_the_text_makes_the_record_stale_and_the_verdict_new(self):
        eng = mk(self.tmp.name)
        run_hook(eng / "_synthesis" / "as-is.md")
        (eng / "_synthesis" / "as-is.md").write_text("# As-is\n\nSó um parágrafo (C-001).\n",
                                                     encoding="utf-8")
        t = D["synthesis_checks"](eng)["topics"]["as-is"]
        self.assertTrue(t["stale_record"])
        self.assertIn("SYN-PARAS", t["codes"])
        self.assertEqual(t["recorded"]["result"], "ok")     # a linha antiga fica, como história

    def test_removing_the_cited_row_changes_the_verdict_without_touching_the_text(self):
        """O caso que um sha do texto não apanharia."""
        eng = mk(self.tmp.name)
        run_hook(eng / "_synthesis" / "as-is.md")
        self.assertEqual(D["synthesis_checks"](eng)["topics"]["as-is"]["verdict"], "ok")
        (eng / "shared-understanding.md").write_text(
            SU.replace("| C-002 | data | o histórico vive numa base partilhada | "
                       "inputs/x.xlsx#S!A2 | 2026-09-01 | organizacional | R-01 |\n", ""),
            encoding="utf-8")
        t = D["synthesis_checks"](eng)["topics"]["as-is"]
        self.assertIn("SYN-DEAD-ID", t["codes"])
        self.assertTrue(t["stale_record"])

    def test_the_last_line_per_topic_is_the_one_that_counts(self):
        eng = mk(self.tmp.name)
        run_hook(eng / "_synthesis" / "as-is.md")
        (eng / "_synthesis" / "as-is.md").write_text("# As-is\n\nUm (C-001).\n", encoding="utf-8")
        run_hook(eng / "_synthesis" / "as-is.md")
        text = (eng / "_synthesis" / "_synthesis-checks.md").read_text(encoding="utf-8")
        self.assertEqual(len([l for l in text.splitlines() if l.startswith("check ·")]), 2)
        self.assertIn("SYN-PARAS", D["synthesis_check_log"](eng)["as-is"]["result"])
        self.assertFalse(D["synthesis_checks"](eng)["topics"]["as-is"]["stale_record"])

    def test_the_line_carries_the_dependency_fingerprint(self):
        eng = mk(self.tmp.name)
        run_hook(eng / "_synthesis" / "as-is.md")
        rec = D["synthesis_check_log"](eng)["as-is"]
        self.assertTrue(rec["deps"])
        self.assertEqual(rec["deps"], D["synthesis_check"](eng, "as-is")["deps"])


class HookBehaviour(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def test_it_reports_and_never_blocks(self):
        eng = mk(self.tmp.name, packs={"as-is": "# As-is\n\nUm.\n"})
        r = run_hook(eng / "_synthesis" / "as-is.md")
        self.assertEqual(r.returncode, 0)
        self.assertIn("SYN-", r.stderr)

    def test_other_writes_are_ignored(self):
        r = subprocess.run(
            [sys.executable, str(HOOK)],
            input=json.dumps({"tool_name": "Write", "tool_input": {"file_path": "notes.md"}}),
            text=True, capture_output=True, encoding="utf-8", errors="replace", cwd=str(ROOT))
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stderr.strip(), "")

    def test_broken_input_is_fail_open(self):
        r = subprocess.run([sys.executable, str(HOOK)], input="not json", text=True,
                           capture_output=True, encoding="utf-8", errors="replace", cwd=str(ROOT))
        self.assertEqual(r.returncode, 0)


class Wiring(unittest.TestCase):

    def test_every_pack_declares_its_solution_terms(self):
        for pack in ("pp", "generic", "outsystems", "mendix"):
            p = ROOT / "library" / "packs" / pack / "pack.yaml"
            if p.is_file():
                self.assertIn("vendor_terms:", p.read_text(encoding="utf-8"), pack)

    def test_the_discovery_list_and_the_solution_list_are_not_the_same(self):
        solution = set(D["pack_vendor_terms"]("pp"))
        self.assertIn("dataverse", solution)
        for current_state in ("sharepoint", "microsoft", "azure", "excel"):
            self.assertNotIn(current_state, solution)

    def test_the_skill_reads_the_recomputed_check(self):
        md = (ROOT / ".claude" / "skills" / "aisa-synthesize" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("synthesis_checks", md)
        self.assertIn("_synthesis-checks.md", md)

    def test_the_model_exposes_the_checks(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = mk(tmp)
            model = D["build_model"](eng, TODAY)
            self.assertIn("synthesis_checks", model["status"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
