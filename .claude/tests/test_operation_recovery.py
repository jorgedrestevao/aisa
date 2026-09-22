# -*- coding: utf-8 -*-
"""W01-W08 — escrita, falha, concorrência e recuperação (P2).

Cada classe é um caso de `validation/cases.json`. As interrupções são reais: o processo
é morto entre publicações, não simulado com uma flag."""
import json
import os
import runpy
import shutil
import subprocess
import sys
import tempfile
import textwrap
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OP_PY = ROOT / "library" / "kernel" / "tools" / "operation.py"
O = runpy.run_path(str(OP_PY))


def new_eng(tmp, files=None):
    eng = Path(tmp) / "eng"
    eng.mkdir(parents=True, exist_ok=True)
    for rel, body in (files or {}).items():
        p = eng / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8", newline="\n")
    return eng


WS = {"shared-understanding.md": "# SU\n\n| C-001 | Confirmed |\n",
      "answers.md": "# Respostas\n\n## A-001\n",
      "_state.json": '{"phase":"discovery","round":"R-01"}\n'}


class W01_CrashAntesDaIntencao(unittest.TestCase):
    """Interromper ANTES da publicação -> artefactos de negócio inalterados."""

    def test_a_rejected_base_touches_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp, {"shared-understanding.md": "original\n"})
            before = (eng / "shared-understanding.md").read_text(encoding="utf-8")
            with self.assertRaises(O["OperationError"]) as ctx:
                O["run"](eng, "op-1", {"shared-understanding.md": "novo\n"},
                         expected={"shared-understanding.md": "base-que-nao-e-a-real"})
            self.assertEqual(ctx.exception.code, "BASE_CHANGED")
            self.assertEqual((eng / "shared-understanding.md").read_text(encoding="utf-8"), before)
            self.assertIsNone(O["read_pending"](eng), "ficou pendência de uma operação recusada")

    def test_rejection_leaves_the_gate_open(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp, {"shared-understanding.md": "original\n"})
            try:
                O["run"](eng, "op-1", {"shared-understanding.md": "x\n"},
                         expected={"shared-understanding.md": "errado"})
            except O["OperationError"]:
                pass
            self.assertTrue(O["gate_open"](eng))


class W02_CrashEntreEscritas(unittest.TestCase):
    """Matar o processo APÓS cada publicação -> pendência visível, sem sucesso,
    recuperação completa e consistente."""

    SCRIPT = textwrap.dedent("""
        import runpy, sys, os
        O = runpy.run_path(r"{op}")
        eng = r"{eng}"
        def sabotado(e, intent):
            done = []
            for rel in sorted(intent["after"]):
                src = os.path.join(e, intent["staging"], rel.replace("/", "__"))
                dst = os.path.join(e, rel)
                os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
                O["_atomic_write"](dst, open(src, encoding="utf-8").read())
                done.append(rel)
                if len(done) == {after_n}:
                    os._exit(9)          # morte real, a meio da publicação
            return done
        O["run"].__globals__["_publish"] = sabotado   # runpy devolve CÓPIA do namespace
        O["run"](eng, "op-crash", {ws})
    """)

    def _crash_after(self, n):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)   # mkdtemp nao se limpa sozinho
        eng = new_eng(tmp, {k: "antigo\n" for k in WS})
        code = self.SCRIPT.format(op=OP_PY, eng=eng, after_n=n, ws=repr(WS))
        p = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=60)
        return tmp, eng, p

    def test_pending_is_visible_after_a_crash_mid_publish(self):
        for n in (1, 2):
            with self.subTest(publicados=n):
                tmp, eng, p = self._crash_after(n)
                self.assertNotEqual(p.returncode, 0, "o processo não morreu")
                st = O["status"](eng)
                self.assertEqual(st["state"], O["PENDING_OPERATION"],
                                 "uma publicação a meio não deixou pendência visível")
                self.assertFalse(O["gate_open"](eng), "o gate abriu sobre estado misto")

    def test_no_success_is_declared(self):
        tmp, eng, p = self._crash_after(1)
        self.assertIsNone(O["read_receipt"](eng, "op-crash"),
                          "há recibo de uma operação que não terminou")

    def test_recovery_completes_the_whole_set(self):
        tmp, eng, p = self._crash_after(1)
        res = O["recover"](eng)
        self.assertEqual(res["result"], "rolled_forward")
        for rel, body in WS.items():
            self.assertEqual((eng / rel).read_text(encoding="utf-8"), body,
                             "`{}` não ficou consistente depois da recuperação".format(rel))
        self.assertTrue(O["gate_open"](eng))


class W03_CrashAposCommit(unittest.TestCase):
    """Matar antes da resposta; repetir o operation_id -> mesmo resultado, sem nova linha."""

    def test_replaying_the_same_request_returns_the_same_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            first = O["run"](eng, "op-idem", WS)
            again = O["run"](eng, "op-idem", WS)
        self.assertTrue(again.get("replayed"), "a repetição não foi reconhecida")
        self.assertEqual(first["request_hash"], again["request_hash"])
        self.assertEqual(first["revision"], again["revision"])

    def test_replaying_does_not_write_again(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            O["run"](eng, "op-idem", WS)
            stamps = {rel: (eng / rel).stat().st_mtime_ns for rel in WS}
            time.sleep(0.01)
            O["run"](eng, "op-idem", WS)
            after = {rel: (eng / rel).stat().st_mtime_ns for rel in WS}
        self.assertEqual(stamps, after, "a repetição reescreveu os ficheiros")

    def test_same_id_with_a_different_payload_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            O["run"](eng, "op-idem", WS)
            with self.assertRaises(O["OperationError"]) as ctx:
                O["run"](eng, "op-idem", dict(WS, **{"answers.md": "outra coisa\n"}))
        self.assertEqual(ctx.exception.code, "RECEIPT_MISMATCH")


class W04_Concorrencia(unittest.TestCase):
    """Dois escritores da MESMA revisão -> um aplica, o outro reavalia. Nada se perde."""

    def test_the_second_writer_is_refused_on_a_stale_base(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp, {"shared-understanding.md": "base\n"})
            base = {"shared-understanding.md": O["digest"](eng / "shared-understanding.md")}
            O["run"](eng, "op-a", {"shared-understanding.md": "A escreveu\n"}, expected=base)
            with self.assertRaises(O["OperationError"]) as ctx:
                O["run"](eng, "op-b", {"shared-understanding.md": "B escreveu\n"}, expected=base)
        self.assertEqual(ctx.exception.code, "BASE_CHANGED")

    def test_the_first_write_survives_intact(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp, {"shared-understanding.md": "base\n"})
            base = {"shared-understanding.md": O["digest"](eng / "shared-understanding.md")}
            O["run"](eng, "op-a", {"shared-understanding.md": "A escreveu\n"}, expected=base)
            try:
                O["run"](eng, "op-b", {"shared-understanding.md": "B escreveu\n"}, expected=base)
            except O["OperationError"]:
                pass
            self.assertEqual((eng / "shared-understanding.md").read_text(encoding="utf-8"),
                             "A escreveu\n", "a actualização de A perdeu-se")

    def test_b_succeeds_once_it_re_reads_the_new_base(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp, {"shared-understanding.md": "base\n"})
            b0 = {"shared-understanding.md": O["digest"](eng / "shared-understanding.md")}
            O["run"](eng, "op-a", {"shared-understanding.md": "A\n"}, expected=b0)
            b1 = {"shared-understanding.md": O["digest"](eng / "shared-understanding.md")}
            O["run"](eng, "op-b", {"shared-understanding.md": "A+B\n"}, expected=b1)
            self.assertEqual((eng / "shared-understanding.md").read_text(encoding="utf-8"), "A+B\n")


class W05_LeitorConcorrente(unittest.TestCase):
    """Ler gate/bootstrap entre publicações -> snapshot consistente OU indisponibilidade
    explícita. Mistura nunca é aceite."""

    def test_a_reader_during_pending_gets_an_explicit_refusal(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp, {k: "antigo\n" for k in WS})
            O["_atomic_write"](O["pending_path"](eng), json.dumps(
                {"intent_version": 1, "operation_id": "op-x", "request_hash": "h",
                 "owner": {}, "before": {}, "after": {"shared-understanding.md": "d"},
                 "staging": "_ops/staging/op-x"}))
            st = O["status"](eng)
            self.assertEqual(st["state"], O["PENDING_OPERATION"])
            self.assertFalse(O["gate_open"](eng))
            self.assertIn("recovery", st, "a indisponibilidade não diz como se recupera")

    def test_a_clean_engagement_reads_clean(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp, {k: "x\n" for k in WS})
            self.assertEqual(O["status"](eng)["state"], O["CLEAN"])
            self.assertTrue(O["gate_open"](eng))


class W06_Locks(unittest.TestCase):
    """Lock activo e abandonado; recuperação repetida -> sem remoção cega, idempotente."""

    def test_an_active_lock_is_not_stolen(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            mine = O["acquire"](eng)
            try:
                # um segundo pedido do MESMO processo vê o lock vivo
                with self.assertRaises(O["OperationError"]) as ctx:
                    O["acquire"](eng)
                self.assertEqual(ctx.exception.code, "LOCK_ACTIVE")
            finally:
                O["release"](eng, mine)

    def test_an_abandoned_lock_is_recovered_and_recorded(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            dead = {"pid": 999_999, "started": "1", "engagement": str(Path(eng).resolve())}
            O["_atomic_write"](O["_lock_path"](eng), json.dumps(dead))
            got = O["acquire"](eng)
            try:
                self.assertIn("recovered_from", got,
                              "o lock abandonado foi tomado sem deixar registo")
                self.assertEqual(got["recovered_from"]["pid"], 999_999)
            finally:
                O["release"](eng, got)

    def test_an_unreadable_lock_is_not_removed_blindly(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            O["_lock_path"](eng).write_text("isto não é json", encoding="utf-8")
            try:
                with self.assertRaises(O["OperationError"]) as ctx:
                    O["acquire"](eng)
                self.assertEqual(ctx.exception.code, "LOCK_UNREADABLE")
                self.assertTrue(O["_lock_path"](eng).exists(), "removeu um lock que não leu")
            finally:
                O["_lock_path"](eng).unlink(missing_ok=True)

    def test_recovery_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            O["run"](eng, "op-1", WS)
            a = O["recover"](eng)
            b = O["recover"](eng)
        self.assertEqual(a["result"], "nothing_pending")
        self.assertEqual(b["result"], "nothing_pending")

    def test_release_only_removes_your_own_lock(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            mine = O["acquire"](eng)
            O["release"](eng, {"pid": 1, "started": "outro"})
            self.assertTrue(O["_lock_path"](eng).exists(), "libertou o lock de outro")
            O["release"](eng, mine)
            self.assertFalse(O["_lock_path"](eng).exists())


class W07_FalhaDeIO(unittest.TestCase):
    """Espaço/permissões e staging danificado -> sem falso sucesso, evidência preservada."""

    def test_damaged_staging_refuses_recovery_without_inventing(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp, {k: "antigo\n" for k in WS})
            intent = {"intent_version": 1, "operation_id": "op-dano", "request_hash": "h",
                      "owner": {}, "before": {k: O["digest"](eng / k) for k in WS},
                      "after": {k: "f" * 64 for k in WS},
                      "staging": "_ops/staging/op-dano"}
            (eng / "_ops" / "staging" / "op-dano").mkdir(parents=True)
            O["_atomic_write"](O["pending_path"](eng), json.dumps(intent))
            with self.assertRaises(O["OperationError"]) as ctx:
                O["recover"](eng)
        self.assertEqual(ctx.exception.code, "STAGING_INCOMPLETE")

    def test_the_pending_marker_survives_a_failed_recovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp, {k: "antigo\n" for k in WS})
            intent = {"intent_version": 1, "operation_id": "op-dano", "request_hash": "h",
                      "owner": {}, "before": {k: O["digest"](eng / k) for k in WS},
                      "after": {k: "f" * 64 for k in WS},
                      "staging": "_ops/staging/op-dano"}
            (eng / "_ops" / "staging" / "op-dano").mkdir(parents=True)
            O["_atomic_write"](O["pending_path"](eng), json.dumps(intent))
            try:
                O["recover"](eng)
            except O["OperationError"]:
                pass
            self.assertIsNotNone(O["read_pending"](eng),
                                 "a pendência sumiu depois de uma recuperação falhada")
            self.assertFalse(O["gate_open"](eng))

    def test_an_unsupported_intent_version_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            O["_atomic_write"](O["pending_path"](eng),
                               json.dumps({"intent_version": 99, "operation_id": "x"}))
            with self.assertRaises(O["OperationError"]) as ctx:
                O["recover"](eng)
        self.assertEqual(ctx.exception.code, "INTENT_VERSION")


class W08_ConflitoExterno(unittest.TestCase):
    """Ficheiro alterado por terceiro durante a pendência -> recusa SEM overwrite,
    conflito e hashes preservados."""

    def _pending_with_third_state(self, tmp):
        eng = new_eng(tmp, {"shared-understanding.md": "antigo\n"})
        stg = eng / "_ops" / "staging" / "op-3"
        stg.mkdir(parents=True)
        (stg / "shared-understanding.md").write_text("novo\n", encoding="utf-8")
        intent = {"intent_version": 1, "operation_id": "op-3", "request_hash": "h",
                  "owner": {},
                  "before": {"shared-understanding.md": O["digest"](eng / "shared-understanding.md")},
                  "after": {"shared-understanding.md":
                            __import__("hashlib").sha256(b"novo\n").hexdigest()},
                  "staging": "_ops/staging/op-3"}
        O["_atomic_write"](O["pending_path"](eng), json.dumps(intent))
        # terceiro escreve por fora
        (eng / "shared-understanding.md").write_text("um terceiro mexeu\n", encoding="utf-8")
        return eng

    def test_third_state_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._pending_with_third_state(tmp)
            with self.assertRaises(O["OperationError"]) as ctx:
                O["recover"](eng)
        self.assertEqual(ctx.exception.code, "THIRD_STATE")

    def test_the_third_partys_bytes_are_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._pending_with_third_state(tmp)
            try:
                O["recover"](eng)
            except O["OperationError"]:
                pass
            self.assertEqual((eng / "shared-understanding.md").read_text(encoding="utf-8"),
                             "um terceiro mexeu\n", "a recuperação sobrescreveu bytes de terceiro")

    def test_the_conflict_reports_all_three_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._pending_with_third_state(tmp)
            try:
                O["recover"](eng)
                self.fail("não recusou")
            except O["OperationError"] as exc:
                p = exc.detail["paths"][0]
                for k in ("actual", "before", "after"):
                    self.assertTrue(p.get(k), "o conflito não preservou o hash `{}`".format(k))

    def test_reusing_an_id_with_a_different_payload_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            O["run"](eng, "op-r", {"answers.md": "a\n"})
            with self.assertRaises(O["OperationError"]) as ctx:
                O["run"](eng, "op-r", {"answers.md": "b\n"})
        self.assertEqual(ctx.exception.code, "RECEIPT_MISMATCH")


if __name__ == "__main__":
    unittest.main(verbosity=2)
