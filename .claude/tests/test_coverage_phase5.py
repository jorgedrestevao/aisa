# -*- coding: utf-8 -*-
"""Fase 5 da reconciliação/cobertura — preservação em síntese e deliverables.

A fase 4 ligou `reconciliation` e `blueprint`. Esta liga a terceira etapa, e a pergunta
que importa é a da projecção:

  1. Cada deliverable lê a **versão que o seu contrato manda ler** — e a cobertura
     verifica isso sem a redefinir (T31, T22).
  2. Uma referência **não** é uma projecção: um id num comentário não prova preservação
     (T32); uma saída exigida que se perdeu é lacuna, e o renderer não a inventa (T33).
  3. O que **não** pode ficar retido: sem UI, headless, sem arquitectura autorizada,
     legado. Ausência legítima é *não aplicável*, nunca lacuna (T34, T35).
  4. Sem registo, sem registo legível ou com schema futuro: nunca verde (T24); template
     alterado depois da revisão, stale (T39); Markdown editado à mão não muda autoridade
     nenhuma (T40).

As fixtures são as da fase 1 (`fixtures/coverage/fx-coverage-f06`), copiadas para um
temporário. O engagement real nunca é tocado.

    python .claude/tests/test_coverage_phase5.py
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
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_coverage_integration as I          # noqa: E402  (fixture helpers, fase 3)

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "library" / "kernel" / "tools" / "coverage.py"
FIX = Path(__file__).resolve().parent / "fixtures" / "coverage" / "fx-coverage-f06"
TEMPLATES = ROOT / "library" / "packs" / "pp" / "deliverable-templates"
CONTRACT = (ROOT / "library" / "kernel" / "coverage-contract.md").read_text(encoding="utf-8")
RENDER_CONTRACT = (ROOT / "library" / "kernel" / "render-contract.md").read_text(encoding="utf-8")
RENDER_SKILL = (ROOT / ".claude" / "skills" / "aisa-render" / "SKILL.md").read_text(encoding="utf-8")
SYNTH_SKILL = (ROOT / ".claude" / "skills" / "aisa-synthesize" / "SKILL.md").read_text(encoding="utf-8")

C = runpy.run_path(str(ENGINE))

RECON = "rec-v01-reconciliation-complete"
# A cadeia inteira: `rec-v05` assenta na `v04`, que assenta na `v03`, que assenta na `v01`.
# Uma revisão não vale mais do que aquela em que diz assentar, e por isso entram todas.
CHAIN = (RECON, "rec-v02-blueprint-missing", "rec-v03-blueprint-partial",
         "rec-v04-blueprint-complete")
RENDER_V01 = "_render/fx-coverage-f06_solution-blueprint_v01.md"
RENDER_V02 = "_render/fx-coverage-f06_solution-blueprint_v02.md"
SPEC_TPL = "library/packs/pp/deliverable-templates/implementation-spec.template.md"
ARCH_TPL = "library/packs/pp/deliverable-templates/solution-blueprint.template.md"

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


class Base(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.eng = self.root / "fx-coverage-f06"
        shutil.copytree(FIX, self.eng)

    # -- fixture plumbing ------------------------------------------------------------
    def install(self, *names, mutate=None):
        (self.eng / "_coverage").mkdir(exist_ok=True)
        for name in names:
            rec = I.hydrate(self.eng, I.load(name))
            if mutate:
                mutate(name, rec)
            (self.eng / "_coverage" / ("coverage_%s.json" % rec["version"])).write_text(
                json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")

    def append(self, rel: str, text: str):
        with io.open(self.eng / rel, "a", encoding="utf-8") as fh:
            fh.write(text)

    def state(self, rel: str = RENDER_V02) -> dict:
        return C["coverage_state"](self.eng, "render", {
            "file": rel, "identity": C["target_identity"](self.eng, "render", rel)})

    def precheck(self, deliverable: str, template=None) -> dict:
        return C["render_precheck"](self.eng, deliverable, template)

    def codes(self, res: dict) -> list:
        return [d["code"] for d in res["diagnostics"] if d["severity"] == "error"]

    def cli(self, *args):
        env = dict(os.environ)
        env["PYTHONIOENCODING"] = "utf-8"
        return subprocess.run([sys.executable, "-B", str(ENGINE), *args], cwd=str(ROOT),
                              env=env, text=True, capture_output=True, encoding="utf-8",
                              errors="replace")

    def as_spec(self, template=SPEC_TPL, version_read=None, retarget=True):
        """Um registo da Implementation Specification, coerente em tudo menos no que o
        teste quer partir.

        Existe porque a primeira versão destes testes montava DUAS incoerências ao mesmo
        tempo — o `id` trocado deixava o documento revisto a ser o de outro deliverable —
        e um teste que acusa dois factos não prova qual deles o motor apanha. Cada caso
        parte um par de cada vez."""
        rel = "_render/fx-coverage-f06_implementation-spec_v01.md"
        body = (self.eng / RENDER_V02).read_text(encoding="utf-8")
        (self.eng / rel).write_text(body, encoding="utf-8")
        sha_doc = hashlib.sha256((self.eng / rel).read_bytes()).hexdigest()
        sha_tpl = hashlib.sha256((ROOT / template).read_bytes()).hexdigest()

        def mutate(name, rec):
            if rec.get("stage") != "render":
                return
            rec["deliverable"].update({"id": "implementation-spec", "template": template,
                                       "template_sha256": sha_tpl,
                                       "blueprint_version_read": version_read})
            for a in rec["basis"]["authorities"]:
                if a["path"].endswith(".template.md"):
                    a.update({"path": template, "sha256": sha_tpl})
            if not retarget:
                return
            rec["target"].update({"file": rel, "identity": "implementation-spec_v01",
                                  "sha256": sha_doc})
            for it in rec["coverage"]:
                for tg in it["targets"]:
                    tg["file"] = rel
        return mutate, rel

    def deauthorize(self):
        """Sem autorização de arquitectura para âmbito nenhum — o caso do `not applicable`."""
        for p in (self.eng / "_blueprint").glob("ux-blueprint_v*.yaml"):
            p.write_text(p.read_text(encoding="utf-8").replace(
                "authorization: authorized", "authorization: not-authorized"),
                encoding="utf-8")


# ================================================ A. a versão de autoridade, por contrato

class VersionAuthority(Base):
    """T31 — spec e brief pedem a aprovada; o relatório de arquitectura pede a última
    autorizada. A selecção é a do contrato de render; a cobertura **verifica**."""

    def test_every_template_declares_which_version_it_reads(self):
        """Ausente não é `none`: é o campo que decide a autoridade, e o silêncio nele era
        a leitura errada em silêncio."""
        for p in sorted(TEMPLATES.glob("*.template.md")):
            auth = C["template_authority"](
                self.eng, "library/packs/pp/deliverable-templates/" + p.name)
            self.assertEqual("ok", auth["state"], p.name)
            self.assertTrue(auth["known"],
                            p.name + ": `blueprint_version_read` ausente ou desconhecido")

    def test_the_architecture_report_reads_the_latest_authorized(self):
        pre = self.precheck("solution-blueprint")
        self.assertEqual("v<latest authorized>", pre["declared"])
        self.assertEqual("v03", pre["expected"]["version"])
        self.assertEqual("available", pre["expected"]["state"])

    def test_the_spec_and_the_brief_read_the_approved_one(self):
        for deliverable in ("implementation-spec", "claude-design-brief"):
            pre = self.precheck(deliverable)
            self.assertEqual("v<approved>", pre["declared"], deliverable)
            # A fixture tem v03 autorizada e nenhuma aprovada: bloqueado, com a razão.
            self.assertIsNone(pre["expected"]["version"], deliverable)
            self.assertEqual("not-approved", pre["expected"]["state"], deliverable)

    def test_an_approval_makes_the_approved_version_resolvable(self):
        self.append("decisions.md", APPROVAL)
        pre = self.precheck("implementation-spec")
        self.assertEqual("v03", pre["expected"]["version"])
        self.assertEqual("available", pre["expected"]["state"])

    def test_the_three_reasons_an_approved_version_is_missing_stay_distinct(self):
        """Não há autorização · há e não foi aprovada · escolha estrutural em aberto.
        Colapsá-las numa só apagava a diferença entre «falta decidir» e «falta aprovar»."""
        self.assertEqual("not-approved", self.precheck("implementation-spec")["expected"]["state"])
        self.deauthorize()
        self.assertEqual("no-authorization", self.precheck("implementation-spec")["expected"]["state"])

    def test_a_deliverable_that_reads_no_design_says_so(self):
        for deliverable in ("discovery-report", "executive-report", "estimate"):
            pre = self.precheck(deliverable)
            self.assertEqual("none", pre["declared"], deliverable)
            self.assertEqual("no-blueprint-read", pre["expected"]["state"], deliverable)

    def test_reading_the_wrong_version_is_an_authority_mismatch(self):
        """T22 — rever a `v01` e consumir para a versão que o contrato manda ler."""
        self.install(*CHAIN, "rec-neg-authority-mismatch")
        res = self.state()
        self.assertIn("COV-AUTHORITY-MISMATCH", self.codes(res))
        self.assertEqual("gaps", res["coverage"])
        self.assertFalse(res["eligible"])

    def test_the_mismatch_names_the_contract_and_not_only_the_upstream_record(self):
        """A verificação nova: contra o que o TEMPLATE manda ler, não só contra o
        `based_on`. Um registo coerente consigo próprio passava só com a antiga."""
        self.install(*CHAIN, "rec-neg-authority-mismatch")
        msgs = [d["message"] for d in self.state()["diagnostics"]
                if d["code"] == "COV-AUTHORITY-MISMATCH"]
        self.assertTrue(any("v<latest authorized>" in m for m in msgs),
                        "nenhum achado cita o token que o contrato declara: %r" % msgs)

    def test_the_spec_reading_the_authorized_version_is_caught_by_the_contract_check(self):
        """T31, e o caso que **só** a verificação nova apanha.

        A Implementation Specification a ler a última **autorizada**, coerente com o
        `based_on` que consome, com o seu próprio template e o seu próprio documento: a
        verificação antiga — `blueprint_version_read` contra o registo de desenho citado —
        não tem nada a dizer. É o contrato de projecção que exige a **aprovada**, e é por
        aí que construir sobre uma versão que ninguém validou passava."""
        mutate, rel = self.as_spec(version_read="v03")
        self.install(*CHAIN, "rec-v05-render-complete", mutate=mutate)
        res = self.state(rel)
        mism = [d for d in res["diagnostics"] if d["code"] == "COV-AUTHORITY-MISMATCH"]
        self.assertEqual(1, len(mism), "esperava só o achado do contrato: %r" % mism)
        self.assertIn("v<approved>", mism[0]["message"])
        self.assertEqual("gaps", res["coverage"])
        self.assertFalse(res["eligible"])

    def test_the_spec_reading_no_version_at_all_is_still_caught(self):
        """E o contrário do anterior: não declarar versão nenhuma também não serve quando
        o contrato exige a aprovada — passar por omissão era a saída fácil."""
        mutate, rel = self.as_spec(version_read=None)
        self.install(*CHAIN, "rec-v05-render-complete", mutate=mutate)
        res = self.state(rel)
        self.assertIn("COV-AUTHORITY-MISMATCH", self.codes(res))
        self.assertFalse(res["eligible"])

    # -- a identidade do contrato de projecção -------------------------------------
    #
    # O buraco que os 43 primeiros testes desta fase não apanhavam, e que a revisão
    # independente encontrou: todos eles verificavam a versão declarada contra o template
    # que o registo aponta, e nenhum perguntava se esse template é o DESTE deliverable.
    # Com `id: implementation-spec` a apontar para o template de arquitectura, a revisão
    # herdava `v<latest authorized>`, batia certo com `v03`, e saía `complete` + `eligible`
    # sem existir versão aprovada nenhuma — uma especificação aceite sem aprovação.

    def _spoof_id(self, deliverable_id):
        def mutate(name, rec):
            if rec.get("stage") == "render":
                rec["deliverable"]["id"] = deliverable_id
        return mutate

    def test_a_spec_reviewed_against_the_architecture_template_is_refused(self):
        """O caso reportado, tal como foi reportado: só o template é que é de outro
        deliverable — o documento revisto é o da spec, e o `id` concorda com ele."""
        mutate, rel = self.as_spec(template=ARCH_TPL, version_read="v03")
        self.install(*CHAIN, "rec-v05-render-complete", mutate=mutate)
        res = self.state(rel)
        self.assertEqual("gaps", res["coverage"])
        self.assertFalse(res["eligible"],
                         "uma especificação sem aprovação não pode sair elegível")
        mism = [d for d in res["diagnostics"] if d["code"] == "COV-AUTHORITY-MISMATCH"]
        self.assertEqual(1, len(mism), [d["message"] for d in mism])
        self.assertIn("implementation-spec", mism[0]["message"])
        self.assertIn("solution-blueprint", mism[0]["message"])

    def test_no_approved_version_exists_in_the_fixture(self):
        """Sem isto, o teste acima podia estar a passar pela razão errada."""
        self.assertIsNone(C["blueprint_versions"](self.eng)["approved"])

    def test_the_wrong_template_is_accused_once_and_the_token_is_not_reused(self):
        """Um facto, um achado — e o token do contrato errado não volta a ser avaliado:
        resolver `v03` a partir do template de outro deliverable era o próprio defeito."""
        mutate, rel = self.as_spec(template=ARCH_TPL, version_read="v03")
        self.install(*CHAIN, "rec-v05-render-complete", mutate=mutate)
        msgs = [d["message"] for d in self.state(rel)["diagnostics"]
                if d["code"] == "COV-AUTHORITY-MISMATCH"]
        self.assertEqual(1, len(msgs), msgs)
        self.assertNotIn("v<latest authorized>", msgs[0])

    def test_reviewing_another_deliverables_document_is_refused(self):
        """A porta gémea: `id` e `template` concordam um com o outro, e nenhum deles com o
        documento revisto. A revisão diz ser da spec e revê o relatório de arquitectura.

        A aprovação entra para que a autoridade da spec exista de facto: sem ela o registo
        teria **duas** incoerências, e o teste não provava qual delas o motor apanha."""
        self.append("decisions.md", APPROVAL)
        mutate, _ = self.as_spec(version_read="v03", retarget=False)
        self.install(*CHAIN, "rec-v05-render-complete", mutate=mutate)
        res = self.state()
        self.assertFalse(res["eligible"])
        mism = [d for d in res["diagnostics"] if d["code"] == "COV-AUTHORITY-MISMATCH"]
        self.assertEqual(1, len(mism), [d["message"] for d in mism])
        self.assertIn("solution-blueprint_v02", mism[0]["message"])

    def test_the_mismatch_is_symmetric(self):
        """Qualquer id que não seja o do template é recusado — não só este par."""
        self.install(*CHAIN, "rec-v05-render-complete",
                     mutate=self._spoof_id("claude-design-brief"))
        self.assertIn("COV-AUTHORITY-MISMATCH", self.codes(self.state()))

    def test_a_template_without_an_identity_cannot_confirm_the_contract(self):
        """Sem `template_id` não há como confirmar de quem é o contrato: não se adivinha
        pelo nome do ficheiro."""
        tpl = self.eng / "fake.template.md"
        tpl.write_text("---\nblueprint_version_read: v<latest authorized>\n---\n",
                       encoding="utf-8")
        sha = hashlib.sha256(tpl.read_bytes()).hexdigest()

        def point_at_it(name, rec):
            if rec.get("stage") == "render":
                rec["deliverable"].update({"template": "fake.template.md",
                                           "template_sha256": sha})
        self.install(*CHAIN, "rec-v05-render-complete", mutate=point_at_it)
        self.assertIn("COV-SCHEMA", self.codes(self.state()))

    def test_the_precheck_refuses_another_deliverables_template(self):
        """O mesmo dever no pré-render: devolver `v03 available` aqui era mandar o
        executor ler uma versão que o contrato da especificação não aceita."""
        pre = self.precheck("implementation-spec", ARCH_TPL)
        self.assertEqual(1, pre["blocking"])
        self.assertIn("COV-AUTHORITY-MISMATCH", [d["code"] for d in pre["diagnostics"]])
        self.assertIsNone(pre["expected"]["version"])
        self.assertEqual("not_evaluated", pre["expected"]["state"])

    def test_the_precheck_still_answers_for_the_right_template(self):
        pre = self.precheck("implementation-spec")
        self.assertEqual(0, pre["blocking"])
        self.assertEqual("not-approved", pre["expected"]["state"])
        self.assertEqual("implementation-spec", pre["template_id"])

    def test_the_positive_case_is_complete(self):
        self.install(*CHAIN, "rec-v05-render-complete")
        res = self.state()
        self.assertEqual("complete", res["coverage"])
        self.assertTrue(res["eligible"])
        self.assertEqual("complete_deliverable", res["action"])

    def test_complete_coverage_is_not_an_approval(self):
        """A quarta pergunta continua por responder, e o resultado di-lo."""
        self.install(*CHAIN, "rec-v05-render-complete")
        res = self.state()
        self.assertIn("não é aprovação", res["note"])
        self.assertIn("ponta-a-ponta", res["note"])


# ================= A2. o resto da classe: dois campos declarados que ninguém conciliava

class DeclaredFieldsMustAgree(Base):
    """O varrimento da classe a que pertencia o falso positivo de 2026-09-16.

    O registo declara vários campos que descrevem a mesma realidade por ângulos
    diferentes, e cada par que ninguém obrigasse a concordar era uma porta. Um a um, com o
    controlo coerente ao lado — sem ele, um teste que acusa tudo não prova nada."""

    def test_the_coherent_record_still_passes(self):
        """O controlo. Uma regra nova que reprovasse o caso legítimo não seria uma regra,
        seria uma avaria."""
        self.install(*CHAIN, "rec-v05-render-complete")
        res = self.state()
        self.assertEqual("complete", res["coverage"])
        self.assertTrue(res["eligible"])

    def test_the_consumed_template_must_be_in_the_freshness_base(self):
        """`basis.authorities` é o que a atualidade recalcula e compara. Um template fora
        dessa lista podia mudar sem que a revisão ficasse stale por essa via."""
        def drop_it(name, rec):
            if rec.get("stage") == "render":
                rec["basis"]["authorities"] = [
                    a for a in rec["basis"]["authorities"]
                    if not a["path"].endswith(".template.md")]
        self.install(*CHAIN, "rec-v05-render-complete", mutate=drop_it)
        res = self.state()
        self.assertIn("COV-SCHEMA", self.codes(res))
        self.assertFalse(res["eligible"])

    def test_an_unreadable_template_blocks_instead_of_warning(self):
        """Era um aviso, e o aviso era o buraco: sem ler o template, a identidade e a
        versão de autoridade ficavam ambas por verificar — e o registo passava por aí.
        O caminho de erro é o que menos pode ser permissivo."""
        def point_outside(name, rec):
            if rec.get("stage") == "render":
                rec["deliverable"]["template"] = (
                    "library/packs/outsystems/deliverable-templates/"
                    "implementation-spec.template.md")
        self.install(*CHAIN, "rec-v05-render-complete", mutate=point_outside)
        res = self.state()
        self.assertIn("COV-SCHEMA", self.codes(res))
        self.assertFalse(res["eligible"])

    def test_a_deliverable_that_was_not_produced_projected_nothing(self):
        """Declarar que o documento não se produz **e** dar obrigações por projectadas é
        uma contradição do próprio registo — e vê-se sem derivar aplicabilidade nenhuma."""
        for state in ("not_applicable", "blocked"):
            with self.subTest(state=state):
                def declare(name, rec, state=state):
                    if rec.get("stage") == "render":
                        rec["deliverable"]["applicability"] = {
                            "state": state, "reason": "razão declarada"}
                self.install(*CHAIN, "rec-v05-render-complete", mutate=declare)
                res = self.state()
                self.assertIn("COV-REVIEW-INCOMPLETE", self.codes(res))
                self.assertFalse(res["eligible"])

    def test_declaring_not_produced_without_claiming_coverage_is_accepted(self):
        """E a declaração honesta não é acusada: é a contradição que é o achado, não a
        aplicabilidade."""
        def declare_and_drop(name, rec):
            if rec.get("stage") != "render":
                return
            rec["deliverable"]["applicability"] = {"state": "blocked",
                                                   "reason": "sem versão aprovada"}
            for it in rec["coverage"]:
                it["assessment"]["status"] = "missing"
                it["required_action"] = "obter a aprovação do desenho"
                it["responsible_role"] = "dono do processo"
            rec["semantic_review"]["findings"] = [it["id"] for it in rec["coverage"]]
        self.install(*CHAIN, "rec-v05-render-complete", mutate=declare_and_drop)
        self.assertNotIn("COV-REVIEW-INCOMPLETE", self.codes(self.state()))

    def test_a_review_made_under_another_pack_is_stale(self):
        """O pacote decide contra que contratos as autoridades se resolvem. Declarado
        diferente do activo, a revisão fala de outro conjunto — e o snapshot não se
        corrige sozinho."""
        def other_pack(name, rec):
            if rec.get("stage") == "render":
                rec["basis"]["pack"] = "outsystems"
        self.install(*CHAIN, "rec-v05-render-complete", mutate=other_pack)
        res = self.state()
        self.assertIn("COV-STALE", self.codes(res))
        self.assertFalse(res["eligible"])

    def test_an_authority_that_does_not_exist_is_not_satisfied_by_omission(self):
        """Fechada a troca de template, restava a omissão: `blueprint_version_read: null`
        batia certo com «não há versão nenhuma» e passava limpo."""
        mutate, rel = self.as_spec(version_read=None)
        self.install(*CHAIN, "rec-v05-render-complete", mutate=mutate)
        res = self.state(rel)
        mism = [d for d in res["diagnostics"] if d["code"] == "COV-AUTHORITY-MISMATCH"]
        self.assertEqual(1, len(mism), [d["message"] for d in mism])
        self.assertIn("não a substitui", mism[0]["message"])
        self.assertFalse(res["eligible"])

    def test_the_same_pairs_are_named_in_the_contract(self):
        """O motor não impõe o que o contrato não escreve."""
        for phrase in ("`basis.authorities`", "`basis.pack`", "não se lê"):
            self.assertIn(phrase, CONTRACT, phrase)


# ============================================== B. referência não é projecção (T32, T33)

class ProjectionIsNotAReference(Base):

    def _point_at_the_comment(self):
        """`item-001` passa a citar o id que a `v01` só tem dentro de um comentário."""
        sha = hashlib.sha256((self.eng / RENDER_V01).read_bytes()).hexdigest()

        def mutate(name, rec):
            if rec.get("stage") != "render":
                return
            rec["target"].update({"file": RENDER_V01, "identity": "solution-blueprint_v01",
                                  "sha256": sha})
            for it in rec["coverage"]:
                for tg in it["targets"]:
                    tg["file"] = RENDER_V01
                if it["id"] == "item-001":
                    it["targets"] = [{"file": RENDER_V01, "selector": "A3/C-007",
                                      "kind": "section", "role": "projection"}]
        return mutate

    def test_the_comment_line_exists_in_the_fixture(self):
        """Sem o engodo, o teste seguinte não provava nada."""
        self.assertIn("<!-- C-007 -->", (self.eng / RENDER_V01).read_text(encoding="utf-8"))

    def test_an_id_in_a_comment_is_not_preservation(self):
        """T32 — o locator resolve (a linha existe), e mesmo assim não é âncora."""
        self.install(*CHAIN, "rec-v05-render-complete", mutate=self._point_at_the_comment())
        res = self.state(RENDER_V01)
        self.assertEqual("gaps", res["coverage"])
        bad = [d for d in res["diagnostics"] if d["item"] == "item-001"]
        self.assertIn("COV-INVALID-TARGET", [d["code"] for d in bad])
        self.assertIn("COV-MISSING-TARGET", [d["code"] for d in bad])
        self.assertTrue(any("comentário" in d["message"] for d in bad))

    def test_the_comment_rule_does_not_swallow_a_real_line(self):
        """Uma linha de tabela que cita o mesmo id continua a ser uma projecção válida."""
        res = C["resolve_target"](self.eng, {"file": RENDER_V01, "selector": "A3/lote-export"})
        self.assertTrue(res["ok"])
        self.assertFalse(res.get("comment_only"))

    def test_a_heading_is_not_a_comment(self):
        self.assertFalse(C["COMMENT_LINE"].match("# A3 — contexto e fronteiras"))
        self.assertTrue(C["COMMENT_LINE"].match("  <!-- C-007 -->  "))

    def test_a_lost_output_is_a_gap_and_the_engine_does_not_invent_it(self):
        """T33 — a saída exigida que o documento não carrega sai como lacuna, com dono."""
        self.install(*CHAIN, "rec-neg-render-id-in-comment")
        res = self.state(RENDER_V01)
        self.assertEqual("gaps", res["coverage"])
        self.assertIn("COV-INVALID-TARGET", self.codes(res))
        self.assertFalse(res["eligible"])

    def test_checking_a_gap_writes_nothing_upstream(self):
        """O render devolve a lacuna ao dono a montante: não reescreve SU nem desenho."""
        self.install(*CHAIN, "rec-neg-render-id-in-comment")
        before = manifest(self.eng)
        self.state(RENDER_V01)
        self.state(RENDER_V01)
        self.assertEqual(manifest(self.eng), before)


# ======================================= C. o que não pode ficar retido (T34, T35)

class NothingLegitimateIsHeld(Base):
    """T34/T35 — sem UI, headless, sem arquitectura autorizada, legado."""

    def test_without_an_architecture_authorization_nothing_is_a_gap(self):
        """T34 — a ausência é *não aplicável*, e o pré-render não a reporta como erro."""
        self.deauthorize()
        pre = self.precheck("solution-blueprint")
        self.assertEqual("no-authorization", pre["expected"]["state"])
        self.assertEqual(0, pre["blocking"],
                         "uma autoridade que ainda não existe não é lacuna: %r"
                         % pre["diagnostics"])

    def test_a_case_with_no_design_at_all_is_not_blocked_either(self):
        """Headless levado ao extremo: `_blueprint/` inteiro ausente."""
        shutil.rmtree(self.eng / "_blueprint")
        pre = self.precheck("claude-design-brief")
        self.assertEqual("no-authorization", pre["expected"]["state"])
        self.assertEqual(0, pre["blocking"])
        self.assertEqual("reconciliation", pre["upstream"]["stage"])

    def test_a_deliverable_that_reads_no_design_is_unaffected_by_its_absence(self):
        """O Discovery Report não fica retido por não haver cobertura de desenho."""
        shutil.rmtree(self.eng / "_blueprint")
        pre = self.precheck("discovery-report")
        self.assertEqual("no-blueprint-read", pre["expected"]["state"])
        self.assertEqual(0, pre["blocking"])

    def test_applicability_is_declared_with_a_reason_or_it_is_incomplete(self):
        """Ausência legítima é declarada, nunca silenciosa."""
        def drop_reason(name, rec):
            if rec.get("stage") == "render":
                rec["deliverable"]["applicability"] = {"state": "not_applicable"}
        self.install(*CHAIN, "rec-v05-render-complete", mutate=drop_reason)
        self.assertIn("COV-REVIEW-INCOMPLETE", self.codes(self.state()))

    def test_a_declared_applicability_with_a_reason_is_accepted(self):
        def declare(name, rec):
            if rec.get("stage") == "render":
                rec["deliverable"]["applicability"] = {
                    "state": "required", "reason": "há autorização para um âmbito"}
        self.install(*CHAIN, "rec-v05-render-complete", mutate=declare)
        res = self.state()
        self.assertEqual("complete", res["coverage"])

    def test_an_invented_applicability_state_is_refused(self):
        """Os quatro estados são os do `render-contract.md`; não há taxonomia paralela."""
        def invent(name, rec):
            if rec.get("stage") == "render":
                rec["deliverable"]["applicability"] = {"state": "partially-applicable",
                                                       "reason": "..."}
        self.install(*CHAIN, "rec-v05-render-complete", mutate=invent)
        self.assertIn("COV-SCHEMA", self.codes(self.state()))

    def test_legacy_approval_survives_and_coverage_reads_not_evaluated(self):
        """T35 — aprovação histórica preservada, cobertura por avaliar. As duas coisas."""
        self.append("decisions.md", APPROVAL)
        before = (self.eng / "decisions.md").read_bytes()
        res = self.state()
        self.assertEqual("not_evaluated", res["contract_validity"])
        self.assertEqual("not_evaluated", res["coverage"])
        self.assertFalse(res["eligible"])
        self.assertEqual(before, (self.eng / "decisions.md").read_bytes())

    def test_legacy_is_neither_a_pass_nor_a_retroactive_failure(self):
        self.append("decisions.md", APPROVAL)
        res = self.state()
        self.assertNotIn(res["coverage"], ("complete", "gaps"))
        self.assertIn("COV-NO-REVIEW", self.codes(res))
        # E a versão aprovada continua a resolver-se: a introdução do mecanismo não a apaga.
        self.assertEqual("v03", self.precheck("implementation-spec")["expected"]["version"])


# ============================================ D. registo ausente, ilegível ou futuro (T24)

class NeverGreenByAccident(Base):

    def test_no_record_for_the_stage_is_not_evaluated(self):
        res = self.state()
        self.assertEqual("not_evaluated", res["coverage"])
        self.assertIn("COV-NO-REVIEW", self.codes(res))

    def test_a_broken_record_never_reads_as_absent(self):
        """T24 — JSON partido em `_coverage/` bloqueia, e não passa por «ainda não há»."""
        self.install(*CHAIN, "rec-v05-render-complete")
        (self.eng / "_coverage" / "coverage_v06.json").write_text("{ partido",
                                                                  encoding="utf-8")
        res = self.state()
        self.assertEqual("invalid", res["contract_validity"])
        self.assertNotEqual("complete", res["coverage"])
        self.assertFalse(res["eligible"])

    def test_a_future_schema_is_unsupported_and_nothing_else_is_interpreted(self):
        """T24 — schema desconhecido não se interpreta por aproximação."""
        def bump(name, rec):
            if rec.get("stage") == "render":
                rec["schema_version"] = 99
        self.install(*CHAIN, "rec-v05-render-complete", mutate=bump)
        res = self.state()
        self.assertEqual("unsupported", res["contract_validity"])
        self.assertEqual("not_evaluated", res["coverage"])
        self.assertEqual("not_evaluated", res["semantic_review"])

    def test_a_newer_review_with_gaps_is_not_replaced_by_an_older_complete_one(self):
        """T23 — o cenário que este mecanismo não pode deixar acontecer."""
        self.install(*CHAIN, "rec-v05-render-complete")
        newer = json.loads((self.eng / "_coverage" / "coverage_v05.json")
                           .read_text(encoding="utf-8"))
        newer["version"] = "v06"
        newer["coverage"][0]["assessment"]["status"] = "missing"
        newer["coverage"][0]["required_action"] = "projectar a publicação no documento"
        newer["coverage"][0]["responsible_role"] = "arquitectura"
        newer["semantic_review"]["findings"] = ["item-001"]
        (self.eng / "_coverage" / "coverage_v06.json").write_text(
            json.dumps(newer, ensure_ascii=False, indent=2), encoding="utf-8")
        res = self.state()
        self.assertEqual("_coverage/coverage_v06.json", res["record"]["file"])
        self.assertEqual("gaps", res["coverage"])

    def test_the_template_changing_after_the_review_makes_it_stale(self):
        """T39 — o contrato de projecção mudou; a revisão que o leu deixou de valer.

        Um template que muda mexe nas DUAS declarações do mesmo digest: a autoridade do
        `basis` (que é o que a atualidade compara) e a do bloco `deliverable`."""
        def moved(name, rec):
            if rec.get("stage") != "render":
                return
            for a in rec["basis"]["authorities"]:
                if a["path"].endswith(".template.md"):
                    a["sha256"] = "0" * 64
            rec["deliverable"]["template_sha256"] = "0" * 64
        self.install(*CHAIN, "rec-v05-render-complete", mutate=moved)
        res = self.state()
        self.assertEqual("stale", res["freshness"])
        self.assertIn("COV-STALE", self.codes(res))
        self.assertFalse(res["eligible"])

    def test_a_record_whose_declared_template_digest_is_wrong_is_not_eligible(self):
        """A segunda declaração do mesmo digest também prende: um registo que diz ter
        lido um template que não é o do disco não se anuncia completo."""
        def break_only_the_block(name, rec):
            if rec.get("stage") == "render":
                rec["deliverable"]["template_sha256"] = "0" * 64
        self.install(*CHAIN, "rec-v05-render-complete", mutate=break_only_the_block)
        res = self.state()
        self.assertIn("COV-STALE", self.codes(res))
        self.assertFalse(res["eligible"])


# ============================================================= E. a linha de comandos

class Cli(Base):

    def test_the_precheck_runs_without_a_target(self):
        r = self.cli("check", "--engagement", str(self.eng), "--stage", "render",
                     "--deliverable", "solution-blueprint", "--json")
        self.assertEqual(0, r.returncode, r.stdout + r.stderr)
        data = json.loads(r.stdout)
        self.assertEqual("aisa.coverage.render_precheck", data["artefact"])
        self.assertEqual("v03", data["expected"]["version"])

    def test_the_render_stage_without_target_or_deliverable_is_a_usage_error(self):
        r = self.cli("check", "--engagement", str(self.eng), "--stage", "render")
        self.assertEqual(2, r.returncode)
        self.assertIn("--deliverable", r.stderr)

    def test_a_template_defect_blocks_the_precheck_and_names_the_template(self):
        bad = self.root / "broken.template.md"
        bad.write_text("---\ntemplate_id: x\n---\n", encoding="utf-8")
        r = self.cli("check", "--engagement", str(self.eng), "--stage", "render",
                     "--deliverable", "solution-blueprint", "--template", str(bad),
                     "--json")
        self.assertEqual(4, r.returncode, r.stdout + r.stderr)
        # Fora da fronteira do engagement e das autoridades da §5.3: recusado sem ler.
        self.assertIn("COV-DEAD-REF", [d["code"] for d in json.loads(r.stdout)["diagnostics"]])

    def test_the_precheck_writes_nothing(self):
        """T38 no caminho novo."""
        before = manifest(self.eng)
        self.cli("check", "--engagement", str(self.eng), "--stage", "render",
                 "--deliverable", "implementation-spec", "--json")
        self.assertEqual(manifest(self.eng), before)

    def test_editing_the_markdown_report_changes_no_authority(self):
        """T40 — o relatório é uma projecção, e a autoridade é o JSON."""
        self.install(*CHAIN, "rec-v05-render-complete")
        before = self.state()
        md = self.eng / "_coverage" / "coverage_v05.md"
        md.write_text("# tudo aprovado e completo\n", encoding="utf-8")
        after = self.state()
        self.assertEqual(before["coverage"], after["coverage"])
        self.assertEqual(before["eligible"], after["eligible"])


# ================================================================ F. o que está escrito

class WhatTheContractsSay(unittest.TestCase):
    """Um contrato que descreve uma ligação diferente da real é o defeito a apanhar."""

    def test_the_coverage_contract_declares_the_render_stage_wired(self):
        head = CONTRACT[:CONTRACT.index("## 1. O que a cobertura")]
        self.assertIn("activo nas três etapas", head)
        self.assertIn("verifica, não redefine", head)

    def test_the_three_version_tokens_are_normative_and_closed(self):
        self.assertIn("`v<latest authorized>`", CONTRACT)
        self.assertIn("`v<approved>`", CONTRACT)
        self.assertIn("não se lê como `none`", CONTRACT)
        for token in C["VERSION_TOKENS"]:
            if token:
                self.assertIn(token, CONTRACT, token + " não está no contrato")

    def test_the_contract_forbids_a_requirement_to_deliverable_table(self):
        self.assertIn("tabela kernel «requisito → deliverable»", CONTRACT)

    def test_the_contract_binds_the_record_id_to_the_template_identity(self):
        """A norma da correcção de 2026-09-16. O motor não impõe o que o contrato não diz,
        e um contrato que a perca deixa o falso positivo voltar em silêncio."""
        self.assertIn("`template_id`", CONTRACT)
        self.assertIn("`deliverable.id` é decorativo", CONTRACT)
        self.assertIn("especificação aceite sem aprovação", CONTRACT)
        self.assertIn("template_id", RENDER_CONTRACT)

    def test_the_render_contract_separates_skip_from_gap(self):
        self.assertIn("Not reaching an authority is not a gap", RENDER_CONTRACT)
        self.assertIn("never an entry in `render-gaps.md`", RENDER_CONTRACT)

    def test_the_render_skill_runs_both_checks_and_neither_speaks_for_the_other(self):
        self.assertIn("--stage render --deliverable", RENDER_SKILL)
        self.assertIn("--stage render --target", RENDER_SKILL)
        self.assertIn("Structure, coverage, approval and end-to-end are four questions",
                      RENDER_SKILL)

    def test_the_render_skill_forbids_repairing_upstream_to_close_a_finding(self):
        flat = " ".join(RENDER_SKILL.split())
        self.assertIn("Never reopen the source workbook", flat)
        self.assertIn("do not reinstate it by declaring the item `covered` anyway", flat)
        self.assertIn("Coverage verifies; it never redefines", RENDER_SKILL)

    def test_synthesis_carries_pending_findings_and_is_not_an_authority(self):
        self.assertIn("Open coverage findings are carried, not closed", SYNTH_SKILL)
        self.assertIn("Coverage is neither authority nor eraser", SYNTH_SKILL)


if __name__ == "__main__":
    unittest.main(verbosity=2)
