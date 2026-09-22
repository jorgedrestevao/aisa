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


# Campos espelhados que MOVEM O GATE. `gate_open` consome-os por `omitted_critical`:
# `state` e `resolved` decidem se a linha continua aberta, `criticidade` decide se ela
# bloqueia. Desvio em qualquer um muda o que o sistema acha que o impede de avançar.
GATE_FIELDS = ("state", "criticidade", "resolved")

# Espelhados que NÃO movem o gate. Reportam-se — o desvio existe e diz-se — mas não fecham
# nada: uma correcção de redacção na SU não muda decisão nenhuma.
INFO_FIELDS = ("text",)


def drift(nodes: list[dict], authority: dict, fields=None) -> list[dict]:
    """Campos espelhados que já não batem com a sua autoridade (K05).

    `authority` mapeia `<id do SU>` → `{campo: valor actual}`. A forma antiga — o valor
    escalar, que era o `state` — continua a ser aceite e lida como `{"state": valor}`, para
    que um chamador anterior signifique exactamente o mesmo.

    Divergência é REPORTADA; o grafo não prevalece nem se auto-corrige. O que muda com o
    código do achado é quem decide o gate, e essa decisão é de quem consome:

      `MIRROR_DRIFT`          campo que move o gate — bloqueia
      `MIRROR_DRIFT_INFO`     campo que não o move — diz-se, não bloqueia
      `MIRROR_SOURCE_MISSING` o grafo afirma o que a autoridade já não diz — bloqueia
    """
    alvo = tuple(fields) if fields else GATE_FIELDS
    out = []
    for n in nodes:
        ref = (n.get("provenance") or {}).get("mirror_of")
        if not ref:
            continue
        if ref not in authority:
            out.append({"code": "MIRROR_SOURCE_MISSING", "id": n.get("id"), "mirror_of": ref,
                        "detail": "o grafo espelha uma linha que a autoridade já não tem"})
            continue
        valores = authority[ref]
        if not isinstance(valores, dict):
            valores = {"state": valores}          # forma antiga: o escalar era o `state`
        props = n.get("props") or {}
        for campo in alvo + INFO_FIELDS:
            if campo not in props or campo not in valores:
                continue
            espelhado, actual = props.get(campo), valores.get(campo)
            if espelhado == actual:
                continue
            bloqueia = campo in alvo
            out.append({
                "code": "MIRROR_DRIFT" if bloqueia else "MIRROR_DRIFT_INFO",
                "id": n.get("id"), "mirror_of": ref, "field": campo,
                "graph": espelhado, "authority": actual,
                "detail": ("a autoridade manda; o grafo não avança um gate sobre isto"
                           if bloqueia else
                           "a autoridade manda; este campo não move o gate, mas diverge")})
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


# ---------------------------------------------------------------- inspecção (E04)
#
# Percorrer, exportar e abrir proveniência. TUDO read-only e TUDO derivado do que está
# escrito: nenhuma função desta secção inventa um nó, uma aresta ou uma raiz para tornar o
# grafo visualmente conectado. Componentes separados são reportados como separados —
# `ACCEPTANCE.md` §7 exige-o por escrito. Contexto parcial é legítimo desde que declare a
# fronteira e o export dê acesso ao resto.


def neighbours(edges: list[dict], node_id: str) -> dict:
    """Arestas que tocam `node_id`, por sentido. Não toca em nós; não confirma que existem."""
    out = [e for e in edges if e.get("src") == node_id]
    inc = [e for e in edges if e.get("dst") == node_id]
    return {"out": sorted(out, key=_edge_key), "in": sorted(inc, key=_edge_key)}


def traverse(nodes: list[dict], edges: list[dict], start: str, depth: int | None = None,
             rels: tuple | None = None) -> dict:
    """Navegação a partir de `start`, em ambos os sentidos, até `depth` saltos.

    Navegar é seguir o que existe. Uma ponta que não corresponde a nenhum nó (o
    `EDGE_END_UNKNOWN` que `validate` reporta) é devolvida em `dangling`, NUNCA materializada
    como nó. Com `depth` a limitar, `truncated` fica a `True` e `frontier` diz exactamente o
    que ficou por abrir — quem quiser o resto chama `export`.
    """
    known = {n.get("id") for n in nodes if n.get("id")}
    if start not in known:
        return {"start": start, "found": False, "reached": [], "edges": [], "dangling": [],
                "truncated": False, "frontier": [], "depth": depth,
                "detail": "nó inexistente — não se inventa para dar resposta"}

    keep = set(rels) if rels else None
    reached, walked, dangling = {start}, [], set()
    frontier, nivel = [start], 0
    while frontier:
        if depth is not None and nivel >= depth:
            break
        seguinte = []
        for nid in frontier:
            viz = neighbours(edges, nid)
            for e in viz["out"] + viz["in"]:
                if keep is not None and e.get("rel") not in keep:
                    continue
                if e not in walked:
                    walked.append(e)
                outro = e.get("dst") if e.get("src") == nid else e.get("src")
                if not outro:
                    continue
                if outro not in known:
                    dangling.add(outro)
                elif outro not in reached:
                    reached.add(outro)
                    seguinte.append(outro)
        frontier = seguinte
        nivel += 1

    por_abrir = sorted(frontier)
    return {"start": start, "found": True, "reached": sorted(reached),
            "edges": sorted(walked, key=_edge_key), "dangling": sorted(dangling),
            "truncated": bool(por_abrir), "frontier": por_abrir, "depth": depth,
            "detail": ("contexto parcial: {} nós por abrir, `export` dá o resto".format(
                len(por_abrir)) if por_abrir else "")}


def components(nodes: list[dict], edges: list[dict]) -> list[list[str]]:
    """Componentes fracamente ligados, REAIS. Dois componentes ficam dois (E04)."""
    known = {n.get("id") for n in nodes if n.get("id")}
    vistos: set = set()
    saida = []
    for nid in sorted(known):
        if nid in vistos:
            continue
        t = traverse(nodes, edges, nid)
        grupo = [x for x in t["reached"] if x in known]
        vistos.update(grupo)
        saida.append(sorted(grupo))
    return sorted(saida, key=lambda g: (-len(g), g[0] if g else ""))


PROV_SOURCE_KEYS = ("mirror_of", "locator", "source", "answered_by")


def provenance(nodes: list[dict], edges: list[dict], node_id: str) -> dict:
    """Abre a proveniência de um nó: de onde veio e a que autoridade responde.

    Sem proveniência, diz-se sem proveniência. A ausência é um facto sobre o grafo, não um
    buraco a tapar com um valor plausível.
    """
    alvo = next((n for n in nodes if n.get("id") == node_id), None)
    if alvo is None:
        return {"id": node_id, "found": False, "detail": "nó inexistente"}
    prov = alvo.get("provenance") or {}
    ligacoes = [{"key": k, "value": prov[k]} for k in PROV_SOURCE_KEYS
                if prov.get(k) not in (None, "")]
    return {"id": node_id, "found": True, "type": alvo.get("type", ""),
            "provenance": prov, "sources": ligacoes,
            "authority": prov.get("mirror_of", ""),
            "has_provenance": bool(prov),
            "edges": neighbours(edges, node_id),
            "detail": "" if prov else "nó sem proveniência declarada"}


def export(nodes: list[dict], edges: list[dict]) -> dict:
    """O grafo inteiro na forma canónica — o acesso ao resto quando o contexto foi parcial."""
    linhas = canonical_lines(nodes, edges)
    return {"revision": revision_of(nodes, edges), "nodes": len(nodes), "edges": len(edges),
            "lines": linhas, "body": "\n".join(linhas) + ("\n" if linhas else "")}


def inspect(eng: Path, start: str | None = None, depth: int | None = None) -> dict:
    """Vista de inspecção do store de um engagement — o que E04 percorre.

    Não decide nada. Se o store não estiver legível, devolve a razão e mais nada: um grafo
    ilegível não se resume, declara-se.
    """
    st = read(eng)
    if st["status"] != OK:
        return {"status": st["status"], "detail": st["detail"], "inspectable": False}
    nodes, edges = st["nodes"], st["edges"]
    comps = components(nodes, edges)
    saida = {"status": OK, "inspectable": True, "revision": st["revision"],
             "nodes": len(nodes), "edges": len(edges),
             "integrity": validate(nodes, edges),
             "components": comps, "component_count": len(comps),
             "types": sorted({str(n.get("type", "")) for n in nodes}),
             "relations": sorted({str(e.get("rel", "")) for e in edges})}
    if start:
        saida["traversal"] = traverse(nodes, edges, start, depth)
        saida["provenance"] = provenance(nodes, edges, start)
    return saida


# ------------------------------------------------- dependencia consumida (C04/C05)

CONSUMED_PATH = "_graph#consumed"


def dependency_fingerprint(nodes: list[dict], edges: list[dict], consumed) -> str:
    """Digest canonico do subconjunto do grafo que uma revisao REALMENTE consumiu.

    Contrato C4: «Relacoes novas no grafo podem servir navegacao sem mudar a base Coverage.
    Se uma relacao exclusivamente no grafo passar a sustentar a avaliacao, acrescentar ao
    contrato uma dependencia explicita e fingerprint canonico do subconjunto efectivamente
    consumido.»

    `consumed` e o conjunto de ids de no e de chaves de aresta (`src|rel|dst`) que a revisao
    declarou consumir. O que nao esta la NAO entra — e por isso que acrescentar uma aresta
    so de navegacao nao torna nada stale (C04), e mudar uma aresta consumida torna (C05).

    Reordenar entrada nao muda o digest: `canonical_lines` ja ordena (C02)."""
    want = set(consumed or ())
    n = [x for x in nodes if x.get("id") in want]
    e = [x for x in edges
         if "{}|{}|{}".format(x.get("src"), x.get("rel"), x.get("dst")) in want]
    body = "\n".join(canonical_lines(n, e))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def as_coverage_source(nodes: list[dict], edges: list[dict], consumed) -> dict:
    """A dependencia do grafo como FONTE do `basis` do coverage.

    Entra pelo mesmo caminho que qualquer outra fonte `use: freshness`, por isso
    `coverage.check_freshness` compara-a sem saber que e um grafo — e sem segunda definicao
    de «a base mudou». Uma revisao que nao consome grafo nenhum nao leva esta entrada."""
    return {"path": CONSUMED_PATH, "use": "freshness",
            "sha256": dependency_fingerprint(nodes, edges, consumed),
            "consumed": sorted(set(consumed or ()))}


# -------------------------------------------------------------- escrita (staging)

def serialize(nodes: list[dict], edges: list[dict]) -> tuple[str, str]:
    """Os bytes a publicar: `(graph.jsonl, meta.json)`. NÃO publica."""
    lines = canonical_lines(nodes, edges)
    body = "\n".join(lines) + ("\n" if lines else "")
    meta = {"schema_version": SCHEMA_VERSION, "revision": revision_of(nodes, edges),
            "nodes": len(nodes), "edges": len(edges)}
    return body, json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_set(nodes: list[dict], edges: list[dict]) -> dict:
    """O conjunto de escrita para `operation.run()` — caminhos relativos ao engagement.

    É esta a porta que os escritores de negócio usam (P4): valida, e devolve bytes para o
    coordenador publicar. Não toca no disco. `stage()` abaixo é a variante de ensaio, para
    quem quer inspeccionar os bytes sem publicar; o coordenador tem o seu próprio staging e
    não consome o de `stage()`."""
    problems = validate(nodes, edges)
    if problems:
        raise GraphError("mutação inválida — não publicada", "INTEGRITY", {"problems": problems})
    body, meta = serialize(nodes, edges)
    return {"{}/{}".format(STORE_DIR, GRAPH_FILE): body,
            "{}/{}".format(STORE_DIR, META_FILE): meta}


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
    ap.add_argument("command", choices=["status", "verify", "inspect", "export"])
    ap.add_argument("--engagement", required=True)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--start", help="no de partida para percorrer (inspect)")
    ap.add_argument("--depth", type=int, help="saltos maximos; sem isto vai ate ao fim")
    a = ap.parse_args(argv)

    eng = Path(a.engagement)
    if not eng.is_dir():
        eng = Path("projects") / a.engagement
    if not eng.is_dir():
        print("engagement não encontrado: {}".format(a.engagement), file=sys.stderr)
        return 2

    if a.command == "status":
        out = _cli_status(eng)
    elif a.command == "inspect":
        out = inspect(eng, a.start, a.depth)
    elif a.command == "export":
        st = read(eng)
        if st["status"] != OK:
            print("grafo ilegivel ({}): {}".format(st["status"], st["detail"]),
                  file=sys.stderr)
            return 1
        print(export(st["nodes"], st["edges"])["body"], end="")
        return 0
    else:
        st = read(eng)
        out = dict(_cli_status(eng),
                   integrity=validate(st["nodes"], st["edges"]) if st["status"] == OK else [])
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        for k, v in out.items():
            print("{:22} {}".format(k, v))
    if out.get("status") in (UNREADABLE, INVALID_FORMAT, UNSUPPORTED_SCHEMA, INCOHERENT_PAIR):
        return 1
    if a.command == "verify" and out.get("integrity"):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
