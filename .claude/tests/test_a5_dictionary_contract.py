"""Frente D (P-6 / P-7) — the data dictionary lives in A5 of the architecture record.

Contract side of frente D, frozen here so a later edit cannot quietly undo it:

- `architecture-core.md` A5 names the two sub-blocks (`fields[]` for `owned`,
  `access_contract` for external), the per-line `state` + `source`, the `key` join with
  `entities[].authority`, and the §4 lacuna form (step-9d §1.2 finding 2).
- the blueprint contract and the `aisa-blueprint` skill carry the same schema, invoke the
  motor (`fields_draft.py`) and require a disposition per column (principle 10).
- the Implementation Specification sources §4 from the record's dictionary, cites the draft
  locator as provenance only, writes the counts the Estimate cites, and declares the P-7
  `sufficiency:` rules `render-validate.py` will check by content.
- the architecture-story template carries the dictionary table and the authority stamp.

    python .claude/tests/test_a5_dictionary_contract.py
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "library" / "packs" / "pp"


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


CORE = read("library/packs/pp/architecture-templates/architecture-core.md")
SKILL = read(".claude/skills/aisa-blueprint/SKILL.md")
CONTRACT = read("library/kernel/blueprint-contract.md")
SPEC = read("library/packs/pp/deliverable-templates/implementation-spec.template.md")
STORY = read("library/kernel/synthesis-templates/architecture-story.template.md")
ESTIMATE = read("library/packs/pp/deliverable-templates/estimate.template.md")

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


def frontmatter(text):
    return yaml.safe_load(text.split("---", 2)[1])


class CoreA5(unittest.TestCase):

    def test_two_sub_blocks_exclusive_by_access_mode(self):
        a5 = CORE.split("### A5")[1].split("### A6")[0]
        self.assertIn("`owned` → `fields[]`", a5)
        self.assertIn("`keep-in-place` | `virtualized` → `access_contract`", a5)
        self.assertIn("`replicated` leva ambos", a5)

    def test_every_line_carries_state_and_source(self):
        a5 = CORE.split("### A5")[1].split("### A6")[0]
        self.assertIn("Toda a linha de `fields` / `reads` / `writes` carrega `state`", a5)
        self.assertIn("`source` (locator", a5)
        self.assertIn("`default` nunca é inferido", a5)

    def test_key_joins_entities_and_the_gap_form_is_named(self):
        a5 = CORE.split("### A5")[1].split("### A6")[0]
        self.assertIn("`entities[].authority`", a5)
        self.assertIn("⚠️ lacuna — entidade sem autoridade de registo", a5)
        self.assertIn("nunca preenchida por analogia", a5)
        self.assertIn("render-gaps.md", a5)

    def test_the_draft_comes_from_the_motor_and_needs_a_disposition(self):
        a5 = CORE.split("### A5")[1].split("### A6")[0]
        self.assertIn("fields_draft.py", a5)
        self.assertIn("`ADOPT` / `MAP` / `DISMISS", a5)
        self.assertIn("aisa-blueprint` step 4", a5)

    def test_the_older_a5_guarantees_survive(self):
        for must in ("No persisted record authority introduced",
                     "Missing evidence is never an empty set", "open_architecture_choices"):
            self.assertIn(must, CORE)

    def test_no_service_limit_literal_in_the_dictionary_paragraphs(self):
        a5 = CORE.split("### A5")[1].split("### A6")[0]
        self.assertNotRegex(a5, r"\b1[\s.,]?000\b", "A5 owns no service limit (contract rule 6)")


class BlueprintSideOfTheContract(unittest.TestCase):

    def test_schema_block_carries_the_dictionary(self):
        for must in ("key: <slug único no scope>", "schema_owner: {value, state:",
                     "fields:\n", "access_contract:\n", "dictionary_entries_without_data",
                     "store_facts: {primary_key_type", "readonly: true|false"):
            self.assertIn(must, SKILL, must)
        self.assertIn("access_mode: owned | virtualized | replicated | keep-in-place", SKILL)

    def test_step_4_invokes_the_motor_and_disposes_every_column(self):
        step4 = SKILL.split("4. **Compile the domain view")[1].split("5. **Run the consolidation")[0]
        self.assertIn("fields_draft.py --engagement <slug> --log", step4)
        self.assertIn("`authority: <record_authority[].key>`", step4)
        for tok in ("`ADOPT`", "`MAP`", "`DISMISS — <razão>`"):
            self.assertIn(tok, step4)
        self.assertIn("No column of the draft is left without a disposition", step4)

    def test_hard_rule_nine_freezes_state_and_source(self):
        self.assertIn("9. **The dictionary is drafted by the motor and judged here — never remembered.**", SKILL)
        self.assertIn("`default` is never inferred", SKILL)

    def test_blueprint_contract_entities_carry_authority(self):
        row = [ln for ln in CONTRACT.splitlines() if ln.startswith("| `entities` |")][0]
        self.assertIn("**`authority`**", row)
        self.assertIn("`record_authority[].key`", row)
        self.assertIn("`none — <reason>`", row)


class ImplementationSpecSection4(unittest.TestCase):

    def setUp(self):
        if yaml is None:
            self.skipTest("PyYAML not installed")
        self.fm = frontmatter(SPEC)

    def test_entities_slot_sources_the_dictionary_joined_by_authority(self):
        src = self.fm["slot_sources"]["entities_to_create"]
        for must in ("fields[] (owned)", "access_contract", "entities[].authority = record_authority[].key",
                     "n campos · n lidas · n escritas · grão · volume", "⚠️ lacuna row"):
            self.assertIn(must, src, must)

    def test_the_draft_is_provenance_only_never_a_source_to_re_read(self):
        fs = "\n".join(str(x) for x in self.fm["forbidden_sources"])
        self.assertIn("_capture/* to re-settle an upstream fact", fs)
        self.assertIn("fields-draft.json", fs)
        self.assertIn("never re-reads the draft", fs)

    def test_the_transformation_is_declared(self):
        pt = "\n".join(str(x) for x in self.fm["permitted_transformations"])
        self.assertIn("record_authority[].fields[] | access_contract -> §4 rows", pt)
        self.assertIn("NEVER a value by analogy", pt)

    def test_sufficiency_rules_are_declared_for_the_four_slots(self):
        suf = self.fm["sufficiency"]
        self.assertEqual(sorted(suf), ["entities_to_create", "flows_to_implement",
                                       "integrations", "security_implementation"])
        ent = "\n".join(suf["entities_to_create"])
        for must in ("type != unknown", "index primary", "readonly true", "open U-nnn",
                     "state and source", "⚠️ lacuna row"):
            self.assertIn(must, ent, must)
        self.assertIn("Papel × (Ecrã | Entidade)", "\n".join(suf["security_implementation"]))

    def test_body_section_4_names_the_form_the_counts_and_the_gap(self):
        body = SPEC.split("## 4. Entidades e estruturas de dados")[1].split("## 5.")[0]
        for must in ("`entities[].authority`", "lidas (n) · escritas (n) · chave",
                     "Os números **ficam escritos** aqui", "⚠️ lacuna — entidade sem autoridade de registo",
                     "nunca «ver secção 16»", "afirmativamente vazio"):
            self.assertIn(must, body, must)

    def test_a5_stays_read_only_here(self):
        self.assertIn("A5 is READ-ONLY here", SPEC)


class ArchitectureStoryCarrier(unittest.TestCase):

    def test_data_section_carries_the_dictionary_table_and_decides_nothing(self):
        data = STORY.split("## Data")[1].split("## Integrations")[0]
        self.assertIn("DICTIONARY TABLE, carried (never authored)", data)
        self.assertIn("decides no disposition, promotes no line, invents no field", data)

    def test_the_authority_stamp_placeholder_sits_under_the_title(self):
        self.assertRegex(STORY, r"# Architecture Story — \{\{slug\}\}\n<!-- authority: _blueprint/ux-blueprint_v<NN>\.yaml#architecture @ sha256:<hex>")
        self.assertIn("--authority-stamp", STORY)


class EstimateReadsOnlyTheSpecification(unittest.TestCase):
    """The counts travel record → §4 → Estimate; the Estimate never reads the draft."""

    def test_estimate_never_names_the_draft_or_the_capture(self):
        if yaml is None:
            self.skipTest("PyYAML not installed")
        fm = frontmatter(ESTIMATE)
        src = str(fm["slot_sources"])
        self.assertNotIn("fields-draft", src)
        self.assertNotIn("_capture", src)

    def test_work_breakdown_carries_a_driver_cited_to_the_specification(self):
        if yaml is None:
            self.skipTest("PyYAML not installed")
        fm = frontmatter(ESTIMATE)
        src = fm["slot_sources"]["work_breakdown"]
        self.assertIn("`driver` column (P-10)", src)
        self.assertIn("n campos · n lidas · n escritas · grão · volume", src)
        self.assertIn("never reads the capture, the SU or a topic pack", src)
        body3 = ESTIMATE.split("## 3. Decomposição de trabalho")[1].split("## 4.")[0]
        self.assertIn("**`driver`** (P-10)", body3)
        self.assertNotIn("as-is", body3)

    def test_operational_impact_reads_the_specifications_section_only(self):
        if yaml is None:
            self.skipTest("PyYAML not installed")
        fm = frontmatter(ESTIMATE)
        src = fm["slot_sources"]["operational_impact"]
        self.assertIn("Alteração do caminho operacional", src)
        for banned in ("as-is", "_synthesis", "shared-understanding", "_capture"):
            self.assertNotIn(banned, src, banned)


LENS_OPS = read(".claude/skills/lens-operations/SKILL.md")
LENS_DATA = read(".claude/skills/lens-data/SKILL.md")
ASIS = read("library/kernel/synthesis-templates/as-is.template.md")


class P5StepTimesAndDataShape(unittest.TestCase):

    def test_operations_lens_records_time_per_step_as_assumed_or_unknown(self):
        self.assertIn("`step_duration`", LENS_OPS)
        blk = LENS_OPS.split("`step_duration` (P-5)")[1][:900]
        self.assertIn("`Assumed` with its basis", blk)
        self.assertIn("`custo=email`", blk)
        self.assertIn("Never a guessed figure", blk)

    def test_data_lens_gets_shape_not_attributes(self):
        self.assertIn("`data_shape`", LENS_DATA)
        blk = LENS_DATA.split("`data_shape` (P-5)")[1][:900]
        self.assertIn("never the attribute list", blk)
        self.assertIn("fields_draft.py", blk)

    def test_as_is_carries_the_steps_and_time_table_for_the_specification_only(self):
        sec = ASIS.split("### Passos e tempo (P-5)")[1].split("## Personas")[0]
        self.assertIn("| passo | quem | tempo | estado · base | fonte |", sec)
        self.assertIn("Unknown (U-nnn, custo=email)", sec)
        self.assertIn("ONE contracted source of the Implementation Specification", sec)
        self.assertIn("NOT an Estimate source in any mode", sec)
        for must in ("NOT required, NOT conditional, NOT fallback, NOT point-of-need",
                     "not required, not\n  conditional, not fallback, not point-of-need"):
            if must in ASIS:
                break
        else:
            self.fail("the as-is template lost its four-way Estimate prohibition")


class P10OperatingPathChange(unittest.TestCase):

    def setUp(self):
        if yaml is None:
            self.skipTest("PyYAML not installed")
        self.fm = frontmatter(SPEC)

    def test_the_section_is_conditional_and_sourced_from_the_as_is_steps_table(self):
        self.assertIn("operating_path_change", self.fm["conditional_slots"])
        self.assertNotIn("operating_path_change", self.fm["required_slots"])
        src = self.fm["slot_sources"]["operating_path_change"]
        self.assertIn("_synthesis/as-is.md# Passos e tempo", src)
        self.assertIn("passo · quem · tempo actual · novo processo · tempo novo · Δ", src)
        cond = self.fm["slot_conditions"]["operating_path_change"]
        self.assertIn("skip, never a gap", cond)
        self.assertIn("`inalterado`", cond)

    def test_the_as_is_edge_is_narrow_and_declared(self):
        cs = "\n".join(str(x) for x in self.fm["conditional_sources"])
        self.assertIn("_synthesis/as-is.md# Passos e tempo — ONLY as the source of the operating-path change table", cs)
        self.assertIn("Never a work unit, never acceptance work, never a proof level", cs)
        fs = "\n".join(str(x) for x in self.fm["forbidden_sources"])
        self.assertIn("_synthesis/as-is.md as the source of acceptance work", fs)

    def test_body_section_16_exists_and_open_work_items_moved_to_17(self):
        self.assertIn("## 16. Alteração do caminho operacional", SPEC)
        self.assertIn("## 17. Itens de trabalho em aberto", SPEC)
        self.assertIn("{{operating_path_change}}", SPEC)
        body = SPEC.split("## 16. Alteração do caminho operacional")[1].split("## 17.")[0]
        for must in ("`not derivable — <razão>`", "`inalterado`", "nunca a justificação do investimento",
                     "só esta — que a Estimativa lê"):
            self.assertIn(must, body, must)


if __name__ == "__main__":
    unittest.main(verbosity=1)
