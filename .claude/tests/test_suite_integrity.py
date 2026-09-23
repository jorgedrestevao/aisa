# -*- coding: utf-8 -*-
"""A suite corre o que se escreveu nela.

O runner (`.github/run_tests.py`) corre cada ficheiro como SCRIPT — `python f` —, e por isso
o `unittest.main()` do bloco `if __name__ == "__main__":` executa no momento em que o
interpretador la chega. Uma classe definida DEPOIS desse bloco nao existe ainda quando os
testes sao recolhidos: nunca corre no CI. Com `unittest discover` corre, porque o modulo e
importado inteiro — e foi assim que o defeito se escondeu.

Medido: 10 casos em dois ficheiros, acrescentados com `cat >>` depois do bloco, que o CI
nunca correu. Um deles (`T7_OsLocatorsDosFormatosNovos`, 7 casos) esteve em `master` desde
`c7fabf6`, e o total reportado incluia-os."""
import glob
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def ficheiros():
    return sorted(glob.glob(str(ROOT / ".claude" / "tests" / "test_*.py"))) + \
        sorted(glob.glob(str(ROOT / "library" / "kernel" / "tools" / "tests" / "test_*.py")))


class I1_NadaDepoisDoMain(unittest.TestCase):

    def test_no_test_is_defined_after_the_main_block(self):
        faltam = []
        for f in ficheiros():
            s = Path(f).read_text(encoding="utf-8")
            m = re.search(r"^if __name__ == .__main__.:", s, re.M)
            if not m:
                continue
            depois = s[m.end():]
            if re.search(r"^class \w+|^    def test_\w+", depois, re.M):
                faltam.append(Path(f).name)
        self.assertEqual(faltam, [],
                         "testes definidos depois do __main__ — o CI nao os corre: {}".format(faltam))

    def test_every_test_file_can_run_as_a_script(self):
        """O runner corre `python f`; um ficheiro sem o bloco nao corre nada e sai 0."""
        sem = [Path(f).name for f in ficheiros()
               if not re.search(r"^if __name__ == .__main__.:", Path(f).read_text(encoding="utf-8"), re.M)]
        self.assertEqual(sem, [], "ficheiros de teste que o runner corre sem executar nada: {}".format(sem))


if __name__ == "__main__":
    unittest.main(verbosity=1)
