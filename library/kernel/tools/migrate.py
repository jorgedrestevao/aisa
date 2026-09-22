# -*- coding: utf-8 -*-
"""Migracao legacy -> memoria persistente (contrato C1/C2).

    python library/kernel/tools/migrate.py dry-run --engagement <slug> [--json]
    python library/kernel/tools/migrate.py apply   --engagement <slug>
    python library/kernel/tools/migrate.py restore --engagement <slug>

Stdlib apenas (ADR-001). Escreve SEMPRE pelo coordenador (`operation.py`).

O DRY-RUN NAO ESCREVE NO ENGAGEMENT (C1)
    Le SU, respostas, decisoes e estado; produz o mapa origem -> destino, a classificacao
    de cada item e as excepcoes. O relatorio fica FORA do snapshot — devolvido ao chamador,
    nunca gravado no engagement. Um dry-run que escrevesse deixaria de ser ensaio.

CLASSIFICACAO (C1.3) — cinco classes, e nenhuma e "mais ou menos"
    projectable          projecta sem ambiguidade
    already_represented  ja existe no grafo com o mesmo id
    ambiguous            origem nao verificavel ou autoridade nao determinavel
    invalid              a linha nao le (o parser marcou `malformed`)
    unsupported          fora do que esta porte trata

    Ambiguo NAO vira confirmado (M04). Um terceiro nao vira owner. Inferencia nao vira
    confirmacao. Linha `resolved` nao reabre.

REVERSAO (C2)
    So sobre a MESMA revisao pos-migracao e sem trabalho posterior. Havendo trabalho novo,
    o restore cego e recusado — preserva-se o que ha e reporta-se, em vez de escolher pelo
    utilizador. Remove apenas os ficheiros NOVOS listados no manifesto; ficheiros alheios
    nunca sao tocados.
"""
from __future__ import annotations

import hashlib
import json
import runpy
import shutil
import sys
from datetime import date
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_D = runpy.run_path(str(_HERE / "dashboard.py"))
_G = runpy.run_path(str(_HERE / "graph.py"))
_O = runpy.run_path(str(_HERE / "operation.py"))

MIGRATION_DIR = "_migration"
MANIFEST = "manifest.json"
BACKUP = "backup"
RUNTIME_VERSION = "p5.1"

SU_FILE = "shared-understanding.md"
DECISIONS_FILE = "decisions.md"
ANSWERS_FILE = "answers.md"
STATE_FILE = "_state.json"
TOUCHED = (SU_FILE, DECISIONS_FILE, ANSWERS_FILE, STATE_FILE)

PROJECTABLE = "projectable"
ALREADY = "already_represented"
AMBIGUOUS = "ambiguous"
INVALID = "invalid"
UNSUPPORTED = "unsupported"


class MigrationError(Exception):
    def __init__(self, message, code, detail=None):
        super().__init__(message)
        self.code = code
        self.detail = detail or {}

    def as_dict(self):
        return {"error": str(self), "code": self.code, "detail": self.detail}


def mig_dir(eng):
    return Path(eng) / MIGRATION_DIR


def _digests(eng):
    eng = Path(eng)
    out = {rel: _O["digest"](eng / rel) for rel in TOUCHED}
    gd = Path(eng) / "_graph"
    for rel in ("_graph/graph.jsonl", "_graph/meta.json"):
        out[rel] = _O["digest"](eng / rel)
    return out


# ----------------------------------------------------------------- classificacao

def classify(row, in_graph, known_ids=frozenset()):
    """A classe de UMA linha da SU. Nunca inventa confirmacao (M04)."""
    rid = (row.get("id") or "").strip()
    if not rid:
        return {"class": INVALID, "reason": "linha sem id"}
    if str(row.get("malformed")) == "True":
        return {"class": INVALID, "reason": "o parser marcou a linha como malformada"}
    if rid in in_graph:
        return {"class": ALREADY, "reason": "ja representado no grafo com o mesmo id"}

    state = row.get("state") or ""
    resolved = str(row.get("resolved")) == "True"
    targets = row.get("resolved_to") or []
    if isinstance(targets, str):
        try:
            targets = json.loads(targets.replace("'", '"'))
        except ValueError:
            targets = [t.strip() for t in targets.strip("[]").split(",") if t.strip()]

    # resolvida para um sucessor que nao existe -> ambigua; nao se corrige por conta propria
    if resolved and targets:
        missing = [t for t in targets if str(t).strip() not in known_ids]
        if missing:
            return {"class": AMBIGUOUS, "state": state, "resolved_to": targets,
                    "reason": "resolvida para sucessor inexistente: {}".format(
                        ", ".join(missing))}
        return {"class": PROJECTABLE, "state": state, "resolved_to": targets,
                "reason": "linha resolvida — cadeia preservada"}
    if resolved and not targets:
        return {"class": AMBIGUOUS, "state": state,
                "reason": "marcada resolvida sem sucessor identificavel"}

    # autoridade nao determinavel numa linha aberta que a exige
    if state in ("Unknown", "Conflicted"):
        raw = row.get("support") or ""
        o = _D["split_owner"](raw)
        if raw.strip() and not (o.get("role") or o.get("source")) and not o.get("unassigned"):
            return {"class": AMBIGUOUS, "state": state,
                    "reason": "`quem responde` sem prefixo `role:`/`fonte:` — o motor nao "
                              "julga se nomeia papel ou pessoa"}
    return {"class": PROJECTABLE, "state": state, "reason": "projecta sem ambiguidade"}


def active_decision(md):
    """A decisao ACTIVA: a ultima que nao foi substituida (M02).

    `classify_decisions` ja le `**Supersedes**: D-NNN` e retro-liga `superseded_by`. Usar o
    que ele computa; varrer outra vez daria uma segunda leitura a divergir da primeira."""
    blocks = _D["classify_decisions"](md or "")
    superseded = {b["id"] for b in blocks if b.get("superseded_by")}
    live = [b for b in blocks if b.get("id") not in superseded]
    return {"all": [b.get("id") for b in blocks],
            "superseded": sorted(superseded),
            "active": live[-1].get("id") if live else ""}


# ---------------------------------------------------------------------- dry-run

def dry_run(eng):
    """Le tudo, nao escreve NADA no engagement (C1.2)."""
    eng = Path(eng)
    if not (eng / SU_FILE).exists():
        raise MigrationError("engagement sem `{}`".format(SU_FILE), "NO_SU",
                             {"engagement": str(eng)})
    md = (eng / SU_FILE).read_text(encoding="utf-8")
    _h, rows, _s, _diag = _D["parse_su"](md)

    st = _G["read"](eng)
    if st["status"] not in (_G["OK"], _G["ABSENT"]):
        raise MigrationError("grafo em estado `{}` — migrar exige ausente ou valido".format(
            st["status"]), "GRAPH_NOT_MIGRATABLE", {"status": st["status"],
                                                    "detail": st["detail"]})
    in_graph = {n.get("id") for n in st.get("nodes", [])}

    known_ids = {(r.get('id') or '').strip() for r in rows}
    mapping, counts = [], {PROJECTABLE: 0, ALREADY: 0, AMBIGUOUS: 0,
                           INVALID: 0, UNSUPPORTED: 0}
    for r in rows:
        c = classify(r, in_graph, known_ids)
        counts[c["class"]] += 1
        mapping.append({"source": "{}#{}".format(SU_FILE, r.get("id") or "?"),
                        "id": r.get("id"), "state": r.get("state"),
                        "destination": ("graph:node:{}".format(r.get("id"))
                                        if c["class"] == PROJECTABLE else ""),
                        "class": c["class"], "reason": c["reason"],
                        "preserved": ["id", "state", "lens", "support", "ronda",
                                      "resolved", "resolved_to", "was"],
                        "resolved_to": c.get("resolved_to", [])})

    dec_md = (eng / DECISIONS_FILE).read_text(encoding="utf-8") if (eng / DECISIONS_FILE).exists() else ""
    decisions = active_decision(dec_md)

    exceptions = [m for m in mapping if m["class"] in (AMBIGUOUS, INVALID, UNSUPPORTED)]
    before = _digests(eng)
    return {"engagement": str(eng), "runtime_version": RUNTIME_VERSION,
            "when": date.today().isoformat(),
            "before": before,
            "plan_hash": hashlib.sha256(
                json.dumps(before, sort_keys=True).encode("utf-8")).hexdigest(),
            "rows": len(rows), "counts": counts, "mapping": mapping,
            "decisions": decisions, "exceptions": exceptions,
            "graph_status_before": st["status"],
            "complete": not exceptions,
            "note": ("migracao com excepcoes — nao declara sucesso total (C1)"
                     if exceptions else "todas as linhas projectam sem ambiguidade")}


# ------------------------------------------------------------------------ apply

def _nodes_from(plan, rows_by_id):
    nodes, edges = [], []
    for m in plan["mapping"]:
        if m["class"] != PROJECTABLE:
            continue
        r = rows_by_id.get(m["id"], {})
        nodes.append({"id": m["id"], "type": "su-row",
                      "props": {"state": m["state"] or "",
                                "text": r.get("claim", ""),
                                "resolved": str(r.get("resolved")) == "True"},
                      "provenance": {"lens": r.get("lens", ""), "ronda": r.get("ronda", ""),
                                     "support": r.get("support", ""),
                                     "source": m["source"],
                                     "migrated": plan["runtime_version"],
                                     "mirror_of": "SU:" + str(m["id"])}})
    have = {n["id"] for n in nodes}
    for m in plan["mapping"]:
        for t in (m.get("resolved_to") or []):
            t = str(t).strip()
            if m["id"] in have and t in have:
                edges.append({"src": t, "rel": "was", "dst": m["id"], "props": {},
                              "provenance": {"inferred": False,
                                             "source": "SU resolved -> marker"}})
    return nodes, edges


def apply(eng, plan=None):
    """Aplica pelo coordenador, com backup verificavel antes (C1.4, C1.5)."""
    eng = Path(eng)
    plan = plan or dry_run(eng)

    # C1: entrada mudou depois do dry-run -> rejeitar plano antigo
    now = _digests(eng)
    if now != plan["before"]:
        raise MigrationError("a entrada mudou depois do ensaio — recalcular", "PLAN_STALE",
                             {"expected": plan["before"], "actual": now})

    # No-op: o estado ACTUAL ja e o estado pos-migracao registado. Comparar `plan_hash`
    # nao serve — ele deriva dos digests PRE-migracao, que mudam assim que se migra.
    existing = read_manifest(eng)
    if existing and existing.get("after") == now:
        return {"result": "no_op", "reason": "migracao ja aplicada; o estado actual e o "
                                             "estado pos-migracao registado",
                "manifest": existing}

    md = (eng / SU_FILE).read_text(encoding="utf-8")
    _h, rows, _s, _d = _D["parse_su"](md)
    rows_by_id = {(r.get("id") or "").strip(): r for r in rows}

    st = _G["read"](eng)
    nodes, edges = _nodes_from(plan, rows_by_id)
    known = {n["id"] for n in st.get("nodes", [])}
    nodes = [n for n in nodes if n["id"] not in known] + list(st.get("nodes", []))
    edges = list(st.get("edges", [])) + [e for e in edges
                                         if not any(x.get("src") == e["src"] and
                                                    x.get("dst") == e["dst"]
                                                    for x in st.get("edges", []))]

    # backup verificavel ANTES de publicar
    bdir = mig_dir(eng) / BACKUP
    bdir.mkdir(parents=True, exist_ok=True)
    backed, new_files = {}, []
    for rel in TOUCHED:
        src = eng / rel
        if src.exists():
            dst = bdir / rel.replace("/", "__")
            shutil.copy2(src, dst)
            back = _O["digest"](dst)
            if back != _O["digest"](src):
                raise MigrationError("backup nao confere em `{}`".format(rel), "BACKUP_MISMATCH",
                                     {"path": rel})
            backed[rel] = back
    for rel in ("_graph/graph.jsonl", "_graph/meta.json"):
        if not (eng / rel).exists():
            new_files.append(rel)

    write_set = _G["write_set"](nodes, edges)
    op = "migrate-{}".format(plan["plan_hash"][:16])
    receipt = _O["run"](eng, op, write_set, expected={k: plan["before"].get(k, "")
                                                     for k in write_set})

    # O id da operacao deriva do `plan_hash`, que deriva dos digests PRE-migracao.
    # Depois de um `restore` o estado volta a ser o de antes, o plano volta a dar o
    # mesmo hash, e o coordenador reconhecia o recibo antigo e devolvia sucesso sem
    # escrever nada — um `migrated` sobre um grafo ausente. `ACCEPTANCE.md` §2 diz
    # «Zero sucesso falso de operacao interrompida/rejeitada», e era isso.
    if receipt.get("replayed") and receipt.get("effects_present") is False:
        raise MigrationError(
            "o recibo desta migracao existe mas os ficheiros nao — um `restore` "
            "reverteu-a e deixou o recibo para tras", "RECEIPT_STALE",
            {"operation_id": op, "published": receipt.get("published", []),
             "recovery": "apagar o recibo desta operacao antes de re-migrar"})

    manifest = {"runtime_version": plan["runtime_version"], "when": plan["when"],
                "plan_hash": plan["plan_hash"], "operation_id": op,
                "before": plan["before"], "after": _digests(eng),
                "backed_up": backed, "new_files": new_files,
                "counts": plan["counts"], "exceptions": plan["exceptions"],
                "complete": plan["complete"]}
    _O["_atomic_write"](mig_dir(eng) / MANIFEST,
                        json.dumps(manifest, ensure_ascii=False, indent=2))
    return {"result": "migrated", "manifest": manifest, "receipt": receipt,
            "success_declared": plan["complete"],
            "note": ("sucesso PARCIAL — ha excepcoes; o avanco afectado fica bloqueado"
                     if not plan["complete"] else "migracao completa")}


def read_manifest(eng):
    p = mig_dir(eng) / MANIFEST
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


# ---------------------------------------------------------------------- restore

def restore(eng, force=False):
    """Reverte — so sobre a mesma revisao pos-migracao e sem trabalho posterior (C2)."""
    eng = Path(eng)
    man = read_manifest(eng)
    if not man:
        raise MigrationError("nao ha manifesto de migracao", "NO_MANIFEST",
                             {"engagement": str(eng)})

    now = _digests(eng)
    drifted = {rel: {"expected": man["after"].get(rel, ""), "actual": now.get(rel, "")}
               for rel in man["after"] if now.get(rel, "") != man["after"].get(rel, "")}
    if drifted and not force:
        raise MigrationError(
            "houve trabalho depois da migracao — restore cego recusado", "WORK_AFTER",
            {"changed": drifted,
             "detail": "o trabalho novo e preservado; reconciliar antes de reverter"})

    for rel, want in man["backed_up"].items():
        src = mig_dir(eng) / BACKUP / rel.replace("/", "__")
        if not src.is_file():
            raise MigrationError("backup em falta para `{}`".format(rel), "BACKUP_MISSING",
                                 {"path": rel})
        if _O["digest"](src) != want:
            raise MigrationError("backup de `{}` nao confere".format(rel), "BACKUP_CORRUPT",
                                 {"path": rel})
        shutil.copy2(src, eng / rel)

    # Reverter e desfazer a operacao, logo o recibo dela deixa de descrever a
    # realidade. Deixa-lo para tras fazia com que uma re-migracao a partir do mesmo
    # estado batesse no recibo antigo e recebesse sucesso sem escrita nenhuma —
    # ver `RECEIPT_STALE` em `apply`.
    op_revertida = man.get("operation_id")
    if op_revertida:
        try:
            _O["receipt_path"](eng, op_revertida).unlink()
        except OSError:
            pass

    removed = []
    for rel in man.get("new_files", []):
        p = eng / rel
        if p.exists():
            p.unlink()
            removed.append(rel)
    gd = eng / "_graph"
    if gd.is_dir() and not any(gd.iterdir()):
        gd.rmdir()

    after = _digests(eng)
    mismatched = {rel: {"expected": man["before"][rel], "actual": after.get(rel, "")}
                  for rel in man["backed_up"] if after.get(rel, "") != man["before"][rel]}
    if mismatched:
        raise MigrationError("restore nao reproduziu os hashes originais", "RESTORE_MISMATCH",
                             {"paths": mismatched})
    return {"result": "restored", "restored": sorted(man["backed_up"]),
            "removed_new_files": removed,
            "note": "apenas ficheiros do manifesto foram tocados; ficheiros alheios intactos"}


# --------------------------------------------------------------------------- CLI

def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description="migracao legacy -> memoria persistente")
    ap.add_argument("command", choices=["dry-run", "apply", "restore"])
    ap.add_argument("--engagement", required=True)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    eng = Path(a.engagement)
    if not eng.is_dir():
        eng = Path("projects") / a.engagement
    try:
        if a.command == "dry-run":
            out = dry_run(eng)
        elif a.command == "apply":
            out = apply(eng)
        else:
            out = restore(eng, force=a.force)
    except (MigrationError, _O["OperationError"], _G["GraphError"]) as exc:
        print(json.dumps(exc.as_dict(), ensure_ascii=False, indent=2), file=sys.stderr)
        return 1
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        for k in ("result", "rows", "counts", "note", "success_declared"):
            if k in out:
                print("{:18} {}".format(k, out[k]))
        for e in out.get("exceptions", [])[:10]:
            print("  ! {:10} {} — {}".format(e["class"], e["id"], e["reason"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
