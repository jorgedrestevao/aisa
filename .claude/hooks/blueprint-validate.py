"""blueprint-validate.py -- PostToolUse on Write|Edit of <engagement>/_blueprint/ux-blueprint_vNN.yaml.

Reports TWO separate things about the version just written, and never merges them:

  1. **Structure** -- dashboard.py::bp_validate (blueprint-contract.md -> "Validação
     estrutural", the 25 codes of the runtime-hardening plan A3).
  2. **Coverage** -- coverage.py::coverage_state for stage `blueprint` on this file
     (coverage-contract.md §8.1). This is the F06 finding made visible: the same version
     the structural check calls valid can have lost a requirement the SU already carried.

It writes NOTHING: the durable records are aisa-blueprint step 13 (validation.violations +
blueprint-log.md) and the published review in `_coverage/`; the hook only makes both results
visible at once. The coverage read is read-only and never finalizes a review.

Soft by design (CLAUDE.md principle 5): reports, never blocks, always exits 0. Silent when
the version has no structural issue AND its coverage is complete and current. A `block`
issue means the version cannot be APPROVED (step 15 refuses mechanically); production is
never blocked, and neither is it by a coverage gap.

The hook is a convenience, never the mechanism: the same two checks run explicitly from
`aisa-blueprint` (steps 1e, 13 and 13b) with the CLI commands printed below, so a session where
no hook fired loses visibility, not enforcement.

Standalone: python .claude/hooks/blueprint-validate.py <path-to-ux-blueprint_vNN.yaml>
"""

from __future__ import annotations

import json
import runpy
import sys
from pathlib import Path


def utf8_stderr() -> None:
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_dashboard():
    return runpy.run_path(str(repo_root() / "library" / "kernel" / "tools" / "dashboard.py"))


def coverage(D, eng: Path, path: Path) -> None:
    """The second half of the report -- never mixed with the first.

    Read-only: it selects the published review for this exact version and recomputes the
    verdicts. No record for it is `not_evaluated`, which is neither approval nor failure
    (coverage-contract.md §10) -- so it is said in one line, with the command that fixes it,
    and never as a pass."""
    rel = "_blueprint/" + path.name
    try:
        C = D["coverage_module"]()
        if C is None:
            print("[blueprint-validate] cobertura não avaliada — motor indisponível",
                  file=sys.stderr)
            return
        if not C["record_files"](eng):
            # Nothing to compare a denominator against; say so without paying for one.
            print("[blueprint-validate] {} — cobertura desta versão: não avaliada (sem "
                  "revisão registada em _coverage/). Não é aprovação nem reprovação, e não "
                  "revoga aprovação nenhuma.\n  → produzir a revisão: aisa-blueprint passo "
                  "13b".format(path.name), file=sys.stderr)
            return
        readers = C["ReaderAdapter"](module=D)
        target = {"file": rel, "identity": C["target_identity"](eng, "blueprint", rel)}
        res = C["coverage_state"](eng, "blueprint", target, readers)
    except Exception as exc:                                        # noqa: BLE001
        print("[blueprint-validate] cobertura não avaliada — {}: {}".format(
            type(exc).__name__, exc), file=sys.stderr)
        return
    cmd = ("python library/kernel/tools/coverage.py check --engagement {} --stage "
           "blueprint --target {}".format(eng.name, rel))
    if res["coverage"] == "complete" and res["freshness"] == "current" \
            and res["contract_validity"] == "valid":
        return                                                      # silent when clean
    gaps = res.get("gaps") or []
    codes = sorted({d["code"] for d in res.get("diagnostics") or [] if d.get("code")})
    print("[blueprint-validate] {} — cobertura: {} · atualidade: {} · registo: {} · "
          "leitura nos dois sentidos: {}".format(
              path.name, res["coverage"], res["freshness"], res["contract_validity"],
              res["semantic_review"]), file=sys.stderr)
    for g in gaps[:20]:
        print("  lacuna · {} · {} · {}".format(
            g.get("item", ""), ", ".join(g.get("requirement_refs") or []) or "—",
            g.get("status", "")), file=sys.stderr)
    if codes:
        print("  códigos: " + " · ".join(codes), file=sys.stderr)
    for r in (res.get("reasons") or [])[:4]:
        print("  → " + r, file=sys.stderr)
    print("  → estrutura e cobertura são perguntas separadas; nenhuma delas é aprovação. "
          "Detalhe: `{}`".format(cmd), file=sys.stderr)


def check(path: Path) -> int:
    D = load_dashboard()
    if not path.is_file() or not D["BP_FILE_RE"].match(path.name):
        return 0
    eng = path.resolve().parent.parent
    su_ids = None
    cfg: dict = {}
    loader = None
    if (eng / "_state.json").is_file():
        _h, rows, _m, _d = D["parse_su"](D["_read"](eng / "shared-understanding.md") or "")
        su_ids = {r["id"] for r in rows if r.get("id")}
        cfg = D["bp_pack_cfg"](D["_read_json"](eng / "_state.json").get("pack", ""))
        loader = D["bp_loader"](eng)
    issues = D["bp_validate"](D["_read"](path) or "", path.name, cfg, su_ids, loader)
    if (eng / "_state.json").is_file():
        coverage(D, eng, path)
    if not issues:
        return 0
    nb = sum(1 for i in issues if i["severity"] == "block")
    nw = len(issues) - nb
    head = ("[blueprint-validate] {} — {} falha(s) que impedem a aprovação, {} aviso(s)"
            if nb else "[blueprint-validate] {} — sem falhas, {} aviso(s) (blocking: {})")
    print(head.format(path.name, nb, nw) if nb else head.format(path.name, nw, nb), file=sys.stderr)
    for i in issues[:40]:
        print("  {code} · {severity} · {path}{ln} · {message}".format(
            ln=(" · L" + str(i["line"])) if i.get("line") else "", **i), file=sys.stderr)
    if len(issues) > 40:
        print("  … {} mais — `python library/kernel/tools/dashboard.py --blueprint-check {}`"
              .format(len(issues) - 40, path), file=sys.stderr)
    if nb:
        print("  → a versão pode ser produzida, não aprovada (blueprint-contract.md → Validação "
              "estrutural). Registo: aisa-blueprint passo 13.", file=sys.stderr)
    return 0


def main() -> int:
    utf8_stderr()
    if len(sys.argv) > 1:
        return check(Path(sys.argv[1]))
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
    fp = (tool.get("tool_input") or {}).get("file_path") or ""
    if not fp:
        return 0
    p = Path(fp)
    if p.parent.name != "_blueprint":
        return 0
    try:
        return check(p)
    except Exception as exc:                                        # noqa: BLE001
        print("[blueprint-validate] not evaluated — {}: {}".format(type(exc).__name__, exc),
              file=sys.stderr)
        return 0


if __name__ == "__main__":
    sys.exit(main())
