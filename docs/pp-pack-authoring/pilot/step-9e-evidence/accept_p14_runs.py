"""Lint the real outputs of frente C's validation runs with the same motor as the regression test:
the five P-14 subagent runs (`p14-runs.md`, fenced blocks) and the real `/status` of pilot-3.

    python docs/pp-pack-authoring/pilot/step-9e-evidence/accept_p14_runs.py
"""

import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
spec = importlib.util.spec_from_file_location("ul", os.path.join(ROOT, ".claude", "tests", "test_user_language.py"))
ul = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ul)


def blocks(path):
    with open(path, encoding="utf-8") as fh:
        md = fh.read()
    titles = re.findall(r"^###? (.+)$", md, flags=re.M)
    fences = re.findall(r"```\n(.*?)```", md, flags=re.S)
    return titles, fences


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    terms = ul.glossary_terms()
    total = 0
    print("| ficheiro / bloco | linhas | violações | detalhe |\n|---|---|---|---|")
    for name in ("p14-runs.md", "status-pilot-3-R04.md", "round-business-val-c-R05.md"):
        _, fences = blocks(os.path.join(HERE, name))
        for i, b in enumerate(fences, 1):
            v = ul.violations(b, terms)
            total += len(v)
            print("| {} #{} | {} | {} | {} |".format(name, i, len([l for l in b.splitlines() if l.strip()]), len(v),
                                                  "; ".join("l{} «{}»".format(ln, tok) for ln, tok, _ in v[:8])))
    print("\nRESULTADO: {}".format("PASSA" if total == 0 else "FALHA ({} violações)".format(total)))
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
