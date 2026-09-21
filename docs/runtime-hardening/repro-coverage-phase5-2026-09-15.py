# -*- coding: utf-8 -*-
"""Ensaio da projecção, fase 5 — corre numa cópia da fixture, escreve a evidência.

    python docs/runtime-hardening/repro-coverage-phase5-2026-09-15.py

Nenhum engagement real é tocado. Sete passos, e cada um mostra o que o executor faria e o
que o estado devolve a seguir — com as autoridades, as lacunas e as ausências legítimas
separadas umas das outras.
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
OUT = ROOT / "docs" / "review-evidence" / "coverage-phase5-rehearsal-2026-09-15.md"

CHAIN = ("rec-v01-reconciliation-complete", "rec-v02-blueprint-missing",
         "rec-v03-blueprint-partial", "rec-v04-blueprint-complete")
RENDER_V01 = "_render/fx-coverage-f06_solution-blueprint_v01.md"
RENDER_V02 = "_render/fx-coverage-f06_solution-blueprint_v02.md"
DELIVERABLES = ("discovery-report", "executive-report", "solution-blueprint",
                "implementation-spec", "claude-design-brief", "estimate")
APPROVAL = """
## D-003 — Blueprint bp-v03 aprovado

- **Aprovado por**: dono do processo
- **Cobertura consumida**: _coverage/coverage_v04.json
- **Timestamp**: 2026-09-15T10:00:00+01:00
"""

lines = []


def say(s=""):
    lines.append(s)
    print(s)


def fresh():
    tmp = Path(tempfile.mkdtemp(prefix="aisa-ph5-"))
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


def state(eng, rel):
    return C["coverage_state"](eng, "render", {
        "file": rel, "identity": C["target_identity"](eng, "render", rel)})


def verdicts(res):
    return ("contrato %s · atualidade %s · fontes %s · dois sentidos %s · cobertura %s · "
            "pode avançar %s" % (res["contract_validity"], res["freshness"],
                                 res["source_review"], res["semantic_review"],
                                 res["coverage"], "sim" if res["eligible"] else "não"))


def errors(res):
    return [(d["code"], d.get("item", ""), d["message"]) for d in res["diagnostics"]
            if d["severity"] == "error"]


def manifest(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file()}


def cli(*args):
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run([sys.executable, "-B", str(ENGINE), *args], cwd=str(ROOT),
                          env=env, text=True, capture_output=True, encoding="utf-8",
                          errors="replace")


say("# Ensaio da projecção — fase 5")
say()
say("Gerado por `docs/runtime-hardening/repro-coverage-phase5-2026-09-15.py` sobre uma")
say("cópia de `.claude/tests/fixtures/coverage/fx-coverage-f06`. Nenhum engagement real")
say("foi lido, escrito ou avaliado.")
say()

# ---------------------------------------------------------------- 1. autoridade
eng = fresh()
before = manifest(eng)
say("## 1. Que versão cada deliverable lê, e porquê")
say()
say("O template declara (`blueprint_version_read`); o motor traduz e resolve. A fixture")
say("tem `v03` autorizada e **nenhuma** aprovada.")
say()
say("| deliverable | declara | resolve | estado | razão |")
say("|---|---|---|---|---|")
for d in DELIVERABLES:
    pre = C["render_precheck"](eng, d)
    say("| `%s` | `%s` | %s | `%s` | %s |" % (
        d, pre["declared"], pre["expected"]["version"] or "—",
        pre["expected"]["state"], pre["expected"]["reason"] or "—"))
say()
say("As três razões pelas quais uma versão aprovada pode não existir ficam separadas:")
say("*sem autorização nenhuma* · *autorizada e por aprovar* · *escolha estrutural em")
say("aberto*. Colapsá-las apagava a diferença entre «falta decidir» e «falta aprovar».")
say()

# ---------------------------------------------------------------- 2. positivo
say("## 2. A projecção que carrega o que foi pedido")
say()
install(eng, *CHAIN, "rec-v05-render-complete")
res = state(eng, RENDER_V02)
say("`coverage.py check --stage render --target %s`" % RENDER_V02)
say()
say("    " + verdicts(res))
say()
say("E o que isto **não** diz, palavra por palavra do resultado:")
say()
say("    " + res["note"])
say()

# ---------------------------------------------------------------- 3. o comentário
say("## 3. O id num comentário (T32)")
say()
say("A `v01` do documento tem a linha `<!-- C-007 -->` e **não** tem o percurso de")
say("publicação. Um registo que aponte a projecção de C-007 para essa linha resolve — a")
say("linha existe, e é por isso que o locator não é um destino morto.")
say()
sha01 = hashlib.sha256((eng / RENDER_V01).read_bytes()).hexdigest()


def point_at_comment(name, rec):
    if rec.get("stage") != "render":
        return
    rec["target"].update({"file": RENDER_V01, "identity": "solution-blueprint_v01",
                          "sha256": sha01})
    for it in rec["coverage"]:
        for tg in it["targets"]:
            tg["file"] = RENDER_V01
        if it["id"] == "item-001":
            it["targets"] = [{"file": RENDER_V01, "selector": "A3/C-007",
                              "kind": "section", "role": "projection"}]


raw = C["resolve_target"](eng, {"file": RENDER_V01, "selector": "A3/C-007"})
say("Resolução crua do mesmo locator: `ok=%s`, `comment_only=%s`. **É este o degrau**:"
    % (raw["ok"], raw.get("comment_only")))
say("sem a regra da §8.2 o destino resolvia e o item passava a `covered`.")
say()
install(eng, *CHAIN, "rec-v05-render-complete", mutate=point_at_comment)

# Medição do degrau, e não afirmação sobre ele: o MESMO registo, contra um motor igual em
# tudo excepto na regra da §8.2. O `__file__` fabricado é o do motor real, para que a raiz
# do repositório e as fronteiras de leitura fiquem exactamente as mesmas.
_src = ENGINE.read_text(encoding="utf-8").replace(
    'COMMENT_LINE = re.compile(r"^\\s*<!--.*?-->\\s*$")',
    'COMMENT_LINE = re.compile(r"(?!x)x")   # regra desligada, só para esta medição')
_ns = {"__name__": "coverage_sem_a_regra", "__file__": str(ENGINE)}
exec(compile(_src, str(ENGINE), "exec"), _ns)                       # noqa: S102
assert _ns["COMMENT_LINE"].pattern != C["COMMENT_LINE"].pattern, "a regra não foi desligada"
without = _ns["coverage_state"](eng, "render", {
    "file": RENDER_V01, "identity": _ns["target_identity"](eng, "render", RENDER_V01)})
res = state(eng, RENDER_V01)

say("| a regra da §8.2 | cobertura | pode avançar |")
say("|---|---|---|")
say("| desligada | `%s` | %s |" % (without["coverage"],
                                   "sim" if without["eligible"] else "não"))
say("| ligada | `%s` | %s |" % (res["coverage"], "sim" if res["eligible"] else "não"))
say()
say("    " + verdicts(res))
say()
for code, item, msg in errors(res):
    if item == "item-001":
        say("    [%s] %s — %s" % (code, item, msg))
say()

# ---------------------------------------------------------------- 4. autoridade errada
say("## 4. Ler a versão errada (T22 / T31)")
say()
install(eng, *CHAIN, "rec-neg-authority-mismatch")
res = state(eng, RENDER_V02)
say("    " + verdicts(res))
say()
for code, item, msg in errors(res):
    if code == "COV-AUTHORITY-MISMATCH":
        say("    [%s] %s" % (code, msg))
say()
say("Dois achados, e são factos diferentes: a revisão consumida é de outra versão, **e**")
say("a versão declarada não é a que o contrato daquele deliverable manda ler.")
say()
say("O caso que **só** a segunda verificação apanha: a Implementation Specification a ler")
say("a última **autorizada** (`v03`), coerente com o `based_on` que consome — e o contrato")
say("dela exige a **aprovada**, que não existe.")
say()


def spec_reads_the_authorized_one(name, rec):
    if rec.get("stage") != "render":
        return
    rec["deliverable"].update({
        "id": "implementation-spec",
        "template": "library/packs/pp/deliverable-templates/implementation-spec.template.md",
        "template_sha256": hashlib.sha256(
            (ROOT / "library/packs/pp/deliverable-templates/"
                    "implementation-spec.template.md").read_bytes()).hexdigest(),
        "blueprint_version_read": "v03"})
    for a in rec["basis"]["authorities"]:
        if a["path"].endswith(".template.md"):
            a["path"] = ("library/packs/pp/deliverable-templates/"
                         "implementation-spec.template.md")
            a["sha256"] = rec["deliverable"]["template_sha256"]


install(eng, *CHAIN, "rec-v05-render-complete", mutate=spec_reads_the_authorized_one)
res = state(eng, RENDER_V02)
say("    " + verdicts(res))
say()
for code, item, msg in errors(res):
    if code == "COV-AUTHORITY-MISMATCH":
        say("    [%s] %s" % (code, msg))
say()
say("O `based_on` está certo — a revisão consumida **é** a do desenho `v03`. A verificação")
say("antiga, sozinha, deixava isto passar: é o contrato de projecção que diz `v<approved>`.")
say()
say("### 4b. E o contrato tem de ser o deste deliverable")
say()
say("`id` e `template` são declarados pelo mesmo registo, e nada os obriga a concordar. Uma")
say("revisão que se diz da Implementation Specification apoiada no template do Architecture")
say("Blueprint herda `v<latest authorized>`, concorda consigo própria — e a versão aprovada")
say("não existe. Medido contra um motor igual em tudo excepto nesta verificação:")
say()


def spoof_the_id(name, rec):
    if rec.get("stage") == "render":
        rec["deliverable"]["id"] = "implementation-spec"   # template continua o de arquitectura


_src_id = ENGINE.read_text(encoding="utf-8").replace(
    'if auth["state"] == "ok" and declared_id and tid and declared_id != tid:',
    'if False:   # verificação desligada, só para esta medição')
_ns_id = {"__name__": "coverage_sem_identidade", "__file__": str(ENGINE)}
exec(compile(_src_id, str(ENGINE), "exec"), _ns_id)                 # noqa: S102
install(eng, *CHAIN, "rec-v05-render-complete", mutate=spoof_the_id)
without = _ns_id["coverage_state"](eng, "render", {
    "file": RENDER_V02, "identity": _ns_id["target_identity"](eng, "render", RENDER_V02)})
res = state(eng, RENDER_V02)
say("| a verificação de identidade | cobertura | pode avançar | versão aprovada |")
say("|---|---|---|---|")
for label, r in (("desligada", without), ("ligada", res)):
    say("| %s | `%s` | %s | %s |" % (
        label, r["coverage"], "sim" if r["eligible"] else "não",
        C["blueprint_versions"](eng)["approved"] or "nenhuma"))
say()
for code, item, msg in errors(res):
    if code == "COV-AUTHORITY-MISMATCH":
        say("    [%s] %s" % (code, msg))
say()
say("Com a verificação desligada, uma especificação sai **elegível sem aprovação nenhuma**.")
say("É o falso positivo que a revisão independente encontrou, e que os 43 testes anteriores")
say("desta fase não apanhavam: todos verificavam a versão contra o template declarado, e")
say("nenhum perguntava de quem era esse template.")
say()
say("O pré-render tinha o mesmo dever, e o mesmo buraco:")
say()
_arch = "library/packs/pp/deliverable-templates/solution-blueprint.template.md"
pre = C["render_precheck"](eng, "implementation-spec", _arch)
say("    pré-render de `implementation-spec` com o template de arquitectura → resolve %s"
    % (pre["expected"]["version"] or "nenhuma versão"))
say("    estado `%s`, %d achado(s) impeditivo(s)" % (pre["expected"]["state"],
                                                     pre["blocking"]))
say()

# ---------------------------------------------------------------- 5. ausências legítimas
say("### 4c. O varrimento da classe")
say()
say("O defeito de 4b vinha de dois campos declarados pelo mesmo registo que ninguém")
say("obrigava a concordar. A classe foi varrida campo a campo: cada caso monta **um** par")
say("incoerente, com o registo coerente como controlo.")
say()

SPEC_TPL_REL = "library/packs/pp/deliverable-templates/implementation-spec.template.md"
SPEC_DOC = "_render/fx-coverage-f06_implementation-spec_v01.md"


def as_spec(e, template=SPEC_TPL_REL, version_read=None, retarget=True):
    """Um registo da spec coerente em tudo menos no par que o caso quer partir."""
    (e / SPEC_DOC).write_text((e / RENDER_V02).read_text(encoding="utf-8"),
                              encoding="utf-8")
    sha_doc = hashlib.sha256((e / SPEC_DOC).read_bytes()).hexdigest()
    sha_tpl = hashlib.sha256((ROOT / template).read_bytes()).hexdigest()

    def mutate(name, rec):
        if rec.get("stage") != "render":
            return
        rec["deliverable"].update({"id": "implementation-spec", "template": template,
                                   "template_sha256": sha_tpl,
                                   "blueprint_version_read": version_read})
        for a in rec["basis"]["authorities"]:
            if a["path"].endswith(".template.md"):
                a.update({"path": template, "sha256": sha_tpl})
        if retarget:
            rec["target"].update({"file": SPEC_DOC,
                                  "identity": "implementation-spec_v01",
                                  "sha256": sha_doc})
            for it in rec["coverage"]:
                for tg in it["targets"]:
                    tg["file"] = SPEC_DOC
    return mutate


def render_only(fn):
    def mutate(name, rec):
        if rec.get("stage") == "render":
            fn(rec)
    return mutate


ARCH_TPL_REL = "library/packs/pp/deliverable-templates/solution-blueprint.template.md"


def drop_template_from_basis(rec):
    rec["basis"]["authorities"] = [a for a in rec["basis"]["authorities"]
                                   if not a["path"].endswith(".template.md")]


def alien_template(rec):
    rec["deliverable"]["template"] = ("library/packs/outsystems/deliverable-templates/"
                                      "implementation-spec.template.md")


def not_applicable_yet_covered(rec):
    rec["deliverable"]["applicability"] = {"state": "not_applicable",
                                           "reason": "razao declarada"}


def other_pack(rec):
    rec["basis"]["pack"] = "outsystems"


# (rótulo, como construir o mutador a partir do engagement, alvo)
SWEEP = [
    ("(controlo) registo coerente", lambda e: (lambda n, r: None), RENDER_V02),
    ("`id` vs `template_id` do template",
     lambda e: as_spec(e, template=ARCH_TPL_REL, version_read="v03"), SPEC_DOC),
    ("`id` vs o deliverable do documento revisto",
     lambda e: as_spec(e, version_read="v03", retarget=False), RENDER_V02),
    ("`template` vs `basis.authorities`",
     lambda e: render_only(drop_template_from_basis), RENDER_V02),
    ("`template` vs um ficheiro legível do pacote",
     lambda e: render_only(alien_template), RENDER_V02),
    ("versão exigida que não existe, declarada por omissão",
     lambda e: as_spec(e, version_read=None), SPEC_DOC),
    ("`applicability` não-produzido vs obrigações cobertas",
     lambda e: render_only(not_applicable_yet_covered), RENDER_V02),
    ("`basis.pack` vs o pacote activo", lambda e: render_only(other_pack), RENDER_V02),
]

say("| par declarado | cobertura | pode avançar | achado |")
say("|---|---|---|---|")
for label, build, tgt in SWEEP:
    e = fresh()
    if label.startswith("`id` vs o deliverable"):
        # A autoridade da spec tem de existir, ou o caso teria DUAS incoerências e o
        # resultado não diria qual delas o motor apanhou.
        with io.open(e / "decisions.md", "a", encoding="utf-8") as fh:
            fh.write(APPROVAL)
    install(e, *CHAIN, "rec-v05-render-complete", mutate=build(e))
    r = state(e, tgt)
    codes = sorted({d["code"] for d in r["diagnostics"] if d["severity"] == "error"})
    say("| %s | `%s` | %s | %s |" % (label, r["coverage"],
                                     "sim" if r["eligible"] else "não",
                                     ", ".join("`%s`" % c for c in codes) or "—"))
say()
say("O controlo coerente continua a passar: uma regra que reprovasse o caso legítimo não")
say("seria uma regra, seria uma avaria.")
say()
say("Fica **declarado como limite**: `deliverable.authority_sources` é verificado na forma")
say("e no efeito sobre a base de atualidade, não contra a lista que o template declara em")
say("prosa. Comparar as duas por texto seria adivinhar.")
say()

say("## 5. O que não pode ficar retido (T34 / T35)")
say()
head = fresh()
for p in (head / "_blueprint").glob("ux-blueprint_v*.yaml"):
    p.write_text(p.read_text(encoding="utf-8").replace(
        "authorization: authorized", "authorization: not-authorized"), encoding="utf-8")
pre = C["render_precheck"](head, "solution-blueprint")
say("Sem autorização de arquitectura para âmbito nenhum: `%s` — %d achado(s) impeditivo(s)."
    % (pre["expected"]["state"], pre["blocking"]))
say()
noui = fresh()
shutil.rmtree(noui / "_blueprint")
pre = C["render_precheck"](noui, "claude-design-brief")
say("Sem `_blueprint/` de todo (headless levado ao extremo): `%s` — %d impeditivo(s), e a"
    % (pre["expected"]["state"], pre["blocking"]))
say("revisão que resta avaliar é a de `%s`." % pre["upstream"]["stage"])
say()
pre = C["render_precheck"](noui, "discovery-report")
say("O Discovery Report, que não lê desenho nenhum: `%s` — %d impeditivo(s). Não fica"
    % (pre["expected"]["state"], pre["blocking"]))
say("retido por não haver cobertura de desenho.")
say()
legacy = fresh()
with io.open(legacy / "decisions.md", "a", encoding="utf-8") as fh:
    fh.write(APPROVAL)
dec_before = (legacy / "decisions.md").read_bytes()
res = state(legacy, RENDER_V02)
pre = C["render_precheck"](legacy, "implementation-spec")
say("Legado (aprovação histórica em `decisions.md`, `_coverage/` vazio): cobertura `%s`,"
    % res["coverage"])
say("versão aprovada continua a resolver-se (`%s`), e `decisions.md` fica byte a byte"
    % pre["expected"]["version"])
say("como estava: %s." % ("sim" if dec_before == (legacy / "decisions.md").read_bytes()
                          else "NÃO"))
say()

# ---------------------------------------------------------------- 6. CLI
say("## 6. A linha de comandos, tal como sai")
say()
r = cli("check", "--engagement", str(eng), "--stage", "render", "--deliverable",
        "implementation-spec")
say("```text")
say("$ coverage.py check --stage render --deliverable implementation-spec")
for ln in r.stdout.splitlines():
    say(ln)
say("(exit %d)" % r.returncode)
say("```")
say()
install(eng, *CHAIN, "rec-v05-render-complete")
r = cli("report", "--engagement", str(eng), "--stage", "render", "--target", RENDER_V02)
say("E a projecção Markdown do registo publicado — que **não** é autoridade (T40):")
say()
say("```text")
for ln in r.stdout.splitlines()[:28]:
    say(ln)
say("… (exit %d)" % r.returncode)
say("```")
say()

# ---------------------------------------------------------------- 7. read-only
say("## 7. O que tudo isto escreveu no engagement")
say()
after = manifest(eng)
changed = sorted(set(after) ^ set(before)) + \
    sorted(k for k in set(after) & set(before) if after[k] != before[k])
outside = [k for k in changed if not k.startswith("_coverage/")]
say("Ficheiros alterados fora de `_coverage/` (onde os registos do ensaio foram")
say("instalados de propósito): **%d**%s." % (len(outside),
                                             "" if not outside else " — " + ", ".join(outside)))
say()
say("O que este ensaio **não** declara: nenhum desenho real está aprovado, completo ou")
say("provado ponta-a-ponta; nenhuma pergunta em aberto foi respondida; nenhuma aprovação")
say("foi registada, e nenhuma aprovação histórica foi tocada.")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n-> " + str(OUT))
