"""Frente D (P-7) — `render-validate.py` checks sufficiency BY CONTENT, not by presence.

The stub logged and validated nothing: pilot-1's spec v02 declared seven entities `keep-in-place`
with no dictionary, `(none)` under flows while two entities carry approval steps, and no
role matrix — and `render-gaps.md` said 0. The motor now executes the rules the template
declares in `sufficiency:` against the APPROVED blueprint's record and the rendered text.

    python .claude/tests/test_render_validate.py
"""

import io
import json
import runpy
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
V = runpy.run_path(str(ROOT / ".claude" / "hooks" / "render-validate.py"))

DECISIONS = """# Decisions

## D-002 — Adopt O-001
- **Chosen option**: O-001
- **Timestamp**: 2026-09-02T10:00:00Z

## D-003 — Blueprint bp-v01 aprovado
- **Timestamp**: 2026-09-08T10:00:00Z
"""

BP_COMPLETE = """version: v01
engagement: eng
decision_ref: decisions.md#D-002
draft: false
architecture:
  scope: whole solution
  authorization: authorized
  authorization_basis: "outcome sentence, verbatim (fixture)"
  architectability_basis: "PP application built from scratch (fixture)"
  experience:
    mode: owned-internal
    primary_surface: "Record-centric app (model-driven)"
  compositions: []
  relocated_responsibilities: []
  proof_obligations: []
  record_authority:
    - domain: Pedidos
      key: requests
      su_refs: [C-001]
      authority: governed relational store
      access_mode: owned
      schema_owner: {value: equipa X, state: Confirmed, su_ref: C-001}
      fields:
        - name: id
          type: identifier
          required: true
          index: primary
          state: Assumed
          source: design (A7)
        - name: estado
          type: choice
          values: [pendente, aprovado]
          required: true
          index: none
          state: Assumed
          source: design (state_machine)
    - domain: Preços
      key: prices
      su_refs: [C-057]
      authority: external system of record
      access_mode: keep-in-place
      schema_owner: {value: equipa BD, state: Assumed, su_ref: C-057, open: U-036}
      access_contract:
        reads:
          - name: Data_Lista
            type: datetime
            state: Assumed
            source: _capture/x.xlsx.fields-draft.json#Inputs/B
        writes: []
        readonly: true
        key: [data]
  open_architecture_choices: []
entities:
  - name: Pedido
    authority: requests
    su_refs: [C-001]
    state_machine:
      - pendente
      - aprovado
    approval: true
  - name: Preco
    authority: prices
    readonly: true
    su_refs: [C-001]
personas:
  - name: Analista
    su_refs: [C-001]
navigation:
  home: {Analista: S1}
screens:
  - name: S1
    type: gallery
    su_refs: [C-001]
excluded_from_ui:
  - field_or_area: "margem interna"
    reason: "sensível"
    su_refs: [C-001]
open_questions: []
validation:
  violations: []
"""

SPEC_GOOD = """# Implementation Specification — x

## 4. Entidades e estruturas de dados
| Entidade | Domínio | access_mode | Campos / Contrato |
|---|---|---|---|
| Pedido | requests | owned | id · estado |
| Preco | prices | keep-in-place | lidas (1) · escritas (0) · chave data |

## 6. Fluxos, automação e transições de estado a implementar
### Pedido — pendente → aprovado
quem transiciona: Superior · o que valida: not named · notifica: not named · dispara: not named

## 7. Integrações
| Sistema | Autenticação e custódia de segredos |
|---|---|
| BD | Entra ID por utilizador; segredos no cofre da plataforma |

## 8. Implementação de segurança e roles
| Papel | Ecrã Pedidos | Entidade Pedido |
|---|---|---|
| Analista | R/W | CREATE |
"""

SPEC_BAD = """# Implementation Specification — x

## 4. Entidades e estruturas de dados
| Entidade | Autoridade | access_mode |
|---|---|---|
| Pedido | external system of record | keep-in-place |

## 6. Fluxos e automação a implementar
`(none)` — nenhum stream registado.

## 7. Integrações
| Sistema | Direcção |
|---|---|
| BD | leitura |

## 8. Implementação de segurança e roles
A forma da matriz segue `security-craft.md` §B.
"""


def mk(tmp, bp=BP_COMPLETE, spec=SPEC_GOOD, decisions=DECISIONS, slug="eng"):
    eng = Path(tmp) / slug
    (eng / "_blueprint").mkdir(parents=True)
    (eng / "_render").mkdir()
    (eng / "_state.json").write_text(json.dumps({"engagement": slug, "pack": "pp", "phase": "decision"}), encoding="utf-8")
    (eng / "decisions.md").write_text(decisions, encoding="utf-8")
    (eng / "_blueprint" / "ux-blueprint_v01.yaml").write_text(bp, encoding="utf-8")
    rendered = eng / "_render" / "{}_implementation-spec_v01.md".format(slug)
    rendered.write_text(spec, encoding="utf-8")
    return eng, rendered


class Harness(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = self._tmp.name

    def tearDown(self):
        self._tmp.cleanup()

    def run_validate(self, eng, rendered, **kw):
        return V["validate"](eng, "implementation-spec", rendered, **kw)


class CompleteRecordPasses(Harness):

    def test_a_complete_dictionary_and_a_complete_spec_produce_no_gap(self):
        eng, rendered = mk(self.tmp)
        r = self.run_validate(eng, rendered)
        self.assertEqual(r["blueprint"], "v01")
        self.assertEqual(r["gaps"], [], r["gaps"])
        self.assertEqual(sorted(r["sufficiency_slots"]),
                         ["entities_to_create", "flows_to_implement", "integrations", "security_implementation"])

    def test_the_record_reader_descends_into_nested_lists(self):
        D = V["_load_dashboard"]()
        rec = V["read_record"](D, BP_COMPLETE)
        self.assertEqual([d["key"] for d in rec["domains"]], ["requests", "prices"])
        self.assertEqual(len(rec["domains"][0]["fields"]), 2)
        self.assertEqual(len(rec["domains"][1]["reads"]), 1)
        self.assertTrue(rec["domains"][1]["readonly"])
        self.assertTrue(rec["domains"][1]["key_nonempty"])
        self.assertEqual([(e["name"], e["authority"], e["state_machine"], e["approval"]) for e in rec["entities"]],
                         [("Pedido", "requests", True, True), ("Preco", "prices", False, False)])


class TheOldShapeFails(Harness):
    """A record without the dictionary + a spec that hides the gaps: every rule fires."""

    def _old_record(self):
        return BP_COMPLETE.replace("      key: requests\n", "").replace("      key: prices\n", "") \
            .replace("      schema_owner: {value: equipa X, state: Confirmed, su_ref: C-001}\n", "") \
            .replace("      schema_owner: {value: equipa BD, state: Assumed, su_ref: C-057, open: U-036}\n", "") \
            .split("      fields:")[0] + "    - domain: Preços\n      authority: external system of record\n      access_mode: keep-in-place\n  open_architecture_choices: []\nentities:\n  - name: Pedido\n    state_machine:\n      - pendente\n      - aprovado\n    approval: true\n  - name: Preco\n"

    def test_entities_without_authority_and_domains_without_dictionary_are_gaps(self):
        eng, rendered = mk(self.tmp, bp=self._old_record(), spec=SPEC_BAD)
        gaps = self.run_validate(eng, rendered)["gaps"]
        rules = [g["rule"] for g in gaps]
        self.assertIn("entities[].authority", rules)
        self.assertIn("record_authority[].key", rules)
        self.assertIn("owned: fields[] typed", rules)
        self.assertIn("external: access_contract", rules)
        self.assertIn("schema_owner", rules)

    def test_none_under_flows_with_an_approval_entity_is_a_gap(self):
        eng, rendered = mk(self.tmp, bp=self._old_record(), spec=SPEC_BAD)
        gaps = [g for g in self.run_validate(eng, rendered)["gaps"] if g["slot"] == "flows_to_implement"]
        self.assertEqual(len(gaps), 1)
        self.assertIn("Pedido", gaps[0]["detail"])
        self.assertEqual(gaps[0]["owner"], "implementation")

    def test_a_craft_citation_is_not_a_role_matrix(self):
        eng, rendered = mk(self.tmp, spec=SPEC_BAD)
        slots = {g["slot"] for g in self.run_validate(eng, rendered)["gaps"]}
        self.assertIn("security_implementation", slots)
        self.assertIn("integrations", slots)

    def test_a_declared_lacuna_row_satisfies_the_authority_rule(self):
        bp = BP_COMPLETE.replace("    authority: prices\n", "    authority: none — what-if efémero (U-039)\n")
        spec = SPEC_GOOD.replace("| Preco | prices | keep-in-place | lidas (1) · escritas (0) · chave data |",
                                 "| Preco | ⚠️ lacuna — entidade sem autoridade de registo — dono: architecture | | |")
        eng, rendered = mk(self.tmp, bp=bp, spec=spec)
        rules = [g["rule"] for g in self.run_validate(eng, rendered)["gaps"]]
        self.assertNotIn("entities[].authority", rules)

    def test_an_undeclared_missing_authority_is_a_gap(self):
        bp = BP_COMPLETE.replace("    authority: prices\n", "")
        eng, rendered = mk(self.tmp, bp=bp)
        gaps = [g for g in self.run_validate(eng, rendered)["gaps"] if g["rule"] == "entities[].authority"]
        self.assertEqual(len(gaps), 1)
        self.assertIn("Preco", gaps[0]["detail"])

    def test_a_named_gap_satisfies_integrations_and_a_persona_matrix_satisfies_security(self):
        spec = SPEC_GOOD.replace("| BD | Entra ID por utilizador; segredos no cofre da plataforma |",
                                 "| BD | não especificadas nesta captura — item aberto |") \
                        .replace("| Papel | Ecrã Pedidos | Entidade Pedido |", "| Persona | Vista Pedidos | Formulário |")
        eng, rendered = mk(self.tmp, spec=spec)
        self.assertEqual(self.run_validate(eng, rendered)["gaps"], [])

    def test_missing_state_or_source_on_a_line_is_a_gap(self):
        bp = BP_COMPLETE.replace("          state: Assumed\n          source: design (A7)\n", "")
        eng, rendered = mk(self.tmp, bp=bp)
        gaps = [g for g in self.run_validate(eng, rendered)["gaps"] if g["rule"] == "line: state + source"]
        self.assertEqual(len(gaps), 1)
        self.assertIn("1 linha(s)", gaps[0]["detail"])


class BackReferences(Harness):

    def test_entities_see_v01_are_read_from_v01(self):
        eng, rendered = mk(self.tmp, spec=SPEC_BAD)
        v02 = BP_COMPLETE.replace("version: v01", "version: v02").split("entities:")[0] + "entities: SEE_V01\n"
        (eng / "_blueprint" / "ux-blueprint_v02.yaml").write_text(v02, encoding="utf-8")
        dec = DECISIONS + "\n## D-004 — Blueprint bp-v02 aprovado\n- **Timestamp**: 2026-09-08T11:00:00Z\n"
        (eng / "decisions.md").write_text(dec, encoding="utf-8")
        r = self.run_validate(eng, rendered)
        self.assertEqual(r["blueprint"], "v02")
        self.assertEqual(r["record"]["entities"], 2, "entities followed SEE_V01")
        self.assertTrue(any(g["slot"] == "flows_to_implement" for g in r["gaps"]))

    def test_a_dangling_back_reference_reads_as_no_entities(self):
        D = V["_load_dashboard"]()
        rec = V["read_record"](D, "version: v03\nentities: SEE_V09\n", loader=lambda v: "")
        self.assertEqual(rec["entities"], [])


class NoApprovedBlueprint(Harness):

    def test_without_an_approval_the_record_rules_are_skipped_and_said_so(self):
        eng, rendered = mk(self.tmp, decisions=DECISIONS.split("## D-003")[0], spec=SPEC_BAD)
        r = self.run_validate(eng, rendered)
        self.assertIsNone(r["blueprint"])
        self.assertTrue(any("sem blueprint aprovado" in n for n in r["notes"]))
        self.assertEqual({g["slot"] for g in r["gaps"]}, {"security_implementation", "integrations"})

    def test_a_deliverable_without_sufficiency_rules_is_not_validated(self):
        eng, rendered = mk(self.tmp)
        r = V["validate"](eng, "executive-report", rendered)
        self.assertEqual(r["gaps"], [])
        self.assertTrue(any("sem bloco" in n for n in r["notes"]))


class HookMode(Harness):

    def _hook(self, payload):
        err = io.StringIO()
        with patch.object(sys, "stdin", io.StringIO(json.dumps(payload))), redirect_stderr(err):
            rc = V["main"]([])
        return rc, err.getvalue()

    def test_a_write_to_a_deliverable_appends_a_validation_block_and_never_blocks(self):
        eng, rendered = mk(self.tmp, spec=SPEC_BAD)
        rc, err = self._hook({"tool_name": "Write", "tool_input": {"file_path": str(rendered)}})
        self.assertEqual(rc, 0)
        self.assertIn("lacuna(s) por conteúdo", err)
        gaps_md = (eng / "_render" / "render-gaps.md").read_text(encoding="utf-8")
        self.assertIn("## Validação", gaps_md)
        self.assertIn("`render-validate.py`", gaps_md)
        self.assertIn("security_implementation", gaps_md)

    def test_a_clean_deliverable_writes_nothing(self):
        eng, rendered = mk(self.tmp)
        rc, err = self._hook({"tool_name": "Write", "tool_input": {"file_path": str(rendered)}})
        self.assertEqual(rc, 0)
        self.assertIn("0 lacunas por conteúdo", err)
        self.assertFalse((eng / "_render" / "render-gaps.md").exists())

    def test_other_writes_are_ignored(self):
        rc, err = self._hook({"tool_name": "Write", "tool_input": {"file_path": "x/shared-understanding.md"}})
        self.assertEqual((rc, err), (0, ""))
        rc, err = self._hook({"tool_name": "Read", "tool_input": {"file_path": "x/_render/a_estimate_v01.md"}})
        self.assertEqual(rc, 0)

    def test_broken_input_is_fail_open(self):
        with patch.object(sys, "stdin", io.StringIO("not json")):
            self.assertEqual(V["main"]([]), 0)


class RealPilot1(unittest.TestCase):
    """The plan's P-7 acceptance: the old v02 spec, nothing else changed, yields >= 3 required
    gaps — §4 fields, §6 flows, §8 matrix. The stub yielded 0."""

    def setUp(self):
        self.eng = ROOT / "projects" / "pricing-marinha-pilot-1"
        self.rendered = self.eng / "_render" / "pricing-marinha_implementation-spec_v02.md"
        if not self.rendered.is_file():
            self.skipTest("pilot-1 v02 not mounted")

    def test_v02_against_the_approved_v05_yields_the_three_families_of_gaps(self):
        r = V["validate"](self.eng, "implementation-spec", self.rendered)
        self.assertEqual(r["blueprint"], "v05")
        slots = {g["slot"] for g in r["gaps"]}
        self.assertGreaterEqual(len(r["gaps"]), 4)
        # Since 1.13.0 a FOURTH family appears, and it is a real finding about this
        # engagement, not a test artefact: the approved v05 fails the structural check
        # (blueprint-contract.md -> Validação estrutural) -- its record_authority items
        # carry no `key` and the keep-in-place/virtualized ones no `access_contract`
        # (both required by aisa-blueprint step 2 since P-6), and one section does not
        # parse. The content rules still run -- the structural failure is added as its
        # own gap instead of collapsing into "no approved blueprint", which would have
        # HIDDEN the three content families below.
        self.assertEqual(slots, {"blueprint", "entities_to_create", "flows_to_implement",
                                 "security_implementation"})
        structural = [g for g in r["gaps"] if g["slot"] == "blueprint"]
        self.assertEqual(len(structural), 1)
        self.assertIn("v05", structural[0]["detail"])
        self.assertIn("BP-RA-REQ", structural[0]["detail"])
        self.assertEqual(r["approved_invalid"]["version"], "v05")
        self.assertTrue(any("access_contract" in g["rule"] for g in r["gaps"]))

    def test_dry_run_writes_nothing(self):
        before = (self.eng / "_render" / "render-gaps.md").read_text(encoding="utf-8")
        out = io.StringIO()
        from contextlib import redirect_stdout
        with redirect_stdout(out):
            rc = V["main"](["--engagement", str(self.eng), "--dry-run"])
        self.assertEqual(rc, 0)
        self.assertIn("lacuna(s)", out.getvalue())
        self.assertEqual((self.eng / "_render" / "render-gaps.md").read_text(encoding="utf-8"), before)


if __name__ == "__main__":
    unittest.main(verbosity=1)
