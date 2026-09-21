# -*- coding: utf-8 -*-
"""Ensaio do percurso do desenho, fase 4 — corre numa cópia da fixture, escreve a evidência.

    python rehearsal_phase4.py            # escreve docs/review-evidence/coverage-phase4-*.md

Nenhum engagement real é tocado. Cada passo mostra o que o executor faria e o que o estado
devolve a seguir, com os quatro veredictos separados.
"""
import io
import json
import os
import runpy
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(r"C:\Users\jorge.estevao\Documents\Galp\Claude Code Projects\aisa-rt-fix")
sys.path.insert(0, str(ROOT / ".claude" / "tests"))
import test_coverage_integration as I          # noqa: E402

ENGINE = ROOT / "library" / "kernel" / "tools" / "coverage.py"
DASH = runpy.run_path(str(ROOT / "library" / "kernel" / "tools" / "dashboard.py"))
FIX = ROOT / ".claude" / "tests" / "fixtures" / "coverage" / "fx-coverage-f06"
OUT = ROOT / "docs" / "review-evidence" / "coverage-phase4-rehearsal-2026-09-15.md"
TODAY = date(2026, 9, 15)

tmp = Path(tempfile.mkdtemp(prefix="aisa-ph4-"))
eng = tmp / "fx-coverage-f06"
shutil.copytree(FIX, eng)
lines = []


def say(s=""):
    lines.append(s)
    print(s)


def cli(*args):
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["AISA_ENGAGEMENTS_ROOT"] = str(tmp)
    return subprocess.run([sys.executable, "-B", str(ENGINE), *args], cwd=str(ROOT),
                          env=env, text=True, capture_output=True, encoding="utf-8",
                          errors="replace")


def hook(name, *args):
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["AISA_ENGAGEMENTS_ROOT"] = str(tmp)
    return subprocess.run([sys.executable, "-B",
                           str(ROOT / ".claude" / "hooks" / name), *args], cwd=str(ROOT),
                          env=env, text=True, capture_output=True, encoding="utf-8",
                          errors="replace", input="")


def install(*names):
    (eng / "_coverage").mkdir(exist_ok=True)
    for n in names:
        rec = I.hydrate(eng, I.load(n))
        (eng / "_coverage" / ("coverage_%s.json" % rec["version"])).write_text(
            json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")


def snapshot(label):
    c = DASH["build_model"](eng, TODAY)["status"]["coverage"]
    r = c["readiness"]
    say("**%s**" % label)
    say()
    say("```text")
    say("estrutura ....... %s" % r["structure"])
    say("cobertura ....... %s" % r["coverage"])
    say("aprovação ....... %s%s" % (r["approval"],
                                    (" (" + r.get("approved_version", "") + ")")
                                    if r.get("approved_version") else ""))
    say("ponta-a-ponta ... %s" % r["e2e"])
    say("pode ir a aprovação: %s" % c["approve_eligible"])
    for st in ("reconciliation", "blueprint"):
        s = c["stages"].get(st)
        if s:
            say("  %-15s cobertura=%-13s atualidade=%-9s leitura=%-9s registo=%s"
                % (st, s["coverage"], s["freshness"], s["semantic_review"],
                   s["record"] or "—"))
            for g in s["gaps"]:
                say("      lacuna: %s · %s · %s" % (g.get("item", ""),
                                                    ", ".join(g.get("requirement_refs")
                                                              or []), g.get("status", "")))
    for b in c["blockers"]:
        say("  bloqueio: %s" % b)
    say("```")
    say()
    return c


say("# Ensaio do percurso do desenho — fase 4 da cobertura")
say()
say("Data: 2026-09-15. Gerado por código "
    "(`docs/runtime-hardening/repro-coverage-phase4-2026-09-15.py`), numa **cópia temporária**")
say("da fixture `.claude/tests/fixtures/coverage/fx-coverage-f06`. Nenhum engagement real foi")
say("lido para escrita, e nenhuma aprovação foi registada em nome de ninguém.")
say()
say("O percurso é o do executor: produzir sem conferir → conferir e encontrar a perda →")
say("desenhar a correcção → conferir outra vez → **continuar sem aprovação** → aprovar →")
say("responder a uma pergunta e ver a conferência caducar.")
say()

# ---------------------------------------------------------------- 1
say("## 1. Antes de existir revisão nenhuma")
say()
say("O desenho `v01` está em disco. A verificação estrutural do runtime diz que é válido.")
say()
for p in sorted((eng / "_blueprint").glob("*.yaml")):
    if p.name != "ux-blueprint_v01.yaml":
        p.unlink()
snapshot("estado, sem `_coverage/`")
r = cli("check", "--engagement", "fx-coverage-f06", "--stage", "reconciliation", "--json")
say("`coverage.py check --stage reconciliation` → exit **%d**, "
    "`%s`, código `%s`." % (r.returncode, json.loads(r.stdout)["coverage"],
                            json.loads(r.stdout)["diagnostics"][0]["code"]))
say()
say("É o que o contrato manda: sem registo, `not_evaluated`. Não é aprovação nem reprovação.")
say()

# ---------------------------------------------------------------- 2
say("## 2. A reconciliação das fontes (passo 1e)")
say()
install("rec-v01-reconciliation-complete")
c = snapshot("estado, com a reconciliação publicada")
r = cli("check", "--engagement", "fx-coverage-f06", "--stage", "reconciliation", "--json")
say("`check --stage reconciliation` → exit **%d**; elegível para produzir: **%s**."
    % (r.returncode, json.loads(r.stdout)["eligible"]))
say()

# ---------------------------------------------------------------- 3
say("## 3. A revisão da versão produzida (passo 13b) — e a perda aparece")
say()
install("rec-v02-blueprint-missing")
snapshot("estado, com a revisão da `v01`")
r = cli("check", "--engagement", "fx-coverage-f06", "--stage", "blueprint", "--target",
        "_blueprint/ux-blueprint_v01.yaml", "--json")
say("`check --stage blueprint --target …v01.yaml` → exit **%d**, cobertura `%s`."
    % (r.returncode, json.loads(r.stdout)["coverage"]))
say()
h = hook("blueprint-validate.py", str(eng / "_blueprint" / "ux-blueprint_v01.yaml"))
say("O hook, sobre o mesmo ficheiro (exit %d, escreve nada):" % h.returncode)
say()
say("```text")
for l in h.stderr.strip().splitlines():
    say(l)
say("```")
say()
say("**É esta a asserção central.** A estrutura diz `valid`; a cobertura diz que o desenho")
say("perdeu dois requisitos que a Shared Understanding já carregava. Uma pergunta não")
say("responde pela outra, e nenhuma das duas é aprovação.")
say()

# ---------------------------------------------------------------- 4
say("## 4. A correcção, e a conferência outra vez")
say()
shutil.copy2(FIX / "_blueprint" / "ux-blueprint_v02.yaml", eng / "_blueprint")
shutil.copy2(FIX / "_blueprint" / "ux-blueprint_v03.yaml", eng / "_blueprint")
install("rec-v03-blueprint-partial", "rec-v04-blueprint-complete")
snapshot("estado, com a `v03` desenhada e revista")
say("A `v03` fecha as duas lacunas. **E continua sem aprovação nenhuma** — não há de onde")
say("a inventar, e `pode ir a aprovação: True` diz exactamente isso: pode ser levada.")
say()
h = hook("blueprint-validate.py", str(eng / "_blueprint" / "ux-blueprint_v03.yaml"))
say("O hook sobre a `v03` fica **em silêncio** (exit %d, %d linhas em stderr) — estrutura "
    "sem falhas e cobertura sem lacunas." % (h.returncode,
                                             len(h.stderr.strip().splitlines())))
say()

# ---------------------------------------------------------------- 5
say("## 5. A aprovação — e o ciclo que não acontece")
say()
say("O negócio aprova (na fixture, um bloco `D-003` acrescentado à mão: **o motor nunca")
say("escreve uma aprovação**, e a skill pergunta por `AskUserQuestion` antes de a escrever).")
say()
with io.open(eng / "decisions.md", "a", encoding="utf-8") as fh:
    fh.write("\n## D-003 — Blueprint bp-v03 aprovado\n\n"
             "- **Aprovado por**: dono do processo\n"
             "- **Cobertura consumida**: _coverage/coverage_v04.json\n"
             "- **Timestamp**: 2026-09-15T10:00:00+01:00\n")
snapshot("estado, depois de aprovar")
say("Acrescentar a aprovação **não** invalidou a revisão que ela consome (§6.4). Se")
say("invalidasse, aprovar destruiria a base da própria aprovação.")
say()

# ---------------------------------------------------------------- 6
say("## 6. Uma resposta nova, e a conferência caduca")
say()
with io.open(eng / "answers.md", "a", encoding="utf-8") as fh:
    fh.write("\n## U-010 — 2026-09-15\n\n- **Resposta**: o consumidor externo existe, "
             "e recebe o ficheiro por outro canal.\n- **Fonte**: dono do processo\n")
c = snapshot("estado, depois de `/answer`")
say("`stale` não diz que a conclusão anterior ficou falsa: diz que **ninguém releu as")
say("fontes desde que elas mudaram**. A aprovação registada mantém-se, e é isso que a")
say("terceira linha continua a dizer.")
say()
say("## O que este ensaio não demonstra")
say()
say("- Que o desenho está correcto. O motor verifica a **forma** da declaração; a")
say("  adequação é julgada e assinada pelo revisor (contrato §9).")
say("- Que a solução funciona ponta-a-ponta. Isso mede-se a correr a solução, e")
say("  `ponta-a-ponta` é `not_evaluated` em todos os passos acima, de propósito.")
say("- Nada sobre nenhum engagement real: a fixture é sintética e o domínio é inventado.")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n--> escrito:", OUT)
shutil.rmtree(tmp, ignore_errors=True)
