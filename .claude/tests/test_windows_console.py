# -*- coding: utf-8 -*-
"""A consola Windows fala cp1252, e o kernel fala portugues.

Tres erros numa so sessao de Discovery real, em Windows, todos iguais:

    bootstrap.py --json          UnicodeEncodeError: '\\u2192'  (→)  position 30439
    python3 -c "...json.dumps"   UnicodeEncodeError: '\\u024f'
    (e o `migrate.py apply` que o guarda manda correr teria sido o terceiro)

Medido no repositorio antes de corrigir:

    imprimem nao-ASCII e NAO protegem a consola:
        bootstrap  graph  migrate  operation  projection  resolve
    imprimem nao-ASCII e protegem:
        coverage  dashboard  fields_draft  text_extract  xlsx_extract

Os seis que falham sao os motores da memoria persistente — os mais novos. Os antigos ja
tinham `utf8_console()`; os novos nunca a herdaram. E um script ad-hoc que a sessao escreve
tem o mesmo defeito, por isso corrigir so os motores nao chega: a segunda camada e
`PYTHONUTF8=1` no ambiente do projecto.

Em Linux, `PYTHONIOENCODING=cp1252` reproduz exactamente a consola Windows."""
import json
import os
import re
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "library" / "kernel" / "tools"
FIX = runpy.run_path(str(ROOT / ".claude" / "tests" / "test_migration.py"))
M = runpy.run_path(str(TOOLS / "migrate.py"))

NAO_ASCII = "margem → preço «spot» ɏ"


def consola_windows():
    """O ambiente de uma consola cp1252, sem o modo UTF-8 do Python a salvar ninguem."""
    env = dict(os.environ, PYTHONIOENCODING="cp1252")
    env.pop("PYTHONUTF8", None)
    return env


def eng_com_acentos(tmp):
    eng = Path(FIX["make"](tmp, FIX["NOVO"]))
    su = eng / "shared-understanding.md"
    t = su.read_text(encoding="utf-8")
    su.write_text(t.replace("Base partilhada", "Base partilhada " + NAO_ASCII, 1),
                  encoding="utf-8", newline="\n")
    M["apply"](eng)
    return eng


def corre(args):
    return subprocess.run([sys.executable] + args, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", env=consola_windows(),
                          timeout=300)


class W1_OsMotoresNaoRebentam(unittest.TestCase):

    def assert_sem_crash(self, p, nome):
        self.assertNotIn("UnicodeEncodeError", p.stderr,
                         "{} rebentou numa consola cp1252:\n{}".format(nome, p.stderr[-400:]))

    def test_bootstrap(self):
        """O primeiro erro real, exactamente."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_com_acentos(tmp)
            p = corre([str(TOOLS / "bootstrap.py"), "--engagement", str(eng), "--json"])
        self.assert_sem_crash(p, "bootstrap")
        self.assertEqual(p.returncode, 0, p.stderr[-300:])

    def test_graph(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_com_acentos(tmp)
            p = corre([str(TOOLS / "graph.py"), "inspect", "--engagement", str(eng), "--json"])
        self.assert_sem_crash(p, "graph")

    def test_migrate(self):
        """O que o guarda manda correr para recuperar — nao pode ser ele a rebentar."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_com_acentos(tmp)
            p = corre([str(TOOLS / "migrate.py"), "dry-run", "--engagement", str(eng), "--json"])
        self.assert_sem_crash(p, "migrate")

    def test_operation(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_com_acentos(tmp)
            p = corre([str(TOOLS / "operation.py"), "status", "--engagement", str(eng), "--json"])
        self.assert_sem_crash(p, "operation")

    def test_projection(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_com_acentos(tmp)
            p = corre([str(TOOLS / "projection.py"), "--engagement", str(eng), "--json"])
        self.assert_sem_crash(p, "projection")


class W2_AClasseNaoOCaso(unittest.TestCase):
    """O defeito repetiu-se em seis ficheiros porque cada um nasceu sem a protecao. Um
    setimo motor nasceria igual. Este caso le TODOS os CLIs do kernel."""

    def test_every_kernel_cli_that_prints_non_ascii_protects_the_console(self):
        faltam = []
        for f in sorted(TOOLS.glob("*.py")):
            src = f.read_text(encoding="utf-8")
            if not re.search(r"^def main\(|__name__ == .__main__.", src, re.M):
                continue
            if "ensure_ascii=False" not in src:
                continue
            if not re.search(r"utf8_console\(\)|\.reconfigure\(", src):
                faltam.append(f.name)
        self.assertEqual(faltam, [],
                         "CLIs que imprimem nao-ASCII sem proteger a consola: {}".format(faltam))

    def test_the_protection_runs_inside_main(self):
        """Definir `utf8_console` e nao a chamar e o mesmo que nao a ter."""
        for nome in ("bootstrap", "graph", "migrate", "operation", "projection", "resolve"):
            src = (TOOLS / (nome + ".py")).read_text(encoding="utf-8")
            corpo = src[src.index("def main("):]
            self.assertRegex(corpo[:600], r"utf8_console\(\)",
                             "{}.main() nao protege a consola".format(nome))


class W3_OAmbienteDoProjecto(unittest.TestCase):
    """A segunda camada: o que a sessao escreve ad-hoc (o terceiro erro real)."""

    def test_the_project_runs_python_in_utf8_mode(self):
        d = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
        self.assertEqual((d.get("env") or {}).get("PYTHONUTF8"), "1",
                         "sem PYTHONUTF8=1, qualquer print ad-hoc rebenta em Windows")

    def test_utf8_mode_saves_an_ad_hoc_script(self):
        """Prova de que a camada funciona: o script exacto do terceiro erro."""
        script = "import json; print(json.dumps({'x': '" + NAO_ASCII + "'}, ensure_ascii=False))"
        env = consola_windows()
        env["PYTHONUTF8"] = "1"
        env.pop("PYTHONIOENCODING")   # PYTHONIOENCODING prevalece sobre o modo UTF-8
        p = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True,
                           encoding="utf-8", env=env, timeout=60)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("→", p.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=1)
