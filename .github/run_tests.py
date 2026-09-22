#!/usr/bin/env python3
"""A suite inteira, um processo por ficheiro, em paralelo.

Corre em qualquer clone, sem instalar nada (ADR-001: stdlib apenas). Sai 1 se algum
ficheiro falhar, para o CI reprovar.

Os 65 ficheiros ja corriam cada um no seu processo — o que nao corriam era ao mesmo tempo.
Medido: 221s sequenciais, 85% em 12 ficheiros e 61% so nos 7 de `coverage`, que refazem o
inventario do engagement (sha256 de cada ficheiro da arvore) em cada caso.

A saida e a mesma de antes, byte a byte, mais um `wall` no fim. `--sequential` corre pela
ordem antiga, e e com ele que se confirma que o paralelo nao esconde nada.
"""
import concurrent.futures as cf
import glob
import json
import os
import re
import subprocess
import sys
import time

VERDICT = re.compile(r"^(OK|FAILED)(\s*\((.*)\))?\s*$")
RAN = re.compile(r"^Ran (\d+) tests? in ")


def corre(f):
    p = subprocess.run([sys.executable, f], capture_output=True, text=True)
    return f, p.stderr + p.stdout


def main():
    files = (sorted(glob.glob(".claude/tests/test_*.py"))
             + sorted(glob.glob("library/kernel/tools/tests/test_*.py")))
    sequencial = "--sequential" in sys.argv
    t0 = time.time()
    if sequencial:
        saidas = [corre(f) for f in files]
    else:
        # Os ficheiros sao independentes: cada um ja corria isolado, com os seus temp dirs.
        with cf.ProcessPoolExecutor(max_workers=min(len(files), os.cpu_count() or 4)) as ex:
            saidas = list(ex.map(corre, files))

    tot = dict(files=0, ok=0, fail_files=0, tests=0, failures=0, errors=0,
               skips=0, expected_failures=0)
    bad = []
    for f, out in sorted(saidas):
        tot["files"] += 1
        ran = 0
        for line in out.splitlines():
            m = RAN.match(line.strip())
            if m:
                ran = int(m.group(1))
        tot["tests"] += ran
        verdict = None
        for line in out.splitlines():
            m = VERDICT.match(line.strip())
            if m:
                verdict = m
        if verdict is None:
            bad.append((f, "sem veredicto"))
            tot["fail_files"] += 1
            continue
        detail = verdict.group(3) or ""
        for key, label in (("failures", "failures"), ("errors", "errors"),
                           ("skips", "skipped"), ("expected_failures", "expected failures")):
            m = re.search(r"(?<!un)\b" + label + r"=(\d+)", detail)
            if m:
                tot[key] += int(m.group(1))
        if verdict.group(1) == "OK":
            tot["ok"] += 1
        else:
            tot["fail_files"] += 1
            bad.append((f, detail))
    tot["wall"] = round(time.time() - t0, 1)
    tot["mode"] = "sequential" if sequencial else "parallel"
    print(json.dumps(tot))
    for f, d in bad:
        print("FAIL", f, d)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
