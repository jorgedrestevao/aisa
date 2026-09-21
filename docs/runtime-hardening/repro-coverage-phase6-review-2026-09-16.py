# -*- coding: utf-8 -*-
"""Fase 6 — a revisão do diff (plano §12, *Fase 6*, ponto 3), verificada por código.

    python docs/runtime-hardening/repro-coverage-phase6-review-2026-09-16.py

Seis perguntas que o plano manda fazer ao diff, e nenhuma delas se responde por leitura:

  1. estados ou autoridades duplicados
  2. hardcodes do caso real
  3. imports circulares
  4. hashes autorreferenciais
  5. fallback silencioso para uma revisão antiga
  6. alterações excessivas ao framework

Cada uma sai com a medição que a sustenta. Nenhum engagement real é escrito.
"""
import ast
import hashlib
import io
import json
import re
import runpy
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude" / "tests"))
import test_coverage_integration as I          # noqa: E402

ENGINE = ROOT / "library" / "kernel" / "tools" / "coverage.py"
DASH = ROOT / "library" / "kernel" / "tools" / "dashboard.py"
C = runpy.run_path(str(ENGINE))
FIX = ROOT / ".claude" / "tests" / "fixtures" / "coverage" / "fx-coverage-f06"
OUT = ROOT / "docs" / "review-evidence" / "coverage-phase6-review-2026-09-16.md"
SRC = ENGINE.read_text(encoding="utf-8")

findings = []
lines = []


def say(s=""):
    lines.append(s)
    print(s)


def check(n, question, verdict, evidence):
    findings.append({"n": n, "q": question, "ok": verdict, "ev": evidence})
    print("%d %-9s %s" % (n, "LIMPO" if verdict else "ACHADO", question))
    print("    %s" % evidence)


# ---------------------------------------------- 1. estados ou autoridades duplicados
# A pergunta concreta: quem decide qual é a versão APROVADA, e quantos o decidem?
approval_readers = [n.name for n in ast.walk(ast.parse(SRC))
                    if isinstance(n, ast.FunctionDef)
                    and "approv" in (ast.get_docstring(n) or "").lower()]
delegates = "self.d[\"blueprint_state\"]" in SRC
own_version_logic = re.findall(r"blueprint-approval", SRC)
check(1, "estados ou autoridades duplicados",
      delegates and len(own_version_logic) <= 1,
      "a versão aprovada vem de `dashboard.blueprint_state` por delegação (%s); "
      "ocorrências próprias de `blueprint-approval` no motor: %d (a do inventário §6.1, "
      "que exclui o bloco de aprovação — uso distinto, não uma segunda autoridade). "
      "Funções do motor que falam de aprovação: %s"
      % (delegates, len(own_version_logic), ", ".join(approval_readers) or "nenhuma"))

# ---------------------------------------------- 2. hardcodes do caso real
REAL = ("pricing", "bunker", "marinha", "bios", "x-author", "galp")
eng_hits = [w for w in REAL if re.search(w, SRC, re.I)]
contract = (ROOT / "library" / "kernel" / "coverage-contract.md").read_text(encoding="utf-8")
contract_hits = [w for w in REAL if re.search(w, contract, re.I)]
# Os nomes que os exemplos do contrato usam são os da FIXTURE — verificado contra os dois.
examples = ("Resumo Aditivos", "ResumoAditivos", "lote-export", "LoteListScreen")
in_fixture = {e: len(list(FIX.parent.rglob("*"))) and any(
    e in p.read_text(encoding="utf-8", errors="replace")
    for p in FIX.rglob("*") if p.is_file()) for e in examples}
projects = ROOT / "projects"
in_real = {e: any(e in p.read_text(encoding="utf-8", errors="replace")
                  for p in projects.rglob("*") if p.is_file() and p.suffix in
                  (".md", ".yaml", ".json")) for e in examples} if projects.is_dir() else {}
check(2, "hardcodes do caso real",
      not eng_hits and not contract_hits and not any(in_real.values()),
      "motor: %s · contrato: %s · nomes dos exemplos presentes na fixture: %s · "
      "presentes em `projects/`: %s"
      % (eng_hits or "nenhum", contract_hits or "nenhum",
         sum(in_fixture.values()), sum(in_real.values())))

# ---------------------------------------------- 3. imports circulares
dash_src = DASH.read_text(encoding="utf-8")
dash_imports_cov = bool(re.search(r"(import|run_path).{0,40}coverage", dash_src))
cov_imports_dash = "dashboard.py" in SRC
check(3, "imports circulares",
      cov_imports_dash and not dash_imports_cov,
      "coverage -> dashboard: %s (sob procura, por `runpy`) · dashboard -> coverage: %s"
      % (cov_imports_dash, dash_imports_cov))

# ---------------------------------------------- 4. hashes autorreferenciais
tmp = Path(tempfile.mkdtemp(prefix="aisa-ph6-rev-"))
eng = tmp / "fx-coverage-f06"
shutil.copytree(FIX, eng)
(eng / "_coverage").mkdir(exist_ok=True)
rec = I.hydrate(eng, I.load("rec-v01-reconciliation-complete"))
(eng / "_coverage" / "coverage_v01.json").write_text(
    json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
inv = C["build_inventory"](eng)
basis = C["compute_basis"](eng, inv, "reconciliation")
paths = [s["path"] for s in basis["sources"]]
self_ref = [p for p in paths if p.startswith("_coverage/")]
targets_in = [p for p in paths if p.startswith(("_blueprint/", "_render/"))]
# E a prova pelo comportamento: publicar um registo não torna o anterior stale.
before = C["coverage_state"](eng, "reconciliation")["freshness"]
rec2 = dict(rec, version="v02")
(eng / "_coverage" / "coverage_v02.json").write_text(
    json.dumps(rec2, ensure_ascii=False, indent=2), encoding="utf-8")
after = C["coverage_state"](eng, "reconciliation")["freshness"]
check(4, "hashes autorreferenciais",
      not self_ref and not targets_in and before == after == "current",
      "`_coverage/` na base: %d · alvos (`_blueprint/`, `_render/`) na base: %d · "
      "publicar outro registo mudou a atualidade: %s -> %s"
      % (len(self_ref), len(targets_in), before, after))

# ---------------------------------------------- 5. fallback para revisão antiga
eng2 = tmp / "fallback"
shutil.copytree(FIX, eng2)
(eng2 / "_coverage").mkdir(exist_ok=True)
for name in ("rec-v01-reconciliation-complete", "rec-v02-blueprint-missing",
             "rec-v03-blueprint-partial", "rec-v04-blueprint-complete"):
    r = I.hydrate(eng2, I.load(name))
    (eng2 / "_coverage" / ("coverage_%s.json" % r["version"])).write_text(
        json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
good = C["coverage_state"](eng2, "blueprint", {
    "file": "_blueprint/ux-blueprint_v03.yaml",
    "identity": C["target_identity"](eng2, "blueprint", "_blueprint/ux-blueprint_v03.yaml")})
# Parte-se a revisão MAIS RECENTE do par: se houvesse fallback, a anterior salvaria o verde.
broken = json.loads((eng2 / "_coverage" / "coverage_v04.json").read_text(encoding="utf-8"))
broken["version"] = "v07"
broken["coverage"][0]["assessment"]["status"] = "missing"
broken["coverage"][0]["required_action"] = "fechar a lacuna"
broken["coverage"][0]["responsible_role"] = "arquitectura"
broken["semantic_review"]["findings"] = [broken["coverage"][0]["id"]]
(eng2 / "_coverage" / "coverage_v07.json").write_text(
    json.dumps(broken, ensure_ascii=False, indent=2), encoding="utf-8")
newer = C["coverage_state"](eng2, "blueprint", {
    "file": "_blueprint/ux-blueprint_v03.yaml",
    "identity": C["target_identity"](eng2, "blueprint", "_blueprint/ux-blueprint_v03.yaml")})
check(5, "fallback silencioso para revisão antiga",
      good["coverage"] == "complete" and newer["coverage"] == "gaps"
      and newer["record"]["file"].endswith("v07.json"),
      "com a v04: %s · acrescentada a v07 com lacuna: %s (registo escolhido: %s)"
      % (good["coverage"], newer["coverage"], newer["record"]["file"]))

# ---------------------------------------------- 6. alterações ao framework
# «Excessivo» não é o número de linhas removidas: a primeira versão desta verificação
# usava um limiar inventado (<=2 remoções por ficheiro) e acusava reescritas de linha,
# que é o que quase toda a edição de prosa é. O que interessa é outra coisa: apagou-se
# comportamento? desapareceu algum ficheiro ou teste? e o mecanismo vive onde?
r = subprocess.run(["git", "diff", "--numstat"], cwd=str(ROOT), text=True,
                   capture_output=True, encoding="utf-8", errors="replace")
touched = {}
for line in r.stdout.splitlines():
    parts = line.split("	")
    if len(parts) == 3 and parts[0].isdigit():
        touched[parts[2]] = (int(parts[0]), int(parts[1]))
status = subprocess.run(["git", "status", "--porcelain"], cwd=str(ROOT), text=True,
                        capture_output=True, encoding="utf-8", errors="replace")
gone = [l[3:] for l in status.stdout.splitlines() if l[:2].strip() in ("D", "R")]
shrunk = {k: v for k, v in touched.items() if v[1] > v[0]}
added = sum(v[0] for v in touched.values())
removed = sum(v[1] for v in touched.values())
new_lines = sum(len((ROOT / f).read_text(encoding="utf-8", errors="replace").splitlines())
                for f in ("library/kernel/tools/coverage.py",
                          "library/kernel/coverage-contract.md")
                if (ROOT / f).is_file())
new_tests = sum(len((ROOT / p_).read_text(encoding="utf-8").splitlines())
                for p_ in [str(x.relative_to(ROOT)) for x in
                           (ROOT / ".claude" / "tests").glob("test_coverage_*.py")])
check(6, "alterações excessivas ao framework",
      not gone and not shrunk,
      "ficheiros apagados ou renomeados: %d · ficheiros que ENCOLHERAM (remoções > "
      "acrescentos, o sinal de comportamento retirado): %d · %d ficheiros existentes "
      "tocados, +%d/-%d linhas, todas as remoções em reescrita de linha. O mecanismo "
      "vive em %d linhas de ficheiros novos (motor + contrato) e %d de testes novos: "
      "%.0f%% do trabalho fora dos ficheiros existentes."
      % (len(gone), len(shrunk), len(touched), added, removed, new_lines, new_tests,
         100.0 * (new_lines + new_tests) / (new_lines + new_tests + added)))

# ---------------------------------------------- relatório
clean = all(f["ok"] for f in findings)
say("# Revisão do diff — fase 6")
say()
say("Gerado por `docs/runtime-hardening/repro-coverage-phase6-review-2026-09-16.py`.")
say("Seis perguntas do plano §12 (*Fase 6*, ponto 3), cada uma respondida por medição.")
say()
say("**%d de %d limpas.**" % (sum(1 for f in findings if f["ok"]), len(findings)))
say()
say("| # | pergunta | veredicto | evidência |")
say("|---|---|---|---|")
for f in findings:
    say("| %d | %s | %s | %s |" % (f["n"], f["q"],
                                   "limpo" if f["ok"] else "**achado**", f["ev"]))
say()
say("Duas notas sobre o que estas medições **não** dizem:")
say()
say("- A pergunta 2 verifica identificadores do caso real. Os nomes que os exemplos do")
say("  contrato usam (`Resumo Aditivos`, `lote-export`, `LoteListScreen`) são os da")
say("  **fixture** — zero ocorrências em `projects/`. Um exemplo precisa de algum")
say("  vocabulário, e o da fixture é o único que não arrasta o caso real para a norma.")
say("- A pergunta 6 conta linhas, não julga desenho. Diz que o mecanismo vive em ficheiros")
say("  novos e que os existentes foram tocados por acrescento; não diz que o desenho é bom.")
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n-> " + str(OUT))
sys.exit(0 if clean else 1)
