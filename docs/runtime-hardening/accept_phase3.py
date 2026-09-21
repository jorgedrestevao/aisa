# -*- coding: utf-8 -*-
"""Aceitação executável da fase 3 do endurecimento do runtime (bloco C).

    python docs/runtime-hardening/accept_phase3.py
    python docs/runtime-hardening/accept_phase3.py --engagement <slug>
    python docs/runtime-hardening/accept_phase3.py --only-phase3

Não escreve nada nos engagements. Sai 0 quando todos os critérios com veredicto passam,
1 quando algum falha.

ORDEM DE EXECUÇÃO (decisão do dono, 2026-09-10): fase 1 → **fase 3** → fase 2 → os quatro
pilotos ponta-a-ponta. Este script corre a fase 1 (regressão) e a fase 3 (o que se
acrescentou). **NÃO corre a fase 2**: os seus cenários de intake ainda não existem, e um
critério que não correu não pode aparecer como aprovado. A fase 2 é reportada, com todas as
letras, como PENDENTE — nem verde, nem vermelha.

O que verifica, por ordem (plano §6 C4):

  A. Os dois stubs desapareceram: nenhum dos hooks anuncia validação que não faz.
  B. Ligações: `phase-gate-check.py` em PreToolUse/Skill, `synthesis-validate.py` em
     PostToolUse/Write|Edit, `_common.py` partilhado, skills e phases.md a apontar.
  C. Cobertura por engagement montado: todos os critérios da fase corrente com o seu modo.
     Medição — os engagements antigos falham critérios por construção e lêem-se.
  D. Ciclo de vida do gate: primeira linha, override com `refers`, estado alterado com
     `refers: none`, stdin inválido sem escrita, exit 0 em tudo.
  D2. Impressão digital por conteúdo: contagens iguais e ids diferentes → ids diferentes.
  D3. Engagement: inferido quando há um, recusado quando há vários sem slug.
  E. Frescura intocada: validar um pack velho mantém-no velho e `_synthesis-log.md`
     byte-idêntico.
  F. Códigos da síntese: os que disparam e os três que NÃO disparam.
  G. Medição sobre os `_synthesis/` reais.
  H. Suite verde · fase 1 verde · **fase 2 pendente, declarada**.
"""

import argparse
import glob
import json
import os
import runpy
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
ENG_ROOT = Path(os.environ.get("AISA_ENGAGEMENTS_ROOT") or (ROOT / "projects"))
HERE = Path(os.path.dirname(os.path.abspath(__file__)))
D = runpy.run_path(str(ROOT / "library" / "kernel" / "tools" / "dashboard.py"))
GATE_HOOK = ROOT / ".claude" / "hooks" / "phase-gate-check.py"
SYN_HOOK = ROOT / ".claude" / "hooks" / "synthesis-validate.py"

FAILED: list[str] = []
PENDING: list[str] = []


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


def pending(label: str, why: str) -> None:
    print("  [PEND] {}  — {}".format(label, why))
    PENDING.append(label)


# ------------------------------------------------------------ fixture helpers

SU_COLS = {
    "Confirmed": ["id", "lens", "claim", "evidência", "verificado_em", "validade", "ronda"],
    "Assumed": ["id", "lens", "claim", "base da assumption", "verificado_em", "validade", "ronda"],
    "Unknown": ["id", "lens", "pergunta", "quem responde", "criticidade", "custo", "swing", "ronda"],
    "Conflicted": ["id", "lens", "conflito", "partes", "criticidade", "ronda"],
    "Risky": ["id", "lens", "risco", "impacto", "mitigação proposta", "ronda"],
}


def su_text(slug, sections=None):
    out = ["# Shared Understanding — {}\n\n**Engagement**: {}\n**Phase**: discovery\n"
           "**Pack**: pp\n**Last updated**: 2026-09-10\n".format(slug, slug)]
    for name, cols in SU_COLS.items():
        out.append("## " + name + "\n")
        out.append("| " + " | ".join(cols) + " |")
        out.append("|" + "|".join(["---"] * len(cols)) + "|")
        for cells in (sections or {}).get(name, []):
            out.append("| " + " | ".join(str(c) for c in cells) + " |")
        out.append("")
    return "\n".join(out) + "\n"


def mk(tmp, slug, sections=None, phase="discovery"):
    eng = Path(tmp) / slug
    (eng / "lens-outputs").mkdir(parents=True, exist_ok=True)
    (eng / "_state.json").write_text(json.dumps(
        {"engagement": slug, "pack": "pp", "phase": phase, "round": "R-01"}), encoding="utf-8")
    (eng / "shared-understanding.md").write_text(su_text(slug, sections), encoding="utf-8")
    for rel, body in (("decisions.md", "# Decisions\n"), ("options.md", ""),
                      ("frame.md", ""), ("council-log.md", "# Council log\n")):
        (eng / rel).write_text(body, encoding="utf-8")
    for lens in D["LENSES_6"]:
        (eng / "lens-outputs" / (lens + ".md")).write_text("# x\n\nC-001\n", encoding="utf-8")
    return eng


def confirmed(n):
    return [["C-{:03d}".format(i), "business", "facto", "inputs/x.xlsx#S!A{}".format(i),
             "2026-09-01", "organizacional", "R-01"] for i in range(1, n + 1)]


def unknown(ids):
    return [[i, "data", "q?", "role: IT", "Critical", "baixo", "decisivo", "R-01"] for i in ids]


def fire_gate(root, args, payload_skill="aisa-frame"):
    env = dict(os.environ)
    env["AISA_ENGAGEMENTS_ROOT"] = str(root)
    return subprocess.run(
        [sys.executable, str(GATE_HOOK)],
        input=json.dumps({"tool_name": "Skill",
                          "tool_input": {"skill": payload_skill, "args": args}}),
        text=True, capture_output=True, encoding="utf-8", errors="replace",
        cwd=str(ROOT), env=env)


def fire_syn(path):
    return subprocess.run(
        [sys.executable, str(SYN_HOOK)],
        input=json.dumps({"tool_name": "Write", "tool_input": {"file_path": str(path)}}),
        text=True, capture_output=True, encoding="utf-8", errors="replace", cwd=str(ROOT))


# ----------------------------------------------------------------------- A

def criterion_a():
    head("A", "Os stubs desapareceram")
    for name in ("phase-gate-check.py", "synthesis-validate.py"):
        text = (ROOT / ".claude" / "hooks" / name).read_text(encoding="utf-8")
        verdict("v0.2.0 will validate" not in text, "{}: sem promessa por cumprir".format(name))
        verdict("log-only" not in text.lower(), "{}: não se diz log-only".format(name))
    md = (ROOT / ".claude" / "hooks" / "HOOKS.md").read_text(encoding="utf-8")
    verdict("**Log only.**" not in md, "HOOKS.md: nenhum hook descrito como log only")
    verdict("gate-log.md" in md and "_synthesis-checks.md" in md,
            "HOOKS.md: nomeia onde cada um regista")


# ----------------------------------------------------------------------- B

def criterion_b():
    head("B", "Ligações")
    st = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
    pre = [h["command"] for e in st["hooks"]["PreToolUse"] if e.get("matcher") == "Skill"
           for h in e["hooks"]]
    post_skill = [h["command"] for e in st["hooks"].get("PostToolUse", [])
                  if e.get("matcher") == "Skill" for h in e["hooks"]]
    post_write = [h["command"] for e in st["hooks"].get("PostToolUse", [])
                  if e.get("matcher") == "Write|Edit" for h in e["hooks"]]
    # forma, nao frase: a invocacao mudou em R7 (DEF-P1-02)
    verdict(any("phase-gate-check.py" in c for c in pre),
            "phase-gate-check em PreToolUse/Skill")
    verdict(not any("phase-gate-check.py" in c for c in post_skill),
            "phase-gate-check saiu de PostToolUse")
    verdict(any("synthesis-validate.py" in c for c in post_write),
            "synthesis-validate em PostToolUse/Write|Edit")
    verdict((ROOT / ".claude" / "hooks" / "_common.py").is_file(), "_common.py existe")
    for name in ("phase-gate-check.py", "synthesis-validate.py"):
        text = (ROOT / ".claude" / "hooks" / name).read_text(encoding="utf-8")
        verdict("from _common import" in text, "{} usa _common".format(name))
    for name in ("aisa-frame", "aisa-options", "aisa-decide"):
        md = (ROOT / ".claude" / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
        verdict("gate-log.md" in md, "{} lê o veredicto".format(name))
    # A ponta que faltava (revisão da fase 3): o hook recusava correctamente, e nenhum
    # comando resolvia o engagement — logo `/options` sem argumentos não produzia veredicto.
    for name in ("frame", "options", "decide"):
        md = (ROOT / ".claude" / "commands" / (name + ".md")).read_text(encoding="utf-8")
        verdict("--which-engagement" in md and "--engagement <slug>" in md,
                "/{} resolve e passa o engagement".format(name))
        verdict("AskUserQuestion" in md,
                "/{} pergunta quando é ambíguo, não adivinha".format(name))
    syn = (ROOT / ".claude" / "skills" / "aisa-synthesize" / "SKILL.md").read_text(encoding="utf-8")
    verdict("synthesis_checks" in syn and "_synthesis-checks.md" in syn,
            "aisa-synthesize lê o check recalculado")
    verdict("Never** write a check line into `_synthesis-log.md`" in syn
            or "never** write a check line into `_synthesis-log.md`" in syn.lower(),
            "aisa-synthesize proíbe escrever checks no log de síntese")
    ph = (ROOT / "library" / "kernel" / "phases.md").read_text(encoding="utf-8")
    verdict("evaluated** by the `phase-gate-check.py` hook" in ph,
            "phases.md deixa de dizer 'apenas avisos'")
    stt = (ROOT / ".claude" / "skills" / "aisa-status" / "SKILL.md").read_text(encoding="utf-8")
    verdict("status.gates" in stt and "synthesis_checks" in stt, "aisa-status lê ambos")


# ----------------------------------------------------------------------- C

def criterion_c(slug):
    head("C", "Cobertura por engagement montado (medição — não se aprova)")
    engs = [p.parent for p in sorted(ENG_ROOT.glob("*/_state.json"))]
    if slug:
        engs = [e for e in engs if e.name == slug]
    if not engs:
        measure("engagements montados", "nenhum")
        return
    seen_modes = set()
    for eng in engs:
        st = json.loads((eng / "_state.json").read_text(encoding="utf-8"))
        phase = st.get("phase", "")
        transition = {"discovery": "discovery→framing", "framing": "framing→options",
                      "options": "options→decision"}.get(phase)
        if not transition:
            measure(eng.name, "fase {} — sem portão de saída".format(phase))
            continue
        g = D["gate_state"](eng, transition)
        seen_modes |= {c["mode"] for c in g["criteria"]}
        measure(eng.name, "{} · {} · red: {}".format(
            g["id"], g["note"], ", ".join(g["red"]) or "nenhum"))
        for c in g["criteria"]:
            mark = {"codigo": ("ok " if c["ok"] else "RED"), "juizo": "juí", "n/a": "n/a"}[c["mode"]]
            print("           [{}] {} — {}".format(mark, c["criterion"], c["value"] or c["note"]))
    if seen_modes:
        verdict("codigo" in seen_modes, "há critérios avaliados por código")
        verdict(bool({"juizo", "n/a"} & seen_modes),
                "há critérios declarados como juízo ou não avaliáveis",
                ", ".join(sorted(seen_modes)))


# ----------------------------------------------------------------------- D

def criterion_d():
    head("D", "Ciclo de vida do portão")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        eng = mk(root, "fx", {"Confirmed": confirmed(3)})
        r1 = fire_gate(root, "--engagement fx")
        log = (eng / "gate-log.md")
        lines = [l for l in log.read_text(encoding="utf-8").splitlines() if l.startswith("2")] \
            if log.is_file() else []
        verdict(r1.returncode == 0, "primeira invocação: exit 0")
        verdict(len(lines) == 1, "primeira invocação: uma linha", str(len(lines)))
        if lines:
            verdict("por código" in lines[0], "a linha declara a cobertura")
            verdict("Confirmed >= 10" in lines[0], "a linha nomeia o critério vermelho")
            gid = next((c for c in lines[0].split(" · ") if c.startswith("G-")), "")
            fire_gate(root, '--engagement fx --override "o dono aceita avançar"')
            lines = [l for l in log.read_text(encoding="utf-8").splitlines() if l.startswith("2")]
            verdict(len(lines) == 2, "override: segunda linha", str(len(lines)))
            verdict('override: yes "o dono aceita avançar"' in lines[1],
                    "override: a razão fica registada")
            verdict("refers: " + gid in lines[1],
                    "override: liga-se à avaliação que responde")
            (eng / "shared-understanding.md").write_text(
                su_text("fx", {"Confirmed": confirmed(12)}), encoding="utf-8")
            fire_gate(root, '--engagement fx --override "avançar"')
            last = [l for l in log.read_text(encoding="utf-8").splitlines()
                    if l.startswith("2")][-1]
            verdict("refers: none" in last,
                    "estado alterado entre as duas: refers none, não uma ligação falsa")
        r = subprocess.run([sys.executable, str(GATE_HOOK)], input="not json", text=True,
                           capture_output=True, encoding="utf-8", errors="replace",
                           cwd=str(ROOT))
        verdict(r.returncode == 0, "stdin inválido: exit 0")

    head("D2", "Impressão digital por conteúdo, não por contagens")
    with tempfile.TemporaryDirectory() as tmp:
        a = mk(Path(tmp), "a", {"Confirmed": confirmed(12), "Unknown": unknown(["U-001"])})
        b = mk(Path(tmp), "b", {"Confirmed": confirmed(12), "Unknown": unknown(["U-002"])})
        ga, gb = D["gate_state"](a, "discovery→framing"), D["gate_state"](b, "discovery→framing")
        same_counts = (ga["evaluated"], ga["total"]) == (gb["evaluated"], gb["total"])
        verdict(same_counts, "as contagens são iguais nos dois estados")
        verdict(ga["id"] != gb["id"], "o id muda com o id da linha", ga["id"] + " vs " + gb["id"])
        verdict(D["gate_state"](a, "discovery→framing")["id"] == ga["id"],
                "o mesmo estado dá o mesmo id")
    with tempfile.TemporaryDirectory() as tmp:
        eng = mk(Path(tmp), "fr", phase="framing")
        (eng / "frame.md").write_text("# Frame\n\nThe problem is X, felt by Y.\n", encoding="utf-8")
        before = D["gate_state"](eng, "framing→options")
        (eng / "decisions.md").write_text(
            "# Decisions\n\n## D-001 — Frame agreed\n- **Validated by**: sponsor\n", encoding="utf-8")
        after = D["gate_state"](eng, "framing→options")
        verdict(before["id"] != after["id"],
                "acrescentar uma aprovação a decisions.md muda o id")

    head("D3", "Engagement: explícito, inferido, ou nada")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        solo = mk(root, "solo", {"Confirmed": confirmed(12)})
        fire_gate(root, "")
        verdict((solo / "gate-log.md").is_file(), "um só montado: infere e escreve")
        if (solo / "gate-log.md").is_file():
            verdict("engagement: only" in (solo / "gate-log.md").read_text(encoding="utf-8"),
                    "e diz que inferiu")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        a = mk(root, "a", {"Confirmed": confirmed(12)})
        b = mk(root, "b", {"Confirmed": confirmed(12)})
        r = fire_gate(root, "")
        verdict("ambiguous engagement" in r.stderr, "vários sem slug: recusa avaliar")
        verdict(not (a / "gate-log.md").is_file() and not (b / "gate-log.md").is_file(),
                "vários sem slug: não escreve em nenhum")
        fire_gate(root, "--engagement b")
        verdict((b / "gate-log.md").is_file() and not (a / "gate-log.md").is_file(),
                "o slug desambigua")


# ----------------------------------------------------------------------- E

def criterion_e():
    head("E", "A frescura fica intocada (o defeito que o ficheiro próprio evita)")
    T = runpy.run_path(str(ROOT / ".claude" / "tests" / "test_synthesis_checks.py"))
    with tempfile.TemporaryDirectory() as tmp:
        su = T["SU"].replace(
            "| C-002 | data | o histórico vive numa base partilhada | inputs/x.xlsx#S!A2 "
            "| 2026-09-01 | organizacional | R-01 |",
            "| C-002 | operations | o histórico vive numa base partilhada | "
            "inputs/x.xlsx#S!A2 | 2026-09-07 | organizacional | R-01 |")
        eng = T["mk"](tmp, su=su,
                      log="# Synthesis Log\n\n2026-09-03T10:00:00Z — as-is — sources: 1\n")
        st = D["build_model"](eng, date(2026, 9, 10))["status"]["synthesis"]
        verdict(st["topics"]["as-is"]["verdict"] == "stale",
                "a pré-condição é real: o pack está velho",
                st["topics"]["as-is"]["verdict"])
        before = (eng / "_synthesis" / "_synthesis-log.md").read_bytes()
        r = fire_syn(eng / "_synthesis" / "as-is.md")
        after = (eng / "_synthesis" / "_synthesis-log.md").read_bytes()
        verdict(r.returncode == 0, "validar não bloqueia")
        verdict(before == after, "_synthesis-log.md byte-idêntico")
        st2 = D["build_model"](eng, date(2026, 9, 10))["status"]["synthesis"]
        verdict(st2["topics"]["as-is"]["verdict"] == "stale",
                "validar um pack velho mantém-no velho", st2["topics"]["as-is"]["verdict"])
        checks = (eng / "_synthesis" / "_synthesis-checks.md").read_text(encoding="utf-8")
        verdict(D["synthesis_entries"](checks) == [],
                "as linhas de check não se leem como corridas de síntese")


# ----------------------------------------------------------------------- F

def criterion_f():
    head("F", "Códigos da síntese: os que disparam e os que NÃO disparam")
    T = runpy.run_path(str(ROOT / ".claude" / "tests" / "test_synthesis_checks.py"))
    GOOD, mk_t = T["GOOD"], T["mk"]
    with tempfile.TemporaryDirectory() as tmp:
        cases = {
            "SYN-PARAS": "# As-is\n\nUm (C-001).\n\nDois (C-002).\n",
            "SYN-NO-IDS": "# As-is\n\nUm.\n\nDois.\n\nTrês.\n",
            "SYN-DEAD-ID": GOOD.replace("C-002", "C-999"),
            "SYN-VENDOR": GOOD + "\nSeria feito em Power Apps (C-001).\n",
        }
        for code, body in cases.items():
            eng = mk_t(tmp, slug="c" + code, packs={"as-is": body})
            got = sorted(c["code"] for c in D["synthesis_check"](eng, "as-is")["codes"])
            verdict(code in got, "dispara: " + code, ", ".join(got))
        eng = mk_t(tmp, slug="clean")
        verdict(not D["synthesis_check"](eng, "as-is")["codes"], "um pack bom fica limpo")
        eng = mk_t(tmp, slug="sp",
                   packs={"as-is": GOOD + "\nOs ficheiros vivem no SharePoint (C-002).\n"})
        got = [c["code"] for c in D["synthesis_check"](eng, "as-is")["codes"]]
        verdict("SYN-VENDOR" not in got,
                "NÃO dispara: `sharepoint` num as-is (nomeia o estado actual)")
        eng = mk_t(tmp, slug="none", packs={"architecture-story":
                   "# Architecture Story\n<!-- authority: none — outcome-forbade -->\n\n"
                   "A escolha não autoriza arquitectura (C-001).\n\nO âmbito é de processo (C-002).\n\n"
                   "Nada se constrói (C-001).\n"})
        got = [c["code"] for c in D["synthesis_check"](eng, "architecture-story")["codes"]]
        verdict("SYN-STAMP" not in got,
                "NÃO dispara: `authority: none — <razão>` (caso legítimo sem arquitectura)")
        res = D["synthesis_check"](mk_t(tmp, slug="gen"), "as-is", pack="generic")
        verdict(any("SYN-VENDOR" in n for n in res["not_evaluated"]),
                "sem lista no pacote: não avaliado, nunca 'ok'")
    solution = set(D["pack_vendor_terms"]("pp"))
    verdict("dataverse" in solution and not ({"sharepoint", "microsoft", "azure", "excel"} & solution),
            "a lista de solução não é a lista de Discovery")

    head("F2", "SYN-STAMP: a autoridade citada tem de existir")
    bp_file = ROOT / ".claude" / "tests" / "fixtures" / "blueprints" / "valid_min_v01.yaml"
    if not bp_file.is_file():
        measure("SYN-STAMP", "fixture de blueprint ausente - nao avaliado")
        return
    valid = bp_file.read_text(encoding="utf-8")
    approved = (T["DECISIONS"] + "\n## D-003 - Blueprint bp-v01 aprovado\n"
                "- **Timestamp**: 2026-09-08T10:00:00Z\n")
    sha = D["architecture_block_sha256"](valid)

    def story(stamp):
        return ("# Architecture Story\n" + stamp + "\n\nUm (C-001).\n\nDois (C-002).\n\n"
                "Tres (C-001).\n")

    def stamp_of(ver, digest):
        return ("<!-- authority: _blueprint/ux-blueprint_" + ver +
                ".yaml#architecture @ sha256:" + digest + " -->")

    with tempfile.TemporaryDirectory() as tmp:
        n = [0]

        def check(body, blueprints=None, decisions=None):
            n[0] += 1
            eng = mk_t(tmp, slug="stamp%d" % n[0], packs={"architecture-story": body},
                       blueprints=blueprints or {}, decisions=decisions or T["DECISIONS"])
            return D["synthesis_check"](eng, "architecture-story")["codes"]

        ghost = check(story(stamp_of("v99", "0" * 64)))
        verdict(bool(ghost) and "nao existe" in ghost[0]["detail"],
                "dispara: carimbo de uma versao que nao existe")
        trunc = check(story(stamp_of("v01", "deadbeef")), {"v01": valid}, approved)
        verdict(bool(trunc) and "64 hex" in trunc[0]["detail"],
                "dispara: sha256 que nao e um sha256")
        wrong = check(story(stamp_of("v01", "f" * 64)), {"v01": valid}, approved)
        verdict(any("sha256 difere" in c["detail"] for c in wrong),
                "dispara: sha que nao corresponde ao bloco")
        not_auth = valid.replace("authorization: authorized", "authorization: not-authorized")
        unauth = check(story(stamp_of("v01", D["architecture_block_sha256"](not_auth))),
                       {"v01": not_auth})
        verdict(any("nao autorizada" in c["detail"] for c in unauth),
                "dispara: carimbo de uma versao nao autorizada")
        unsupported = check(story("<!-- authority: none - outcome-forbade -->"),
                            {"v01": valid}, approved)
        verdict(bool(unsupported) and "nao se sustenta" in unsupported[0]["detail"],
                "dispara: `authority: none` com arquitectura autorizada no disco")
        bad_reason = check(story("<!-- authority: none - porque -->"))
        verdict(bool(bad_reason) and "razao reconhecida" in bad_reason[0]["detail"],
                "dispara: razao nao reconhecida")
        verdict(check(story(stamp_of("v01", sha)), {"v01": valid}, approved) == [],
                "NAO dispara: o carimbo certo da versao aprovada")

    # ---- `authority: none`: alcance ESTRUTURAL contra os pares (scope, outcome) ------
    # Decisao do dono (A+C, 2026-09-11): falta de informacao historica nao e inconsistencia
    # verificavel, e o motor nao as junta. 2 de 23 engagements persistem os pares.
    head("F3", "`authority: none`: os quatro casos do alcance estrutural")
    PAIRS_TAIL = ("\n- **Selected solution / composition**: mudar o processo, construir nada"
                  "\n- **(Scope, outcome) pairs - UNCOLLAPSED**:"
                  "\n  - whole solution - \"nenhuma alternativa de construcao e viavel\"\n")
    with tempfile.TemporaryDirectory() as tmp:
        k = [0]

        def res(body, blueprints=None, decisions=None):
            k[0] += 1
            eng = mk_t(tmp, slug="pair%d" % k[0], packs={"architecture-story": body},
                       blueprints=blueprints or {}, decisions=decisions or T["DECISIONS"])
            return D["synthesis_check"](eng, "architecture-story")

        def none(reason="outcome-forbade"):
            return story("<!-- authority: none - " + reason + " -->")

        # 1. ausencia -> nao avaliado, com motivo. Nunca verificado, nunca falha.
        for label, dec in (("sem decisao de solucao", "# Decisions\n"),
                           ("decisao generica sem pares", T["DECISIONS"])):
            r = res(none(), decisions=dec)
            verdict(r["codes"] == [] and bool(r["not_evaluated"]),
                    "nao avaliado (nao limpo, nao falha): " + label,
                    "; ".join(x[:60] for x in r["not_evaluated"]))
            verdict(not r["notes"], "e sem nota de base documental: " + label)

        # 2. presenca -> estrutura validada, e a nota diz o que nao foi julgado
        r = res(none(), decisions=T["DECISIONS"] + PAIRS_TAIL)
        verdict(r["codes"] == [] and r["not_evaluated"] == [] and bool(r["notes"]),
                "pares completos: estrutura satisfeita")
        verdict(bool(r["notes"]) and "SIGNIFICADO" in r["notes"][0],
                "e a nota declara que o significado da razao nao foi avaliado")

        # 3. `outside-pack-authority` fala da solucao seleccionada
        no_sel = (T["DECISIONS"] + "\n- **(Scope, outcome) pairs - UNCOLLAPSED**:"
                  "\n  - whole solution - \"nao ha alternativa de construcao\"\n")
        r = res(none("outside-pack-authority"), decisions=no_sel)
        verdict([c["code"] for c in r["codes"]] == ["SYN-STAMP"]
                and "solucao seleccionada" in r["codes"][0]["detail"],
                "dispara: outside-pack-authority sem a solucao seleccionada")
        verdict(res(none("outcome-forbade"), decisions=no_sel)["codes"] == [],
                "e a mesma decisao serve outcome-forbade, que nao fala da solucao")

        # 4. malformado e contradicao -> SYN-STAMP, nunca nao avaliado
        bad = (T["DECISIONS"] + "\n- **(Scope, outcome) pairs - UNCOLLAPSED**:"
               "\n  - whole solution\n")
        r = res(none(), decisions=bad)
        verdict([c["code"] for c in r["codes"]] == ["SYN-STAMP"]
                and r["not_evaluated"] == [],
                "dispara (nao converte em nao avaliado): pares malformados")
        r = res(none(), {"v01": valid}, approved + PAIRS_TAIL)
        verdict([c["code"] for c in r["codes"]] == ["SYN-STAMP"]
                and r["not_evaluated"] == [],
                "dispara (nao converte em nao avaliado): contradicao verificavel")

        # 5. a decisao EM VIGOR e a unica que fornece a evidencia
        superseded = (T["DECISIONS"] + PAIRS_TAIL +
                      "\n## D-003 - Adopt O-004 (supersedes D-002)"
                      "\n- **Chosen option**: O-004"
                      "\n- **(Scope, outcome) pairs - UNCOLLAPSED**:"
                      "\n  - whole solution"
                      "\n- **Timestamp**: 2026-09-06T10:00:00Z\n")
        pr = D["decision_scope_outcome_pairs"](superseded)
        verdict(pr["decision"] == "D-003" and not pr["pairs"] and bool(pr["malformed"]),
                "os pares vem do bloco da decisao em vigor, nao do substituido",
                "decisao lida: " + (pr["decision"] or "-"))
        r = res(none(), decisions=superseded)
        verdict([c["code"] for c in r["codes"]] == ["SYN-STAMP"]
                and "malformados" in r["codes"][0]["detail"],
                "dispara: D-003 com pares malformados nao herda os de D-002")

    # Medicao: quantos engagements reais tem a base documental. A presenca dos dados e o
    # criterio -- a geracao nunca se infere pela data nem pela versao.
    withp = [p.parent.name for p in sorted(ENG_ROOT.glob("*/decisions.md"))
             if D["decision_scope_outcome_pairs"](
                 D["_read"](p) or "")["pairs"]]
    total = len(list(ENG_ROOT.glob("*/decisions.md")))
    measure("engagements com pares (scope, outcome)",
            "{} de {} — {}".format(len(withp), total, ", ".join(withp) or "nenhum"))


def criterion_g(slug):
    head("G", "Medição sobre os `_synthesis/` reais")
    engs = [p.parent for p in sorted(ENG_ROOT.glob("*/_state.json"))
            if (p.parent / "_synthesis").is_dir()]
    if slug:
        engs = [e for e in engs if e.name == slug]
    if not engs:
        measure("engagements com síntese", "nenhum")
        return
    for eng in engs:
        checks = D["synthesis_checks"](eng)
        line = "; ".join("{}: {}".format(t, ",".join(v["codes"]) or v["verdict"])
                         for t, v in checks["topics"].items())
        measure(eng.name, line)


# ----------------------------------------------------------------------- H

def criterion_h(skip_suite):
    head("H", "Suite, fase 1, e o estado da fase 2")
    if not skip_suite:
        py = ROOT / ".test-venv" / "Scripts" / "python.exe"
        exe = str(py) if py.is_file() else sys.executable
        r = subprocess.run([exe, "-m", "pytest", str(ROOT / ".claude" / "tests"), "-q"],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", cwd=str(ROOT))
        tail = [l for l in (r.stdout or "").strip().splitlines() if l.strip()][-1:]
        verdict(r.returncode == 0, "suite verde", tail[0] if tail else "")
    else:
        pending("suite", "--skip-suite pedido")

    p1 = HERE / "accept_phase1.py"
    if p1.is_file():
        r = subprocess.run([sys.executable, str(p1), "--skip-suite"],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", cwd=str(ROOT))
        verdict(r.returncode == 0, "fase 1 continua verde (regressão)",
                "" if r.returncode == 0 else "correr accept_phase1.py para o detalhe")
    else:
        verdict(False, "accept_phase1.py existe")

    p2 = HERE / "accept_phase2.py"
    scen = ROOT / "docs" / "runtime-hardening" / "intake-scenarios"
    if p2.is_file():
        pending("fase 2 (bloco B — intake e âmbito)",
                "o script existe mas NÃO é corrido aqui: a ordem acordada é 1 → 3 → 2, e um "
                "critério que não correu não é um critério aprovado. Correr "
                "`python docs/runtime-hardening/accept_phase2.py` quando a fase 2 fechar.")
    else:
        pending("fase 2 (bloco B — intake e âmbito)",
                "por implementar: não existe `accept_phase2.py` nem os cenários em "
                "`docs/runtime-hardening/intake-scenarios/`. Nada aqui a afirma, nem verde "
                "nem vermelho.")
    measure("cenários de intake registados",
            "{} de 3 (onboarding · manutenção · pricing)".format(
                len(list(scen.glob("*.md"))) if scen.is_dir() else 0))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--engagement", help="restringe a medição a um slug")
    ap.add_argument("--skip-suite", action="store_true")
    ap.add_argument("--only-phase3", action="store_true",
                    help="não corre a aceitação da fase 1")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    print("Aceitação — fase 3 (bloco C) · repo {} · engagements {}".format(ROOT, ENG_ROOT))
    print("Ordem acordada: fase 1 → fase 3 → fase 2 → quatro pilotos ponta-a-ponta.")
    criterion_a()
    criterion_b()
    criterion_c(args.engagement)
    criterion_d()
    criterion_e()
    criterion_f()
    criterion_g(args.engagement)
    if args.only_phase3:
        head("H", "Suite e fases vizinhas")
        pending("fase 1 e suite", "--only-phase3 pedido")
        pending("fase 2 (bloco B)", "por implementar; a ordem acordada é 1 → 3 → 2")
    else:
        criterion_h(args.skip_suite)

    print("\n" + "=" * 78)
    if PENDING:
        print("PENDENTE (declarado, nunca contado como aprovado):")
        for p in PENDING:
            print("  · " + p)
    if FAILED:
        print("FALHA — {} critério(s): {}".format(len(FAILED), "; ".join(FAILED)))
        return 1
    print("Fase 3: todos os critérios com veredicto passam.")
    print("As medições sobre engagements reais imprimem-se e não se aprovam (§11).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
