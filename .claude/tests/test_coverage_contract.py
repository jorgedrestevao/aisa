"""Fase 3 da reconciliação/cobertura — validação de registos e veredictos calculados.

A pergunta deste módulo: **um registo incompleto pode produzir um falso verde?** Cada
classe é uma maneira concreta de tentar obter «coberto» sem ter coberto nada — e a
asserção é sempre a mesma: o motor recusa, com código, e diz o que fecha o achado.

O que vive aqui:

  F06        o caso de origem, nos dois sentidos: a versão que perde o requisito dá
             lacuna; a versão que o concretiza dá cobertura completa **e a aprovação
             continua ausente**, porque são perguntas diferentes.
  Schema     campo obrigatório, tipo errado, versão do schema desconhecida.
  Destinos   destino decorativo, nó inexistente, ligação a pergunta ou a prova futura.
  Exclusões  material sem autoridade, materialidade por declarar, mecânica com fundamento.
  Herança    a obrigação que desaparece entre etapas, a fusão e a exclusão herdada.
  Selecção   duas revisões do mesmo par (etapa, alvo): vale a mais recente, sempre.
  Relatório  a projecção Markdown é determinística e **não é autoridade**.

    python .claude/tests/test_coverage_contract.py
"""

import copy
import json
import runpy
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
C = runpy.run_path(str(ROOT / "library" / "kernel" / "tools" / "coverage.py"))
FIX = Path(__file__).resolve().parent / "fixtures" / "coverage"
ENG = FIX / "fx-coverage-f06"
RECORDS = FIX / "records"
PLACEHOLDER = "b31c2af5507500ef2272d791693f3335b4be63f86ff8a781a8436d1cc253fb81"

BP01 = "_blueprint/ux-blueprint_v01.yaml"
BP02 = "_blueprint/ux-blueprint_v02.yaml"
BP03 = "_blueprint/ux-blueprint_v03.yaml"
RD01 = "_render/fx-coverage-f06_solution-blueprint_v01.md"
RD02 = "_render/fx-coverage-f06_solution-blueprint_v02.md"

RECON = "rec-v01-reconciliation-complete"


def load(name: str) -> dict:
    return json.loads((RECORDS / (name + ".json")).read_text(encoding="utf-8"))


def hydrate(eng: Path, rec: dict) -> dict:
    """Troca os três placeholders derivados pelo que o motor calcula (fase 1, D9).

    Os digests de bytes das fixtures são reais; estes três dependiam de uma
    canonicalização que não existia quando foram escritos."""
    basis = rec.get("basis")
    if not isinstance(basis, dict):
        return rec
    inv = C["build_inventory"](eng)
    synth = tuple(sorted(
        s for s in ((rec.get("deliverable") or {}).get("authority_sources") or [])
        if str(s).startswith("_synthesis/")))
    now = C["compute_basis"](eng, inv, rec["stage"], rec.get("target"),
                             authorities=basis.get("authorities", ()),
                             synthesis_authorities=synth)
    for field in ("inventory_sha256", "su_fingerprint", "decision_fingerprint"):
        if basis.get(field) == PLACEHOLDER:
            basis[field] = now[field]
    return rec


class Harness(unittest.TestCase):
    """Uma cópia do engagement por teste, com os registos pedidos em `_coverage/`."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.eng = Path(self.tmp.name) / "fx-coverage-f06"
        shutil.copytree(ENG, self.eng)
        (self.eng / "_coverage").mkdir()

    def install(self, *names, **edits):
        """Instala registos pelo nome da fixture; `edits` permite mutar o último."""
        last = None
        for name in names:
            rec = hydrate(self.eng, load(name))
            last = rec
            self.write(rec)
        if edits and last is not None:
            self.fail("usar `write(mutate(...))`: `edits` não é aplicado às fixtures")
        return last

    def write(self, rec: dict) -> Path:
        path = self.eng / "_coverage" / ("coverage_%s.json" % rec["version"])
        path.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def state(self, stage, target_rel=None):
        target = {"file": target_rel} if target_rel else None
        return C["coverage_state"](self.eng, stage, target)

    def codes(self, result):
        return [d["code"] for d in result["diagnostics"]]

    def assertCode(self, result, code, msg=""):
        self.assertIn(code, self.codes(result),
                      msg or "esperado %s; saíram %s" % (code, self.codes(result)))

    def assertNoCode(self, result, code):
        self.assertNotIn(code, self.codes(result),
                         "%s não devia disparar aqui" % code)


# ============================================================================== F06

class F06(unittest.TestCase):
    """O caso de origem, demonstrado nos dois sentidos sobre a fixture sintética.

    A propriedade central: a `v01` **passa** a verificação estrutural do runtime com zero
    bloqueios e mesmo assim perdeu um requisito que a Shared Understanding já carregava.
    Estrutura e cobertura são perguntas diferentes, e é por isso que este mecanismo
    existe."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.eng = Path(self.tmp.name) / "fx-coverage-f06"
        shutil.copytree(ENG, self.eng)
        (self.eng / "_coverage").mkdir()

    def install(self, *names):
        for name in names:
            rec = hydrate(self.eng, load(name))
            (self.eng / "_coverage" / ("coverage_%s.json" % rec["version"])).write_text(
                json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")

    def test_the_structural_check_says_valid_on_the_version_that_lost_the_output(self):
        st = C["structural_check"](self.eng, BP01)
        self.assertTrue(st["evaluated"])
        self.assertEqual(st["blocking"], 0,
                         "a v01 tem de continuar estruturalmente válida — é essa a "
                         "coexistência que o F06 é")

    def test_the_lost_requirement_is_a_gap_on_the_version_that_lost_it(self):
        self.install(RECON, "rec-v02-blueprint-missing")
        res = C["coverage_state"](self.eng, "blueprint", {"file": BP01})
        self.assertEqual(res["coverage"], "gaps")
        self.assertFalse(res["eligible"])
        gaps = {tuple(g["requirement_refs"]): g["status"] for g in res["gaps"]}
        self.assertEqual(gaps.get(("C-007",)), "missing",
                         "a saída que o desenho não concretiza tem de aparecer perdida")

    def test_a_partial_gap_still_blocks_even_when_the_f06_requirement_is_delivered(self):
        self.install(RECON, "rec-v02-blueprint-missing", "rec-v03-blueprint-partial")
        res = C["coverage_state"](self.eng, "blueprint", {"file": BP02})
        self.assertEqual(res["coverage"], "gaps")
        gaps = {tuple(g["requirement_refs"]): g["status"] for g in res["gaps"]}
        self.assertNotIn(("C-007",), gaps, "C-007 já está coberto na v02")
        self.assertEqual(gaps.get(("C-010",)), "partial")

    def test_the_complete_version_covers_everything_and_is_still_not_approved(self):
        self.install(RECON, "rec-v03-blueprint-partial", "rec-v04-blueprint-complete")
        res = C["coverage_state"](self.eng, "blueprint", {"file": BP03})
        self.assertEqual(res["coverage"], "complete")
        self.assertEqual(res["semantic_review"], "completed")
        self.assertTrue(res["eligible"])
        decisions = (self.eng / "decisions.md").read_text(encoding="utf-8")
        self.assertNotIn("aprovado", decisions.lower(),
                         "cobertura completa não pode ter produzido uma aprovação")
        self.assertTrue(any("aprovação ao negócio" in r for r in res["reasons"]),
                        "o resultado tem de dizer que falta o pedido ao negócio")

    def test_the_decorative_target_never_becomes_coverage(self):
        """`covered` cujo único destino é a entidade que cita o id: não é cobertura."""
        self.install(RECON, "rec-neg-decorative-projection")
        res = C["coverage_state"](self.eng, "blueprint", {"file": BP01})
        self.assertIn("COV-MISSING-TARGET", [d["code"] for d in res["diagnostics"]])
        self.assertEqual(res["coverage"], "gaps")

    def test_lying_about_the_role_lands_on_a_node_that_does_not_exist(self):
        """A segunda via mecânica: mentir no papel obriga a apontar para um nó real."""
        self.install(RECON, "rec-neg-decorative-invalid-target")
        res = C["coverage_state"](self.eng, "blueprint", {"file": BP01})
        self.assertIn("COV-INVALID-TARGET", [d["code"] for d in res["diagnostics"]])
        self.assertEqual(res["coverage"], "gaps")

    def test_coverage_and_approval_and_e2e_stay_three_separate_things(self):
        self.install(RECON, "rec-v03-blueprint-partial", "rec-v04-blueprint-complete")
        res = C["coverage_state"](self.eng, "blueprint", {"file": BP03})
        self.assertIn("aprovação", res["note"].lower())
        self.assertIn("ponta-a-ponta", res["note"].lower())


# =========================================================================== schema

class Schema(Harness):
    """§4.1 — o que torna um registo ilegível, e o que apenas o torna pobre."""

    def test_a_future_schema_is_unsupported_and_nothing_else_is_interpreted(self):
        self.install(RECON, "rec-neg-schema-future")
        res = self.state("blueprint", BP03)
        self.assertEqual(res["contract_validity"], "unsupported")
        for key in ("freshness", "source_review", "semantic_review", "coverage"):
            self.assertEqual(res[key], "not_evaluated",
                             "`unsupported` é «não sei ler isto», não «li e falta-lhe "
                             "coisa» — %s não podia ter veredicto" % key)
        self.assertFalse(res["eligible"])

    def test_an_invalid_record_is_invalid_and_never_covered(self):
        self.install(RECON, "rec-neg-schema-invalid")
        res = self.state("blueprint", BP01)
        self.assertEqual(res["contract_validity"], "invalid")
        self.assertEqual(res["coverage"], "not_evaluated")
        self.assertFalse(res["eligible"])

    def test_a_missing_required_field_is_a_contract_error(self):
        rec = hydrate(self.eng, load(RECON))
        del rec["semantic_review"]
        out = C["validate_record"](rec, C["build_inventory"](self.eng), self.eng)
        self.assertEqual(out["contract_validity"], "invalid")

    def test_an_unknown_root_field_is_a_warning_and_is_not_read(self):
        rec = hydrate(self.eng, load(RECON))
        rec["verdict"] = "everything is fine"
        out = C["validate_record"](rec, C["build_inventory"](self.eng), self.eng)
        self.assertEqual(out["contract_validity"], "valid")
        warn = [d for d in out["diagnostics"]
                if d["code"] == "COV-SCHEMA" and d["severity"] == "warn"]
        self.assertTrue(warn, "campo desconhecido tem de ser visível")

    def test_a_persisted_verdict_is_not_a_verdict(self):
        """Contrato §3: os veredictos recalculam-se; o que o ficheiro diz não conta."""
        rec = hydrate(self.eng, load("rec-neg-schema-invalid"))
        rec["contract_validity"] = "valid"
        rec["coverage"] = "complete"
        self.write(rec)
        self.write(hydrate(self.eng, load(RECON)))
        res = self.state("blueprint", BP01)
        self.assertEqual(res["contract_validity"], "invalid")
        self.assertNotEqual(res["coverage"], "complete")

    def test_the_version_has_to_match_the_file_name(self):
        rec = hydrate(self.eng, load(RECON))
        out = C["validate_record"](rec, C["build_inventory"](self.eng), self.eng,
                                   filename="coverage_v09.json")
        self.assertEqual(out["contract_validity"], "invalid")

    def test_reconciliation_with_a_target_is_a_contract_error(self):
        rec = hydrate(self.eng, load(RECON))
        rec["target"] = {"file": BP01, "kind": "blueprint", "identity": "v01",
                         "sha256": "0" * 64}
        out = C["validate_record"](rec, C["build_inventory"](self.eng), self.eng)
        self.assertEqual(out["contract_validity"], "invalid")

    def test_a_blueprint_record_without_based_on_is_a_contract_error(self):
        rec = hydrate(self.eng, load("rec-v02-blueprint-missing"))
        rec["based_on"] = []
        out = C["validate_record"](rec, C["build_inventory"](self.eng), self.eng)
        self.assertEqual(out["contract_validity"], "invalid")

    def test_based_on_that_names_a_record_that_does_not_exist_is_a_contract_error(self):
        self.write(hydrate(self.eng, load("rec-v02-blueprint-missing")))
        res = self.state("blueprint", BP01)
        self.assertEqual(res["contract_validity"], "invalid",
                         "`based_on` sem o registo que nomeia não é revisão pobre, é "
                         "ligação partida")


# ================================================================ revisão das fontes

class SourceReview(Harness):
    """§4.3 e §6.1 — o denominador é do inventário, e nenhuma unidade desaparece."""

    def test_an_unreviewed_unit_is_named(self):
        self.install("rec-neg-unreviewed-unit")
        res = self.state("reconciliation")
        self.assertEqual(res["source_review"], "incomplete")
        self.assertCode(res, "COV-UNREVIEWED")
        self.assertEqual(res["unreviewed_units"], 1)
        self.assertFalse(res["eligible"])

    def test_a_complete_reconciliation_is_complete_with_open_questions(self):
        self.install(RECON)
        res = self.state("reconciliation")
        self.assertEqual(res["source_review"], "complete")
        self.assertEqual(res["coverage"], "complete")
        self.assertTrue(res["eligible"])
        su = (self.eng / "shared-understanding.md").read_text(encoding="utf-8")
        self.assertIn("U-010", su, "a pergunta em aberto continua na SU")

    def test_a_source_without_an_extractor_is_unverifiable_never_not_applicable(self):
        self.install("rec-neg-capture-limit-as-covered")
        res = self.state("reconciliation")
        self.assertCode(res, "COV-CAPTURE-LIMIT")
        self.assertFalse(res["eligible"])

    def test_the_capture_limit_is_shown_even_when_everything_else_is_fine(self):
        self.install(RECON)
        res = self.state("reconciliation")
        self.assertTrue(res["limitations"],
                        "a fonte que não se consegue ler mostra-se sempre")

    def test_a_unit_key_that_is_not_in_the_inventory_is_a_dead_reference(self):
        rec = hydrate(self.eng, load(RECON))
        rec["source_review"][0]["unit_refs"] = ["answers.md#U-999"]
        out = C["validate_record"](rec, C["build_inventory"](self.eng), self.eng)
        self.assertIn("COV-DEAD-REF", [d["code"] for d in out["diagnostics"]])

    def test_an_entry_without_rationale_is_review_incomplete(self):
        rec = hydrate(self.eng, load(RECON))
        rec["source_review"][0]["rationale"] = "   "
        out = C["validate_record"](rec, C["build_inventory"](self.eng), self.eng)
        self.assertIn("COV-REVIEW-INCOMPLETE", [d["code"] for d in out["diagnostics"]])

    def test_the_inventory_is_not_defined_by_the_record(self):
        """§6.1 — omitir ao mesmo tempo o requisito e a linha de revisão não dá verde."""
        rec = hydrate(self.eng, load(RECON))
        rec["source_review"] = rec["source_review"][:3]
        rec["coverage"] = rec["coverage"][:1]
        self.write(rec)
        res = self.state("reconciliation")
        self.assertEqual(res["source_review"], "incomplete")
        self.assertGreater(res["unreviewed_units"], 50)


# ====================================================================== obrigações

class Obligations(Harness):
    """§4.4 — o que `covered` exige, e o que uma exclusão exige."""

    def test_covered_with_unresolved_refs_is_review_incomplete(self):
        rec = hydrate(self.eng, load(RECON))
        item = [i for i in rec["coverage"] if i["assessment"]["status"] == "covered"][0]
        item["unresolved_refs"] = ["U-010"]
        out = C["validate_record"](rec, C["build_inventory"](self.eng), self.eng)
        self.assertIn("COV-REVIEW-INCOMPLETE", [d["code"] for d in out["diagnostics"]])

    def test_a_gap_without_owner_or_next_action_is_review_incomplete(self):
        rec = hydrate(self.eng, load("rec-v02-blueprint-missing"))
        gap = [i for i in rec["coverage"] if i["assessment"]["status"] == "missing"][0]
        gap["responsible_role"] = ""
        out = C["validate_record"](rec, C["build_inventory"](self.eng), self.eng)
        self.assertIn("COV-REVIEW-INCOMPLETE", [d["code"] for d in out["diagnostics"]])

    def test_a_requirement_that_does_not_exist_is_a_dead_reference(self):
        self.install(RECON, "rec-neg-dead-ref")
        res = self.state("blueprint", BP01)
        self.assertCode(res, "COV-DEAD-REF")
        self.assertCode(res, "COV-INVALID-TARGET")
        self.assertEqual(res["coverage"], "gaps")

    def test_a_material_exclusion_without_scope_authority_is_refused(self):
        self.install(RECON, "rec-neg-exclusion-no-decision")
        res = self.state("blueprint", BP01)
        self.assertCode(res, "COV-EXCLUSION-NO-DECISION")
        self.assertEqual(res["coverage"], "gaps")

    def test_an_exclusion_with_undeclared_materiality_is_review_incomplete(self):
        self.install(RECON, "rec-neg-exclusion-undetermined")
        res = self.state("blueprint", BP01)
        self.assertCode(res, "COV-REVIEW-INCOMPLETE")
        self.assertNoCode(res, "COV-EXCLUSION-NO-DECISION")

    def test_a_mechanical_exclusion_with_grounds_is_accepted(self):
        self.install(RECON, "rec-v03-blueprint-partial", "rec-pos-exclusion-mechanical")
        res = self.state("blueprint", BP03)
        self.assertEqual(res["coverage"], "complete",
                         "uma coluna mecânica retirada com fundamento não é lacuna")
        self.assertTrue(res["eligible"])

    def test_the_waiver_needs_every_linked_unit_to_be_not_material(self):
        """§4.4.1: a dispensa lê-se pela positiva, e uma unidade material chega para a
        anular."""
        rec = hydrate(self.eng, load("rec-pos-exclusion-mechanical"))
        for sr in rec["source_review"]:
            if sr["materiality"] == "not-material":
                sr["materiality"] = "material"
        item = [i for i in rec["coverage"] if i["assessment"]["status"] == "excluded"][0]
        item["scope_basis_refs"] = []
        out = C["validate_record"](rec, C["build_inventory"](self.eng), self.eng)
        self.assertIn("COV-EXCLUSION-NO-DECISION", [d["code"] for d in out["diagnostics"]])

    def test_a_scope_authority_that_does_not_resolve_is_a_dead_reference(self):
        rec = hydrate(self.eng, load("rec-pos-exclusion-mechanical"))
        item = [i for i in rec["coverage"] if i["assessment"]["status"] == "excluded"][0]
        item["scope_basis_refs"] = ["C-999"]
        out = C["validate_record"](rec, C["build_inventory"](self.eng), self.eng)
        self.assertIn("COV-DEAD-REF", [d["code"] for d in out["diagnostics"]])

    def test_a_covered_item_sourced_from_an_unreadable_source_is_refused(self):
        rec = hydrate(self.eng, load(RECON))
        item = [i for i in rec["coverage"] if i["assessment"]["status"] == "covered"][0]
        item["source_unit_refs"] = ["inputs/fluxo-de-libertacao.pptx"]
        out = C["validate_record"](rec, C["build_inventory"](self.eng), self.eng)
        self.assertIn("COV-CAPTURE-LIMIT", [d["code"] for d in out["diagnostics"]])


# ================================================================ herança de etapas

class Inheritance(Harness):
    """§4.4.4 — nenhuma obrigação desaparece entre a reconciliação e o desenho."""

    def test_a_dropped_obligation_is_caught_and_the_record_stays_readable(self):
        self.install(RECON, "rec-neg-obligation-dropped")
        res = self.state("blueprint", BP01)
        self.assertCode(res, "COV-UNREVIEWED")
        self.assertEqual(res["contract_validity"], "valid",
                         "um requisito perdido é revisão incompleta, não erro de "
                         "ficheiro — confundi-los esconderia o achado")
        self.assertEqual(res["source_review"], "incomplete")
        named = [d for d in res["diagnostics"] if d["code"] == "COV-UNREVIEWED"]
        self.assertTrue(any("C-008" in d["locator"] for d in named),
                        "o diagnóstico tem de nomear a obrigação perdida")

    def test_a_merge_counts_as_treatment(self):
        rec = hydrate(self.eng, load("rec-v04-blueprint-complete"))
        first, second = rec["coverage"][0], rec["coverage"][1]
        first["requirement_refs"] = sorted(set(first["requirement_refs"])
                                           | set(second["requirement_refs"]))
        first["targets"] = first["targets"] + second["targets"]
        rec["coverage"].remove(second)
        self.install(RECON, "rec-v03-blueprint-partial")
        self.write(rec)
        res = self.state("blueprint", BP03)
        self.assertNoCode(res, "COV-UNREVIEWED")

    def test_an_inherited_exclusion_that_loses_its_authority_is_caught(self):
        self.install(RECON, "rec-v03-blueprint-partial")
        rec = hydrate(self.eng, load("rec-v04-blueprint-complete"))
        item = [i for i in rec["coverage"] if i["assessment"]["status"] == "excluded"][0]
        item["scope_basis_refs"] = []
        for sr in rec["source_review"]:
            if sr["materiality"] == "material":
                continue
            sr["materiality"] = "not-material"
        self.write(rec)
        res = self.state("blueprint", BP03)
        self.assertCode(res, "COV-EXCLUSION-NO-DECISION")

    def test_there_is_no_legitimate_subtraction_in_the_blueprint_stage(self):
        rec = hydrate(self.eng, load("rec-v04-blueprint-complete"))
        rec["deliverable"] = {"not_selected": [{"requirement_refs": ["C-008"],
                                                "reason": "não cabe"}]}
        out = C["validate_record"](rec, C["build_inventory"](self.eng), self.eng)
        self.assertEqual(out["contract_validity"], "invalid")

    def test_render_may_subtract_only_by_declaring_it(self):
        self.install(RECON, "rec-v03-blueprint-partial", "rec-v04-blueprint-complete",
                     "rec-v05-render-complete")
        res = self.state("render", RD02)
        self.assertEqual(res["coverage"], "complete")
        self.assertNoCode(res, "COV-UNREVIEWED")

    def test_render_that_subtracts_without_declaring_it_is_caught(self):
        self.install(RECON, "rec-v03-blueprint-partial", "rec-v04-blueprint-complete")
        rec = hydrate(self.eng, load("rec-v05-render-complete"))
        rec["deliverable"]["not_selected"] = []
        self.write(rec)
        res = self.state("render", RD02)
        self.assertCode(res, "COV-UNREVIEWED")

    def test_not_selected_without_a_reason_is_review_incomplete(self):
        self.install(RECON, "rec-v03-blueprint-partial", "rec-v04-blueprint-complete")
        rec = hydrate(self.eng, load("rec-v05-render-complete"))
        rec["deliverable"]["not_selected"][0]["reason"] = ""
        self.write(rec)
        res = self.state("render", RD02)
        self.assertCode(res, "COV-REVIEW-INCOMPLETE")


class TargetsBelongToTheReviewedVersion(Harness):
    """P1d — o destino que prova a cobertura tem de estar na versão revista.

    O falso verde: alvo e digest correctos da `v01`, e **todos** os
    `coverage[].targets` a apontar para a `v03`. Os locators resolvem (a `v03` existe e
    tem os nós), o alvo confere (é mesmo a `v01`), e o que está a ser dado por coberto
    não está na versão que se diz estar a rever."""

    def _record_reviewing(self, target_rel, identity):
        rec = hydrate(self.eng, load("rec-v04-blueprint-complete"))
        rec["target"] = {"file": target_rel, "kind": "blueprint", "identity": identity,
                         "sha256": C["sha256_file"](self.eng / target_rel)}
        return rec

    def test_targets_in_another_version_never_prove_coverage(self):
        self.install(RECON, "rec-v03-blueprint-partial")
        self.write(self._record_reviewing(BP01, "v01"))   # destinos ficam na v03
        res = self.state("blueprint", BP01)
        self.assertNotEqual(res["coverage"], "complete")
        self.assertFalse(res["eligible"])
        self.assertCode(res, "COV-AUTHORITY-MISMATCH")
        self.assertCode(res, "COV-MISSING-TARGET")

    def test_the_diagnostic_names_both_files(self):
        self.install(RECON, "rec-v03-blueprint-partial")
        self.write(self._record_reviewing(BP01, "v01"))
        res = self.state("blueprint", BP01)
        msg = " ".join(d["message"] for d in res["diagnostics"]
                       if d["code"] == "COV-AUTHORITY-MISMATCH")
        self.assertIn("ux-blueprint_v03.yaml", msg)
        self.assertIn("ux-blueprint_v01.yaml", msg)

    def test_targets_in_the_reviewed_version_still_prove_it(self):
        """A fronteira: a regra não pode recusar o caso normal."""
        self.install(RECON, "rec-v03-blueprint-partial", "rec-v04-blueprint-complete")
        res = self.state("blueprint", BP03)
        self.assertEqual(res["coverage"], "complete")
        self.assertNoCode(res, "COV-AUTHORITY-MISMATCH")

    def test_a_non_anchor_target_may_live_elsewhere(self):
        """Um destino que **não** é âncora — uma linha da SU citada num registo de
        desenho — não é obrigado a viver no ficheiro revisto."""
        self.install(RECON, "rec-v03-blueprint-partial")
        rec = hydrate(self.eng, load("rec-v04-blueprint-complete"))
        rec["coverage"][0]["targets"].append(
            {"file": "shared-understanding.md", "selector": "C-007",
             "kind": "su_row", "role": "su_row"})
        self.write(rec)
        res = self.state("blueprint", BP03)
        self.assertEqual(res["coverage"], "complete")
        self.assertNoCode(res, "COV-AUTHORITY-MISMATCH")


class TheChainIsValidated(Harness):
    """P2d — uma revisão não vale mais do que aquela em que diz assentar."""

    def test_an_incomplete_reconciliation_cannot_carry_a_complete_blueprint(self):
        """O falso verde: reconciliação pobre, zero obrigações, e a herança passava por
        vacuidade — não havia obrigações nenhumas a perder."""
        poor = hydrate(self.eng, load(RECON))
        poor["source_review"] = poor["source_review"][:1]
        poor["coverage"] = []
        poor["semantic_review"]["findings"] = []
        self.write(poor)
        empty = hydrate(self.eng, load("rec-v02-blueprint-missing"))
        empty["coverage"] = []
        empty["semantic_review"]["findings"] = []
        self.write(empty)
        res = self.state("blueprint", BP01)
        self.assertNotEqual(res["coverage"], "complete")
        self.assertFalse(res["eligible"])
        self.assertCode(res, "COV-UNREVIEWED")
        self.assertTrue(res["upstream"], "a saúde de montante tem de ser reportada")
        self.assertEqual(res["upstream"][0]["source_review"], "incomplete")

    def test_a_stale_upstream_blocks_the_downstream(self):
        self.install(RECON, "rec-v02-blueprint-missing")
        before = self.state("blueprint", BP01)
        self.assertEqual(before["upstream"][0]["freshness"], "current")
        (self.eng / "inputs" / "nova.txt").write_text("x\n", encoding="utf-8")
        res = self.state("blueprint", BP01)
        self.assertFalse(res["eligible"])
        self.assertNotEqual(res["upstream"][0]["freshness"], "current")

    def test_a_record_cannot_be_based_on_itself(self):
        self.install(RECON)
        selfref = hydrate(self.eng, load("rec-v02-blueprint-missing"))
        selfref["based_on"] = ["coverage_v02.json"]
        self.write(selfref)
        res = self.state("blueprint", BP01)
        self.assertEqual(res["contract_validity"], "invalid")
        self.assertFalse(res["eligible"])

    def test_a_cycle_in_the_chain_is_a_contract_error(self):
        self.install(RECON)
        a = hydrate(self.eng, load("rec-v02-blueprint-missing"))
        a["based_on"] = ["coverage_v03.json"]      # cita uma versão POSTERIOR
        self.write(a)
        b = hydrate(self.eng, load("rec-v03-blueprint-partial"))
        b["based_on"] = ["coverage_v02.json"]
        self.write(b)
        res = self.state("blueprint", BP01)
        self.assertEqual(res["contract_validity"], "invalid")
        msgs = " ".join(d["message"] for d in res["diagnostics"])
        self.assertIn("versões anteriores", msgs)

    def test_a_blueprint_chain_that_never_touched_reconciliation_is_refused(self):
        """§4.6 — não basta citar alguma coisa: tem de ser da etapa que o contrato pede."""
        self.install(RECON, "rec-v02-blueprint-missing")
        bad = hydrate(self.eng, load("rec-v03-blueprint-partial"))
        bad["based_on"] = ["coverage_v02.json"]    # só desenho, nenhuma reconciliação
        self.write(bad)
        res = self.state("blueprint", BP02)
        self.assertEqual(res["contract_validity"], "invalid")
        msgs = " ".join(d["message"] for d in res["diagnostics"])
        self.assertIn("reconciliation", msgs)

    def _upstream_that_cannot_be_evaluated(self):
        """Uma reconciliação com `target` — que a etapa proíbe — faz `compute_basis`
        levantar `CoverageError` quando alguém a tenta avaliar."""
        up = hydrate(self.eng, load(RECON))
        up["target"] = {"file": BP01, "kind": "blueprint", "identity": "v01",
                        "sha256": "0" * 64}
        self.write(up)
        down = hydrate(self.eng, load("rec-v03-blueprint-partial"))
        down["based_on"] = ["coverage_v01.json"]
        for item in down["coverage"]:
            item["assessment"]["status"] = "covered"
            item.pop("required_action", None)
            item.pop("responsible_role", None)
            item["targets"] = [dict(t, file=BP02) for t in item.get("targets", [])
                               if t.get("role") == "implementation"] or [
                {"file": BP02, "selector": "architecture/compositions[component=resumo-email]",
                 "kind": "composition", "role": "implementation"}]
        down["semantic_review"]["findings"] = []
        self.write(down)

    def test_a_failure_to_evaluate_upstream_is_blocking_and_named(self):
        """P2e — o erro engolido. `upstream_health` apanhava o `CoverageError` da revisão
        de montante e seguia com `continue`: a lista de montante saía **vazia**, e vazia
        lê-se como «não havia nada a verificar». O desenho dava `complete`.

        Contrato §8: falha de avaliação é «não avaliado», nunca sucesso silencioso."""
        self._upstream_that_cannot_be_evaluated()
        res = self.state("blueprint", BP02)
        self.assertNotEqual(res["coverage"], "complete")
        self.assertFalse(res["eligible"])
        self.assertTrue(res["upstream"], "a revisão que falhou tem de aparecer")
        up = res["upstream"][0]
        self.assertEqual(up["file"], "coverage_v01.json",
                         "a identificação de quem falhou tem de sobreviver")
        self.assertTrue(up["error"])
        self.assertEqual(up["contract_validity"], "invalid")
        blocking = [d for d in res["diagnostics"]
                    if d["file"] == "coverage_v01.json" and d["severity"] == "error"]
        self.assertTrue(blocking, "a falha tem de sair como diagnóstico impeditivo")
        self.assertIn(blocking[0]["code"], ("COV-SCHEMA", "COV-UNEXPECTED"))

    def test_an_unexpected_failure_upstream_is_also_recorded(self):
        """A mesma porta para o erro que ninguém previu: `COV-UNEXPECTED`, nunca
        silêncio."""
        self.install(RECON, "rec-v02-blueprint-missing")
        G = C["coverage_state"].__globals__
        original = G["upstream_health"].__globals__["coverage_state"]
        calls = {"n": 0}

        def exploding(*a, **k):
            calls["n"] += 1
            if k.get("_depth", 0) > 0:
                raise RuntimeError("leitor rebentou a meio")
            return original(*a, **k)

        G["coverage_state"] = exploding
        try:
            res = original(self.eng, "blueprint", {"file": BP01})
        finally:
            G["coverage_state"] = original
        self.assertFalse(res["eligible"])
        self.assertEqual(res["upstream"][0]["code"], "COV-UNEXPECTED")
        self.assertIn("leitor rebentou", res["upstream"][0]["error"])
        self.assertIn("COV-UNEXPECTED", [d["code"] for d in res["diagnostics"]])

    def test_a_healthy_chain_still_passes(self):
        self.install(RECON, "rec-v03-blueprint-partial", "rec-v04-blueprint-complete")
        res = self.state("blueprint", BP03)
        self.assertEqual(res["coverage"], "complete")
        self.assertTrue(res["eligible"])
        self.assertTrue(all(u["source_review"] == "complete" for u in res["upstream"]))

    def test_a_wrongly_typed_target_argument_is_a_use_error_not_a_crash(self):
        with self.assertRaises(C["CoverageError"]) as ctx:
            C["coverage_state"](self.eng, "blueprint", BP01)   # string em vez de mapa
        self.assertEqual(ctx.exception.exit_code, 2)


class ObligationsDoNotVanish(Harness):
    """P1e — esvaziar `coverage[]` mantendo as fontes revistas dava `complete`.

    O motor verificava que as fontes tinham sido lidas e nunca perguntava se alguma
    obrigação tinha sido tratada. Três regras pela forma, nenhuma por semântica:
    ligações mortas são referências mortas; zero obrigações com material lido é revisão
    por acabar; e obrigações não desaparecem entre revisões sucessivas do mesmo par."""

    def _hollow(self, rec):
        rec["coverage"] = []
        rec["semantic_review"]["findings"] = []
        return rec

    def test_an_emptied_reconciliation_is_not_complete(self):
        self.write(self._hollow(hydrate(self.eng, load(RECON))))
        res = self.state("reconciliation")
        self.assertNotEqual(res["coverage"], "complete")
        self.assertFalse(res["eligible"])
        self.assertCode(res, "COV-REVIEW-INCOMPLETE")

    def test_an_emptied_blueprint_over_an_emptied_reconciliation_is_not_complete(self):
        self.write(self._hollow(hydrate(self.eng, load(RECON))))
        self.write(self._hollow(hydrate(self.eng, load("rec-v02-blueprint-missing"))))
        res = self.state("blueprint", BP01)
        self.assertNotEqual(res["coverage"], "complete")
        self.assertFalse(res["eligible"])

    def test_zero_obligations_is_coherent_only_when_nothing_is_material(self):
        """A fronteira da regra: um denominador em que nada é material pode, de facto,
        não ter nada a preservar."""
        rec = self._hollow(hydrate(self.eng, load(RECON)))
        for sr in rec["source_review"]:
            if sr["assessment"] == "reviewed":
                sr["materiality"] = "not-material"
        out = C["validate_record"](rec, C["build_inventory"](self.eng), self.eng)
        msgs = [d["message"] for d in out["diagnostics"]
                if d["code"] == "COV-REVIEW-INCOMPLETE"]
        self.assertFalse(any("nenhuma obrigação tratada" in m for m in msgs))

    def test_a_partial_hollowing_between_versions_is_caught(self):
        """O ataque realista, que o reporte não testou: a v02 larga cinco das seis."""
        self.install(RECON)
        v02 = hydrate(self.eng, load(RECON))
        v02["version"] = "v02"
        v02["coverage"] = v02["coverage"][:1]
        v02["semantic_review"]["findings"] = []
        self.write(v02)
        res = self.state("reconciliation")
        self.assertEqual(res["record"]["version"], "v02")
        self.assertEqual(res["previous"], ["_coverage/coverage_v01.json"])
        self.assertNotEqual(res["coverage"], "complete")
        self.assertFalse(res["eligible"])
        lost = [d for d in res["diagnostics"] if d["code"] == "COV-UNREVIEWED"]
        self.assertEqual(len(lost), 5, [d["locator"] for d in lost])

    def _keep_one(self, version):
        rec = hydrate(self.eng, load(RECON))
        rec["version"] = version
        rec["coverage"] = rec["coverage"][:1]
        rec["semantic_review"]["findings"] = []
        return rec

    def test_repeating_an_incomplete_review_does_not_launder_the_gaps(self):
        """P1f — o defeito: a comparação era só com a revisão imediatamente anterior.

        v01 tratava seis; v02 tratava uma e saía com lacunas; v03 repetia a v02 e saía
        `complete`, porque «a anterior» já só tinha uma. As cinco obrigações deixavam de
        ser exigidas sem disposição nenhuma. O conjunto exigido é a UNIÃO de todas as
        versões anteriores do par."""
        self.install(RECON)
        self.write(self._keep_one("v02"))
        self.write(self._keep_one("v03"))
        res = self.state("reconciliation")
        self.assertEqual(res["record"]["version"], "v03")
        self.assertEqual(res["previous"], ["_coverage/coverage_v01.json",
                                           "_coverage/coverage_v02.json"])
        self.assertNotEqual(res["coverage"], "complete")
        self.assertFalse(res["eligible"])
        lost = [d for d in res["diagnostics"] if d["code"] == "COV-UNREVIEWED"]
        self.assertEqual(len(lost), 5, [d["locator"] for d in lost])
        self.assertTrue(all(d["file"] == "_coverage/coverage_v01.json" for d in lost),
                        "cada obrigação perdida nomeia a versão que a tratava")

    def test_laundering_across_many_repetitions_is_still_caught(self):
        self.install(RECON)
        for v in ("v02", "v03", "v04", "v05"):
            self.write(self._keep_one(v))
        res = self.state("reconciliation")
        self.assertEqual(len([d for d in res["diagnostics"]
                              if d["code"] == "COV-UNREVIEWED"]), 5)
        self.assertFalse(res["eligible"])

    def test_a_disposition_given_once_must_be_carried_forward(self):
        """A saída legítima, e o que ela exige a seguir: a v03 retira com autoridade e
        passa; a v04 que volta a largar a obrigação é apanhada — a exclusão herdada
        reaparece (§4.4.4)."""
        self.install(RECON)
        v03 = hydrate(self.eng, load(RECON))
        v03["version"] = "v03"
        for item in v03["coverage"][1:]:
            item["disposition"] = "retire"
            item["assessment"]["status"] = "excluded"
            item["scope_basis_refs"] = ["D-002"]
            item["required_action"] = "—"
            item["responsible_role"] = "arquitetura"
        v03["semantic_review"]["findings"] = [i["id"] for i in v03["coverage"][1:]]
        self.write(v03)
        ok = self.state("reconciliation")
        self.assertNoCode(ok, "COV-UNREVIEWED")
        self.write(self._keep_one("v04"))
        res = self.state("reconciliation")
        self.assertEqual(len([d for d in res["diagnostics"]
                              if d["code"] == "COV-UNREVIEWED"]), 5,
                         "uma disposição dada uma vez não dispensa as versões seguintes")

    def test_a_retired_obligation_reappears_with_a_disposition_and_passes(self):
        """A saída legítima: a obrigação não desaparece, recebe uma disposição."""
        self.install(RECON)
        v02 = hydrate(self.eng, load(RECON))
        v02["version"] = "v02"
        item = v02["coverage"][1]
        item["disposition"] = "retire"
        item["assessment"]["status"] = "excluded"
        item["scope_basis_refs"] = ["D-002"]
        item["required_action"] = "—"
        item["responsible_role"] = "arquitetura"
        v02["semantic_review"]["findings"] = [item["id"]]
        self.write(v02)
        res = self.state("reconciliation")
        self.assertNoCode(res, "COV-UNREVIEWED")

    def test_a_merge_across_versions_counts_as_treatment(self):
        self.install(RECON)
        v02 = hydrate(self.eng, load(RECON))
        v02["version"] = "v02"
        a, b = v02["coverage"][0], v02["coverage"][1]
        a["requirement_refs"] = sorted(set(a["requirement_refs"]) | set(b["requirement_refs"]))
        a["source_unit_refs"] = a["source_unit_refs"] + b["source_unit_refs"]
        v02["coverage"].remove(b)
        self.write(v02)
        res = self.state("reconciliation")
        self.assertNoCode(res, "COV-UNREVIEWED")

    def test_dangling_links_are_dead_references(self):
        rec = hydrate(self.eng, load(RECON))
        rec["source_review"][0]["links"] = {"su_refs": ["C-999"],
                                            "coverage_items": ["item-999"],
                                            "obligations": ["X-1"]}
        out = C["validate_record"](rec, C["build_inventory"](self.eng), self.eng)
        dead = [d for d in out["diagnostics"] if d["code"] == "COV-DEAD-REF"]
        self.assertEqual(len(dead), 3, [d["message"] for d in dead])

    def test_links_that_resolve_are_accepted(self):
        rec = hydrate(self.eng, load(RECON))
        rec["source_review"][0]["links"] = {"su_refs": ["C-007"],
                                            "coverage_items": ["item-001"],
                                            "obligations": ["C-007"]}
        out = C["validate_record"](rec, C["build_inventory"](self.eng), self.eng)
        self.assertNotIn("COV-DEAD-REF", [d["code"] for d in out["diagnostics"]])

    def test_a_reconciliation_with_a_blocking_finding_is_not_eligible(self):
        """R8 — a elegibilidade da reconciliação só olhava para as lacunas encaminhadas."""
        rec = hydrate(self.eng, load(RECON))
        rec["coverage"][0]["requirement_refs"] = ["C-999"]
        self.write(rec)
        res = self.state("reconciliation")
        self.assertCode(res, "COV-DEAD-REF")
        self.assertFalse(res["eligible"])
        self.assertTrue(any("impeditivo" in r for r in res["reasons"]))


# ============================================================= revisão semântica §4.7

class SemanticReview(Harness):
    """§4.7 e §9 — as duas passagens são declaradas, e referências válidas não as
    substituem."""

    def test_pending_semantics_do_not_complete_the_review(self):
        self.install(RECON, "rec-v03-blueprint-partial", "rec-neg-semantic-pending")
        res = self.state("blueprint", BP03)
        self.assertEqual(res["semantic_review"], "pending")
        self.assertEqual(res["coverage"], "complete",
                         "as referências resolvem todas — e mesmo assim não basta")
        self.assertFalse(res["eligible"],
                         "cobertura completa com leitura por acabar não é prontidão")

    def test_completed_needs_both_passes(self):
        rec = hydrate(self.eng, load("rec-v04-blueprint-complete"))
        rec["semantic_review"]["passes"]["target_to_source"] = False
        out = C["validate_record"](rec, C["build_inventory"](self.eng), self.eng)
        self.assertEqual(out["semantic_review"], "pending")

    def test_completed_needs_a_real_author(self):
        rec = hydrate(self.eng, load("rec-v04-blueprint-complete"))
        rec["semantic_review"]["performed_by"] = {"kind": "sponsor", "name": ""}
        out = C["validate_record"](rec, C["build_inventory"](self.eng), self.eng)
        self.assertEqual(out["semantic_review"], "pending")

    def test_a_declared_gap_has_to_appear_in_the_findings(self):
        rec = hydrate(self.eng, load("rec-v02-blueprint-missing"))
        rec["semantic_review"]["findings"] = []
        out = C["validate_record"](rec, C["build_inventory"](self.eng), self.eng)
        self.assertEqual(out["semantic_review"], "pending")

    def test_findings_are_a_condition_of_completed_not_of_the_record(self):
        """Uma revisão em curso não é acusada duas vezes pela mesma pendência."""
        rec = hydrate(self.eng, load("rec-neg-semantic-pending"))
        out = C["validate_record"](rec, C["build_inventory"](self.eng), self.eng)
        self.assertEqual(out["semantic_review"], "pending")
        self.assertNotIn("findings", " ".join(d["message"] for d in out["diagnostics"]))


# ======================================================== selecção de revisão §6.6

class Selection(Harness):
    """§6.6 — etapa + identidade do alvo, e entre as candidatas vale a mais recente."""

    def test_the_newest_review_of_the_same_target_wins(self):
        self.install(RECON, "rec-v02-blueprint-missing")
        good = hydrate(self.eng, load("rec-v02-blueprint-missing"))
        good["version"] = "v21"
        for item in good["coverage"]:
            item["assessment"]["status"] = "covered"
            item.pop("required_action", None)
            item.pop("responsible_role", None)
        self.write(good)
        sel = C["select_record"](self.eng, "blueprint", "v01")
        self.assertEqual(sel["selected"]["version"], "v21")

    def test_an_older_complete_review_never_hides_a_newer_one_with_gaps(self):
        """T23 — o cenário que este mecanismo não pode deixar acontecer."""
        self.install(RECON, "rec-v02-blueprint-missing", "rec-v03-blueprint-partial")
        complete = hydrate(self.eng, load("rec-v04-blueprint-complete"))
        complete["version"] = "v21"
        complete["target"] = {"file": BP02, "kind": "blueprint", "identity": "v02",
                              "sha256": C["sha256_file"](self.eng / BP02)}
        for item in complete["coverage"]:
            item["targets"] = [dict(t, file=BP02) for t in item.get("targets", [])]
        self.write(complete)
        newer = hydrate(self.eng, load("rec-v03-blueprint-partial"))
        newer["version"] = "v22"
        self.write(newer)
        res = self.state("blueprint", BP02)
        self.assertEqual(res["record"]["version"], "v22")
        self.assertEqual(res["coverage"], "gaps")
        self.assertIn("_coverage/coverage_v21.json", res["superseded"])

    def test_a_review_of_one_version_cannot_be_relabelled_to_validate_another(self):
        """P1c — cruzar a identidade e mais nada deixava passar a troca de uma etiqueta.

        A revisão completa da `v03`, com `target.identity` trocado à mão para `"v01"`,
        validava a `v01`: o digest do alvo confere (é o da `v03`, que é para onde o
        registo aponta), a identidade confere (foi trocada), e o ficheiro revisto não é
        o que se pediu. Agora o registo não se consegue situar — diz rever uma versão e
        aponta para outra — e isso bloqueia, em vez de ficar invisível."""
        self.install(RECON, "rec-v03-blueprint-partial")
        lying = hydrate(self.eng, load("rec-v04-blueprint-complete"))
        lying["target"]["identity"] = "v01"      # só a etiqueta; o ficheiro é a v03
        self.write(lying)
        res = self.state("blueprint", BP01)
        self.assertNotEqual(res["coverage"], "complete",
                            "a revisão da v03 validou a v01")
        self.assertFalse(res["eligible"])
        self.assertEqual(res["contract_validity"], "invalid")
        self.assertIn("_coverage/coverage_v04.json", res["unreadable_records"])

    def test_the_same_identity_on_another_file_is_not_this_target(self):
        """A outra metade: identidade igual, ficheiro diferente."""
        self.install(RECON, "rec-v02-blueprint-missing")
        other = hydrate(self.eng, load("rec-v02-blueprint-missing"))
        other["version"] = "v21"
        other["target"] = dict(other["target"], file=BP03,
                               sha256=C["sha256_file"](self.eng / BP03))
        # identidade continua a dizer `v01`, ficheiro passa a ser a v03
        self.write(other)
        sel = C["select_record"](self.eng, "blueprint", "v01", target_file=BP01)
        self.assertIsNotNone(sel["selected"])
        self.assertEqual(sel["selected"]["version"], "v02",
                         "o registo do outro ficheiro não é candidato deste alvo")

    def test_two_records_claiming_the_same_identity_are_separated_by_the_file(self):
        """O cruzamento do FICHEIRO, isolado do da identidade.

        Quando o nome do ficheiro não deixa derivar uma versão — `ux-blueprint-final.yaml`
        não traz `_vNN` — a verificação de identidade contra o próprio ficheiro não tem
        nada com que comparar e deixa passar. Aí só o ficheiro separa dois registos que
        declaram a mesma identidade. É o caso que mantém o segundo cruzamento a valer a
        pena, e sem ele este teste falha."""
        self.install(RECON, "rec-v02-blueprint-missing")
        odd = self.eng / "_blueprint" / "ux-blueprint-final.yaml"
        odd.write_text((self.eng / BP03).read_text(encoding="utf-8"), encoding="utf-8")
        self.assertEqual(C["target_identity"](self.eng, "blueprint", odd.name), "",
                         "o cenário exige um nome de que não se deriva versão")
        impostor = hydrate(self.eng, load("rec-v04-blueprint-complete"))
        impostor["version"] = "v21"
        impostor["target"] = {"file": "_blueprint/ux-blueprint-final.yaml",
                              "kind": "blueprint", "identity": "v01",
                              "sha256": C["sha256_file"](odd)}
        self.write(impostor)
        sel = C["select_record"](self.eng, "blueprint", "v01", target_file=BP01)
        self.assertEqual(sel["selected"]["version"], "v02",
                         "o registo de outro ficheiro foi escolhido para este alvo")
        res = self.state("blueprint", BP01)
        self.assertNotEqual(res["coverage"], "complete",
                            "a revisão de outro ficheiro validou este alvo")

    def test_a_well_formed_record_still_selects(self):
        """A fronteira: a verificação nova não pode recusar o caso normal."""
        self.install(RECON, "rec-v03-blueprint-partial", "rec-v04-blueprint-complete")
        res = self.state("blueprint", BP03)
        self.assertEqual(res["record"]["version"], "v04")
        self.assertEqual(res["coverage"], "complete")

    def test_a_review_of_another_version_is_not_applicable_to_this_one(self):
        self.install(RECON, "rec-v02-blueprint-missing")
        res = self.state("blueprint", BP03)
        self.assertEqual(res["coverage"], "not_evaluated")
        self.assertCode(res, "COV-NO-REVIEW")

    def test_no_review_at_all_is_not_evaluated_never_approval(self):
        res = self.state("reconciliation")
        self.assertEqual(res["coverage"], "not_evaluated")
        self.assertEqual(res["freshness"], "not_evaluated")
        self.assertFalse(res["eligible"])
        self.assertCode(res, "COV-NO-REVIEW")

    def test_an_unreadable_record_is_invalid_and_visible(self):
        (self.eng / "_coverage" / "coverage_v01.json").write_text("{ not json",
                                                                  encoding="utf-8")
        res = self.state("reconciliation")
        self.assertEqual(res["contract_validity"], "invalid")
        self.assertCode(res, "COV-SCHEMA")

    def test_a_broken_record_beside_a_good_one_never_gives_a_green(self):
        """P1 — o defeito mais perigoso deste módulo, e o mais fácil de não ver.

        Com a `v01` completa e a `v02` corrompida, a selecção escolhia a `v01` — porque
        a `v02` não se lê — e devolvia `coverage: complete`, `eligible: true`, saída 0.
        O registo que impediria o verde é exactamente o que ninguém consegue ler: não se
        sabe a que etapa pertence, nem a que alvo, nem o que dizia. Escolher o anterior é
        escolher o que convém (§6.6)."""
        self.install(RECON)
        (self.eng / "_coverage" / "coverage_v02.json").write_text("{ corrompido",
                                                                  encoding="utf-8")
        res = self.state("reconciliation")
        self.assertEqual(res["contract_validity"], "invalid")
        self.assertEqual(res["coverage"], "not_evaluated")
        self.assertFalse(res["eligible"],
                         "um ficheiro corrompido em `_coverage/` não pode deixar passar "
                         "um verde")
        self.assertIn("_coverage/coverage_v02.json", res["unreadable_records"])
        self.assertTrue(any("não se conseguem situar" in r for r in res["reasons"]))

    def test_a_record_that_parses_but_cannot_be_situated_also_blocks(self):
        """P1b — o mesmo falso verde, pela porta do lado.

        `select_record` filtrava por `stage` ANTES de perguntar se o registo se conseguia
        situar. Um `{}`, um `schema_version` que mudou de nome às chaves, uma etapa
        inventada ou um registo de desenho sem alvo «não eram desta etapa» — e
        desapareciam em silêncio, deixando a revisão anterior a valer. Situar é saber a
        que par (etapa, alvo) pertence; enquanto não se souber, pode ser o mais recente
        deste."""
        for label, payload in (
                ("objecto vazio", {}),
                ("schema que não traz `stage`", {"schema_version": 99}),
                ("etapa inventada", {"schema_version": 1, "stage": "xpto"}),
                ("desenho sem alvo", {"schema_version": 1, "stage": "blueprint"})):
            with self.subTest(label):
                for f in (self.eng / "_coverage").glob("*.json"):
                    f.unlink()
                self.install(RECON)
                (self.eng / "_coverage" / "coverage_v02.json").write_text(
                    json.dumps(payload), encoding="utf-8")
                res = self.state("reconciliation")
                self.assertEqual(res["contract_validity"], "invalid", label)
                self.assertEqual(res["coverage"], "not_evaluated", label)
                self.assertFalse(res["eligible"], label)
                self.assertIn("_coverage/coverage_v02.json", res["unreadable_records"],
                              label)

    def test_an_unknown_schema_that_can_be_situated_is_unsupported_not_invalid(self):
        """A fronteira do teste acima: situar não é validar.

        Um registo que declara outra versão do contrato **mas diz a que par pertence** é
        seleccionado e traduzido para `unsupported` (T41). Bloqueá-lo na selecção
        transformaria `unsupported` em `invalid`, e são coisas diferentes (§7)."""
        self.install(RECON, "rec-neg-schema-future")
        res = self.state("blueprint", BP03)
        self.assertEqual(res["contract_validity"], "unsupported")
        self.assertEqual(res["record"]["version"], "v15")

    def test_the_broken_record_blocks_every_stage_not_just_its_own(self):
        """Não se sabe a que etapa pertence — por isso bloqueia todas."""
        self.install(RECON, "rec-v02-blueprint-missing")
        (self.eng / "_coverage" / "coverage_v09.json").write_text("nao e json",
                                                                  encoding="utf-8")
        for stage, target in (("reconciliation", None), ("blueprint", BP01)):
            res = self.state(stage, target)
            self.assertEqual(res["contract_validity"], "invalid", stage)
            self.assertFalse(res["eligible"], stage)

    def test_the_stage_separates_records_of_the_same_engagement(self):
        self.install(RECON, "rec-v02-blueprint-missing")
        self.assertEqual(
            C["select_record"](self.eng, "reconciliation")["selected"]["version"], "v01")
        self.assertEqual(
            C["select_record"](self.eng, "blueprint", "v01")["selected"]["version"], "v02")


# ================================================================== autoridade §8.3

class AuthorityVersion(Harness):
    """§8.3 — a revisão consumida tem de ser a da versão que o deliverable lê."""

    def test_reading_v01_while_consuming_the_review_of_v03_is_a_mismatch(self):
        self.install(RECON, "rec-v03-blueprint-partial", "rec-v04-blueprint-complete",
                     "rec-neg-authority-mismatch")
        res = self.state("render", RD02)
        self.assertCode(res, "COV-AUTHORITY-MISMATCH")
        self.assertEqual(res["coverage"], "gaps")
        self.assertFalse(res["eligible"])

    def test_the_mismatch_is_not_a_schema_error(self):
        self.install(RECON, "rec-v03-blueprint-partial", "rec-v04-blueprint-complete",
                     "rec-neg-authority-mismatch")
        res = self.state("render", RD02)
        self.assertEqual(res["contract_validity"], "valid")

    def test_a_changed_deliverable_template_makes_the_review_stale(self):
        self.install(RECON, "rec-v03-blueprint-partial", "rec-v04-blueprint-complete")
        rec = hydrate(self.eng, load("rec-v05-render-complete"))
        rec["deliverable"]["template_sha256"] = "0" * 64
        self.write(rec)
        res = self.state("render", RD02)
        self.assertCode(res, "COV-STALE")


# ====================================================== elegibilidade por acção §8.1

class Eligibility(Harness):
    """§8.1 — produzir para discussão não é aprovar, e as regras diferem."""

    def test_reconciliation_with_routed_gaps_may_still_produce_a_blueprint(self):
        rec = hydrate(self.eng, load(RECON))
        item = rec["coverage"][0]
        item["assessment"]["status"] = "partial"
        item["required_action"] = "fechar a regra com o dono do processo"
        item["responsible_role"] = "dono do processo"
        # `findings` ACUMULA: substituí-lo largava o item `excluded` que o registo já
        # trazia, e isso é um achado impeditivo por direito próprio (§4.7).
        rec["semantic_review"]["findings"].append(item["id"])
        self.write(rec)
        res = self.state("reconciliation")
        self.assertEqual(res["coverage"], "gaps")
        self.assertTrue(res["eligible"],
                        "uma perda identificada e encaminhada não impede produzir uma "
                        "versão para discussão (§8.1)")

    def test_a_gap_without_owner_blocks_production(self):
        """A mesma lacuna, com e sem dono: o que muda a elegibilidade é o encaminhamento.

        E não é erro de ficheiro: o registo continua válido e legível — o que falta é
        revisão, e é por isso que sai `COV-REVIEW-INCOMPLETE` e não `COV-SCHEMA`."""
        rec = hydrate(self.eng, load(RECON))
        item = rec["coverage"][0]
        item["assessment"]["status"] = "partial"
        item["required_action"] = "fechar a regra"
        item["responsible_role"] = "dono do processo"
        rec["semantic_review"]["findings"].append(item["id"])
        self.write(rec)
        self.assertTrue(self.state("reconciliation")["eligible"])
        rec["coverage"][0]["responsible_role"] = " "
        self.write(rec)
        after = self.state("reconciliation")
        self.assertEqual(after["contract_validity"], "valid")
        self.assertFalse(after["eligible"])
        self.assertCode(after, "COV-REVIEW-INCOMPLETE")

    def test_a_blueprint_with_gaps_is_never_ready_for_approval(self):
        self.install(RECON, "rec-v02-blueprint-missing")
        res = self.state("blueprint", BP01)
        self.assertEqual(res["action"], "approve_blueprint")
        self.assertFalse(res["eligible"])

    def test_a_structurally_blocked_version_is_not_ready_even_with_full_coverage(self):
        self.install(RECON, "rec-v03-blueprint-partial", "rec-v04-blueprint-complete")
        before = self.state("blueprint", BP03)
        self.assertTrue(before["eligible"])
        path = self.eng / BP03
        path.write_text(path.read_text(encoding="utf-8").replace(
            "screens:", "screens_broken:", 1), encoding="utf-8")
        res = self.state("blueprint", BP03)
        self.assertNotEqual(res["freshness"], "current",
                            "mexer no alvo torna a revisão stale, antes de tudo o resto")
        self.assertFalse(res["eligible"])

    def test_the_structural_verdict_travels_with_the_result(self):
        self.install(RECON, "rec-v03-blueprint-partial", "rec-v04-blueprint-complete")
        res = self.state("blueprint", BP03)
        self.assertTrue(res["structural"]["evaluated"])
        self.assertEqual(res["structural"]["blocking"], 0)


# ==================================================== relatório determinístico §3

class Report(Harness):
    """A projecção Markdown: determinística, derivada do JSON, **não** autoridade."""

    def setUp(self):
        super().setUp()
        self.install(RECON, "rec-v03-blueprint-partial", "rec-v04-blueprint-complete")
        self.rec = hydrate(self.eng, load("rec-v04-blueprint-complete"))
        self.res = self.state("blueprint", BP03)

    def test_the_same_state_gives_the_same_text(self):
        a = C["render_report"](self.rec, self.res)
        b = C["render_report"](self.rec, self.state("blueprint", BP03))
        self.assertEqual(a, b, "o relatório não pode depender da hora a que corre")

    def test_it_says_it_is_not_authority(self):
        md = C["render_report"](self.rec, self.res)
        self.assertIn("**Não é autoridade**", md)

    def test_it_carries_the_five_verdicts_and_the_action(self):
        md = C["render_report"](self.rec, self.res)
        for key in ("contract_validity", "freshness", "source_review",
                    "semantic_review", "coverage"):
            self.assertIn(self.res[key], md)
        self.assertIn(self.res["action"], md)

    def test_it_shows_the_gaps_with_owner_and_next_action(self):
        res = None
        self.write(hydrate(self.eng, load("rec-v02-blueprint-missing")))
        res = self.state("blueprint", BP01)
        md = C["render_report"](hydrate(self.eng, load("rec-v02-blueprint-missing")), res)
        self.assertIn("Lacunas conhecidas", md)
        self.assertIn("C-007", md)

    def test_it_never_claims_approval(self):
        md = C["render_report"](self.rec, self.res)
        self.assertIn("aprovação e ponta-a-ponta são quatro perguntas separadas", md)
        self.assertIn("falta o pedido de aprovação ao negócio", md,
                      "a página de uma revisão sem lacunas tem de dizer o que ainda "
                      "falta, ou lê-se como aprovação")


# ====================================================================== a porta do
# rascunho

class TheDraftDoor(unittest.TestCase):
    """`read_draft` é a única excepção à porta de leitura, e tem disciplina própria.

    Existe porque um rascunho é um argumento explícito de uma operação explícita e vive,
    por desenho, fora do engagement. O que ela não pode é ler às cegas: um directório, um
    ficheiro que não existe e um ficheiro que não é JSON são três estados distintos, e
    nenhum deles é «vazio»."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)

    def test_a_missing_file_is_absent(self):
        self.assertEqual(C["read_draft"](self.dir / "nope.json")[1], "absent")

    def test_a_directory_is_absent_not_a_read(self):
        self.assertEqual(C["read_draft"](self.dir)[1], "absent")

    def test_text_that_is_not_json_is_unreadable_never_empty(self):
        p = self.dir / "d.json"
        p.write_text("{ nope", encoding="utf-8")
        self.assertEqual(C["read_draft"](p)[1], "unreadable")

    def test_json_that_is_not_an_object_is_unreadable(self):
        p = self.dir / "d.json"
        p.write_text("[1, 2, 3]", encoding="utf-8")
        self.assertEqual(C["read_draft"](p)[1], "unreadable")

    def test_a_real_draft_reads(self):
        p = self.dir / "d.json"
        p.write_text(json.dumps({"stage": "reconciliation"}), encoding="utf-8")
        data, state = C["read_draft"](p)
        self.assertEqual((state, data["stage"]), ("ok", "reconciliation"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
