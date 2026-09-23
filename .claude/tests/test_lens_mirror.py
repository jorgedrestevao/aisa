# -*- coding: utf-8 -*-
"""O que uma lente escreve, o grafo acompanha.

Sessao real de Discovery, piloto `pricing-bancas-marinha`: a SEGUNDA escrita de uma lente
na SU foi recusada pelo guarda de autoridade.

    1a escrita da lente   grafo coerente         -> allow
                          a lente acrescenta linhas a SU pela ferramenta Edit
                          on-su-change.py so regenera o dashboard — nao espelha
    2a escrita da lente   AUTHORITY_UNMIRRORED   -> DENY

Todo o endurecimento do P7.5 assumiu que as escritas de conhecimento passam pelo
coordenador (`/answer`, `resolve.py`, `migrate.py`) — e essas chamam `mirror_write_set`.
O caminho dominante do Discovery nao passa: a lente edita a SU directamente. 2585 testes
verdes nunca exercitaram «Edit de lente -> guarda na Edit seguinte».

A regra do kernel ja estava escrita — **quem escreve a autoridade escreve o espelho dela**
— e faltava-lhe um escritor. Este hook e esse escritor para o caminho Edit/Write.

O que o espelho pode resolver, e so isso: `AUTHORITY_UNMIRRORED` (linha que o grafo nao
conhece) e `AUTHORITY_DRIFT` (campo espelhado divergente). O bootstrap para por ordem —
pendencia, legacy, grafo ilegivel, integridade, desvio, linha sem no — e por isso, quando
para num dos dois ultimos, tudo o resto ja passou. Pendencia, grafo partido ou modo legacy
NAO sao deste escritor: recusa, e diz qual e a recuperacao."""
import json
import os
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "library" / "kernel" / "tools"
HOOKS = ROOT / ".claude" / "hooks"
FIX = runpy.run_path(str(ROOT / ".claude" / "tests" / "test_migration.py"))
M = runpy.run_path(str(TOOLS / "migrate.py"))
B = runpy.run_path(str(TOOLS / "bootstrap.py"))
R = runpy.run_path(str(TOOLS / "resolve.py"))
G = runpy.run_path(str(TOOLS / "graph.py"))
O = runpy.run_path(str(TOOLS / "operation.py"))

ANCORA = "| C-001 | data | Base partilhada | inicial | 2026-01-01 | organizacional | R-01 |"


def eng_migrado(tmp):
    projects = Path(tmp) / "projects"
    projects.mkdir()
    eng = Path(FIX["make"](str(projects), FIX["NOVO"]))
    M["apply"](eng)
    return projects, eng


def lente_acrescenta(eng, rid="C-050", texto="Linha nova de lente"):
    """O que a lente faz: Edit na SU, sem coordenador."""
    su = eng / "shared-understanding.md"
    t = su.read_text(encoding="utf-8")
    nova = "| {} | business | {} | acta R-02 | 2026-03-01 | organizacional | R-02 |".format(
        rid, texto)
    su.write_text(t.replace(ANCORA, ANCORA + "\n" + nova, 1), encoding="utf-8", newline="\n")
    return su


def hook(nome, projects, file_path, tool="Edit"):
    payload = {"tool_name": tool,
               "tool_input": {"file_path": str(file_path), "old_string": "x", "new_string": "y"}}
    env = dict(os.environ, AISA_ENGAGEMENTS_ROOT=str(projects))
    return subprocess.run([sys.executable, str(HOOKS / nome)], input=json.dumps(payload),
                          capture_output=True, text=True, env=env, timeout=300)


def guarda_decide(projects, su):
    return "deny" if hook("pre-authority-guard.py", projects, su).returncode == 2 else "allow"


class L1_OCicloQueRebentou(unittest.TestCase):

    def test_the_second_lens_write_is_no_longer_denied(self):
        """O erro real, ponta a ponta: escrita, hook, escrita seguinte."""
        with tempfile.TemporaryDirectory() as tmp:
            projects, eng = eng_migrado(tmp)
            su = lente_acrescenta(eng)
            p = hook("on-su-mirror.py", projects, su)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(guarda_decide(projects, su), "allow",
                             "a segunda escrita da lente continua recusada")

    def test_after_the_hook_the_kernel_is_ready(self):
        with tempfile.TemporaryDirectory() as tmp:
            projects, eng = eng_migrado(tmp)
            su = lente_acrescenta(eng)
            self.assertFalse(B["bootstrap"](eng)["ready"], "a premissa do caso caiu")
            hook("on-su-mirror.py", projects, su)
            self.assertTrue(B["bootstrap"](eng)["ready"])

    def test_many_writes_in_a_row_stay_ready(self):
        """Uma passagem tem seis lentes. Nenhuma pode bloquear a seguinte."""
        with tempfile.TemporaryDirectory() as tmp:
            projects, eng = eng_migrado(tmp)
            su = eng / "shared-understanding.md"
            for i in range(6):
                # a ordem real: o guarda (PreToolUse) decide ANTES, a escrita acontece,
                # o espelho (PostToolUse) corre DEPOIS. A primeira versao escrevia e so
                # depois perguntava ao guarda — um ciclo que o Claude Code nunca faz.
                self.assertEqual(guarda_decide(projects, su), "allow",
                                 "a escrita {} foi recusada".format(i + 1))
                lente_acrescenta(eng, rid="C-0{}".format(60 + i))
                hook("on-su-mirror.py", projects, su)
            self.assertTrue(B["bootstrap"](eng)["ready"])


class L2_OQueOEspelhoFaz(unittest.TestCase):

    def test_the_new_row_becomes_a_node(self):
        with tempfile.TemporaryDirectory() as tmp:
            _p, eng = eng_migrado(tmp)
            lente_acrescenta(eng)
            R["sync_mirror"](eng)
            ids = {n["id"] for n in G["read"](eng)["nodes"]}
        self.assertIn("C-050", ids)

    def test_a_changed_mirrored_field_is_brought_back(self):
        """A lente marca uma linha como resolvida -> desvio num campo espelhado.

        A primeira versao riscava o texto (`~~...~~ (resolved)`) e o bootstrap continuava
        pronto: so mudava `text`, que informa e nao bloqueia. O caso passava sem haver
        desvio nenhum. O marcador do kernel vive na ULTIMA celula (`detect_resolution`)."""
        with tempfile.TemporaryDirectory() as tmp:
            _p, eng = eng_migrado(tmp)
            su = eng / "shared-understanding.md"
            t = su.read_text(encoding="utf-8")
            resolvida = ANCORA.replace("| R-01 |", "| R-01 - resolved -> C-050 |")
            su.write_text(t.replace(ANCORA, resolvida, 1), encoding="utf-8", newline="\n")
            antes = [l["code"] for l in B["bootstrap"](eng)["limitations"]]
            self.assertIn("AUTHORITY_DRIFT", antes, "a premissa do caso caiu: nao ha desvio")
            R["sync_mirror"](eng)
            self.assertTrue(B["bootstrap"](eng)["ready"], B["bootstrap"](eng)["limitations"])

    def test_the_answer_history_survives(self):
        """O espelho reconstroi campos, nao o grafo: `was`, `claim` e `answered_by` ficam."""
        with tempfile.TemporaryDirectory() as tmp:
            _p, eng = eng_migrado(tmp)
            R["apply"](eng, row_id="U-001", answer_text="A equipa de dados.",
                       answered_by={"role": "dono"}, locator="answers.md#U-001")
            antes = G["read"](eng)
            lente_acrescenta(eng)
            R["sync_mirror"](eng)
            depois = G["read"](eng)
        was = lambda st: sorted((e["src"], e["dst"]) for e in st["edges"] if e["rel"] == "was")
        self.assertEqual(was(depois), was(antes), "o historico de respostas perdeu-se")
        self.assertIn("claim", {n["type"] for n in depois["nodes"]})
        self.assertTrue([n for n in depois["nodes"]
                         if (n.get("provenance") or {}).get("answered_by")])

    def test_it_goes_through_the_coordinator(self):
        """Um recibo prova que publicou pelo caminho de toda a gente, sob a mesma exclusao."""
        with tempfile.TemporaryDirectory() as tmp:
            _p, eng = eng_migrado(tmp)
            # os recibos sao FICHEIROS em `_ops/receipts/`; `rglob("*receipt*")` contava a
            # pasta e dava 1 antes e 1 depois
            recibos = lambda: sorted((eng / "_ops" / "receipts").glob("*.json"))
            antes = recibos()
            lente_acrescenta(eng)
            r = R["sync_mirror"](eng)
            depois = recibos()
        self.assertTrue(r.get("published"), "diz que espelhou e nao publicou nada")
        novos = [f.name for f in depois if f not in antes]
        self.assertEqual(len(novos), 1, "publicou sem recibo — fora do coordenador")
        self.assertTrue(novos[0].startswith("mirror-"), novos)

    def test_a_su_that_moved_under_the_read_is_not_mirrored(self):
        """A SU entra no conjunto com os bytes LIDOS para que a precondicao a cubra. Se ela
        mudar entre a leitura e o lock, publicar seria espelhar uma SU que ja nao existe.
        Simula-se a corrida devolvendo uma leitura velha."""
        with tempfile.TemporaryDirectory() as tmp:
            _p, eng = eng_migrado(tmp)
            su = eng / "shared-understanding.md"
            velha = su.read_text(encoding="utf-8")
            lente_acrescenta(eng)                    # a SU real ja e outra
            import hashlib
            leitura_velha = {"shared-understanding.md": {
                "text": velha + "\n| C-099 | data | fantasma | x | 2026-03-01 | organizacional | R-02 |\n",
                "digest": hashlib.sha256(velha.encode("utf-8")).hexdigest()}}
            # `runpy.run_path` devolve uma COPIA das globais: `R["read_base"] = ...` nao
            # chega a funcao. A primeira versao fazia isso, a funcao lia a SU verdadeira, e
            # o caso nao conseguia distinguir o codigo certo do errado. Injecta-se nas
            # globais que a funcao realmente consulta.
            g = R["sync_mirror"].__globals__
            original = g["read_base"]
            g["read_base"] = lambda eng, rels=(): leitura_velha
            try:
                with self.assertRaises(Exception) as cm:
                    R["sync_mirror"](eng)
            finally:
                g["read_base"] = original
            self.assertIn("BASE_CHANGED", str(getattr(cm.exception, "code", cm.exception)))
            ids = {n["id"] for n in G["read"](eng)["nodes"]}
        self.assertNotIn("C-099", ids, "publicou o espelho de uma SU que ja nao existia")

    def test_nothing_to_mirror_publishes_nothing(self):
        """Um espelho que nao muda nao se publica: sem recibo a mentir que o grafo mudou."""
        with tempfile.TemporaryDirectory() as tmp:
            _p, eng = eng_migrado(tmp)
            r = R["sync_mirror"](eng)
        self.assertEqual(r.get("published", []), [])
        self.assertEqual(r.get("status"), "unchanged")


class L3_OQueNaoEDesteEscritor(unittest.TestCase):

    def test_a_pending_operation_is_not_mirrored_over(self):
        """Uma pendencia e do `operation.py recover`. Espelhar por cima apagava a prova."""
        with tempfile.TemporaryDirectory() as tmp:
            _p, eng = eng_migrado(tmp)
            O["_atomic_write"](O["pending_path"](eng), json.dumps(
                {"intent_version": 1, "operation_id": "op-x", "request_hash": "h",
                 "owner": {}, "before": {}, "after": {"shared-understanding.md": "f" * 64},
                 "staging": "_ops/staging/op-x"}))
            lente_acrescenta(eng)
            r = R["sync_mirror"](eng)
        self.assertEqual(r.get("status"), "refused")
        self.assertIn("PENDING_OPERATION", r.get("blocking", []))
        self.assertTrue(r.get("recovery"), "recusou e nao disse o que fazer")

    def test_a_legacy_engagement_is_left_alone(self):
        """Sem grafo nao ha espelho a manter: isso e `migrate.py`, nao este hook."""
        with tempfile.TemporaryDirectory() as tmp:
            projects = Path(tmp) / "projects"
            projects.mkdir()
            eng = Path(FIX["make"](str(projects), FIX["NOVO"]))   # sem migrar
            su = lente_acrescenta(eng)
            p = hook("on-su-mirror.py", projects, su)
            self.assertFalse((eng / "_graph").exists(), "criou um grafo por conta propria")
            r = R["sync_mirror"](eng)
        self.assertEqual(p.returncode, 0)
        self.assertEqual(r["status"], "refused")
        self.assertIn("LEGACY_MODE", r["blocking"])
        self.assertIn("migrate.py", r["recovery"], "recusou e nao disse como migrar")

    def test_the_hook_ignores_files_that_are_not_the_su(self):
        with tempfile.TemporaryDirectory() as tmp:
            projects, eng = eng_migrado(tmp)
            lente_acrescenta(eng)
            p = hook("on-su-mirror.py", projects, eng / "frame.md")
            self.assertFalse(B["bootstrap"](eng)["ready"],
                             "espelhou numa escrita que nao era da SU")
        self.assertEqual(p.returncode, 0)

    def test_the_hook_never_blocks(self):
        """PostToolUse nao desfaz a escrita. Falhar alto, sair 0: bloquear aqui so esconde."""
        with tempfile.TemporaryDirectory() as tmp:
            projects, eng = eng_migrado(tmp)
            O["_atomic_write"](O["pending_path"](eng), json.dumps(
                {"intent_version": 1, "operation_id": "op-y", "request_hash": "h",
                 "owner": {}, "before": {}, "after": {"shared-understanding.md": "f" * 64},
                 "staging": "_ops/staging/op-y"}))
            su = lente_acrescenta(eng)
            p = hook("on-su-mirror.py", projects, su)
        self.assertEqual(p.returncode, 0)
        self.assertIn("recover", p.stderr, "recusou em silencio")


class L4_OHookEstaLigado(unittest.TestCase):

    def test_the_hook_is_registered_after_writes(self):
        d = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
        post = d.get("hooks", {}).get("PostToolUse", [])
        comandos = [h.get("command", "") for g in post for h in g.get("hooks", [])
                    if "Write" in g.get("matcher", "") or "Edit" in g.get("matcher", "")]
        self.assertTrue([c for c in comandos if "on-su-mirror.py" in c],
                        "o hook existe e ninguem o chama")

    def test_it_runs_before_the_dashboard(self):
        """O dashboard le o kernel; se correr antes do espelho, mostra 'por reconstruir'."""
        d = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
        comandos = [h.get("command", "") for g in d["hooks"]["PostToolUse"]
                    for h in g.get("hooks", [])]
        i_mirror = next(i for i, c in enumerate(comandos) if "on-su-mirror.py" in c)
        i_dash = next(i for i, c in enumerate(comandos) if "on-su-change.py" in c)
        self.assertLess(i_mirror, i_dash)


if __name__ == "__main__":
    unittest.main(verbosity=1)
