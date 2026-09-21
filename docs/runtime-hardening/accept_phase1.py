# -*- coding: utf-8 -*-
"""Aceitação executável da fase 1 do endurecimento do runtime (bloco A).

    python docs/runtime-hardening/accept_phase1.py
    python docs/runtime-hardening/accept_phase1.py --engagement <slug>

Corre contra os engagements reais que existirem em `projects/` (ou em
`$AISA_ENGAGEMENTS_ROOT`) e contra os ficheiros do repositório. Não escreve nada.
Sai com 0 quando todos os critérios com veredicto passam, 1 quando algum falha.

O que verifica, por ordem (plano §4 A5):

  A. O defeito reportado desapareceu, e os escalares seguem a tabela declarada.
  B. Compatibilidade: `bp_read` sobre os blueprints reais == snapshot b81d39c, menos
     as diferenças justificadas uma a uma. Um diff fora da lista é regressão.
  C. Correcção: equivalência entre formas (Y2≡Y3, Y5≡Y6, ordem de campos).
  D. Cada código de `bp_validate` tem fixture que dispara e fixture que não.
  E. Aprovação sobre versão inválida: os quatro consumidores reagem.
  F. Ligações: skill, hook, settings, contrato, packs, versão do motor.
  G. Suite verde.

Os critérios A-G têm veredicto. A medição sobre os blueprints reais imprime-se e
NÃO se aprova: §11 do plano proíbe reescrever engagements, por isso os números sobem
por construção quando a regra aperta, e lêem-se.
"""

import argparse
import glob
import json
import os
import runpy
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
ENG_ROOT = Path(os.environ.get("AISA_ENGAGEMENTS_ROOT") or (ROOT / "projects"))
FIX = ROOT / ".claude" / "tests" / "fixtures" / "blueprints"
D = runpy.run_path(str(ROOT / "library" / "kernel" / "tools" / "dashboard.py"))
VALID = (FIX / "valid_min_v01.yaml").read_text(encoding="utf-8")
SU_IDS = {"C-001", "C-002", "C-003", "A-001", "U-001"}

FAILED: list[str] = []


def head(letter: str, title: str) -> None:
    print("\n" + "=" * 78)
    print("{}. {}".format(letter, title))
    print("=" * 78)


def verdict(ok: bool, label: str, detail: str = "") -> None:
    print("  [{}] {}{}".format("ok " if ok else "FALHA", label,
                               ("  — " + detail) if detail else ""))
    if not ok:
        FAILED.append(label)


def measure(label: str, value) -> None:
    print("  [ .. ] {}: {}".format(label, value))


def validate(text, name="ux-blueprint_v01.yaml", su_ids=SU_IDS, cfg=None, loader=None):
    return D["bp_validate"](text, name, cfg or {}, su_ids, loader)


def blocking(text, **kw):
    return sorted({i["code"] for i in validate(text, **kw) if i["severity"] == "block"})


def all_codes(text, **kw):
    return sorted({i["code"] for i in validate(text, **kw)})


def swap(text, old, new):
    if text.count(old) != 1:
        raise SystemExit("âncora não única na fixture: " + old[:60])
    return text.replace(old, new)


def choices(text):
    block = D["yl_find_block"](text, "open_architecture_choices", "architecture") \
        or D["yl_find_block"](text, "open_architecture_choices")
    return D["yl_list_of_maps"](block)


# ----------------------------------------------------------------------- A

def criterion_a():
    head("A", "O defeito reportado e a tabela de escalares")
    got = choices("""architecture:
  open_architecture_choices:
    - choice: Choose authentication
      su_refs:
        - U-001
      structural: true
      resolved: false
""")
    verdict(len(got) == 1, "um item, não dois", "itens lidos: {}".format(len(got)))
    if got:
        verdict(got[0].get("su_refs") == ["U-001"], "su_refs preservado",
                repr(got[0].get("su_refs")))
        verdict(got[0].get("structural") is True, "structural preservado",
                repr(got[0].get("structural")))
        verdict(got[0].get("resolved") is False, "resolved preservado",
                repr(got[0].get("resolved")))
    table = [("null", None), ("~", None), ("", None), ("none", "none"),
             ("true", True), ("yes", True), ("no", False), ('"none"', "none"),
             ("'null'", "null"), ("6", 6), ("v06", "v06")]
    bad = [(raw, D["yl_scalar"](raw)) for raw, want in table if D["yl_scalar"](raw) != want]
    verdict(not bad, "escalares seguem a tabela declarada (A2, Y1)", repr(bad))
    headless = VALID.replace('    mode: owned-internal\n'
                             '    primary_surface: "Record-centric app (model-driven)"',
                             "    mode: none\n    primary_surface: null")
    verdict(D["yl_scalar_at"](headless, "mode", "experience") == "none",
            "`mode: none` (headless) lê-se como texto")
    verdict("BP-ENUM" not in all_codes(headless) and "BP-SURFACE" not in all_codes(headless),
            "um blueprint headless válido não dispara nada")


# ----------------------------------------------------------------------- B

def criterion_b(slug):
    head("B", "Compatibilidade — snapshot b81d39c, menos as diferenças justificadas")
    snap_f, just_f = FIX / "snapshot-b81d39c.json", FIX / "snapshot-diff-justified.json"
    if not snap_f.is_file() or not just_f.is_file():
        verdict(False, "snapshot e lista justificada presentes")
        return
    snap = json.loads(snap_f.read_text(encoding="utf-8"))["blueprints"]
    just = {(r["file"], r["key"], r["item"])
            for r in json.loads(just_f.read_text(encoding="utf-8"))["justified"]}
    files = {f: old for f, old in snap.items()
             if (ROOT / f).is_file() and (not slug or slug in f)}
    if not files:
        measure("engagements montados", "nenhum — compatibilidade não avaliada")
        return
    unjustified, compared = [], 0
    for f, old in files.items():
        new = json.loads(json.dumps(D["bp_read"](ROOT / f), default=str))
        for k, ov in old.items():
            compared += 1
            nv = new.get(k)
            if nv == ov:
                continue
            if isinstance(ov, list) and isinstance(nv, list) and len(ov) == len(nv):
                for i, (o, n) in enumerate(zip(ov, nv)):
                    if o != n and (f, k, i) not in just:
                        unjustified.append("{} · {}[{}]".format(f, k, i))
            elif (f, k, None) not in just:
                unjustified.append("{} · {}".format(f, k))
    measure("blueprints comparados", len(files))
    measure("chaves comparadas", compared)
    measure("diferenças justificadas na lista", len(just))
    verdict(not unjustified, "zero diferenças fora da lista justificada",
            "; ".join(unjustified[:4]))
    md = (FIX / "snapshot-diff-justified.md")
    verdict(md.is_file() and "Y7-in-Y4" in md.read_text(encoding="utf-8"),
            "cada diferença tem a sua regra escrita")


# ----------------------------------------------------------------------- C

def criterion_c():
    head("C", "Correcção — equivalência entre formas (o snapshot não a prova)")
    inline = """architecture:
  open_architecture_choices:
    - choice: c
      su_refs: [U-001, C-002]
      structural: true
      would_be_settled_by: w
"""
    block = """architecture:
  open_architecture_choices:
    - choice: c
      su_refs:
        - U-001
        - C-002
      structural: true
      would_be_settled_by: w
"""
    verdict(choices(inline) == choices(block), "Y2 ≡ Y3 (lista inline ≡ lista em bloco)")
    flow = """architecture:
  record_authority:
    - domain: d
      schema_owner: {value: equipa, state: Assumed, su_ref: A-001}
"""
    blk = """architecture:
  record_authority:
    - domain: d
      schema_owner:
        value: equipa
        state: Assumed
        su_ref: A-001
"""
    f = D["yl_list_of_maps"](D["yl_find_block"](flow, "record_authority", "architecture"))
    b = D["yl_list_of_maps"](D["yl_find_block"](blk, "record_authority", "architecture"))
    verdict(f == b, "Y5 ≡ Y6 (mapa de fluxo ≡ mapa em bloco)")
    one = """architecture:
  open_architecture_choices:
    - choice: c
      structural: true
      su_refs: [U-001]
"""
    two = """architecture:
  open_architecture_choices:
    - su_refs: [U-001]
      structural: true
      choice: c
"""
    verdict(choices(one) == choices(two), "a ordem dos campos não muda a leitura")
    deep = """architecture:
  record_authority:
    - domain: d
      access_contract:
        confidentiality:
          row_level: {value: por unidade, state: Confirmed, su_ref: C-003}
"""
    it = D["yl_list_of_maps"](D["yl_find_block"](deep, "record_authority", "architecture"))
    ok = bool(it) and it[0]["access_contract"]["confidentiality"]["row_level"]["value"] == "por unidade"
    verdict(ok, "mapa a três níveis (access_contract.confidentiality.row_level)")
    for raw in ("&base x", "*base", "{a: {b: c}}"):
        verdict(isinstance(D["yl_scalar"](raw), D["YlUnsupported"]),
                "fora do subconjunto é sinalizado: " + raw)


# ----------------------------------------------------------------------- D

def criterion_d(slug):
    head("D", "Cada código dispara e não dispara")
    verdict(validate(VALID) == [], "a fixture de referência está limpa",
            repr([i["code"] for i in validate(VALID)]))
    cases = {
        "BP-REQ-KEY": swap(VALID, "open_questions: [U-001]\n", ""),      # warn variant
        "BP-TYPE": swap(VALID, "open_questions: [U-001]", "open_questions: null"),
        "BP-ITEM-TYPE": swap(VALID, "  relocated_responsibilities: []",
                             "  relocated_responsibilities:\n    -"),
        "BP-ARCH-REQ": swap(VALID, "  scope: whole solution\n", ""),
        "BP-ENUM": swap(VALID, "  authorization: authorized", "  authorization: true"),
        "BP-SURFACE": swap(VALID, "    mode: owned-internal", "    mode: none"),
        "BP-COMP-REQ": swap(VALID, "      pattern: data-virtualization\n", ""),
        "BP-RA-REQ": swap(VALID, "      key: pedidos\n", ""),
        "BP-AC-KEY": swap(VALID, "        key: [id]", "        key: []"),
        "BP-RR-REQ": swap(VALID, "  relocated_responsibilities: []",
                          "  relocated_responsibilities:\n    - responsibility: r\n      owner: o"),
        "BP-NO-SUREFS": swap(VALID, "    rbac_group: analistas\n    su_refs: [C-001]\n",
                             "    rbac_group: analistas\n"),
        "BP-LEAF-NO-SUREF": swap(VALID,
                                 "          primary_key_type: {value: int, state: Confirmed, su_ref: C-003}",
                                 "          primary_key_type: {value: int, state: Confirmed}"),
        "BP-BAD-ID": swap(VALID, "    su_refs: [C-001]\n\nentities:",
                          "    su_refs: [banana]\n\nentities:"),
        "BP-DEAD-ID": swap(VALID, "    su_refs: [C-001]\n\nentities:",
                           "    su_refs: [C-999]\n\nentities:"),
        "BP-STRUCT-TYPE": swap(VALID, "      structural: false", "      structural: maybe"),
        "BP-STRUCT-MISSING": swap(VALID, "      structural: false\n", ""),
        "BP-STRUCT-NO-SETTLE": swap(
            swap(VALID, "      would_be_settled_by: \"sessão com os analistas\"\n", ""),
            "      structural: false", "      structural: true"),
        "BP-RESOLVED-TYPE": swap(VALID, "      resolved: false", "      resolved: sim"),
        "BP-RESOLVED-NO-BASIS": swap(swap(VALID, "      structural: false",
                                          "      structural: true"),
                                     "      resolved: false", "      resolved: true"),
        "BP-PO-REQ": swap(VALID, "      owner: developer\n", ""),
        "BP-DRAFT": swap(VALID, "draft: false", "draft: true"),
        "BP-NESTED-SPLIT": swap(VALID, "  open_architecture_choices:\n",
                                "  open_architecture_choices:\n    - U-001\n"),
        "BP-YAML-MALFORMED": VALID.replace("open_questions: [U-001]",
                                           "open_questions:\n\t- U-001"),
        "BP-YAML-UNSUPPORTED": VALID + "\n---\nversion: 2\n",
    }
    for code, text in sorted(cases.items()):
        verdict(code in all_codes(text), "dispara: " + code)
    verdict("BP-VERSION" in blocking(VALID, name="ux-blueprint_v02.yaml"),
            "dispara: BP-VERSION")
    missing = sorted(set(D["BP_SEVERITY"]) - set(cases) - {"BP-VERSION"})
    verdict(not missing, "todos os códigos da tabela têm caso", ", ".join(missing))

    head("D'", "Medição sobre os blueprints reais (imprime-se, não se aprova)")
    tot, files = Counter(), sorted(glob.glob(str(ENG_ROOT / "*" / "_blueprint" / "ux-blueprint_v*.y*ml")))
    if slug:
        files = [f for f in files if slug in f]
    for f in files:
        p = Path(f)
        eng = p.parent.parent
        rows = D["parse_su"](D["_read"](eng / "shared-understanding.md") or "")[1]
        iss = D["bp_validate"](D["_read"](p) or "", p.name,
                               D["bp_pack_cfg"](D["_read_json"](eng / "_state.json").get("pack", "")),
                               {r["id"] for r in rows if r.get("id")}, D["bp_loader"](eng))
        c = Counter(i["code"] for i in iss)
        tot.update(c)
        nb = sum(1 for i in iss if i["severity"] == "block")
        measure("{} / {}".format(eng.name, p.name),
                "block={} warn={} {}".format(nb, len(iss) - nb, dict(sorted(c.items()))))
    measure("total por código", dict(sorted(tot.items())))


# ----------------------------------------------------------------------- E

def criterion_e():
    head("E", "Aprovação sobre versão inválida — os quatro consumidores")
    decisions = ("# Decisions\n\n## D-002 — Adopt O-001\n- **Chosen option**: O-001\n"
                 "- **Timestamp**: 2026-09-02T10:00:00Z\n\n"
                 "## D-003 — Blueprint bp-v01 aprovado\n- **Timestamp**: 2026-09-08T10:00:00Z\n")
    with tempfile.TemporaryDirectory() as tmp:
        eng = Path(tmp) / "fx"
        (eng / "_blueprint").mkdir(parents=True)
        (eng / "_state.json").write_text(json.dumps(
            {"engagement": "fx", "pack": "pp", "phase": "decision", "round": "D-01"}),
            encoding="utf-8")
        (eng / "decisions.md").write_text(decisions, encoding="utf-8")
        (eng / "shared-understanding.md").write_text("# SU\n", encoding="utf-8")
        bad = swap(VALID, "      structural: false\n", "")
        (eng / "_blueprint" / "ux-blueprint_v01.yaml").write_text(bad, encoding="utf-8")
        blocks = D["classify_decisions"](decisions)

        bp = D["blueprint_state"](eng, blocks, [], "pp")
        verdict(bp["approved"] is not None, "1/4 motor: a aprovação continua registada (é história)")
        verdict(bp["approved_valid"] is False, "1/4 motor: `approved_valid` é falso")

        import io
        from contextlib import redirect_stdout, redirect_stderr
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            rc = D["main"](["--engagement", str(eng), "--authority-stamp"])
        verdict(rc == 5 and "INVALID" in out.getvalue(),
                "2/4 carimbo: sai 5 e diz INVALID", "rc={}".format(rc))

        good = VALID
        (eng / "_blueprint" / "ux-blueprint_v01.yaml").write_text(good, encoding="utf-8")
        out2 = io.StringIO()
        with redirect_stdout(out2), redirect_stderr(io.StringIO()):
            rc2 = D["main"](["--engagement", str(eng), "--authority-stamp"])
        verdict(rc2 == 0 and "INVALID" not in out2.getvalue(),
                "2/4 carimbo: uma versão válida carimba normalmente")

    # 3/4 render-validate e 4/4 frescura, no engagement real que os exercita
    pilot = ENG_ROOT / "pricing-marinha-pilot-1"
    if (pilot / "_state.json").is_file():
        V = runpy.run_path(str(ROOT / ".claude" / "hooks" / "render-validate.py"))
        rendered = sorted((pilot / "_render").glob("*implementation-spec*.md"))
        if rendered:
            r = V["validate"](pilot, "implementation-spec", rendered[-1])
            has = any(g["slot"] == "blueprint" for g in r["gaps"])
            verdict(has or r.get("approved_invalid") is None,
                    "3/4 render: a aprovação inválida vira gap (sem apagar os de conteúdo)",
                    "gaps={}".format(sorted({g["slot"] for g in r["gaps"]})))
            if r.get("approved_invalid"):
                measure("3/4 render: versão aprovada inválida", r["approved_invalid"])
        model = D["build_model"](pilot, __import__("datetime").date.today())
        arch = model["status"]["synthesis"]["topics"]["architecture-story"]
        measure("4/4 frescura: identidade do architecture-story", arch["identity"])
    else:
        measure("3/4 e 4/4", "pilot-1 não montado — não avaliados")


# ----------------------------------------------------------------------- F

def criterion_f():
    head("F", "Ligações — skill, hook, settings, contrato, packs, versão")
    skill = (ROOT / ".claude" / "skills" / "aisa-blueprint" / "SKILL.md").read_text(encoding="utf-8")
    verdict(skill.count("--blueprint-check") >= 2,
            "aisa-blueprint nomeia a verificação ao escrever e ao aprovar",
            "ocorrências: {}".format(skill.count("--blueprint-check")))
    st = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
    cmds = [h["command"] for e in st["hooks"]["PostToolUse"] for h in e["hooks"]]
    verdict(any("blueprint-validate.py" in c for c in cmds),
            "hook ligado em settings.json")   # forma, nao frase (R7)
    hooks_md = (ROOT / ".claude" / "hooks" / "HOOKS.md").read_text(encoding="utf-8")
    verdict("`blueprint-validate.py`" in hooks_md, "HOOKS.md documenta o hook")
    contract = (ROOT / "library" / "kernel" / "blueprint-contract.md").read_text(encoding="utf-8")
    verdict("## Validação estrutural" in contract, "contrato tem a secção")
    missing = [c for c in D["BP_SEVERITY"] if c not in contract]
    verdict(not missing, "cada código está no contrato", ", ".join(missing))
    for y in ("Y1", "Y2", "Y3", "Y4", "Y5", "Y6", "Y7"):
        if y not in contract:
            verdict(False, "subconjunto YAML declarado no contrato", y + " em falta")
            break
    else:
        verdict(True, "subconjunto YAML declarado no contrato (Y1-Y7)")
    for pack in ("pp", "generic", "outsystems", "mendix"):
        p = ROOT / "library" / "packs" / pack / "pack.yaml"
        if p.is_file():
            verdict("\nblueprint:" in p.read_text(encoding="utf-8"),
                    "pack {} declara o bloco blueprint".format(pack))
    verdict(D["TOOL_VERSION"] == "1.13.0", "motor em 1.13.0", D["TOOL_VERSION"])
    for skill_name, needle in (("aisa-synthesize", "INVALID"),
                               ("aisa-render", "approved_valid"),
                               ("aisa-status", "blueprint.versions[].valid")):
        text = (ROOT / ".claude" / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
        verdict(needle in text, "{} reage à aprovação inválida".format(skill_name))


# ----------------------------------------------------------------------- G

def criterion_g():
    head("G", "Suite")
    py = ROOT / ".test-venv" / "Scripts" / "python.exe"
    exe = str(py) if py.is_file() else sys.executable
    r = subprocess.run([exe, "-m", "pytest", str(ROOT / ".claude" / "tests"), "-q"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       cwd=str(ROOT))
    tail = [l for l in (r.stdout or "").strip().splitlines() if l.strip()][-1:]
    if r.returncode != 0 and "No module named pytest" in (r.stdout + r.stderr):
        fails = []
        for f in sorted((ROOT / ".claude" / "tests").glob("test_*.py")):
            rr = subprocess.run([exe, str(f)], capture_output=True, text=True,
                                encoding="utf-8", errors="replace", cwd=str(ROOT))
            if rr.returncode != 0:
                fails.append(f.name)
        verdict(not fails, "suite verde (unittest)", ", ".join(fails))
        return
    verdict(r.returncode == 0, "suite verde", tail[0] if tail else "")
    if tail:
        measure("resultado", tail[0])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--engagement", help="restringe a medição a um slug")
    ap.add_argument("--skip-suite", action="store_true", help="não corre a suite (G)")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    print("Aceitação — fase 1 (bloco A) · repo {} · engagements {}".format(ROOT, ENG_ROOT))
    criterion_a()
    criterion_b(args.engagement)
    criterion_c()
    criterion_d(args.engagement)
    criterion_e()
    criterion_f()
    if not args.skip_suite:
        criterion_g()
    print("\n" + "=" * 78)
    if FAILED:
        print("FALHA — {} critério(s): {}".format(len(FAILED), "; ".join(FAILED)))
        return 1
    print("Fase 1: todos os critérios com veredicto passam.")
    print("As medições sobre engagements reais imprimem-se e não se aprovam (§11).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
