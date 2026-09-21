#!/usr/bin/env python3
"""Gera `inventory-expected.json` e os registos de cobertura da fixture (schema v1).

    python .claude/tests/fixtures/coverage/build_fixtures.py <repo-root>

O denominador esperado deriva dos FICHEIROS da fixture, nao de uma lista escrita a mao: e
essa a propriedade que a fase 2 tem de reproduzir.

Regras do contrato que este gerador materializa:
  §4.4.4  identidade da obrigacao = sorted(set(requirement_refs)); as 6 obrigacoes da
          reconciliacao reaparecem TODAS em cada registo a jusante, excepto o que a etapa
          render declara em `not_selected`.
  §4.4    `unresolved_refs` nao vazio impede `covered`.
  §6.3    manifesto POR ETAPA, com `use: freshness | informative`. `_blueprint/` e
          `_render/` ficam fora (sao alvos); a SU e as decisoes sao `informative`.
  §6.5    os tres digests derivados levam placeholder -- a canonicalizacao e da fase 2.
  §6.1    o registo de uma aprovacao de blueprint fica FORA do inventario, por inteiro.

Isto e ferramenta de fixtures, nao o motor: `coverage.py` e da fase 2, e a fase 2
reproduz este denominador com a sua propria implementacao ou justifica a diferenca.
"""

from __future__ import annotations

import hashlib
import json
import re
import runpy
import sys
from pathlib import Path

# Importável (o teste usa `units()` sobre cópias) e executável (regenera as fixtures).
# A raiz resolve-se SEMPRE por `__file__`, nunca por `sys.argv`: este modulo e importado
# pelos testes, e um modulo que le os argumentos de quem o importa passa a depender da
# forma de execucao -- com `unittest discover`, `sys.argv[1]` e a string "discover".
# O argumento da linha de comandos existe, e e validado, mas so dentro de `main()`.
REPO = Path(__file__).resolve().parents[4]
FIXROOT = REPO / ".claude" / "tests" / "fixtures" / "coverage"
ENG = FIXROOT / "fx-coverage-f06"
RECORDS = FIXROOT / "records"
PLACEHOLDER = hashlib.sha256(b"aisa-coverage-fixture-placeholder").hexdigest()


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ----------------------------------------------------------------- inventario

def approval_ids(eng: Path) -> set[str]:
    """Os ids dos blocos de aprovacao de blueprint (contrato 6.1/6.4).

    Sao identificados POSITIVAMENTE pelo tipo que o leitor de decisoes atribui ao bloco,
    nunca pelo prefixo do id: nenhuma outra linha `D-*` sai do inventario."""
    dec = eng / "decisions.md"
    if not dec.is_file():
        return set()
    D = runpy.run_path(str(REPO / "library" / "kernel" / "tools" / "dashboard.py"))
    return {b["id"] for b in D["classify_decisions"](dec.read_text(encoding="utf-8"))
            if b["kind"] == "blueprint-approval"}


def units(eng: Path | None = None) -> list[dict]:
    """O denominador, derivado dos FICHEIROS -- nunca de uma lista escrita a mao.

    Fora do inventario, por inteiro (contrato 6.1): o registo de uma aprovacao de
    blueprint -- o bloco em `decisions.md` e a linha que o espelha na SU. Nao e material
    de origem; e o registo de uma decisao humana, lido a parte como autoridade. Se
    entrasse, acrescentar a aprovacao mudava o `inventory_sha256` e tornava stale a
    revisao que a aprovacao esta a consumir.
    """
    eng = ENG if eng is None else eng
    skip = approval_ids(eng)
    out: list[dict] = []

    def add(key, cls, note=""):
        out.append({"unit_key": key, "class": cls, "note": note})

    ctx = json.loads((eng / "context.json").read_text(encoding="utf-8"))
    for field in ("literal_request", "requester", "inputs", "funding_gate"):
        if field in ctx:
            add("context.json#" + field, "context-field")

    enq = (eng / "enquadramento.md").read_text(encoding="utf-8")
    for m in re.finditer(r"^##\s+(T\d)\s*·", enq, re.M):
        add("enquadramento.md#" + m.group(1), "enquadramento-theme")
    for mid in sorted(set(re.findall(r"\bM-\d+\b", enq))):
        add("enquadramento.md#" + mid, "invariant")

    ans = (eng / "answers.md").read_text(encoding="utf-8")
    heads: list[str] = []
    for line in ans.splitlines():
        if line.startswith("## "):
            heads.append(re.split(r"\s+—\s+|\s+--\s+", line[3:].strip())[0].strip())
    for i, h in enumerate(heads):
        n = heads[:i].count(h)
        key = "answers.md#" + h + (("[%d]" % (n + 1)) if heads.count(h) > 1 else "")
        add(key, "answer-section",
            "seccao repetida: ordinal explicito" if heads.count(h) > 1 else "")

    su = (eng / "shared-understanding.md").read_text(encoding="utf-8")
    for m in re.finditer(r"^\|\s*([A-Z]{1,2}-\d{3})\s*\|", su, re.M):
        if m.group(1) in skip:
            continue
        add("shared-understanding.md#" + m.group(1), "su-row")

    dec = (eng / "decisions.md").read_text(encoding="utf-8")
    for m in re.finditer(r"^##\s+(D-\d{3})\b", dec, re.M):
        if m.group(1) in skip:
            continue
        add("decisions.md#" + m.group(1), "decision-block")

    for p in sorted((eng / "inputs").iterdir()):
        add("inputs/" + p.name, "input-file",
            "formato fora dos tiers de captura" if p.suffix == ".pptx" else "")

    fd_name = "registo-de-lotes.xlsx.fields-draft.json"
    fd = json.loads((eng / "_capture" / fd_name).read_text(encoding="utf-8"))
    base = "_capture/" + fd_name + "#"
    for sheet in fd["sheets"]:
        for col in sheet["columns"]:
            add(base + sheet["name"] + "/" + col["column"], "xlsx-column")
    for e in fd["dictionary"]["entries_without_data"]:
        add(base + "dictionary/entries_without_data/" + e["name"],
            "xlsx-dictionary-entry", "nome sem dados: entra no denominador")

    ex_name = "registo-de-lotes-2024.xlsx.extraction.json"
    ex = json.loads((eng / "_capture" / ex_name).read_text(encoding="utf-8"))
    for sheet in ex["sheets"]:
        add("_capture/" + ex_name + "#sheets[name=" + sheet["name"] + "]", "xlsx-sheet",
            "mesmo nome de folha noutro workbook: chave distinta pelo ficheiro"
            if sheet["name"] == "Resumo Aditivos" else "")

    pm = (eng / "_capture" / "process-model.md").read_text(encoding="utf-8")
    for pid in sorted(set(re.findall(r"\bPM-U-\d{3}\b", pm))):
        add("_capture/process-model.md#" + pid, "process-question")
    for pid in sorted(set(re.findall(r"\bPM-\d{3}\b", pm))):
        add("_capture/process-model.md#" + pid, "process-rule")

    add("_capture/evidence-index.md", "capture-index")
    add("_capture/registo-de-lotes.xlsx.replay.md", "replay-report",
        "limitacoes de replay entram como limitacao, nao como facto novo")
    for name in ("frame.md", "options.md", "premortem.md"):
        add(name, "phase-artefact", "fonte auxiliar: nao cria verdade mais forte que a SU")
    for p in sorted((eng / "lens-outputs").iterdir()):
        add("lens-outputs/" + p.name, "lens-output",
            "fonte auxiliar: nao cria verdade mais forte que a SU")
    return out


# ------------------------------------------------------------------- constantes

GROUP_CUSTO = [
    "_capture/registo-de-lotes.xlsx.fields-draft.json#Entradas/F",
    "_capture/registo-de-lotes.xlsx.fields-draft.json#Entradas/G",
    "_capture/registo-de-lotes.xlsx.fields-draft.json#Entradas/H",
]
U_C007 = "answers.md#U-004"
U_C010 = "answers.md#U-009"
BP01 = "_blueprint/ux-blueprint_v01.yaml"
BP02 = "_blueprint/ux-blueprint_v02.yaml"
BP03 = "_blueprint/ux-blueprint_v03.yaml"
RD01 = "_render/fx-coverage-f06_solution-blueprint_v01.md"
RD02 = "_render/fx-coverage-f06_solution-blueprint_v02.md"
TEMPLATE = "library/packs/pp/deliverable-templates/solution-blueprint.template.md"
STORY = "_synthesis/architecture-story.md"

OUT_OF_MANIFEST = ("_coverage/", "_blueprint/", "_render/", "_synthesis/")
DERIVED = ("dashboard.html", "story.md", "council-log.md", "gate-log.md",
           "_capture/_capture-log.md")
INFORMATIVE = ("shared-understanding.md", "decisions.md")


def sources_manifest(stage: str) -> list[dict]:
    out = []
    for p in sorted(ENG.rglob("*")):
        if not p.is_file():
            continue
        r = p.relative_to(ENG).as_posix()
        if r in DERIVED or r.startswith(OUT_OF_MANIFEST):
            continue
        role = ("input" if r.startswith("inputs/")
                else "capture" if r.startswith("_capture/") else "engagement")
        use = "informative" if r in INFORMATIVE else "freshness"
        out.append({"path": r, "sha256": sha(p), "role": role, "use": use})
    if stage == "render":
        out.append({"path": STORY, "sha256": sha(ENG / STORY),
                    "role": "engagement", "use": "freshness"})
    return sorted(out, key=lambda e: e["path"])


def basis(stage: str, **over) -> dict:
    d = {
        "inventory_sha256": PLACEHOLDER,
        "su_fingerprint": PLACEHOLDER,
        "decision_fingerprint": PLACEHOLDER,
        "sources": sources_manifest(stage),
        "authorities": [],
        "decision_ref": "D-002",
        "contract_version": "1",
        "pack": "pp",
    }
    d.update(over)
    return d


# ------------------------------------------------------------------- construtores

def sr(i, refs, assessment="reviewed", materiality="material", rationale="",
       su_refs=(), items=(), limitation=None):
    e = {"id": "sr-%03d" % i, "unit_refs": list(refs), "assessment": assessment,
         "materiality": materiality,
         "rationale": rationale or "Unidade lida na passagem fonte -> destino.",
         "links": {"su_refs": list(su_refs), "coverage_items": list(items),
                   "obligations": []}}
    if limitation:
        e["limitation"] = limitation
    return e


def item(i, reqs, units_, disposition, status, rationale, targets=(),
         scope=(), accept=(), unresolved=(), action="", role=""):
    assert not (unresolved and status == "covered"), \
        "contrato 4.4: `unresolved_refs` nao vazio impede `covered`"
    e = {"id": "item-%03d" % i, "requirement_refs": list(reqs),
         "source_unit_refs": list(units_), "disposition": disposition,
         "scope_basis_refs": list(scope), "targets": list(targets),
         "assessment": {"status": status, "rationale": rationale,
                        "acceptance_basis_refs": list(accept) or list(reqs)},
         "unresolved_refs": list(unresolved)}
    if status != "covered":
        e["required_action"] = action or "Concretizar no desenho."
        e["responsible_role"] = role or "arquitetura"
    return e


def renumber(items, start=1):
    return [dict(it, id="item-%03d" % n) for n, it in enumerate(items, start)]


def tgt(file, selector, kind, role):
    return {"file": file, "selector": selector, "kind": kind, "role": role}


def semantic(status="completed", s2t=True, t2s=True, findings=(), limitations=None):
    d = {"status": status,
         "performed_by": {"kind": "agent", "name": "executor do aisa (fixture)"},
         "method": "source-to-target and target-to-source",
         "passes": {"source_to_target": s2t, "target_to_source": t2s},
         "limitations": list(limitations if limitations is not None else
                             ["Revisao documental; nao executa a solucao."]),
         "findings": list(findings)}
    if status == "completed":
        d["completed_at"] = "2026-03-10T10:00:00+01:00"
    return d


def record(version, stage, **kw):
    d = {"schema_version": 1, "version": version, "engagement": "fx-coverage-f06",
         "stage": stage, "generated_at": "2026-03-10T10:00:00+01:00",
         "based_on": [], "target": None}
    d.update(kw)
    order = ["schema_version", "version", "engagement", "stage", "generated_at",
             "based_on", "target", "deliverable", "basis", "source_review",
             "coverage", "semantic_review"]
    return {k: d[k] for k in order if k in d}


def findings_of(items):
    return [it["id"] for it in items
            if it["assessment"]["status"] in ("partial", "missing", "excluded")]


# ------------------------------------------------------------- revisoes de fonte

def full_source_review():
    """`reconciliation`: uma entrada por unidade do inventario (contrato 4.3)."""
    out, i = [], 1
    grouped = set(GROUP_CUSTO)
    for u in units():
        k = u["unit_key"]
        if k in grouped:
            continue
        mat, assess, lim, why = "material", "reviewed", None, ""
        if k == "inputs/fluxo-de-libertacao.pptx":
            assess, why = "unverifiable", "Formato fora dos tiers de captura."
            lim = {"reason": "sem extractor para .pptx",
                   "impact": "obrigacoes descritas so neste ficheiro podem nao estar no "
                             "denominador",
                   "action": "leitura humana antes de aprovar o desenho"}
        elif "Parametros/" in k:
            mat, why = "not-material", "Parametro de calculo; nao e obrigacao de negocio."
        elif u["class"] in ("phase-artefact", "lens-output", "capture-index",
                            "replay-report"):
            mat, why = "not-material", "Fonte auxiliar; nao cria obrigacao propria."
        out.append(sr(i, [k], assess, mat, why, limitation=lim))
        i += 1
    out.append(sr(i, GROUP_CUSTO, "reviewed", "not-material",
                  "Grupo de colunas de forma repetida, membros enumerados: residuo de um "
                  "estudo antigo, sem entrada em nenhum calculo (C-009).",
                  su_refs=["C-009"]))
    return out


def stage_source_review(render=False):
    """A revisao de fontes das etapas de desenho e de render. Em `render`, a obrigacao
    {C-009} e declarada em `not_selected` e NAO tem item: a entrada sr-006 nao pode ligar
    a `item-006`, que nesse registo nao existe (uma ligacao morta e uma referencia morta)."""
    """`blueprint` / `render`: so as unidades que a etapa volta a consultar (4.3)."""
    return [
        sr(1, [U_C007], "reviewed", "material",
           "Relida na passagem fonte -> destino: e a obrigacao de saida em causa.",
           su_refs=["C-007", "A-003"], items=["item-001"]),
        sr(2, ["shared-understanding.md#C-006"], "reviewed", "material",
           "Relida: a outra saida de resumo, para nao confundir os dois canais.",
           su_refs=["C-006"], items=["item-002"]),
        sr(3, ["shared-understanding.md#C-008"], "reviewed", "material",
           "Relida: C-008 nao revoga C-006 nem C-007, sao saidas distintas.",
           su_refs=["C-008"], items=["item-003"]),
        sr(4, ["enquadramento.md#M-2"], "reviewed", "material",
           "Relida: o invariante de segregacao.",
           su_refs=["C-002", "C-005"], items=["item-004"]),
        sr(5, [U_C010], "reviewed", "material",
           "Relida: a resposta que diz onde a regra e imposta.",
           su_refs=["C-010"], items=["item-005"]),
        sr(6, GROUP_CUSTO, "reviewed", "not-material",
           "Grupo de colunas de forma repetida, membros enumerados: sem entrada em "
           "calculo (C-009). Exclusao herdada da reconciliacao.",
           su_refs=["C-009"], items=([] if render else ["item-006"])),
    ]


# ------------------------------------------------------- as 6 obrigacoes, por etapa

def obligations_reconciliation():
    return [
        item(1, ["C-007"], [U_C007, "shared-understanding.md#C-007"], "preserve",
             "covered", "A obrigacao de manter a saida e o seu canal esta escrita em C-007 "
             "e a hipotese de consumidor externo ficou registada em A-003."),
        item(2, ["C-006"], ["enquadramento.md#T4"], "preserve", "covered",
             "A saida por email esta escrita em C-006."),
        item(3, ["C-008"], ["answers.md#U-006"], "preserve", "covered",
             "O contrato do ficheiro de integracao esta escrito em C-008."),
        item(4, ["C-002", "C-005"], ["enquadramento.md#M-2"], "preserve", "covered",
             "O invariante de segregacao esta em C-002 e o comportamento real em C-005."),
        item(5, ["C-010"], [U_C010], "preserve", "covered",
             "A resposta da equipa de sistemas fixou o ponto de imposicao e esta escrita "
             "em C-010."),
        item(6, ["C-009"], GROUP_CUSTO, "retire", "excluded",
             "Grupo de colunas sem entrada em calculo; a resposta do dono fechou o tema em "
             "C-009. Todas as unidades do grupo estao declaradas nao materiais, com razao.",
             scope=["C-009"], action="—", role="arquitetura"),
    ]


def obligations_blueprint(bp, c007, c010):
    """As 6 obrigacoes projectadas sobre uma versao do desenho."""
    st7, why7, tg7, un7, ac7 = c007
    st10, why10, tg10, un10, ac10 = c010
    return [
        item(1, ["C-007"], [U_C007], "preserve", st7, why7, targets=tg7,
             unresolved=un7, action=ac7, role="arquitetura"),
        item(2, ["C-006"], ["enquadramento.md#T4"], "preserve", "covered",
             "A saida por email tem componente propria.",
             targets=[tgt(bp, "architecture/compositions[component=resumo-email]",
                          "composition", "implementation")]),
        item(3, ["C-008"], ["answers.md#U-006"], "preserve", "covered",
             "O ficheiro de integracao tem componente propria, do lado de la da fronteira.",
             targets=[tgt(bp, "architecture/compositions[component=lote-export]",
                          "composition", "implementation")]),
        item(4, ["C-002", "C-005"], ["enquadramento.md#M-2"], "preserve", "covered",
             "O percurso separa quem regista de quem liberta, com accoes e visibilidade "
             "distintas por papel.",
             targets=[tgt(bp, "screens[name=LoteListScreen]", "screen", "implementation"),
                      tgt(bp, "personas[name=Libertador]", "persona", "implementation")]),
        item(5, ["C-010"], [U_C010], "preserve", st10, why10, targets=tg10,
             unresolved=un10, action=ac10, role="arquitetura"),
        item(6, ["C-009"], GROUP_CUSTO, "retire", "excluded",
             "Exclusao herdada da reconciliacao, com a mesma autoridade: colunas sem "
             "entrada em calculo, fora da UI por fundamento de desenho.",
             targets=[tgt(bp, "excluded_from_ui[0]", "section", "implementation")],
             scope=["C-009"], action="—", role="arquitetura"),
    ]


def _check_root_argument() -> None:
    """O argumento documentado (`... build_fixtures.py .`) tem de apontar para este repo."""
    if len(sys.argv) < 2:
        return
    given = Path(sys.argv[1]).resolve()
    if given != REPO:
        raise SystemExit(
            "raiz do repositorio nao corresponde: argumento {} != {} (derivada de "
            "__file__). Correr a partir da raiz do repositorio, ou sem argumento."
            .format(given, REPO))


def main() -> None:
    _check_root_argument()
    RECORDS.mkdir(parents=True, exist_ok=True)
    inv = units()
    (FIXROOT / "inventory-expected.json").write_text(json.dumps({
        "artefact": "aisa.coverage.inventory-expected",
        "contract_version": "1",
        "engagement": "fx-coverage-f06",
        "note": ("Denominador ESPERADO da fase 1, derivado dos ficheiros da fixture. A "
                 "fase 2 reproduz esta lista ou justifica a diferenca no seu relatorio. "
                 "Nao e output de motor: o motor ainda nao existe."),
        "counts_by_class": {c: sum(1 for u in inv if u["class"] == c)
                            for c in sorted({u["class"] for u in inv})},
        "total": len(inv),
        "units": inv,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("inventory-expected.json:", len(inv), "unidades")

    shas = {k: sha(ENG / v) for k, v in
            {"bp01": BP01, "bp02": BP02, "bp03": BP03, "rd01": RD01, "rd02": RD02}.items()}
    tpl_sha = sha(REPO / TEMPLATE)
    out: dict[str, dict] = {}

    # ---------------------------------------------------- v01 reconciliacao completa
    recon = obligations_reconciliation()
    out["rec-v01-reconciliation-complete.json"] = record(
        "v01", "reconciliation", basis=basis("reconciliation"),
        source_review=full_source_review(), coverage=recon,
        semantic_review=semantic(findings=findings_of(recon)))

    # ------------------------------------------------- v02 blueprint v01: a perda F06
    miss = obligations_blueprint(
        BP01,
        c007=("missing",
              "O desenho tem a entidade ResumoAditivos, e nao tem percurso nenhum de "
              "publicacao nem de consulta: nenhuma composicao, nenhum ecra e nenhum campo "
              "de entrega. Existir como entidade nao e entregar a saida.",
              [tgt(BP01, "entities[name=ResumoAditivos]", "entity", "projection")], (),
              "Concretizar a publicacao diaria e a consulta no desenho."),
        c010=("missing",
              "C-010 exige imposicao ao nivel do armazenamento. A v01 so tem a escolha em "
              "aberto; nao ha componente, campo nem obrigacao de prova que a concretize.",
              [tgt(BP01, "architecture/open_architecture_choices[su_ref=U-009]",
                   "open_architecture_choice", "open_choice")], (),
              "Desenhar o ponto de imposicao no armazenamento."))
    out["rec-v02-blueprint-missing.json"] = record(
        "v02", "blueprint", based_on=["coverage_v01.json"],
        target={"file": BP01, "kind": "blueprint", "identity": "v01",
                "sha256": shas["bp01"]},
        basis=basis("blueprint"), source_review=stage_source_review(), coverage=miss,
        semantic_review=semantic(findings=findings_of(miss)))

    # ------------------------------- v03 blueprint v02: C-007 entregue, C-010 por fechar
    partial = obligations_blueprint(
        BP02,
        c007=("covered",
              "A publicacao diaria na area partilhada e uma composicao propria, o ecra de "
              "consulta existe, e a entrega fica registada em campos com canal, local e "
              "instante. As tres pecas juntas sao o percurso que C-007 descreve.",
              [tgt(BP02, "architecture/compositions[component=resumo-aditivos-publicacao]",
                   "composition", "implementation"),
               tgt(BP02, "screens[name=ResumoAditivosConsultaScreen]", "screen",
                   "implementation"),
               tgt(BP02,
                   "architecture/record_authority[key=publicacoes]/fields[name=local_publicacao]",
                   "field", "implementation")], (), ""),
        c010=("partial",
              "A regra vive no percurso de ecras e a escolha continua em aberto no "
              "desenho: C-010 exige imposicao no armazenamento, e nenhum componente a "
              "concretiza.",
              [tgt(BP02, "architecture/open_architecture_choices[su_ref=U-009]",
                   "open_architecture_choice", "open_choice")], (),
              "Desenhar o ponto de imposicao no armazenamento e fechar a escolha."))
    out["rec-v03-blueprint-partial.json"] = record(
        "v03", "blueprint", based_on=["coverage_v01.json", "coverage_v02.json"],
        target={"file": BP02, "kind": "blueprint", "identity": "v02",
                "sha256": shas["bp02"]},
        basis=basis("blueprint"), source_review=stage_source_review(), coverage=partial,
        semantic_review=semantic(findings=findings_of(partial)))

    # ---------------------------------------- v04 blueprint v03: cobertura sem aprovacao
    complete = obligations_blueprint(
        BP03,
        c007=("covered",
              "Composicao de publicacao, ecra de consulta e campos de entrega -- o "
              "percurso completo que C-007 descreve.",
              [tgt(BP03, "architecture/compositions[component=resumo-aditivos-publicacao]",
                   "composition", "implementation"),
               tgt(BP03, "screens[name=ResumoAditivosConsultaScreen]", "screen",
                   "implementation"),
               tgt(BP03,
                   "architecture/record_authority[key=publicacoes]/fields[name=local_publicacao]",
                   "field", "implementation")], (), ""),
        c010=("covered",
              "O ponto de imposicao esta no armazenamento, com componente propria, os dois "
              "identificadores no registo e obrigacao de prova de que uma escrita directa "
              "pelo proprio registador e recusada. A escolha estrutural fechou com base "
              "declarada.",
              [tgt(BP03,
                   "architecture/compositions[component=imposicao-segregacao-no-armazenamento]",
                   "composition", "implementation"),
               tgt(BP03, "architecture/record_authority[key=lotes]/fields[name=libertado_por]",
                   "field", "implementation"),
               tgt(BP03, "architecture/proof_obligations[1]", "proof_obligation",
                   "proof_obligation")], (), ""))
    out["rec-v04-blueprint-complete.json"] = record(
        "v04", "blueprint", based_on=["coverage_v01.json", "coverage_v03.json"],
        target={"file": BP03, "kind": "blueprint", "identity": "v03",
                "sha256": shas["bp03"]},
        basis=basis("blueprint"), source_review=stage_source_review(), coverage=complete,
        semantic_review=semantic(findings=findings_of(complete)))

    # -------------------------------------------------------------- v05 render completo
    deliv = {"id": "solution-blueprint", "template": TEMPLATE, "template_sha256": tpl_sha,
             "authority_sources": ["the architecture block",
                                   "architecture-templates/architecture-core.md",
                                   "_synthesis/architecture-story.md"],
             "blueprint_version_read": "v03",
             "not_selected": [{"requirement_refs": ["C-009"],
                               "reason": "exclusao de superficie de utilizador; este "
                                         "deliverable projecta a arquitectura, nao o "
                                         "dicionario de ecras"}]}
    ren = renumber([
        item(0, ["C-007"], [U_C007], "preserve", "covered",
             "A seccao de fronteiras carrega a linha da publicacao com o que a forca.",
             targets=[tgt(RD02, "A3/resumo-aditivos-publicacao", "section", "projection")]),
        item(0, ["C-006"], ["enquadramento.md#T4"], "preserve", "covered",
             "A linha do email esta na seccao de fronteiras.",
             targets=[tgt(RD02, "A3/resumo-email", "section", "projection")]),
        item(0, ["C-008"], ["answers.md#U-006"], "preserve", "covered",
             "A linha do export esta na seccao de fronteiras.",
             targets=[tgt(RD02, "A3/lote-export", "section", "projection")]),
        item(0, ["C-002", "C-005"], ["enquadramento.md#M-2"], "preserve", "covered",
             "A seccao de identidade descreve a separacao entre os dois papeis.",
             targets=[tgt(RD02, "A7/C-002", "section", "projection")]),
        item(0, ["C-010"], [U_C010], "preserve", "covered",
             "A seccao de identidade diz onde a regra e imposta, e a de provas carrega a "
             "prova de recusa.",
             targets=[tgt(RD02, "A7/C-010", "section", "projection"),
                      tgt(RD02, "A12/acesso directo", "section", "projection")]),
    ])
    out["rec-v05-render-complete.json"] = record(
        "v05", "render", based_on=["coverage_v04.json"],
        target={"file": RD02, "kind": "deliverable",
                "identity": "solution-blueprint_v02", "sha256": shas["rd02"]},
        deliverable=deliv,
        basis=basis("render", authorities=[{"path": TEMPLATE, "sha256": tpl_sha}]),
        source_review=stage_source_review(render=True), coverage=ren,
        semantic_review=semantic(findings=findings_of(ren)))

    # ------------------------------------------------------------------- negativos
    short = full_source_review()
    dropped = next(e for e in short
                   if e["unit_refs"] == ["_capture/registo-de-lotes.xlsx.fields-draft.json"
                                         "#Resumo Aditivos/D"])
    short.remove(dropped)
    out["rec-neg-unreviewed-unit.json"] = record(
        "v06", "reconciliation", basis=basis("reconciliation"), source_review=short,
        coverage=recon, semantic_review=semantic(findings=findings_of(recon)))

    def blueprint_neg(version, first):
        body = renumber([first] + miss[1:])
        return record(version, "blueprint", based_on=["coverage_v01.json"],
                      target={"file": BP01, "kind": "blueprint", "identity": "v01",
                              "sha256": shas["bp01"]},
                      basis=basis("blueprint"), source_review=stage_source_review(),
                      coverage=body, semantic_review=semantic(findings=findings_of(body)))

    out["rec-neg-decorative-projection.json"] = blueprint_neg(
        "v07", item(0, ["C-007"], [U_C007], "preserve", "covered",
                    "A entidade ResumoAditivos cita C-007.",
                    targets=[tgt(BP01, "entities[name=ResumoAditivos]", "entity",
                                 "projection")]))
    out["rec-neg-decorative-invalid-target.json"] = blueprint_neg(
        "v08", item(0, ["C-007"], [U_C007], "preserve", "covered",
                    "Declara implementacao num componente de publicacao.",
                    targets=[tgt(BP01,
                                 "architecture/compositions"
                                 "[component=resumo-aditivos-publicacao]",
                                 "composition", "implementation")]))
    # A ref morta ACRESCENTA-SE as seis obrigacoes; substitui-las faria a fixture falhar
    # tambem por obrigacao perdida, e um codigo esconderia o outro.
    dead = renumber(miss + [
        item(0, ["C-999"], ["answers.md#U-020"], "preserve", "covered",
             "Requisito inexistente e seccao citada sem ordinal.",
             targets=[tgt(BP01, "entities[name=NaoExiste]", "entity",
                          "implementation")])])
    out["rec-neg-dead-ref.json"] = record(
        "v09", "blueprint", based_on=["coverage_v01.json"],
        target={"file": BP01, "kind": "blueprint", "identity": "v01",
                "sha256": shas["bp01"]},
        basis=basis("blueprint"), source_review=stage_source_review(), coverage=dead,
        semantic_review=semantic(findings=findings_of(dead)))
    out["rec-neg-exclusion-no-decision.json"] = blueprint_neg(
        "v10", item(0, ["C-007"], [U_C007], "retire", "excluded",
                    "Sai do ambito por decisao de desenho: as consultas sao esporadicas.",
                    scope=[], action="—", role="arquitetura"))
    out["rec-neg-exclusion-undetermined.json"] = blueprint_neg(
        "v11", item(0, ["C-007"], [], "retire", "excluded",
                    "Sai do ambito. Nenhuma unidade ligada, e portanto materialidade por "
                    "declarar.", scope=[], action="—", role="arquitetura"))

    mech = renumber([complete[5]] + complete[:5])
    out["rec-pos-exclusion-mechanical.json"] = record(
        "v12", "blueprint", based_on=["coverage_v01.json", "coverage_v03.json"],
        target={"file": BP03, "kind": "blueprint", "identity": "v03",
                "sha256": shas["bp03"]},
        basis=basis("blueprint"), source_review=stage_source_review(), coverage=mech,
        semantic_review=semantic(findings=findings_of(mech)))

    dropped_obl = renumber([it for it in miss if it["requirement_refs"] != ["C-008"]])
    out["rec-neg-obligation-dropped.json"] = record(
        "v13", "blueprint", based_on=["coverage_v01.json"],
        target={"file": BP01, "kind": "blueprint", "identity": "v01",
                "sha256": shas["bp01"]},
        basis=basis("blueprint"), source_review=stage_source_review(),
        coverage=dropped_obl,
        semantic_review=semantic(findings=findings_of(dropped_obl)))

    out["rec-neg-semantic-pending.json"] = record(
        "v14", "blueprint", based_on=["coverage_v01.json", "coverage_v03.json"],
        target={"file": BP03, "kind": "blueprint", "identity": "v03",
                "sha256": shas["bp03"]},
        basis=basis("blueprint"), source_review=stage_source_review(), coverage=complete,
        semantic_review=semantic("pending", s2t=True, t2s=False, findings=[]))

    fut = record("v15", "blueprint", based_on=["coverage_v01.json"],
                 target={"file": BP03, "kind": "blueprint", "identity": "v03",
                         "sha256": shas["bp03"]},
                 basis=basis("blueprint"), source_review=stage_source_review(),
                 coverage=complete, semantic_review=semantic())
    fut["schema_version"] = 2
    out["rec-neg-schema-future.json"] = fut

    out["rec-neg-schema-invalid.json"] = record(
        "v16", "blueprint", based_on=["coverage_v01.json"],
        target={"file": BP01, "kind": "blueprint", "identity": "v01"},
        source_review=[{"id": "sr-001", "unit_refs": [U_C007]}],
        coverage=[{"id": "item-001", "requirement_refs": ["C-007"],
                   "disposition": "preserve"}],
        semantic_review={"status": "completed"})

    out["rec-neg-stale-target.json"] = record(
        "v17", "blueprint", based_on=["coverage_v01.json"],
        target={"file": BP01, "kind": "blueprint", "identity": "v01",
                "sha256": shas["bp02"]},
        basis=basis("blueprint"), source_review=stage_source_review(), coverage=miss,
        semantic_review=semantic(findings=findings_of(miss)))

    out["rec-neg-authority-mismatch.json"] = record(
        "v18", "render", based_on=["coverage_v04.json"],
        target={"file": RD02, "kind": "deliverable",
                "identity": "solution-blueprint_v02", "sha256": shas["rd02"]},
        deliverable=dict(deliv, blueprint_version_read="v01"),
        basis=basis("render", authorities=[{"path": TEMPLATE, "sha256": tpl_sha}]),
        source_review=stage_source_review(render=True), coverage=ren,
        semantic_review=semantic(findings=findings_of(ren)))

    limited = full_source_review()
    for e in limited:
        if e["unit_refs"] == ["inputs/fluxo-de-libertacao.pptx"]:
            e["assessment"] = "not_applicable"
            e["rationale"] = "Sem extractor para este formato."
            e.pop("limitation", None)
    out["rec-neg-capture-limit-as-covered.json"] = record(
        "v19", "reconciliation", basis=basis("reconciliation"), source_review=limited,
        coverage=recon, semantic_review=semantic(findings=findings_of(recon)))

    idcomment = renumber([
        item(0, ["C-007"], [U_C007], "preserve", "covered",
             "O id aparece no documento.",
             targets=[tgt(RD01, "A3/resumo-aditivos-publicacao", "section",
                          "projection")])] + ren[1:])
    out["rec-neg-render-id-in-comment.json"] = record(
        "v20", "render", based_on=["coverage_v04.json"],
        target={"file": RD01, "kind": "deliverable",
                "identity": "solution-blueprint_v01", "sha256": shas["rd01"]},
        deliverable=dict(deliv),
        basis=basis("render", authorities=[{"path": TEMPLATE, "sha256": tpl_sha}]),
        source_review=stage_source_review(render=True), coverage=idcomment,
        semantic_review=semantic(findings=findings_of(idcomment)))

    for old in sorted(RECORDS.glob("*.json")):
        old.unlink()
    for name, rec in sorted(out.items()):
        (RECORDS / name).write_text(
            json.dumps(rec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("wrote", name)
    print("placeholder digest:", PLACEHOLDER)


if __name__ == "__main__":
    main()
