"""synthesis-validate.py -- PostToolUse on Write|Edit of <engagement>/_synthesis/<topic>.md.

Evaluates the contract of `aisa-synthesize` (step 7 + rules 2 and 3) by code:

    SYN-PARAS     fewer than 3 non-empty paragraphs
    SYN-NO-IDS    no SU id cited
    SYN-DEAD-ID   an id cited with no row in the SU nor block in decisions.md
    SYN-VENDOR    a term that NAMES A SOLUTION in a neutral topic -- and in
                  architecture-story too when no architecture was authorized
    SYN-TEMPLATE  a topic outside the kernel's five
    SYN-STAMP     architecture-story with no `authority:` stamp, or one naming a
                  version that fails the structural check. `authority: none — <reason>`
                  is the legitimate case where no architecture was authorized.

Everything is a warning: synthesis is narrative and the judgement is the skill's. The hook
signals, with the line and the term.

WHERE IT WRITES, and why not the obvious place. The record goes to

    <engagement>/_synthesis/_synthesis-checks.md

and NEVER to `_synthesis-log.md`: `synthesis_entries()` matches any `<ISO> — <token>` line
and `synthesis_state()` takes the newest of them as when the topic was synthesised, so a
validation line dated today would make a stale pack look fresh. The check file is history
-- what this hook saw, with the sha of the text and of the dependencies. The VERDICT is
recomputed on every read (`dashboard.py::synthesis_checks`), because SYN-DEAD-ID,
SYN-VENDOR and SYN-STAMP also depend on the SU, the pack and the blueprint: the text can sit
unchanged while the answer changes.

Soft: reports, never blocks, always exits 0.

Standalone: python .claude/hooks/synthesis-validate.py <path-to-_synthesis/<topic>.md>
"""

from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import load_dashboard, read_text, tool_payload, utf8_stderr  # noqa: E402

HEADER = ("# Synthesis checks — {slug}\n\n"
          "Um registo por validação de um topic pack, escrito pelo hook\n"
          "`synthesis-validate.py`. **Isto é história, não é o veredicto**: os testes\n"
          "dependem também da SU, do pacote e do desenho aprovado, por isso o veredicto\n"
          "é recalculado quando alguém pergunta (`dashboard.py --json` → `synthesis_checks`).\n"
          "Cada linha traz o `sha` do texto validado e o `deps` das fontes de que dependia.\n"
          "Ficheiro append-only; a última linha por tópico é a mais recente. Nada bloqueia.\n\n")


def line_for(res: dict) -> str:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if res["codes"]:
        result = ", ".join("{} ({})".format(c["code"], c["detail"]) if c["detail"]
                           else c["code"] for c in res["codes"])
    else:
        result = "ok"
    if res["not_evaluated"]:
        result += " · não avaliado: " + "; ".join(res["not_evaluated"])
    if res.get("notes"):
        result += " · nota: " + "; ".join(res["notes"])
    return "check · {} · {} · sha:{} · deps:{} · {}\n".format(
        stamp, res["topic"], res["sha"], res["deps"], result)


def check(path: Path) -> int:
    D = load_dashboard()
    topic = path.stem
    eng = path.resolve().parent.parent
    if not (eng / "_state.json").is_file():
        return 0
    res = D["synthesis_check"](eng, topic)
    if not res["present"]:
        return 0
    out = eng / "_synthesis" / "_synthesis-checks.md"
    try:
        if not out.is_file():
            out.write_text(HEADER.format(slug=eng.name), encoding="utf-8")
        with out.open("a", encoding="utf-8") as fh:
            fh.write(line_for(res))
    except OSError as exc:
        print("[synthesis-validate] não consegui escrever _synthesis-checks.md: {}".format(exc),
              file=sys.stderr)
    if res["codes"]:
        print("[synthesis-validate] {} — {} aviso(s)".format(path.name, len(res["codes"])),
              file=sys.stderr)
        for c in res["codes"]:
            print("  {} · {}".format(c["code"], c["detail"] or ""), file=sys.stderr)
        print("  → registo em _synthesis/_synthesis-checks.md (história); o veredicto "
              "recalcula-se na consulta.", file=sys.stderr)
    elif res["not_evaluated"]:
        print("[synthesis-validate] {} — sem avisos · não avaliado: {}".format(
            path.name, "; ".join(res["not_evaluated"])), file=sys.stderr)
    elif res.get("notes"):
        print("[synthesis-validate] {} — sem avisos · {}".format(
            path.name, "; ".join(res["notes"])), file=sys.stderr)
    return 0


def main() -> int:
    utf8_stderr()
    if len(sys.argv) > 1:
        return check(Path(sys.argv[1]))
    tool = tool_payload(sys.stdin.read())
    if tool.get("tool_name") not in {"Write", "Edit"}:
        return 0
    fp = (tool.get("tool_input") or {}).get("file_path") or ""
    norm = fp.replace("\\", "/")
    if not re.search(r"_synthesis/[^_/][^/]*\.md$", norm):
        return 0          # `_synthesis-log.md` and `_synthesis-checks.md` never self-validate
    try:
        return check(Path(fp))
    except Exception as exc:                                        # noqa: BLE001
        print("[synthesis-validate] not evaluated — {}: {}".format(
            type(exc).__name__, exc), file=sys.stderr)
        return 0


if __name__ == "__main__":
    sys.exit(main())
