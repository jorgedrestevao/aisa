"""Phase E — council persona wiring checks.

Asserts what the simplification claims: seven distinct personas, no framework
duplication inside them, one centrally supplied set of council mechanics, and a
chairman that still parses what the personas return. Deliberately small: no
council driver, no fixture engagement, no new framework.

    python .claude/tests/test_council_wiring.py
"""

import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PERSONAS = (
    "business-analyst",
    "operations-lead",
    "user-advocate",
    "data-steward",
    "compliance-officer",
    "cfo-lens",
    "solution-architect",
)
DISCOVERY_PERSONAS = PERSONAS[:6]
PERSONA_LENS = {
    "business-analyst": "business",
    "operations-lead": "operations",
    "user-advocate": "user",
    "data-steward": "data",
    "compliance-officer": "governance",
    "cfo-lens": "financial",
    "solution-architect": "technology",
}
SCHEMA_SECTIONS = (
    "### Headline",
    "### Evidence anchors",
    "### Proposal",
    "### Open questions / Unknowns flagged",
    "### Conflicts seen",
    "### Risks",
)


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as fh:
        return fh.read()


AGENTS = {p: read(".claude", "agents", p + ".md") for p in PERSONAS}
FRAME = read(".claude", "skills", "aisa-frame", "SKILL.md")
OPTIONS = read(".claude", "skills", "aisa-options", "SKILL.md")
CHAIRMAN = read(".claude", "skills", "chairman-synthesis", "SKILL.md")
ORCH = read("library", "kernel", "orchestration.md")
PREAMBLE = CHAIRMAN.split("## Council launch preamble")[1].split("\n## Hard rules")[0]


class TestPersonasExistAndStayDistinct(unittest.TestCase):
    def test_all_seven_exist_with_identity_and_mandate(self):
        for name, text in AGENTS.items():
            self.assertIn("## Identity", text, name)
            self.assertIn("## Mandate per phase", text, name)
            self.assertIn("## Memory consulted", text, name)
            for phase in ("**Framing**", "**Options**", "**Decision**"):
                self.assertIn(phase, text, name + " missing " + phase + " mandate")

    def test_each_persona_states_what_it_challenges(self):
        for name, text in AGENTS.items():
            self.assertIn("What you challenge", text, name)

    def test_identities_are_not_interchangeable(self):
        bodies = {}
        for name, text in AGENTS.items():
            body = text.split("## Identity")[1].split("\n## ")[0].strip()
            self.assertTrue(len(body) > 200, name + " identity is too thin to be a voice")
            self.assertNotIn(body, bodies, name + " duplicates " + str(bodies.get(body)))
            bodies[body] = name

    def test_bound_perspectives_are_preserved(self):
        markers = {
            "business-analyst": ("impact", "urgency", "stakeholder"),
            "operations-lead": ("exception", "handoff", "documented process"),
            "user-advocate": ("adoption", "accessibility", "context"),
            "data-steward": ("owns the data", "sensitiv", "quality"),
            "compliance-officer": ("audit", "access control", "compliance"),
            "cfo-lens": ("cost", "payback", "run cost"),
            "solution-architect": ("architect", "integration", "reversib"),
        }
        for name, needles in markers.items():
            low = AGENTS[name].lower()
            for needle in needles:
                self.assertIn(needle.lower(), low, name + " lost '" + needle + "'")


class TestNoFrameworkDuplicationInPersonas(unittest.TestCase):
    def test_no_persona_carries_the_return_schema(self):
        for name, text in AGENTS.items():
            self.assertNotIn("## Output format", text, name)
            for section in SCHEMA_SECTIONS:
                self.assertNotIn(section, text, name + " still copies the return schema")

    def test_no_persona_carries_council_mode_mechanics(self):
        for name, text in AGENTS.items():
            low = text.lower()
            self.assertNotIn("## mode (council-independent)", low, name)
            self.assertNotIn("in-flight", low, name)
            self.assertNotIn("read-only by tool grant", low, name)
            self.assertNotIn("every file under", low, name)

    def test_no_persona_restates_kernel_state_semantics(self):
        for name, text in AGENTS.items():
            for token in ("verificado_em", "validade", "states.md", "was <id>", "append-only"):
                self.assertNotIn(token, text, name + " restates kernel state semantics")

    def test_personas_are_not_told_to_read_their_lens_skill(self):
        for name, text in AGENTS.items():
            self.assertIn("You do not read its `SKILL.md`", text, name)
            self.assertNotIn("lens-" + PERSONA_LENS[name] + "/SKILL.md", text, name)

    def test_council_prompts_do_not_send_personas_to_the_lens_skill(self):
        for name, skill in (("aisa-frame", FRAME), ("aisa-options", OPTIONS)):
            self.assertNotIn("your lens skill at", skill, name)
            self.assertIn("do not tell", skill.lower(), name)

    def test_personas_shrank(self):
        for name, text in AGENTS.items():
            self.assertLess(len(text), 3200, name + " is " + str(len(text)) + " chars")


class TestCommonMechanicsCentralized(unittest.TestCase):
    def test_preamble_exists_once(self):
        self.assertEqual(CHAIRMAN.count("## Council launch preamble"), 1)
        for skill in (FRAME, OPTIONS):
            self.assertIn("Council launch preamble", skill)
            self.assertIn("chairman-synthesis/SKILL.md", skill)

    def test_preamble_carries_every_required_context_item(self):
        for needle in (
            "Council-independent mode",
            "<phase>",
            "<round>",
            "engagement",
            "pack",
            "_council-prep",
            "evidence-index.md",
            "agent-memory",
            "Independence:",
            "Technology neutrality:",
            "Evidence integrity:",
            "Mandate:",
        ):
            self.assertIn(needle, PREAMBLE, "preamble missing " + needle)

    def test_independence_rule_present_once_in_the_launch_context(self):
        self.assertIn("do not see, request or wait on any", PREAMBLE)
        self.assertIn("Only the chairman writes", PREAMBLE)
        for name, text in AGENTS.items():
            self.assertNotIn("Only the chairman writes", text, name)

    def test_orchestration_owns_the_persona_boundary(self):
        self.assertIn("Common council mechanics live here", ORCH)
        self.assertIn("not required to re-read its lens", ORCH)


class TestSharedEvidenceInCouncil(unittest.TestCase):
    def test_read_every_input_instruction_is_gone(self):
        for name, skill in (("aisa-frame", FRAME), ("aisa-options", OPTIONS)):
            self.assertNotIn("every file under `<engagement>/inputs/`", skill, name)

    def test_index_is_the_source_map(self):
        self.assertIn("_capture/evidence-index.md", PREAMBLE)
        self.assertIn("source map", PREAMBLE)
        self.assertIn("authoritative on conflict", PREAMBLE)

    def test_no_persona_specific_evidence_routing(self):
        low = (FRAME + OPTIONS + PREAMBLE).lower()
        self.assertIn("do not build a per-persona evidence view", FRAME.lower())
        self.assertIn("no evidence has been assigned to you", PREAMBLE.lower())
        for banned in ("evidence bundle", "relevance score", "evidence router"):
            self.assertNotIn(banned, low)

    def test_absence_is_stated_not_assumed(self):
        self.assertIn("raw `inputs/` is the evidence surface", PREAMBLE)
        self.assertIn("raw `inputs/` is the evidence surface", FRAME)


class TestPackCues(unittest.TestCase):
    def test_cues_keep_attention_cue_semantics(self):
        self.assertIn("cues, not a checklist", PREAMBLE)
        self.assertIn("an uncovered cue is not a gap", PREAMBLE)

    def test_cues_are_resolved_verbatim_and_degrade(self):
        self.assertIn("extra_signals", FRAME)
        self.assertIn("verbatim", FRAME)
        self.assertIn("omit the cue line", FRAME.lower())
        self.assertIn("no scoring, ranking, filtering, reordering or rewriting", FRAME)

    def test_technology_is_excluded_from_the_discovery_cue_model(self):
        self.assertIn("receives no Discovery `extra_signals`", OPTIONS)
        self.assertIn("Pack knowledge is pull-based", AGENTS["solution-architect"])

    def test_domain_knowledge_is_not_preloaded(self):
        self.assertIn("Your pack access is pull-based and Options-only", OPTIONS)
        self.assertIn("never place `decision-tree.md` or `domain-knowledge/` contents", OPTIONS)
        self.assertIn(
            "Never load the domain-knowledge base by default",
            AGENTS["solution-architect"],
        )
        self.assertIn("Do not dump", PREAMBLE)


class TestPhaseBoundaries(unittest.TestCase):
    def test_framing_stays_technology_neutral(self):
        self.assertIn("[Framing, all personas] No vendor or product names", PREAMBLE)
        self.assertIn("keep the `[Framing, all personas]` technology-neutrality line", FRAME)
        vendors = (
            "power platform",
            "outsystems",
            "mendix",
            "dataverse",
            "canvas app",
            "power automate",
            "sharepoint",
        )
        for name in DISCOVERY_PERSONAS:
            low = AGENTS[name].lower()
            for vendor in vendors:
                self.assertNotIn(vendor, low, name + " names a vendor")

    def test_solution_architect_is_not_launched_in_framing(self):
        self.assertIn("solution-architect is NOT invoked in Framing", FRAME)
        self.assertIn("**Framing**: **not invoked**", AGENTS["solution-architect"])
        self.assertIn("## Phase gate", AGENTS["solution-architect"])

    def test_options_allows_technology_reasoning_only_for_the_architect(self):
        self.assertIn("[Options, solution-architect]", PREAMBLE)
        self.assertIn("[Options, the six Discovery personas]", PREAMBLE)
        self.assertIn("Naming products belongs to `solution-architect` alone", PREAMBLE)


class TestChairmanCompatibility(unittest.TestCase):
    def test_chairman_parses_the_schema_it_owns(self):
        for section in SCHEMA_SECTIONS:
            self.assertIn(section, PREAMBLE, "schema missing " + section)
        for label in ("Headline", "Evidence anchors", "Proposal", "Conflicts seen", "Risks"):
            self.assertIn(label, CHAIRMAN, "chairman stopped consuming " + label)
        self.assertIn("Parse the six sections", CHAIRMAN)

    def test_chairman_no_longer_points_at_persona_files_for_the_schema(self):
        self.assertNotIn("see persona agent files for the schema", CHAIRMAN)
        self.assertNotIn("*Output format*", CHAIRMAN)

    def test_empty_section_convention_survives(self):
        self.assertIn("- (none)", PREAMBLE)

    def test_synthesis_reasoning_untouched(self):
        for step in (
            "Step 1 — Read the persona outputs",
            "Step 2 — Build the synthesis map",
            "Step 2b — Dialectic hand-back",
            "Step 3 — Assign Shared Understanding states",
        ):
            self.assertIn(step, CHAIRMAN)


class TestMemoryBinding(unittest.TestCase):
    def test_each_persona_keeps_its_own_memory_paths(self):
        for name, text in AGENTS.items():
            self.assertIn("_universal/" + name + "/", text)
            self.assertIn("_tenant/<tenant>/" + name + "/", text)
            self.assertIn("diary.md", text)

    def test_memory_is_a_pointer_not_a_dump(self):
        self.assertIn("Memory (optional)", PREAMBLE)
        self.assertIn("A pointer, never contents", FRAME)


if __name__ == "__main__":
    unittest.main(verbosity=2)
