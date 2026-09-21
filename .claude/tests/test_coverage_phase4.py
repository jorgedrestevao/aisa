# -*- coding: utf-8 -*-
"""Fase 4 da reconciliação/cobertura — integração no desenho, nas respostas e no estado.

A fase 3 entregou o motor e deixou-o **desligado**. Esta fase liga-o, e a pergunta que
importa deixa de ser *o motor calcula bem?* (isso já está coberto pelas três suites
anteriores) e passa a ser:

  1. O que é que quem consulta o estado **vê**, e consegue ver as quatro perguntas
     separadas — estrutura, cobertura, aprovação e ponta-a-ponta?
  2. O que é que a integração **não** faz: não escreve aprovações, não revoga as antigas,
     não guarda booleanos de verdade, não transforma «não avaliado» em verde, e não gera
     ciclos de escrita por alguém olhar para o estado.

As fixtures são as da fase 1 (`fixtures/coverage/fx-coverage-f06`), copiadas para um
temporário. O engagement real nunca é tocado.

    python .claude/tests/test_coverage_phase4.py
"""

import hashlib
import io
import json
import os
import runpy
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_coverage_integration as I          # noqa: E402  (fixture helpers, fase 3)

ROOT = Path(__file__).resolve().parents[2]
DASH_PATH = ROOT / "library" / "kernel" / "tools" / "dashboard.py"
ENGINE = ROOT / "library" / "kernel" / "tools" / "coverage.py"
FIX = Path(__file__).resolve().parent / "fixtures" / "coverage" / "fx-coverage-f06"
TODAY = date(2026, 9, 15)

D = runpy.run_path(str(DASH_PATH))
C = runpy.run_path(str(ENGINE))

RECON = "rec-v01-reconciliation-complete"
# `rec-v04` diz ter assentado na `v03`, que por sua vez assenta na `v01`: a cadeia entra
# toda, ou a revisão a jusante não vale mais do que a montante que não se consegue ler.
CHAIN_V03 = (RECON, "rec-v03-blueprint-partial", "rec-v04-blueprint-complete")
BP01, BP02, BP03 = ("_blueprint/ux-blueprint_v01.yaml",
                    "_blueprint/ux-blueprint_v02.yaml",
                    "_blueprint/ux-blueprint_v03.yaml")

APPROVAL = """
## D-003 — Blueprint bp-v03 aprovado

- **Aprovado por**: dono do processo
- **Cobertura consumida**: _coverage/coverage_v04.json
- **Timestamp**: 2026-09-15T10:00:00+01:00
"""


def manifest(root: Path, skip=()) -> dict:
    out = {}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            rel = p.relative_to(root).as_posix()
            if any(rel.startswith(s) for s in skip):
                continue
            out[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def hook(name: str, *args, root: Path | None = None):
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    if root:
        env["AISA_ENGAGEMENTS_ROOT"] = str(root)
    return subprocess.run([sys.executable, "-B", str(ROOT / ".claude" / "hooks" / name),
                           *args], cwd=str(ROOT), env=env, text=True, capture_output=True,
                          encoding="utf-8", errors="replace", input="")


class Base(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.eng = self.root / "fx-coverage-f06"
        shutil.copytree(FIX, self.eng)

    # -- fixture plumbing ------------------------------------------------------------
    def install(self, *names):
        (self.eng / "_coverage").mkdir(exist_ok=True)
        for name in names:
            rec = I.hydrate(self.eng, I.load(name))
            (self.eng / "_coverage" / ("coverage_%s.json" % rec["version"])).write_text(
                json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")

    def only_version(self, keep: str):
        """Leave a single non-draft version on disk, so `current` is the one under test."""
        for p in (self.eng / "_blueprint").glob("ux-blueprint_v*.yaml"):
            if p.name != keep:
                p.unlink()

    def append(self, rel: str, text: str):
        with io.open(self.eng / rel, "a", encoding="utf-8") as fh:
            fh.write(text)

    def cov(self) -> dict:
        return D["build_model"](self.eng, TODAY)["status"]["coverage"]


# ====================================================== A. as quatro perguntas separadas

class FourQuestions(Base):
    """Estrutura, cobertura, aprovação e ponta-a-ponta. Nenhuma responde pela outra."""

    def test_a_valid_structure_does_not_make_the_design_covered(self):
        """T01 — a asserção central do F06, agora pelo caminho que o utilizador percorre.

        A mesma versão que o verificador estrutural dá por válida perdeu dois requisitos
        que a Shared Understanding já carregava."""
        self.only_version("ux-blueprint_v01.yaml")
        self.install(RECON, "rec-v02-blueprint-missing")
        c = self.cov()
        self.assertEqual(c["readiness"]["structure"], "valid")
        self.assertEqual(c["readiness"]["coverage"], "gaps")
        self.assertFalse(c["approve_eligible"])
        refs = sorted({r for g in c["stages"]["blueprint"]["gaps"]
                       for r in g.get("requirement_refs", [])})
        self.assertEqual(refs, ["C-007", "C-010"])

    def test_a_decorative_reference_is_not_coverage(self):
        """T02 — o destino que cita o id sem concretizar nada não vira `covered`."""
        self.only_version("ux-blueprint_v01.yaml")
        self.install(RECON, "rec-neg-decorative-projection")
        c = self.cov()
        self.assertEqual(c["readiness"]["coverage"], "gaps")
        self.assertIn("COV-MISSING-TARGET", c["stages"]["blueprint"]["codes"])

    def test_complete_coverage_is_still_not_an_approval(self):
        """T03 — sem lacunas, sem escolha estrutural aberta, e aprovação na mesma ausente.

        `approve_eligible` diz que a versão PODE ser levada ao negócio. Nada mais."""
        self.install(*CHAIN_V03)
        c = self.cov()
        self.assertEqual(c["readiness"]["coverage"], "complete")
        self.assertEqual(c["readiness"]["approval"], "absent")
        self.assertTrue(c["approve_eligible"])
        self.assertEqual(c["readiness"]["e2e"], "not_evaluated")
        self.assertNotIn("D-003", (self.eng / "decisions.md").read_text(encoding="utf-8"))

    def test_end_to_end_is_never_claimed_from_here(self):
        for names in ((), CHAIN_V03):
            with self.subTest(records=len(names)):
                if names:
                    self.install(*names)
                self.assertEqual(self.cov()["readiness"]["e2e"], "not_evaluated")

    def test_the_block_publishes_its_own_judgement(self):
        """`/status` lê `julgamento` antes de reportar: diz o que o bloco não prova."""
        self.install(*CHAIN_V03)
        j = self.cov()["julgamento"]
        self.assertIn("quatro perguntas separadas", j)
        self.assertIn("nunca que o negócio aprovou", j)


# =========================================================== B. o que nunca dá verde

class NeverAFalseGreen(Base):

    def test_no_record_is_not_evaluated_and_never_complete(self):
        c = self.cov()
        self.assertFalse(c["present"])
        self.assertEqual(c["readiness"]["coverage"], "not_evaluated")
        self.assertIsNone(c["approve_eligible"])
        self.assertIn("não avaliado", c["julgamento"])

    def test_a_pending_semantic_review_is_not_complete(self):
        """T30 — todas as referências resolvem e a leitura não foi feita."""
        self.install(RECON, "rec-neg-semantic-pending")
        c = self.cov()
        self.assertEqual(c["stages"]["blueprint"]["semantic_review"], "pending")
        self.assertFalse(c["approve_eligible"])

    def test_an_unreadable_record_is_invalid_not_absent(self):
        """T24 — JSON partido em `_coverage/` nunca se lê como «ainda não há revisão»."""
        self.install(*CHAIN_V03)
        (self.eng / "_coverage" / "coverage_v07.json").write_text("{ nope",
                                                                  encoding="utf-8")
        c = self.cov()
        self.assertTrue(c["present"])
        self.assertEqual(c["readiness"]["coverage"], "invalid")
        self.assertFalse(c["approve_eligible"])

    def test_a_future_schema_is_unsupported_not_interpreted(self):
        """T24 — schema desconhecido não se interpreta por aproximação."""
        self.install(RECON, "rec-neg-schema-future")
        c = self.cov()
        self.assertIn(c["stages"]["blueprint"]["contract_validity"],
                      ("unsupported", "invalid"))
        self.assertFalse(c["approve_eligible"])

    def test_a_review_of_another_version_is_not_consumed_for_this_one(self):
        """T22 — rever a `v01` e tentar consumir para a `v03`.

        A revisão é de uma versão concreta. Havendo só a da `v01`, a versão actual fica
        `not_evaluated` — nunca «completa» por empréstimo."""
        self.install(RECON, "rec-v02-blueprint-missing")          # alvo: v01
        c = self.cov()
        self.assertEqual(c["readiness"]["current_version"], "v03")
        self.assertEqual(c["stages"]["blueprint"]["coverage"], "not_evaluated")
        self.assertIn("COV-NO-REVIEW", c["stages"]["blueprint"]["codes"])
        self.assertFalse(c["approve_eligible"])

    def test_the_newer_review_wins_even_when_it_is_the_worse_one(self):
        """T23 — nunca escolher a antiga para esconder que a recente não fechou."""
        self.install(*CHAIN_V03)                                  # v04: completa
        c = self.cov()
        self.assertEqual(c["stages"]["blueprint"]["record"], "_coverage/coverage_v04.json")
        self.install("rec-neg-semantic-pending")                  # v14: leitura por acabar
        c = self.cov()
        self.assertEqual(c["stages"]["blueprint"]["record"], "_coverage/coverage_v14.json")
        self.assertEqual(c["stages"]["blueprint"]["semantic_review"], "pending")
        self.assertFalse(c["approve_eligible"])

    def test_an_open_question_is_not_a_gap(self):
        """T37 — a reconciliação fecha com perguntas em aberto; o que não fecha é obrigação.

        A fixture deixa `U-010` aberta de propósito: uma pergunta em aberto é uma pergunta
        em aberto, não uma obrigação por cobrir — e não impede produzir."""
        self.install(RECON)
        recon = self.cov()["stages"]["reconciliation"]
        self.assertEqual(recon["coverage"], "complete")
        self.assertTrue(recon["eligible"])
        self.assertEqual(recon["gaps"], [])
        self.assertIn("U-010", (self.eng / "shared-understanding.md").read_text(
            encoding="utf-8"))

    def test_an_engine_failure_is_reported_as_incomplete_not_as_zero_gaps(self):
        """Uma verificação que não correu não é uma verificação que passou.

        O motor ausente simula-se como ele falha de verdade: uma cópia do dashboard sem
        o `coverage.py` ao lado. Mexer na variável de módulo não serviria — `run_path`
        devolve uma **cópia** dos globals, e as funções continuariam a ler os seus."""
        alone = self.root / "tools"
        alone.mkdir()
        shutil.copy2(DASH_PATH, alone / "dashboard.py")
        dash = runpy.run_path(str(alone / "dashboard.py"))
        c = dash["coverage_status"](self.eng, {"current": None}, "pp")
        self.assertEqual(c["engine"], "absent")
        self.assertEqual(c["readiness"]["coverage"], "not_evaluated")
        self.assertIn("verificação", c["julgamento"])
        self.assertIn("nunca «sem lacunas»", c["julgamento"])

    def test_a_structurally_invalid_version_is_named_as_its_own_blocker(self):
        """A estrutura e a cobertura bloqueiam por razões próprias, e dizem qual é qual."""
        self.only_version("ux-blueprint_v03.yaml")
        self.install(*CHAIN_V03)
        text = (self.eng / "_blueprint" / "ux-blueprint_v03.yaml").read_text(
            encoding="utf-8")
        (self.eng / "_blueprint" / "ux-blueprint_v03.yaml").write_text(
            text + "\ndraft: true\n", encoding="utf-8")       # BP-DRAFT: block
        c = self.cov()
        self.assertEqual(c["readiness"]["structure"], "invalid")
        self.assertFalse(c["approve_eligible"])
        self.assertTrue(any("estrutura" in b.lower() for b in c["blockers"]), c["blockers"])


# ================================================ C. atualidade pelo caminho do executor

class Freshness(Base):

    def test_a_new_answer_makes_the_applicable_review_stale(self):
        """T17 — responder muda `answers.md` e a SU; a revisão anterior deixa de valer.

        `stale` não diz que a conclusão ficou falsa: diz que ninguém releu as fontes
        desde que elas mudaram."""
        self.install(*CHAIN_V03)
        self.assertEqual(self.cov()["stages"]["blueprint"]["freshness"], "current")
        self.append("answers.md", "\n## U-010 — 2026-09-15\n\n- **Resposta**: novo facto.\n")
        c = self.cov()
        self.assertEqual(c["stages"]["reconciliation"]["freshness"], "stale")
        self.assertIn("COV-STALE", c["stages"]["reconciliation"]["codes"])
        self.assertEqual(c["readiness"]["coverage"], "stale")

    def test_a_changed_solution_decision_invalidates(self):
        """T20 — mudar a decisão-solução invalida, mesmo com o mesmo id."""
        self.install(*CHAIN_V03)
        p = self.eng / "decisions.md"
        p.write_text(p.read_text(encoding="utf-8").replace(
            "- **Sponsor confirmation**: yes",
            "- **Sponsor confirmation**: yes\n- **Nota nova**: âmbito alterado"),
            encoding="utf-8")
        self.assertEqual(self.cov()["stages"]["reconciliation"]["freshness"], "stale")

    def test_appending_a_blueprint_approval_does_not_invalidate_the_review(self):
        """T19 — o ciclo que este contrato existe para partir.

        Aprovar acrescenta um bloco a `decisions.md`. Se isso invalidasse a revisão, a
        aprovação destruiria a revisão de que depende, e nenhuma versão seria aprovável
        duas vezes seguidas."""
        self.install(*CHAIN_V03)
        before = self.cov()
        self.append("decisions.md", APPROVAL)
        after = self.cov()
        self.assertEqual(after["stages"]["blueprint"]["freshness"], "current")
        self.assertEqual(after["readiness"]["coverage"], before["readiness"]["coverage"])
        self.assertEqual(after["readiness"]["approval"], "approved")
        self.assertEqual(after["readiness"]["approved_version"], "v03")

    def test_editing_the_version_after_the_review_makes_it_stale(self):
        """T21 — a revisão é de uma versão concreta, e o alvo tem digest."""
        self.install(*CHAIN_V03)
        p = self.eng / "_blueprint" / "ux-blueprint_v03.yaml"
        p.write_text(p.read_text(encoding="utf-8") + "\n# nota posterior\n",
                     encoding="utf-8")
        self.assertEqual(self.cov()["stages"]["blueprint"]["freshness"], "stale")

    def test_regenerating_the_dashboard_does_not_make_anything_stale(self):
        """T18 — o derivado não pode invalidar aquilo de que deriva."""
        self.install(*CHAIN_V03)
        first = self.cov()["stages"]["blueprint"]["freshness"]
        (self.eng / "dashboard.html").write_text("<html>gerado</html>", encoding="utf-8")
        (self.eng / "_blueprint" / "blueprint-log.md").write_text("log\n", encoding="utf-8")
        self.assertEqual(first, "current")
        self.assertEqual(self.cov()["stages"]["blueprint"]["freshness"], "current")


# ================================================= D. compatibilidade: o legado sobrevive

class Legacy(Base):
    """T35 — engagement sem `_coverage/` e **com** aprovação histórica."""

    def setUp(self):
        super().setUp()
        self.append("decisions.md", APPROVAL)

    def test_the_historical_approval_is_preserved_and_reported(self):
        c = self.cov()
        self.assertEqual(c["readiness"]["approval"], "approved")
        self.assertEqual(c["readiness"]["approved_version"], "v03")
        self.assertEqual(c["readiness"]["coverage"], "not_evaluated")

    def test_introducing_the_mechanism_rewrites_no_decision(self):
        before = (self.eng / "decisions.md").read_bytes()
        self.cov()
        self.assertEqual((self.eng / "decisions.md").read_bytes(), before)

    def test_not_evaluated_is_neither_a_pass_nor_a_failure(self):
        c = self.cov()
        self.assertNotIn(c["readiness"]["coverage"], ("complete", "gaps"))
        self.assertIsNone(c["approve_eligible"])
        self.assertIn("não revoga aprovação nenhuma", c["julgamento"])


# ========================================================= E. ler o estado não escreve

class ReadOnly(Base):

    def test_building_the_model_twice_mutates_nothing_and_says_the_same(self):
        """T38 — e é o que impede que olhar para o estado gere ciclos de escrita."""
        self.install(*CHAIN_V03)
        before = manifest(self.eng, skip=("dashboard.html",))
        first = self.cov()
        second = self.cov()
        self.assertEqual(manifest(self.eng, skip=("dashboard.html",)), before)
        self.assertEqual(first["readiness"], second["readiness"])
        self.assertEqual(first["stages"]["blueprint"]["gaps"],
                         second["stages"]["blueprint"]["gaps"])

    def test_no_truth_boolean_reaches_the_state_file(self):
        """Contrato §10 — o estado de cobertura deriva dos registos, e nunca se guarda."""
        self.install(*CHAIN_V03)
        before = (self.eng / "_state.json").read_bytes()
        self.cov()
        after = json.loads((self.eng / "_state.json").read_text(encoding="utf-8"))
        self.assertEqual((self.eng / "_state.json").read_bytes(), before)
        self.assertEqual([k for k in after if "coverage" in k.lower()], [])

    def test_the_skills_forbid_writing_such_a_flag(self):
        for rel in (".claude/skills/aisa-answer/SKILL.md",
                    ".claude/skills/aisa-capture/SKILL.md"):
            md = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("_state.json", md, rel)
            self.assertRegex(md, r"(?i)(nenhum|no) (flag|boolean)", rel)


# ======================================================================= F. os hooks

class Hooks(Base):

    def test_blueprint_validate_reports_coverage_beside_structure(self):
        self.only_version("ux-blueprint_v01.yaml")
        self.install(RECON, "rec-v02-blueprint-missing")
        r = hook("blueprint-validate.py", str(self.eng / "_blueprint" /
                                              "ux-blueprint_v01.yaml"))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("cobertura:", r.stderr)
        self.assertIn("C-007", r.stderr)
        self.assertIn("perguntas separadas", r.stderr)

    def test_blueprint_validate_says_not_evaluated_never_no_gaps(self):
        r = hook("blueprint-validate.py", str(self.eng / "_blueprint" /
                                              "ux-blueprint_v03.yaml"))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("não avaliada", r.stderr)
        self.assertIn("não revoga aprovação nenhuma", r.stderr)

    def test_blueprint_validate_writes_nothing(self):
        self.install(*CHAIN_V03)
        before = manifest(self.eng)
        hook("blueprint-validate.py", str(self.eng / "_blueprint" /
                                          "ux-blueprint_v03.yaml"))
        self.assertEqual(manifest(self.eng), before)

    def test_publishing_a_review_makes_the_page_stale(self):
        """F01 da revisão independente — e o defeito era meio arranjo, não zero.

        `_coverage/` nos gatilhos do hook não chegava: o hook lança o gerador **sem**
        `--force`, e quem decide se vale a pena regenerar é `_needs_rebuild`, que percorre
        `INDEX_DIRS`. Fora dessa lista, publicar uma revisão mudava o modelo e deixava a
        página com o veredicto antigo."""
        self.assertIn("_coverage", D["INDEX_DIRS"])
        out = self.eng / "dashboard.html"
        out.write_text("<html>antigo</html>", encoding="utf-8")
        self.assertFalse(D["_needs_rebuild"](self.eng, out, 0))
        time.sleep(0.05)
        self.install(RECON)
        self.assertTrue(D["_needs_rebuild"](self.eng, out, 0),
                        "publicar uma revisão tem de tornar a página desactualizada")

    def test_regenerating_the_page_does_not_ask_for_another_rebuild(self):
        """O outro lado da mesma moeda: incluir a pasta não pode gerar um ciclo."""
        self.install(RECON)
        out = self.eng / "dashboard.html"
        time.sleep(0.05)
        out.write_text("<html>regenerado</html>", encoding="utf-8")
        self.assertFalse(D["_needs_rebuild"](self.eng, out, 0))

    def test_the_reviews_are_listed_in_business_language(self):
        """A pasta entra no índice de ficheiros, e com um nome que se lê."""
        self.install(RECON)
        groups = {a["group"] for a in D["build_model"](self.eng, TODAY)["artefacts"]}
        self.assertIn("_coverage", groups)
        self.assertEqual(D["GROUP_LABEL"]["_coverage"], "Conferência do que foi pedido")

    def test_on_su_change_triggers_on_the_coverage_folder(self):
        H = runpy.run_path(str(ROOT / ".claude" / "hooks" / "on-su-change.py"))
        self.assertTrue(H["should_trigger"]("projects/x/_coverage/coverage_v01.json"))
        self.assertTrue(H["should_trigger"]("projects/x/_blueprint/ux-blueprint_v01.yaml"))
        # o derivado nunca é gatilho de si próprio
        self.assertFalse(H["should_trigger"]("projects/x/notas.txt"))

    def test_phase_completeness_asks_for_nothing_before_a_blueprint_exists(self):
        """Logo depois de `/decide` não há desenho para cobrir — e nada a reportar."""
        shutil.rmtree(self.eng / "_blueprint")
        r = hook("phase-completeness.py", "--engagement", "fx-coverage-f06",
                 root=self.root)
        self.assertEqual(r.returncode, 0)
        self.assertNotIn("_coverage", r.stderr)

    def test_phase_completeness_asks_once_a_version_exists(self):
        r = hook("phase-completeness.py", "--engagement", "fx-coverage-f06",
                 root=self.root)
        self.assertEqual(r.returncode, 0)
        self.assertIn("revisao de reconciliacao em _coverage/", r.stderr)
        self.assertIn("revisao de cobertura da versao actual", r.stderr)

    def test_phase_completeness_is_satisfied_by_the_records(self):
        self.install(*CHAIN_V03)
        r = hook("phase-completeness.py", "--engagement", "fx-coverage-f06",
                 root=self.root)
        self.assertEqual(r.returncode, 0)
        self.assertNotIn("revisao de reconciliacao em _coverage/", r.stderr)
        self.assertNotIn("revisao de cobertura da versao actual", r.stderr)

    def test_no_hook_is_the_mechanism(self):
        """T25 — sem hooks, os mesmos dois checks correm à mão, e estão documentados."""
        self.only_version("ux-blueprint_v01.yaml")
        self.install(RECON, "rec-v02-blueprint-missing")
        r = I.cli("check", "--engagement", str(self.eng), "--stage", "blueprint",
                  "--target", BP01, "--json")
        self.assertEqual(r.returncode, 4)
        self.assertEqual(json.loads(r.stdout)["coverage"], "gaps")
        skill = (ROOT / ".claude" / "skills" / "aisa-blueprint" / "SKILL.md").read_text(
            encoding="utf-8")
        self.assertIn("coverage.py check --engagement <slug> --stage reconciliation",
                      skill)
        self.assertIn("the hook is a convenience, never the mechanism", skill)


# ================================================== G. o protocolo que as skills declaram

class Protocol(unittest.TestCase):

    BP = (ROOT / ".claude" / "skills" / "aisa-blueprint" / "SKILL.md").read_text(
        encoding="utf-8")
    ANSWER = (ROOT / ".claude" / "skills" / "aisa-answer" / "SKILL.md").read_text(
        encoding="utf-8")
    CAPTURE = (ROOT / ".claude" / "skills" / "aisa-capture" / "SKILL.md").read_text(
        encoding="utf-8")
    STATUS = (ROOT / ".claude" / "skills" / "aisa-status" / "SKILL.md").read_text(
        encoding="utf-8")
    BPC = (ROOT / "library" / "kernel" / "blueprint-contract.md").read_text(
        encoding="utf-8")
    PHASES = (ROOT / "library" / "kernel" / "phases.md").read_text(encoding="utf-8")
    ORCH = (ROOT / "library" / "kernel" / "orchestration.md").read_text(encoding="utf-8")
    COV = (ROOT / "library" / "kernel" / "coverage-contract.md").read_text(
        encoding="utf-8")

    def test_the_blueprint_skill_reconciles_before_and_reviews_after(self):
        self.assertIn("1e. **Reconciliation", self.BP)
        self.assertIn("13b. **Coverage of the version just written", self.BP)
        self.assertIn("--stage blueprint --target", self.BP)

    def test_the_five_conditions_of_a_new_approval_are_written_out(self):
        step = self.BP[self.BP.index("15. **On approval**"):]
        for needle in ("current** for **this** version", "semantic_review.status: completed",
                       "authorized scope disposition", "structural blocks",
                       "no motor replaces"):
            self.assertIn(needle, step, needle)
        self.assertIn("AskUserQuestion", step)
        self.assertIn("never rewritten, superseded or revoked by this rule", step)
        self.assertIn("`not_evaluated` is **not** a pass", step)

    def test_producing_with_gaps_stays_possible_and_draft_keeps_its_meaning(self):
        self.assertIn("A version with gaps is produced, written and discussed", self.BP)
        self.assertIn("candidate before the decision", self.BP)
        self.assertIn('never becomes a\n   marker for "produced with gaps"', self.BPC)

    def test_answer_and_capture_compute_staleness_and_write_no_flag(self):
        self.assertIn("--stage reconciliation --json", self.ANSWER)
        self.assertIn("No boolean is written anywhere", self.ANSWER)
        self.assertIn("--stage reconciliation --json", self.CAPTURE)
        self.assertIn("No flag is written anywhere", self.CAPTURE)

    def test_status_reports_four_answers_and_never_merges_them(self):
        self.assertIn("status.coverage", self.STATUS)
        self.assertIn("readiness.structure", self.STATUS)
        self.assertIn("Conferência do desenho", self.STATUS)
        self.assertIn("four separate answers", self.STATUS)

    def test_the_contracts_carry_the_new_approval_condition(self):
        self.assertIn("A new approval requires an applicable coverage review", self.BPC)
        self.assertIn("coverage-contract.md", self.BPC)
        self.assertIn("Readiness is not approval", self.PHASES)
        self.assertIn("no fifth phase", self.PHASES)
        self.assertIn("where the disposition stops being a promise", self.ORCH)

    def test_the_coverage_contract_says_this_phase_wired_design_and_reconciliation(self):
        """O que ESTA fase entregou, e nada sobre o que as seguintes entregarem.

        Até à fase 5 esta asserção prendia também a frase «render por ligar»; quando a
        fase 5 ligou a terceira etapa, essa metade passou a ser dela
        (`test_coverage_phase5.py` -> `WhatTheContractsSay`). Uma fase não afirma o estado
        de ligação de outra: era assim que um contrato desactualizado passava despercebido
        por haver dois testes a dizer coisas diferentes."""
        head = self.COV[:self.COV.index("## 1. O que a cobertura")]
        self.assertIn("`reconciliation` e `blueprint` estão **ligadas ao runtime**", head)
        self.assertIn("passo 1b", head)
        self.assertIn("passo 13b", head)
        self.assertIn("`status.coverage`", head)

    def test_nothing_in_the_integration_writes_a_decision(self):
        """O motor nunca escreve uma aprovação — nem por engano, nem por conveniência."""
        engine = ENGINE.read_text(encoding="utf-8")
        flat = " ".join(engine.split())
        self.assertIn("não escreve decisões, não aprova nada", flat)
        self.assertIn("a ÚNICA operação de escrita, e escreve só em `_coverage/`", flat)
        for hook_name in ("blueprint-validate.py", "phase-completeness.py"):
            src = (ROOT / ".claude" / "hooks" / hook_name).read_text(encoding="utf-8")
            # A única escrita do motor não é invocável a partir de um hook de relato.
            self.assertNotIn('["finalize"]', src, hook_name)
            self.assertNotIn("finalize(", src, hook_name)
            self.assertNotIn('"w"', src, hook_name)

    def test_the_engine_header_states_where_it_is_wired(self):
        """Um motor que diz estar desligado depois de ligado é documentação a mentir."""
        flat = " ".join(ENGINE.read_text(encoding="utf-8").split())
        self.assertIn("`aisa-blueprint` nos passos 1e, 13b e 15", flat)
        self.assertIn("A etapa `render` está implementada e **continua por ligar**", flat)


if __name__ == "__main__":
    unittest.main(verbosity=2)
