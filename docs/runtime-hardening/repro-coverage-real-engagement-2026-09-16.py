# -*- coding: utf-8 -*-
"""O mecanismo de cobertura contra o engagement REAL — `projects/pricing-bunkers-v2`.

    python docs/runtime-hardening/repro-coverage-real-engagement-2026-09-16.py [slug]

Até aqui tudo correu sobre a fixture (79 unidades, 3 desenhos, 5 registos). O engagement
real tem outra ordem de grandeza — ~1050 unidades, 9 desenhos, 13 registos, 11 deliverables
produzidos — e é aí que uma validação só por fixture é fraca.

Duas partes, e a fronteira entre elas é o que protege o engagement:

  A. **Sobre o original, só leitura.** Manifesto SHA-256 antes e depois. Diz o que o
     mecanismo responde hoje sobre o trabalho real.
  B. **Sobre uma CÓPIA temporária.** Os cenários que precisam de mutar alguma coisa —
     atualidade, unidades por rever, selecção entre registos, a classe §4.5.1 — correm
     contra as formas reais dos dados, e nunca contra o original.

O que este ficheiro **não** faz: não revê cobertura nenhuma, não responde a perguntas em
aberto, não regista nem toca aprovações, e não corre `finalize` sobre o original.
"""
import hashlib
import io
import json
import os
import re
import runpy
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude" / "tests"))

ENGINE = ROOT / "library" / "kernel" / "tools" / "coverage.py"
C = runpy.run_path(str(ENGINE))
SLUG = sys.argv[1] if len(sys.argv) > 1 else "pricing-bunkers-v2"
ENG = ROOT / "projects" / SLUG
OUT = ROOT / "docs" / "review-evidence" / ("coverage-real-%s-2026-09-16.md" % SLUG)

lines = []
partA, partB = [], []


def say(s=""):
    lines.append(s)
    print(s)


def manifest(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file()}


def state(eng, stage, rel=None):
    tgt = None if stage == "reconciliation" else {
        "file": rel, "identity": C["target_identity"](eng, stage, rel)}
    return C["coverage_state"](eng, stage, tgt)


def codes(res):
    return sorted({d["code"] for d in res.get("diagnostics", [])
                   if d.get("severity") == "error"})


def verdict(res):
    return "%s · %s · %s · %s · **%s** · %s" % (
        res["contract_validity"], res["freshness"], res["source_review"],
        res["semantic_review"], res["coverage"],
        "pode avançar" if res["eligible"] else "não avança")


def case(bucket, name, expected, observed, ok):
    bucket.append({"name": name, "expected": expected, "observed": observed, "ok": ok})
    print("%-9s %-58s %s" % ("OK" if ok is True else
                             ("INCONCLUSIVO" if ok is None else "FALHA"), name, observed))


if not ENG.is_dir():
    print("engagement não montado: %s" % ENG)
    sys.exit(2)

# =====================================================================  PARTE A
before = manifest(ENG)
inv = C["build_inventory"](ENG)
recs = sorted((ENG / "_coverage").glob("coverage_v*.json")) \
    if (ENG / "_coverage").is_dir() else []
stages = {}
for p in recs:
    d = json.loads(p.read_text(encoding="utf-8"))
    stages.setdefault(d.get("stage"), []).append(p.name)

bps = sorted((ENG / "_blueprint").glob("ux-blueprint_v*.yaml")) \
    if (ENG / "_blueprint").is_dir() else []
renders = sorted(p for p in (ENG / "_render").glob("*_v*.md")) \
    if (ENG / "_render").is_dir() else []
# O último de cada deliverable: é o que um render novo consumiria.
latest = {}
for p in renders:
    m = re.match(r"^(?P<slug>.+?)_(?P<d>[a-z-]+)_v(?P<n>\d+)\.md$", p.name)
    if m:
        latest[m.group("d")] = max(latest.get(m.group("d"), p), p, key=lambda x: x.name)

recon = state(ENG, "reconciliation")
case(partA, "reconciliação: o que o registo em vigor diz",
     "um veredicto, qualquer que seja", verdict(recon), True)

for bp in bps:
    r = state(ENG, "blueprint", "_blueprint/" + bp.name)
    case(partA, "desenho %s" % bp.stem.split("_")[-1],
         "not_evaluated onde não há revisão; veredicto onde há", verdict(r), True)

for d in ("discovery-report", "executive-report", "solution-blueprint",
          "implementation-spec", "claude-design-brief", "estimate"):
    pre = C["render_precheck"](ENG, d)
    case(partA, "pré-render %s" % d, "a versão que o contrato manda ler",
         "%s → %s (%s) · %d impeditivo(s)"
         % (pre["declared"], pre["expected"]["version"] or "nenhuma",
            pre["expected"]["state"], pre["blocking"]), pre["blocking"] == 0)

for d, p in sorted(latest.items()):
    r = state(ENG, "render", "_render/" + p.name)
    case(partA, "projecção %s" % p.name, "not_evaluated sem registo de render",
         verdict(r), True)

after = manifest(ENG)
changed = sorted(set(before) ^ set(after)) + \
    sorted(k for k in set(before) & set(after) if before[k] != after[k])
case(partA, "o original ficou como estava", "0 ficheiros alterados",
     "%d alterado(s) em %d" % (len(changed), len(before)), not changed)

# =====================================================================  PARTE B
tmp = Path(tempfile.mkdtemp(prefix="aisa-real-"))
COPY = tmp / SLUG
shutil.copytree(ENG, COPY)


def fresh_copy():
    d = Path(tempfile.mkdtemp(prefix="aisa-real-"))
    shutil.copytree(ENG, d / SLUG)
    return d / SLUG


base_recon = state(COPY, "reconciliation")
BASE_FRESH = base_recon["freshness"]

# -- atualidade: o que TEM de invalidar
for name, mutate in (
    ("fonte nova em `inputs/`",
     lambda e: (e / "inputs" / "fonte-nova.xlsx").write_bytes(b"PK\x03\x04 nova")),
    ("workbook alterado",
     lambda e: next((e / "inputs").glob("*.xls*")).write_bytes(
         next((e / "inputs").glob("*.xls*")).read_bytes() + b"\x00x")),
    ("resposta nova em `answers.md`",
     lambda e: io.open(e / "answers.md", "a", encoding="utf-8").write(
         "\n## U-901\n\nRegra nova acrescentada pelo ensaio.\n")),
    ("decisão-solução alterada",
     lambda e: (e / "decisions.md").write_text(
         (e / "decisions.md").read_text(encoding="utf-8").replace(
             "Adopt O-004", "Adopt O-004 (âmbito alterado pelo ensaio)"),
         encoding="utf-8")),
):
    e = fresh_copy()
    mutate(e)
    r = state(e, "reconciliation")
    case(partB, "invalida: " + name, "stale", r["freshness"], r["freshness"] == "stale")

# -- atualidade: o que NÃO pode invalidar
e = fresh_copy()
for rel in ("dashboard.html", "story.md", "_render/render-log.md",
            "_capture/_capture-log.md"):
    p = e / rel
    if p.is_file():
        with io.open(p, "a", encoding="utf-8") as fh:
            fh.write("\nlinha derivada acrescentada pelo ensaio\n")
r = state(e, "reconciliation")
case(partB, "não invalida: derivados (dashboard, story, logs)", BASE_FRESH,
     r["freshness"], r["freshness"] == BASE_FRESH)

e = fresh_copy()
with io.open(e / "decisions.md", "a", encoding="utf-8") as fh:
    fh.write("\n## D-999 — Blueprint bp-v09 aprovado\n\n- **Aprovado por**: ensaio\n"
             "- **Timestamp**: 2026-09-16T18:00:00+01:00\n")
r = state(e, "reconciliation")
case(partB, "não invalida: acrescentar uma aprovação", BASE_FRESH, r["freshness"],
     r["freshness"] == BASE_FRESH)

# -- o desenho alterado depois da revisão
if bps:
    e = fresh_copy()
    target = "_blueprint/" + bps[-1].name
    b0 = state(e, "blueprint", target)
    (e / target).write_text((e / target).read_text(encoding="utf-8")
                            + "\n# comentário do ensaio\n", encoding="utf-8")
    b1 = state(e, "blueprint", target)
    case(partB, "desenho alterado depois da revisão", "stale (se havia revisão actual)",
         "%s → %s" % (b0["freshness"], b1["freshness"]),
         b1["freshness"] == "stale" or b0["freshness"] != "current")

# -- unidade por rever, à escala real
e = fresh_copy()
sel = C["select_record"](e, "reconciliation", None)
entry = sel["selected"]
if entry:
    rec = entry["record"]
    victim = None
    for sr in rec.get("source_review", []):
        if sr.get("unit_refs"):
            victim = sr
            break
    if victim:
        rec["source_review"] = [s for s in rec["source_review"] if s is not victim]
        (e / "_coverage" / entry["file"].split("/")[-1]).write_text(
            json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
        r = state(e, "reconciliation")
        case(partB, "unidade sem tratamento, em ~%d" % inv["total"],
             "COV-UNREVIEWED", ",".join(codes(r)) or "sem achados",
             "COV-UNREVIEWED" in codes(r))
    else:
        case(partB, "unidade sem tratamento", "COV-UNREVIEWED",
             "o registo em vigor não tem `source_review` com unidades", None)
else:
    case(partB, "unidade sem tratamento", "COV-UNREVIEWED",
         "não há registo de reconciliação para partir", None)

# -- selecção entre 13 registos: a mais recente do par manda
if entry:
    e = fresh_copy()
    good = state(e, "reconciliation")
    rec = json.loads((e / "_coverage" / entry["file"].split("/")[-1])
                     .read_text(encoding="utf-8"))
    nxt = "coverage_v%02d.json" % (int(re.search(r"v(\d+)", entry["file"]).group(1)) + 90)
    rec["version"] = "v%02d" % (int(re.search(r"v(\d+)", entry["file"]).group(1)) + 90)
    for it in rec.get("coverage", [])[:1]:
        it["assessment"]["status"] = "missing"
        it["required_action"] = "fechar a lacuna (ensaio)"
        it["responsible_role"] = "arquitectura"
        rec.setdefault("semantic_review", {}).setdefault("findings", []).append(it["id"])
    (e / "_coverage" / nxt).write_text(json.dumps(rec, ensure_ascii=False, indent=2),
                                       encoding="utf-8")
    newer = state(e, "reconciliation")
    case(partB, "a revisão mais recente manda, mesmo com lacuna",
         "escolhe a nova e mostra gaps",
         "%s → %s (%s)" % (good["coverage"], newer["coverage"],
                           (newer.get("record") or {}).get("file", "—")),
         (newer.get("record") or {}).get("file", "").endswith(nxt))

# -- registo ilegível não se lê como ausente
e = fresh_copy()
(e / "_coverage" / "coverage_v98.json").write_text("{ partido", encoding="utf-8")
r = state(e, "reconciliation")
case(partB, "registo partido não passa por «ainda não há»", "invalid",
     r["contract_validity"], r["contract_validity"] == "invalid")

# -- schema futuro
if entry:
    e = fresh_copy()
    rec = json.loads((e / "_coverage" / entry["file"].split("/")[-1])
                     .read_text(encoding="utf-8"))
    rec["schema_version"] = 99
    (e / "_coverage" / entry["file"].split("/")[-1]).write_text(
        json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
    r = state(e, "reconciliation")
    case(partB, "schema futuro não se interpreta por aproximação", "unsupported",
         "%s · cobertura %s" % (r["contract_validity"], r["coverage"]),
         r["contract_validity"] == "unsupported" and r["coverage"] == "not_evaluated")

# -- fronteira de caminhos
e = fresh_copy()
out = C["resolve_target"](e, {"file": "../fora.md", "selector": "A1"})
case(partB, "traversal recusado sem ler", "recusado",
     "%s" % out.get("code"), not out["ok"])

# -- determinismo e zero escrita na cópia
e = fresh_copy()
m0 = manifest(e)
a = state(e, "reconciliation")
b = state(e, "reconciliation")
m1 = manifest(e)
same = all(a[k] == b[k] for k in ("contract_validity", "freshness", "source_review",
                                  "semantic_review", "coverage", "eligible"))
case(partB, "duas leituras: mesmo resultado, zero escrita", "idêntico e 0 alterações",
     "idêntico %s · %d alterado(s)" % (same, sum(1 for k in m0 if m0[k] != m1.get(k))),
     same and m0 == m1)

# =====================================================================  relatório
okA = sum(1 for c in partA if c["ok"] is True)
okB = sum(1 for c in partB if c["ok"] is True)
badB = [c for c in partB if c["ok"] is False]
incB = [c for c in partB if c["ok"] is None]

say("# O mecanismo de cobertura contra o engagement real")
say()
say("Engagement: `projects/%s` · gerado por" % SLUG)
say("`docs/runtime-hardening/repro-coverage-real-engagement-2026-09-16.py`.")
say()
say("| | |")
say("|---|---|")
say("| fase | %s · ronda %s · pacote `%s` |" % (
    json.loads((ENG / "_state.json").read_text(encoding="utf-8")).get("phase"),
    json.loads((ENG / "_state.json").read_text(encoding="utf-8")).get("round"),
    json.loads((ENG / "_state.json").read_text(encoding="utf-8")).get("pack")))
say("| unidades no denominador | **%d** (a fixture tem 79) |" % inv["total"])
say("| ficheiros | %d |" % len(before))
say("| desenhos | %d |" % len(bps))
say("| deliverables produzidos | %d |" % len(renders))
say("| registos de cobertura | %d — %s |" % (
    len(recs), " · ".join("%s: %d" % (k, len(v)) for k, v in sorted(stages.items()))))
say()
say("> **O que este ensaio não faz.** Não revê cobertura nenhuma, não responde a perguntas")
say("> em aberto, não regista nem toca aprovações, e não corre `finalize` sobre o")
say("> original. A parte A é leitura; a parte B corre sobre **cópias temporárias**.")
say()
say("## A. Sobre o original, só leitura")
say()
say("| o que se perguntou | o que o mecanismo respondeu |")
say("|---|---|")
for c in partA:
    say("| %s | %s |" % (c["name"], c["observed"]))
say()
say("## B. Sobre cópias, os cenários que precisam de mutar")
say()
say("**%d de %d como esperado**%s." % (okB, len(partB),
                                       "" if not incB else
                                       " · %d inconclusivo(s)" % len(incB)))
say()
say("| cenário | esperado | observado | |")
say("|---|---|---|---|")
for c in partB:
    say("| %s | %s | %s | %s |" % (
        c["name"], c["expected"], c["observed"],
        "OK" if c["ok"] is True else ("**inconclusivo**" if c["ok"] is None
                                      else "**FALHA**")))
say()

# =====================================================================  PARTE C
say("## C. Os testes da suite que lêem este engagement")
say()
SUITE = ("test_blueprint_yaml", "test_coverage_integration", "test_coverage_inventory",
         "test_coverage_phase4", "test_hook_invocation", "test_hooks_gates",
         "test_motor_identity", "test_options_artefact", "test_round_in_progress",
         "test_status_model", "test_step8c_semantic_continuity")
say("| ficheiro | testes | resultado |")
say("|---|---|---|")
env = dict(os.environ)
env["PYTHONIOENCODING"] = "utf-8"
suite_fail = []
for name in SUITE:
    r = subprocess.run([sys.executable, "-B", str(ROOT / ".claude" / "tests" /
                                                  (name + ".py"))], cwd=str(ROOT),
                       env=env, text=True, capture_output=True, encoding="utf-8",
                       errors="replace")
    body = r.stdout + r.stderr
    n = re.search(r"^Ran (\d+) test", body, re.M)
    sk = re.search(r"skipped=(\d+)", body)
    if r.returncode:
        suite_fail.append(name)
    say("| `%s.py` | %s | %s%s |" % (
        name, n.group(1) if n else "?", "ok" if not r.returncode else "**FALHA**",
        " · %s saltado(s)" % sk.group(1) if sk else ""))
say()
say("**%d de %d verdes.**" % (len(SUITE) - len(suite_fail), len(SUITE)))
say()

# O que a falha mede, em concreto — é conteúdo do engagement, não do mecanismo.
opts = ENG / "options.md"
if opts.is_file():
    over = []
    for b in re.split(r"^### ", opts.read_text(encoding="utf-8"), flags=re.M):
        if b.startswith("O-"):
            w = len(b.split())
            if w > 160:
                over.append((b.split()[0].rstrip(":—-"), w))
    if over:
        say("`test_options_artefact.py` falha sobre `options.md` **deste** engagement: o")
        say("contrato orça a prosa em 120 palavras por opção, com tecto de 160 (o tecto é")
        say("um terço acima do orçamento, de propósito — é contrato, não régua). Acima do")
        say("tecto:")
        say()
        say("| opção | palavras | acima do tecto em |")
        say("|---|---:|---:|")
        for oid, w in over:
            say("| %s | %d | %d |" % (oid, w, w - 160))
        say()
        say("O teste reporta a primeira que encontra; são **%d**. Isto é conteúdo do"
            % len(over))
        say("engagement, não do mecanismo de cobertura — encurtá-lo é decisão de quem o")
        say("conduz, e `projects/` não está sob git neste checkout.")
        say()
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n-> " + str(OUT))
sys.exit(1 if badB else 0)
