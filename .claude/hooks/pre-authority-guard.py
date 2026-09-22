"""pre-authority-guard.py — PreToolUse guard for Write/Edit on engagement authorities.

W2 of P7.5. Refuses to let the agent write to an engagement's authoritative files while
that engagement's bootstrap is NOT ready — a pending operation, an unreadable graph, an
incoherent pair. The refusal names the limitation and the recovery.

WHY A HOOK AND NOT A STEP IN EACH SKILL

The obvious shape would be a "run the bootstrap first" step in each of the fourteen
`SKILL.md` files. It fails on both counts W2 asks for:

  - `ACCEPTANCE.md` §1: «Um teste de estrutura de prompts é insuficiente para provar
    comportamento de runtime.» A test could only assert the sentence is in the file.
  - W2 itself asks to prove «que nenhum entrypoint contorna o bootstrap por uma chamada
    indirecta». Prose does not prevent a bypass; it asks for one not to happen.

So the enforcement is programmatic, the same way `library/` read-only already is.

WHAT IT COVERS, AND WHAT IT DOES NOT

Covers the AGENT's writes through `Write`/`Edit` — which is exactly the path that bypasses
the kernel today, since none of the 24 skills invokes `bootstrap.py`.

Does NOT cover writes by subprocess: a documented limitation of the hook surface
(`on-su-change.py` says the same about `PostToolUse`). The motors that write by subprocess
— `resolve`, `migrate` — already go through the coordinator, which refuses to mutate over a
pending operation. The two layers do not replace each other: this guard catches the agent,
the coordinator catches the motors.

FAILS CLOSED, LIKE ITS NEIGHBOUR

If the bootstrap cannot be evaluated at all, the write is refused rather than waved
through: not being able to verify is not the same as having verified.
`AISA_GUARD_MODE=log` is the explicit administrative override, the same switch
`pre-write-guard.py` honours.

Standalone use (no stdin):
    python .claude/hooks/pre-authority-guard.py --engagement <slug>
"""

from __future__ import annotations

import json
import os
import runpy
import sys
from pathlib import Path

# <repo>/.claude/hooks/pre-authority-guard.py -> <repo>
REPO_ROOT = Path(__file__).resolve().parents[2]
BOOTSTRAP = REPO_ROOT / "library" / "kernel" / "tools" / "bootstrap.py"

# As autoridades do engagement. Escrever numa destas muda o que o aisa SABE — e por isso
# exige que o estado tenha sido reconstruído primeiro. `_capture/`, `_render/`,
# `_simulation/` e companhia são derivados: ficam de fora de propósito.
AUTORIDADES = {"shared-understanding.md", "decisions.md", "answers.md", "_state.json"}


def engagements_root() -> Path:
    raw = os.environ.get("AISA_ENGAGEMENTS_ROOT")
    if raw:
        p = Path(raw)
        return p if p.is_absolute() else (REPO_ROOT / p)
    return REPO_ROOT / "projects"


def block(reason: str) -> None:
    payload = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }
    print(json.dumps(payload), file=sys.stderr)
    sys.exit(2)


def engagement_of(file_path: str) -> tuple[Path | None, str]:
    """`(engagement, nome do ficheiro)` quando o alvo é uma autoridade; `(None, "")` se não.

    A comparação é sobre o caminho canónico: `./projects/x/../x/decisions.md` é a mesma
    autoridade que `projects/x/decisions.md`, e um guarda que só olhasse à string deixava
    passar a primeira."""
    try:
        alvo = Path(file_path)
    except (OSError, ValueError):
        return None, ""
    if alvo.name not in AUTORIDADES:
        return None, ""

    base = engagements_root()
    try:
        base_real = base.resolve()
    except OSError:
        base_real = base
    for cand in {alvo, }:
        try:
            cand_real = cand.resolve()
        except OSError:
            # `resolve()` falhou: o caminho canonico tem de sair de outra forma, ou um
            # `projects/eng/x/../decisions.md` escapava por nao bater com a base.
            cand_real = Path(os.path.abspath(os.path.normpath(str(cand))))
        try:
            rel = cand_real.relative_to(base_real)
        except ValueError:
            continue
        if len(rel.parts) < 2:
            continue                      # um ficheiro solto na raiz não é engagement
        return base_real / rel.parts[0], alvo.name
    return None, ""


def avalia(eng: Path) -> tuple[bool, str]:
    """`(pronto, razão)`. Um bootstrap que não se consegue avaliar NÃO conta como pronto."""
    if not (eng / "_state.json").is_file():
        # Ainda não é um engagement: é `/start` a criá-lo. Não há estado a reconstruir.
        return True, ""
    try:
        B = runpy.run_path(str(BOOTSTRAP))
        boot = B["bootstrap"](eng)
    except Exception as exc:                                  # noqa: BLE001 — fail closed
        return False, "o bootstrap de `{}` não pôde ser avaliado ({}: {}) — não é o mesmo " \
                      "que ter sido avaliado".format(eng.name, type(exc).__name__, exc)
    if boot.get("ready"):
        return True, ""

    limitacoes = boot.get("limitations") or []
    partes = []
    for lim in limitacoes:
        detalhe = lim.get("detail") or lim.get("code", "")
        recup = lim.get("recovery") or ""
        partes.append("{}{}".format(detalhe, " → " + recup if recup else ""))
    return False, "o engagement `{}` não está reconstruído: {}".format(
        eng.name, " · ".join(partes) or "bootstrap não pronto, sem limitação nomeada")


def main() -> int:
    if "--engagement" in sys.argv:
        slug = sys.argv[sys.argv.index("--engagement") + 1]
        pronto, razao = avalia(engagements_root() / slug)
        print("pronto" if pronto else "BLOQUEIA: " + razao)
        return 0 if pronto else 1

    raw = sys.stdin.read()
    for i, ch in enumerate(raw):
        if ch in "{[":
            raw = raw[i:]
            break
    try:
        tool = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return 0

    if tool.get("tool_name") not in {"Write", "Edit"}:
        return 0

    file_path = (tool.get("tool_input") or {}).get("file_path") or ""
    if not file_path:
        return 0

    eng, nome = engagement_of(file_path)
    if eng is None:
        return 0

    pronto, razao = avalia(eng)
    if pronto:
        return 0

    if os.environ.get("AISA_GUARD_MODE") == "log":
        print("[pre-authority-guard] (log) {} — escrita em `{}` permitida por override".format(
            razao, nome), file=sys.stderr)
        return 0

    block("{}\n\nEscrever em `{}` sobre estado por reconstruir decide sobre estado misto. "
          "Recuperar primeiro; `AISA_GUARD_MODE=log` é o override administrativo "
          "explícito.".format(razao, nome))
    return 2


if __name__ == "__main__":
    sys.exit(main())
