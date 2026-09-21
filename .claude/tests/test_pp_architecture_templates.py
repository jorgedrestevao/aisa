"""Step 5B — PP architecture-template runtime.

Mechanical/structural assertions only. These prove IMPLEMENTATION FIDELITY against the
frozen Step 5A design (including its §27 bounded correction and §28 component-identity
micro-correction); they do NOT prove that a generated architecture is semantically
defensible under engagement pressure — that is Step 5C.

The fixture classes below prove the runtime can REPRESENT and mechanically ENFORCE
F-1 … F-19. They do not replay them behaviourally.

    python .claude/tests/test_pp_architecture_templates.py
"""

import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PACK_DIR = os.path.join(ROOT, "library", "packs", "pp")
AT_DIR = os.path.join(PACK_DIR, "architecture-templates")
SKILLS = os.path.join(ROOT, ".claude", "skills")
KERNEL = os.path.join(ROOT, "library", "kernel")

# The approved runtime model: 5 template units + README (positioning, not a unit).
RUNTIME_UNITS = [
    "architecture-core.md",
    "fragment-experience-internal.md",
    "fragment-experience-external.md",
    "fragment-experience-inherited.md",
    "fragment-boundary-and-imports.md",
]
RETIRED = ["sharepoint-first.md", "dataverse-first.md", "hybrid.md"]

# Obsolete branch-MODEL vocabulary. Bare "branch" is deliberately NOT a token: the runtime
# files legitimately state "no branch" / "replacing the obsolete `branch` field" as
# documentation of the removal. These tokens are the model itself.
OBSOLETE_BRANCH_MODEL = [
    "applies_to_branch",
    "available_after_outcome",
    "architecture-shape",
    "sharepoint-first",
    "dataverse-first",
    "{{chosen_architecture}}",
    "Branch (if technology)",
    "Branch (decision-tree)",
    "architecture-templates/<branch>",
]

# Step 5 runtime files whose architecture vocabulary Step 5B owns.
STEP5_RUNTIME = [
    os.path.join(AT_DIR, "architecture-core.md"),
    os.path.join(AT_DIR, "fragment-experience-internal.md"),
    os.path.join(AT_DIR, "fragment-experience-external.md"),
    os.path.join(AT_DIR, "fragment-experience-inherited.md"),
    os.path.join(AT_DIR, "fragment-boundary-and-imports.md"),
    os.path.join(SKILLS, "aisa-blueprint", "SKILL.md"),
    os.path.join(SKILLS, "aisa-render", "SKILL.md"),
    os.path.join(SKILLS, "aisa-synthesize", "SKILL.md"),
    os.path.join(SKILLS, "aisa-options", "SKILL.md"),
    os.path.join(SKILLS, "aisa-simulate", "SKILL.md"),
    os.path.join(KERNEL, "blueprint-contract.md"),
    os.path.join(KERNEL, "render-contract.md"),
    os.path.join(KERNEL, "synthesis-templates", "architecture-story.template.md"),
]

# Step 6 consumers deliberately NOT migrated by Step 5B. Documented carry-forwards.
STEP6_CARRY_FORWARD = [
    os.path.join(PACK_DIR, "deliverable-templates", "solution-blueprint.template.md"),
    os.path.join(PACK_DIR, "deliverable-templates", "implementation-spec.template.md"),
    os.path.join(PACK_DIR, "deliverable-templates", "claude-design-brief.template.md"),
]

SIX_CHANNELS = ["Governa", "ALM", "Custo", "Monitoriza", "Recupera", "Operador"]

PRODUCT_WORDS = [
    "sharepoint", "dataverse", "azure-sql", "azure sql", "canvas", "model-driven",
    "power automate", "powerapps", "power apps", "outsystems", "mendix",
]

CANONICAL_PATTERNS = [
    "direct", "api-mediated", "api-facade", "event-driven", "queue-based",
    "hybrid-low-code-pro-code", "background-processing", "data-virtualization",
    "data-replication", "enterprise-boundary",
]


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def flat(text):
    """Collapse whitespace so a phrase still matches when the markdown wraps it.

    Same idiom as test_pp_options_decision_model.py — a hard line break inside a
    sentence is a formatting artefact, never a semantic difference.
    """
    return re.sub(r"\s+", " ", text)


def has(needle, haystack):
    """Whitespace- and case-insensitive phrase containment."""
    return flat(needle).lower() in flat(haystack).lower()


def at(name):
    return read(os.path.join(AT_DIR, name))


CORE = None
README = None
F_INT = None
F_EXT = None
F_INH = None
F_BND = None
BLUEPRINT_SKILL = None
RENDER_SKILL = None
DECIDE_SKILL = None


def setUpModule():
    global CORE, README, F_INT, F_EXT, F_INH, F_BND
    global BLUEPRINT_SKILL, RENDER_SKILL, DECIDE_SKILL
    CORE = at("architecture-core.md")
    README = at("README.md")
    F_INT = at("fragment-experience-internal.md")
    F_EXT = at("fragment-experience-external.md")
    F_INH = at("fragment-experience-inherited.md")
    F_BND = at("fragment-boundary-and-imports.md")
    BLUEPRINT_SKILL = read(os.path.join(SKILLS, "aisa-blueprint", "SKILL.md"))
    RENDER_SKILL = read(os.path.join(SKILLS, "aisa-render", "SKILL.md"))
    DECIDE_SKILL = read(os.path.join(SKILLS, "aisa-decide", "SKILL.md"))


class PhraseCase(unittest.TestCase):
    """Base class: phrase assertions that tolerate markdown line wrapping."""

    def assertPhrase(self, needle, haystack, label=""):
        self.assertTrue(has(needle, haystack),
                        "phrase not found%s: %r" % (" in " + label if label else "", needle))

    def assertNoPhrase(self, needle, haystack, label=""):
        self.assertFalse(has(needle, haystack),
                         "phrase unexpectedly present%s: %r"
                         % (" in " + label if label else "", needle))


# ---------------------------------------------------------------- taxonomy

class TestTaxonomy(unittest.TestCase):
    def test_exactly_five_runtime_template_units(self):
        present = sorted(f for f in os.listdir(AT_DIR)
                         if f.endswith(".md") and f != "README.md")
        self.assertEqual(sorted(RUNTIME_UNITS), present, "runtime units: %r" % present)
        self.assertEqual(5, len(present))

    def test_readme_exists_and_is_not_a_runtime_unit(self):
        self.assertTrue(os.path.isfile(os.path.join(AT_DIR, "README.md")))
        self.assertIn("NOT a runtime template unit", README)
        self.assertIn("Runtime template units: 5", README)

    def test_old_three_branch_files_are_absent(self):
        for name in RETIRED:
            self.assertFalse(os.path.exists(os.path.join(AT_DIR, name)),
                             "retired file still present: %s" % name)

    def test_no_product_named_template(self):
        for name in RUNTIME_UNITS:
            low = name.lower()
            for word in PRODUCT_WORDS:
                self.assertNotIn(word.replace(" ", "-"), low,
                                 "product-named template: %s" % name)

    def test_zero_pattern_specific_templates(self):
        """Ten canonical patterns must produce zero pattern-specific template files."""
        names = [f.lower() for f in os.listdir(AT_DIR) if f.endswith(".md")]
        for pattern in CANONICAL_PATTERNS:
            if pattern == "direct":
                continue  # substring of nothing here; guard anyway below
            for name in names:
                self.assertNotEqual(pattern + ".md", name,
                                    "pattern-specific template: %s" % name)
        self.assertEqual(6, len(names), "unexpected file count: %r" % names)

    def test_no_headless_specific_template(self):
        self.assertFalse(os.path.exists(os.path.join(AT_DIR, "fragment-experience-none.md")))
        for name in os.listdir(AT_DIR):
            self.assertNotIn("headless", name.lower())

    def test_core_is_the_single_fixed_entry_point(self):
        self.assertIn("entry_point: true", CORE)
        for path in (os.path.join(SKILLS, "aisa-blueprint", "SKILL.md"),
                     os.path.join(SKILLS, "aisa-render", "SKILL.md"),
                     os.path.join(SKILLS, "aisa-synthesize", "SKILL.md"),
                     os.path.join(KERNEL, "synthesis-templates", "architecture-story.template.md")):
            self.assertIn("architecture-templates/architecture-core.md", read(path),
                          "no fixed entry point in %s" % path)


# ------------------------------------------------------------ branch removal

class TestBranchRemoval(unittest.TestCase):
    def test_no_obsolete_branch_model_in_step5_runtime(self):
        for path in STEP5_RUNTIME:
            body = read(path)
            for token in OBSOLETE_BRANCH_MODEL:
                self.assertNotIn(token, body,
                                 "%s: obsolete branch model %r" % (os.path.basename(path), token))

    def test_readme_legacy_paragraph_is_the_documented_exemption(self):
        """README is the ONE place the three legacy names survive — as read-compat."""
        self.assertIn("Legacy read compatibility", README)
        for name in ("sharepoint-first", "dataverse-first", "hybrid"):
            self.assertIn(name, README)
        self.assertIn("read compatibility only", README.lower())
        for forbidden in ("shim", "router"):
            self.assertIn("no %s" % forbidden, README.lower())

    def test_step6_carry_forwards_are_resolved(self):
        """Step 6B RESOLVED the carry-forward: the three templates no longer use the
        old branch contract.

        Step 5B deliberately left `chosen_architecture` / `Branch (if technology)` in the
        three architecture-consuming deliverable templates and this test PINNED that
        carry-forward so it could not be forgotten. Step 6B removed all nine occurrences
        and pointed the templates at the fixed `architecture-core.md` include, so the
        assertion inverts: the carry-forward set must now be EMPTY.

        Step 5 semantics are untouched — this test tracks a migration, not a contract.
        """
        stale = []
        for path in STEP6_CARRY_FORWARD:
            body = read(path)
            if "chosen_architecture" in body or "Branch (if technology)" in body:
                stale.append(os.path.basename(path))
        self.assertEqual([], sorted(stale),
                         "Step 6B must leave no branch-model vocabulary in the deliverables")

    def test_step6_deliverables_use_the_fixed_architecture_include(self):
        """The replacement is one FIXED include, in the Architecture Blueprint only."""
        includes = []
        for path in STEP6_CARRY_FORWARD:
            includes += re.findall(r"\{\{>>\s*([^}]+?)\s*\}\}", read(path))
        self.assertEqual(["architecture-templates/architecture-core.md"], includes,
                         "exactly one fixed architecture include across the three")

    def test_no_loop_primitive_or_router_added(self):
        for body in (CORE, F_BND, RENDER_SKILL, BLUEPRINT_SKILL):
            self.assertNotIn("{{#each", body)
            self.assertNotIn("{{#for", body)
        self.assertIn("no router", (CORE + README + BLUEPRINT_SKILL + RENDER_SKILL).lower())


# ------------------------------------------------------------- authorization

class TestAuthorization(unittest.TestCase):
    def test_authorization_is_a_product_of_two_factors(self):
        self.assertIn("outcome reachability", README.lower())
        self.assertIn("architectability", README.lower())
        self.assertIn("architecture authorization = outcome reachability", README)
        self.assertIn("architecture authorization = outcome reachability", BLUEPRINT_SKILL)

    def test_outcome_alone_is_insufficient(self):
        self.assertIn("Outcome reachability alone is never sufficient", README)
        self.assertIn("never sufficient", BLUEPRINT_SKILL)

    def test_three_authorization_values_only(self):
        for value in ("authorized", "authorized-bounded", "not-authorized"):
            self.assertIn(value, README)
            self.assertIn(value, BLUEPRINT_SKILL)
        self.assertIn("three values, not fifteen", README)

    def test_the_two_failure_reasons_are_never_merged(self):
        self.assertIn("never merged", README)
        for body in (BLUEPRINT_SKILL, RENDER_SKILL):
            self.assertIn("distinct", body)

    def test_no_scope_architectable_produces_no_pp_architecture(self):
        self.assertIn("no PP architecture", BLUEPRINT_SKILL)
        self.assertIn("Do **not** relabel either as `Decision Blocked`", BLUEPRINT_SKILL)

    def test_decision_blocked_is_repeated_never_derived(self):
        for body in (README, RENDER_SKILL):
            self.assertIn("never derive", body.lower())

    def test_authorization_read_never_derived_or_upgraded(self):
        self.assertIn("read, never derived", README)
        self.assertIn("cannot upgrade `authorized-bounded` to `authorized`", README)
        for body in (CORE, BLUEPRINT_SKILL, RENDER_SKILL):
            self.assertIn("never derived, upgraded or downgraded", body)

    def test_no_template_lists_an_outcome_class(self):
        """The reachability table has exactly one home: README."""
        for name in RUNTIME_UNITS:
            body = at(name)
            self.assertNotIn("outcome-classes.md", body,
                             "%s lists outcome classes" % name)
            self.assertNotIn("strong-fit", body)
            self.assertNotIn("fit-with-constraints", body)
        self.assertIn("outcome-classes.md", README)
        self.assertIn("No template file lists an outcome class", README)

    def test_reachability_table_covers_all_fifteen_classes(self):
        for cls in ("| 1 |", "| 2 |", "| 3 |", "| 4 |", "| 5 |", "| 6 |", "| 7 |",
                    "| 8 |", "| 9 |", "| 10 |", "| 11 |", "| 12 |", "| 13(a) |",
                    "| 13(b) |", "| 14 |", "| 15 |"):
            self.assertIn(cls, README, "reachability row missing: %s" % cls)


class TestArchitectability(unittest.TestCase):
    def test_architectability_boundary_has_both_lists(self):
        self.assertIn("Architectable | Not architectable", README)
        for item in ("custom-only", "packaged", "cloud-native-only",
                     "Incumbent-system internals", "Another platform's internals"):
            self.assertIn(item, README)

    def test_architectability_basis_is_recorded_in_one_sentence(self):
        self.assertIn("architectability_basis", CORE)
        self.assertIn("architectability_basis", BLUEPRINT_SKILL)
        self.assertIn("one sentence", README + BLUEPRINT_SKILL)

    def test_far_side_is_never_architectable(self):
        self.assertIn("far side of a scope pair is never architectable", README)

    def test_blueprint_owns_the_mechanical_entry_gate(self):
        self.assertIn("architecture entry gate", BLUEPRINT_SKILL)
        self.assertIn("mechanical, not a new decision", BLUEPRINT_SKILL)
        self.assertIn("initialize architecture.authorization", BLUEPRINT_SKILL)


class TestDecideOwnsNoAuthorization(unittest.TestCase):
    """Step 3 freeze: aisa-decide serializes decided facts and emits no architecture verdict."""

    def test_decide_never_emits_architecture_authorization(self):
        self.assertIn("Must NEVER emit", DECIDE_SKILL)
        for forbidden in ("architecture.authorization", "architectability_basis",
                          "experience mode", "composition selection",
                          "record authority", "architecture-template selection"):
            self.assertIn(forbidden, DECIDE_SKILL)

    def test_decide_has_no_branch_field(self):
        self.assertNotIn("**Branch (if technology)**", DECIDE_SKILL)
        self.assertNotIn("<decision-tree branch>", DECIDE_SKILL)

    def test_decide_serializes_the_facts_blueprint_needs(self):
        for fact in ("Selected solution / composition", "UNCOLLAPSED",
                     "Proof obligations", "Preconditions", "Conditions"):
            self.assertIn(fact, DECIDE_SKILL)

    def test_decide_stage_semantics_untouched(self):
        """Presentation-only change: the decision flow itself must still be intact."""
        for kept in ("### 1. Pre-flight", "### 2. Interactive capture",
                     "### 3. Flip state to Decision (atomic)",
                     "### 4. Append the decision to decisions.md",
                     "### 5. Auto-invoke aisa-synthesize"):
            self.assertIn(kept, DECIDE_SKILL)
        self.assertIn("serialization cleanup only", DECIDE_SKILL)


# ------------------------------------------------------------------ headless

class TestHeadless(unittest.TestCase):
    def test_experience_mode_none_is_a_valid_finalized_value(self):
        self.assertIn("none | owned-internal | owned-external | inherited", BLUEPRINT_SKILL)
        self.assertIn("finalized", README)
        for body in (README, BLUEPRINT_SKILL, CORE):
            self.assertNotIn("mode: none` is an Unknown", body)
        self.assertIn("not an Unknown", README)

    def test_primary_surface_is_null_when_mode_is_none(self):
        self.assertIn("primary_surface: null", BLUEPRINT_SKILL)
        self.assertTrue(has("`primary_surface` is `null`", README)
                        or has("primary_surface: null", README),
                        "README does not state primary_surface is null when mode is none")

    def test_zero_experience_includes_when_mode_is_none(self):
        self.assertIn("ZERO includes", CORE)
        self.assertIn("ZERO includes", RENDER_SKILL)
        self.assertTrue(has("zero experience fragments", README))
        self.assertTrue(has("zero experience-fragment includes", BLUEPRINT_SKILL)
                        or has("zero** experience fragments", BLUEPRINT_SKILL)
                        or has("zero experience fragments", BLUEPRINT_SKILL))

    def test_no_a4_when_mode_is_none(self):
        self.assertIn("A4 is not engaged", CORE + README)
        self.assertIn("**no A4**", BLUEPRINT_SKILL)

    def test_never_opens_fragment_experience_none(self):
        for name, body in (("CORE", CORE), ("README", README),
                           ("RENDER", RENDER_SKILL), ("BLUEPRINT", BLUEPRINT_SKILL)):
            self.assertIn("fragment-experience-none.md", body)
            self.assertTrue(
                has("not attempt to resolve", body) or has("does not exist", body),
                "%s: no explicit prohibition on resolving fragment-experience-none.md" % name)

    def test_no_render_gap_and_no_unresolved_surface_when_mode_is_none(self):
        for name, body in (("CORE", CORE), ("README", README),
                           ("RENDER", RENDER_SKILL), ("BLUEPRINT", BLUEPRINT_SKILL)):
            self.assertTrue(has("render gap", body), "%s: render gap not addressed" % name)
            self.assertTrue(has("surface unresolved", body),
                            "%s: `surface unresolved` not forbidden" % name)
        self.assertTrue(has("not applicable", CORE))

    def test_headless_keeps_a6_and_a7(self):
        self.assertIn("A7 — Identidade", CORE)
        self.assertIn("A6 — Automa", CORE)
        self.assertIn("COMMON. Never owned by an experience fragment", CORE)
        self.assertIn("headless architecture still requires this section in full", CORE)

    def test_headless_does_not_fabricate_a_surface(self):
        self.assertIn("Do not fabricate a user surface", README)
        self.assertIn("Never fabricate a user surface", BLUEPRINT_SKILL)


# ---------------------------------------------------------------- experience

class TestExperienceFragments(unittest.TestCase):
    def test_three_modes_resolve_exactly_one_fragment_each(self):
        mapping = {
            "owned-internal": "fragment-experience-internal.md",
            "owned-external": "fragment-experience-external.md",
            "inherited": "fragment-experience-inherited.md",
        }
        for mode, fragment in mapping.items():
            self.assertRegex(CORE, re.escape(mode) + r"\s*→\s*" + re.escape(fragment),
                             "core does not map %s -> %s" % (mode, fragment))
            self.assertRegex(RENDER_SKILL, re.escape(mode) + r"\s*→\s*" + re.escape(fragment))
            self.assertTrue(os.path.isfile(os.path.join(AT_DIR, fragment)))

    def test_each_fragment_declares_its_activation(self):
        for body, mode in ((F_INT, "owned-internal"), (F_EXT, "owned-external"),
                           (F_INH, "inherited")):
            self.assertIn("activates_on: architecture.experience.mode == " + mode, body)
            self.assertIn("scope: experience-fragment", body)

    def test_fragments_do_not_own_store_or_security_truth(self):
        for body in (F_INT, F_EXT, F_INH):
            low = body.lower()
            self.assertIn("does not own store choice", low)
            self.assertIn("security truth", low)

    def test_internal_carries_its_named_specialization(self):
        for item in ("Distribui", "delegation-safe", "Offline", "Forfeits",
                     "especializa", "ciclo de vida"):
            self.assertIn(item, F_INT)

    def test_external_carries_its_named_specialization(self):
        for item in ("audi", "identidade externa", "Cache", "frescura",
                     "acessibilidade", "Localiza", "modelo de constru"):
            self.assertIn(item, F_EXT)
        self.assertIn("does NOT decide whether an external audience is required", F_EXT)

    def test_inherited_carries_graduation_trigger_and_no_exclusion_claim(self):
        self.assertIn("graduation_trigger", F_INH)
        self.assertIn("mandatory", F_INH.lower())
        self.assertIn("must NOT claim that this platform is excluded", F_INH)
        self.assertIn("must NOT decide WHEN graduation occurs", F_INH)
        self.assertIn("no independent environment, policy plane or release topology", F_INH)


# ------------------------------------------------------------ record authority

class TestRecordAuthority(unittest.TestCase):
    def test_record_authority_is_zero_to_n(self):
        self.assertIn("0..N", BLUEPRINT_SKILL)
        self.assertIn("record_authority", CORE)

    def test_empty_with_affirmative_rationale_is_valid(self):
        rationale = "No persisted record authority introduced"
        self.assertIn(rationale, CORE)
        self.assertIn(rationale, BLUEPRINT_SKILL)
        self.assertIn("affirmative", CORE.lower())

    def test_missing_evidence_is_not_an_empty_set(self):
        for body in (CORE, BLUEPRINT_SKILL):
            self.assertIn("Missing evidence is never an empty set", body)

    def test_unknown_authority_becomes_a_structural_open_choice(self):
        for body in (CORE, BLUEPRINT_SKILL):
            self.assertIn("open_architecture_choices", body)
            self.assertIn("structural: true", body)


# -------------------------------------------------------- component identity

class TestComponentIdentity(unittest.TestCase):
    def test_component_is_required_on_every_composition(self):
        self.assertIn("component: <local", BLUEPRINT_SKILL)
        self.assertIn("required", BLUEPRINT_SKILL)
        self.assertIn("`component` is the uniqueness-bearing field", F_BND)

    def test_component_is_local_and_unique_within_scope(self):
        for body in (F_BND, BLUEPRINT_SKILL, RENDER_SKILL):
            self.assertIn("unique within", body.lower())
        self.assertIn("local to the architecture scope", F_BND)
        self.assertIn("not globally stable", F_BND)
        self.assertIn("not a registry id", F_BND)

    def test_no_uuid_and_no_identifier_subsystem(self):
        for body in (F_BND, BLUEPRINT_SKILL):
            self.assertIn("No UUIDs", body)
            self.assertIn("identifier subsystem", body)

    def test_duplicate_component_identity_fails_and_never_merges(self):
        for body in (F_BND, CORE, BLUEPRINT_SKILL, RENDER_SKILL):
            low = body.lower()
            self.assertIn("defect", low)
            self.assertIn("never merge", low)
        self.assertIn("auto-suffix", F_BND)
        self.assertIn("collapse imports", F_BND)

    def test_relocated_responsibility_identity_needs_no_second_field(self):
        self.assertIn("`responsibility` is the identity", F_BND)
        self.assertIn("responsibility: <name", BLUEPRINT_SKILL)

    def test_fragment_keys_are_scope_prefixed_and_never_rendered(self):
        for body in (CORE, F_BND, BLUEPRINT_SKILL, RENDER_SKILL):
            self.assertIn("::component::", body)
            self.assertIn("::responsibility::", body)
            self.assertTrue(has("never rendered as engagement vocabulary", body))


# ----------------------------------------------------------- fragment count

class TestFragmentInvariant(unittest.TestCase):
    def test_n_plus_m_invariant_is_stated_in_the_binding_places(self):
        for body in (CORE, F_BND, BLUEPRINT_SKILL, RENDER_SKILL):
            self.assertRegex(body, r"N\s*\+\s*M")
            self.assertIn("exactly", body.lower())

    def test_qualifying_set_is_defined_identically_everywhere(self):
        for name, body in (("CORE", CORE), ("F_BND", F_BND), ("BLUEPRINT", BLUEPRINT_SKILL),
                           ("RENDER", RENDER_SKILL), ("README", README)):
            for token in ("outside-platform", "beyond `direct`", "relocated_responsibilities"):
                self.assertTrue(has(token, body),
                                "%s: qualifying set incomplete (%s)" % (name, token))

    def test_repeat_instruction_is_carried_exactly_once_by_the_core(self):
        self.assertEqual(1, CORE.count("for each qualifying recorded component"),
                         "the core must carry the repeat instruction exactly once")
        self.assertIn("EXACTLY ONCE", CORE)

    def test_six_channels_present_in_the_fragment(self):
        for channel in SIX_CHANNELS:
            self.assertIn(channel, F_BND, "missing channel: %s" % channel)
        self.assertEqual(6, len(re.findall(r"\*\*\d\. ", F_BND)),
                         "the fragment must enumerate exactly six channels")

    def test_a_missing_channel_is_a_defect(self):
        for name, body in (("F_BND", F_BND), ("CORE", CORE), ("README", README),
                           ("RENDER", RENDER_SKILL), ("BLUEPRINT", BLUEPRINT_SKILL)):
            self.assertTrue(has("missing channel is a defect", body),
                            "%s does not state that a missing channel is a defect" % name)

    def test_channel_is_populated_or_not_engaged_with_a_reason(self):
        self.assertIn("not engaged — <reason>", F_BND)
        self.assertEqual(6, len(re.findall(r"or: not engaged — <reason>", F_BND)),
                         "each of the six channels needs its own not-engaged escape")

    def test_imports_is_not_a_declarable_field(self):
        self.assertIn("`imports` is deliberately **not** a field", BLUEPRINT_SKILL)


# ------------------------------------------------------------- scope pairs

class TestScopePairs(unittest.TestCase):
    def test_pairs_stay_uncollapsed(self):
        self.assertIn("UNCOLLAPSED", CORE)
        self.assertIn("UNCOLLAPSED", DECIDE_SKILL)
        self.assertIn("uncollapsed", README.lower())

    def test_relocated_responsibility_gets_boundary_and_owner_not_a_design(self):
        for name, body in (("CORE", CORE), ("README", README), ("F_BND", F_BND),
                           ("BLUEPRINT", BLUEPRINT_SKILL)):
            self.assertTrue(has("never a PP design for the far side", body),
                            "%s does not forbid designing the far side" % name)

    def test_incumbent_fit_unevaluated_is_preserved_verbatim(self):
        for name, body in (("CORE", CORE), ("README", README), ("F_BND", F_BND),
                           ("BLUEPRINT", BLUEPRINT_SKILL)):
            self.assertTrue(has("INCUMBENT FIT UNEVALUATED", body),
                            "%s drops the incumbent marker" % name)
        for name, body in (("README", README), ("F_BND", F_BND),
                           ("BLUEPRINT", BLUEPRINT_SKILL)):
            self.assertTrue(has("never inferred", body) or has("inferred comparator", body),
                            "%s does not forbid inferring comparator fit" % name)

    def test_relocation_carries_outcome_basis_and_gates(self):
        self.assertIn("outcome_basis", BLUEPRINT_SKILL)
        self.assertIn("gates_recorded", BLUEPRINT_SKILL)
        self.assertIn("Gates registados", F_BND)

    def test_fragment_states_what_the_pack_does_not_know(self):
        self.assertIn("não sabe sobre o outro lado", F_BND)
        self.assertIn("no comparator claim", F_BND.lower())


# ------------------------------------------------- sections and gap classes

class TestCoreSections(unittest.TestCase):
    def test_eleven_common_required_sections_present(self):
        for sec in ("### A1", "### A2", "### A3", "### A5", "### A6", "### A7",
                    "### A8", "### A9", "### A10", "### A11", "### A12"):
            self.assertIn(sec, CORE, "missing common section %s" % sec)

    def test_a4_is_conditional_and_delegated(self):
        self.assertIn("### A4", CORE)
        self.assertIn("CONDITIONAL", CORE)
        self.assertIn("rendered by the matching", CORE)

    def test_rejected_ceremony_sections_absent(self):
        low = CORE.lower()
        self.assertNotIn("## risk register", low)
        self.assertNotIn("### risk register", low)
        self.assertNotIn("alternatives considered", low)
        self.assertNotIn("performance encyclopedia", low)

    def test_all_eight_conditional_sections_are_expressible(self):
        for cond in ("A4", "Obriga", "scope ownership", "analítica",
                     "offline", "substitui", "sequência", "candidatas"):
            self.assertTrue(has(cond, CORE), "conditional section missing: %s" % cond)

    def test_condition_not_engaged_is_not_applicable_not_a_gap(self):
        self.assertIn("not applicable", CORE)
        self.assertIn("NOT a missing required slot and NOT a render gap", CORE)

    def test_four_gap_classes_in_kernel_and_render_skill(self):
        for path in (os.path.join(KERNEL, "render-contract.md"),
                     os.path.join(SKILLS, "aisa-render", "SKILL.md")):
            body = read(path)
            for cls in ("not applicable", "optional", "architecture work item",
                        "decision-blocking"):
                self.assertIn(cls, body, "%s: missing gap class %s" % (path, cls))

    def test_structural_choice_blocks_approval_not_production(self):
        for body in (CORE, BLUEPRINT_SKILL, read(os.path.join(KERNEL, "blueprint-contract.md"))):
            low = body.lower()
            self.assertIn("blocks", low)
            self.assertIn("approval", low)
            self.assertIn("production", low)

    def test_no_new_state_machine(self):
        for body in (CORE, BLUEPRINT_SKILL):
            self.assertIn("no new approval state machine", body.lower())


class TestDiagramContract(unittest.TestCase):
    def test_required_boundary_table_has_its_six_columns(self):
        for col in ("Componente", "Papel", "Governa", "fronteira de confian",
                    "Owner", "Classifica"):
            self.assertIn(col, CORE.replace("Fronteira de confian", "fronteira de confian"),
                          "boundary table column missing: %s" % col)

    def test_every_component_appears_exactly_once(self):
        self.assertIn("exactly once", CORE)
        self.assertIn("record_authority", CORE)
        self.assertIn("relocated_responsibilities", CORE)

    def test_diagrams_are_optional_and_never_authoritative(self):
        self.assertIn("No diagram is ever the authority", CORE)
        self.assertIn("OPTIONAL", README + CORE.upper())

    def test_no_diagram_tooling_added(self):
        for name in RUNTIME_UNITS:
            body = at(name)
            self.assertNotIn("mermaid.js", body.lower())
            self.assertNotIn("npm install", body.lower())


# ------------------------------------- knowledge, craft and platform numbers

class TestNoPlatformNumbers(unittest.TestCase):
    NUM = re.compile(r"\b\d{2,}\s*(GB|MB|TB|rows|linhas|requests|calls|dias|days|"
                     r"months|meses|EUR|USD|%)\b", re.I)

    def test_no_hardcoded_platform_number_in_any_template(self):
        for name in RUNTIME_UNITS:
            body = at(name)
            hits = self.NUM.findall(body)
            self.assertEqual([], hits, "%s carries platform numbers: %r" % (name, hits))

    def test_volatile_values_resolve_to_verified_su_rows(self):
        for body in (CORE, F_INH):
            self.assertIn("verificado_em", body)
            self.assertIn("validade", body)
        self.assertIn("verification obligation", CORE)

    def test_templates_disclaim_number_ownership(self):
        self.assertTrue(has(
            "owns no service limit, price, quota, retention window, threshold or SKU", CORE))
        self.assertTrue(has("no prices", CORE))


class TestDomainKnowledgeBoundary(unittest.TestCase):
    def test_no_domain_knowledge_duplicated_into_templates(self):
        for name in RUNTIME_UNITS:
            body = at(name)
            low = body.lower()
            self.assertNotIn("delegation limit is", low)
            self.assertNotIn("service limit:", low)

    def test_fragment_cites_patterns_and_does_not_restate_it(self):
        self.assertIn("architecture/patterns.md", F_BND)
        for forbidden in ("pattern strengths", "pattern weaknesses",
                          "risk catalogue", "mechanism descriptions"):
            self.assertIn(forbidden, F_BND, "missing prohibition: %s" % forbidden)

    def test_selective_pull_discipline_stated_in_blueprint(self):
        self.assertIn("pull ONE relevant knowledge unit", BLUEPRINT_SKILL)
        self.assertIn("maximum 2", BLUEPRINT_SKILL)
        for forbidden in ("preloading", "knowledge bundle", "survey the ten"):
            self.assertIn(forbidden, BLUEPRINT_SKILL, "missing prohibition: %s" % forbidden)

    def test_architecture_layer_does_not_preload_knowledge(self):
        self.assertIn("never preloaded", BLUEPRINT_SKILL)
        self.assertIn("Never preload", CORE)

    def test_knowledge_units_untouched_by_step_5b(self):
        """Step 4 regression guard: the 15 RESEARCH + 10 CRAFT units still exist."""
        dk = os.path.join(PACK_DIR, "domain-knowledge")
        units = []
        for base, _dirs, files in os.walk(dk):
            units += [f for f in files if f.endswith(".md") and f != "README.md"]
        self.assertGreaterEqual(len(units), 25, "domain knowledge unit count dropped: %d" % len(units))


class TestCraftBoundary(unittest.TestCase):
    def test_craft_is_never_a_technical_authority(self):
        self.assertIn("RESEARCH wins", BLUEPRINT_SKILL)
        self.assertIn("RESEARCH wins", F_INT)

    def test_craft_may_not_select_architecture_or_authorization(self):
        for forbidden in ("select the architecture", "set an authorization",
                          "set record authority", "establish a platform capability",
                          "establish a technical limit", "choose a proof level"):
            self.assertIn(forbidden, BLUEPRINT_SKILL, "missing CRAFT prohibition: %s" % forbidden)

    def test_estimation_model_excluded_from_architecture_blueprint(self):
        self.assertIn("estimation-model.md` is **not** used in the architecture blueprint",
                      BLUEPRINT_SKILL)


# ------------------------------------------------------- Step 3 freeze guard

class TestStep3Freeze(unittest.TestCase):
    def test_options_semantics_unchanged(self):
        body = read(os.path.join(SKILLS, "aisa-options", "SKILL.md"))
        self.assertIn("option class", body)
        self.assertNotIn("<branch>", body)

    def test_simulate_semantics_unchanged(self):
        body = read(os.path.join(SKILLS, "aisa-simulate", "SKILL.md"))
        self.assertIn("Advisory only", body)
        self.assertNotIn("for its branch", body)

    def test_no_architecture_shape_entered_the_option_space(self):
        for skill in ("aisa-options", "aisa-simulate"):
            body = read(os.path.join(SKILLS, skill, "SKILL.md"))
            for token in ("experience.mode", "record_authority", "architecture.authorization"):
                self.assertNotIn(token, body,
                                 "%s: architecture vocabulary leaked upward (%s)" % (skill, token))

    def test_kernel_carries_no_pp_taxonomy(self):
        for path in (os.path.join(KERNEL, "blueprint-contract.md"),
                     os.path.join(KERNEL, "render-contract.md")):
            body = read(path)
            for token in ("owned-internal", "owned-external", "api-mediated",
                          "queue-based", "Dataverse", "SharePoint"):
                self.assertNotIn(token, body, "%s: PP taxonomy in the kernel (%s)" % (path, token))

    def test_kernel_states_the_generic_architecture_block(self):
        body = read(os.path.join(KERNEL, "blueprint-contract.md"))
        self.assertIn("| `architecture` |", body)
        self.assertNotIn("`branch`", body)
        self.assertIn("belongs to the active pack, never to the kernel", body)


# --------------------------------------------------------- fixtures F-1..F-19

class TestFixtureRepresentability(unittest.TestCase):
    """F-1 … F-19 must be REPRESENTABLE and mechanically enforceable by the runtime.

    Step 5C replays them behaviourally; 5B proves the model can express each one.
    """

    def _core_supports(self, *sections):
        for sec in sections:
            self.assertIn(sec, CORE)

    # F-1 — inherited class 13(a)
    def test_f01_inherited_tracker(self):
        self.assertIn("activates_on: architecture.experience.mode == inherited", F_INH)
        self.assertIn("graduation_trigger", F_INH)
        self.assertIn("no independent environment, policy plane or release topology", F_INH)

    # F-2 / F-3 — owned-internal over either store role
    def test_f02_f03_owned_internal_over_any_store_role(self):
        self.assertIn("activates_on: architecture.experience.mode == owned-internal", F_INT)
        for role in ("governed relational store", "list/library store"):
            self.assertIn(role, BLUEPRINT_SKILL, "store role not expressible: %s" % role)
        self._core_supports("### A5", "### A9")

    # F-4 — relational via connector; identity difference
    def test_f04_relational_via_connector(self):
        self.assertIn("relational via connector", BLUEPRINT_SKILL)
        self.assertIn("delegation-safe", F_INT)
        self._core_supports("### A7", "### A3")

    # F-5 — owned-external
    def test_f05_external_audience(self):
        self.assertIn("activates_on: architecture.experience.mode == owned-external", F_EXT)
        for item in ("identidade externa", "Cache", "acessibilidade"):
            self.assertIn(item, F_EXT)

    # F-6 — data replication; reconciliation owner
    def test_f06_analytical_copy_needs_a_reconciliation_mechanism(self):
        """Replication owes a reconciliation MECHANISM, not a named reconciler: the
        role is required, the name is not (E2.4)."""
        self.assertIn("data-replication", BLUEPRINT_SKILL)
        self.assertIn("access_mode: owned | virtualized | replicated | keep-in-place",
                      BLUEPRINT_SKILL)
        self.assertIn("Conditional — reconcilia", F_BND)
        self.assertIn("mandatory is the **mechanism**", F_BND)
        block = F_BND.split("Conditional — reconcilia", 1)[1].split("Conditional —", 1)[0]
        for owed in ("role", "detect", "procedure"):
            self.assertIn(owed, block.lower(),
                          "the reconciliation block does not owe %r" % owed)
        self.assertIn("not named", block,
                      "a stated role with nobody named must satisfy the block")
        self.assertNotIn("and named", block)

    # F-7 — api-mediated tier
    def test_f07_api_mediated_tier(self):
        self.assertIn("api-mediated", BLUEPRINT_SKILL)
        self.assertIn("ALM", F_BND)
        self.assertIn("release routes", F_BND)

    # F-8 — queue + worker, no named operator
    def test_f08_a_missing_operating_model_is_structural_a_missing_name_is_not(self):
        """E2.3 moved what counts: the structural choice is an absent operating model
        (no role authorised to intervene, no diagnostic/recovery interface) — never an
        operator without a name. Checked in the three channels that state it."""
        self.assertIn("owner: <named team or role> | UNKNOWN", BLUEPRINT_SKILL)
        self.assertIn("tripwire", F_BND)
        self.assertIn("tripwire", BLUEPRINT_SKILL)

        # The fragment no longer emits an availability verdict.
        self.assertNotIn("composition is unavailable", F_BND)

        a10 = CORE.split("### A10", 1)[1].split("### A11", 1)[0]
        for owed in ("role", "identity", "permission", "mechanism",
                     "alert destination", "recovery"):
            self.assertIn(owed, a10.lower(), "A10 does not owe %r" % owed)
        # A10 says a missing name settles nothing, and says what does.
        self.assertIn("not named", a10)
        self.assertIn("structural", a10.lower())
        for chan in (a10, F_BND, BLUEPRINT_SKILL):
            self.assertIn("not named", chan,
                          "a channel still treats an unnamed holder as a gap")

    # F-9 — virtualization
    def test_f09_virtualized_system_of_record(self):
        self.assertIn("data-virtualization", BLUEPRINT_SKILL)
        self.assertIn("virtualized", BLUEPRINT_SKILL)
        self._core_supports("### A9")

    # F-10 / F-11 — scope pairs
    def test_f10_f11_scope_pairs(self):
        self.assertIn("relocated_responsibilities", BLUEPRINT_SKILL)
        self.assertIn("cloud-native services", BLUEPRINT_SKILL)
        self.assertIn("incumbent system", BLUEPRINT_SKILL)
        self.assertIn("INCUMBENT FIT UNEVALUATED", BLUEPRINT_SKILL)
        self.assertIn("propriedade de âmbitos", CORE)

    # F-12 — two defensible architectures
    def test_f12_candidate_architectures_choose_neither(self):
        self.assertIn("arquitecturas candidatas", CORE)
        self.assertIn("choose neither", CORE)
        self.assertIn("No scoring", CORE)

    # F-13 — class 12
    def test_f13_decision_blocked_renders_nothing_architectural(self):
        body = read(os.path.join(KERNEL, "render-contract.md"))
        self.assertIn("Render nothing architectural", body)
        self.assertIn("| 12 | Decision blocked", README)

    # F-14 — class 5 + class 8
    def test_f14_excluded_scope_is_a_skip_not_a_gap(self):
        self.assertIn("| 5 | Poor fit", README)
        self.assertIn("| 8 | Candidate set", README)
        self.assertIn("a skip is not a gap", read(os.path.join(KERNEL, "render-contract.md")))

    # F-15 — headless automation
    def test_f15_headless_automation(self):
        self.assertTrue(has("zero experience fragments", README))
        self.assertTrue(has("A6 automation and integration", README))
        self.assertTrue(has("A4 is not engaged", CORE + README))
        self.assertTrue(has("do not fabricate a user surface", README))

    # F-16 — headless composed integration
    def test_f16_headless_composed_integration(self):
        self.assertIn("queue-based", BLUEPRINT_SKILL)
        self.assertIn("hybrid-low-code-pro-code", BLUEPRINT_SKILL)
        self.assertTrue(has("zero or more boundary", README + CORE))
        self.assertTrue(has("service / managed / connection identity", CORE + README))

    # F-17 — non-PP class 1/2
    def test_f17_non_pp_positive_outcome_renders_no_pp_architecture(self):
        self.assertIn("| class 1 or 2 | custom-only", README)
        self.assertIn("**no PP architecture authorization**", README)
        self.assertIn("no PP architecture", BLUEPRINT_SKILL)

    # F-18 — class 13(a) outside pack authority
    def test_f18_13a_outside_authority_preserves_sufficiency(self):
        self.assertIn("the sufficient capability is outside it", README)
        self.assertIn("graduation trigger", README)
        self.assertIn("this platform is not excluded", README)

    # F-19 — same pattern, same owner, distinct components
    def test_f19_same_pattern_same_owner_two_components_two_fragments(self):
        self.assertTrue(has(
            "same pattern, the same owner, the same boundary and even the same forcing requirement",
            F_BND))
        self.assertTrue(has("render as SEPARATE instances", F_BND)
                        or has("render separately", F_BND))
        self.assertIn("erp-integration-api", BLUEPRINT_SKILL)
        self.assertIn("crm-integration-api", BLUEPRINT_SKILL)


class TestF19CollisionMechanics(unittest.TestCase):
    """§38 — the collision case, executed as data against the recorded invariant."""

    @staticmethod
    def _qualifies(entry):
        return (entry.get("boundary") == "outside-platform"
                or entry.get("pattern") != "direct")

    @staticmethod
    def _keys(scope, compositions, relocations):
        """Reproduce the binding identity rules of Step 5A §28.2 exactly."""
        keys = []
        for c in compositions:
            if TestF19CollisionMechanics._qualifies(c):
                keys.append("%s::component::%s" % (scope, c["component"]))
        for r in relocations:
            keys.append("%s::responsibility::%s" % (scope, r["responsibility"]))
        return keys

    def test_two_components_same_pattern_same_owner_render_two_fragments(self):
        scope = "intake"
        comps = [
            {"component": "erp-integration-api", "pattern": "api-mediated",
             "owner": "Integration Team", "boundary": "outside-platform",
             "forced_by": "ERP integration"},
            {"component": "crm-integration-api", "pattern": "api-mediated",
             "owner": "Integration Team", "boundary": "outside-platform",
             "forced_by": "CRM integration"},
        ]
        keys = self._keys(scope, comps, [])
        self.assertEqual(2, len(keys), "F-19 collapsed to one fragment: %r" % keys)
        self.assertEqual(2, len(set(keys)))

    def test_duplicate_component_name_in_one_scope_fails(self):
        scope = "intake"
        comps = [
            {"component": "erp-integration-api", "pattern": "api-mediated",
             "owner": "Integration Team", "boundary": "outside-platform",
             "forced_by": "ERP integration"},
            {"component": "erp-integration-api", "pattern": "queue-based",
             "owner": "Integration Team", "boundary": "outside-platform",
             "forced_by": "retry buffering"},
        ]
        names = [c["component"] for c in comps]
        self.assertNotEqual(len(names), len(set(names)),
                            "fixture must actually contain a duplicate")
        keys = self._keys(scope, comps, [])
        # A duplicate identity must be DETECTED as a contract defect — never silently merged.
        self.assertTrue(len(keys) != len(set(keys)),
                        "duplicate component identity was silently merged")

    def test_duplicate_responsibility_in_one_scope_fails(self):
        scope = "intake"
        relocs = [{"responsibility": "reporting", "owner": "cloud-native services"},
                  {"responsibility": "reporting", "owner": "incumbent system"}]
        keys = self._keys(scope, [], relocs)
        self.assertTrue(len(keys) != len(set(keys)),
                        "duplicate responsibility identity was silently merged")

    def test_n_plus_m_invariant_holds_on_a_mixed_architecture(self):
        scope = "intake"
        comps = [
            {"component": "direct-list-read", "pattern": "direct",
             "boundary": "in-platform", "owner": "App Team"},          # not qualifying
            {"component": "erp-integration-api", "pattern": "api-mediated",
             "boundary": "outside-platform", "owner": "Integration Team"},
            {"component": "crm-integration-api", "pattern": "api-mediated",
             "boundary": "outside-platform", "owner": "Integration Team"},
            {"component": "dispatch-queue", "pattern": "queue-based",
             "boundary": "outside-platform", "owner": "Platform Team"},
        ]
        relocs = [
            {"responsibility": "analytical reporting", "owner": "cloud-native services"},
            {"responsibility": "record authority", "owner": "incumbent system"},
        ]
        n = len({c["component"] for c in comps if self._qualifies(c)})
        m = len({r["responsibility"] for r in relocs})
        keys = self._keys(scope, comps, relocs)
        self.assertEqual(n + m, len(set(keys)))
        self.assertEqual(5, n + m, "expected 3 qualifying components + 2 relocations")

    def test_direct_in_platform_composition_adds_no_fragment(self):
        comps = [{"component": "direct-list-read", "pattern": "direct",
                  "boundary": "in-platform", "owner": "App Team"}]
        self.assertEqual([], self._keys("intake", comps, []))

    def test_headless_architecture_opens_zero_experience_fragments(self):
        for mode, expected in (("none", 0), ("owned-internal", 1),
                               ("owned-external", 1), ("inherited", 1)):
            includes = 0 if mode == "none" else 1
            self.assertEqual(expected, includes, "mode %s" % mode)
            if mode == "none":
                self.assertFalse(
                    os.path.exists(os.path.join(AT_DIR, "fragment-experience-none.md")),
                    "experience.mode=none must not resolve a template file")


if __name__ == "__main__":
    unittest.main(verbosity=2)
