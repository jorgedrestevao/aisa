"""Fase 1 da reconciliação/cobertura — integridade das fixtures e do contrato.

O motor (`coverage.py`) é da fase 2. Este módulo não o simula: verifica que a
ESPECIFICAÇÃO que a fase 1 entrega se mantém verdadeira e apanha as falhas
observáveis que a fariam apodrecer em silêncio —

  ancoragem    todo o selector dos registos POSITIVOS resolve num nó do desenho, da SU
               ou do deliverable da fixture; todo o selector dos registos NEGATIVOS que
               existem para não resolver continua a não resolver. Renomear uma entidade
               do blueprint parte este teste, em vez de parir uma fixture que deixou de
               provar o que diz.
  denominador  `inventory-expected.json` continua a bater certo com os ficheiros. Acrescentar
               uma coluna ao workbook sem actualizar a expectativa é uma falha.
  F06          a v01 passa a verificação estrutural do runtime com zero bloqueios E não
               tem percurso de entrega para C-007; a v02 tem. É esta a reprodução
               documental do caso de origem, e é código que a verifica.
  contrato     cada código que o README nomeia existe na tabela do contrato, e cada
               registo está na tabela do README.

    python .claude/tests/test_coverage_fixtures.py
"""

import ast
import json
import re
import runpy
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
D = runpy.run_path(str(ROOT / "library" / "kernel" / "tools" / "dashboard.py"))
FIX = Path(__file__).resolve().parent / "fixtures" / "coverage"
ENG = FIX / "fx-coverage-f06"
RECORDS = FIX / "records"
CONTRACT = (ROOT / "library" / "kernel" / "coverage-contract.md").read_text(encoding="utf-8")
README = (FIX / "README.md").read_text(encoding="utf-8")

PLACEHOLDER = "b31c2af5507500ef2272d791693f3335b4be63f86ff8a781a8436d1cc253fb81"

# Registos cujos selectors existem PARA não resolver, com o que se espera que falhe.
EXPECTED_UNRESOLVABLE = {
    "rec-neg-decorative-invalid-target.json":
        ["architecture/compositions[component=resumo-aditivos-publicacao]"],
    "rec-neg-dead-ref.json": ["entities[name=NaoExiste]"],
    "rec-neg-render-id-in-comment.json": ["A3/resumo-aditivos-publicacao"],
}
# O registo de reconciliação que fixa as obrigações herdadas por todos os outros.
BASE_RECONCILIATION = "rec-v01-reconciliation-complete.json"
# `_blueprint/` e `_render/` são ALVOS: nunca entram no manifesto de fontes (contrato §6.3).
NEVER_IN_MANIFEST = ("_blueprint/", "_render/", "_coverage/")
INFORMATIVE_PATHS = ("shared-understanding.md", "decisions.md")

# O derivador do denominador vive com as fixtures e e a expectativa executavel da fase 1.
BUILD = runpy.run_path(str(FIX / "build_fixtures.py"))

# Uma aprovacao de blueprint, tal como `aisa-blueprint` a escreveria.
APPROVAL_BLOCK = '''
## D-003 — Blueprint bp-v03 aprovado

- **Timestamp**: 2026-03-11T09:00:00+01:00
- **Validated by**: owner (Responsavel de Qualidade — fixture, via AskUserQuestion)
'''
APPROVAL_ROW = ("| D-003 | chair | Aprovação do desenho, versão 03; ver decisions.md#D-003 "
                "| decisions.md#D-003 | 2026-03-11 | organizacional | D-01 |\n")
# Registos que não são schema-válidos de propósito.
MALFORMED = {"rec-neg-schema-invalid.json", "rec-neg-schema-future.json"}

ROOT_REQUIRED = ("schema_version", "version", "engagement", "stage", "generated_at",
                 "based_on", "target", "basis", "source_review", "coverage",
                 "semantic_review")


def identity(item: dict) -> tuple:
    """Contrato §4.4.4 — a identidade da obrigação, nunca o id local do item."""
    return tuple(sorted(set(item["requirement_refs"])))


def records():
    for p in sorted(RECORDS.glob("*.json")):
        yield p.name, json.loads(p.read_text(encoding="utf-8"))


# ------------------------------------------------------------------ resolução
# Resolvedor deliberadamente pequeno: só as formas que as fixtures usam. NÃO é o motor
# da fase 2 — é o suficiente para provar que uma fixture ainda aponta para onde diz.

SEL_RE = re.compile(r"^(?P<name>[^\[/]+)(?:\[(?P<disc>[^\]]+)\])?$")


def _yaml_nodes(text: str, path: list[str]):
    """Lista de mapas na posição `path` (ex.: ['architecture', 'compositions'])."""
    if len(path) == 1:
        blk = D["yl_find_block"](text, path[0])
    else:
        blk = D["yl_find_block"](text, path[-1], path[-2])
    return D["yl_list_of_maps"](blk) if blk else []


def resolve_yaml(text: str, selector: str) -> int:
    """Quantos nós o selector selecciona. 1 = resolve; 0 ou >1 = não."""
    segs = selector.split("/")
    m = SEL_RE.match(segs[0])
    if not m:
        return 0
    container = [m.group("name")]
    disc = m.group("disc")
    if m.group("name") == "architecture" and len(segs) > 1:
        m2 = SEL_RE.match(segs[1])
        container, disc, segs = ["architecture", m2.group("name")], m2.group("disc"), segs[1:]
    nodes = _yaml_nodes(text, container)
    if disc is None:
        return 1 if nodes else 0
    if disc.isdigit():
        return 1 if int(disc) < len(nodes) else 0
    key, _, val = disc.partition("=")
    hits = [n for n in nodes
            if str(n.get(key, "")) == val
            or val in [str(x) for x in (n.get(key) or [] if isinstance(n.get(key), list) else [])]]
    if len(segs) > 1 and len(hits) == 1:
        # `record_authority[key=publicacoes]/fields[name=local_publicacao]`
        m3 = SEL_RE.match(segs[1])
        sub = hits[0].get(m3.group("name"))
        if not isinstance(sub, list):
            return 0
        k2, _, v2 = (m3.group("disc") or "").partition("=")
        return len([x for x in sub if isinstance(x, dict) and str(x.get(k2, "")) == v2])
    return len(hits)


def resolve_md(text: str, selector: str) -> int:
    """`A3` = uma secção `## A3 ...`; `A3/<token>` = uma linha dentro dela com o token."""
    head, _, row = selector.partition("/")
    m = re.search(r"^#{2,4}\s+" + re.escape(head) + r"\b.*?$(.*?)(?=^#{2,4}\s|\Z)",
                  text, re.M | re.S)
    if not m:
        return 0
    return 1 if not row else len([l for l in m.group(1).splitlines() if row in l])


def resolve_target(t: dict) -> int:
    f = ENG / t["file"]
    if not f.is_file():
        return 0
    text = f.read_text(encoding="utf-8")
    return resolve_yaml(text, t["selector"]) if f.suffix in (".yaml", ".yml") \
        else resolve_md(text, t["selector"])


# ------------------------------------------------------------------ os testes

class Engagement(unittest.TestCase):

    def test_the_fixture_engagement_has_no_coverage_directory(self):
        """Ausência de registo tem de poder dar `not_evaluated` (contrato §10)."""
        self.assertFalse((ENG / "_coverage").exists())

    def test_no_derived_artefact_leaked_into_the_fixture(self):
        """Os hooks escrevem estes por cima quando alguém usa Write/Edit na fixture."""
        for junk in ("dashboard.html", "_synthesis/_synthesis-checks.md"):
            self.assertFalse((ENG / junk).exists(),
                             junk + " voltou para a fixture — ver o aviso no README")

    def test_the_two_workbooks_share_a_sheet_name(self):
        names = []
        for f in ("registo-de-lotes.xlsx.extraction.json",
                  "registo-de-lotes-2024.xlsx.extraction.json"):
            d = json.loads((ENG / "_capture" / f).read_text(encoding="utf-8"))
            names.append({s["name"] for s in d["sheets"]})
        self.assertIn("Resumo Aditivos", names[0] & names[1])


class F06(unittest.TestCase):
    """A propriedade que justifica a fixture inteira."""

    def _validate(self, version):
        p = ENG / "_blueprint" / ("ux-blueprint_%s.yaml" % version)
        text = p.read_text(encoding="utf-8")
        rows = D["parse_su"]((ENG / "shared-understanding.md").read_text(encoding="utf-8"))[1]
        issues = D["bp_validate"](text, p.name, D["bp_pack_cfg"]("pp"),
                                  {r["id"] for r in rows}, D["bp_loader"](ENG))
        return text, issues

    def test_v01_is_structurally_valid(self):
        _text, issues = self._validate("v01")
        self.assertEqual([i for i in issues if i["severity"] == "block"], [])
        self.assertEqual(issues, [], "a v01 tem de passar limpa, como o caso real")

    def test_v01_has_no_delivery_path_for_the_requirement(self):
        """O requisito está na SU e o desenho não o entrega — a perda silenciosa."""
        text, _ = self._validate("v01")
        comps = _yaml_nodes(text, ["architecture", "compositions"])
        forced = " ".join(str(c.get("forced_by", "")) for c in comps)
        self.assertNotIn("C-007", forced)
        screens = _yaml_nodes(text, ["screens"])
        self.assertEqual([s for s in screens if "C-007" in str(s.get("su_refs", ""))], [])
        # ... e mesmo assim a entidade cita o requisito: é isso o destino decorativo.
        ents = _yaml_nodes(text, ["entities"])
        self.assertTrue([e for e in ents if "C-007" in str(e.get("su_refs", ""))])

    def test_v02_is_structurally_valid_and_delivers_it(self):
        text, issues = self._validate("v02")
        self.assertEqual([i for i in issues if i["severity"] == "block"], [])
        comps = _yaml_nodes(text, ["architecture", "compositions"])
        self.assertTrue([c for c in comps if "C-007" in str(c.get("forced_by", ""))])
        screens = _yaml_nodes(text, ["screens"])
        self.assertTrue([s for s in screens if "C-007" in str(s.get("su_refs", ""))])

    def test_f16_is_fixed(self):
        """`concretizes_decision` no ficheiro, e o leitor devolve a ligação (T36).

        Era o contrário até à fase 2: `bp_validate` aceitava as duas chaves e `bp_read`
        só procurava `decision_ref`, por isso uma ligação documental existente
        desaparecia da projecção do runtime. A fixture continua a escrever a forma que
        expunha o defeito — é isso que faz dela uma regressão."""
        text = (ENG / "_blueprint" / "ux-blueprint_v01.yaml").read_text(encoding="utf-8")
        self.assertIn("concretizes_decision", text)
        self.assertNotIn("decision_ref:", text)
        bp = D["bp_read"](ENG / "_blueprint" / "ux-blueprint_v01.yaml")
        self.assertEqual(bp["decision_ref"], "D-002")
        self.assertEqual(bp["decision_id"], "D-002")

    def test_the_other_spelling_normalises_to_the_same_id(self):
        """`decision_ref: decisions.md#D-002` e `concretizes_decision: D-002` dão o mesmo
        `decision_id` — que é o que qualquer consumidor deve comparar."""
        import shutil as _sh
        import tempfile as _tf
        with _tf.TemporaryDirectory() as tmp:
            q = Path(tmp) / "ux-blueprint_v01.yaml"
            _sh.copyfile(ROOT / ".claude" / "tests" / "fixtures" / "blueprints"
                         / "valid_min_v01.yaml", q)
            other = D["bp_read"](q)
        self.assertEqual(other["decision_ref"], "decisions.md#D-002")
        self.assertEqual(other["decision_id"], "D-002")

    def test_no_identifier_of_the_real_case_leaks_into_the_fixture(self):
        forbidden = ("BIOS", "SharePoint", "pricing-bunkers", "Marinha", "X-Author",
                     "bancas")
        for p in sorted(ENG.rglob("*")):
            if not p.is_file() or p.suffix in (".xlsx", ".xlsm"):
                continue
            body = p.read_text(encoding="utf-8", errors="replace")
            for token in forbidden:
                self.assertNotIn(token, body, "%s: %r" % (p.name, token))


class Inventory(unittest.TestCase):

    def setUp(self):
        self.inv = json.loads((FIX / "inventory-expected.json").read_text(encoding="utf-8"))
        self.keys = [u["unit_key"] for u in self.inv["units"]]

    def test_keys_are_unique(self):
        self.assertEqual(len(self.keys), len(set(self.keys)))

    def test_total_matches_the_list(self):
        self.assertEqual(self.inv["total"], len(self.keys))

    def test_every_xlsx_column_of_the_capture_is_a_unit(self):
        fd = json.loads((ENG / "_capture" /
                         "registo-de-lotes.xlsx.fields-draft.json").read_text(encoding="utf-8"))
        want = {"_capture/registo-de-lotes.xlsx.fields-draft.json#%s/%s"
                % (s["name"], c["column"])
                for s in fd["sheets"] for c in s["columns"]}
        self.assertEqual(want - set(self.keys), set())

    def test_every_su_row_is_a_unit(self):
        rows = D["parse_su"]((ENG / "shared-understanding.md").read_text(encoding="utf-8"))[1]
        want = {"shared-understanding.md#" + r["id"] for r in rows}
        self.assertEqual(want - set(self.keys), set())

    def test_every_input_file_is_a_unit_even_without_an_extractor(self):
        want = {"inputs/" + p.name for p in (ENG / "inputs").iterdir()}
        self.assertEqual(want - set(self.keys), set())
        self.assertIn("inputs/fluxo-de-libertacao.pptx", self.keys)

    def test_the_homonymous_sheets_do_not_collide(self):
        hits = [k for k in self.keys if k.endswith("#sheets[name=Resumo Aditivos]")]
        self.assertEqual(len(hits), 1)
        self.assertIn("registo-de-lotes-2024", hits[0])

    def test_the_dictionary_entry_without_data_is_in_the_denominator(self):
        self.assertTrue([k for k in self.keys if "entries_without_data/Custo_Posto_D" in k])


class Records(unittest.TestCase):

    def test_every_record_parses_and_is_listed_in_the_readme(self):
        for name, _rec in records():
            self.assertIn(name, README, name + " não está na tabela do README")

    def test_the_readme_lists_no_record_that_is_gone(self):
        on_disk = {p.name for p in RECORDS.glob("*.json")}
        for m in re.finditer(r"`(rec-[a-z0-9-]+\.json)`", README):
            self.assertIn(m.group(1), on_disk)

    def test_wellformed_records_carry_the_required_root_fields(self):
        for name, rec in records():
            if name in MALFORMED:
                continue
            for field in ROOT_REQUIRED:
                self.assertIn(field, rec, "%s sem %s" % (name, field))
            self.assertEqual(rec["schema_version"], 1, name)
            self.assertEqual(rec["engagement"], "fx-coverage-f06", name)
            self.assertIn(rec["stage"], ("reconciliation", "blueprint", "render"), name)

    def test_ids_are_unique_inside_each_record(self):
        for name, rec in records():
            for key in ("source_review", "coverage"):
                ids = [e.get("id") for e in rec.get(key, [])]
                self.assertEqual(len(ids), len(set(ids)), "%s: %s" % (name, key))

    def test_reconciliation_has_a_null_target_and_the_others_do_not(self):
        for name, rec in records():
            if name in MALFORMED:
                continue
            if rec["stage"] == "reconciliation":
                self.assertIsNone(rec["target"], name)
            else:
                self.assertIsNotNone(rec["target"], name)

    def test_only_the_three_derived_digests_use_the_placeholder(self):
        for name, rec in records():
            basis = rec.get("basis")
            if not basis:
                continue
            for field in ("inventory_sha256", "su_fingerprint", "decision_fingerprint"):
                self.assertEqual(basis[field], PLACEHOLDER, "%s.%s" % (name, field))
            for src in basis["sources"]:
                self.assertNotEqual(src["sha256"], PLACEHOLDER, name)
                self.assertRegex(src["sha256"], r"^[0-9a-f]{64}$")

    def test_byte_digests_match_the_files_they_name(self):
        import hashlib
        for name, rec in records():
            basis = rec.get("basis")
            if not basis:
                continue
            for src in basis["sources"]:
                p = ENG / src["path"]
                self.assertTrue(p.is_file(), "%s: %s" % (name, src["path"]))
                self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), src["sha256"],
                                 "%s: digest de %s desactualizado" % (name, src["path"]))

    def test_the_stale_fixture_really_names_the_wrong_digest(self):
        import hashlib
        rec = json.loads((RECORDS / "rec-neg-stale-target.json").read_text(encoding="utf-8"))
        real = hashlib.sha256((ENG / rec["target"]["file"]).read_bytes()).hexdigest()
        self.assertNotEqual(rec["target"]["sha256"], real)
        other = hashlib.sha256(
            (ENG / "_blueprint" / "ux-blueprint_v02.yaml").read_bytes()).hexdigest()
        self.assertEqual(rec["target"]["sha256"], other)

    def test_source_review_is_exhaustive_only_at_reconciliation(self):
        inv = json.loads((FIX / "inventory-expected.json").read_text(encoding="utf-8"))
        total = inv["total"]
        for name, rec in records():
            if name in MALFORMED or rec["stage"] != "reconciliation":
                continue
            covered = {u for e in rec["source_review"] for u in e["unit_refs"]}
            missing = {u["unit_key"] for u in inv["units"]} - covered
            if name == "rec-neg-unreviewed-unit.json":
                self.assertEqual(len(missing), 1, "a fixture de T05 tem de falhar por UMA")
            else:
                self.assertEqual(missing, set(), name)
                self.assertLessEqual(len(rec["source_review"]), total)


class Targets(unittest.TestCase):

    def test_positive_targets_resolve_to_exactly_one_node(self):
        for name, rec in records():
            if name in MALFORMED or name in EXPECTED_UNRESOLVABLE:
                continue
            for it in rec["coverage"]:
                for t in it["targets"]:
                    self.assertEqual(resolve_target(t), 1,
                                     "%s / %s: %s não resolve para um nó único"
                                     % (name, it["id"], t["selector"]))

    def test_negative_targets_still_fail_to_resolve(self):
        for name, selectors in EXPECTED_UNRESOLVABLE.items():
            rec = json.loads((RECORDS / name).read_text(encoding="utf-8"))
            bad = {t["selector"] for it in rec["coverage"] for t in it["targets"]
                   if resolve_target(t) != 1}
            for sel in selectors:
                self.assertIn(sel, bad,
                              "%s: %s passou a resolver — a fixture deixou de provar o "
                              "que diz" % (name, sel))

    def test_requirement_refs_resolve_except_where_the_fixture_wants_them_dead(self):
        rows = {r["id"] for r in
                D["parse_su"]((ENG / "shared-understanding.md").read_text(encoding="utf-8"))[1]}
        blocks = {b["id"] for b in
                  D["classify_decisions"]((ENG / "decisions.md").read_text(encoding="utf-8"))}
        known = rows | blocks
        for name, rec in records():
            if name in MALFORMED:
                continue
            refs = {r for it in rec["coverage"] for r in it["requirement_refs"]}
            dead = refs - known
            if name == "rec-neg-dead-ref.json":
                self.assertEqual(dead, {"C-999"}, name)
            else:
                self.assertEqual(dead, set(), name)

    def test_covered_items_carry_the_role_the_stage_requires(self):
        need = {"blueprint": "implementation", "render": "projection"}
        for name, rec in records():
            if name in MALFORMED or name.startswith("rec-neg-"):
                continue
            want = need.get(rec["stage"])
            if not want:
                continue
            for it in rec["coverage"]:
                if it["assessment"]["status"] != "covered":
                    continue
                self.assertIn(want, [t["role"] for t in it["targets"]],
                              "%s / %s: `covered` sem destino de papel %s"
                              % (name, it["id"], want))

    def test_the_decorative_fixture_has_no_implementation_role(self):
        rec = json.loads(
            (RECORDS / "rec-neg-decorative-projection.json").read_text(encoding="utf-8"))
        it = rec["coverage"][0]
        self.assertEqual(it["assessment"]["status"], "covered")
        self.assertEqual([t["role"] for t in it["targets"]], ["projection"])


class Obligations(unittest.TestCase):
    """Contrato §4.4.4 — o que atravessa etapas é a obrigação, não o id do item."""

    def setUp(self):
        base = json.loads((RECORDS / BASE_RECONCILIATION).read_text(encoding="utf-8"))
        self.inherited = {identity(it) for it in base["coverage"]}

    def test_the_reconciliation_fixes_six_obligations(self):
        self.assertEqual(len(self.inherited), 6)

    def test_every_downstream_record_treats_every_inherited_obligation(self):
        for name, rec in records():
            if name in MALFORMED or rec["stage"] == "reconciliation":
                continue
            if name == "rec-neg-obligation-dropped.json":
                continue
            here = {identity(it) for it in rec["coverage"]}
            declared = {tuple(sorted(set(n["requirement_refs"])))
                        for n in (rec.get("deliverable") or {}).get("not_selected", [])}
            lost = self.inherited - here - declared
            self.assertEqual(lost, set(),
                             "%s perdeu obrigações herdadas: %s" % (name, sorted(lost)))

    def test_the_dropped_fixture_really_drops_one(self):
        rec = json.loads((RECORDS / "rec-neg-obligation-dropped.json")
                         .read_text(encoding="utf-8"))
        here = {identity(it) for it in rec["coverage"]}
        self.assertEqual(self.inherited - here, {("C-008",)})

    def test_render_subtracts_only_by_declaring_it(self):
        seen = 0
        for name, rec in records():
            if rec.get("stage") != "render":
                continue
            seen += 1
            here = {identity(it) for it in rec["coverage"]}
            declared = {tuple(sorted(set(n["requirement_refs"])))
                        for n in rec["deliverable"]["not_selected"]}
            self.assertTrue(declared, name + ": render sem `not_selected` declarado")
            self.assertEqual(self.inherited - here - declared, set(), name)
            for n in rec["deliverable"]["not_selected"]:
                self.assertTrue(n["reason"].strip(), name + ": subtracção sem razão")
        self.assertTrue(seen)

    def test_an_inherited_exclusion_keeps_its_authority(self):
        for name, rec in records():
            if name in MALFORMED or rec["stage"] != "blueprint":
                continue
            for it in rec["coverage"]:
                if identity(it) != ("C-009",):
                    continue
                self.assertEqual(it["assessment"]["status"], "excluded", name)
                self.assertEqual(it["scope_basis_refs"], ["C-009"], name)


class Freshness(unittest.TestCase):
    """Contrato §6.3 — o manifesto por etapa não pode criar ciclos de invalidação."""

    def test_targets_are_never_in_the_source_manifest(self):
        for name, rec in records():
            basis = rec.get("basis")
            if not basis:
                continue
            for src in basis["sources"]:
                self.assertFalse(src["path"].startswith(NEVER_IN_MANIFEST),
                                 "%s: %s é um alvo e está no manifesto — produzir uma "
                                 "versão nova invalidaria a revisão da anterior"
                                 % (name, src["path"]))

    def test_su_and_decisions_are_informative_never_compared_by_bytes(self):
        for name, rec in records():
            basis = rec.get("basis")
            if not basis:
                continue
            by_path = {s["path"]: s for s in basis["sources"]}
            for path in INFORMATIVE_PATHS:
                self.assertIn(path, by_path, name)
                self.assertEqual(by_path[path]["use"], "informative",
                                 "%s: %s como `freshness` faria a própria aprovação "
                                 "invalidar a revisão" % (name, path))

    def test_every_source_declares_a_use_and_a_role(self):
        for name, rec in records():
            basis = rec.get("basis")
            if not basis:
                continue
            for src in basis["sources"]:
                self.assertIn(src["use"], ("freshness", "informative"), name)
                self.assertIn(src["role"], ("input", "capture", "engagement"), name)

    def test_the_render_stage_adds_the_synthesis_it_declares(self):
        for name, rec in records():
            if rec.get("stage") != "render":
                continue
            fresh = {s["path"] for s in rec["basis"]["sources"]
                     if s["use"] == "freshness"}
            self.assertIn("_synthesis/architecture-story.md", fresh, name)


class Materiality(unittest.TestCase):
    """Contrato §4.4.1 — desconhecer a materialidade não dispensa autoridade de âmbito."""

    def _linked(self, rec, it):
        by_unit = {}
        for e in rec["source_review"]:
            for u in e["unit_refs"]:
                by_unit[u] = e["materiality"]
        return [by_unit.get(u, "undetermined") for u in it["source_unit_refs"]]

    def test_the_accepted_mechanical_exclusion_has_every_unit_not_material(self):
        rec = json.loads((RECORDS / "rec-pos-exclusion-mechanical.json")
                         .read_text(encoding="utf-8"))
        it = next(i for i in rec["coverage"] if identity(i) == ("C-009",))
        mats = self._linked(rec, it)
        self.assertTrue(mats)
        self.assertEqual(set(mats), {"not-material"})

    def test_the_refused_exclusion_links_a_material_unit_and_has_no_authority(self):
        rec = json.loads((RECORDS / "rec-neg-exclusion-no-decision.json")
                         .read_text(encoding="utf-8"))
        it = next(i for i in rec["coverage"] if identity(i) == ("C-007",))
        self.assertEqual(it["assessment"]["status"], "excluded")
        self.assertEqual(it["scope_basis_refs"], [])
        self.assertIn("material", self._linked(rec, it))

    def test_the_undetermined_exclusion_links_nothing_at_all(self):
        rec = json.loads((RECORDS / "rec-neg-exclusion-undetermined.json")
                         .read_text(encoding="utf-8"))
        it = next(i for i in rec["coverage"] if identity(i) == ("C-007",))
        self.assertEqual(it["assessment"]["status"], "excluded")
        self.assertEqual(it["source_unit_refs"], [])
        self.assertEqual(it["scope_basis_refs"], [])

    def test_no_record_claims_covered_while_pointing_at_something_unresolved(self):
        for name, rec in records():
            if name in MALFORMED:
                continue
            for it in rec["coverage"]:
                if it["assessment"]["status"] == "covered":
                    self.assertEqual(it["unresolved_refs"], [],
                                     "%s / %s: `covered` com `unresolved_refs`"
                                     % (name, it["id"]))


class Separation(unittest.TestCase):
    """As cinco perguntas do plano ficam separadas, e as fixtures provam-no."""

    def test_the_complete_record_still_has_no_approval_on_file(self):
        rec = json.loads((RECORDS / "rec-v04-blueprint-complete.json")
                         .read_text(encoding="utf-8"))
        self.assertEqual([it for it in rec["coverage"]
                          if it["assessment"]["status"] in ("partial", "missing")], [])
        blocks = D["classify_decisions"](
            (ENG / "decisions.md").read_text(encoding="utf-8"))
        self.assertEqual([b for b in blocks if b["kind"] == "blueprint-approval"], [],
                         "a fixture ganhou uma aprovação — deixou de separar cobertura "
                         "revista de decisão humana")

    def test_the_partial_record_is_not_complete(self):
        rec = json.loads((RECORDS / "rec-v03-blueprint-partial.json")
                         .read_text(encoding="utf-8"))
        gaps = [it for it in rec["coverage"]
                if it["assessment"]["status"] in ("partial", "missing")]
        self.assertEqual([identity(it) for it in gaps], [("C-010",)],
                         "o exemplo de `gaps` deixou de ter exactamente a lacuna que diz")

    def test_only_v03_has_no_open_structural_choice(self):
        opens = {}
        for v in ("v01", "v02", "v03"):
            bp = D["bp_read"](ENG / "_blueprint" / ("ux-blueprint_%s.yaml" % v))
            opens[v] = len(bp["structural_open"])
        self.assertEqual(opens, {"v01": 1, "v02": 1, "v03": 0})

    def test_every_blueprint_version_is_structurally_valid(self):
        rows = D["parse_su"](
            (ENG / "shared-understanding.md").read_text(encoding="utf-8"))[1]
        for v in ("v01", "v02", "v03"):
            p = ENG / "_blueprint" / ("ux-blueprint_%s.yaml" % v)
            issues = D["bp_validate"](p.read_text(encoding="utf-8"), p.name,
                                      D["bp_pack_cfg"]("pp"),
                                      {r["id"] for r in rows}, D["bp_loader"](ENG))
            self.assertEqual([i for i in issues if i["severity"] == "block"], [], v)


class ApprovalDoesNotInvalidateItsOwnReview(unittest.TestCase):
    """Contrato §6.1 + §6.4 — a forma do ciclo que o plano manda cortar.

    Aprovar acrescenta um bloco a `decisions.md` e a linha que o espelha na SU. Se
    qualquer parte da base os lesse, a revisão que a aprovação está a consumir ficava
    `stale` no instante em que era usada. A §6.3 tirou-os da comparação de bytes; esta
    classe cobre a **outra** porta, a do inventário.

    **O que isto prova, e o que não prova.** Prova que o CONJUNTO DE UNIDADES não muda
    com a aprovação — que é a entrada do `inventory_sha256` (§6.5). Não calcula digest
    nenhum, não compara a base completa e não decide freshness: não há motor que o faça,
    e um digest calculado aqui seria uma segunda implementação a competir com a da fase
    2. **O T19 completo — a base inteira, manifesto e os dois fingerprints incluídos,
    com veredicto `current` — é da fase 2**, e este é o seu teste preparatório.
    """

    def _approved_copy(self, tmp: Path) -> Path:
        eng = tmp / "fx-coverage-f06"
        shutil.copytree(ENG, eng)
        dec = eng / "decisions.md"
        dec.write_text(dec.read_text(encoding="utf-8") + APPROVAL_BLOCK, encoding="utf-8")
        su = eng / "shared-understanding.md"
        body = su.read_text(encoding="utf-8")
        anchor = "| D-002 | chair |"
        self.assertIn(anchor, body)
        line_end = body.index("\n", body.index(anchor)) + 1
        su.write_text(body[:line_end] + APPROVAL_ROW + body[line_end:], encoding="utf-8")
        return eng

    def test_the_fixture_has_no_approval_to_begin_with(self):
        blocks = D["classify_decisions"](
            (ENG / "decisions.md").read_text(encoding="utf-8"))
        self.assertEqual([b["id"] for b in blocks if b["kind"] == "blueprint-approval"], [])

    def test_the_copy_really_records_an_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._approved_copy(Path(tmp))
            blocks = D["classify_decisions"](
                (eng / "decisions.md").read_text(encoding="utf-8"))
            approvals = [b for b in blocks if b["kind"] == "blueprint-approval"]
            self.assertEqual([b["id"] for b in approvals], ["D-003"])
            self.assertEqual(approvals[0]["blueprint_version"], "v03")
            rows = {r["id"] for r in D["parse_su"](
                (eng / "shared-understanding.md").read_text(encoding="utf-8"))[1]}
            self.assertIn("D-003", rows)

    def test_the_unit_set_is_unchanged_by_the_approval(self):
        before = {u["unit_key"] for u in BUILD["units"](ENG)}
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._approved_copy(Path(tmp))
            after = {u["unit_key"] for u in BUILD["units"](eng)}
        self.assertEqual(after - before, set(),
                         "a aprovação acrescentou unidades ao denominador — voltaria a "
                         "invalidar a revisão que ela própria consome")
        self.assertEqual(before - after, set())

    def test_changing_the_solution_decision_still_shows_up(self):
        """A excepção é estreita: só o registo da aprovação sai do inventário."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._approved_copy(Path(tmp))
            dec = eng / "decisions.md"
            dec.write_text(dec.read_text(encoding="utf-8").replace(
                "- **Chosen option**: O-002 — aplicação com base de dados governada",
                "- **Chosen option**: O-001 — manter a folha com procedimento escrito"),
                encoding="utf-8")
            keys = {u["unit_key"] for u in BUILD["units"](eng)}
        self.assertIn("decisions.md#D-002", keys,
                      "o bloco da decisão-solução tem de continuar no inventário")
        self.assertNotIn("decisions.md#D-003", keys)

    def test_no_other_d_row_is_dropped(self):
        keys = {u["unit_key"] for u in BUILD["units"](ENG)}
        self.assertIn("shared-understanding.md#D-002", keys)
        self.assertIn("decisions.md#D-001", keys)
        self.assertIn("decisions.md#D-002", keys)

    def test_the_committed_expectation_matches_the_derivation(self):
        """`inventory-expected.json` não pode divergir do que o derivador produz."""
        expected = json.loads((FIX / "inventory-expected.json").read_text(encoding="utf-8"))
        derived = BUILD["units"](ENG)
        self.assertEqual([u["unit_key"] for u in derived],
                         [u["unit_key"] for u in expected["units"]])
        self.assertEqual(expected["total"], len(derived))


class ExclusionDispensation(unittest.TestCase):
    """Contrato §4.4.1 + §7 — `scope_basis_refs` vazio não é, por si só, falta de autoridade."""

    def _by_unit(self, rec):
        out = {}
        for e in rec["source_review"]:
            for u in e["unit_refs"]:
                out[u] = e["materiality"]
        return out

    def test_the_mechanical_exclusion_is_authorized_by_dispensation(self):
        rec = json.loads((RECORDS / "rec-pos-exclusion-mechanical.json")
                         .read_text(encoding="utf-8"))
        it = next(i for i in rec["coverage"] if identity(i) == ("C-009",))
        mats = [self._by_unit(rec).get(u, "undetermined") for u in it["source_unit_refs"]]
        self.assertEqual(set(mats), {"not-material"})
        for e in rec["source_review"]:
            if e["unit_refs"] == it["source_unit_refs"]:
                self.assertTrue(e["rationale"].strip(),
                                "a dispensa exige razão escrita por unidade")

    def test_the_contract_states_the_dispensation_in_the_aggregate_rule(self):
        tail = CONTRACT[CONTRACT.index("## 7. Resultado computado"):]
        head = tail[:tail.index("## 8.")]
        self.assertIn("dispensa", head,
                      "a regra agregada não reconhece a dispensa da §4.4.1")
        self.assertIn("legitimamente **vazio**", head)

    def test_the_contract_keeps_the_inventory_exclusion_narrow(self):
        self.assertRegex(CONTRACT, r"outra linha `D-[*]` sai")


class BuildersAreImportable(unittest.TestCase):
    """Regressão: um módulo importável não pode ler os argumentos de quem o importa.

    `build_fixtures.py` resolvia a raiz do repositório por `sys.argv[1]`. Importado por
    `unittest discover`, `sys.argv[1]` é a string "discover", a raiz passava a ser
    `<cwd>/discover`, e quatro testes desta suite falhavam **consoante a forma de
    execução** — verdes em execução directa, vermelhos em discovery.
    """

    BUILDERS = ("build_fixtures.py", "build_workbooks.py")

    def _import_with_argv(self, name, argv):
        real = sys.argv
        try:
            sys.argv = argv
            return runpy.run_path(str(FIX / name))
        finally:
            sys.argv = real

    def test_the_root_is_the_repository_whatever_argv_says(self):
        for name in self.BUILDERS:
            for argv in (["prog"],
                         ["prog", "discover"],
                         ["prog", "-m", "unittest", "discover"],
                         ["prog", str(Path.home())]):
                mod = self._import_with_argv(name, argv)
                self.assertEqual(mod["REPO"], ROOT,
                                 "%s com argv=%r resolveu a raiz para %s"
                                 % (name, argv, mod["REPO"]))

    def test_no_builder_reads_argv_at_module_level(self):
        """A leitura de `sys.argv` vive dentro de uma função, nunca no corpo do módulo.

        Lido pela árvore sintáctica, não por procura de texto: um comentário que explique
        a regra não é uma violação dela."""
        for name in self.BUILDERS:
            tree = ast.parse((FIX / name).read_text(encoding="utf-8"))
            for node in tree.body:                       # só o nível do módulo
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    continue
                for sub in ast.walk(node):
                    if (isinstance(sub, ast.Attribute) and sub.attr == "argv"
                            and isinstance(sub.value, ast.Name) and sub.value.id == "sys"):
                        self.fail("%s lê sys.argv no corpo do módulo, linha %d"
                                  % (name, sub.lineno))

    def test_the_derivation_works_the_same_under_discovery(self):
        """O caso concreto que falhava: `units()` precisa do leitor de decisões."""
        mod = self._import_with_argv("build_fixtures.py", ["prog", "discover"])
        keys = {u["unit_key"] for u in mod["units"](ENG)}
        self.assertIn("decisions.md#D-002", keys)
        self.assertEqual(len(keys), len(BUILD["units"](ENG)))


class Contract(unittest.TestCase):

    def test_the_contract_declares_exactly_how_far_it_is_wired(self):
        """Fase 5 ligou a terceira etapa: `render` deixou de estar por ligar.

        Antes da fase 4 o cabeçalho dizia «contrato em implementação»; na fase 4 dizia
        «activo no desenho, pendente nos deliverables». Um contrato que descreve um estado
        de ligação diferente do real é o defeito que este teste existe para apanhar — em
        qualquer das duas direcções, e é por isso que a asserção muda com cada fase."""
        head = CONTRACT[:CONTRACT.index("## 1. O que a cobertura")]
        self.assertIn("activo nas três etapas", head)
        self.assertIn("fase 5", head)
        self.assertNotIn("pendente nos deliverables", head)
        self.assertNotIn("nada disto está ligado ao runtime", head)
        # Ligado não é decidir: o cabeçalho tem de continuar a dizer o que a cobertura
        # NÃO passa a fazer, senão «ligado» lê-se como «manda».
        self.assertIn("verifica, não redefine", head)
        self.assertIn("not_evaluated", CONTRACT)

    def test_every_code_named_in_the_readme_exists_in_the_contract(self):
        for code in sorted(set(re.findall(r"\bCOV-[A-Z-]+\b", README))):
            self.assertIn("| `%s` |" % code, CONTRACT, code + " não está na tabela")

    def test_every_contract_code_is_exercised_or_deferred(self):
        codes = set(re.findall(r"^\|\s*`(COV-[A-Z-]+)`\s*\|", CONTRACT, re.M))
        self.assertTrue(codes)
        # `COV-NO-REVIEW`, `COV-STALE`, `COV-UNEXPECTED` e `COV-REVIEW-INCOMPLETE` são
        # estados do motor, não conteúdo de um registo: exercitam-se pela ausência ou
        # pela mutação, nas fases 2-3.
        by_fixture = set(re.findall(r"\bCOV-[A-Z-]+\b", README))
        deferred = {"COV-NO-REVIEW", "COV-UNEXPECTED", "COV-SCHEMA", "COV-STALE"}
        self.assertEqual(codes - by_fixture - deferred, set())

    def test_the_contract_pins_what_covered_requires_per_stage(self):
        self.assertIn("role: implementation", CONTRACT)
        self.assertIn("role: projection", CONTRACT)
        self.assertIn("`COV-MISSING-TARGET`", CONTRACT)

    def test_the_contract_forbids_writing_upstream(self):
        self.assertIn("não escreve na Shared Understanding", CONTRACT)
        self.assertIn("não altera `D-nnn`", CONTRACT)


if __name__ == "__main__":
    unittest.main(verbosity=2)
