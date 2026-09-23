#!/usr/bin/env python3
"""PostToolUse(Write|Edit): o grafo acompanha o que se escreveu na SU.

Sessao real de Discovery: a segunda escrita de uma lente foi recusada pelo guarda de
autoridade. As lentes editam `shared-understanding.md` com a ferramenta Edit, e nada
espelhava essas linhas no grafo — `AUTHORITY_UNMIRRORED` bloqueava a escrita seguinte.

Este hook e o escritor que faltava para esse caminho: depois de cada escrita na SU de um
engagement com grafo, chama `resolve.sync_mirror`, que publica pelo coordenador.

Nunca bloqueia. Um PostToolUse nao desfaz a escrita que ja aconteceu, e sair com erro
aqui so esconderia a causa. Quando recusa — pendencia, grafo ilegivel — diz porque e qual
e a recuperacao, em stderr, e sai 0. O guarda de autoridade, na escrita seguinte, continua
a ser quem decide.

Corre ANTES de `on-su-change.py`: o dashboard le o kernel, e se corresse primeiro
mostraria «por reconstruir» sobre um estado que o espelho estava prestes a repor.
"""
import json
import os
import runpy
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RESOLVE = REPO_ROOT / "library" / "kernel" / "tools" / "resolve.py"
SU = "shared-understanding.md"


def engagements_root() -> Path:
    raw = os.environ.get("AISA_ENGAGEMENTS_ROOT")
    if raw:
        p = Path(raw)
        return p if p.is_absolute() else (REPO_ROOT / p)
    return REPO_ROOT / "projects"


def engagement_of(file_path: str):
    """O engagement cuja SU foi escrita — ou None. Caminho canonico, como o guarda."""
    try:
        alvo = Path(file_path).resolve()
        raiz = engagements_root().resolve()
    except OSError:
        return None
    if alvo.name != SU:
        return None
    try:
        rel = alvo.relative_to(raiz)
    except ValueError:
        return None
    if len(rel.parts) != 2:          # projects/<slug>/shared-understanding.md, e so isso
        return None
    return raiz / rel.parts[0]


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    raw = sys.stdin.read()
    try:
        tool = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return 0
    if tool.get("tool_name") not in {"Write", "Edit"}:
        return 0
    eng = engagement_of((tool.get("tool_input") or {}).get("file_path") or "")
    if eng is None or not (eng / "_state.json").is_file():
        return 0
    try:
        R = runpy.run_path(str(RESOLVE))
        r = R["sync_mirror"](eng)
    except Exception as exc:                                   # noqa: BLE001
        print("[on-su-mirror] o espelho de `{}` falhou ({}: {}). A proxima escrita na SU "
              "sera recusada pelo guarda; recuperar com: python library/kernel/tools/"
              "migrate.py apply --engagement {}".format(
                  eng.name, type(exc).__name__, exc, eng.name), file=sys.stderr)
        return 0
    if r.get("status") == "refused":
        print("[on-su-mirror] `{}`: espelho recusado — {} nao e deste escritor. "
              "Recuperar: {}".format(eng.name, ", ".join(r.get("blocking", [])),
                                     r.get("recovery", "")), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
