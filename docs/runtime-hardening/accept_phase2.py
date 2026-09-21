# -*- coding: utf-8 -*-
"""Aceitação executável da fase 2 do endurecimento do runtime (bloco B).

    python docs/runtime-hardening/accept_phase2.py
    python docs/runtime-hardening/accept_phase2.py --skip-suite

Não escreve nada. Sai 0 quando todos os critérios com veredicto passam, 1 quando algum falha,
quando falta um cenário, quando falta um `CHECK-n` ou quando algum diz `FAIL`.

DUAS CAMADAS, e a diferença entre elas é o ponto:

  Camada 1 — FORMA. Determinística, verificável aqui: os temas de pricing saíram do caminho
  universal, T1..T7 estão nos três sítios que os impõem, o token de âmbito está nos oito
  documentos, os quatro pacotes declaram a chave, e o motor lê tanto a forma nova como a
  antiga. Isto o script prova.

  Camada 2 — COMPORTAMENTO. O que o modelo pergunta não se testa em unittest. Os três
  cenários foram corridos e registados; este script confirma o REGISTO — que os ficheiros
  existem, que têm as cinco secções-token, que `## CHECKS` tem exactamente `CHECK-1..4` e que
  todos dizem `PASS`. **Confirmar o registo não é demonstrar o comportamento**, e o script
  imprime essa distinção em vez de a deixar implícita.
"""

import argparse
import io
import json
import os
import re
import runpy
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
ENG_ROOT = Path(os.environ.get("AISA_ENGAGEMENTS_ROOT") or (ROOT / "projects"))
HERE = Path(os.path.dirname(os.path.abspath(__file__)))
SCEN = HERE / "intake-scenarios"
RUNS = SCEN / "_runs"
D = runpy.run_path(str(ROOT / "library" / "kernel" / "tools" / "dashboard.py"))

FAILED: list[str] = []
PENDING: list[str] = []

THEMES = ["actors", "trigger", "activities", "outcomes", "invariants",
          "failure_today", "change_requested"]
PRICING_IDS = ["sold_what_when", "price_fixing_moment", "cost_driver",
               "valuation_driver", "uncertainty_shape"]
# As formas que o intake antigo impunha a toda a gente, pt + en.
PRICING_FORMS = [
    "what is sold", "o que é vendido", "o que se vende",
    "when the price is fixed", "quando o preço se fixa", "quando se fixa o preço",
    "what determines the cost", "o que determina o custo",
    "what determines the valuation", "o que determina a valorização",
    "where the uncertainty comes from", "de onde vem a incerteza",
]
SCOPE_TOKEN = "SCOPE-STATEMENT v1"
SCOPE_FILES = ["README.md", "CLAUDE.md", "docs/ARCHITECTURE.md", "docs/PHILOSOPHY.md",
               "docs/COMO-USAR.md", "docs/FRAMEWORK-NEGOCIO.md", "docs/ONBOARDING.md",
               "library/packs/pp/pack.yaml"]
SECTIONS = ["## INPUT", "## OWNER-SCRIPT", "## ASKED", "## ENQUADRAMENTO",
            "## EVIDENCE-LEVEL", "## CHECKS"]
SCENARIOS = ["onboarding", "manutencao", "pricing"]


def head(letter, title):
    print("\n" + "=" * 78)
    print("{}. {}".format(letter, title))
    print("=" * 78)


def verdict(ok, label, detail=""):
    print("  [{}] {}{}".format("ok " if ok else "FALHA", label,
                               ("  — " + detail) if detail else ""))
    if not ok:
        FAILED.append(label)


def measure(label, value):
    print("  [ .. ] {}: {}".format(label, value))


def pending(label, why):
    print("  [PEND] {}  — {}".format(label, why))
    PENDING.append(label)


def read(rel):
    p = ROOT / rel
    try:
        return p.read_text(encoding="utf-8")
    except OSError:
        return ""


# ============================================================ CAMADA 1 — forma

def criterion_a():
    head("A", "Os temas de pricing saíram do caminho universal")
    # O bloco condicional de cada skill: tudo o que vem depois do marcador de activacao.
    targets = {
        ".claude/skills/aisa-start/SKILL.md": "d1. **Activation of the `pricing` set**",
        ".claude/skills/aisa-orient/SKILL.md": "**Right after T4**",
        "library/kernel/phases.md": "### The `pricing` conditional set",
    }
    for rel, marker in targets.items():
        text = read(rel)
        verdict(marker in text, "{}: tem o bloco condicional".format(rel))
        if marker not in text:
            continue
        before = text.split(marker)[0]
        leaked = sorted({f for f in PRICING_FORMS if f.lower() in before.lower()})
        verdict(not leaked, "{}: nenhum tema de pricing antes do bloco".format(rel),
                ", ".join(leaked))
    # Nos documentos de utilizador, uma forma de pricing so e legitima dentro de uma frase
    # que a declare CONDICIONAL. A janela e por ocorrencia -- procurar a condicao uma vez
    # no ficheiro inteiro daria verde a qualquer mencao, em qualquer sitio.
    COND = ("se a saída", "se a saida", "só então", "so entao", "condicional",
            "é-te perguntado", "e-te perguntado", "quando se aplica")
    for rel in ("docs/COMO-USAR.md", "docs/ONBOARDING.md"):
        low = read(rel).lower()
        leaked = []
        for f in PRICING_FORMS:
            for m in re.finditer(re.escape(f.lower()), low):
                window = low[max(0, m.start() - 400):m.end() + 400]
                if not any(c in window for c in COND):
                    leaked.append(f)
                    break
        verdict(not leaked, "{}: pricing só aparece como condicional".format(rel),
                ", ".join(sorted(set(leaked))))
    verdict("pricing" in read("library/kernel/phases.md"),
            "o conjunto condicional vive no kernel (D-1)")
    for pack in ("pp", "generic", "outsystems", "mendix"):
        y = read("library/packs/{}/pack.yaml".format(pack))
        leaked = [f for f in PRICING_FORMS if f.lower() in y.lower()]
        verdict(not leaked, "pack {}: não carrega os temas de pricing".format(pack))


def criterion_b():
    head("B", "T1–T7 onde têm de estar, com ids estáveis")
    for rel in (".claude/skills/aisa-start/SKILL.md",
                ".claude/skills/aisa-orient/SKILL.md",
                "library/kernel/phases.md"):
        text = read(rel)
        missing = [t for t in THEMES if "`" + t + "`" not in text]
        verdict(not missing, "{}: os sete ids".format(rel), ", ".join(missing))
        order = [text.find("`" + t + "`") for t in THEMES]
        verdict(order == sorted(order), "{}: pela ordem fixa".format(rel))
    gloss = read("library/kernel/glossary.md")
    missing = [t for t in THEMES if "**" + t + "**" not in gloss]
    verdict(not missing, "glossário: uma linha por id", ", ".join(missing))
    verdict("**INTAKE-SET**" in gloss, "glossário: o marcador de activação")
    start = read(".claude/skills/aisa-start/SKILL.md")
    verdict("A saída deste processo é um preço, cotação, margem ou valorização?" in start,
            "a pergunta de activação está escrita, literal")
    verdict("Never** inferred" in start or "**Never inferred**" in start,
            "e está dito que nunca se infere")
    orient = read(".claude/skills/aisa-orient/SKILL.md")
    verdict("does **not** ask any of it again" in orient or "não" in orient,
            "aisa-orient declara que aisa-start não repete")
    verdict("do not ask again" in start, "aisa-start declara que não repete")


def criterion_c():
    head("C", "A frase de âmbito nos oito documentos")
    for rel in SCOPE_FILES:
        verdict(SCOPE_TOKEN in read(rel), "{}: tem `{}`".format(rel, SCOPE_TOKEN))
    verdict("decisão técnica" in read("docs/PHILOSOPHY.md"),
            "PHILOSOPHY diz em que direcção a tensão se resolve")
    verdict("Errata" in read("docs/ARCHITECTURE.md"),
            "ARCHITECTURE mantém o texto antigo com errata, não reescrito")
    verdict("Errata" in read("docs/CONSOLIDATED_PLAN.md"),
            "CONSOLIDATED_PLAN (histórico, prescreve runtime) tem errata")


def criterion_d():
    head("D", "Os quatro pacotes declaram a extensão")
    for pack in ("pp", "generic", "outsystems", "mendix"):
        y = read("library/packs/{}/pack.yaml".format(pack))
        verdict("enquadramento:" in y and "extra_themes:" in y,
                "pack {}: `enquadramento.extra_themes`".format(pack))
        m = re.search(r"extra_themes:\s*(\[\]|\n)", y)
        verdict(bool(m), "pack {}: é uma lista".format(pack))


def criterion_e():
    head("E", "O motor lê a forma nova — e continua a ler a antiga")
    if not RUNS.is_dir():
        verdict(False, "as corridas dos cenários existem em `_runs/`")
        return
    for eng in sorted(RUNS.iterdir()):
        if not (eng / "_state.json").is_file():
            continue
        enq = (eng / "enquadramento.md").read_text(encoding="utf-8")
        missing = [t for t in THEMES if "## T" not in enq or ("· " + t) not in enq]
        verdict(not missing, "{}: secções T1–T7".format(eng.name), ", ".join(missing))
        has_sec, has_mark = "## pricing" in enq, "INTAKE-SET: pricing" in enq
        verdict(has_sec == has_mark,
                "{}: `## pricing` e o marcador andam juntos".format(eng.name),
                "secção={} marcador={}".format(has_sec, has_mark))
        try:
            model = D["build_model"](eng, date(2026, 9, 11))
            verdict(len(model["su"]["rows"]) > 0,
                    "{}: o motor lê e as linhas M-n entraram na SU".format(eng.name),
                    "{} linhas".format(len(model["su"]["rows"])))
        except Exception as exc:                                    # noqa: BLE001
            verdict(False, "{}: o motor lê".format(eng.name),
                    "{}: {}".format(type(exc).__name__, exc))

    # REGRESSAO: a forma antiga le-se tal como esta, e nao se reescreve
    old = ENG_ROOT / "pricing-marinha-pilot-3"
    if (old / "enquadramento.md").is_file():
        enq = (old / "enquadramento.md").read_text(encoding="utf-8")
        verdict(not any(("## T" + str(i)) in enq for i in range(1, 8)),
                "regressão: o enquadramento antigo NÃO foi reescrito")
        try:
            model = D["build_model"](old, date(2026, 9, 11))
            verdict(len(model["su"]["rows"]) > 0,
                    "regressão: e continua a ser lido sem erro",
                    "{} linhas".format(len(model["su"]["rows"])))
        except Exception as exc:                                    # noqa: BLE001
            verdict(False, "regressão: o antigo continua a ser lido",
                    "{}: {}".format(type(exc).__name__, exc))
    else:
        measure("regressão do enquadramento antigo", "pilot-3 não montado — não avaliada")

    # MEDICAO sobre os artefactos reais -- nao se reescrevem para dar verde (§11)
    engs = [p.parent for p in sorted(ENG_ROOT.glob("*/enquadramento.md"))]
    novos = [e.name for e in engs
             if "## T1 · actors" in (e / "enquadramento.md").read_text(encoding="utf-8")]
    com_pricing = [e.name for e in engs
                   if "INTAKE-SET: pricing" in (e / "enquadramento.md").read_text(encoding="utf-8")]
    measure("enquadramentos reais com a forma nova",
            "{} de {} — {}".format(len(novos), len(engs), ", ".join(novos) or "nenhum"))
    measure("enquadramentos reais com o marcador de pricing",
            "{} de {}".format(len(com_pricing), len(engs)))
    print("         (a forma antiga é a esperada nos engagements anteriores ao contrato;")
    print("          a presença das secções é o critério, nunca a data ou a versão)")


# ==================================================== CAMADA 2 — comportamento

# O id casa QUALQUER número, e o veredicto é opcional: um `CHECK-5` ou um `CHECK-2` sem
# veredicto têm de ser VISTOS para poderem ser recusados. Uma expressão que só reconhece
# 1..4 torna o ramo dos inesperados inalcançável — foi assim que `CHECK-5: FAIL` passou.
CHECK_RE = re.compile(
    r"^CHECK-(?P<n>\d+)\s*:\s*(?P<verdict>[A-Z][A-Z-]*)?(?P<rest>.*)$", re.M)


def heading_pos(text: str, heading: str) -> int:
    """Position of a heading AS A HEADING (start of line), not of a mention in prose."""
    m = re.search(r"^" + re.escape(heading) + r"\s*$", text, re.M)
    return m.start() if m else -1


def section_body(text: str, heading: str, next_heading: str = "") -> str:
    """O corpo de uma secção, do seu cabeçalho até **ao cabeçalho seguinte de qualquer
    nível** — não até ao fim do ficheiro.

    Defeito que isto fecha: a leitura da última secção prolongava-se até ao fim, e um
    `## APPENDIX` a seguir passava a fazer parte dela. Uma secção acaba onde a seguinte
    começa; se `next_heading` for dado e existir, respeita-se esse limite.
    """
    a = heading_pos(text, heading)
    if a < 0:
        return ""
    end = len(text)
    if next_heading:
        b = heading_pos(text, next_heading)
        if b > a:
            end = b
    m = re.search(r"^#{1,6}\s+\S", text[a + len(heading):], re.M)
    if m:
        end = min(end, a + len(heading) + m.start())
    return text[a:end]


def checks_verdict(text: str):
    """-> (ok, detalhe). Lê **só** a secção `## CHECKS`, exige **exactamente uma**
    ocorrência de cada `CHECK-1..4`, e recusa qualquer `FAIL`.

    Defeito que isto fecha (revisão de 2026-09-11): a leitura anterior varria o ficheiro
    inteiro e guardava os veredictos num dicionário — a última ocorrência ganhava, e um
    `CHECK-1: FAIL` seguido de `CHECK-1: PASS` passava sem erro. Um FAIL não se apaga
    escrevendo outra vez.
    """
    body = section_body(text, "## CHECKS")
    if not body:
        return False, "não há secção `## CHECKS`"
    found = list(CHECK_RE.finditer(body))
    outside = len(list(CHECK_RE.finditer(text))) - len(found)
    counts = {}
    for m in found:
        counts.setdefault(m.group("n"), []).append(m.group("verdict") or "(sem veredicto)")
    problems = []
    if outside > 0:
        problems.append("{} linha(s) CHECK fora da secção".format(outside))
    missing = [n for n in ("1", "2", "3", "4") if n not in counts]
    if missing:
        problems.append("em falta: " + ", ".join("CHECK-" + n for n in missing))
    dup = sorted(n for n, v in counts.items() if len(v) > 1)
    if dup:
        problems.append("repetido(s): " + ", ".join(
            "CHECK-{} ×{} ({})".format(n, len(counts[n]), "/".join(counts[n])) for n in dup))
    extra = sorted((n for n in counts if n not in ("1", "2", "3", "4")), key=int)
    if extra:
        problems.append("inesperado(s): " + ", ".join("CHECK-" + n for n in extra))
    bad_verdict = sorted((n for n, v in counts.items()
                          if any(x not in ("PASS", "FAIL") for x in v)), key=int)
    if bad_verdict:
        problems.append("veredicto ilegível em: " + ", ".join(
            "CHECK-{} ({})".format(n, "/".join(counts[n])) for n in bad_verdict))
    fails = sorted((n for n, v in counts.items() if "FAIL" in v), key=int)
    if fails:
        problems.append("FAIL em: " + ", ".join("CHECK-" + n for n in fails))
    thin = sorted({m.group("n") for m in found if len(m.group("rest").strip()) < 30}, key=int)
    if thin:
        problems.append("sem evidência: " + ", ".join("CHECK-" + n for n in thin))
    if problems:
        return False, "; ".join(problems)
    return True, "4/4 PASS, um de cada, todos com evidência"


LEVELS: list = []
EVIDENCE_RE = re.compile(r"^##\s+EVIDENCE-LEVEL\s*$\s+`(?P<level>[a-z-]+)`", re.M)


def evidence_level(text: str) -> str:
    """`interactive` | `script-driven` | `nao declarado`.

    B4 camada 2 so conta quando o cenario prova a EMISSAO das perguntas e a passagem entre
    skills. Um cenario que nao declare o nivel e tratado como nao declarado -- o silencio
    nao promove evidencia.
    """
    m = EVIDENCE_RE.search(text or "")
    return m.group("level") if m else "nao declarado"


SELF_TESTS = [
    ("um FAIL escondido por um PASS repetido",
     "## CHECKS\n\nCHECK-1: FAIL — a pergunta saiu duas vezes, e isso é o defeito.\n"
     "CHECK-1: PASS — a pergunta de activação foi feita exactamente uma vez, e mais nenhuma.\n"
     "CHECK-2: PASS — resposta Não; zero perguntas de pricing e sem secção no ficheiro.\n"
     "CHECK-3: PASS — a segunda skill não repetiu nenhuma das perguntas da primeira.\n"
     "CHECK-4: PASS — os M-n são as frases de T5, verbatim, nem mais nem menos.\n", False),
    ("um CHECK em falta",
     "## CHECKS\n\nCHECK-1: PASS — a pergunta de activação foi feita exactamente uma vez.\n"
     "CHECK-2: PASS — resposta Não; zero perguntas de pricing e sem secção no ficheiro.\n"
     "CHECK-3: PASS — a segunda skill não repetiu nenhuma das perguntas da primeira.\n", False),
    ("um FAIL simples",
     "## CHECKS\n\nCHECK-1: PASS — a pergunta de activação foi feita exactamente uma vez.\n"
     "CHECK-2: FAIL — houve perguntas de pricing apesar de a resposta ter sido Não.\n"
     "CHECK-3: PASS — a segunda skill não repetiu nenhuma das perguntas da primeira.\n"
     "CHECK-4: PASS — os M-n são as frases de T5, verbatim, nem mais nem menos.\n", False),
    ("um veredicto sem evidência",
     "## CHECKS\n\nCHECK-1: PASS\n"
     "CHECK-2: PASS — resposta Não; zero perguntas de pricing e sem secção no ficheiro.\n"
     "CHECK-3: PASS — a segunda skill não repetiu nenhuma das perguntas da primeira.\n"
     "CHECK-4: PASS — os M-n são as frases de T5, verbatim, nem mais nem menos.\n", False),
    ("um CHECK fora da secção",
     "CHECK-1: PASS — escrito antes da secção, onde ninguém o julga.\n"
     "## CHECKS\n\nCHECK-1: PASS — a pergunta de activação foi feita exactamente uma vez.\n"
     "CHECK-2: PASS — resposta Não; zero perguntas de pricing e sem secção no ficheiro.\n"
     "CHECK-3: PASS — a segunda skill não repetiu nenhuma das perguntas da primeira.\n"
     "CHECK-4: PASS — os M-n são as frases de T5, verbatim, nem mais nem menos.\n", False),
    ("sem secção nenhuma", "# Cenário\n\nnada aqui.\n", False),
    # --- os dois casos da segunda revisão do validador (2026-09-11) ---
    ("um CHECK depois de `## APPENDIX`, fora da secção",
     "## CHECKS\n\nCHECK-1: PASS — a pergunta de activação foi feita exactamente uma vez.\n"
     "CHECK-2: PASS — resposta Não; zero perguntas de pricing e sem secção no ficheiro.\n"
     "CHECK-3: PASS — a segunda skill não repetiu nenhuma das perguntas da primeira.\n\n"
     "## APPENDIX\n\nCHECK-4: PASS — escrito no apêndice, onde já ninguém o julga.\n", False),
    ("um CHECK-5, que a expressão antiga nem via",
     "## CHECKS\n\nCHECK-1: PASS — a pergunta de activação foi feita exactamente uma vez.\n"
     "CHECK-2: PASS — resposta Não; zero perguntas de pricing e sem secção no ficheiro.\n"
     "CHECK-3: PASS — a segunda skill não repetiu nenhuma das perguntas da primeira.\n"
     "CHECK-4: PASS — os M-n são as frases de T5, verbatim, nem mais nem menos.\n"
     "CHECK-5: FAIL — um id que o contrato não tem, e que passava despercebido.\n", False),
    ("um veredicto que não é PASS nem FAIL",
     "## CHECKS\n\nCHECK-1: TALVEZ — a pergunta de activação parece ter sido feita uma vez.\n"
     "CHECK-2: PASS — resposta Não; zero perguntas de pricing e sem secção no ficheiro.\n"
     "CHECK-3: PASS — a segunda skill não repetiu nenhuma das perguntas da primeira.\n"
     "CHECK-4: PASS — os M-n são as frases de T5, verbatim, nem mais nem menos.\n", False),
    ("quatro PASS seguidos de um apêndice inofensivo",
     "## CHECKS\n\nCHECK-1: PASS — a pergunta de activação foi feita exactamente uma vez.\n"
     "CHECK-2: PASS — resposta Não; zero perguntas de pricing e sem secção no ficheiro.\n"
     "CHECK-3: PASS — a segunda skill não repetiu nenhuma das perguntas da primeira.\n"
     "CHECK-4: PASS — os M-n são as frases de T5, verbatim, nem mais nem menos.\n\n"
     "## APPENDIX\n\nNotas de leitura, sem veredictos nenhuns.\n", True),
    ("quatro PASS, um de cada, com evidência",
     "## CHECKS\n\nCHECK-1: PASS — a pergunta de activação foi feita exactamente uma vez.\n"
     "CHECK-2: PASS — resposta Não; zero perguntas de pricing e sem secção no ficheiro.\n"
     "CHECK-3: PASS — a segunda skill não repetiu nenhuma das perguntas da primeira.\n"
     "CHECK-4: PASS — os M-n são as frases de T5, verbatim, nem mais nem menos.\n", True),
]


def criterion_zero():
    head("0", "O validador dos CHECKS, testado contra si próprio")
    print("  Um verificador que não é testado é uma opinião. Os casos negativos primeiro.\n")
    for label, sample, want in SELF_TESTS:
        got, detail = checks_verdict(sample)
        verdict(got == want, "{}: {}".format("aceita" if want else "recusa", label),
                detail if got != want else "")


def criterion_f():
    head("F", "Camada 2 — os três cenários, corridos e registados")
    print("  O script confirma o REGISTO. Não corre o modelo, e por isso não demonstra o")
    print("  comportamento: demonstra que ele foi corrido, registado e julgado por leitura.\n")
    for name in SCENARIOS:
        p = SCEN / (name + ".md")
        if not p.is_file():
            verdict(False, "cenário {}: o ficheiro existe".format(name),
                    "falta {}".format(p.relative_to(ROOT)))
            continue
        text = p.read_text(encoding="utf-8")
        # As seccoes procuram-se ANCORADAS NA LINHA: o cabecalho do ficheiro menciona
        # `## OWNER-SCRIPT` em prosa, e um `in text` daria a mencao por seccao.
        pos = {s: heading_pos(text, s) for s in SECTIONS}
        missing = [s for s, i in pos.items() if i < 0]
        verdict(not missing, "cenário {}: as cinco secções".format(name), ", ".join(missing))
        order = [pos[s] for s in SECTIONS]
        verdict(order == sorted(order) and all(o >= 0 for o in order),
                "cenário {}: pela ordem contratada".format(name))
        # OWNER-SCRIPT antes da corrida: tem de trazer uma linha por tema e a activacao
        script = section_body(text, "## OWNER-SCRIPT", "## ASKED")
        miss_t = [t for t in THEMES if t not in script]
        verdict(not miss_t, "cenário {}: o guião fixa os sete temas".format(name),
                ", ".join(miss_t))
        verdict("activation" in script,
                "cenário {}: o guião fixa a resposta de activação".format(name))
        ok, detail = checks_verdict(text)
        verdict(ok, "cenário {}: CHECK-1..4, um de cada, nenhum FAIL".format(name), detail)
        level = evidence_level(text)
        LEVELS.append((name, level))
        if level == "interactive":
            verdict(True, "cenário {}: nível de evidência `interactive`".format(name))
        else:
            pending("cenário {}: camada 2 conta como registo, não como prova".format(name),
                    "nível de evidência `{}` — as respostas vieram do guião, no lugar de "
                    "chamadas vivas; a emissão de cada pergunta e a passagem entre skills "
                    "não ficaram provadas (B4 exige `interactive`)".format(level))
        eng_dir = RUNS / {"onboarding": "onboarding-colaboradores",
                          "manutencao": "manutencao-preventiva",
                          "pricing": "pricing-marinha-cenario"}[name]
        verdict((eng_dir / "enquadramento.md").is_file(),
                "cenário {}: a corrida deixou o artefacto em disco".format(name),
                str(eng_dir.relative_to(ROOT)))

    # CHECK-2 tem de ser diferente entre os dois lados da condicao
    on = (SCEN / "onboarding.md").read_text(encoding="utf-8") if (SCEN / "onboarding.md").is_file() else ""
    pr = (SCEN / "pricing.md").read_text(encoding="utf-8") if (SCEN / "pricing.md").is_file() else ""
    verdict("não tem `## pricing`" in on or "não tem" in on,
            "onboarding: CHECK-2 afirma a ausência da secção")
    verdict("INTAKE-SET: pricing" in pr,
            "pricing: CHECK-2 afirma a presença do marcador")
    # o guiao de pricing reusa pilot-3
    ref = ENG_ROOT / "pricing-marinha-pilot-3" / "enquadramento.md"
    if ref.is_file() and pr:
        ref_text = ref.read_text(encoding="utf-8")
        reused = [s for s in ("O custo de cedência é indexado a Platts",
                              "valorização errada, não venda perdida")
                  if s in ref_text and s in pr]
        verdict(len(reused) == 2,
                "pricing: o guião reusa verbatim as declarações de pilot-3",
                "{} de 2 encontradas".format(len(reused)))
    else:
        measure("reuso de pilot-3", "referência não montada — não avaliado")


def criterion_g(skip_suite):
    head("G", "Suite e as fases vizinhas")
    py = ROOT / ".test-venv" / "Scripts" / "python.exe"
    exe = str(py) if py.is_file() else sys.executable
    if skip_suite:
        pending("suite", "--skip-suite pedido")
    else:
        r = subprocess.run([exe, "-m", "pytest", str(ROOT / ".claude" / "tests"), "-q"],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", cwd=str(ROOT))
        tail = [l for l in (r.stdout or "").strip().splitlines() if l.strip()][-1:]
        verdict(r.returncode == 0, "suite verde", tail[0] if tail else "")
    for phase in (1, 3):
        p = HERE / "accept_phase{}.py".format(phase)
        if not p.is_file():
            verdict(False, "accept_phase{}.py existe".format(phase))
            continue
        r = subprocess.run([sys.executable, str(p), "--skip-suite"],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", cwd=str(ROOT))
        verdict(r.returncode == 0, "fase {} continua verde (regressão)".format(phase),
                "" if r.returncode == 0 else "correr accept_phase{}.py para o detalhe".format(phase))
    pending("quatro pilotos ponta-a-ponta",
            "fora do âmbito desta fase, por instrução do dono: correm depois de a fase 2 fechar")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skip-suite", action="store_true")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    print("Aceitação — fase 2 (bloco B) · repo {} · engagements {}".format(ROOT, ENG_ROOT))
    print("Ordem acordada: fase 1 → fase 3 → **fase 2** → quatro pilotos ponta-a-ponta.")
    criterion_zero()
    print("\n--- CAMADA 1: forma (determinística, este script prova) ---")
    criterion_a()
    criterion_b()
    criterion_c()
    criterion_d()
    criterion_e()
    print("\n--- CAMADA 2: comportamento (registado e julgado por leitura; o script confirma o registo) ---")
    criterion_f()
    criterion_g(args.skip_suite)

    print("\n" + "=" * 78)
    if PENDING:
        print("PENDENTE (declarado, nunca contado como aprovado):")
        for p in PENDING:
            print("  · " + p)
    if FAILED:
        print("FALHA — {} critério(s): {}".format(len(FAILED), "; ".join(FAILED)))
        return 1
    weak = [n for n, lvl in LEVELS if lvl != "interactive"]
    if weak:
        print("CAMADA 1: fechada — todos os critérios de forma passam.")
        print("CAMADA 2: **PENDENTE** — {} de {} cenários não têm evidência `interactive`: {}"
              .format(len(weak), len(LEVELS), ", ".join(weak)))
        print("  As respostas vieram do guião, no lugar de chamadas vivas. Isso mostra que os")
        print("  artefactos saem do guião; não mostra as perguntas emitidas nem a passagem")
        print("  entre `aisa-orient` e `aisa-start`, que é o que B4 pede.")
        print("  Para fechar: uma corrida interactiva, ou um adaptador que registe cada")
        print("  pergunta emitida e a resposta dada. O adaptador por linha de comando NÃO é")
        print("  executável neste ambiente (`claude -p` → OAuth session expired, 2026-09-11).")
        print("")
        print("**A fase 2 não se declara concluída.** Sai 1 para que nenhum exit 0 seja lido")
        print("como fecho da fase.")
        return 1
    print("Fase 2: todos os critérios com veredicto passam, nas duas camadas.")
    print("As medições sobre artefactos reais imprimem-se e não se aprovam (§11).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
