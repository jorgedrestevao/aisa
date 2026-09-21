"""Endurecimento do runtime, bloco A — o parser YAML do kernel e a verificação estrutural.

Três camadas de prova (plano §4 A2), e são deliberadamente distintas:

  compatibilidade  o snapshot de `bp_read` em b81d39c sobre os blueprints reais, menos as
                   diferenças justificadas uma a uma (fixtures/blueprints/snapshot-diff-*.json).
                   Um diff que não esteja na lista é regressão.
  correcção        equivalência entre formas: a mesma informação em lista inline (Y2) e em
                   lista de bloco (Y3), em mapa de fluxo (Y5) e em mapa de bloco (Y6), com os
                   campos por qualquer ordem, dá o MESMO dicionário. O snapshot não prova isto:
                   provaria apenas que continuamos a ler o que já líamos, erros incluídos.
  fronteira        cada forma fora do subconjunto declarado dispara o seu código, e cada um
                   dos 25 códigos tem uma fixture que o dispara e uma que não.

O defeito de origem (revisão externa 2026-09-10, ponto 2): um item cujo `su_refs` vinha em
lista de bloco era lido como DOIS itens -- o primeiro perdia as referências e o flag
`structural`, o segundo nascia do id. `test_the_reported_defect_is_gone` é esse caso.

    python .claude/tests/test_blueprint_yaml.py
"""

import json
import os
import runpy
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
D = runpy.run_path(str(ROOT / "library" / "kernel" / "tools" / "dashboard.py"))
FIX = Path(__file__).resolve().parent / "fixtures" / "blueprints"
VALID = (FIX / "valid_min_v01.yaml").read_text(encoding="utf-8")
SU_IDS = {"C-001", "C-002", "C-003", "A-001", "U-001"}


def choices(text: str):
    """`open_architecture_choices` as the motor reads them inside `architecture`."""
    block = D["yl_find_block"](text, "open_architecture_choices", "architecture") \
        or D["yl_find_block"](text, "open_architecture_choices")
    return D["yl_list_of_maps"](block)


def validate(text, name="ux-blueprint_v01.yaml", su_ids=SU_IDS, cfg=None, loader=None):
    return D["bp_validate"](text, name, cfg or {}, su_ids, loader)


def codes(text, **kw):
    return sorted({i["code"] for i in validate(text, **kw)})


def blocking(text, **kw):
    return sorted({i["code"] for i in validate(text, **kw) if i["severity"] == "block"})


def swap(section: str, old: str, new: str) -> str:
    assert section.count(old) == 1, "âncora não única: " + old[:60]
    return section.replace(old, new)


# --------------------------------------------------------------- Y1: escalares

class Scalars(unittest.TestCase):
    """YAML 1.2 para o nulo; `none` é TEXTO -- é o valor headless de experience.mode e o
    leitor antigo transformava-o em None, deixando o campo vazio e o enum por cumprir."""

    def test_only_null_tilde_and_empty_are_null(self):
        for raw in ("null", "Null", "NULL", "~", ""):
            self.assertIsNone(D["yl_scalar"](raw), raw)

    def test_none_is_text_not_null(self):
        self.assertEqual(D["yl_scalar"]("none"), "none")
        self.assertEqual(D["yl_scalar"]("None"), "none".replace("none", "None"))

    def test_a_headless_blueprint_reads_its_mode(self):
        text = VALID.replace("    mode: owned-internal\n"
                             "    primary_surface: \"Record-centric app (model-driven)\"",
                             "    mode: none\n    primary_surface: null")
        self.assertEqual(D["yl_scalar_at"](text, "mode", "experience"), "none")
        self.assertIsNone(D["yl_scalar_at"](text, "primary_surface", "experience"))
        self.assertNotIn("BP-ENUM", codes(text))
        self.assertNotIn("BP-SURFACE", codes(text))

    def test_booleans_keep_yaml_1_1(self):
        # the step-2 template writes `funded: yes|no`; dropping yes/no would be a second
        # correction with no defect behind it.
        for raw in ("true", "True", "yes", "on"):
            self.assertIs(D["yl_scalar"](raw), True, raw)
        for raw in ("false", "no", "off"):
            self.assertIs(D["yl_scalar"](raw), False, raw)

    def test_quotes_always_win(self):
        self.assertEqual(D["yl_scalar"]('"none"'), "none")
        self.assertEqual(D["yl_scalar"]("'null'"), "null")
        self.assertEqual(D["yl_scalar"]('"true"'), "true")

    def test_ints_and_text(self):
        self.assertEqual(D["yl_scalar"]("6"), 6)
        self.assertEqual(D["yl_scalar"]("-2"), -2)
        self.assertEqual(D["yl_scalar"]("v06"), "v06")


# ------------------------------------------------------- Y2..Y7: formas e equivalência

class Forms(unittest.TestCase):

    def test_the_reported_defect_is_gone(self):
        """Revisão externa 2026-09-10, ponto 2: um item com `su_refs` em bloco lia-se
        como dois, o primeiro sem referências nem flag estrutural."""
        text = """architecture:
  open_architecture_choices:
    - choice: Choose authentication
      su_refs:
        - U-001
      structural: true
      resolved: false
"""
        got = choices(text)
        self.assertEqual(len(got), 1)
        self.assertEqual(got[0]["choice"], "Choose authentication")
        self.assertEqual(got[0]["su_refs"], ["U-001"])
        self.assertIs(got[0]["structural"], True)
        self.assertIs(got[0]["resolved"], False)

    def test_inline_and_block_lists_are_equivalent(self):
        inline = """architecture:
  open_architecture_choices:
    - choice: c
      su_refs: [U-001, C-002]
      structural: true
      would_be_settled_by: w
"""
        block = """architecture:
  open_architecture_choices:
    - choice: c
      su_refs:
        - U-001
        - C-002
      structural: true
      would_be_settled_by: w
"""
        self.assertEqual(choices(inline), choices(block))

    def test_flow_and_block_maps_are_equivalent(self):
        flow = """architecture:
  record_authority:
    - domain: d
      schema_owner: {value: equipa, state: Assumed, su_ref: A-001}
"""
        blk = """architecture:
  record_authority:
    - domain: d
      schema_owner:
        value: equipa
        state: Assumed
        su_ref: A-001
"""
        f = D["yl_list_of_maps"](D["yl_find_block"](flow, "record_authority", "architecture"))
        b = D["yl_list_of_maps"](D["yl_find_block"](blk, "record_authority", "architecture"))
        self.assertEqual(f, b)
        self.assertEqual(f[0]["schema_owner"]["su_ref"], "A-001")

    def test_field_order_does_not_change_the_reading(self):
        one = """architecture:
  open_architecture_choices:
    - choice: c
      structural: true
      su_refs: [U-001]
      would_be_settled_by: w
"""
        two = """architecture:
  open_architecture_choices:
    - would_be_settled_by: w
      su_refs: [U-001]
      structural: true
      choice: c
"""
        self.assertEqual(choices(one), choices(two))

    def test_nested_block_maps_of_any_depth(self):
        text = """architecture:
  record_authority:
    - domain: d
      access_contract:
        confidentiality:
          row_level:
            value: por unidade
            state: Confirmed
            su_ref: C-003
"""
        it = D["yl_list_of_maps"](D["yl_find_block"](text, "record_authority", "architecture"))[0]
        self.assertEqual(it["access_contract"]["confidentiality"]["row_level"]["value"],
                         "por unidade")

    def test_block_scalar_as_the_first_pair_keeps_the_sibling_keys(self):
        """A regressão histórica: `- choice: >` dobrava structural/would_be_settled_by/
        su_ref para dentro do texto (snapshot-diff-justified.md, regra Y7-in-Y4)."""
        text = """architecture:
  open_architecture_choices:
    - choice: >
        uma escolha escrita
        em duas linhas
      structural: true
      would_be_settled_by: "confirmação do IT"
      su_ref: U-001
"""
        got = choices(text)
        self.assertEqual(len(got), 1)
        self.assertEqual(got[0]["choice"], "uma escolha escrita em duas linhas")
        self.assertIs(got[0]["structural"], True)
        self.assertEqual(got[0]["su_ref"], "U-001")

    def test_a_scalar_item_becomes_value(self):
        text = "architecture:\n  open_architecture_choices:\n    - U-001\n"
        self.assertEqual(choices(text), [{"_value": "U-001"}])


# ------------------------------------------------------------------ fronteira

class Boundary(unittest.TestCase):

    def _wrap(self, snippet):
        return VALID.replace("open_questions: [U-001]", snippet)

    def test_anchor_alias_and_tag_are_signalled_not_read(self):
        for raw in ("&base x", "*base", "!!str x"):
            v = D["yl_scalar"](raw)
            self.assertIsInstance(v, D["YlUnsupported"], raw)

    def test_nested_flow_mapping_is_outside_the_subset(self):
        self.assertIsInstance(D["yl_scalar"]("{a: {b: c}}"), D["YlUnsupported"])
        self.assertIn("BP-YAML-UNSUPPORTED", blocking(self._wrap("open_questions: {a: {b: c}}")))

    def test_a_tab_indent_is_malformed_and_the_rest_still_reads(self):
        text = VALID.replace("open_questions: [U-001]", "open_questions:\n\t- U-001")
        self.assertIn("BP-YAML-MALFORMED", blocking(text))
        # the architecture block is still read: tolerance is the point of this parser
        self.assertEqual(D["yl_scalar_at"](text, "authorization", "architecture"), "authorized")

    def test_a_document_that_is_not_a_map_is_unreadable(self):
        iss = validate("- a\n- b\n")
        self.assertEqual([i["code"] for i in iss], ["BP-YAML-MALFORMED"])

    def test_a_second_document_is_signalled(self):
        self.assertIn("BP-YAML-UNSUPPORTED", blocking(VALID + "\n---\nversion: 2\n"))


# ------------------------------------------------------- 25 códigos: dispara / não dispara

class Codes(unittest.TestCase):
    """Cada código com a fixture que o dispara e a prova de que a válida não o dispara."""

    def test_the_reference_fixture_is_clean(self):
        self.assertEqual(validate(VALID), [])

    def test_req_key_absent_top_level(self):
        text = VALID.replace("personas:\n  - name: Analista\n    label: \"Analista\"\n"
                             "    rbac_group: analistas\n    su_refs: [C-001]\n", "")
        self.assertIn("BP-REQ-KEY", blocking(text))

    def test_advised_keys_are_warn_not_block(self):
        text = VALID.replace("open_questions: [U-001]\n", "")
        iss = [i for i in validate(text) if i["code"] == "BP-REQ-KEY"]
        self.assertEqual([i["severity"] for i in iss], ["warn"])

    def test_pack_required_keys_add_to_the_kernel_list(self):
        self.assertNotIn("BP-REQ-KEY", codes(VALID))
        self.assertIn("BP-REQ-KEY", blocking(VALID, cfg={"required_keys": ["migration"]}))

    def test_type_null_is_not_empty(self):
        self.assertIn("BP-TYPE", blocking(swap(VALID, "open_questions: [U-001]",
                                                "open_questions: null")))

    def test_type_text_where_a_list_belongs(self):
        self.assertIn("BP-TYPE", blocking(swap(VALID, "open_questions: [U-001]",
                                                "open_questions: qualquer coisa")))

    def test_an_empty_list_is_affirmative_and_does_not_fire(self):
        self.assertEqual(validate(swap(VALID, "open_questions: [U-001]",
                                       "open_questions: []")), [])

    def test_a_see_back_reference_is_a_valid_container(self):
        # real versions write `screens: SEE_V01 + export_features (ver v04)`
        text = VALID[:VALID.index("screens:")] + \
            "screens: SEE_V01 + export_features\nexcluded_from_ui: SEE_V01\n" + \
            VALID[VALID.index("open_questions:"):]
        self.assertNotIn("BP-TYPE", codes(text))

    def test_arch_req_missing_scalar_and_missing_list(self):
        self.assertIn("BP-ARCH-REQ", blocking(swap(VALID, "  scope: whole solution\n", "")))
        self.assertIn("BP-ARCH-REQ", blocking(swap(VALID, "  relocated_responsibilities: []\n", "")))

    def test_enum_values(self):
        self.assertIn("BP-ENUM", blocking(swap(VALID, "authorization: authorized",
                                               "authorization: maybe")))
        self.assertIn("BP-ENUM", blocking(swap(VALID, "      access_mode: owned",
                                               "      access_mode: borrowed")))
        self.assertIn("BP-ENUM", blocking(swap(VALID, "      level: V2", "      level: V9")))
        self.assertIn("BP-ENUM", blocking(swap(VALID, "      boundary: outside-platform",
                                               "      boundary: sideways")))

    def test_surface_both_ways(self):
        headless_with_surface = swap(VALID, "    mode: owned-internal", "    mode: none")
        self.assertIn("BP-SURFACE", blocking(headless_with_surface))
        no_surface = swap(VALID, '    primary_surface: "Record-centric app (model-driven)"\n', "")
        self.assertIn("BP-SURFACE", blocking(no_surface))

    def test_composition_required_fields_and_duplicates(self):
        self.assertIn("BP-COMP-REQ", blocking(swap(VALID, "      pattern: data-virtualization\n", "")))
        dup = swap(VALID, "  relocated_responsibilities: []",
                   "    - component: sql-history\n"
                   "      pattern: direct\n"
                   "      forced_by: x\n"
                   "      boundary: in-platform\n"
                   "  relocated_responsibilities: []")
        self.assertIn("BP-COMP-REQ", blocking(dup))

    def test_record_authority_key_contract_and_duplicates(self):
        self.assertIn("BP-RA-REQ", blocking(swap(VALID, "      key: pedidos\n", "")))
        no_contract = swap(VALID, "      access_contract:\n", "      other:\n")
        self.assertIn("BP-RA-REQ", blocking(no_contract))

    def test_access_contract_empty_key_needs_an_open_question(self):
        self.assertIn("BP-AC-KEY", blocking(swap(VALID, "        key: [id]", "        key: []")))
        with_open = swap(VALID, "        key: [id]", "        key: []\n        open: U-001")
        self.assertNotIn("BP-AC-KEY", codes(with_open))

    def test_relocated_responsibility_fields(self):
        text = swap(VALID, "  relocated_responsibilities: []",
                    "  relocated_responsibilities:\n    - responsibility: r\n      owner: o")
        self.assertIn("BP-RR-REQ", blocking(text))

    def test_provenance_missing_on_a_node(self):
        text = swap(VALID, "  - name: PedidoListScreen\n    type: gallery\n    entity: Pedido\n"
                           "    personas: [Analista]\n    su_refs: [C-001]\n",
                    "  - name: PedidoListScreen\n    type: gallery\n    entity: Pedido\n"
                    "    personas: [Analista]\n")
        self.assertIn("BP-NO-SUREFS", blocking(text))

    def test_singular_su_ref_is_equivalent_to_plural(self):
        text = swap(VALID, "    rbac_group: analistas\n    su_refs: [C-001]",
                    "    rbac_group: analistas\n    su_ref: C-001")
        self.assertNotIn("BP-NO-SUREFS", codes(text))

    def test_an_action_without_provenance_is_a_gap(self):
        text = swap(VALID, "      - {name: aprovar, kind: primary, su_refs: [C-002]}",
                    "      - {name: aprovar, kind: primary}")
        self.assertIn("BP-NO-SUREFS", blocking(text))

    def test_leaf_without_su_ref_is_a_warning(self):
        text = swap(VALID, "          primary_key_type: {value: int, state: Confirmed, su_ref: C-003}",
                    "          primary_key_type: {value: int, state: Confirmed}")
        self.assertIn("BP-LEAF-NO-SUREF", codes(text))
        self.assertNotIn("BP-LEAF-NO-SUREF", blocking(text))

    def test_bad_and_dead_ids_are_warnings(self):
        self.assertIn("BP-BAD-ID", codes(swap(VALID, "    su_refs: [C-001]\n\nentities:",
                                              "    su_refs: [banana]\n\nentities:")))
        self.assertIn("BP-DEAD-ID", codes(swap(VALID, "    su_refs: [C-001]\n\nentities:",
                                               "    su_refs: [C-999]\n\nentities:")))

    def test_dead_id_is_not_evaluated_without_an_engagement(self):
        text = swap(VALID, "    su_refs: [C-001]\n\nentities:", "    su_refs: [C-999]\n\nentities:")
        self.assertNotIn("BP-DEAD-ID", codes(text, su_ids=None))

    def test_structural_missing_blocks(self):
        text = swap(VALID, "      structural: false\n", "")
        self.assertIn("BP-STRUCT-MISSING", blocking(text))

    def test_structural_wrong_type_blocks(self):
        self.assertIn("BP-STRUCT-TYPE", blocking(swap(VALID, "      structural: false",
                                                      "      structural: maybe")))

    def test_structural_true_needs_what_would_settle_it(self):
        text = swap(VALID, "      structural: false\n      would_be_settled_by: \"sessão com os analistas\"\n",
                    "      structural: true\n")
        self.assertIn("BP-STRUCT-NO-SETTLE", blocking(text))

    def test_resolved_type_and_closure_basis(self):
        self.assertIn("BP-RESOLVED-TYPE", blocking(swap(VALID, "      resolved: false",
                                                        "      resolved: sim")))
        text = swap(VALID, "      structural: false\n", "      structural: true\n")
        text = swap(text, "      resolved: false", "      resolved: true")
        self.assertIn("BP-RESOLVED-NO-BASIS", blocking(text))
        with_basis = swap(text, "      resolved: true",
                          "      resolved: true\n      closure_basis: \"medição B, spike de 2026-09\"")
        self.assertNotIn("BP-RESOLVED-NO-BASIS", codes(with_basis))

    def test_proof_obligation_fields_are_warnings(self):
        text = swap(VALID, "      owner: developer\n", "")
        self.assertIn("BP-PO-REQ", codes(text))
        self.assertNotIn("BP-PO-REQ", blocking(text))

    def test_draft_is_never_approvable(self):
        self.assertIn("BP-DRAFT", blocking(swap(VALID, "draft: false", "draft: true")))

    def test_version_must_match_the_file_name(self):
        self.assertIn("BP-VERSION", blocking(VALID, name="ux-blueprint_v02.yaml"))

    def test_nested_split_symptom_is_flagged(self):
        text = swap(VALID, "  open_architecture_choices:\n",
                    "  open_architecture_choices:\n    - U-001\n")
        self.assertIn("BP-NESTED-SPLIT", codes(text))

    # --- os quatro buracos que a revisão do bloco A encontrou (2026-09-10) ---------
    # Partilhavam a mesma forma: uma verificação que se auto-desligava perante o valor
    # errado e devolvia "sem problemas" para uma versão que nunca chegou a ser verificada.

    def _replace_choices(self, replacement: str) -> str:
        head = VALID[:VALID.index("  open_architecture_choices:")]
        tail = VALID[VALID.index("\npersonas:"):]
        return head + replacement + tail

    def test_a_scalar_item_where_a_mapping_belongs_blocks(self):
        text = self._replace_choices('  open_architecture_choices: ["missing classification"]\n')
        self.assertIn("BP-ITEM-TYPE", blocking(text))

    def test_a_scalar_composition_blocks(self):
        old = ('  compositions:\n'
               '    - component: sql-history\n'
               '      pattern: data-virtualization\n'
               '      forced_by: "C-003 — histórico já reside em SQL"\n'
               '      boundary: outside-platform\n'
               '      owner: "equipa que opera a BD"\n')
        text = swap(VALID, old, '  compositions: ["missing component"]\n')
        self.assertIn("BP-ITEM-TYPE", blocking(text))

    def test_a_null_item_blocks_too(self):
        text = swap(VALID, "  relocated_responsibilities: []",
                    "  relocated_responsibilities:\n    -")
        self.assertIn("BP-ITEM-TYPE", blocking(text))

    def test_an_enum_with_the_wrong_type_is_a_wrong_value(self):
        # `authorization: true` used to slip through: the enum only ran on text.
        for bad in ("true", "6"):
            self.assertIn("BP-ENUM", blocking(swap(VALID, "  authorization: authorized",
                                                   "  authorization: " + bad)), bad)
        self.assertIn("BP-ENUM", blocking(swap(VALID, "    mode: owned-internal",
                                               "    mode: true")))

    def _architecture_ref(self, ref: str) -> str:
        return (VALID[:VALID.index("architecture:")] + "architecture: " + ref + "\n"
                + VALID[VALID.index("\npersonas:"):])

    def test_an_unresolvable_architecture_reference_blocks(self):
        iss = [i for i in validate(self._architecture_ref("SEE_V99"))
               if i["severity"] == "block"]
        self.assertEqual([i["code"] for i in iss], ["BP-TYPE"])
        self.assertIn("não foi verificada", iss[0]["message"])

    def test_a_resolvable_architecture_reference_is_validated_at_the_target(self):
        ref = self._architecture_ref("SEE_V01")
        self.assertEqual(blocking(ref, loader=lambda v: VALID if v == "v01" else ""), [])
        broken = swap(VALID, "      structural: false\n", "")
        self.assertIn("BP-STRUCT-MISSING",
                      blocking(ref, loader=lambda v: broken if v == "v01" else ""))

    def test_a_null_architecture_blocks(self):
        text = (VALID[:VALID.index("architecture:")] + "architecture:\n"
                + VALID[VALID.index("\npersonas:"):])
        self.assertIn("BP-TYPE", blocking(text))

    def test_every_documented_code_has_a_severity(self):
        contract = (ROOT / "library" / "kernel" / "blueprint-contract.md").read_text(encoding="utf-8")
        for code in D["BP_SEVERITY"]:
            self.assertIn(code, contract, code + " sem linha no contrato")


# ------------------------------------------------------------- compatibilidade

class Snapshot(unittest.TestCase):
    """b81d39c vs agora, sobre os blueprints reais. Diferenças só as justificadas."""

    def setUp(self):
        f = FIX / "snapshot-b81d39c.json"
        j = FIX / "snapshot-diff-justified.json"
        if not f.is_file() or not j.is_file():
            self.skipTest("snapshot ausente")
        self.snap = json.loads(f.read_text(encoding="utf-8"))["blueprints"]
        self.just = {(r["file"], r["key"], r["item"])
                     for r in json.loads(j.read_text(encoding="utf-8"))["justified"]}

    def test_no_unjustified_difference(self):
        missing = [f for f in self.snap if not (ROOT / f).is_file()]
        if missing:
            self.skipTest("engagements não montados")
        bad = []
        for f, old in self.snap.items():
            new = json.loads(json.dumps(D["bp_read"](ROOT / f), default=str))
            for k, ov in old.items():
                nv = new.get(k)
                if nv == ov:
                    continue
                if isinstance(ov, list) and isinstance(nv, list) and len(ov) == len(nv):
                    for i, (o, n) in enumerate(zip(ov, nv)):
                        if o != n and (f, k, i) not in self.just:
                            bad.append((f, k, i))
                elif (f, k, None) not in self.just:
                    bad.append((f, k, None))
        self.assertEqual(bad, [], "diferenças fora da lista justificada")

    def test_the_justified_list_explains_each_entry(self):
        md = (FIX / "snapshot-diff-justified.md").read_text(encoding="utf-8")
        self.assertIn("Y7-in-Y4", md)
        for f, k, _i in self.just:
            self.assertIn(k, md)

    def test_the_f16_alias_cannot_move_any_value_in_this_snapshot(self):
        """F16 contra o snapshot, sem precisar dos engagements montados.

        O `test_no_unjustified_difference` acima **salta** neste checkout: `projects/` é
        um ponto de montagem para um repositório privado e os 12 ficheiros não estão cá.
        Um teste saltado não prova nada — mas a pergunta que ele responderia tem resposta
        aqui, e é uma resposta por construção:

        a correcção F16 mudou `decision_ref` de `yl_scalar_at("decision_ref")` para
        `yl_scalar_at("decision_ref") or yl_scalar_at("concretizes_decision")`. O `or`
        **só chega ao segundo termo quando o primeiro é vazio**. O snapshot registou um
        `decision_ref` NÃO VAZIO para os 12 ficheiros, logo o primeiro termo era
        verdadeiro em todos, logo o segundo nunca é avaliado, logo o valor não pode ter
        mudado. E `decision_id` é chave nova: a comparação percorre as chaves do
        snapshot, por isso uma chave que ele não tem não gera diferença nenhuma.

        Fica dito o que isto **não** prova: se um daqueles engagements ganhar, amanhã, um
        desenho sem `decision_ref`, o snapshot terá de ser refeito de qualquer maneira."""
        empty = [f for f, v in self.snap.items() if not v.get("decision_ref")]
        self.assertEqual(empty, [],
                         "estes ficheiros têm `decision_ref` vazio no snapshot; para "
                         "eles o alias F16 PODE mudar o valor e a diferença tem de ser "
                         "justificada: %s" % empty)
        self.assertNotIn("decision_id", set().union(*(set(v) for v in self.snap.values())),
                         "o snapshot não conhece `decision_id`, e é por isso que a chave "
                         "nova não pode gerar diferença")

    def test_the_alias_only_fires_when_the_primary_key_is_absent(self):
        """A outra metade da mesma prova, esta executável: o comportamento do leitor."""
        both = "version: v01\ndecision_ref: decisions.md#D-002\nconcretizes_decision: D-009\n"
        alias = "version: v01\nconcretizes_decision: D-002\n"
        with tempfile.TemporaryDirectory() as tmp:
            a = Path(tmp) / "ux-blueprint_v01.yaml"
            a.write_text(both, encoding="utf-8")
            read = D["bp_read"](a)
            self.assertEqual(read["decision_ref"], "decisions.md#D-002",
                             "com `decision_ref` presente, o valor CRU não se mexe")
            self.assertEqual(read["decision_id"], "D-002")
            a.write_text(alias, encoding="utf-8")
            read = D["bp_read"](a)
            self.assertEqual(read["decision_ref"], "D-002",
                             "sem `decision_ref`, o alias entra — era o defeito F16")
            self.assertEqual(read["decision_id"], "D-002")


# --------------------------------------------------- aprovação inválida a jusante

class ApprovedInvalid(unittest.TestCase):
    """A4.5: uma aprovação registada sobre uma versão que falha a estrutura é história,
    não licença. Os quatro consumidores reagem, e nenhum deles a consome em silêncio."""

    DECISIONS = ("# Decisions\n\n## D-002 — Adopt O-001\n- **Chosen option**: O-001\n"
                 "- **Timestamp**: 2026-09-02T10:00:00Z\n\n"
                 "## D-003 — Blueprint bp-v01 aprovado\n- **Timestamp**: 2026-09-08T10:00:00Z\n")

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.eng = Path(self.tmp.name) / "fx"
        (self.eng / "_blueprint").mkdir(parents=True)
        (self.eng / "_state.json").write_text(json.dumps(
            {"engagement": "fx", "pack": "pp", "phase": "decision", "round": "D-01"}),
            encoding="utf-8")
        (self.eng / "decisions.md").write_text(self.DECISIONS, encoding="utf-8")
        (self.eng / "shared-understanding.md").write_text("# SU\n", encoding="utf-8")

    def _write(self, text):
        (self.eng / "_blueprint" / "ux-blueprint_v01.yaml").write_text(text, encoding="utf-8")
        return D["classify_decisions"](self.DECISIONS)

    def test_a_valid_approval_is_consumable(self):
        blocks = self._write(VALID)
        bp = D["blueprint_state"](self.eng, blocks, [], "pp")
        self.assertTrue(bp["approved"]["valid"])
        self.assertIs(bp["approved_valid"], True)

    def test_an_invalid_approval_is_flagged_not_hidden(self):
        blocks = self._write(swap(VALID, "      structural: false\n", ""))
        bp = D["blueprint_state"](self.eng, blocks, [], "pp")
        self.assertIsNotNone(bp["approved"])          # the record survives -- it is history
        self.assertFalse(bp["approved"]["valid"])
        self.assertIs(bp["approved_valid"], False)
        self.assertIn("BP-STRUCT-MISSING", bp["versions"][0]["issue_codes"])

    def test_the_authority_stamp_refuses_an_invalid_version(self):
        self._write(swap(VALID, "      structural: false\n", ""))
        import io
        from contextlib import redirect_stdout, redirect_stderr
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            rc = D["main"](["--engagement", str(self.eng), "--authority-stamp"])
        self.assertEqual(rc, 5)
        self.assertIn("INVALID", out.getvalue())
        self.assertIn("BP-STRUCT-MISSING", err.getvalue())

    def test_a_valid_version_stamps_normally(self):
        self._write(VALID)
        import io
        from contextlib import redirect_stdout, redirect_stderr
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            rc = D["main"](["--engagement", str(self.eng), "--authority-stamp"])
        self.assertEqual(rc, 0)
        self.assertNotIn("INVALID", out.getvalue())
        self.assertIn("authority: _blueprint/ux-blueprint_v01.yaml#architecture", out.getvalue())


# ------------------------------------------------------------------------ CLI

class Cli(unittest.TestCase):

    def test_exit_0_when_valid_and_4_when_blocking(self):
        import io
        from contextlib import redirect_stdout, redirect_stderr
        with tempfile.TemporaryDirectory() as tmp:
            good = Path(tmp) / "ux-blueprint_v01.yaml"
            good.write_text(VALID, encoding="utf-8")
            out = io.StringIO()
            with redirect_stdout(out), redirect_stderr(io.StringIO()):
                rc = D["main"](["--blueprint-check", str(good)])
            self.assertEqual(rc, 0)
            self.assertIn("valid: yes", out.getvalue())
            self.assertIn("BP-DEAD-ID not evaluated", out.getvalue())

            bad = Path(tmp) / "ux-blueprint_v02.yaml"
            bad.write_text(swap(VALID, "draft: false", "draft: true"), encoding="utf-8")
            out = io.StringIO()
            with redirect_stdout(out), redirect_stderr(io.StringIO()):
                rc = D["main"](["--blueprint-check", str(bad)])
            self.assertEqual(rc, 4)
            self.assertIn("BP-DRAFT", out.getvalue())

    def test_a_missing_file_is_loud(self):
        import io
        from contextlib import redirect_stderr
        err = io.StringIO()
        with redirect_stderr(err):
            rc = D["main"](["--blueprint-check", "does-not-exist.yaml"])
        self.assertEqual(rc, 3)


# ----------------------------------------------------------------------- hook

class Hook(unittest.TestCase):

    def _run(self, payload):
        import io
        import subprocess
        return subprocess.run(
            ["python", str(ROOT / ".claude" / "hooks" / "blueprint-validate.py")],
            input=json.dumps(payload), text=True, capture_output=True,
            encoding="utf-8", errors="replace", cwd=str(ROOT))

    def test_it_reports_and_never_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "_blueprint"
            d.mkdir(parents=True)
            f = d / "ux-blueprint_v01.yaml"
            f.write_text(swap(VALID, "draft: false", "draft: true"), encoding="utf-8")
            r = self._run({"tool_name": "Write", "tool_input": {"file_path": str(f)}})
            self.assertEqual(r.returncode, 0)
            self.assertIn("BP-DRAFT", r.stderr)

    def test_a_clean_version_is_silent(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "_blueprint"
            d.mkdir(parents=True)
            f = d / "ux-blueprint_v01.yaml"
            f.write_text(VALID, encoding="utf-8")
            r = self._run({"tool_name": "Write", "tool_input": {"file_path": str(f)}})
            self.assertEqual(r.returncode, 0)
            self.assertEqual(r.stderr.strip(), "")

    def test_other_writes_and_broken_input_are_ignored(self):
        r = self._run({"tool_name": "Write", "tool_input": {"file_path": "notes.md"}})
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stderr.strip(), "")


# ------------------------------------------------------------------- wiring

class Wiring(unittest.TestCase):

    def test_the_hook_is_wired(self):
        st = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
        cmds = [h["command"] for e in st["hooks"]["PostToolUse"] for h in e["hooks"]]
        # Por FORMA, nao pela frase: a maneira de invocar mudou em R7
        # (`python "${CLAUDE_PROJECT_DIR:-.}/..."`, DEF-P1-02).
        self.assertTrue(any("blueprint-validate.py" in c for c in cmds), cmds)

    def test_hooks_md_documents_it(self):
        md = (ROOT / ".claude" / "hooks" / "HOOKS.md").read_text(encoding="utf-8")
        self.assertIn("`blueprint-validate.py`", md)

    def test_the_skill_names_the_check_at_write_and_at_approval(self):
        md = (ROOT / ".claude" / "skills" / "aisa-blueprint" / "SKILL.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(md.count("--blueprint-check"), 2)

    def test_every_pack_declares_the_blueprint_block(self):
        for pack in ("pp", "generic", "outsystems", "mendix"):
            p = ROOT / "library" / "packs" / pack / "pack.yaml"
            if not p.is_file():
                continue
            self.assertIn("\nblueprint:", p.read_text(encoding="utf-8"), pack)

    def test_the_motor_version_moved(self):
        self.assertEqual(D["TOOL_VERSION"], "1.14.0")


if __name__ == "__main__":
    unittest.main(verbosity=2)
