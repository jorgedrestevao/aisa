# -*- coding: utf-8 -*-
"""Grafo aditivo do engagement — armazenamento, integridade e consulta.

    python library/kernel/tools/graph.py status --engagement <slug>
    python library/kernel/tools/graph.py verify --engagement <slug> [--json]

Stdlib apenas (ADR-001). Executar não é escrever: este motor só escreve através de
`operation.py`, que coordena a publicação; as funções de escrita aqui recebem sempre um
caminho de staging e nunca publicam sozinhas.

FORMATO (P1, decidido contra `contracts/WRITES_AND_RECOVERY.md`)

    <engagement>/_graph/graph.jsonl   registos, um por linha, ordem canónica
    <engagement>/_graph/meta.json     schema, revisão, contagens, digest

JSONL porque o grafo é aditivo e uma linha por registo torna a serialização estável,
o diff legível e a leitura incremental possível sem carregar tudo. `meta.json` separado
porque a revisão tem de ser lida sem ler o grafo inteiro — os gates fazem-no a cada
operação.

O par é verificado em conjunto: `meta` sozinho, `graph` sozinho, ou digest que não bate,
são estados DISTINTOS de «não existe» (K07). Nenhum deles autoriza modo legacy.

DETERMINISMO (K03)

Nós ordenam por `(type, id)`, arestas por `(src, rel, dst)`; as chaves de cada registo
saem em ordem fixa; `ensure_ascii=False` e `\n` explícito. Duas entradas semanticamente
iguais por ordem diferente produzem bytes iguais — e portanto a mesma revisão.

AUTORIDADE (K05)

Um campo espelhado do SU (`mirror_of`) NUNCA prevalece sobre a sua autoridade. `verify()`
compara-o com a origem e reporta `drift`; não corrige, não promove, e o chamador não pode
avançar um gate sobre drift. `fact != fit` continua a valer: o grafo guarda relações, não
decide adequação.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

SCHEMA_VERSION = 1
STORE_DIR = "_graph"
GRAPH_FILE = "graph.jsonl"
META_FILE = "meta.json"

# Estados do store. `ABSENT` é o único que autoriza modo legacy (contrato B4).
ABSENT = "absent"
OK = "ok"
UNREADABLE = "unreadable"
INVALID_FORMAT = "invalid_format"
UNSUPPORTED_SCHEMA = "unsupported_schema"
INCOHERENT_PAIR = "incoherent_pair"

NODE_KEYS = ("kind", "id", "type", "props", "provenance")
EDGE_KEYS = ("kind", "src", "rel", "dst", "props", "provenance")


class GraphError(Exception):
    """Erro explícito com código — nunca um silêncio (K04, K06)."""

    def __init__(self, message: str, code: str, detail: dict | None = None):
        super().__init__(message)
        self.code = code
        self.detail = detail or {}

    def as_dict(self) -> dict:
        return {"error": str(self), "code": self.code, "detail": self.detail}


# --------------------------------------------------------------------- caminhos

def store_dir(eng: Path) -> Path:
    return Path(eng) / STORE_DIR


def _within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def guard_path(eng: Path, candidate: Path) -> Path:
    """O caminho pertence a ESTE engagement, resolvido (K08).

    Resolve antes de decidir: um symlink que sai do engagement é recusado mesmo quando
    o caminho escrito parece interior. É a mesma disciplina que `coverage.py` aplica ao
    inventário — a fronteira decide-se sobre o caminho real, não sobre o texto."""
    eng_real = Path(eng).resolve()
    try:
        real = Path(candidate).resolve()
    except OSError as exc:
        raise GraphError("caminho irresolúvel: {}".format(candidate),
                         "PATH_UNRESOLVABLE", {"path": str(candidate), "os": str(exc)})
    if not _within(real, eng_real):
        raise GraphError(
            "caminho fora do engagement — recusado sem ler: {}".format(real),
            "PATH_ESCAPE", {"path": str(real), "engagement": str(eng_real)})
    return real


# ------------------------------------------------------------------ serialização

def _ordered(record: dict, keys: tuple) -> dict:
    """Chaves na ordem do contrato; desconhecidas no fim, por ordem, NUNCA apagadas (K06)."""
    out = {k: record[k] for k in keys if k in record}
    for k in sorted(record):
        if k not in out:
            out[k] = record[k]
    return out


def _node_key(n: dict) -> tuple:
    return (str(n.get("type", "")), str(n.get("id", "")))


def _edge_key(e: dict) -> tuple:
    return (str(e.get("src", "")), str(e.get("rel", "")), str(e.get("dst", "")))


def canonical_lines(nodes: list[dict], edges: list[dict]) -> list[str]:
    """A representação canónica. Mesma semântica, mesmos bytes (K03)."""
    lines = []
    for n in sorted(nodes, key=_node_key):
        lines.append(json.dumps(_ordered(dict(n, kind="node"), NODE_KEYS),
                                ensure_ascii=False, sort_keys=False, separators=(",", ":")))
    for e in sorted(edges, key=_edge_key):
        lines.append(json.dumps(_ordered(dict(e, kind="edge"), EDGE_KEYS),
                                ensure_ascii=False, sort_keys=False, separators=(",", ":")))
    return lines


def revision_of(nodes: list[dict], edges: list[dict]) -> str:
    body = "\n".join(canonical_lines(nodes, edges))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


# -------------------------------------------------------------------- integridade

def validate(nodes: list[dict], edges: list[dict]) -> list[dict]:
    """Erros de integridade, TODOS de uma vez. Lista vazia = válido (K04)."""
    problems = []
    seen: dict[str, dict] = {}
    for n in nodes:
        nid = n.get("id")
        if not nid or not isinstance(nid, str):
            problems.append({"code": "NODE_ID_MISSING", "record": n})
            continue
        if not n.get("type"):
            problems.append({"code": "NODE_TYPE_MISSING", "id": nid})
        if nid in seen:
            problems.append({"code": "NODE_ID_DUPLICATE", "id": nid,
                             "detail": "o mesmo id aparece duas vezes"})
        seen[nid] = n
    for e in edges:
        src, rel, dst = e.get("src"), e.get("rel"), e.get("dst")
        if not rel or not isinstance(rel, str):
            problems.append({"code": "EDGE_REL_MISSING", "record": e})
        for end, val in (("src", src), ("dst", dst)):
            if not val or not isinstance(val, str):
                problems.append({"code": "EDGE_END_MISSING", "end": end, "record": e})
            elif val not in seen:
                problems.append({"code": "EDGE_END_UNKNOWN", "end": end, "id": val,
                                 "detail": "ponta que não corresponde a nenhum nó"})
    return problems


def drift(nodes: list[dict], authority: dict) -> list[dict]:
    """Campos espelhados que já não batem com a sua autoridade (K05).

    `authority` mapeia `<id do SU>` → valor actual. Um nó com `mirror_of` aponta para lá.
    Divergência é REPORTADA; o grafo não prevalece nem se auto-corrige."""
    out = []
    for n in nodes:
        ref = (n.get("provenance") or {}).get("mirror_of")
        if not ref:
            continue
        if ref not in authority:
            out.append({"code": "MIRROR_SOURCE_MISSING", "id": n.get("id"), "mirror_of": ref})
            continue
        mirrored = (n.get("props") or {}).get("state")
        current = authority[ref]
        if mirrored is not None and mirrored != current:
            out.append({"code": "MIRROR_DRIFT", "id": n.get("id"), "mirror_of": ref,
                        "graph": mirrored, "authority": current,
                        "detail": "a autoridade manda; o grafo não avança um gate sobre isto"})
    return out


# ------------------------------------------------------------------------ leitura

def read(eng: Path) -> dict:
    """O store, ou a razão exacta por que não está legível.

    Devolve sempre um dict com `status`. Só `ABSENT` autoriza modo legacy; qualquer outro
    estado é um problema a reportar, nunca «projecto sem grafo» (K07)."""
    d = store_dir(eng)
    gp, mp = d / GRAPH_FILE, d / META_FILE
    g_exists, m_exists = gp.exists(), mp.exists()

    if not g_exists and not m_exists:
        return {"status": ABSENT, "nodes": [], "edges": [], "meta": {},
                "detail": "nem `graph.jsonl` nem `meta.json`; modo legacy é legítimo"}
    if g_exists != m_exists:
        return {"status": INCOHERENT_PAIR, "nodes": [], "edges": [], "meta": {},
                "detail": "existe `{}` e falta `{}` — par incoerente, NÃO é ausência".format(
                    GRAPH_FILE if g_exists else META_FILE,
                    META_FILE if g_exists else GRAPH_FILE)}
    try:
        raw_meta = mp.read_text(encoding="utf-8")
        raw_graph = gp.read_text(encoding="utf-8")
    except OSError as exc:
        return {"status": UNREADABLE, "nodes": [], "edges": [], "meta": {},
                "detail": "{}: {}".format(type(exc).__name__, exc)}

    try:
        meta = json.loads(raw_meta)
        if not isinstance(meta, dict):
            raise ValueError("meta.json não é um objecto")
    except ValueError as exc:
        return {"status": INVALID_FORMAT, "nodes": [], "edges": [], "meta": {},
                "detail": "meta.json ilegível: {}".format(exc)}

    schema = meta.get("schema_version")
    if schema != SCHEMA_VERSION:
        return {"status": UNSUPPORTED_SCHEMA, "nodes": [], "edges": [], "meta": meta,
                "detail": "schema {} não suportado (este motor lê {})".format(
                    schema, SCHEMA_VERSION)}

    nodes, edges = [], []
    for i, line in enumerate(raw_graph.splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except ValueError as exc:
            return {"status": INVALID_FORMAT, "nodes": [], "edges": [], "meta": meta,
                    "detail": "linha {} ilegível: {}".format(i, exc)}
        kind = rec.get("kind")
        if kind == "node":
            nodes.append(rec)
        elif kind == "edge":
            edges.append(rec)
        else:
            return {"status": INVALID_FORMAT, "nodes": [], "edges": [], "meta": meta,
                    "detail": "linha {}: `kind` desconhecido {!r}".format(i, kind)}

    actual = revision_of(nodes, edges)
    if meta.get("revision") and meta["revision"] != actual:
        return {"status": INCOHERENT_PAIR, "nodes": nodes, "edges": edges, "meta": meta,
                "detail": "revisão de `meta.json` ({}) não corresponde ao grafo ({})".format(
                    str(meta.get("revision"))[:12], actual[:12])}

    return {"status": OK, "nodes": nodes, "edges": edges, "meta": meta, "revision": actual,
            "detail": ""}


def empty_store() -> dict:
    """Store válido e vazio — distinto de ausente (K01)."""
    return {"schema_version": SCHEMA_VERSION, "revision": revision_of([], []),
            "nodes": 0, "edges": 0}


# -------------------------------------------------------------- escrita (staging)

def serialize(nodes: list[dict], edges: list[dict]) -> tuple[str, str]:
    """Os bytes a publicar: `(graph.jsonl, meta.json)`. NÃO publica."""
    lines = canonical_lines(nodes, edges)
    body = "\n".join(lines) + ("\n" if lines else "")
    meta = {"schema_version": SCHEMA_VERSION, "revision": revision_of(nodes, edges),
            "nodes": len(nodes), "edges": len(edges)}
    return body, json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def stage(eng: Path, nodes: list[dict], edges: list[dict], staging: Path) -> dict:
    """Valida e escreve para STAGING. A publicação é de `operation.py` (contrato B2.4)."""
    problems = validate(nodes, edges)
    if problems:
        raise GraphError("mutação inválida — não publicada", "INTEGRITY", {"problems": problems})
    staging = Path(staging)
    staging.mkdir(parents=True, exist_ok=True)
    body, meta = serialize(nodes, edges)
    (staging / GRAPH_FILE).write_text(body, encoding="utf-8", newline="\n")
    (staging / META_FILE).write_text(meta, encoding="utf-8", newline="\n")
    return {"revision": revision_of(nodes, edges), "nodes": len(nodes), "edges": len(edges),
            "staging": str(staging)}


# ---------------------------------------------------------------------------- CLI

def _cli_status(eng: Path) -> dict:
    st = read(eng)
    return {"engagement": str(eng), "status": st["status"], "detail": st["detail"],
            "revision": st.get("revision", ""),
            "nodes": len(st["nodes"]), "edges": len(st["edges"]),
            "legacy_mode_allowed": st["status"] == ABSENT}


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="grafo do engagement (read-only na CLI)")
    ap.add_argument("command", choices=["status", "verify"])
    ap.add_argument("--engagement", required=True)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    eng = Path(a.engagement)
    if not eng.is_dir():
        eng = Path("projects") / a.engagement
    if not eng.is_dir():
        print("engagement não encontrado: {}".format(a.engagement), file=sys.stderr)
        return 2

    if a.command == "status":
        out = _cli_status(eng)
    else:
        st = read(eng)
        out = dict(_cli_status(eng),
                   integrity=validate(st["nodes"], st["edges"]) if st["status"] == OK else [])
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        for k, v in out.items():
            print("{:22} {}".format(k, v))
    if out["status"] in (UNREADABLE, INVALID_FORMAT, UNSUPPORTED_SCHEMA, INCOHERENT_PAIR):
        return 1
    if a.command == "verify" and out.get("integrity"):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
