# -*- coding: utf-8 -*-
"""W2 — o guarda que impõe bootstrap antes de escrever numa autoridade (P7.5).

Todos os casos correm o hook em PROCESSO REAL, com o payload que o harness lhe entrega.
`ACCEPTANCE.md` §1 é explícita — «Um teste de estrutura de prompts é insuficiente para
provar comportamento de runtime» — logo nenhum teste aqui lê o `SKILL.md` de coisa nenhuma
à procura de uma frase.

O que se afirma, caso a caso: o guarda deixa passar o que não é autoridade, recusa o que é
autoridade sobre estado por reconstruir, e não se deixa contornar pela forma como o caminho
foi escrito."""
import json
import os
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / ".claude" / "hooks" / "pre-authority-guard.py"
TOOLS = ROOT / "library" / "kernel" / "tools"
G = runpy.run_path(str(TOOLS / "graph.py"))
O = runpy.run_path(str(TOOLS / "operation.py"))

SU = "shared-understanding.md"
CABECA = """> Fase actual: Discovery

## Confirmed

| id | lens | claim | evidência | verificado_em | validade | ronda |
|---|---|---|---|---|---|---|
| C-001 | data | facto | fonte: inicial | 2026-01-01 | organizacional | R-01 |
"""


def engagement(base: Path, nome="eng", com_grafo=True):
    eng = base / nome
    eng.mkdir(parents=True, exist_ok=True)
    (eng / "_state.json").write_text('{"phase":"discovery","round":"R-01"}\n',
                                     encoding="utf-8", newline="\n")
    (eng / SU).write_text(CABECA, encoding="utf-8", newline="\n")
    (eng / "decisions.md").write_text("# Decisions\n", encoding="utf-8", newline="\n")
    (eng / "answers.md").write_text("# Respostas\n", encoding="utf-8", newline="\n")
    if com_grafo:
        # `mirror_of` nao e decoracao: e o que declara que este no ESPELHA aquela linha.
        # O `drift` so olha para nos que o tenham, e desde F05/F08 o bootstrap tambem
        # recusa uma linha da autoridade sem no que a espelhe. Sem isto, a fixture dizia
        # ter grafo e nao espelhava nada — e o guarda recusava com razao.
        nodes = [{"id": "C-001", "type": "su-row",
                  "props": {"state": "Confirmed", "text": "facto", "resolved": False,
                            "criticidade": ""},
                  "provenance": {"mirror_of": "SU:C-001"}}]
        body, meta = G["serialize"](nodes, [])
        (eng / "_graph").mkdir(exist_ok=True)
        (eng / "_graph" / "graph.jsonl").write_text(body, encoding="utf-8", newline="\n")
        (eng / "_graph" / "meta.json").write_text(meta, encoding="utf-8", newline="\n")
    return eng


def corre(payload, base=None, modo=None):
    """O hook em processo real, como o harness o invoca."""
    env = dict(os.environ)
    if base is not None:
        env["AISA_ENGAGEMENTS_ROOT"] = str(base)
    if modo is not None:
        env["AISA_GUARD_MODE"] = modo
    else:
        env.pop("AISA_GUARD_MODE", None)
    return subprocess.run([sys.executable, str(HOOK)], input=json.dumps(payload),
                          capture_output=True, text=True, env=env)


def escrita(caminho, tool="Write"):
    return {"tool_name": tool, "tool_input": {"file_path": str(caminho)}}


def negou(p):
    if p.returncode != 2:
        return False
    try:
        saida = json.loads(p.stderr.strip().splitlines()[-1])
    except (ValueError, IndexError):
        return False
    return (saida.get("hookSpecificOutput", {}).get("permissionDecision") == "deny")


class W2a_DeixaPassarOQueNaoEAutoridade(unittest.TestCase):
    """Um guarda que bloqueia tudo não é um guarda, é uma avaria."""

    def test_a_derived_artefact_is_not_an_authority(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            eng = engagement(base, com_grafo=False)      # bootstrap em modo legacy
            for rel in ("_render/estimate_v01.md", "_simulation/x.md", "story.md",
                        "_capture/evidence-index.md"):
                p = corre(escrita(eng / rel), base)
                self.assertEqual(p.returncode, 0,
                                 "{} é derivado, não autoridade: {}".format(rel, p.stderr))

    def test_a_file_outside_any_engagement_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            engagement(base)
            p = corre(escrita(Path(tmp) / "solto" / "decisions.md"), base)
        self.assertEqual(p.returncode, 0, "fora de `projects/` não é autoridade de ninguém")

    def test_an_authority_named_file_at_the_root_is_not_an_engagement(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            base.mkdir(exist_ok=True)
            p = corre(escrita(base / "decisions.md"), base)
        self.assertEqual(p.returncode, 0, "um ficheiro solto na raiz não tem engagement")

    def test_a_tool_that_is_not_write_or_edit_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            eng = engagement(base)
            O["_atomic_write"](O["pending_path"](eng), json.dumps({"operation_id": "x"}))
            for tool in ("Read", "Bash", "Grep", "Skill"):
                p = corre(escrita(eng / SU, tool=tool), base)
                self.assertEqual(p.returncode, 0, "o guarda é sobre escrita, não sobre " + tool)

    def test_malformed_input_never_blocks(self):
        p = subprocess.run([sys.executable, str(HOOK)], input="isto nao e json",
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, "entrada ilegível não é razão para recusar")


class W2b_EscritaSobreEstadoPronto(unittest.TestCase):
    def test_a_healthy_engagement_lets_every_authority_through(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            eng = engagement(base)
            for nome in (SU, "decisions.md", "answers.md", "_state.json"):
                p = corre(escrita(eng / nome), base)
                self.assertEqual(p.returncode, 0,
                                 "estado pronto: `{}` passa. {}".format(nome, p.stderr))

    def test_a_directory_without_state_is_start_creating_it(self):
        """`/start` é a excepção justificada: não há estado anterior a reconstruir."""
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            novo = base / "ainda-nao-existe"
            novo.mkdir(parents=True)
            p = corre(escrita(novo / "_state.json"), base)
        self.assertEqual(p.returncode, 0)


class W2c_RecusaSobreEstadoPorReconstruir(unittest.TestCase):
    """O caso que o W2 existe para impor."""

    def test_a_pending_operation_blocks_the_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            eng = engagement(base)
            O["_atomic_write"](O["pending_path"](eng),
                               json.dumps({"operation_id": "op-a-meio"}))
            p = corre(escrita(eng / SU), base)
        self.assertTrue(negou(p), "escrita sobre operação pendente tinha de ser recusada")
        self.assertIn("eng", p.stderr)

    def test_the_refusal_names_the_recovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            eng = engagement(base)
            O["_atomic_write"](O["pending_path"](eng), json.dumps({"operation_id": "x"}))
            p = corre(escrita(eng / "decisions.md"), base)
        razao = json.loads(p.stderr.strip().splitlines()[-1])[
            "hookSpecificOutput"]["permissionDecisionReason"]
        self.assertIn("não está reconstruído", razao)
        self.assertIn("decisions.md", razao, "a recusa diz em QUE autoridade ia escrever")

    def test_a_corrupt_graph_blocks_the_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            eng = engagement(base)
            (eng / "_graph" / "graph.jsonl").write_text("{ isto nao e json\n", encoding="utf-8")
            p = corre(escrita(eng / SU), base)
        self.assertTrue(negou(p), "um grafo ilegível não autoriza escrever sobre ele")

    def test_edit_is_blocked_exactly_like_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            eng = engagement(base)
            O["_atomic_write"](O["pending_path"](eng), json.dumps({"operation_id": "x"}))
            p = corre(escrita(eng / SU, tool="Edit"), base)
        self.assertTrue(negou(p), "`Edit` é escrita como `Write` é")

    def test_every_authority_is_covered_not_just_the_su(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            eng = engagement(base)
            O["_atomic_write"](O["pending_path"](eng), json.dumps({"operation_id": "x"}))
            for nome in (SU, "decisions.md", "answers.md", "_state.json"):
                p = corre(escrita(eng / nome), base)
                self.assertTrue(negou(p), "`{}` é autoridade e passou".format(nome))


class W2d_NaoSeContornaPelaGrafiaDoCaminho(unittest.TestCase):
    """«Testar que nenhum entrypoint contorna o bootstrap por uma chamada indirecta»."""

    def caminhos_equivalentes(self, eng):
        return [eng / SU,
                eng / "." / SU,
                eng / ".." / eng.name / SU,
                eng / "_graph" / ".." / SU]

    def test_a_path_that_resolves_into_the_engagement_is_still_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            eng = engagement(base)
            O["_atomic_write"](O["pending_path"](eng), json.dumps({"operation_id": "x"}))
            for caminho in self.caminhos_equivalentes(eng):
                p = corre(escrita(caminho), base)
                self.assertTrue(negou(p), "contornado por `{}`".format(caminho))

    def test_an_absolute_path_is_blocked_too(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            eng = engagement(base)
            O["_atomic_write"](O["pending_path"](eng), json.dumps({"operation_id": "x"}))
            p = corre(escrita(Path(os.path.abspath(str(eng / SU)))), base)
        self.assertTrue(negou(p))


class W2e_FalhaFechada(unittest.TestCase):
    """Não conseguir verificar não é o mesmo que ter verificado."""

    def test_an_unevaluable_bootstrap_is_refused_not_waved_through(self):
        """O teste que faltava — e a sua ausencia deixava passar um guarda que falha ABERTO.

        A primeira versao deste caso tolerava os dois resultados com um `skipTest`: sobre um
        `_state.json` ilegivel o bootstrap nao rebenta, entao o teste nao decidia nada. Aqui
        forca-se o caso real — a avaliacao levanta — e afirma-se o unico resultado aceitavel.
        Em processo, porque o ramo a testar e o `except` de `avalia`."""
        guarda = runpy.run_path(str(HOOK))

        class Rebenta(dict):
            def __getitem__(self, k):
                raise RuntimeError("bootstrap indisponivel")

        original = guarda["runpy"].run_path
        guarda["runpy"].run_path = lambda *a, **kw: Rebenta()
        try:
            with tempfile.TemporaryDirectory() as tmp:
                eng = engagement(Path(tmp))
                pronto, razao = guarda["avalia"](eng)
        finally:
            guarda["runpy"].run_path = original

        self.assertFalse(pronto, "nao conseguir verificar NAO e o mesmo que ter verificado")
        self.assertIn("não pôde ser avaliado", razao)

    def test_an_unreadable_state_file_is_handled_one_way_or_the_other(self):
        """Complemento honesto: se o bootstrap tolerar, o guarda deixa passar — e diz-se."""
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            eng = engagement(base)
            (eng / "_state.json").write_text("{ nao e json", encoding="utf-8")
            p = corre(escrita(eng / SU), base)
        self.assertIn(p.returncode, (0, 2), "o guarda nao pode rebentar sobre entrada torta")
        if p.returncode == 2:
            self.assertTrue(negou(p))

    def test_the_administrative_override_is_explicit_and_logged(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            eng = engagement(base)
            O["_atomic_write"](O["pending_path"](eng), json.dumps({"operation_id": "x"}))
            bloqueado = corre(escrita(eng / SU), base)
            permitido = corre(escrita(eng / SU), base, modo="log")
        self.assertTrue(negou(bloqueado), "sem override, recusa")
        self.assertEqual(permitido.returncode, 0, "com override, passa")
        self.assertIn("override", permitido.stderr, "e o override deixa rasto")


class W2f_OGuardaEstaLigado(unittest.TestCase):
    """Um guarda que o harness não invoca não guarda nada."""

    def test_the_hook_is_registered_as_a_pretooluse_on_write_and_edit(self):
        cfg = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
        comandos = []
        for regra in (cfg.get("hooks") or {}).get("PreToolUse", []):
            matcher = regra.get("matcher", "")
            for h in regra.get("hooks", []):
                if "pre-authority-guard" in h.get("command", ""):
                    comandos.append(matcher)
        self.assertTrue(comandos, "o guarda não está registado em settings.json")
        self.assertTrue(any("Write" in m and "Edit" in m for m in comandos),
                        "registado, mas não sobre `Write|Edit`: {}".format(comandos))

    def test_the_hook_file_is_executable_python(self):
        p = subprocess.run([sys.executable, str(HOOK), "--engagement", "nao-existe"],
                           capture_output=True, text=True)
        self.assertIn(p.returncode, (0, 1), p.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=1)
