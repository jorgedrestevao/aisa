# -*- coding: utf-8 -*-
"""Fase 6 — os 40 cenários do plano §13, executados um a um sobre a fixture.

    python docs/runtime-hardening/repro-coverage-phase6-matrix-2026-09-16.py

Não substitui as suites: **executa o cenário** e compara o veredicto observado com o que o
plano exige, para que a matriz seja uma medição e não um mapeamento por citação. Cada linha
diz onde o cenário também vive como teste nomeado.

Um cenário que este executor não consiga montar sai **INCONCLUSIVO**, nunca OK — a fase 1
aprendeu isso da pior maneira ("inconclusivo lido como verde", P-15).

Nenhum engagement real é lido, escrito ou avaliado.
"""
import hashlib
import io
import json
import os
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
C = runpy.run_path(str(ENGINE))
FIX = ROOT / ".claude" / "tests" / "fixtures" / "coverage" / "fx-coverage-f06"
OUT = ROOT / "docs" / "review-evidence" / "coverage-phase6-matrix-2026-09-16.md"

RECON = "rec-v01-reconciliation-complete"
CHAIN_BP = (RECON, "rec-v02-blueprint-missing", "rec-v03-blueprint-partial",
            "rec-v04-blueprint-complete")
BP01, BP02, BP03 = ("_blueprint/ux-blueprint_v01.yaml",
                    "_blueprint/ux-blueprint_v02.yaml",
                    "_blueprint/ux-blueprint_v03.yaml")
RENDER_V01 = "_render/fx-coverage-f06_solution-blueprint_v01.md"
RENDER_V02 = "_render/fx-coverage-f06_solution-blueprint_v02.md"
SPEC_TPL = "library/packs/pp/deliverable-templates/implementation-spec.template.md"
ARCH_TPL = "library/packs/pp/deliverable-templates/solution-blueprint.template.md"
APPROVAL = """
## D-003 — Blueprint bp-v03 aprovado

- **Aprovado por**: dono do processo
- **Cobertura consumida**: _coverage/coverage_v04.json
- **Timestamp**: 2026-09-16T10:00:00+01:00
"""

rows = []
lines = []


def say(s=""):
    lines.append(s)
    print(s)


def fresh():
    tmp = Path(tempfile.mkdtemp(prefix="aisa-ph6-"))
    eng = tmp / "fx-coverage-f06"
    shutil.copytree(FIX, eng)
    return eng


def install(eng, *names, mutate=None):
    shutil.rmtree(eng / "_coverage", ignore_errors=True)
    (eng / "_coverage").mkdir()
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


def record(tid, what, expected, observed, ok, where):
    rows.append({"id": tid, "what": what, "expected": expected,
                 "observed": observed, "ok": ok, "where": where})
    print("%-5s %-9s %s" % (tid, "OK" if ok is True else
                            ("INCONCLUSIVO" if ok is None else "FALHA"), what))


def scenario(tid, what, where, fn):
    """Corre o cenário. Uma excepção é INCONCLUSIVO, nunca OK."""
    try:
        expected, observed, ok = fn()
    except Exception as exc:                                        # noqa: BLE001
        record(tid, what, "—", "%s: %s" % (type(exc).__name__, exc), None, where)
        return
    record(tid, what, expected, observed, ok, where)


# ============================================================ T01 - T04
def t01():
    eng = fresh()
    install(eng, RECON, "rec-v02-blueprint-missing")
    res = state(eng, "blueprint", BP01)
    st = C["structural_check"](eng, BP01)
    obs = "estrutura %d bloqueio(s) · cobertura %s" % (st["blocking"], res["coverage"])
    return "estrutura válida · cobertura gaps", obs, st["blocking"] == 0 and res["coverage"] == "gaps"


def t02():
    eng = fresh()
    install(eng, RECON, "rec-neg-decorative-projection")
    res = state(eng, "blueprint", BP01)
    return ("COV-MISSING-TARGET · não satisfeito", "%s · %s" % (",".join(codes(res)),
                                                                res["coverage"]),
            "COV-MISSING-TARGET" in codes(res) and res["coverage"] == "gaps")


def t03():
    eng = fresh()
    install(eng, *CHAIN_BP)
    res = state(eng, "blueprint", BP03)
    appr = C["blueprint_versions"](eng)["approved"]
    return ("cobertura complete · aprovação ausente",
            "cobertura %s · aprovada %s" % (res["coverage"], appr or "nenhuma"),
            res["coverage"] == "complete" and appr is None)


def t04():
    """Obrigação numa resposta que a SU não carrega: a unidade continua no denominador,
    e omitir a linha de cobertura não dá verde."""
    eng = fresh()
    inv = C["build_inventory"](eng)
    keys = {u["unit_key"] for u in inv["units"]}
    answer_units = {k for k in keys if k.startswith("answers.md#")}
    install(eng, RECON)
    # Retira UMA entrada de revisão: a unidade continua a existir, e o verde tem de cair.
    victim = sorted(answer_units)[0]

    def drop(name, rec):
        rec["source_review"] = [e for e in rec["source_review"]
                                if victim not in e.get("unit_refs", [])]
    install(eng, RECON, mutate=drop)
    res = state(eng, "reconciliation")
    return ("unidade sem tratamento → COV-UNREVIEWED",
            "%s · %s" % (",".join(codes(res)), res["source_review"]),
            "COV-UNREVIEWED" in codes(res) and res["source_review"] == "incomplete")


# ============================================================ T05 - T10
def t05():
    eng = fresh()

    def drop_sheet(name, rec):
        rec["source_review"] = [e for e in rec["source_review"]
                                if not any(".xlsx" in u for u in e.get("unit_refs", []))]
    install(eng, RECON, mutate=drop_sheet)
    res = state(eng, "reconciliation")
    return "COV-UNREVIEWED", ",".join(codes(res)), "COV-UNREVIEWED" in codes(res)


def t06():
    eng = fresh()
    install(eng, RECON)
    (eng / "inputs" / "nova-fonte.xlsx").write_bytes(b"PK\x03\x04 fonte nova")
    res = state(eng, "reconciliation")
    return ("stale ou unreviewed", "atualidade %s · %s" % (res["freshness"],
                                                           ",".join(codes(res))),
            res["freshness"] == "stale" or "COV-UNREVIEWED" in codes(res))


def t07():
    eng = fresh()
    install(eng, RECON)
    wb = next((eng / "inputs").glob("*.xlsx"))
    wb.write_bytes(wb.read_bytes() + b"\x00alterado")
    res = state(eng, "reconciliation")
    return "stale", res["freshness"], res["freshness"] == "stale"


def t08():
    eng = fresh()
    install(eng, "rec-neg-capture-limit-as-covered")
    res = state(eng, "reconciliation")
    return "COV-CAPTURE-LIMIT", ",".join(codes(res)), "COV-CAPTURE-LIMIT" in codes(res)


def t09():
    eng = fresh()
    inv = C["build_inventory"](eng)
    keys = [u["unit_key"] for u in inv["units"]]
    dupes = [k for k in set(keys) if keys.count(k) > 1]
    two = sorted({k.split("#")[0] for k in keys if k.endswith("#Outputs/A")})
    return ("sem colisão de chaves entre workbooks",
            "%d chaves, %d repetidas; ficheiros com `Outputs`: %d"
            % (len(keys), len(dupes), len(two)), not dupes)


def t10():
    eng = fresh()
    inv = C["build_inventory"](eng)
    keys = {u["unit_key"] for u in inv["units"]}
    members = sorted(k for k in keys if "Custo_Posto_" in k)
    install(eng, RECON)
    before = state(eng, "reconciliation")

    def drop_one(name, rec):
        for e in rec["source_review"]:
            if any("Custo_Posto_" in u for u in e.get("unit_refs", [])):
                e["unit_refs"] = [u for u in e["unit_refs"] if "Custo_Posto_D" not in u]
    install(eng, RECON, mutate=drop_one)
    after = state(eng, "reconciliation")
    return ("grupo aceite, membro omitido detectado",
            "%d membros · com todos: %s · sem um: %s"
            % (len(members), before["source_review"], after["source_review"]),
            before["source_review"] == "complete"
            and after["source_review"] == "incomplete")


# ============================================================ T11 - T15
def t11():
    eng = fresh()
    install(eng, RECON, "rec-neg-dead-ref")
    res = state(eng, "blueprint", BP01)
    got = codes(res)
    return ("COV-DEAD-REF e/ou COV-INVALID-TARGET", ",".join(got),
            "COV-DEAD-REF" in got or "COV-INVALID-TARGET" in got)


def t12():
    eng = fresh()
    install(eng, RECON, "rec-neg-decorative-invalid-target")
    res = state(eng, "blueprint", BP01)
    return ("COV-INVALID-TARGET", ",".join(codes(res)),
            "COV-INVALID-TARGET" in codes(res))


def t13():
    eng = fresh()
    install(eng, RECON, "rec-neg-exclusion-no-decision")
    a = codes(state(eng, "blueprint", BP01))
    eng2 = fresh()
    install(eng2, RECON, "rec-neg-exclusion-undetermined")
    b = codes(state(eng2, "blueprint", BP01))
    return ("COV-EXCLUSION-NO-DECISION · COV-REVIEW-INCOMPLETE",
            "sem decisão: %s | materialidade por declarar: %s"
            % (",".join(a), ",".join(b)),
            "COV-EXCLUSION-NO-DECISION" in a and "COV-REVIEW-INCOMPLETE" in b)


def t14():
    eng = fresh()
    install(eng, RECON, "rec-v03-blueprint-partial", "rec-pos-exclusion-mechanical")
    res = state(eng, "blueprint", BP02)
    return ("exclusão mecânica aceite (sem COV-EXCLUSION-NO-DECISION)",
            ",".join(codes(res)) or "sem achados",
            "COV-EXCLUSION-NO-DECISION" not in codes(res))


def t15():
    eng = fresh()
    install(eng, RECON, "rec-v02-blueprint-missing", "rec-v03-blueprint-partial")
    res = state(eng, "blueprint", BP02)
    return ("gaps por lacuna material conhecida", res["coverage"],
            res["coverage"] == "gaps")


# ============================================================ T16 - T21
def t16():
    eng = fresh()
    install(eng, RECON)
    su = eng / "shared-understanding.md"
    rows_ = C["ReaderAdapter"]().parse_su(su.read_text(encoding="utf-8"))[1]
    assumed = [r for r in rows_ if r.get("state") == "Assumed"]
    res = state(eng, "reconciliation")
    return ("Assumed continua Assumed; nenhum upgrade",
            "%d linhas Assumed · cobertura %s" % (len(assumed), res["coverage"]),
            bool(assumed) and res["coverage"] in ("complete", "gaps"))


def t17():
    eng = fresh()
    install(eng, RECON)
    with io.open(eng / "answers.md", "a", encoding="utf-8") as fh:
        fh.write("\n## U-099\n\nRegra nova que substitui a anterior.\n")
    res = state(eng, "reconciliation")
    return ("stale", res["freshness"], res["freshness"] == "stale")


def t18():
    eng = fresh()
    install(eng, RECON)
    before = state(eng, "reconciliation")["freshness"]
    for rel in ("story.md", "dashboard.html", "_capture/_capture-log.md"):
        p = eng / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        with io.open(p, "a", encoding="utf-8") as fh:
            fh.write("\nlinha derivada acrescentada\n")
    after = state(eng, "reconciliation")["freshness"]
    return ("current antes e depois", "%s -> %s" % (before, after),
            before == "current" and after == "current")


def t19():
    eng = fresh()
    install(eng, *CHAIN_BP)
    before = state(eng, "blueprint", BP03)["freshness"]
    with io.open(eng / "decisions.md", "a", encoding="utf-8") as fh:
        fh.write(APPROVAL)
    after = state(eng, "blueprint", BP03)
    return ("current antes e depois; aprova só a v03",
            "%s -> %s · aprovada %s" % (before, after["freshness"],
                                        C["blueprint_versions"](eng)["approved"]),
            before == "current" and after["freshness"] == "current"
            and C["blueprint_versions"](eng)["approved"] == "v03")


def t20():
    eng = fresh()
    install(eng, RECON)
    dec = eng / "decisions.md"
    txt = dec.read_text(encoding="utf-8")
    dec.write_text(txt.replace("aplicação com base de dados governada",
                               "aplicação com base de dados governada (âmbito alterado)"),
                   encoding="utf-8")
    res = state(eng, "reconciliation")
    return "stale", res["freshness"], res["freshness"] == "stale"


def t21():
    eng = fresh()
    install(eng, *CHAIN_BP)
    bp = eng / BP03
    bp.write_text(bp.read_text(encoding="utf-8") + "\n# comentário acrescentado\n",
                  encoding="utf-8")
    res = state(eng, "blueprint", BP03)
    return "stale", res["freshness"], res["freshness"] == "stale"


# ============================================================ T22 - T25
def t22():
    eng = fresh()
    install(eng, *CHAIN_BP, "rec-neg-authority-mismatch")
    res = state(eng, "render", RENDER_V02)
    return ("COV-AUTHORITY-MISMATCH", ",".join(codes(res)),
            "COV-AUTHORITY-MISMATCH" in codes(res))


def t23():
    eng = fresh()
    install(eng, *CHAIN_BP, "rec-v05-render-complete")
    newer = json.loads((eng / "_coverage" / "coverage_v05.json").read_text(encoding="utf-8"))
    newer["version"] = "v06"
    newer["coverage"][0]["assessment"]["status"] = "missing"
    newer["coverage"][0]["required_action"] = "projectar a publicação"
    newer["coverage"][0]["responsible_role"] = "arquitectura"
    newer["semantic_review"]["findings"] = ["item-001"]
    (eng / "_coverage" / "coverage_v06.json").write_text(
        json.dumps(newer, ensure_ascii=False, indent=2), encoding="utf-8")
    res = state(eng, "render", RENDER_V02)
    return ("escolhe a v06 e mostra gaps",
            "%s · %s" % (res["record"]["file"], res["coverage"]),
            res["record"]["file"].endswith("v06.json") and res["coverage"] == "gaps")


def t24():
    eng = fresh()
    install(eng, *CHAIN_BP, "rec-v05-render-complete")
    (eng / "_coverage" / "coverage_v06.json").write_text("{ partido", encoding="utf-8")
    a = state(eng, "render", RENDER_V02)
    eng2 = fresh()

    def future(name, rec):
        if rec.get("stage") == "render":
            rec["schema_version"] = 99
    install(eng2, *CHAIN_BP, "rec-v05-render-complete", mutate=future)
    b = state(eng2, "render", RENDER_V02)
    eng3 = fresh()
    c = state(eng3, "render", RENDER_V02)
    return ("invalid · unsupported · not_evaluated, nenhum verde",
            "%s · %s · %s" % (a["contract_validity"], b["contract_validity"],
                              c["contract_validity"]),
            a["contract_validity"] == "invalid"
            and b["contract_validity"] == "unsupported"
            and c["contract_validity"] == "not_evaluated"
            and not any(x["eligible"] for x in (a, b, c)))


def t25():
    """Hooks que não dispararam: o check explícito continua disponível e documentado."""
    eng = fresh()
    install(eng, *CHAIN_BP)
    r = cli("check", "--engagement", str(eng), "--stage", "blueprint", "--target", BP03)
    # As duas skills que correm o motor dizem-no, e é a frase que o prende: um hook que
    # não disparou perde visibilidade, não perde a verificação.
    documented = all(
        "the hook is a convenience, never the mechanism"
        in (ROOT / ".claude" / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
        for name in ("aisa-blueprint", "aisa-render"))
    return ("CLI corre sem hook · e está documentado",
            "exit %d · documentado %s" % (r.returncode, documented),
            r.returncode == 0 and documented)


def cli(*args, cwd=None):
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run([sys.executable, "-B", str(ENGINE), *args],
                          cwd=str(cwd or ROOT), env=env, text=True, capture_output=True,
                          encoding="utf-8", errors="replace")


# ============================================================ T26 - T30
def t26():
    eng = fresh()
    weird = eng.parent / "pasta com espaços e acentuação"
    weird.mkdir()
    shutil.copytree(eng, weird / "fx-coverage-f06")
    install(weird / "fx-coverage-f06", RECON)
    r = cli("check", "--engagement", str(weird / "fx-coverage-f06"),
            "--stage", "reconciliation", cwd=weird)
    return ("resolve, exit 0", "exit %d" % r.returncode, r.returncode == 0)


def t27():
    root = Path(tempfile.mkdtemp(prefix="aisa-ph6-multi-"))
    for slug in ("um", "dois"):
        shutil.copytree(FIX, root / slug)
    env = dict(os.environ)
    env["AISA_ENGAGEMENTS_ROOT"] = str(root)
    env["PYTHONIOENCODING"] = "utf-8"
    r = subprocess.run([sys.executable, "-B", str(ENGINE), "inventory"], cwd=str(ROOT),
                       env=env, text=True, capture_output=True, encoding="utf-8",
                       errors="replace")
    return ("falha explícita, sem escolher", "exit %d · %s" % (r.returncode,
                                                               r.stderr.strip()[:60]),
            r.returncode != 0)


def t28():
    eng = fresh()
    out = C["resolve_target"](eng, {"file": "../fora.md", "selector": "A1"})
    outside = eng.parent / "fora.md"
    outside.write_text("# A1\nconteudo\n", encoding="utf-8")
    out2 = C["resolve_target"](eng, {"file": "../fora.md", "selector": "A1"})
    return ("recusado nos dois casos",
            "sem ficheiro: %s · com ficheiro: %s" % (out["code"], out2["code"]),
            not out["ok"] and not out2["ok"])


def t29():
    eng = fresh()
    install(eng, RECON)
    draft = eng.parent / "draft.json"
    rec = I.hydrate(eng, I.load(RECON))
    draft.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
    taken = eng / "_coverage" / "coverage_v01.json"
    before = taken.read_bytes()
    out = C["finalize"](eng, draft)
    return ("não sobrescreve a v01 e publica outra versão",
            "publicou %s · v01 intacta %s" % (out.get("version"),
                                              taken.read_bytes() == before),
            out.get("version") != "v01" and taken.read_bytes() == before)


def t30():
    eng = fresh()

    def pending(name, rec):
        rec["semantic_review"]["status"] = "pending"
        rec["semantic_review"]["passes"] = {"source_to_target": True,
                                            "target_to_source": False}
    install(eng, RECON, "rec-v04-blueprint-complete", mutate=pending)
    res = state(eng, "blueprint", BP03)
    return ("não completa por referências válidas",
            "semântica %s · elegível %s" % (res["semantic_review"], res["eligible"]),
            res["semantic_review"] == "pending" and not res["eligible"])


# ============================================================ T31 - T35
def t31():
    eng = fresh()
    a = C["render_precheck"](eng, "solution-blueprint")
    b = C["render_precheck"](eng, "implementation-spec")
    c = C["render_precheck"](eng, "claude-design-brief")
    return ("arquitectura lê a autorizada; spec e brief a aprovada",
            "arq %s(%s) · spec %s · brief %s" % (a["expected"]["version"],
                                                 a["declared"], b["declared"],
                                                 c["declared"]),
            a["expected"]["version"] == "v03"
            and a["declared"] == "v<latest authorized>"
            and b["declared"] == "v<approved>" and c["declared"] == "v<approved>")


def t32():
    eng = fresh()
    sha = hashlib.sha256((eng / RENDER_V01).read_bytes()).hexdigest()

    def comment(name, rec):
        if rec.get("stage") != "render":
            return
        rec["target"].update({"file": RENDER_V01, "identity": "solution-blueprint_v01",
                              "sha256": sha})
        for it in rec["coverage"]:
            for tg in it["targets"]:
                tg["file"] = RENDER_V01
            if it["id"] == "item-001":
                it["targets"] = [{"file": RENDER_V01, "selector": "A3/C-007",
                                  "kind": "section", "role": "projection"}]
    install(eng, *CHAIN_BP, "rec-v05-render-complete", mutate=comment)
    res = state(eng, "render", RENDER_V01)
    raw = C["resolve_target"](eng, {"file": RENDER_V01, "selector": "A3/C-007"})
    return ("locator resolve e mesmo assim não é âncora",
            "resolve=%s comment_only=%s · cobertura %s"
            % (raw["ok"], raw.get("comment_only"), res["coverage"]),
            raw["ok"] and raw.get("comment_only") and res["coverage"] == "gaps")


def t33():
    eng = fresh()
    install(eng, *CHAIN_BP, "rec-neg-render-id-in-comment")
    before = manifest(eng, skip=("_coverage/",))
    res = state(eng, "render", RENDER_V01)
    state(eng, "render", RENDER_V01)
    after = manifest(eng, skip=("_coverage/",))
    return ("gaps explícitos e zero escrita a montante",
            "cobertura %s · %d achado(s) · ficheiros alterados %d"
            % (res["coverage"], len(codes(res)), len(set(before.items()) ^ set(after.items()))),
            res["coverage"] == "gaps" and before == after)


def t34():
    eng = fresh()
    for p in (eng / "_blueprint").glob("ux-blueprint_v*.yaml"):
        p.write_text(p.read_text(encoding="utf-8").replace(
            "authorization: authorized", "authorization: not-authorized"),
            encoding="utf-8")
    a = C["render_precheck"](eng, "solution-blueprint")
    eng2 = fresh()
    shutil.rmtree(eng2 / "_blueprint")
    b = C["render_precheck"](eng2, "claude-design-brief")
    c = C["render_precheck"](eng2, "discovery-report")
    return ("sem autorização/UI: 0 impeditivos e nenhum ecrã inventado",
            "sem autorização %d · headless %d · sem desenho %d"
            % (a["blocking"], b["blocking"], c["blocking"]),
            a["blocking"] == 0 and b["blocking"] == 0 and c["blocking"] == 0)


def t35():
    eng = fresh()
    with io.open(eng / "decisions.md", "a", encoding="utf-8") as fh:
        fh.write(APPROVAL)
    before = (eng / "decisions.md").read_bytes()
    res = state(eng, "render", RENDER_V02)
    appr = C["blueprint_versions"](eng)["approved"]
    return ("aprovação preservada · cobertura not_evaluated",
            "aprovada %s · cobertura %s · decisions intacto %s"
            % (appr, res["coverage"], (eng / "decisions.md").read_bytes() == before),
            appr == "v03" and res["coverage"] == "not_evaluated"
            and (eng / "decisions.md").read_bytes() == before)


# ============================================================ T36 - T40
def t36():
    eng = fresh()
    dec = eng / "decisions.md"
    txt = dec.read_text(encoding="utf-8")
    readers = C["ReaderAdapter"]()
    blocks = readers.classify_decisions(txt)
    live = readers.live_solution_decision(txt)
    return ("o leitor devolve a decisão-solução normalizada",
            "%s (%d blocos)" % ((live or {}).get("id"), len(blocks)),
            bool(live and (live or {}).get("id", "").startswith("D-")))


def t37():
    eng = fresh()
    install(eng, RECON)
    res = state(eng, "reconciliation")
    su = (eng / "shared-understanding.md").read_text(encoding="utf-8")
    open_q = su.count("| U-")
    return ("reconciliação fecha com perguntas em aberto; E2E continua por provar",
            "elegível %s · linhas U- na SU %d · nota E2E %s"
            % (res["eligible"], open_q, "ponta-a-ponta" in res["note"]),
            res["eligible"] and "ponta-a-ponta" in res["note"])


def t38():
    eng = fresh()
    install(eng, *CHAIN_BP)
    before = manifest(eng)
    a = state(eng, "blueprint", BP03)
    b = state(eng, "blueprint", BP03)
    after = manifest(eng)
    same = all(a[k] == b[k] for k in ("contract_validity", "freshness", "source_review",
                                      "semantic_review", "coverage", "eligible"))
    return ("mesmo resultado, zero mutações",
            "idêntico %s · ficheiros alterados %d" % (same,
                                                      sum(1 for k in before
                                                          if before[k] != after.get(k))),
            same and before == after)


def t39():
    eng = fresh()

    def moved(name, rec):
        if rec.get("stage") != "render":
            return
        for a in rec["basis"]["authorities"]:
            if a["path"].endswith(".template.md"):
                a["sha256"] = "0" * 64
        rec["deliverable"]["template_sha256"] = "0" * 64
    install(eng, *CHAIN_BP, "rec-v05-render-complete", mutate=moved)
    res = state(eng, "render", RENDER_V02)
    return ("stale", "%s · %s" % (res["freshness"], ",".join(codes(res))),
            res["freshness"] == "stale")


def t40():
    eng = fresh()
    install(eng, *CHAIN_BP, "rec-v05-render-complete")
    before = state(eng, "render", RENDER_V02)
    md = eng / "_coverage" / "coverage_v05.md"
    md.write_text("# tudo aprovado e completo\n", encoding="utf-8")
    after = state(eng, "render", RENDER_V02)
    return ("veredicto inalterado",
            "%s/%s -> %s/%s" % (before["coverage"], before["eligible"],
                                after["coverage"], after["eligible"]),
            before["coverage"] == after["coverage"]
            and before["eligible"] == after["eligible"])


def manifest(root, skip=()):
    out = {}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            rel = p.relative_to(root).as_posix()
            if any(rel.startswith(s) for s in skip):
                continue
            out[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


CASES = [
    ("T01", "F06: C-014 sem destino no desenho", "test_coverage_phase4.py", t01),
    ("T02", "C-014 citado só na entidade blend", "test_coverage_contract.py", t02),
    ("T03", "percurso completo revisto; aprovação ausente", "test_coverage_phase4.py", t03),
    ("T04", "obrigação sem tratamento não dá verde", "test_coverage_contract.py", t04),
    ("T05", "folha/coluna fora do source_review", "test_coverage_fixtures.py", t05),
    ("T06", "fonte nova em inputs depois da revisão", "test_coverage_freshness.py", t06),
    ("T07", "workbook alterado, captura antiga", "test_coverage_freshness.py", t07),
    ("T08", "fonte sem extractor não é não-aplicável", "test_coverage_contract.py", t08),
    ("T09", "dois workbooks com folha homónima", "test_coverage_inventory.py", t09),
    ("T10", "grupo de colunas: membro omitido detectado", "test_coverage_inventory.py", t10),
    ("T11", "su_ref/locator inexistente", "test_coverage_contract.py", t11),
    ("T12", "campo de ecrã inexistente", "test_coverage_contract.py", t12),
    ("T13", "exclusão material sem decisão", "test_coverage_contract.py", t13),
    ("T14", "exclusão mecânica com fundamento", "test_coverage_contract.py", t14),
    ("T15", "covered só com pergunta/prova futura", "test_coverage_contract.py", t15),
    ("T16", "Assumed continua Assumed", "test_coverage_freshness.py", t16),
    ("T17", "correcção de resposta invalida", "test_coverage_freshness.py", t17),
    ("T18", "logs/dashboard não invalidam", "test_coverage_freshness.py", t18),
    ("T19", "aprovação não invalida a própria revisão", "test_coverage_freshness.py", t19),
    ("T20", "mudar a decisão-solução invalida", "test_coverage_freshness.py", t20),
    ("T21", "desenho alterado depois da revisão", "test_coverage_freshness.py", t21),
    ("T22", "rever v01, consumir noutra versão", "test_coverage_phase5.py", t22),
    ("T23", "revisão nova com gaps não é escondida", "test_coverage_phase5.py", t23),
    ("T24", "ausente/inválido/futuro: nunca verde", "test_coverage_phase5.py", t24),
    ("T25", "hooks não dispararam: CLI disponível", "test_coverage_phase4.py", t25),
    ("T26", "cwd externo, espaços e acentos", "test_coverage_integration.py", t26),
    ("T27", "engagements múltiplos sem selecção", "test_coverage_integration.py", t27),
    ("T28", "traversal recusado sem ler", "test_coverage_inventory.py", t28),
    ("T29", "finalize não sobrescreve histórico", "test_coverage_integration.py", t29),
    ("T30", "só revisão semântica pendente", "test_coverage_phase4.py", t30),
    ("T31", "selecção de versão por deliverable", "test_coverage_phase5.py", t31),
    ("T32", "id em comentário não é projecção", "test_coverage_phase5.py", t32),
    ("T33", "render com lacuna, sem reparar a montante", "test_coverage_phase5.py", t33),
    ("T34", "sem UI/headless/sem arquitectura", "test_coverage_phase5.py", t34),
    ("T35", "legado: aprovação preservada", "test_coverage_phase5.py", t35),
    ("T36", "decision_ref normalizado", "test_coverage_fixtures.py", t36),
    ("T37", "perguntas em aberto não bloqueiam", "test_coverage_phase4.py", t37),
    ("T38", "read-only repetido: zero mutações", "test_coverage_phase5.py", t38),
    ("T39", "template alterado: stale", "test_coverage_phase5.py", t39),
    ("T40", "Markdown editado não muda autoridade", "test_coverage_integration.py", t40),
]

if __name__ == "__main__":
    for tid, what, where, fn in CASES:
        scenario(tid, what, where, fn)

    ok = sum(1 for r in rows if r["ok"] is True)
    bad = [r for r in rows if r["ok"] is False]
    inc = [r for r in rows if r["ok"] is None]

    say("# Matriz dos 40 cenários — fase 6")
    say()
    say("Gerado por `docs/runtime-hardening/repro-coverage-phase6-matrix-2026-09-16.py`")
    say("sobre cópias de `.claude/tests/fixtures/coverage/fx-coverage-f06`. Cada linha é uma")
    say("**execução**, não um mapeamento por citação: o cenário é montado, corrido, e o")
    say("veredicto observado comparado com o que o plano §13 exige.")
    say()
    say("**%d OK · %d falha(s) · %d inconclusivo(s)**, de %d." % (ok, len(bad), len(inc),
                                                                  len(rows)))
    say()
    say("| id | cenário | esperado | observado | veredicto | também em |")
    say("|---|---|---|---|---|---|")
    for r in rows:
        say("| %s | %s | %s | %s | %s | `%s` |" % (
            r["id"], r["what"], r["expected"], r["observed"],
            "OK" if r["ok"] is True else ("**INCONCLUSIVO**" if r["ok"] is None
                                          else "**FALHA**"), r["where"]))
    say()
    say("Um cenário que este executor não consiga montar sai **inconclusivo**, nunca OK: é")
    say("a regra que a fase 1 aprendeu quando «inconclusivo» foi lido como verde (P-15).")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n-> " + str(OUT))
    sys.exit(1 if bad or inc else 0)
