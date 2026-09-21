"""phase-completeness.py -- Stop hook: did the phase skill actually write everything it owes?

Why a Stop hook and not PostToolUse on Skill: `PostToolUse` fires when the Skill tool
RETURNS, i.e. when the instructions are loaded -- long before the agent has executed
them, so `frame.md` does not exist yet at that moment. `Stop` fires when the turn ends,
with every write already on disk. That is the only point where completeness is a fact.

Soft gate by design (CLAUDE.md principle 5): it reports, never blocks, always exits 0.
Silent when the phase is complete.

Every check below is grounded in a skill's documented "Outputs (written)" section:
  .claude/skills/aisa-frame/SKILL.md    steps 3-6 (council) and 8/8c (validation)
  .claude/skills/aisa-options/SKILL.md  same shape, 7 personas
  .claude/skills/aisa-decide/SKILL.md   D-NNN + chained _synthesis/
  .claude/skills/chairman-synthesis/SKILL.md  the options.md content rule

Standalone use (no stdin): python .claude/hooks/phase-completeness.py [--engagement <slug>]
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

COUNCIL_6 = ["business-analyst", "operations-lead", "user-advocate",
             "data-steward", "compliance-officer", "cfo-lens"]
COUNCIL_7 = COUNCIL_6 + ["solution-architect"]
SYNTHESIS_PACKS = ["business-story", "as-is", "architecture-story",
                   "risks-and-assumptions", "financial-story"]


def utf8_stderr() -> None:
    """Claude Code surfaces hook stderr verbatim; on Windows it defaults to cp1252 and
    mangles the report's arrows and accents."""
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def engagements_root() -> Path:
    raw = os.environ.get("AISA_ENGAGEMENTS_ROOT")
    if raw:
        p = Path(raw)
        return p if p.is_absolute() else (repo_root() / p)
    return repo_root() / "projects"


def _activity_mtime(eng: Path) -> float:
    stamps = [0.0]
    for rel in ("_state.json", "shared-understanding.md", "decisions.md", "council-log.md"):
        f = eng / rel
        if f.exists():
            try:
                stamps.append(f.stat().st_mtime)
            except OSError:
                pass
    return max(stamps)


def find_engagement(slug: str | None = None) -> Path | None:
    base = engagements_root()
    if slug:
        cand = base / slug
        return cand if (cand / "_state.json").is_file() else None
    if not base.is_dir():
        return None
    engs = [d for d in base.iterdir() if d.is_dir() and (d / "_state.json").is_file()]
    return max(engs, key=_activity_mtime) if engs else None


def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def read_state(eng: Path) -> dict:
    raw = read_text(eng / "_state.json")
    for i, ch in enumerate(raw):
        if ch in "{[":
            raw = raw[i:]
            break
    try:
        out = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return {}
    return out if isinstance(out, dict) else {}


def su_has_round(su: str, section_round: str) -> int:
    """Rows written in this round: the `ronda` column is the last cell."""
    n = 0
    for line in su.splitlines():
        if line.startswith("|") and re.search(r"\|\s*" + re.escape(section_round) + r"\b[^|]*\|\s*$", line):
            n += 1
    return n


# --------------------------------------------------------------- per-phase checks


def check_framing(eng: Path, rnd: str, su: str) -> tuple[list, list]:
    """(council, validation) -- each a list of (ok, label, detail)."""
    frame = read_text(eng / "frame.md")
    sentence = ""
    m = re.search(r"^##\s+Single problem sentence\s*$(.*?)(?=^##\s|\Z)", frame, re.M | re.S)
    if m:
        sentence = " ".join(l.strip().lstrip(">").strip()
                            for l in m.group(1).splitlines() if l.strip())
    prep = eng / "lens-outputs" / "_council-prep"
    missing_prep = [p for p in COUNCIL_6 if not (prep / f"{rnd}-{p}.md").is_file()]
    rows = su_has_round(su, rnd)
    council = [
        (bool(frame.strip()), "frame.md escrito", f"{len(frame)} caracteres"),
        (len(sentence) > 40, "frase unica do problema",
         f"{len(sentence)} caracteres" if sentence else "seccao ausente ou vazia"),
        (rnd in frame[:200], f"frame.md carimbado com {rnd}",
         "cabecalho: " + (frame.splitlines()[0][:60] if frame else "-")),
        ((eng / "lens-outputs" / f"chairman-synthesis-{rnd}.md").is_file(),
         f"chairman-synthesis-{rnd}.md", ""),
        (not missing_prep, f"_council-prep 6/6 personas",
         "em falta: " + ", ".join(missing_prep) if missing_prep else "6/6"),
        (rows > 0, f"rows novas no SU com ronda {rnd}", f"{rows} rows"),
        (rnd in read_text(eng / "council-log.md"), f"council-log menciona {rnd}", ""),
        ("Framing" in read_text(eng / "shared-understanding.md")[:600],
         "cabecalho do SU diz Framing", ""),
    ]
    decisions = read_text(eng / "decisions.md")
    story = read_text(eng / "story.md")
    # The approval is any free D-NNN, not a fixed D-001 (P-18/F05): frame, solution and
    # blueprint approvals share one counter, and a re-approval in a later round gets its
    # own id. What must be true is that an approval exists AND cites this framing round.
    approvals = re.findall(r"^##\s+(D-\d+)\s+—?\s*Frame agreed(.*)$", decisions, re.M)
    cites_round = bool(re.search(
        r"\*\*Agreed in round\*\*\s*:\s*`?" + re.escape(rnd), decisions))
    validation = [
        (bool(approvals),
         "D-NNN — Frame agreed em decisions.md",
         "step 8, so apos validacao do utilizador"),
        (not approvals or cites_round,
         f"a aprovacao cita a passagem {rnd}",
         "aprovacao de outra passagem — /options compara a impressao digital"),
        (bool(re.search(r"^##\s+Epis[oó]dio.*\b(frame|frase)\b", story, re.M | re.I)),
         "episodio da story sobre o frame", "step 8c"),
    ]
    return council, validation


def check_options(eng: Path, rnd: str, su: str) -> tuple[list, list]:
    opts = read_text(eng / "options.md")
    blocks = re.findall(r"^###\s+(O-\d+)", opts, re.M)
    prep = eng / "lens-outputs" / "_council-prep"
    missing_prep = [p for p in COUNCIL_7 if not (prep / f"{rnd}-{p}.md").is_file()]
    rows = su_has_round(su, rnd)
    # As duas classes condicionais: o hook reporta a DECLARACAO em falta, nunca a classe
    # em falta. Le os marcadores do log da ronda, que sao verbatim e nao traduzidos — uma
    # palavra inglesa procurada no artefacto falha em falso, porque o artefacto sai na
    # lingua do pacote (defeito real, P-19: bunkers O-02 tinha as duas classes e o hook
    # reportava as duas em falta).
    log = read_text(eng / "lens-outputs" / f"chairman-synthesis-{rnd}.md")
    council = [
        (bool(opts.strip()), "options.md escrito", f"{len(opts)} caracteres"),
        (len(blocks) >= 3, "pelo menos 3 opcoes", f"{len(blocks)}: {', '.join(blocks) or '-'}"),
        ("DO-NOTHING" in log, "cobertura da classe DO-NOTHING declarada",
         "no log da ronda: na mesa (O-NNN) ou NOT PLAUSIBLE com ids"),
        ("PROCESS-CHANGE" in log, "cobertura da classe PROCESS-CHANGE declarada",
         "no log da ronda: na mesa (O-NNN) ou NOT PLAUSIBLE com ids"),
        (bool(re.search(r"(?mi)^##\s+(recomenda|recommendation)", opts)),
         "options.md fecha com a recomendacao", "chairman-synthesis, seccao Recommendation"),
        ((eng / "lens-outputs" / f"chairman-synthesis-{rnd}.md").is_file(),
         f"chairman-synthesis-{rnd}.md", ""),
        (not missing_prep, "_council-prep 7/7 personas",
         "em falta: " + ", ".join(missing_prep) if missing_prep else "7/7 (inclui solution-architect)"),
        (rows > 0, f"rows novas no SU com ronda {rnd}", f"{rows} rows"),
        (rnd in read_text(eng / "council-log.md"), f"council-log menciona {rnd}", ""),
    ]
    story = read_text(eng / "story.md")
    validation = [
        (bool(re.search(r"^##\s+Epis[oó]dio.*\bop[cç][oõ]es\b", story, re.M | re.I)),
         "episodio da story sobre as opcoes", "step story"),
    ]
    return council, validation


def blueprint_versions(eng: Path) -> list[str]:
    """The non-draft `ux-blueprint_vNN.yaml` files, newest last. Filenames only."""
    d = eng / "_blueprint"
    if not d.is_dir():
        return []
    out = []
    for p in sorted(d.glob("ux-blueprint_v*.yaml")):
        if re.search(r"(?m)^\s*draft\s*:\s*(true|yes)\s*$", read_text(p)):
            continue
        out.append(p.name)
    return out


def coverage_records(eng: Path) -> list[dict]:
    """`_coverage/coverage_vNN.json`, read for `stage` and `target.file` only.

    Filenames and two fields -- no inventory, no verdicts. A Stop hook runs on every turn
    end, and a full coverage evaluation there would cost a second of everybody's time to
    say what `/status` already says properly. Unreadable records are kept in the list with
    `stage: ""`, so a corrupt file reads as *present and unreadable*, never as absent."""
    d = eng / "_coverage"
    if not d.is_dir():
        return []
    out = []
    for p in sorted(d.glob("coverage_v*.json")):
        try:
            rec = json.loads(read_text(p))
            rec = rec if isinstance(rec, dict) else {}
        except Exception:                                           # noqa: BLE001
            rec = {}
        tgt = rec.get("target") if isinstance(rec.get("target"), dict) else {}
        out.append({"file": p.name, "stage": rec.get("stage") or "",
                    "target": (tgt or {}).get("file") or ""})
    return out


def check_coverage(eng: Path) -> list:
    """Coverage items -- **only once `/blueprint` actually ran** (plan phase 4, item 5).

    Right after `/decide` there is no design to cover, so there is nothing to check and no
    finding to report: an engagement that never produced a version gets an empty list, not
    a red line. Once a version exists, two things are owed: the reconciliation the version
    was produced against, and the review of that concrete version
    (coverage-contract.md §8.1). Reporting their absence is not revoking anything -- no
    record means `not_evaluated`, and any historical approval keeps standing (§10)."""
    versions = blueprint_versions(eng)
    if not versions:
        return []
    recs = coverage_records(eng)
    current = versions[-1]
    reviewed = {r["target"].rsplit("/", 1)[-1] for r in recs if r["stage"] == "blueprint"}
    return [
        (any(r["stage"] == "reconciliation" for r in recs),
         "revisao de reconciliacao em _coverage/",
         "aisa-blueprint passo 1e — sem ela a versao foi desenhada sem conferir as fontes"),
        (current in reviewed,
         f"revisao de cobertura da versao actual ({current})",
         "aisa-blueprint passo 13b — nao avaliada nao e aprovada nem reprovada"),
    ]


def check_decision(eng: Path, rnd: str, su: str) -> tuple[list, list]:
    decisions = read_text(eng / "decisions.md")
    blocks = re.findall(r"^##\s+(D-\d+)", decisions, re.M)
    # Which blocks are frame approvals is read from the file, not assumed of D-001.
    frame_blocks = set(re.findall(r"^##\s+(D-\d+)\s+—?\s*Frame agreed", decisions, re.M))
    final = [b for b in blocks if b not in frame_blocks]
    syn = eng / "_synthesis"
    missing_syn = [t for t in SYNTHESIS_PACKS if not (syn / f"{t}.md").is_file()]
    sim = sorted((eng / "_simulation").glob("options-comparison_v*.md")) if (eng / "_simulation").is_dir() else []
    cf = sorted((eng / "_simulation" / "counterfactuals").glob("O-*.md")) \
        if (eng / "_simulation" / "counterfactuals").is_dir() else []
    core = [
        (bool(final), "bloco D-NNN final em decisions.md", ", ".join(final) or "so aprovacoes do frame"),
        (not missing_syn, "5 topic packs em _synthesis/",
         "em falta: " + ", ".join(missing_syn) if missing_syn else "5/5"),
        (bool(re.search(r"^\|\s*D-\d+\s*\|", su, re.M)), "row D-NNN no SU", ""),
        (rnd in read_text(eng / "council-log.md"), f"council-log menciona {rnd}", ""),
    ]
    if sim:
        core.append((bool(cf), "counterfactuals congelados em _simulation/counterfactuals/",
                     f"{len(cf)} ficheiros (ha simulacao em {sim[-1].name})"))
    core += check_coverage(eng)
    story = read_text(eng / "story.md")
    validation = [
        (bool(re.search(r"^##\s+Epis[oó]dio.*\bdecis[aã]o\b", story, re.M | re.I)),
         "episodio da story sobre a decisao", "step story"),
    ]
    return core, validation


CHECKS = {"framing": check_framing, "options": check_options, "decision": check_decision}
GROUP_LABEL = {"framing": ("council (passos 3-6)", "fecho por validacao (passos 8, 8c)"),
               "options": ("council", "narrativa"),
               "decision": ("decisao + sintese", "narrativa")}


def run(eng: Path) -> int:
    state = read_state(eng)
    phase = (state.get("phase") or "").strip().lower()
    rnd = (state.get("round") or "").strip()
    fn = CHECKS.get(phase)
    if not fn:
        return 0  # discovery has no single-artefact contract; /round + lenses cover it
    su = read_text(eng / "shared-understanding.md")
    core, validation = fn(eng, rnd, su)
    bad_core = [c for c in core if not c[0]]
    bad_val = [c for c in validation if not c[0]]
    if not bad_core and not bad_val:
        return 0

    core_lbl, val_lbl = GROUP_LABEL[phase]
    out = [f"[phase-completeness] {eng.name} — {phase} {rnd}: "
           f"{len(core) - len(bad_core)}/{len(core)} {core_lbl}, "
           f"{len(validation) - len(bad_val)}/{len(validation)} {val_lbl}"]
    for label, items in ((core_lbl, bad_core), (val_lbl, bad_val)):
        for _, name, detail in items:
            out.append(f"  ✗ {label}: {name}" + (f" — {detail}" if detail else ""))
    if bad_core and not bad_val:
        out.append(f"  → o council de {rnd} nao fechou. Re-correr /{phase[:5]} ou completar o artefacto em falta.")
    elif bad_val and not bad_core:
        out.append("  → trabalho do council completo; falta o fecho. "
                   "Se ja validaste, a skill saltou o passo — pede-lhe para o escrever.")
    print("\n".join(out), file=sys.stderr)
    return 0


def main() -> int:
    utf8_stderr()
    args = sys.argv[1:]
    slug = None
    if "--engagement" in args:
        i = args.index("--engagement")
        if i + 1 < len(args):
            slug = args[i + 1]
    if not sys.stdin.isatty() and "--engagement" not in args:
        raw = sys.stdin.read()  # Stop payload; nothing in it is needed, but it must be drained
        del raw
    eng = find_engagement(slug)
    if eng is None:
        return 0
    return run(eng)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # a reporting hook must never break the turn
        print(f"[phase-completeness] ignorado: {exc}", file=sys.stderr)
        sys.exit(0)
