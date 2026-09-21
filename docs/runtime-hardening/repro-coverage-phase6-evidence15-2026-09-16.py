# -*- coding: utf-8 -*-
"""Fase 6 — a evidência final da §15 do plano, gerada por código.

    python docs/runtime-hardening/repro-coverage-phase6-evidence15-2026-09-16.py

Os oito pontos que o plano §15 exige do Claude. Os que se medem, medem-se aqui; os que
são declaração ficam escritos no relatório da fase e são citados a partir dele.

O ponto 5 pede **exemplo real** de CLI JSON e de relatório Markdown «sem editar engagement
original»: correm-se contra o engagement real em modo de leitura, com manifesto antes e
depois, e é isso que este ficheiro mostra.
"""
import hashlib
import io
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "library" / "kernel" / "tools" / "coverage.py"
OUT = ROOT / "docs" / "review-evidence" / "coverage-phase6-evidence15-2026-09-16.md"
PROJECTS = ROOT / "projects"
REAL_WORDS = ("pricing", "bunker", "marinha", "galp", "x-author", "bios")

NEW_FILES = [
    "library/kernel/tools/coverage.py",
    "library/kernel/coverage-contract.md",
    ".claude/tests/test_coverage_contract.py",
    ".claude/tests/test_coverage_inventory.py",
    ".claude/tests/test_coverage_freshness.py",
    ".claude/tests/test_coverage_integration.py",
    ".claude/tests/test_coverage_fixtures.py",
    ".claude/tests/test_coverage_phase4.py",
    ".claude/tests/test_coverage_phase5.py",
]

lines = []


def say(s=""):
    lines.append(s)
    print(s)


def manifest(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file()}


def run(*args):
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run([sys.executable, "-B", str(ENGINE), *args], cwd=str(ROOT),
                          env=env, text=True, capture_output=True, encoding="utf-8",
                          errors="replace")


say("# Evidência final §15 — fase 6")
say()
say("Gerado por `docs/runtime-hardening/repro-coverage-phase6-evidence15-2026-09-16.py`.")
say()

# ---------------------------------------------------------------- §15.1
say("## §15.1 — ficheiros alterados e decisões que divergem do plano")
say()
r = subprocess.run(["git", "diff", "--numstat"], cwd=str(ROOT), text=True,
                   capture_output=True, encoding="utf-8", errors="replace")
touched = [l.split("\t") for l in r.stdout.splitlines() if l.split("\t")[0].isdigit()]
say("**%d ficheiros existentes alterados** (+%d/-%d linhas) e **%d ficheiros novos**."
    % (len(touched), sum(int(t[0]) for t in touched), sum(int(t[1]) for t in touched),
       len(NEW_FILES)))
say()
say("| ficheiro novo | linhas |")
say("|---|---|")
for f in NEW_FILES:
    p = ROOT / f
    say("| `%s` | %d |" % (f, len(p.read_text(encoding="utf-8").splitlines())
                           if p.is_file() else 0))
say()
say("As divergências face ao plano, com justificação, estão em cada relatório de fase")
say("(§6 da fase 5; §4 e §5 das fases 1-3) e consolidadas no relatório desta fase.")
say()

# ---------------------------------------------------------------- §15.5
say("## §15.5 — CLI JSON e relatório Markdown, sobre o engagement real, sem o editar")
say()
engagements = sorted(p.name for p in PROJECTS.iterdir()
                     if p.is_dir() and (p / "_state.json").is_file()) \
    if PROJECTS.is_dir() else []
if not engagements:
    say("> **INCONCLUSIVO** — não há engagement montado neste checkout. O exemplo real")
    say("> não foi produzido, e isso não é o mesmo que tê-lo produzido sem achados.")
else:
    slug = engagements[0]
    eng = PROJECTS / slug
    before = manifest(eng)
    j = run("check", "--engagement", slug, "--stage", "reconciliation", "--json")
    m = run("report", "--engagement", slug, "--stage", "reconciliation")
    after = manifest(eng)
    data = json.loads(j.stdout)
    say("`coverage.py check --engagement %s --stage reconciliation --json` (exit %d):"
        % (slug, j.returncode))
    say()
    say("```json")
    trimmed = {k: data[k] for k in ("artefact", "contract_version", "engagement", "stage",
                                    "contract_validity", "freshness", "source_review",
                                    "semantic_review", "coverage", "action", "eligible")
               if k in data}
    trimmed["record"] = data.get("record")
    trimmed["inventory"] = data.get("inventory")
    trimmed["reasons"] = data.get("reasons")
    say(json.dumps(trimmed, ensure_ascii=False, indent=2)[:1400])
    say("```")
    say()
    say("`coverage.py report --engagement %s --stage reconciliation` (exit %d), primeiras"
        % (slug, m.returncode))
    say("linhas da projecção Markdown — que **não** é autoridade:")
    say()
    say("```text")
    for ln in m.stdout.splitlines()[:16]:
        say(ln)
    say("```")
    say()
    say("**Ficheiros do engagement alterados por estas duas execuções: %d**, em %d."
        % (sum(1 for k in before if before.get(k) != after.get(k))
           + len(set(before) ^ set(after)), len(before)))
    say()
    say("Os veredictos acima são **lidos** dos registos que quem conduz o engagement")
    say("publicou. Nada neste ficheiro os produziu, e nada aqui os valida.")
    say()

# ---------------------------------------------------------------- §15.6
say("## §15.6 — sem identificadores do caso real, e os read-only não escrevem")
say()
say("| ficheiro | ocorrências de %s |" % ", ".join("`%s`" % w for w in REAL_WORDS))
say("|---|---|")
worst, explained = 0, []
for f in NEW_FILES + [".claude/hooks/render-validate.py",
                      ".claude/skills/aisa-render/SKILL.md",
                      "library/kernel/render-contract.md"]:
    p = ROOT / f
    if not p.is_file():
        continue
    body = p.read_text(encoding="utf-8", errors="replace")
    n = sum(len(re.findall(w, body, re.I)) for w in REAL_WORDS)
    # A excepção é uma só, e é a que prova a regra: o teste que PROÍBE estes tokens tem
    # de os nomear para os procurar. Contá-la como violação seria acusar a fechadura de
    # ser a porta aberta.
    guard = "forbidden = (" in body and "no_identifier_of_the_real_case" in body
    if guard:
        explained.append((f, n))
    else:
        worst = max(worst, n)
    say("| `%s` | %d%s |" % (f, n, " (lista do teste que os proíbe)" if guard else ""))
say()
say("**Máximo fora da lista do guarda: %d.**" % worst)
for f, n in explained:
    say("As %d ocorrências em `%s` são os tokens que" % (n, f))
    say("`test_no_identifier_of_the_real_case_leaks_into_the_fixture` procura na fixture —")
    say("o teste tem de os nomear para os proibir.")
say()
say("A ausência de escrita dos comandos read-only está medida em")
say("`coverage-phase6-integrity-2026-09-16.md` (manifesto SHA-256 antes/depois).")
say()

# ---------------------------------------------------------------- §15.7 e §15.8
say("## §15.7 — limites remanescentes")
say()
say("Três, e nenhum deles se fecha com mais código:")
say()
say("1. **A compreensão semântica não é provada por código.** O motor verifica a forma da")
say("   ligação — que o destino existe, que está no artefacto sob revisão, que não é um")
say("   comentário. Se a secção apontada *diz* o que a obrigação exige é julgamento do")
say("   agente, escrito e assinado (§9 do contrato).")
say("2. **Há fontes que não se capturam.** Um `.pptx`, uma macro, um formato sem extractor")
say("   entram como limitação declarada (`COV-CAPTURE-LIMIT`) e **nunca** como cobertas.")
say("   O que o mecanismo garante é que a limitação aparece, não que desaparece.")
say("3. **O resultado depende do julgamento do agente.** Quais unidades geram obrigações,")
say("   e se uma projecção preserva o que foi pedido, é declarado por quem revê. O motor")
say("   verifica a estrutura da declaração e a sua actualidade — nunca a verdade dela.")
say()
say("## §15.8 — o que esta entrega não declara")
say()
say("O desenho real **não** está aprovado por este trabalho, **não** está declarado")
say("completo por ele e **não** está validado ponta-a-ponta. O E2E demonstrado na fase 6")
say("é o **do protocolo do framework**, em fixture. O E2E da solução de pricing não foi")
say("tentado, não foi medido e não é afirmado em lado nenhum.")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n-> " + str(OUT))
