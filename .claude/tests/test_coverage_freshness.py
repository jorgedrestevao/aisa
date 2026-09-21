"""Fase 2 da reconciliação/cobertura — a base, os fingerprints e a atualidade.

A pergunta que este módulo responde é sempre a mesma: **o que tem de invalidar uma
revisão, e o que nunca pode invalidá-la.** Um mecanismo que invalida por tudo ensina toda
a gente a ignorar `stale`; um que nunca invalida não serve para nada.

Invalida (`stale`):  requisito, fonte, captura, decisão-solução, alvo, template de pacote.
Não invalida:        acrescentar a própria aprovação · produzir uma versão nova do
                     desenho · renderizar um deliverable · escrever num log · regenerar
                     o dashboard.

O T19 completo vive aqui: acrescenta-se uma aprovação a uma cópia e compara-se a **base
inteira** — manifesto, `inventory_sha256` e os dois fingerprints — não só os fingerprints.
A fase 1 deixou este cenário como teste preparatório sobre conjuntos de chaves; é este
que o fecha.

    python .claude/tests/test_coverage_freshness.py
"""

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
BP01 = "_blueprint/ux-blueprint_v01.yaml"
BP03 = "_blueprint/ux-blueprint_v03.yaml"
RD02 = "_render/fx-coverage-f06_solution-blueprint_v02.md"
TEMPLATE = "library/packs/pp/deliverable-templates/solution-blueprint.template.md"

APPROVAL_BLOCK = """
## D-003 — Blueprint bp-v03 aprovado

- **Timestamp**: 2026-03-11T09:00:00+01:00
- **Validated by**: owner (Responsavel de Qualidade — fixture, via AskUserQuestion)
"""
APPROVAL_ROW = ("| D-003 | chair | Aprovação do desenho, versão 03; ver decisions.md#D-003 "
                "| decisions.md#D-003 | 2026-03-11 | organizacional | D-01 |\n")


def copy_engagement(tmp) -> Path:
    dst = Path(tmp) / "fx-coverage-f06"
    shutil.copytree(ENG, dst)
    return dst


def basis_of(eng: Path, stage="blueprint", target=None, authorities=()):
    inv = C["build_inventory"](eng)
    tgt = target if stage != "reconciliation" else None
    return C["compute_basis"](eng, inv, stage, tgt, authorities)


def record_for(eng: Path, stage="blueprint", target_rel=BP01, authorities=()):
    """Uma revisão acabada de escrever: a base dela é a base de agora."""
    target = None
    if stage != "reconciliation":
        target = {"file": target_rel, "kind": "blueprint", "identity": "v01",
                  "sha256": C["sha256_file"](eng / target_rel)}
    return {"schema_version": 1, "stage": stage, "target": target,
            "basis": basis_of(eng, stage, target, authorities)}


def freshness(eng: Path, record, stage=None, authorities=()):
    stage = stage or record["stage"]
    now = basis_of(eng, stage, record.get("target"), authorities)
    return C["check_freshness"](record, now, C["current_target"](eng, record.get("target")))


def append(path: Path, text: str) -> None:
    path.write_text(path.read_text(encoding="utf-8") + text, encoding="utf-8")


def with_approval(eng: Path) -> Path:
    append(eng / "decisions.md", APPROVAL_BLOCK)
    su = eng / "shared-understanding.md"
    body = su.read_text(encoding="utf-8")
    end = body.index("\n", body.index("| D-002 | chair |")) + 1
    su.write_text(body[:end] + APPROVAL_ROW + body[end:], encoding="utf-8")
    return eng


# ================================================================ canonicalização §6.5

class Canonicalisation(unittest.TestCase):

    def test_key_order_does_not_change_the_digest(self):
        self.assertEqual(C["digest"]({"a": 1, "b": 2}), C["digest"]({"b": 2, "a": 1}))

    def test_whitespace_is_collapsed_and_stripped(self):
        self.assertEqual(C["digest"]({"k": "  uma   frase\n"}),
                         C["digest"]({"k": "uma frase"}))

    def test_unicode_is_normalised_to_nfc(self):
        composed, decomposed = "ç", "ç"
        self.assertNotEqual(composed, decomposed)
        self.assertEqual(C["digest"]({"k": composed}), C["digest"]({"k": decomposed}))

    def test_absent_and_empty_are_the_same(self):
        """Contrato §6.5: "campo vazio" e "campo ausente" não podem divergir por acidente."""
        self.assertEqual(C["norm_text"](None), "")
        self.assertEqual(C["digest"]({"k": None}), C["digest"]({"k": ""}))

    def test_the_digest_is_reproducible_across_calls(self):
        inv = C["build_inventory"](ENG)
        self.assertEqual(C["inventory_digest"](inv),
                         C["inventory_digest"](C["build_inventory"](ENG)))

    def test_a_different_unit_content_changes_the_inventory_digest(self):
        before = C["inventory_digest"](C["build_inventory"](ENG))
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            append(eng / "frame.md", "\nmais uma linha\n")
            after = C["inventory_digest"](C["build_inventory"](eng))
        self.assertNotEqual(before, after)


# ========================================================= T19: a base inteira, completa

class ApprovalDoesNotInvalidateTheReviewItConsumes(unittest.TestCase):
    """T19, sobre a **base completa** — não só os dois fingerprints.

    É o ciclo que o plano §7.2 manda cortar: a revisão que autoriza a aprovação não pode
    ficar `stale` no instante em que a aprovação é escrita."""

    def test_the_whole_basis_is_unchanged_by_the_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            rec = record_for(eng, "blueprint", BP03)
            before = rec["basis"]
            with_approval(eng)
            after = basis_of(eng, "blueprint", rec["target"])
        self.assertEqual(before["inventory_sha256"], after["inventory_sha256"])
        self.assertEqual(before["su_fingerprint"], after["su_fingerprint"])
        self.assertEqual(before["decision_fingerprint"], after["decision_fingerprint"])
        self.assertEqual([s for s in before["sources"] if s["use"] == "freshness"],
                         [s for s in after["sources"] if s["use"] == "freshness"])

    def test_the_verdict_is_current(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            rec = record_for(eng, "blueprint", BP03)
            with_approval(eng)
            verdict = freshness(eng, rec)
        self.assertEqual(verdict["status"], "current", verdict["reasons"])
        self.assertEqual(verdict["changed"], [])

    def test_the_bytes_of_the_two_files_did_change(self):
        """A prova de que o teste não é vácuo: os ficheiros mudaram mesmo."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            was = {p: C["sha256_file"](eng / p)
                   for p in ("decisions.md", "shared-understanding.md")}
            with_approval(eng)
            now = {p: C["sha256_file"](eng / p) for p in was}
        for p in was:
            self.assertNotEqual(was[p], now[p], p + " não mudou — o cenário é vácuo")

    def test_the_two_files_are_informative_in_the_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            sources = {s["path"]: s for s in basis_of(eng, "reconciliation")["sources"]}
        for path in ("decisions.md", "shared-understanding.md"):
            self.assertEqual(sources[path]["use"], "informative", path)

    def test_an_approval_of_another_version_still_does_not_invalidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            rec = record_for(eng, "blueprint", BP01)
            with_approval(eng)                      # aprova a v03, a revisão é da v01
            verdict = freshness(eng, rec)
        self.assertEqual(verdict["status"], "current", verdict["reasons"])


# ============================================ os outros dois ciclos que não podem morder

class ProducingDownstreamDoesNotInvalidate(unittest.TestCase):
    """Contrato §6.3 — `_blueprint/` e `_render/` são alvos, não fontes."""

    def test_a_new_blueprint_version_does_not_invalidate_the_review_of_an_older_one(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            rec = record_for(eng, "blueprint", BP01)
            shutil.copyfile(eng / BP03, eng / "_blueprint" / "ux-blueprint_v04.yaml")
            verdict = freshness(eng, rec)
        self.assertEqual(verdict["status"], "current", verdict["reasons"])

    def test_rendering_a_deliverable_does_not_invalidate_the_design_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            rec = record_for(eng, "blueprint", BP03)
            (eng / "_render" / "fx-coverage-f06_solution-blueprint_v03.md").write_text(
                "# Architecture Blueprint\n\nnovo render\n", encoding="utf-8")
            verdict = freshness(eng, rec)
        self.assertEqual(verdict["status"], "current", verdict["reasons"])

    def test_no_target_directory_is_in_the_manifest(self):
        paths = [s["path"] for s in basis_of(ENG, "blueprint",
                                             {"file": BP01, "sha256": ""})["sources"]]
        self.assertEqual([p for p in paths
                          if p.startswith(("_blueprint/", "_render/", "_coverage/"))], [])

    def test_writing_a_log_or_a_dashboard_does_not_invalidate(self):
        """T18 — histórico e derivados nunca tornam uma cobertura stale."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            rec = record_for(eng, "reconciliation")
            append(eng / "council-log.md", "\n## nota nova\n")
            append(eng / "_capture" / "_capture-log.md",
                   "| 2026-03-20 | L1 | x | y | z |\n")
            append(eng / "_blueprint" / "blueprint-log.md", "\n## v04 — nota\n")
            (eng / "dashboard.html").write_text("<html>gerado</html>", encoding="utf-8")
            (eng / "story.md").write_text("# narrativa regenerada\n", encoding="utf-8")
            (eng / "_synthesis" / "_synthesis-checks.md").write_text("check\n",
                                                                    encoding="utf-8")
            verdict = freshness(eng, rec)
        self.assertEqual(verdict["status"], "current", verdict["reasons"])


# ==================================================================== o que TEM de morder

class MaterialChangesInvalidate(unittest.TestCase):

    def test_a_new_source_file_makes_it_stale(self):
        """T06 — o manifesto carrega o CONJUNTO de ficheiros, não só os conhecidos."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            rec = record_for(eng, "reconciliation")
            (eng / "inputs" / "nota-nova.txt").write_text("uma fonte nova\n",
                                                          encoding="utf-8")
            verdict = freshness(eng, rec)
        self.assertEqual(verdict["status"], "stale")
        kinds = {c["kind"] for c in verdict["changed"]}
        self.assertIn("source-added", kinds)

    def test_a_removed_source_makes_it_stale(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            rec = record_for(eng, "reconciliation")
            (eng / "inputs" / "fluxo-de-libertacao.pptx").unlink()
            verdict = freshness(eng, rec)
        self.assertEqual(verdict["status"], "stale")
        self.assertIn("source-removed", {c["kind"] for c in verdict["changed"]})

    def test_a_changed_workbook_without_recapture_makes_it_stale(self):
        """T07 — a captura antiga não pode carimbar um ficheiro novo como revisto."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            rec = record_for(eng, "reconciliation")
            wb = eng / "inputs" / "registo-de-lotes.xlsx"
            wb.write_bytes(wb.read_bytes() + b"\x00")
            verdict = freshness(eng, rec)
        self.assertEqual(verdict["status"], "stale")
        changed = [c for c in verdict["changed"] if c["kind"] == "source-changed"]
        self.assertTrue(any("registo-de-lotes.xlsx" in c["what"] for c in changed))

    def test_changing_a_requirement_row_makes_it_stale(self):
        """T20 — muda o requisito, mesmo com o id igual."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            rec = record_for(eng, "reconciliation")
            su = eng / "shared-understanding.md"
            su.write_text(su.read_text(encoding="utf-8").replace(
                "gravado diariamente na área partilhada da qualidade",
                "enviado por email às sextas"), encoding="utf-8")
            verdict = freshness(eng, rec)
        self.assertEqual(verdict["status"], "stale")
        what = {c["what"] for c in verdict["changed"]}
        self.assertIn("su_fingerprint", what)
        self.assertIn("inventory_sha256", what)

    def test_changing_the_solution_decision_makes_it_stale(self):
        """T20 — e a exclusão dos espelhos de aprovação não protege isto."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            rec = record_for(eng, "reconciliation")
            dec = eng / "decisions.md"
            dec.write_text(dec.read_text(encoding="utf-8").replace(
                "- **Chosen option**: O-002 — aplicação com base de dados governada",
                "- **Chosen option**: O-001 — manter a folha com procedimento escrito"),
                encoding="utf-8")
            verdict = freshness(eng, rec)
        self.assertEqual(verdict["status"], "stale")
        self.assertIn("decision_fingerprint", {c["what"] for c in verdict["changed"]})

    def test_a_correcting_answer_makes_it_stale_and_keeps_the_old_one(self):
        """T17 — a cadeia de supersessão não se apaga; a revisão é que tem de a reler."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            rec = record_for(eng, "reconciliation")
            before = {u["unit_key"] for u in C["build_inventory"](eng)["units"]}
            append(eng / "answers.md",
                   "\n## U-004 — 2026-03-20 (correcção)\n"
                   "- **Resposta**: \"Afinal também segue por email às sextas.\"\n")
            verdict = freshness(eng, rec)
            after = {u["unit_key"] for u in C["build_inventory"](eng)["units"]}
        self.assertEqual(verdict["status"], "stale")
        self.assertIn("answers.md#U-004[1]", after)
        self.assertIn("answers.md#U-004[2]", after)
        self.assertIn("answers.md#U-004", before)

    def test_modifying_the_target_makes_it_stale(self):
        """T21 — pelo digest do alvo, que não vive no manifesto."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            rec = record_for(eng, "blueprint", BP01)
            append(eng / BP01, "\n# uma linha acrescentada depois da revisão\n")
            verdict = freshness(eng, rec)
        self.assertEqual(verdict["status"], "stale")
        self.assertIn("target-changed", {c["kind"] for c in verdict["changed"]})

    def test_a_missing_target_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            rec = record_for(eng, "blueprint", BP01)
            (eng / BP01).unlink()
            verdict = freshness(eng, rec)
        self.assertEqual(verdict["status"], "stale")
        self.assertIn("target-missing", {c["kind"] for c in verdict["changed"]})

    def test_a_changed_pack_template_makes_it_stale(self):
        """T39 — autoridade de pacote entra por digest, recalculado do ficheiro.

        O template real não se toca: o que se altera é o digest que o REGISTO declara,
        que é o lado histórico. O lado actual vem sempre do ficheiro (achado A3)."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            rec = record_for(eng, "blueprint", BP03,
                             authorities=[str(ROOT / TEMPLATE)])
            self.assertTrue(rec["basis"]["authorities"])
            self.assertEqual(rec["basis"]["authorities"][0]["sha256"],
                             C["sha256_file"](ROOT / TEMPLATE))
            fake = dict(rec["basis"]["authorities"][0], sha256="0" * 64)
            rec["basis"] = dict(rec["basis"], authorities=[fake])
            verdict = freshness(eng, rec, authorities=[str(ROOT / TEMPLATE)])
        self.assertEqual(verdict["status"], "stale")
        self.assertIn("authority-changed", {c["kind"] for c in verdict["changed"]})

    def test_a_different_contract_version_is_not_staleness_at_all(self):
        """T41 — e achado A5: o motor dizia `unsupported` e devolvia `stale`.

        São coisas diferentes. `stale` é «a base mudou, relê»; `unsupported` é «este
        motor não sabe ler este schema». Sai num campo próprio, e quem valida registos
        (fase 3) traduz para `contract_validity`."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            rec = record_for(eng, "reconciliation")
            rec["basis"] = dict(rec["basis"], contract_version="0")
            verdict = freshness(eng, rec)
        self.assertEqual(verdict["status"], "current",
                         "a versão do contrato não é atualidade")
        self.assertEqual([c for c in verdict["changed"]
                          if c.get("kind") == "contract-version"], [])
        mismatch = verdict["contract_version_mismatch"]
        self.assertIsNotNone(mismatch)
        self.assertEqual(mismatch["verdict"], "unsupported")
        self.assertEqual(mismatch["declared"], "0")
        self.assertEqual(mismatch["implemented"], C["CONTRACT_VERSION"])

    def test_the_same_contract_version_reports_no_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            verdict = freshness(eng, record_for(eng, "reconciliation"))
        self.assertIsNone(verdict["contract_version_mismatch"])

    def test_stale_says_what_it_does_not_prove(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            rec = record_for(eng, "reconciliation")
            (eng / "inputs" / "outro.txt").write_text("x", encoding="utf-8")
            verdict = freshness(eng, rec)
        self.assertIn("não declara falsa nenhuma conclusão", verdict["note"])


# ============================================================== o que os fingerprints leem

class Fingerprints(unittest.TestCase):

    def test_an_assumed_row_stays_assumed(self):
        """T16 — o fingerprint lê o estado; nada aqui promove nada."""
        readers = C["ReaderAdapter"]()
        _h, rows, _m, _d = readers.parse_su(
            (ENG / "shared-understanding.md").read_text(encoding="utf-8"))
        states = {r["id"]: r["state"] for r in rows}
        self.assertEqual(states["A-002"], "Assumed")
        self.assertEqual(states["A-003"], "Assumed")

    def test_the_su_fingerprint_ignores_the_derived_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            before = C["su_fingerprint"](eng, C["ReaderAdapter"]())
            su = eng / "shared-understanding.md"
            su.write_text(su.read_text(encoding="utf-8").replace(
                "> Última actualização: 2026-03-06T18:00:00+01:00",
                "> Última actualização: 2026-04-01T09:00:00+01:00"), encoding="utf-8")
            after = C["su_fingerprint"](eng, C["ReaderAdapter"]())
        self.assertEqual(before, after,
                         "um carimbo derivado não é conhecimento e não pode invalidar")

    def test_the_su_fingerprint_drops_only_the_approval_mirror(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            before = C["su_fingerprint"](eng, C["ReaderAdapter"]())
            with_approval(eng)
            after = C["su_fingerprint"](eng, C["ReaderAdapter"]())
            su = eng / "shared-understanding.md"
            su.write_text(su.read_text(encoding="utf-8").replace(
                "| D-002 | chair | Decisão: O-002",
                "| D-002 | chair | Decisão: O-009"), encoding="utf-8")
            changed = C["su_fingerprint"](eng, C["ReaderAdapter"]())
        self.assertEqual(before, after, "a linha da aprovação não podia entrar")
        self.assertNotEqual(after, changed, "a linha da decisão-solução tinha de entrar")

    def test_the_decision_fingerprint_follows_the_live_decision(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            before = C["decision_fingerprint"](eng, C["ReaderAdapter"]())
            with_approval(eng)
            after = C["decision_fingerprint"](eng, C["ReaderAdapter"]())
            append(eng / "decisions.md",
                   "\n## D-005 — Adopt O-001 — manter a folha\n\n"
                   "- **Chosen option**: O-001\n"
                   "- **Supersedes**: D-002 — reaberta\n"
                   "- **Timestamp**: 2026-04-02T10:00:00+01:00\n")
            reopened = C["decision_fingerprint"](eng, C["ReaderAdapter"]())
        self.assertEqual(before, after, "a aprovação não é a decisão-solução")
        self.assertNotEqual(after, reopened, "uma decisão nova tem de invalidar")

    def test_the_basis_names_the_live_decision(self):
        self.assertEqual(basis_of(ENG, "reconciliation")["decision_ref"], "D-002")


# ================================================ os registos da fase 1, hidratados

PLACEHOLDER = "b31c2af5507500ef2272d791693f3335b4be63f86ff8a781a8436d1cc253fb81"
RECORDS = FIX / "records"


def hydrate(eng: Path, record: dict, stage: str, synthesis_authorities=()) -> dict:
    """Troca os três digests derivados de placeholder pelo que o motor calcula.

    É isto que a fase 1 deixou por fazer (dependência 3): a canonicalização era do motor,
    e os registos guardavam um valor convencional em vez de um digest inventado à mão.
    O manifesto e as autoridades dos registos ficam como estão — são digests de bytes,
    reais desde a fase 1."""
    now = basis_of(eng, stage, record.get("target"))
    basis = dict(record["basis"])
    for field in ("inventory_sha256", "su_fingerprint", "decision_fingerprint"):
        assert basis[field] == PLACEHOLDER, field + " já não é o placeholder"
        basis[field] = now[field]
    return dict(record, basis=basis)


class Phase1RecordsHydrate(unittest.TestCase):
    """Os registos que a fase 1 escreveu tornam-se utilizáveis sem serem reescritos."""

    def _load(self, name):
        return json.loads((RECORDS / name).read_text(encoding="utf-8"))

    def test_every_wellformed_record_still_carries_the_placeholder(self):
        seen = 0
        for p in sorted(RECORDS.glob("*.json")):
            rec = json.loads(p.read_text(encoding="utf-8"))
            basis = rec.get("basis")
            if not basis:
                continue
            seen += 1
            for field in ("inventory_sha256", "su_fingerprint", "decision_fingerprint"):
                self.assertEqual(basis[field], PLACEHOLDER, p.name)
        self.assertGreater(seen, 10)

    def test_a_hydrated_record_is_current_against_the_untouched_fixture(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            rec = hydrate(eng, self._load("rec-v04-blueprint-complete.json"), "blueprint")
            verdict = freshness(eng, rec)
        self.assertEqual(verdict["status"], "current", verdict["reasons"])

    def test_the_manifest_of_a_phase_one_record_still_matches_the_files(self):
        """Os digests de bytes que a fase 1 escreveu continuam a bater certo."""
        rec = self._load("rec-v04-blueprint-complete.json")
        bad = []
        for src in rec["basis"]["sources"]:
            p = ENG / src["path"]
            if not p.is_file() or C["sha256_file"](p) != src["sha256"]:
                bad.append(src["path"])
        self.assertEqual(bad, [])

    def test_a_hydrated_record_goes_stale_when_the_source_changes(self):
        """A hidratação não é um passe-livre: só troca o que era convencional."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            rec = hydrate(eng, self._load("rec-v04-blueprint-complete.json"), "blueprint")
            append(eng / "answers.md", "\n## U-011 — 2026-04-01\n- x\n")
            verdict = freshness(eng, rec)
        self.assertEqual(verdict["status"], "stale")

    def test_the_target_digest_of_the_stale_fixture_is_wrong_on_purpose(self):
        rec = self._load("rec-neg-stale-target.json")
        real = C["sha256_file"](ENG / rec["target"]["file"])
        self.assertNotEqual(rec["target"]["sha256"], real)
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            hydrated = hydrate(eng, rec, "blueprint")
            verdict = freshness(eng, hydrated)
        self.assertEqual(verdict["status"], "stale")
        self.assertIn("target-changed", {c["kind"] for c in verdict["changed"]})


# ==================================== A3: a base "actual" nao transporta evidencia antiga

class AuthorityDigestsAreAlwaysRecomputed(unittest.TestCase):
    """Achado A3 — `compute_basis()` copiava o sha256 recebido em vez de o recalcular.

    A consequência era silenciosa e grave: a base que se diz «actual» transportava o
    digest que o chamador declarou, por isso uma alteração de template passava
    despercebida por essa via — exactamente o cenário T39 que o contrato quer apanhar."""

    def _authority(self, eng: Path) -> Path:
        p = eng / "autoridade-de-teste.md"
        p.write_text("versão 1\n", encoding="utf-8")
        return p

    def test_the_string_form_hashes_the_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            p = self._authority(eng)
            basis = basis_of(eng, "reconciliation", authorities=[str(p)])
            real = C["sha256_file"](p)
        self.assertEqual(basis["authorities"][0]["sha256"], real)

    def test_the_dict_form_ignores_the_declared_digest(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            p = self._authority(eng)
            stale_declared = "0" * 64
            basis = basis_of(eng, "reconciliation",
                             authorities=[{"path": "autoridade-de-teste.md",
                                           "sha256": stale_declared}])
            real = C["sha256_file"](p)
        self.assertNotEqual(basis["authorities"][0]["sha256"], stale_declared)
        self.assertEqual(basis["authorities"][0]["sha256"], real)

    def test_a_changed_authority_is_seen_through_the_dict_form(self):
        """O caso concreto que o revisor correu: alterar o ficheiro e recalcular."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            p = self._authority(eng)
            before = basis_of(eng, "reconciliation", authorities=[str(p)])
            declared = before["authorities"][0]["sha256"]
            p.write_text("versão 2 — mudou\n", encoding="utf-8")
            after = basis_of(eng, "reconciliation",
                             authorities=[{"path": "autoridade-de-teste.md",
                                           "sha256": declared}])
        self.assertNotEqual(declared, after["authorities"][0]["sha256"],
                            "a base actual reutilizou o digest antigo")

    def test_it_makes_the_review_stale_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            p = self._authority(eng)
            rec = record_for(eng, "reconciliation", authorities=[str(p)])
            p.write_text("versão 2 — mudou\n", encoding="utf-8")
            verdict = freshness(eng, rec, authorities=[str(p)])
        self.assertEqual(verdict["status"], "stale")
        self.assertIn("authority-changed", {c["kind"] for c in verdict["changed"]})

    def test_a_missing_authority_is_reported_not_silently_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            basis = basis_of(eng, "reconciliation",
                             authorities=["autoridade-que-nao-existe.md"])
        self.assertEqual(basis["authorities"][0]["sha256"], "")
        self.assertEqual(basis["authorities"][0]["state"], "absent")
        self.assertTrue(any(d["blocking"] for d in basis["diagnostics"]))

    def test_an_authority_outside_the_boundary_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            outside = Path(tmp) / "fora.md"
            outside.write_text("x", encoding="utf-8")
            basis = basis_of(eng, "reconciliation", authorities=[str(outside)])
        self.assertEqual(basis["authorities"][0]["state"], "refused")
        self.assertTrue(any(d["blocking"] for d in basis["diagnostics"]))

    def test_a_real_pack_template_is_an_allowed_authority(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            basis = basis_of(eng, "reconciliation",
                             authorities=[str(ROOT / TEMPLATE)])
        self.assertEqual(basis["authorities"][0]["state"], "ok")
        self.assertEqual(basis["authorities"][0]["sha256"],
                         C["sha256_file"](ROOT / TEMPLATE))


# ================================================================== contrato da API

class ApiContract(unittest.TestCase):

    def test_reconciliation_refuses_a_target(self):
        inv = C["build_inventory"](ENG)
        with self.assertRaises(C["CoverageError"]):
            C["compute_basis"](ENG, inv, "reconciliation", {"file": BP01})

    def test_the_other_stages_require_one(self):
        inv = C["build_inventory"](ENG)
        for stage in ("blueprint", "render"):
            with self.assertRaises(C["CoverageError"]):
                C["compute_basis"](ENG, inv, stage, None)

    def test_an_unknown_stage_is_refused(self):
        inv = C["build_inventory"](ENG)
        with self.assertRaises(C["CoverageError"]):
            C["compute_basis"](ENG, inv, "aprovacao", None)

    def test_a_record_without_a_basis_is_not_evaluated(self):
        """Nunca `current` por omissão: não avaliado é um resultado, não um verde."""
        verdict = C["check_freshness"]({"stage": "blueprint"}, basis_of(ENG, "reconciliation"))
        self.assertEqual(verdict["status"], "not_evaluated")

    def test_the_render_stage_admits_the_synthesis_it_declares(self):
        story = "_synthesis/architecture-story.md"
        target = {"file": RD02, "sha256": ""}
        without = basis_of(ENG, "render", target)
        with_it = C["compute_basis"](ENG, C["build_inventory"](ENG), "render", target,
                                     synthesis_authorities=[story])
        self.assertNotIn(story, [s["path"] for s in without["sources"]])
        entry = [s for s in with_it["sources"] if s["path"] == story]
        self.assertEqual(len(entry), 1)
        self.assertEqual(entry[0]["use"], "freshness")

    def test_nothing_here_writes(self):
        import hashlib
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            snap = {p.relative_to(eng).as_posix():
                    hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in eng.rglob("*") if p.is_file()}
            rec = record_for(eng, "blueprint", BP01)
            freshness(eng, rec)
            C["resolve_unit"](eng, "shared-understanding.md#C-007")
            after = {p.relative_to(eng).as_posix():
                     hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in eng.rglob("*") if p.is_file()}
        self.assertEqual(snap, after)


if __name__ == "__main__":
    unittest.main(verbosity=2)
