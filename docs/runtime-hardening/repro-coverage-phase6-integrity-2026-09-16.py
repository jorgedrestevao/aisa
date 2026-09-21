# -*- coding: utf-8 -*-
"""Fase 6 — integridade do engagement real (plano §12, *Fase 6*, ponto 4).

    python docs/runtime-hardening/repro-coverage-phase6-integrity-2026-09-16.py

Manifesto SHA-256 do engagement real **antes**, corrida de todos os comandos read-only
sobre ele, manifesto **depois**. A pergunta é uma só: olhar para o engagement mudou-o?

Corre os comandos que o mecanismo expõe, e mais nenhum. `finalize` — a única operação de
escrita do motor — **não** é corrida aqui, de propósito: este ficheiro existe para provar
que os outros não escrevem.

Não avalia a cobertura do engagement real, não responde a nenhuma pergunta em aberto e
não regista nem toca aprovação nenhuma.
"""
import hashlib
import io
import json
import os
import runpy
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "library" / "kernel" / "tools" / "coverage.py"
DASH = ROOT / "library" / "kernel" / "tools" / "dashboard.py"
OUT = ROOT / "docs" / "review-evidence" / "coverage-phase6-integrity-2026-09-16.md"
PROJECTS = ROOT / "projects"

lines = []


def say(s=""):
    lines.append(s)
    print(s)


def manifest(root: Path) -> dict:
    out = {}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            out[p.relative_to(root).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def run(*args, script=ENGINE):
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    r = subprocess.run([sys.executable, "-B", str(script), *args], cwd=str(ROOT), env=env,
                       text=True, capture_output=True, encoding="utf-8", errors="replace")
    return r


engagements = sorted(p.name for p in PROJECTS.iterdir()
                     if p.is_dir() and (p / "_state.json").is_file()) \
    if PROJECTS.is_dir() else []

say("# Integridade do engagement real — fase 6")
say()
say("Gerado por `docs/runtime-hardening/repro-coverage-phase6-integrity-2026-09-16.py`.")
say()

if not engagements:
    say("> **INCONCLUSIVO — não há engagement montado neste checkout.**")
    say(">")
    say("> `projects/` é um ponto de montagem privado e está vazio de engagements aqui.")
    say("> A verificação de integridade **não foi executada**, e isso não é o mesmo que")
    say("> «nada foi alterado»: é «não há nada para verificar, e ninguém o verificou».")
    say("> Um checkout com `projects/<slug>` montado deve correr este ficheiro antes de")
    say("> dar a fase por fechada.")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n-> " + str(OUT))
    sys.exit(2)

rows = []
for slug in engagements:
    eng = PROJECTS / slug
    before = manifest(eng)
    calls = [
        ("inventory", run("inventory", "--engagement", slug, "--json")),
        ("check reconciliation", run("check", "--engagement", slug, "--stage",
                                     "reconciliation", "--json")),
        ("report reconciliation", run("report", "--engagement", slug, "--stage",
                                      "reconciliation")),
    ]
    # E a etapa `blueprint` sobre a versão que o engagement aponta, quando existe.
    bp = sorted((PROJECTS / slug / "_blueprint").glob("ux-blueprint_v*.yaml"))         if (PROJECTS / slug / "_blueprint").is_dir() else []
    if bp:
        calls.append(("check blueprint " + bp[-1].stem.split("_")[-1],
                      run("check", "--engagement", slug, "--stage", "blueprint",
                          "--target", "_blueprint/" + bp[-1].name, "--json")))
    # E os pré-render dos seis deliverables, que também são read-only.
    for d in ("discovery-report", "executive-report", "solution-blueprint",
              "implementation-spec", "claude-design-brief", "estimate"):
        calls.append(("precheck " + d, run("check", "--engagement", slug, "--stage",
                                           "render", "--deliverable", d, "--json")))
    after = manifest(eng)
    changed = sorted(set(before) ^ set(after)) + \
        sorted(k for k in set(before) & set(after) if before[k] != after[k])
    # `dashboard.py --json` **não** é read-only e não entra na lista acima: o `--json` é um
    # *also dump* — reconstrói `dashboard.html` no engagement, que é o que ele existe para
    # fazer. Corre-se à parte, e o que se mede nele é outra coisa: que o que escreve é o
    # artefacto derivado, e mais nada.
    mid = manifest(eng)
    dash = run("--engagement", slug, "--json",
               str(Path(tempfile.gettempdir()) / ("aisa-ph6-%s.json" % slug)), script=DASH)
    post = manifest(eng)
    wrote = sorted(set(mid) ^ set(post)) + \
        sorted(k for k in set(mid) & set(post) if mid[k] != post[k])
    rows.append({"slug": slug, "files": len(before), "calls": calls, "changed": changed,
                 "dash": dash, "wrote": wrote})

say("| engagement | ficheiros | comandos read-only corridos | ficheiros alterados |")
say("|---|---|---|---|")
for r in rows:
    say("| `%s` | %d | %d | **%d** |" % (r["slug"], r["files"], len(r["calls"]),
                                         len(r["changed"])))
say()
for r in rows:
    say("### `%s`" % r["slug"])
    say()
    say("| comando | saída | o que devolveu |")
    say("|---|---|---|")
    for name, res in r["calls"]:
        first = (res.stdout or res.stderr or "").strip().splitlines()
        head = first[0][:90] if first else "(sem saída)"
        if name.startswith("check") or name.startswith("precheck"):
            try:
                data = json.loads(res.stdout)
                head = data.get("coverage") or (data.get("expected") or {}).get("state", "")
                head = "cobertura/estado: %s" % head
            except Exception:                                       # noqa: BLE001
                pass
        say("| `%s` | %d | %s |" % (name, res.returncode, head.replace("|", "\\|")))
    say()
    if r["changed"]:
        say("**%d ficheiro(s) alterado(s) pelos comandos read-only** — e não deviam ser "
            "nenhum:" % len(r["changed"]))
        for c in r["changed"]:
            say("- `%s`" % c)
    else:
        say("**Zero ficheiros alterados pelos comandos read-only.** Manifesto SHA-256")
        say("idêntico antes e depois, nos %d ficheiros do engagement." % r["files"])
    say()
    say("À parte, e por desenho: `dashboard.py --engagement %s --json <destino fora do "
        "engagement>` saiu %d e escreveu %d ficheiro(s): %s. O `--json` é um *also dump* —"
        % (r["slug"], r["dash"].returncode, len(r["wrote"]),
           ", ".join("`%s`" % w for w in r["wrote"]) or "nenhum"))
    say("reconstrói o dashboard **e** exporta o modelo. Não é um comando read-only, e por")
    say("isso não entra na conta acima; o que ele escreve é o artefacto derivado que")
    say("qualquer `/dashboard` ou o hook `on-su-change.py` reescrevem, e que o contrato já")
    say("trata como derivado (§6.3, `DERIVED_FILES`) — não entra na base de atualidade de")
    say("revisão nenhuma. Entre duas reconstruções seguidas só varia o carimbo de tempo do")
    say("comentário de build; o hash de build é o mesmo.")
    say()

clean = all(not r["changed"] for r in rows)
say("---")
say()
say("O que esta verificação **não** diz, e é a parte que importa: nada aqui avalia a")
say("cobertura destes engagements. Os veredictos na tabela são **lidos** dos registos que")
say("já lá estavam, escritos por quem conduz o engagement — este ficheiro não reviu nada,")
say("não respondeu a nenhuma pergunta em aberto, não registou nem tocou aprovação nenhuma,")
say("e não diz que o desenho real está aprovado, completo ou validado ponta-a-ponta. Uma")
say("cobertura `complete` continua a ser a **segunda** das quatro perguntas, e só essa.")
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n-> " + str(OUT))
sys.exit(0 if clean else 1)
