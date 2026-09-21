"""Fase 3 da reconciliação/cobertura — linha de comandos e persistência versionada.

Duas perguntas, e as duas são sobre escrita:

  1. **O que é que a verificação escreve?** Nada. `inventory`, `check` e `report` correm
     sobre o engagement e deixam-no byte a byte como estava — verificado com manifesto
     SHA-256 antes e depois, e com duas execuções seguidas.
  2. **O que é que `finalize` se recusa a fazer?** Publicar um registo ilegível, publicar
     sobre uma base que mudou depois da revisão, e sobrescrever uma versão publicada.
     A terceira é a que este mecanismo existe para impedir: carimbar como revista uma
     fonte que mudou sem ser relida.

Mais os códigos de saída, a resolução de engagement e a projecção Markdown que não é
autoridade (T40).

    python .claude/tests/test_coverage_integration.py
"""

import hashlib
import json
import os
import runpy
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "library" / "kernel" / "tools" / "coverage.py"
C = runpy.run_path(str(ENGINE))
FIX = Path(__file__).resolve().parent / "fixtures" / "coverage"
ENG = FIX / "fx-coverage-f06"
RECORDS = FIX / "records"
PLACEHOLDER = "b31c2af5507500ef2272d791693f3335b4be63f86ff8a781a8436d1cc253fb81"
BP01 = "_blueprint/ux-blueprint_v01.yaml"
BP03 = "_blueprint/ux-blueprint_v03.yaml"
RECON = "rec-v01-reconciliation-complete"


def load(name: str) -> dict:
    return json.loads((RECORDS / (name + ".json")).read_text(encoding="utf-8"))


def hydrate(eng: Path, rec: dict) -> dict:
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


def manifest(root: Path, skip=()) -> dict:
    out = {}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            rel = p.relative_to(root).as_posix()
            if any(rel.startswith(s) for s in skip):
                continue
            out[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def cli(*args, cwd=None, root=None):
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    if root:
        env["AISA_ENGAGEMENTS_ROOT"] = str(root)
    return subprocess.run([sys.executable, "-B", str(ENGINE), *args],
                          cwd=str(cwd or ROOT), env=env, text=True,
                          capture_output=True, encoding="utf-8", errors="replace")


class Base(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.eng = self.root / "fx-coverage-f06"
        shutil.copytree(ENG, self.eng)

    def install(self, *names):
        (self.eng / "_coverage").mkdir(exist_ok=True)
        for name in names:
            rec = hydrate(self.eng, load(name))
            (self.eng / "_coverage" / ("coverage_%s.json" % rec["version"])).write_text(
                json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")

    def draft(self, name=RECON, mutate=None) -> Path:
        rec = hydrate(self.eng, load(name))
        if mutate:
            mutate(rec)
        path = self.root / "draft.json"
        path.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
        return path


# ================================================================== códigos de saída

class ExitCodes(Base):
    """Contrato §7 — e o JSON continua a sair mesmo quando o código não é 0."""

    def test_inventory_exits_zero_on_a_complete_denominator(self):
        r = cli("inventory", "--engagement", str(self.eng))
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_check_without_a_review_exits_four_and_still_prints_json(self):
        r = cli("check", "--engagement", str(self.eng), "--stage", "reconciliation",
                "--json")
        self.assertEqual(r.returncode, 4)
        data = json.loads(r.stdout)
        self.assertEqual(data["coverage"], "not_evaluated")
        self.assertIn("COV-NO-REVIEW", [d["code"] for d in data["diagnostics"]])

    def test_a_complete_reconciliation_exits_zero(self):
        self.install(RECON)
        r = cli("check", "--engagement", str(self.eng), "--stage", "reconciliation",
                "--json")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue(json.loads(r.stdout)["eligible"])

    def test_a_blueprint_with_gaps_exits_four(self):
        self.install(RECON, "rec-v02-blueprint-missing")
        r = cli("check", "--engagement", str(self.eng), "--stage", "blueprint",
                "--target", BP01, "--json")
        self.assertEqual(r.returncode, 4)
        self.assertEqual(json.loads(r.stdout)["coverage"], "gaps")

    def test_an_invalid_schema_exits_two(self):
        self.install(RECON, "rec-neg-schema-invalid")
        r = cli("check", "--engagement", str(self.eng), "--stage", "blueprint",
                "--target", BP01, "--json")
        self.assertEqual(r.returncode, 2)
        self.assertEqual(json.loads(r.stdout)["contract_validity"], "invalid")

    def test_a_future_schema_exits_two(self):
        self.install(RECON, "rec-neg-schema-future")
        r = cli("check", "--engagement", str(self.eng), "--stage", "blueprint",
                "--target", BP03, "--json")
        self.assertEqual(r.returncode, 2)
        self.assertEqual(json.loads(r.stdout)["contract_validity"], "unsupported")

    def test_a_stage_that_needs_a_target_without_one_exits_two(self):
        r = cli("check", "--engagement", str(self.eng), "--stage", "blueprint")
        self.assertEqual(r.returncode, 2)
        self.assertIn("--target", r.stderr)

    def test_reconciliation_with_a_target_exits_two(self):
        r = cli("check", "--engagement", str(self.eng), "--stage", "reconciliation",
                "--target", BP01)
        self.assertEqual(r.returncode, 2)

    def test_an_unknown_engagement_exits_three(self):
        r = cli("check", "--engagement", "nao-existe", "--stage", "reconciliation")
        self.assertEqual(r.returncode, 3)

    def test_exit_zero_never_means_approval(self):
        self.install(RECON, "rec-v03-blueprint-partial", "rec-v04-blueprint-complete")
        r = cli("check", "--engagement", str(self.eng), "--stage", "blueprint",
                "--target", BP03, "--json")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        data = json.loads(r.stdout)
        self.assertTrue(data["eligible"])
        self.assertIn("aprovação", data["note"].lower())
        self.assertNotIn("aprovado",
                         (self.eng / "decisions.md").read_text(encoding="utf-8").lower())


class WrongTypesAreSchemaErrors(Base):
    """P2c — um registo é DADO, não código. O tipo errado sai como diagnóstico.

    `target: "bad"` e `based_on: [{}]` davam `COV-UNEXPECTED`, saída **5** e stdout
    vazio: nenhum JSON, nenhum código da tabela §8, nada para quem estivesse a ler a
    saída. Um consumidor que trate 5 como «erro do motor» ficava sem saber que o
    problema era o ficheiro dele. Saída 5 fica para falha interna genuína — e este teste
    existe para que a próxima forma de tipo errado não volte a chegar lá."""

    MUTATIONS = (
        ("target string", lambda r: r.__setitem__("target", "bad")),
        ("target lista", lambda r: r.__setitem__("target", [])),
        ("target número", lambda r: r.__setitem__("target", 7)),
        ("based_on com mapa", lambda r: r.__setitem__("based_on", [{}])),
        ("based_on número", lambda r: r.__setitem__("based_on", 7)),
        ("based_on string", lambda r: r.__setitem__("based_on", "coverage_v01.json")),
        ("basis string", lambda r: r.__setitem__("basis", "x")),
        ("basis lista", lambda r: r.__setitem__("basis", [])),
        ("basis.sources string", lambda r: r["basis"].__setitem__("sources", "x")),
        ("basis.authorities número", lambda r: r["basis"].__setitem__("authorities", 3)),
        ("source_review mapa", lambda r: r.__setitem__("source_review", {})),
        ("coverage string", lambda r: r.__setitem__("coverage", "x")),
        ("semantic_review lista", lambda r: r.__setitem__("semantic_review", [])),
        ("unit_refs string", lambda r: r["source_review"][0].__setitem__(
            "unit_refs", "answers.md#U-004")),
        ("requirement_refs string", lambda r: r["coverage"][0].__setitem__(
            "requirement_refs", "C-007")),
        ("source_unit_refs mapa", lambda r: r["coverage"][0].__setitem__(
            "source_unit_refs", {})),
        ("targets string", lambda r: r["coverage"][0].__setitem__("targets", "x")),
        ("targets com string", lambda r: r["coverage"][0].__setitem__("targets", ["x"])),
        ("assessment string", lambda r: r["coverage"][0].__setitem__("assessment", "ok")),
        ("findings string", lambda r: r["semantic_review"].__setitem__(
            "findings", "item-001")),
        ("limitations string", lambda r: r["semantic_review"].__setitem__(
            "limitations", "nenhuma")),
        ("performed_by string", lambda r: r["semantic_review"].__setitem__(
            "performed_by", "eu")),
    )

    def test_no_wrong_type_reaches_the_internal_failure_exit(self):
        for label, mutate in self.MUTATIONS:
            with self.subTest(label):
                self.install(RECON)
                rec = hydrate(self.eng, load("rec-v02-blueprint-missing"))
                mutate(rec)
                (self.eng / "_coverage" / "coverage_v02.json").write_text(
                    json.dumps(rec, ensure_ascii=False), encoding="utf-8")
                r = cli("check", "--engagement", str(self.eng), "--stage", "blueprint",
                        "--target", BP01, "--json")
                self.assertNotEqual(r.returncode, 5,
                                    "%s deu falha interna: %s" % (label, r.stderr[:200]))
                self.assertIn(r.returncode, (2, 4), label)
                data = json.loads(r.stdout)      # rebenta se o JSON não saiu
                self.assertFalse(data["eligible"], label)
                for f in (self.eng / "_coverage").glob("*.json"):
                    f.unlink()

    def test_the_diagnostic_names_the_field_and_the_type_it_got(self):
        self.install(RECON)
        rec = hydrate(self.eng, load("rec-v02-blueprint-missing"))
        rec["target"] = "bad"
        (self.eng / "_coverage" / "coverage_v02.json").write_text(
            json.dumps(rec, ensure_ascii=False), encoding="utf-8")
        r = cli("check", "--engagement", str(self.eng), "--stage", "blueprint",
                "--target", BP01, "--json")
        self.assertEqual(r.returncode, 2)
        messages = " ".join(d["message"] for d in json.loads(r.stdout)["diagnostics"])
        self.assertIn("target", messages)
        self.assertIn("str", messages, "o diagnóstico tem de dizer o tipo que recebeu")

    def test_a_finalize_of_a_wrongly_typed_draft_refuses_with_two(self):
        rec = hydrate(self.eng, load(RECON))
        rec["basis"] = "x"
        draft = self.root / "draft.json"
        draft.write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")
        r = cli("finalize", "--engagement", str(self.eng), "--draft", str(draft))
        self.assertEqual(r.returncode, 2, r.stderr[:200])
        self.assertFalse((self.eng / "_coverage").is_dir())


# ============================================================ resolução e ambiente

class Environment(Base):
    """T26, T27 — cwd arbitrário, caminhos com espaços e acentos, e ambiguidade."""

    def test_it_runs_from_a_directory_outside_the_repository(self):
        other = self.root / "algures"
        other.mkdir()
        r = cli("inventory", "--engagement", str(self.eng), cwd=other)
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_a_path_with_spaces_and_accents_resolves(self):
        odd = self.root / "pasta com acentuação e espaços"
        odd.mkdir()
        eng = odd / "fx-coverage-f06"
        shutil.copytree(ENG, eng)
        r = cli("check", "--engagement", str(eng), "--stage", "reconciliation", "--json")
        self.assertEqual(r.returncode, 4)
        self.assertEqual(json.loads(r.stdout)["engagement"], "fx-coverage-f06")

    def test_a_slug_under_the_engagements_root_resolves(self):
        r = cli("inventory", "--engagement", "fx-coverage-f06", root=self.root)
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_two_engagements_without_a_slug_fail_instead_of_choosing(self):
        shutil.copytree(ENG, self.root / "outro")
        r = cli("check", "--stage", "reconciliation", root=self.root)
        self.assertEqual(r.returncode, 2)
        self.assertIn("mais do que um", r.stderr)

    def test_a_target_outside_the_engagement_is_refused(self):
        r = cli("check", "--engagement", str(self.eng), "--stage", "blueprint",
                "--target", str(ROOT / "library" / "kernel" / "tools" / "dashboard.py"))
        self.assertEqual(r.returncode, 3)


# ================================================================== zero escrita

class ReadOnly(Base):
    """T38 — a verificação corre sobre o engagement e não lhe toca."""

    def test_check_and_report_write_nothing(self):
        self.install(RECON, "rec-v03-blueprint-partial", "rec-v04-blueprint-complete")
        before = manifest(self.eng)
        for _ in range(2):
            cli("inventory", "--engagement", str(self.eng))
            cli("check", "--engagement", str(self.eng), "--stage", "reconciliation")
            cli("check", "--engagement", str(self.eng), "--stage", "blueprint",
                "--target", BP03)
            cli("report", "--engagement", str(self.eng), "--stage", "blueprint",
                "--target", BP03)
        self.assertEqual(manifest(self.eng), before,
                         "uma verificação read-only que escreve deixou de ser read-only")

    def test_two_runs_give_the_same_answer(self):
        self.install(RECON)
        a = cli("check", "--engagement", str(self.eng), "--stage", "reconciliation",
                "--json")
        b = cli("check", "--engagement", str(self.eng), "--stage", "reconciliation",
                "--json")
        self.assertEqual(a.stdout, b.stdout)
        self.assertEqual(a.returncode, b.returncode)

    def test_the_engine_never_writes_outside_finalize(self):
        """Lido pela árvore sintáctica: `open(...,'w')` e `mkdir` só dentro de
        `finalize`."""
        import ast
        tree = ast.parse(ENGINE.read_text(encoding="utf-8"))
        allowed = {"finalize", "_coverage_dir"}
        offenders = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef) or node.name in allowed:
                continue
            for sub in ast.walk(node):
                if not isinstance(sub, ast.Call):
                    continue
                name = ""
                if isinstance(sub.func, ast.Attribute):
                    name = sub.func.attr
                elif isinstance(sub.func, ast.Name):
                    name = sub.func.id
                if name in ("write_text", "write_bytes", "mkdir", "replace", "unlink",
                            "rename"):
                    if name == "replace" and isinstance(sub.func, ast.Attribute) \
                            and not isinstance(sub.func.value, ast.Name):
                        continue        # str.replace, não os.replace
                    offenders.append("%s:%d %s" % (node.name, sub.lineno, name))
        self.assertEqual(offenders, [],
                         "escrita fora de `finalize`: %s" % offenders)

    def test_no_except_swallows_silently(self):
        """Lido pela árvore sintáctica: nenhum `except` do motor tem por corpo só
        `pass` ou `continue`.

        Foi assim que nasceu o P2e — `except CoverageError: continue`, com um comentário
        a explicar porque é que não fazia mal. Uma excepção apanhada tem de devolver um
        estado, um diagnóstico ou um valor; o que não pode é desaparecer. Contrato §8:
        falha de avaliação é «não avaliado», nunca sucesso silencioso."""
        import ast
        tree = ast.parse(ENGINE.read_text(encoding="utf-8"))
        offenders = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.ExceptHandler):
                continue
            body = [st for st in node.body if not isinstance(st, ast.Expr)
                    or not isinstance(getattr(st, "value", None), ast.Constant)]
            if body and all(isinstance(st, (ast.Pass, ast.Continue)) for st in body):
                offenders.append("linha %d: %s" % (
                    node.lineno, ast.unparse(node).splitlines()[0][:70]))
        self.assertEqual(offenders, [],
                         "estes `except` engolem sem registar: %s" % offenders)

    def test_there_is_no_os_replace_over_a_published_version(self):
        """Lido pela ÁRVORE SINTÁCTICA, não por procura de texto.

        A lição da fase 1: um comentário que explica a regra não pode contar como
        violação dela — e o docstring de `finalize` diz, de propósito, que `os.replace`
        não existe aqui."""
        import ast
        tree = ast.parse(ENGINE.read_text(encoding="utf-8"))
        calls = [n.lineno for n in ast.walk(tree)
                 if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                 and n.func.attr == "replace" and isinstance(n.func.value, ast.Name)
                 and n.func.value.id in ("os", "shutil")]
        self.assertEqual(calls, [],
                         "`os.replace` sobre uma versão publicada é exactamente o que o "
                         "contrato §6.6 proíbe (linhas %s)" % calls)


# ==================================================================== finalização

class Finalize(Base):
    """§6.6 — reserva exclusiva, recusa fundamentada, e nunca sobrescreve."""

    def test_a_clean_draft_is_published_as_the_next_version(self):
        out = C["finalize"](self.eng, self.draft())
        self.assertTrue(out["published"], out.get("message"))
        self.assertEqual(out["version"], "v01")
        self.assertTrue((self.eng / "_coverage" / "coverage_v01.json").is_file())
        self.assertTrue((self.eng / "_coverage" / "coverage_v01.md").is_file())

    def test_the_second_finalize_takes_the_next_free_version(self):
        C["finalize"](self.eng, self.draft())
        out = C["finalize"](self.eng, self.draft())
        self.assertEqual(out["version"], "v02")
        self.assertTrue((self.eng / "_coverage" / "coverage_v01.json").is_file())

    def test_an_occupied_version_is_never_overwritten(self):
        """T29 — a versão que já existe fica como está, byte a byte."""
        (self.eng / "_coverage").mkdir()
        taken = self.eng / "_coverage" / "coverage_v01.json"
        taken.write_text(json.dumps(hydrate(self.eng, load(RECON)), ensure_ascii=False),
                         encoding="utf-8")
        before = taken.read_bytes()
        out = C["finalize"](self.eng, self.draft())
        self.assertEqual(out["version"], "v02")
        self.assertEqual(taken.read_bytes(), before)

    def test_concurrent_finalizes_get_distinct_versions(self):
        drafts = [self.draft() for _ in range(1)]
        results = []
        lock = threading.Lock()

        def run():
            try:
                out = C["finalize"](self.eng, drafts[0])
            except Exception as exc:                                # noqa: BLE001
                out = {"published": False, "error": repr(exc)}
            with lock:
                results.append(out)

        threads = [threading.Thread(target=run) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        versions = [r.get("version") for r in results if r.get("published")]
        self.assertEqual(len(versions), len(set(versions)),
                         "duas finalizações concorrentes ficaram com a mesma versão: %s"
                         % versions)
        files = sorted(p.name for p in (self.eng / "_coverage").glob("*.json"))
        self.assertEqual(len(files), len(set(files)))

    def test_a_stale_draft_is_refused_and_nothing_is_published(self):
        draft = self.draft()
        (self.eng / "inputs" / "nova-fonte.txt").write_text("fonte nova\n",
                                                            encoding="utf-8")
        out = C["finalize"](self.eng, draft)
        self.assertFalse(out["published"])
        self.assertEqual(out["reason"], "stale")
        self.assertFalse((self.eng / "_coverage").exists()
                         and list((self.eng / "_coverage").glob("*.json")))

    def test_the_old_digests_are_never_replaced_by_the_current_ones(self):
        """A recusa central: republicar com os digests de agora carimbaria como revista
        uma fonte que mudou sem ser relida."""
        draft_path = self.draft()
        declared = json.loads(draft_path.read_text(encoding="utf-8"))["basis"]
        (self.eng / "answers.md").write_text(
            (self.eng / "answers.md").read_text(encoding="utf-8") + "\n## U-099 — nova\n",
            encoding="utf-8")
        out = C["finalize"](self.eng, draft_path)
        self.assertFalse(out["published"])
        after = json.loads(draft_path.read_text(encoding="utf-8"))["basis"]
        self.assertEqual(after, declared, "o rascunho não pode ser reescrito")

    def test_an_invalid_draft_is_refused_with_its_diagnostics(self):
        out = C["finalize"](self.eng, self.draft("rec-neg-schema-invalid"))
        self.assertFalse(out["published"])
        self.assertEqual(out["reason"], "schema")
        self.assertTrue(out["diagnostics"])

    def test_a_missing_draft_is_an_explicit_error(self):
        with self.assertRaises(C["CoverageError"]) as ctx:
            C["finalize"](self.eng, self.root / "nao-existe.json")
        self.assertEqual(ctx.exception.exit_code, 3)

    def test_finalize_writes_only_inside_coverage(self):
        before = manifest(self.eng, skip=("_coverage/",))
        C["finalize"](self.eng, self.draft())
        self.assertEqual(manifest(self.eng, skip=("_coverage/",)), before,
                         "`finalize` escreveu fora de `_coverage/`")

    def test_finalize_never_writes_the_su_or_the_decisions(self):
        su = (self.eng / "shared-understanding.md").read_bytes()
        dec = (self.eng / "decisions.md").read_bytes()
        C["finalize"](self.eng, self.draft())
        self.assertEqual((self.eng / "shared-understanding.md").read_bytes(), su)
        self.assertEqual((self.eng / "decisions.md").read_bytes(), dec)

    def test_the_published_version_matches_the_file_name(self):
        C["finalize"](self.eng, self.draft())
        out = C["finalize"](self.eng, self.draft())
        published = json.loads(
            (self.eng / "_coverage" / "coverage_v02.json").read_text(encoding="utf-8"))
        self.assertEqual(published["version"], "v02")
        self.assertEqual(
            C["coverage_state"](self.eng, "reconciliation")["contract_validity"], "valid")

    def test_a_review_with_known_gaps_can_still_be_published(self):
        """Uma revisão com lacunas é evidência válida de incompletude, não lixo."""
        C["finalize"](self.eng, self.draft())
        out = C["finalize"](self.eng, self.draft("rec-v02-blueprint-missing"))
        self.assertTrue(out["published"], out.get("message"))
        self.assertEqual(out["result"]["coverage"], "gaps")

    def test_the_markdown_projection_is_written_next_to_the_json(self):
        out = C["finalize"](self.eng, self.draft())
        md = (self.eng / out["md"]).read_text(encoding="utf-8")
        self.assertIn("**Não é autoridade**", md)
        self.assertIn("reconciliation", md)


class FinalizeUnderChange(Base):
    """P2 e P3 — o que acontece quando o mundo se mexe a meio da publicação.

    A reserva é exclusiva, mas entre reservar e escrever há uma janela. O que lá entra
    tem de ser apanhado pela MESMA definição de «a base mudou» que recusa um rascunho
    stale à entrada — e o alvo conta, embora não esteja no manifesto (é um alvo, §6.3)."""

    def _hook_second_basis(self, mutate):
        """Corre `mutate()` entre a reserva e a verificação final de `finalize`.

        `compute_basis` é chamado duas vezes; a segunda é a de saída. O gancho vai aos
        globais REAIS do módulo — os do `runpy` são uma cópia e não afectam o motor."""
        G = C["finalize"].__globals__
        original = G["compute_basis"]
        state = {"n": 0}

        def hooked(*a, **k):
            state["n"] += 1
            if state["n"] == 2:
                mutate()
            return original(*a, **k)

        G["compute_basis"] = hooked
        self.addCleanup(lambda: G.__setitem__("compute_basis", original))
        return original

    def test_touching_the_target_during_finalize_refuses_the_publication(self):
        """O defeito: o alvo não está no manifesto, e a comparação de saída só olhava
        para o manifesto — publicava-se uma revisão já `stale`."""
        self.install(RECON)
        draft = self.draft("rec-v02-blueprint-missing")
        bp = self.eng / BP01

        self._hook_second_basis(lambda: bp.write_text(
            bp.read_text(encoding="utf-8") + "\n# tocado a meio\n", encoding="utf-8"))
        out = C["finalize"](self.eng, draft)
        self.assertFalse(out["published"],
                         "publicou uma revisão cujo alvo mudou durante a operação")
        self.assertEqual(out["reason"], "changed-during")
        self.assertEqual(sorted(p.name for p in (self.eng / "_coverage").iterdir()),
                         ["coverage_v01.json"],
                         "a reserva tinha de ter sido desfeita")

    def test_touching_a_source_during_finalize_refuses_the_publication(self):
        draft = self.draft()
        answers = self.eng / "answers.md"
        self._hook_second_basis(lambda: answers.write_text(
            answers.read_text(encoding="utf-8") + "\n## U-099 — nova\n",
            encoding="utf-8"))
        out = C["finalize"](self.eng, draft)
        self.assertFalse(out["published"])
        self.assertEqual(out["reason"], "changed-during")
        self.assertFalse(list((self.eng / "_coverage").glob("*.json")))

    def _hook_recheck(self, mutate, on_call=2):
        """Corre `mutate()` depois da n-ésima chamada a `finalize_recheck`.

        A chamada 1 é a de entrada; a 2 é a de saída. Mexer depois da 2 cai na janela
        entre a verificação final e o veredicto que vai ser reportado."""
        G = C["finalize"].__globals__
        original = G["finalize_recheck"]
        state = {"n": 0}

        def hooked(*a, **k):
            out = original(*a, **k)
            state["n"] += 1
            if state["n"] == on_call:
                mutate()
            return out

        G["finalize_recheck"] = hooked
        self.addCleanup(lambda: G.__setitem__("finalize_recheck", original))

    def test_a_change_after_the_last_check_still_undoes_the_publication(self):
        """P2b — há sempre uma janela entre uma verificação e a linha seguinte.

        O que não pode haver é publicar **depois** de a ter visto fechada: o veredicto
        final é o mesmo que ia ser reportado, e se ele diz `stale`, a reserva desfaz-se."""
        self.install(RECON)
        draft = self.draft("rec-v02-blueprint-missing")
        bp = self.eng / BP01
        self._hook_recheck(lambda: bp.write_text(
            bp.read_text(encoding="utf-8") + "\n# tocado depois do recheck\n",
            encoding="utf-8"))
        out = C["finalize"](self.eng, draft)
        self.assertFalse(out["published"],
                         "publicou uma revisão que o próprio veredicto final dava como "
                         "desactualizada")
        self.assertEqual(out["reason"], "changed-during")
        self.assertEqual(sorted(p.name for p in (self.eng / "_coverage").iterdir()),
                         ["coverage_v01.json"])

    def test_the_refusal_carries_the_verdict_that_caused_it(self):
        self.install(RECON)
        bp = self.eng / BP01
        self._hook_recheck(lambda: bp.write_text(
            bp.read_text(encoding="utf-8") + "\n# x\n", encoding="utf-8"))
        out = C["finalize"](self.eng, self.draft("rec-v02-blueprint-missing"))
        self.assertEqual(out["result"]["freshness"], "stale")
        self.assertIn("atualidade", out["message"])

    def test_a_published_review_is_never_published_stale(self):
        """A propriedade, dita de uma vez: se publicou, está actual."""
        out = C["finalize"](self.eng, self.draft())
        self.assertTrue(out["published"], out.get("message"))
        self.assertEqual(out["result"]["freshness"], "current")

    def test_each_concurrent_publication_reports_on_itself(self):
        """P3 — a finalização avalia o registo que acabou de publicar, não «o mais
        recente da etapa»: com concorrência, o mais recente é o da outra."""
        draft = self.draft()
        results = []
        lock = threading.Lock()

        def run():
            try:
                out = C["finalize"](self.eng, draft)
            except Exception as exc:                                # noqa: BLE001
                out = {"published": False, "error": repr(exc)}
            with lock:
                results.append(out)

        threads = [threading.Thread(target=run) for _ in range(6)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        published = [r for r in results if r.get("published")]
        self.assertTrue(published, "nenhuma publicação correu: %s" % results)
        for r in published:
            self.assertEqual((r["result"].get("record") or {}).get("version"),
                             r["version"],
                             "a revisão %s foi avaliada contra outro registo"
                             % r["version"])
            self.assertEqual(r["result"]["record"]["file"], r["json"])

    def test_each_markdown_names_its_own_version(self):
        a = C["finalize"](self.eng, self.draft())
        b = C["finalize"](self.eng, self.draft())
        for out in (a, b):
            md = (self.eng / out["md"]).read_text(encoding="utf-8")
            self.assertIn("coverage_%s.json" % out["version"], md)
            other = "v02" if out["version"] == "v01" else "v01"
            self.assertNotIn("coverage_%s.json" % other, md,
                             "o relatório de %s fala de %s" % (out["version"], other))


# ============================================================ o relatório não manda

class TheReportIsNotAuthority(Base):
    """T40 — editar o Markdown à mão não muda nada, e não produz aprovação nenhuma."""

    def test_editing_the_markdown_changes_no_verdict(self):
        C["finalize"](self.eng, self.draft())          # a reconciliação que o desenho cita
        out = C["finalize"](self.eng, self.draft("rec-v02-blueprint-missing"))
        self.assertTrue(out["published"], out.get("message"))
        md = self.eng / out["md"]
        md.write_text(md.read_text(encoding="utf-8")
                      .replace("gaps", "complete")
                      .replace("não", "sim") + "\n\nAPROVADO POR TODOS\n",
                      encoding="utf-8")
        res = C["coverage_state"](self.eng, "blueprint", {"file": BP01})
        self.assertEqual(res["coverage"], "gaps")
        self.assertFalse(res["eligible"])

    def test_the_json_is_untouched_by_editing_the_markdown(self):
        out = C["finalize"](self.eng, self.draft())
        before = (self.eng / out["json"]).read_bytes()
        md = self.eng / out["md"]
        md.write_text("mentira\n", encoding="utf-8")
        C["coverage_state"](self.eng, "reconciliation")
        self.assertEqual((self.eng / out["json"]).read_bytes(), before)

    def test_report_regenerates_the_projection_from_the_json(self):
        out = C["finalize"](self.eng, self.draft())
        md = self.eng / out["md"]
        original = md.read_text(encoding="utf-8")
        md.write_text("mentira\n", encoding="utf-8")
        r = cli("report", "--engagement", str(self.eng), "--stage", "reconciliation")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("**Não é autoridade**", r.stdout)
        self.assertEqual(md.read_text(encoding="utf-8"), "mentira\n",
                         "`report` imprime; não reescreve o ficheiro")
        self.assertIn("Veredictos", original)


class PreviewADraft(Base):
    """`report --record` avalia o registo indicado, não o publicado.

    Sem isto, a página mostrava as obrigações de um rascunho debaixo dos veredictos de
    outro registo — ou de nenhum — e era a pior mistura possível."""

    def test_a_clean_draft_previews_as_current_and_complete(self):
        draft = self.draft()
        r = cli("report", "--engagement", str(self.eng), "--record", str(draft))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("completa (complete)", r.stdout)
        self.assertIn("produce_blueprint", r.stdout)

    def test_previewing_a_draft_publishes_nothing(self):
        before = manifest(self.eng)
        cli("report", "--engagement", str(self.eng), "--record", str(self.draft()))
        self.assertEqual(manifest(self.eng), before)
        self.assertFalse((self.eng / "_coverage").is_dir())

    def test_a_draft_whose_base_moved_previews_as_stale(self):
        draft = self.draft()
        (self.eng / "inputs" / "nova.txt").write_text("x\n", encoding="utf-8")
        r = cli("report", "--engagement", str(self.eng), "--record", str(draft), "--json")
        self.assertEqual(r.returncode, 4)
        self.assertEqual(json.loads(r.stdout)["freshness"], "stale")

    def test_a_draft_is_not_judged_by_a_file_name_it_does_not_have(self):
        """A `version` do rascunho não se compara com o nome do temporário."""
        draft = self.draft()
        r = cli("report", "--engagement", str(self.eng), "--record", str(draft), "--json")
        self.assertEqual(json.loads(r.stdout)["contract_validity"], "valid")

    def test_a_record_that_does_not_exist_exits_three(self):
        r = cli("report", "--engagement", str(self.eng), "--record",
                str(self.root / "nao-existe.json"))
        self.assertEqual(r.returncode, 3)


# ============================================================ o engagement real

class TheRealEngagementIsUntouched(unittest.TestCase):
    """O motor corre contra o engagement real — em leitura, e prova-se."""

    ENGAGEMENTS = ROOT / "projects"

    def setUp(self):
        mounted = [p for p in self.ENGAGEMENTS.glob("*")
                   if (p / "_state.json").is_file()] if self.ENGAGEMENTS.is_dir() else []
        if not mounted:
            self.skipTest("engagements não montados neste checkout")
        self.eng = mounted[0]

    def test_inventory_and_check_leave_it_byte_identical(self):
        before = manifest(self.eng)
        cli("inventory", "--engagement", str(self.eng))
        cli("check", "--engagement", str(self.eng), "--stage", "reconciliation")
        self.assertEqual(manifest(self.eng), before)

    def test_a_real_engagement_without_records_is_not_evaluated(self):
        if (self.eng / "_coverage").is_dir() and \
                list((self.eng / "_coverage").glob("coverage_v*.json")):
            self.skipTest("este engagement já tem registos de cobertura")
        res = C["coverage_state"](self.eng, "reconciliation")
        self.assertEqual(res["coverage"], "not_evaluated")
        self.assertFalse(res["eligible"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
