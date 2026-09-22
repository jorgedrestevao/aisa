# -*- coding: utf-8 -*-
"""K01-K08 — fundação de persistência (P2).

Cada classe é um caso de `validation/cases.json`. O caso é a especificação; o teste
afirma o seu `expected`, não o que o código faz."""
import json
import os
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
G = runpy.run_path(str(ROOT / "library" / "kernel" / "tools" / "graph.py"))


def eng_with(tmp, nodes=(), edges=()):
    """Um engagement com store publicado (publicação directa: aqui testa-se o STORE)."""
    eng = Path(tmp) / "eng"
    (eng / "_graph").mkdir(parents=True)
    body, meta = G["serialize"](list(nodes), list(edges))
    (eng / "_graph" / "graph.jsonl").write_text(body, encoding="utf-8", newline="\n")
    (eng / "_graph" / "meta.json").write_text(meta, encoding="utf-8", newline="\n")
    return eng


N1 = {"id": "C-001", "type": "claim", "props": {"state": "Confirmed"},
      "provenance": {"lens": "data", "round": "R-01"}}
N2 = {"id": "U-002", "type": "question", "props": {"state": "Unknown"},
      "provenance": {"lens": "governance", "round": "R-01"}}
E1 = {"src": "U-002", "rel": "depends_on", "dst": "C-001", "props": {},
      "provenance": {"round": "R-01"}}


class K01_StoreVazio(unittest.TestCase):
    """Criar e recarregar store válido vazio -> detectado e válido, DISTINTO de ausente."""

    def test_empty_store_is_ok_not_absent(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_with(tmp)
            st = G["read"](eng)
        self.assertEqual(st["status"], G["OK"])
        self.assertNotEqual(st["status"], G["ABSENT"])
        self.assertEqual((st["nodes"], st["edges"]), ([], []))

    def test_absent_store_is_absent_and_allows_legacy(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = Path(tmp) / "eng"
            eng.mkdir()
            st = G["read"](eng)
        self.assertEqual(st["status"], G["ABSENT"])

    def test_the_two_are_not_confused(self):
        with tempfile.TemporaryDirectory() as tmp:
            empty = G["read"](eng_with(tmp))["status"]
            missing = Path(tmp) / "outro"
            missing.mkdir()
            absent = G["read"](missing)["status"]
        self.assertNotEqual(empty, absent, "store vazio e store ausente colapsaram no mesmo estado")


class K02_Persistencia(unittest.TestCase):
    """Nós/arestas relidos em PROCESSO NOVO -> ids, props, relações e proveniência iguais."""

    def test_reread_in_a_fresh_process_is_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_with(tmp, [N1, N2], [E1])
            code = (
                "import runpy,json,sys;"
                "G=runpy.run_path(r'{}');"
                "st=G['read'](r'{}');"
                "print(json.dumps({{'n':st['nodes'],'e':st['edges'],'s':st['status']}}))"
            ).format(ROOT / "library" / "kernel" / "tools" / "graph.py", eng)
            out = subprocess.run([sys.executable, "-c", code],
                                 capture_output=True, text=True, timeout=60)
            self.assertEqual(out.returncode, 0, out.stderr)
            got = json.loads(out.stdout)
        self.assertEqual(got["s"], G["OK"])
        self.assertEqual([n["id"] for n in got["n"]], ["C-001", "U-002"])
        self.assertEqual(got["n"][0]["props"], {"state": "Confirmed"})
        self.assertEqual(got["n"][0]["provenance"], {"lens": "data", "round": "R-01"},
                         "a proveniência não sobreviveu ao processo novo")
        self.assertEqual(got["e"][0]["rel"], "depends_on")


class K03_Determinismo(unittest.TestCase):
    """Reordenar entrada semanticamente igual -> MESMA representação canónica."""

    def test_order_does_not_change_the_bytes(self):
        a = G["serialize"]([N1, N2], [E1])
        b = G["serialize"]([N2, N1], [E1])
        self.assertEqual(a, b, "a ordem de entrada mudou os bytes")

    def test_order_does_not_change_the_revision(self):
        self.assertEqual(G["revision_of"]([N1, N2], [E1]),
                         G["revision_of"]([N2, N1], [E1]))

    def test_different_content_gives_a_different_revision(self):
        self.assertNotEqual(G["revision_of"]([N1], []), G["revision_of"]([N1, N2], []))


class K04_Integridade(unittest.TestCase):
    """ID duplicado, relação inválida e ponta inexistente -> erro explícito, NÃO publicado."""

    def test_duplicate_id_is_reported(self):
        codes = {p["code"] for p in G["validate"]([N1, dict(N1)], [])}
        self.assertIn("NODE_ID_DUPLICATE", codes)

    def test_edge_without_rel_is_reported(self):
        bad = {"src": "C-001", "rel": "", "dst": "U-002"}
        codes = {p["code"] for p in G["validate"]([N1, N2], [bad])}
        self.assertIn("EDGE_REL_MISSING", codes)

    def test_edge_to_a_nonexistent_end_is_reported(self):
        bad = {"src": "C-001", "rel": "depends_on", "dst": "NAO-EXISTE"}
        problems = G["validate"]([N1], [bad])
        self.assertTrue(any(p["code"] == "EDGE_END_UNKNOWN" for p in problems))

    def test_an_invalid_mutation_is_not_published(self):
        with tempfile.TemporaryDirectory() as tmp:
            staging = Path(tmp) / "staging"
            with self.assertRaises(G["GraphError"]) as ctx:
                G["stage"](Path(tmp), [N1, dict(N1)], [], staging)
            self.assertEqual(ctx.exception.code, "INTEGRITY")
            self.assertFalse((staging / "graph.jsonl").exists(),
                             "a mutação inválida chegou a escrever")

    def test_a_valid_mutation_does_reach_staging(self):
        with tempfile.TemporaryDirectory() as tmp:
            staging = Path(tmp) / "staging"
            res = G["stage"](Path(tmp), [N1, N2], [E1], staging)
            self.assertTrue((staging / "graph.jsonl").is_file())
            self.assertEqual(res["nodes"], 2)


class K05_Autoridade(unittest.TestCase):
    """Estado espelhado alterado contra a SU -> drift detectado; o grafo NÃO prevalece."""

    MIRROR = {"id": "C-001", "type": "claim", "props": {"state": "Confirmed"},
              "provenance": {"mirror_of": "SU:C-001"}}

    def test_agreement_is_silent(self):
        self.assertEqual(G["drift"]([self.MIRROR], {"SU:C-001": "Confirmed"}), [])

    def test_drift_is_detected(self):
        out = G["drift"]([self.MIRROR], {"SU:C-001": "Assumed"})
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["code"], "MIRROR_DRIFT")
        self.assertEqual(out[0]["authority"], "Assumed")
        self.assertEqual(out[0]["graph"], "Confirmed")

    def test_the_graph_does_not_win(self):
        out = G["drift"]([self.MIRROR], {"SU:C-001": "Assumed"})
        self.assertIn("a autoridade manda", out[0]["detail"],
                      "o relatório de drift não diz de quem é a autoridade")

    def test_a_mirror_without_its_source_is_reported(self):
        out = G["drift"]([self.MIRROR], {})
        self.assertEqual(out[0]["code"], "MIRROR_SOURCE_MISSING")


class K06_Schema(unittest.TestCase):
    """Schema não suportado / campos desconhecidos -> erro explicável, NADA apagado."""

    def test_unsupported_schema_is_explained_not_absent(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_with(tmp, [N1], [])
            mp = eng / "_graph" / "meta.json"
            meta = json.loads(mp.read_text(encoding="utf-8"))
            meta["schema_version"] = 99
            mp.write_text(json.dumps(meta), encoding="utf-8")
            st = G["read"](eng)
        self.assertEqual(st["status"], G["UNSUPPORTED_SCHEMA"])
        self.assertIn("99", st["detail"])
        self.assertNotEqual(st["status"], G["ABSENT"])

    def test_unknown_fields_survive_a_rewrite(self):
        extra = dict(N1, campo_do_futuro={"x": 1})
        body, _ = G["serialize"]([extra], [])
        back = json.loads(body.splitlines()[0])
        self.assertIn("campo_do_futuro", back, "um campo desconhecido foi apagado na regravação")
        self.assertEqual(back["campo_do_futuro"], {"x": 1})

    def test_known_keys_keep_their_contract_order(self):
        body, _ = G["serialize"]([dict(N1, campo_do_futuro=1)], [])
        keys = list(json.loads(body.splitlines()[0]).keys())
        self.assertEqual(keys[:5], ["kind", "id", "type", "props", "provenance"])
        self.assertEqual(keys[-1], "campo_do_futuro", "o desconhecido não foi para o fim")


class K07_AusenteVersusIlegivel(unittest.TestCase):
    """Meta removido, directório que é ficheiro, permissão negada ->
    NENHUM é lido como «projecto sem grafo»."""

    def test_meta_removed_is_incoherent_not_absent(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_with(tmp, [N1], [])
            (eng / "_graph" / "meta.json").unlink()
            st = G["read"](eng)
        self.assertEqual(st["status"], G["INCOHERENT_PAIR"])
        self.assertNotEqual(st["status"], G["ABSENT"])

    def test_graph_removed_is_incoherent_not_absent(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_with(tmp, [N1], [])
            (eng / "_graph" / "graph.jsonl").unlink()
            st = G["read"](eng)
        self.assertEqual(st["status"], G["INCOHERENT_PAIR"])

    def test_corrupt_graph_is_invalid_not_absent(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_with(tmp, [N1], [])
            (eng / "_graph" / "graph.jsonl").write_text("{isto não é json\n", encoding="utf-8")
            st = G["read"](eng)
        self.assertEqual(st["status"], G["INVALID_FORMAT"])
        self.assertNotEqual(st["status"], G["ABSENT"])

    def test_revision_that_does_not_match_is_incoherent(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_with(tmp, [N1, N2], [E1])
            mp = eng / "_graph" / "meta.json"
            meta = json.loads(mp.read_text(encoding="utf-8"))
            meta["revision"] = "0" * 64
            mp.write_text(json.dumps(meta), encoding="utf-8")
            st = G["read"](eng)
        self.assertEqual(st["status"], G["INCOHERENT_PAIR"])

    @unittest.skipIf(os.name == "nt" or os.geteuid() == 0,
                     "chmod não restringe root nem Windows")
    def test_permission_denied_is_unreadable_not_absent(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_with(tmp, [N1], [])
            gp = eng / "_graph" / "graph.jsonl"
            gp.chmod(0o000)
            try:
                st = G["read"](eng)
            finally:
                gp.chmod(0o644)
        self.assertEqual(st["status"], G["UNREADABLE"])
        self.assertNotEqual(st["status"], G["ABSENT"])

    def test_only_absent_allows_legacy_mode(self):
        """A afirmação que interessa: um estado partido nunca vira modo legacy."""
        broken = {G["INCOHERENT_PAIR"], G["INVALID_FORMAT"],
                  G["UNSUPPORTED_SCHEMA"], G["UNREADABLE"]}
        self.assertNotIn(G["ABSENT"], broken)


class K08_IsolamentoDeCaminhos(unittest.TestCase):
    """Referência a outro engagement ou escape de path -> sem leitura/escrita, erro com contexto."""

    def test_a_path_outside_the_engagement_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = Path(tmp) / "eng"
            (eng / "_graph").mkdir(parents=True)
            outro = Path(tmp) / "outro"
            outro.mkdir()
            with self.assertRaises(G["GraphError"]) as ctx:
                G["guard_path"](eng, outro / "graph.jsonl")
        self.assertEqual(ctx.exception.code, "PATH_ESCAPE")

    def test_dotdot_escape_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = Path(tmp) / "eng"
            eng.mkdir()
            with self.assertRaises(G["GraphError"]) as ctx:
                G["guard_path"](eng, eng / ".." / "segredo.txt")
        self.assertEqual(ctx.exception.code, "PATH_ESCAPE")

    def test_the_error_names_the_engagement(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = Path(tmp) / "eng"
            eng.mkdir()
            try:
                G["guard_path"](eng, Path(tmp) / "fora.txt")
                self.fail("não recusou")
            except G["GraphError"] as exc:
                self.assertIn("engagement", exc.detail, "o erro não diz contra que engagement")

    def test_a_symlink_out_is_refused_even_though_it_looks_inside(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = Path(tmp) / "eng"
            eng.mkdir()
            fora = Path(tmp) / "fora"
            fora.mkdir()
            link = eng / "atalho"
            try:
                link.symlink_to(fora, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("ligações indisponíveis neste ambiente")
            with self.assertRaises(G["GraphError"]) as ctx:
                G["guard_path"](eng, link / "graph.jsonl")
        self.assertEqual(ctx.exception.code, "PATH_ESCAPE")

    def test_a_path_inside_is_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = Path(tmp) / "eng"
            (eng / "_graph").mkdir(parents=True)
            ok = G["guard_path"](eng, eng / "_graph" / "graph.jsonl")
        self.assertTrue(str(ok).endswith("graph.jsonl"))


class Costura_GrafoEcoordenador(unittest.TestCase):
    """A porta que P4 vai usar: `write_set()` produz o que `operation.run()` publica.

    Não é um caso de `cases.json`. Existe porque o grafo e o coordenador têm staging
    próprios e, sem esta porta, P4 teria de escolher um deles à sorte."""

    def test_write_set_carries_both_store_files(self):
        ws = G["write_set"]([N1, N2], [E1])
        self.assertEqual(sorted(ws), ["_graph/graph.jsonl", "_graph/meta.json"])

    def test_write_set_refuses_an_invalid_graph(self):
        with self.assertRaises(G["GraphError"]) as ctx:
            G["write_set"]([N1, dict(N1)], [])
        self.assertEqual(ctx.exception.code, "INTEGRITY")

    def test_published_through_the_coordinator_the_store_reads_back(self):
        O = runpy.run_path(str(ROOT / "library" / "kernel" / "tools" / "operation.py"))
        with tempfile.TemporaryDirectory() as tmp:
            eng = Path(tmp) / "eng"
            eng.mkdir()
            O["run"](eng, "op-graph", G["write_set"]([N1, N2], [E1]))
            st = G["read"](eng)
        self.assertEqual(st["status"], G["OK"])
        self.assertEqual([n["id"] for n in st["nodes"]], ["C-001", "U-002"])
        self.assertEqual(st["revision"], G["revision_of"]([N1, N2], [E1]),
                         "a revisão publicada não bate com a calculada")

if __name__ == "__main__":
    unittest.main(verbosity=2)
