"""phase-gate-check.py -- PreToolUse on Skill: the soft gate of a phase transition is
EVALUATED, and the verdict is written down.

Why PreToolUse and not PostToolUse: the gate judges the phase that is ENDING, and that
state is on disk before the transition skill runs. (Completeness is the opposite case and
stays a Stop hook -- see phase-completeness.py's own note.)

Soft by design (CLAUDE.md principle 5): it reports, never blocks, always exits 0. What it
adds over the previous stub is that the criteria of `library/kernel/phases.md` are actually
computed (`dashboard.py::gate_state`), each one carries its MODE -- `codigo`, `juizo`,
`n/a` -- and the result survives the terminal:

    <engagement>/gate-log.md      one line per evaluation, append-only, only this hook writes

Coverage is declared, never implied: the line says `n de m por codigo`, and a criterion
nobody can measure is `n/a`, never OK.

Identity and life cycle. The override arrives on a SECOND invocation (the owner answers,
the skill runs again with --override), so both lines must be tied to the same evaluation.
The id is a fingerprint of the STATE that was judged -- ids of the open rows, sha of
decisions.md / options.md / frame.md / the lens outputs, plus each criterion's own result --
so the second line carries `refers: <same id>` when nothing changed, and a NEW id with
`refers: none` when the owner fixed something in between. That is information, not an error.

The engagement is EXPLICIT: the three commands pass `--engagement <slug>`. With no slug and
several engagements mounted the hook writes NOTHING and says `not evaluated (ambiguous
engagement)` -- recording a verdict against the wrong project is worse than not recording one.

Standalone: python .claude/hooks/phase-gate-check.py --engagement <slug> --skill aisa-frame
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    arg_override, arg_slug, engagements_root, find_engagement, load_dashboard,
    read_text, tool_payload, utf8_stderr,
)

HEADER = ("# Gate log — {slug}\n\n"
          "Um veredicto por transição de fase, escrito pelo hook `phase-gate-check.py`.\n"
          "Cada linha diz quantos critérios foram avaliados **por código**, quais ficaram\n"
          "vermelhos, quais dependem de juízo e quais não são avaliáveis. Um override é do\n"
          "dono, com razão, e liga-se à avaliação que o antecedeu (`refers`).\n"
          "Ficheiro append-only; nada aqui bloqueia nada.\n\n")


def log_line(g: dict, slug: str, override: bool, reason: str, refers: str,
             how: str) -> str:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    parts = [
        stamp,
        "{}{}".format(slug, "" if how == "explicit" else " (engagement: {})".format(how)),
        g["transition"],
        g["id"],
        "{}/{} por código".format(g["evaluated"], g["total"]),
        "red: " + (", ".join(g["red"]) if g["red"] else "nenhum"),
        "juízo: " + (", ".join(g["judgement"]) if g["judgement"] else "nenhum"),
        "n/a: " + (", ".join(g["na"]) if g["na"] else "nenhum"),
        ("override: yes \"{}\"".format(reason) if override else "override: no"),
    ]
    if override:
        parts.append("refers: " + (refers or "none"))
    return " · ".join(parts) + "\n"


def previous_id(eng: Path, transition: str) -> str:
    """The id of the most recent evaluation of this transition WITHOUT an override --
    what a later override refers back to."""
    for line in reversed(read_text(eng / "gate-log.md").splitlines()):
        if transition in line and "override: no" in line:
            for chunk in line.split(" · "):
                if chunk.startswith("G-"):
                    return chunk
    return ""


def report(g: dict, slug: str, override: bool, reason: str) -> None:
    print("[phase-gate-check] {} · {} · {} — {}/{} por código{}".format(
        slug, g["transition"], g["id"], g["evaluated"], g["total"],
        " · override: \"{}\"".format(reason) if override else ""), file=sys.stderr)
    for c in g["criteria"]:
        mark = {"codigo": ("ok " if c["ok"] else "RED"), "juizo": "juí", "n/a": "n/a"}[c["mode"]]
        detail = c["value"] or c["note"]
        print("  [{}] {}{}".format(mark, c["criterion"],
                                   ("  — " + detail) if detail else ""), file=sys.stderr)
    print("  → {}. O veredicto fica em gate-log.md; a decisão de avançar é do dono.".format(
        g["note"]), file=sys.stderr)


def run(eng: Path, skill: str, args_text: str, how: str) -> int:
    D = load_dashboard()
    transition = D["GATE_TRANSITIONS"].get(skill, "")
    if not transition:
        return 0
    try:
        g = D["gate_state"](eng, transition)
    except Exception as exc:                                        # noqa: BLE001
        print("[phase-gate-check] gate: not evaluated — {}: {}".format(
            type(exc).__name__, exc), file=sys.stderr)
        _append(eng, "{} · {} · {} · gate: not evaluated — {}\n".format(
            dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            eng.name, transition, type(exc).__name__))
        return 0
    override, reason = arg_override(args_text)
    # An override refers back to the evaluation it answers -- but only when the state did
    # not move in between. If the owner fixed something before repeating, the id is new and
    # `refers: none` says exactly that: this override answers a different reality.
    prev = previous_id(eng, transition) if override else ""
    refers = prev if prev == g["id"] else "none"
    _append(eng, log_line(g, eng.name, override, reason, refers, how))
    report(g, eng.name, override, reason)
    return 0


def _append(eng: Path, line: str) -> None:
    f = eng / "gate-log.md"
    try:
        if not f.is_file():
            f.write_text(HEADER.format(slug=eng.name), encoding="utf-8")
        with f.open("a", encoding="utf-8") as fh:
            fh.write(line)
    except OSError as exc:
        print("[phase-gate-check] não consegui escrever gate-log.md: {}".format(exc),
              file=sys.stderr)


def main() -> int:
    utf8_stderr()
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--engagement")
    ap.add_argument("--skill")
    ap.add_argument("--args", default="")
    cli, _rest = ap.parse_known_args()

    skill, args_text, slug = cli.skill or "", cli.args or "", cli.engagement or ""
    if not skill:
        tool = tool_payload(sys.stdin.read())
        ti = tool.get("tool_input") or {}
        skill = ti.get("skill") or ""
        args_text = ti.get("args") or ""
        slug = arg_slug(args_text)
    if not skill:
        return 0
    D_transitions = ("aisa-frame", "aisa-options", "aisa-decide")
    if skill not in D_transitions:
        return 0

    eng, how = find_engagement(slug or None, allow_ambiguous=False)
    if eng is None:
        if how == "ambiguous":
            print("[phase-gate-check] gate: not evaluated (ambiguous engagement) — "
                  "vários engagements montados em {} e a invocação de {} não passou "
                  "`--engagement <slug>`; nada foi escrito.".format(
                      engagements_root(), skill), file=sys.stderr)
        else:
            print("[phase-gate-check] gate: not evaluated — engagement não resolvido"
                  "{}".format(" ({})".format(slug) if slug else ""), file=sys.stderr)
        return 0
    try:
        return run(eng, skill, args_text, how)
    except Exception as exc:                                        # noqa: BLE001
        print("[phase-gate-check] gate: not evaluated — {}: {}".format(
            type(exc).__name__, exc), file=sys.stderr)
        return 0


if __name__ == "__main__":
    sys.exit(main())
