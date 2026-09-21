# -*- coding: utf-8 -*-
"""Fase 6 — o ensaio isolado do fluxo completo (plano §12, *Fase 6*, ponto 2).

    python docs/runtime-hardening/repro-coverage-phase6-flow-2026-09-16.py

Onze passos, um a seguir ao outro, sobre **uma só** cópia da fixture:

    fontes -> reconciliação -> desenho com perda -> revisão correctiva -> cobertura actual
    -> ausência de aprovação -> aprovação simulada SÓ em fixture -> render com perda
    -> render corrigido -> nova resposta que invalida a cobertura

O que isto demonstra é o **E2E do protocolo do framework**, em fixture: que a sequência de
verificações se comporta como o contrato diz, do princípio ao fim, sem saltos. Não é, e em
nenhum ponto se aproxima de, o E2E da solução de pricing — nenhuma solução é executada,
nenhum dado real é lido, nenhum utilizador aprova nada.

Nenhum engagement real é lido, escrito ou avaliado.
"""
import hashlib
import io
import json
import runpy
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude" / "tests"))
import test_coverage_integration as I          # noqa: E402

ENGINE = ROOT / "library" / "kernel" / "tools" / "coverage.py"
C = runpy.run_path(str(ENGINE))
FIX = ROOT / ".claude" / "tests" / "fixtures" / "coverage" / "fx-coverage-f06"
OUT = ROOT / "docs" / "review-evidence" / "coverage-phase6-flow-2026-09-16.md"

BP01, BP02, BP03 = ("_blueprint/ux-blueprint_v01.yaml",
                    "_blueprint/ux-blueprint_v02.yaml",
                    "_blueprint/ux-blueprint_v03.yaml")
RENDER_V01 = "_render/fx-coverage-f06_solution-blueprint_v01.md"
RENDER_V02 = "_render/fx-coverage-f06_solution-blueprint_v02.md"
APPROVAL = """
## D-003 — Blueprint bp-v03 aprovado

- **Aprovado por**: dono do processo (SIMULADO — fixture, nunca um engagement real)
- **Cobertura consumida**: _coverage/coverage_v04.json
- **Timestamp**: 2026-09-16T10:00:00+01:00
"""

lines = []
steps = []


def say(s=""):
    lines.append(s)
    print(s)


def install(eng, *names, mutate=None):
    (eng / "_coverage").mkdir(exist_ok=True)
    for name in names:
        rec = I.hydrate(eng, I.load(name))
        if mutate:
            mutate(name, rec)
        (eng / "_coverage" / ("coverage_%s.json" % rec["version"])).write_text(
            json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")


def state(eng, stage, rel=None):
    tgt = None if stage == "reconciliation" else {
        "file": rel, "identity": C["target_identity"](eng, stage, rel)}
    return C["coverage_state"](eng, stage, tgt)


def codes(res):
    return sorted({d["code"] for d in res.get("diagnostics", [])
                   if d.get("severity") == "error"})


def step(n, title, res, expect, note=""):
    got = "%s · base %s · %s · elegível %s" % (
        res["contract_validity"], res["freshness"], res["coverage"],
        "sim" if res["eligible"] else "não")
    ok = expect(res)
    steps.append({"n": n, "title": title, "got": got, "codes": codes(res), "ok": ok,
                  "note": note})
    print("%-2s %-8s %-46s %s" % (n, "OK" if ok else "FALHA", title, got))
    return ok


eng = Path(tempfile.mkdtemp(prefix="aisa-ph6-flow-")) / "fx-coverage-f06"
shutil.copytree(FIX, eng)

# ---------------------------------------------------------------- 1. fontes
inv = C["build_inventory"](eng)

# ---------------------------------------------------------------- 2. reconciliação
install(eng, "rec-v01-reconciliation-complete")
s2 = state(eng, "reconciliation")
step(2, "reconciliação completa sobre as fontes", s2,
     lambda r: r["coverage"] == "complete" and r["eligible"])

# ---------------------------------------------------------------- 3. desenho com perda
install(eng, "rec-v02-blueprint-missing")
s3 = state(eng, "blueprint", BP01)
st3 = C["structural_check"](eng, BP01)
step(3, "desenho v01: estrutura válida, requisito perdido", s3,
     lambda r: r["coverage"] == "gaps" and not r["eligible"],
     note="estrutura: %d bloqueio(s)" % st3["blocking"])

# ---------------------------------------------------------------- 4. revisão correctiva
install(eng, "rec-v03-blueprint-partial")
s4 = state(eng, "blueprint", BP02)
step(4, "v02 corrige C-007; C-010 ainda parcial", s4,
     lambda r: r["coverage"] == "gaps" and not r["eligible"])

# ---------------------------------------------------------------- 5. cobertura actual
install(eng, "rec-v04-blueprint-complete")
s5 = state(eng, "blueprint", BP03)
step(5, "v03: cobertura completa e actual", s5,
     lambda r: r["coverage"] == "complete" and r["freshness"] == "current"
     and r["eligible"])

# ---------------------------------------------------------------- 6. ausência de aprovação
appr_before = C["blueprint_versions"](eng)["approved"]
pre_spec_before = C["render_precheck"](eng, "implementation-spec")
steps.append({"n": 6, "title": "cobertura completa NÃO é aprovação",
              "got": "aprovada: %s · a spec resolve: %s (%s)"
                     % (appr_before or "nenhuma",
                        pre_spec_before["expected"]["version"] or "nenhuma versão",
                        pre_spec_before["expected"]["state"]),
              "codes": [], "ok": appr_before is None
              and pre_spec_before["expected"]["version"] is None, "note": ""})
print("%-2s %-8s %-46s %s" % (6, "OK" if steps[-1]["ok"] else "FALHA",
                              steps[-1]["title"], steps[-1]["got"]))

# ---------------------------------------------------------------- 7. aprovação simulada
with io.open(eng / "decisions.md", "a", encoding="utf-8") as fh:
    fh.write(APPROVAL)
s7 = state(eng, "blueprint", BP03)
appr_after = C["blueprint_versions"](eng)["approved"]
step(7, "aprovação (SIMULADA, fixture) não invalida a revisão", s7,
     lambda r: r["freshness"] == "current" and r["coverage"] == "complete",
     note="aprovada: %s" % appr_after)

# ---------------------------------------------------------------- 8. render com perda
install(eng, "rec-neg-render-id-in-comment")
s8 = state(eng, "render", RENDER_V01)
step(8, "render v01: obrigação perdida, id em comentário", s8,
     lambda r: r["coverage"] == "gaps" and not r["eligible"])

# ---------------------------------------------------------------- 9. render corrigido
for p in (eng / "_coverage").glob("coverage_v20.json"):
    p.unlink()
install(eng, "rec-v05-render-complete")
s9 = state(eng, "render", RENDER_V02)
step(9, "render v02: a projecção carrega o que foi pedido", s9,
     lambda r: r["coverage"] == "complete" and r["eligible"])

# ------------------------------------------- 10. nova resposta invalida a cobertura
with io.open(eng / "answers.md", "a", encoding="utf-8") as fh:
    fh.write("\n## U-097\n\nO canal de publicação passa a exigir confirmação de recepção.\n")
s10r = state(eng, "render", RENDER_V02)
s10b = state(eng, "blueprint", BP03)
s10c = state(eng, "reconciliation")
step(10, "resposta nova torna as três etapas stale", s10r,
     lambda r: r["freshness"] == "stale" and not r["eligible"],
     note="desenho: %s · reconciliação: %s" % (s10b["freshness"], s10c["freshness"]))

# ------------------------------------------- 11. a aprovação sobrevive à invalidação
appr_end = C["blueprint_versions"](eng)["approved"]
steps.append({"n": 11, "title": "a aprovação registada sobrevive, e não é revalidada",
              "got": "aprovada: %s · cobertura do desenho: %s"
                     % (appr_end, s10b["coverage"]),
              "codes": [], "ok": appr_end == "v03", "note": ""})
print("%-2s %-8s %-46s %s" % (11, "OK" if steps[-1]["ok"] else "FALHA",
                              steps[-1]["title"], steps[-1]["got"]))

# ---------------------------------------------------------------- relatório
ok_all = all(s["ok"] for s in steps)

say("# Ensaio do fluxo completo — fase 6")
say()
say("Gerado por `docs/runtime-hardening/repro-coverage-phase6-flow-2026-09-16.py` sobre")
say("**uma só** cópia de `.claude/tests/fixtures/coverage/fx-coverage-f06`. Os passos")
say("correm em sequência, no mesmo engagement, como um percurso real correria.")
say()
say("> **O que este ensaio é.** O E2E do **protocolo do framework**: a sequência de")
say("> verificações comporta-se como o contrato diz, do princípio ao fim, sem saltos.")
say(">")
say("> **O que este ensaio não é.** O E2E da **solução de pricing**. Nenhuma solução é")
say("> executada, nenhum dado real é lido, nenhum utilizador aprova nada. A aprovação do")
say("> passo 7 é escrita por este script numa fixture temporária, e está marcada como")
say("> simulada no próprio bloco. Confundir os dois seria a afirmação que todo este")
say("> mecanismo existe para impedir.")
say()
say("**%d de %d passos como esperado.**" % (sum(1 for s in steps if s["ok"]), len(steps)))
say()
say("| # | passo | observado | achados |")
say("|---|---|---|---|")
for s in steps:
    note = (" · " + s["note"]) if s["note"] else ""
    say("| %d | %s%s | %s | %s |" % (
        s["n"], s["title"], "" if s["ok"] else " ⚠️", s["got"] + note,
        ", ".join("`%s`" % c for c in s["codes"]) or "—"))
say()
say("Cinco coisas que este percurso mostra, e que nenhuma responde pela outra:")
say()
say("1. **Estrutura válida não é cobertura** (passo 3): a `v01` passa a verificação")
say("   estrutural com zero bloqueios e mesmo assim perdeu um requisito que a SU carregava.")
say("2. **Cobertura completa não é aprovação** (passo 6): a `v03` fica completa e actual, e")
say("   a versão aprovada continua a não existir — a especificação continua bloqueada.")
say("3. **Aprovar não invalida a revisão que a aprovação consome** (passo 7): o fingerprint")
say("   semântico ignora o bloco de aprovação, ou aprovar tornaria stale a própria base.")
say("4. **Uma resposta nova invalida as três etapas** (passo 10), e invalida-as *como")
say("   stale*, não como reprovadas: a base mudou, e o que se pede é uma releitura.")
say("5. **A aprovação registada sobrevive à invalidação** (passo 11): a cobertura fica por")
say("   rever, e nada revoga o que o negócio já decidiu (§10).")
say()
say("Nenhuma aprovação real foi registada. Nenhuma pergunta em aberto foi respondida.")
say("Nenhum desenho real está aprovado, completo ou validado ponta-a-ponta.")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n-> " + str(OUT))
sys.exit(0 if ok_all else 1)
