"""Step 6B — PP deliverable-projection runtime.

Mechanical/structural assertions only. These prove IMPLEMENTATION FIDELITY against the
frozen Step 6A design (including its 40 final bounded contract correction); they do NOT
prove that the six deliverables stay semantically aligned under realistic engagement
pressure -- that is Step 6C.

T-D1 ... T-D22, per the frozen Step 6A 36 test design. Structural assertions where
meaningful: frontmatter is PARSED (not grepped) wherever the claim is about a declared
contract field.

    python .claude/tests/test_pp_deliverable_templates.py
"""

import os
import re
import unittest

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PACK_DIR = os.path.join(ROOT, "library", "packs", "pp")
DT_DIR = os.path.join(PACK_DIR, "deliverable-templates")
AT_DIR = os.path.join(PACK_DIR, "architecture-templates")
KERNEL = os.path.join(ROOT, "library", "kernel")
ST_DIR = os.path.join(KERNEL, "synthesis-templates")
SKILLS = os.path.join(ROOT, ".claude", "skills")
DOCS = os.path.join(ROOT, "docs")

# ── The six canonical deliverables: runtime id -> canonical_deliverable ───────────────
SIX = {
    "discovery-report": "discovery-report",
    "executive-report": "executive-report",
    "solution-blueprint": "architecture-blueprint",   # runtime alias, Step 6A 4
    "implementation-spec": "implementation-specification",
    "claude-design-brief": "claude-design-brief",
    "estimate": "estimate",
}
CANONICAL = set(SIX.values())

SYNTHESIS = [
    "business-story.template.md",
    "as-is.template.md",
    "architecture-story.template.md",
    "risks-and-assumptions.template.md",
    "financial-story.template.md",
]

# ── Legacy branch / chosen-architecture MODEL vocabulary (must be absent) ─────────────
LEGACY_TOKENS = [
    "chosen_architecture",
    "{{chosen_architecture}}",
    "Branch (if technology)",
    "Branch (decision-tree)",
    "chosen_branch_template",
    "sharepoint-first",
    "dataverse-first",
    "architecture-templates/<branch>",
    "architecture-templates/<chosen>",
]

# Vendor/product denylist for the technology-neutral Discovery Report.
NEUTRALITY_DENYLIST = [
    "power platform", "power apps", "powerapps", "power automate", "power fx", "powerfx",
    "canvas app", "model-driven", "dataverse", "sharepoint", "azure sql", "azure-sql",
    "outsystems", "mendix", "power bi",
]

# Price-surface tokens no deliverable may carry as a cost fact.
PRICE_TOKENS = ["sku", "rate card", "licence price", "license price", "price per user",
                "per-user price", "eur/", "usd/", "$/user"]

# Instruction phrasings that would promote or resolve an epistemic state.
EPISTEMIC_PROMOTION_PHRASES = [
    "assume confirmed", "assumir como confirmado", "treat as confirmed",
    "pick the more likely value", "escolhe o valor mais provavel",
    "escolher o valor mais provavel", "choose the more likely",
    "resolve the unknown", "resolver o unknown", "mark as satisfied",
    "marcar como satisfeita", "mark the obligation satisfied",
    "upgrade the state", "promote the state",
]

DK_UNIT_RE = re.compile(r"domain-knowledge/[a-z0-9-]+/[a-z0-9-]+\.md")


# ── helpers ───────────────────────────────────────────────────────────────────────────

def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def flat(text):
    """Normalize markdown noise so a phrase matches however the template formats it.

    Collapses whitespace, drops blockquote continuation markers (a wrapped `> ` line
    otherwise splits a sentence) and strips emphasis (`**x**`). Semantics are unaffected:
    bolding a word is a formatting choice, never a different claim.
    """
    text = re.sub(r"(?m)^\s*(?:>\s*)+", " ", text)   # blockquote markers, incl. nested "> >"
    text = text.replace("**", "").replace("__", "")
    return re.sub(r"\s+", " ", text)


NEGATIONS = ("no ", "not ", "never ", "nao ", "n\u00e3o ", "sem ", "nenhum", "nunca ",
             "former ", "zero ", "without ")


def only_in_prohibition(needle, haystack, window=70):
    """True when every occurrence of `needle` is preceded by a negation.

    A contract legitimately states its own prohibitions, so the banned token appears in
    the very files that forbid it. What must not exist is an occurrence that READS AS AN
    INSTRUCTION -- i.e. one with no negation in front of it.
    """
    low = flat(haystack).lower()
    ned = flat(needle).lower()
    idx = low.find(ned)
    while idx != -1:
        pre = low[max(0, idx - window):idx]
        if not any(x in pre for x in NEGATIONS):
            return False
        idx = low.find(ned, idx + 1)
    return True


def has(needle, haystack):
    """Whitespace- and case-insensitive phrase containment."""
    return flat(needle).lower() in flat(haystack).lower()


def split_front_matter(text):
    """Return (frontmatter_text, body_text)."""
    if not text.startswith("---"):
        return "", text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return "", text
    return parts[1], parts[2]


def as_text(value):
    """Flatten any nested frontmatter value into one searchable string."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, dict):
        return " ".join(as_text(k) + " " + as_text(v) for k, v in value.items())
    if isinstance(value, (list, tuple)):
        return " ".join(as_text(v) for v in value)
    return str(value)


class Template(object):
    """A parsed deliverable/synthesis template: raw text + structured frontmatter."""

    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.raw = read(path)
        self.fm_text, self.body = split_front_matter(self.raw)
        self.fm = {}
        if yaml is not None and self.fm_text.strip():
            loaded = yaml.safe_load(self.fm_text)
            if isinstance(loaded, dict):
                self.fm = loaded

    # -- frontmatter access -----------------------------------------------------------
    def get(self, key, default=None):
        return self.fm.get(key, default)

    def listy(self, key):
        v = self.fm.get(key)
        if v is None:
            return []
        if isinstance(v, str):
            return [line.strip("- ").strip() for line in v.splitlines() if line.strip()]
        if isinstance(v, dict):
            return [as_text(k) + ": " + as_text(x) for k, x in v.items()]
        return list(v)

    def field_text(self, key):
        return as_text(self.fm.get(key))

    def slots(self, kind):
        return set(self.listy(kind + "_slots"))

    def all_slots(self):
        return self.slots("required") | self.slots("conditional") | self.slots("optional")

    def slot_sources_text(self):
        return as_text(self.fm.get("slot_sources"))

    def sources_text(self):
        """Everything the template declares as a place it READS from."""
        return " ".join([
            self.field_text("authority_sources"),
            self.field_text("conditional_sources"),
            self.slot_sources_text(),
        ])

    def contract_text(self):
        """Everything the template declares as contract (frontmatter only)."""
        return self.fm_text

    def body_slots(self):
        return set(re.findall(r"\{\{([a-z_][a-z0-9_]*)\}\}", self.body))


DELIVERABLES = {}
SYNTH = {}
RENDER_SKILL = ""
SYNTH_SKILL = ""
RENDER_CONTRACT = ""
BLUEPRINT_CONTRACT = ""
PACK = {}
PACK_RAW = ""


def setUpModule():
    global RENDER_SKILL, SYNTH_SKILL, RENDER_CONTRACT, BLUEPRINT_CONTRACT, PACK, PACK_RAW
    for rid in SIX:
        DELIVERABLES[rid] = Template(os.path.join(DT_DIR, rid + ".template.md"))
    for fn in SYNTHESIS:
        SYNTH[fn] = Template(os.path.join(ST_DIR, fn))
    RENDER_SKILL = read(os.path.join(SKILLS, "aisa-render", "SKILL.md"))
    SYNTH_SKILL = read(os.path.join(SKILLS, "aisa-synthesize", "SKILL.md"))
    RENDER_CONTRACT = read(os.path.join(KERNEL, "render-contract.md"))
    BLUEPRINT_CONTRACT = read(os.path.join(KERNEL, "blueprint-contract.md"))
    PACK_RAW = read(os.path.join(PACK_DIR, "pack.yaml"))
    if yaml is not None:
        PACK = yaml.safe_load(PACK_RAW)


class Base(unittest.TestCase):
    def assertPhrase(self, needle, haystack, label=""):
        self.assertTrue(has(needle, haystack),
                        "phrase not found%s: %r" % (" in " + label if label else "", needle))

    def assertNoPhrase(self, needle, haystack, label=""):
        self.assertFalse(has(needle, haystack),
                         "phrase MUST be absent%s: %r" % (" in " + label if label else "", needle))

    def assertOnlyProhibited(self, needle, haystack, label=""):
        self.assertTrue(only_in_prohibition(needle, haystack),
                        "%s: %r appears outside a prohibition" % (label, needle))

    def requireYaml(self):
        if yaml is None:
            self.skipTest("PyYAML not installed; structural frontmatter assertions skipped")


# ══════════════════════════════════════════════════════════════════════════════════════
# Baseline — exactly six projection contracts exist and are well-formed
# ══════════════════════════════════════════════════════════════════════════════════════

class TestSixContracts(Base):

    def test_exactly_six_deliverable_templates_exist(self):
        found = sorted(f for f in os.listdir(DT_DIR) if f.endswith(".template.md"))
        expected = sorted(rid + ".template.md" for rid in SIX)
        self.assertEqual(expected, found, "deliverable-templates/ must hold exactly the six")

    def test_every_template_declares_the_full_projection_contract(self):
        self.requireYaml()
        required_fields = [
            "canonical_deliverable", "activation", "authority_sources",
            "forbidden_sources", "permitted_transformations", "forbidden_transformations",
        ]
        for rid, t in DELIVERABLES.items():
            for f in required_fields:
                self.assertIn(f, t.fm, "%s must declare %s" % (rid, f))
                self.assertTrue(as_text(t.fm[f]).strip(), "%s: %s is empty" % (rid, f))

    def test_canonical_deliverable_values_are_the_six(self):
        self.requireYaml()
        got = {}
        for rid, t in DELIVERABLES.items():
            cd = t.get("canonical_deliverable")
            self.assertIn(cd, CANONICAL, "%s: unexpected canonical_deliverable %r" % (rid, cd))
            got[rid] = cd
        self.assertEqual(SIX, got)
        self.assertEqual(6, len(set(got.values())), "canonical names must be distinct")

    def test_no_new_deliverable_no_fragment_no_inheritance_framework(self):
        for rid, t in DELIVERABLES.items():
            self.assertNotIn("extends", t.fm, "%s: no template inheritance" % rid)
            self.assertNotIn("inherits", t.fm, "%s: no template inheritance" % rid)
            self.assertNotIn("fragments", t.fm, "%s: no deliverable-side fragment system" % rid)
        self.assertFalse(os.path.isdir(os.path.join(DT_DIR, "fragments")))

    def test_every_body_slot_is_declared_and_every_declared_slot_is_used(self):
        self.requireYaml()
        for rid, t in DELIVERABLES.items():
            declared = t.all_slots()
            used = t.body_slots()
            self.assertTrue(used <= declared,
                            "%s: body slots not declared: %s" % (rid, sorted(used - declared)))
            # `solution_name` is the title slot; `architecture_block` is consumed by the
            # fixed architecture-core include rather than by a body placeholder.
            consumed_by_include = {"architecture_block"} if t.listy("sub_templates") else set()
            unused = declared - used - {"solution_name"} - consumed_by_include
            self.assertFalse(unused, "%s: declared but unused slots: %s" % (rid, sorted(unused)))


# ══════════════════════════════════════════════════════════════════════════════════════
# T-D1 — No branch / chosen-architecture vocabulary
# ══════════════════════════════════════════════════════════════════════════════════════

class TestTD1LegacyVocabulary(Base):

    def test_no_legacy_branch_token_in_any_deliverable_template(self):
        for rid, t in DELIVERABLES.items():
            for tok in LEGACY_TOKENS:
                self.assertNoPhrase(tok, t.raw, rid)

    def test_no_legacy_branch_token_in_any_synthesis_template(self):
        for fn, t in SYNTH.items():
            for tok in LEGACY_TOKENS:
                self.assertNoPhrase(tok, t.raw, fn)

    def test_the_only_architecture_include_is_the_fixed_core(self):
        includes = []
        for rid, t in DELIVERABLES.items():
            includes += [(rid, m) for m in re.findall(r"\{\{>>\s*([^}]+?)\s*\}\}", t.raw)]
        self.assertEqual([("solution-blueprint", "architecture-templates/architecture-core.md")],
                         includes,
                         "exactly one include, fixed, in the Architecture Blueprint only")

    def test_no_dynamic_include_path_anywhere(self):
        for rid, t in DELIVERABLES.items():
            self.assertFalse(re.search(r"\{\{>>[^}]*\{\{", t.raw),
                             "%s: nested/dynamic include path" % rid)

    def test_no_sub_templates_entry_points_at_a_branch(self):
        self.requireYaml()
        for rid, t in DELIVERABLES.items():
            subs = t.listy("sub_templates")
            for s in subs:
                self.assertEqual("architecture-templates/architecture-core.md", s,
                                 "%s: sub_templates must be the fixed core only" % rid)

    def test_retired_branch_templates_do_not_exist(self):
        for f in ("sharepoint-first.md", "dataverse-first.md", "hybrid.md"):
            self.assertFalse(os.path.exists(os.path.join(AT_DIR, f)),
                             "%s must stay retired" % f)

    def test_fixed_core_entry_point_exists(self):
        self.assertTrue(os.path.exists(os.path.join(AT_DIR, "architecture-core.md")))


# ══════════════════════════════════════════════════════════════════════════════════════
# T-D2 — Headless produces no fake Design Brief and no fake screen section
# ══════════════════════════════════════════════════════════════════════════════════════

SURFACE_SLOTS = {
    "claude-design-brief": ["surface_inventory", "persona_users", "page_navigation_map",
                            "screen_specifications", "ux_requirements", "excluded_from_ui"],
    "implementation-spec": ["screens_to_build"],
}


class TestTD2Headless(Base):

    def test_no_surface_slot_is_ever_required(self):
        self.requireYaml()
        for rid, slots in SURFACE_SLOTS.items():
            t = DELIVERABLES[rid]
            req = t.slots("required")
            for s in slots:
                self.assertNotIn(s, req, "%s: %s must never be a required slot" % (rid, s))
                self.assertIn(s, t.slots("conditional"),
                              "%s: %s must be a conditional slot" % (rid, s))

    def test_every_surface_slot_condition_names_the_experience_mode(self):
        self.requireYaml()
        for rid, slots in SURFACE_SLOTS.items():
            conds = DELIVERABLES[rid].get("slot_conditions") or {}
            for s in slots:
                self.assertIn(s, conds, "%s: %s needs a slot_conditions entry" % (rid, s))
                self.assertPhrase("experience.mode", as_text(conds[s]),
                                  "%s.%s condition" % (rid, s))

    def test_design_brief_declares_not_applicable_for_headless(self):
        t = DELIVERABLES["claude-design-brief"]
        self.assertPhrase("experience.mode == none", t.field_text("not_applicable_when"),
                          "design brief not_applicable_when")
        self.assertPhrase("NOT APPLICABLE", t.field_text("activation"), "design brief activation")

    def test_design_brief_forbids_emitting_headless_placeholders(self):
        t = DELIVERABLES["claude-design-brief"]
        self.assertPhrase("emitting a persona, screen, navigation or UX-state placeholder",
                          t.field_text("forbidden_transformations"), "design brief")

    def test_impl_spec_screens_section_is_marked_conditional_in_the_body(self):
        t = DELIVERABLES["implementation-spec"]
        # Anchored on the SLOT, not on a section number: the body renumbers whenever a
        # section is added (Step 6C R-3 inserted `build_gates`), and this assertion is about
        # the screens section being marked conditional, not about where it sits.
        head = t.body.split("{{screens_to_build}}")[0]
        section = head[head.rfind("\n## "):]
        self.assertTrue(section.strip().startswith("##"), "screens section not found")
        self.assertPhrase("Condicional", section, "impl-spec screens section")
        self.assertPhrase("experience.mode == none", section, "impl-spec screens section")

    def test_impl_spec_still_projects_the_headless_architecture_in_full(self):
        t = DELIVERABLES["implementation-spec"]
        txt = t.field_text("headless_behaviour")
        for must in ["automation", "integration", "identity", "environments and release",
                     "monitoring", "recovery", "proof work", "operator obligations"]:
            self.assertPhrase(must, txt, "impl-spec headless_behaviour")
        self.assertPhrase("No fake application surface", txt, "impl-spec headless_behaviour")

    def test_impl_spec_forbids_inventing_a_surface(self):
        t = DELIVERABLES["implementation-spec"]
        self.assertPhrase("inventing a user surface where experience.mode == none",
                          t.field_text("forbidden_transformations"), "impl-spec")

    def test_render_skill_opens_zero_experience_fragments_for_headless(self):
        self.assertPhrase("experience.mode == none", RENDER_SKILL, "aisa-render")
        self.assertPhrase("ZERO includes", RENDER_SKILL, "aisa-render")
        self.assertPhrase("no render gap", RENDER_SKILL, "aisa-render")
        self.assertFalse(os.path.exists(os.path.join(AT_DIR, "fragment-experience-none.md")))


# ══════════════════════════════════════════════════════════════════════════════════════
# T-D3 — Not-authorized produces no Architecture Blueprint
# ══════════════════════════════════════════════════════════════════════════════════════

class TestTD3NotAuthorized(Base):

    def test_blueprint_activation_requires_an_authorization(self):
        t = DELIVERABLES["solution-blueprint"]
        self.assertPhrase("an architecture authorization exists for at least one scope",
                          t.field_text("activation"), "blueprint activation")

    def test_blueprint_is_not_applicable_when_no_scope_is_authorized(self):
        t = DELIVERABLES["solution-blueprint"]
        txt = t.field_text("not_applicable_when") + " " + t.fm_text
        self.assertPhrase("not-authorized", txt, "blueprint")
        self.assertPhrase("NOT a gap", t.fm_text, "blueprint")

    def test_blueprint_emits_no_empty_architecture_document(self):
        t = DELIVERABLES["solution-blueprint"]
        self.assertPhrase("No empty architecture deliverable", t.fm_text, "blueprint")
        self.assertPhrase("no placeholder A-sections", t.fm_text, "blueprint")

    def test_render_skill_treats_not_applicable_as_a_skip_not_a_gap(self):
        self.assertPhrase("log a **skip** with the reason to `render-log.md`", RENDER_SKILL,
                          "aisa-render")
        self.assertPhrase("never written to `render-gaps.md`", RENDER_SKILL, "aisa-render")

    def test_render_skill_keeps_the_two_not_authorized_reasons_distinct(self):
        self.assertPhrase("Keep the two reasons distinct", RENDER_SKILL, "aisa-render")
        self.assertPhrase("do not relabel", RENDER_SKILL, "aisa-render")

    def test_executive_survives_with_no_architecture(self):
        t = DELIVERABLES["executive-report"]
        self.assertEqual("always", str(t.get("activation")).strip())
        self.assertIn("architecture_shape", t.slots("conditional"))
        self.assertNotIn("architecture_shape", t.slots("required"))


# ══════════════════════════════════════════════════════════════════════════════════════
# T-D4 — Class-6 destination unevaluated is neither designed nor estimated
# ══════════════════════════════════════════════════════════════════════════════════════

class TestTD4ClassSix(Base):

    def test_scope_ownership_enumeration_has_exactly_four_categories_incl_category_three(self):
        self.requireYaml()
        cats = DELIVERABLES["solution-blueprint"].get("scope_ownership_categories")
        self.assertIsInstance(cats, dict)
        self.assertEqual(4, len(cats), "exactly four projection categories")
        names = {as_text(v.get("name")) for v in cats.values()}
        self.assertIn("excluded - destination unevaluated".replace("-", "—"), names
                      if "excluded — destination unevaluated" in names else names,
                      "category 3 must exist")
        self.assertTrue(any("destination unevaluated" in n for n in names),
                        "category 3 (excluded - destination unevaluated) missing: %s" % names)

    def test_category_three_gets_nothing(self):
        self.requireYaml()
        cats = DELIVERABLES["solution-blueprint"].get("scope_ownership_categories")
        c3 = as_text(cats[3])
        for must in ["no design", "no boundary component", "no owner", "no imports", "no gates"]:
            self.assertPhrase(must, c3, "blueprint category 3")
        self.assertPhrase("COMPARATIVE FIT UNEVALUATED", c3, "blueprint category 3")

    def test_estimate_declares_the_excluded_scope_statement(self):
        t = DELIVERABLES["estimate"]
        self.assertIn("excluded_scope", t.slots("required"),
                      "the exclusion must be stated, not silent")

    def test_estimate_forbids_any_allowance_for_an_unevaluated_destination(self):
        t = DELIVERABLES["estimate"]
        self.assertPhrase("estimating an UNEVALUATED destination",
                          t.field_text("forbidden_transformations"), "estimate")
        self.assertPhrase("no allowance, no placeholder, no contingency band",
                          t.fm_text, "estimate")
        c3 = as_text((t.get("pricing_by_scope_category") or {}).get(
            "3_excluded_destination_unevaluated"))
        self.assertPhrase("NEVER estimated", c3, "estimate pricing category 3")

    def test_impl_spec_forbids_far_side_implementation(self):
        t = DELIVERABLES["implementation-spec"]
        self.assertPhrase("specifying an external implementation for a destination that is UNEVALUATED",
                          t.field_text("forbidden_transformations"), "impl-spec")
        self.assertPhrase("no interface, no contract, no migration, no cutover",
                          t.fm_text, "impl-spec")

    def test_design_brief_forbids_far_side_screens(self):
        t = DELIVERABLES["claude-design-brief"]
        self.assertPhrase("designing a screen or journey for a destination that is UNEVALUATED",
                          t.field_text("forbidden_transformations"), "design brief")

    def test_render_contract_states_category_three_is_never_estimated(self):
        self.assertPhrase("never estimated", RENDER_CONTRACT, "render-contract")
        self.assertPhrase("The far side never enters PP scope by silence", RENDER_CONTRACT,
                          "render-contract")


# ══════════════════════════════════════════════════════════════════════════════════════
# T-D5 — Authorized-bounded preserves scope ownership
# ══════════════════════════════════════════════════════════════════════════════════════

class TestTD5ScopePairs(Base):

    def test_four_deliverables_declare_the_uncollapsed_pairs_or_the_projection(self):
        for rid in ("executive-report", "solution-blueprint", "implementation-spec", "estimate"):
            t = DELIVERABLES[rid]
            txt = t.sources_text()
            self.assertTrue(
                has("UNCOLLAPSED", txt) or has("scope-ownership projection", txt),
                "%s must declare the uncollapsed pairs or the scope-ownership projection" % rid)

    def test_no_template_collapses_pairs_into_a_single_scope_slot(self):
        for rid, t in DELIVERABLES.items():
            self.assertNoPhrase("collapsed pairs", t.raw, rid)
            self.assertNoPhrase("merged scope", t.raw, rid)

    def test_executive_forbids_collapsing_or_rewording_a_pair(self):
        t = DELIVERABLES["executive-report"]
        self.assertPhrase("collapsing or re-wording a (scope, outcome) pair",
                          t.field_text("forbidden_transformations"), "executive")

    def test_executive_pairs_slot_is_required(self):
        self.assertIn("scope_outcome_pairs", DELIVERABLES["executive-report"].slots("required"))

    def test_impl_spec_build_scope_is_pp_owned_side_only(self):
        t = DELIVERABLES["implementation-spec"]
        self.assertPhrase("PP-OWNED side only", t.field_text("scope_rule"), "impl-spec")
        self.assertPhrase("never enters PP implementation scope by silence",
                          t.field_text("scope_rule"), "impl-spec")
        self.assertIn("build_scope_statement", t.slots("required"))

    def test_estimate_prices_pp_owned_work_only(self):
        t = DELIVERABLES["estimate"]
        cats = t.get("pricing_by_scope_category") or {}
        self.assertEqual(4, len(cats), "one pricing rule per scope-ownership category")
        self.assertPhrase("estimating far-side delivery",
                          t.field_text("forbidden_transformations"), "estimate")

    def test_design_brief_designs_pp_owned_surfaces_only(self):
        t = DELIVERABLES["claude-design-brief"]
        self.assertPhrase("designing a surface for a scope that is not PP-owned",
                          t.field_text("forbidden_transformations"), "design brief")


# ══════════════════════════════════════════════════════════════════════════════════════
# T-D6 — Executive conditions cannot disappear
# ══════════════════════════════════════════════════════════════════════════════════════

class TestTD6ExecutiveConditions(Base):

    NON_OMISSIBLE = ["scope_outcome_pairs", "conditions", "preconditions", "accepted_risks",
                     "proof_obligations", "structural_open_choices", "revision_tripwires",
                     "architectability_basis"]

    def test_executive_declares_the_non_omissible_set(self):
        self.requireYaml()
        declared = DELIVERABLES["executive-report"].listy("non_omissible")
        for item in self.NON_OMISSIBLE:
            self.assertIn(item, declared, "executive non_omissible must carry %s" % item)

    def test_non_omissible_items_are_required_subject_to_existence(self):
        self.requireYaml()
        t = DELIVERABLES["executive-report"]
        allslots = t.all_slots()
        for name in ("conditions_and_preconditions", "accepted_risks", "scope_outcome_pairs"):
            self.assertIn(name, t.slots("required"), "%s must be required" % name)
        for name in ("proof_obligations", "structural_open_choices", "revision_tripwires",
                     "architectability_basis"):
            self.assertIn(name, t.slots("conditional"),
                          "%s is required SUBJECT TO EXISTENCE => conditional" % name)
            self.assertIn(name, (t.get("slot_conditions") or {}),
                          "%s needs an existence condition" % name)
        self.assertTrue({"conditions_and_preconditions"} <= allslots)

    def test_no_template_converts_a_condition_into_satisfied(self):
        for rid, t in DELIVERABLES.items():
            self.assertNoPhrase("mark the condition satisfied", t.raw, rid)
            self.assertNoPhrase("render the condition as satisfied", t.raw, rid)
        t = DELIVERABLES["executive-report"]
        self.assertPhrase("converting a condition into a satisfied state",
                          t.field_text("forbidden_transformations"), "executive")

    def test_the_satisfaction_rule_is_stated(self):
        t = DELIVERABLES["executive-report"]
        self.assertPhrase("uma condição só passa a", t.body, "executive body")
        risks = SYNTH["risks-and-assumptions.template.md"]
        self.assertPhrase("NEVER rendered as satisfied", risks.raw, "risks synthesis")

    def test_impl_spec_carries_conditions_that_gate_build(self):
        t = DELIVERABLES["implementation-spec"]
        self.assertPhrase("Conditions", t.sources_text(), "impl-spec sources")
        self.assertPhrase("Preconditions", t.sources_text(), "impl-spec sources")


# ══════════════════════════════════════════════════════════════════════════════════════
# T-D7 — Implementation cannot change architecture
# ══════════════════════════════════════════════════════════════════════════════════════

class TestTD7ImplCannotChangeArchitecture(Base):

    def test_architecture_block_is_a_primary_authority(self):
        t = DELIVERABLES["implementation-spec"]
        self.assertPhrase("the architecture block", t.field_text("authority_sources"), "impl-spec")
        self.assertPhrase("PRIMARY", t.field_text("authority_sources"), "impl-spec")

    def test_architecture_is_declared_read_only(self):
        t = DELIVERABLES["implementation-spec"]
        self.assertPhrase("Architecture is READ-ONLY here",
                          t.field_text("architecture_projection"), "impl-spec")

    def test_impl_spec_forbids_selecting_store_composition_pattern_or_mode(self):
        t = DELIVERABLES["implementation-spec"]
        fb = t.field_text("forbidden_transformations")
        for must in ["selecting or changing record authority / store",
                     "selecting or changing a composition or a pattern",
                     "changing the experience mode",
                     "changing architecture authorization or scope",
                     "reopening Options"]:
            self.assertPhrase(must, fb, "impl-spec forbidden_transformations")

    def test_impl_spec_marks_a5_a3_a6_a4_read_only_per_section(self):
        t = DELIVERABLES["implementation-spec"]
        for must in ["A5 is READ-ONLY here", "A3 / A6 are READ-ONLY here",
                     "A4 is READ-ONLY here"]:
            self.assertPhrase(must, t.fm_text, "impl-spec")

    def test_impl_spec_declares_no_selection_slot_source(self):
        self.requireYaml()
        src = DELIVERABLES["implementation-spec"].slot_sources_text().lower()
        for banned in ["select the store", "choose the store", "select a composition",
                       "choose a composition", "select the pattern", "choose the pattern"]:
            self.assertNotIn(banned, src, "impl-spec slot_sources must not select architecture")

    def test_impl_spec_renders_an_open_work_item_instead_of_inventing_detail(self):
        t = DELIVERABLES["implementation-spec"]
        self.assertPhrase("fabricating implementation detail for an UNRESOLVED architecture choice",
                          t.field_text("forbidden_transformations"), "impl-spec")
        self.assertPhrase("OPEN WORK ITEM", t.fm_text, "impl-spec")
        self.assertIn("open_work_items", t.slots("required"))

    def test_forbidden_authorities_replace_d7_d8_d9(self):
        t = DELIVERABLES["implementation-spec"]
        fs = t.field_text("forbidden_sources")
        self.assertPhrase("raw shared-understanding.md rows as the source of a migration plan",
                          fs, "impl-spec (D-9)")
        self.assertPhrase("as-is.md as the source of acceptance work", fs, "impl-spec (D-7)")
        self.assertPhrase("financial-story.md as the source of sequencing", fs, "impl-spec (D-8)")

    def test_sequencing_authority_is_architecture_dependencies_only(self):
        self.requireYaml()
        rules = DELIVERABLES["implementation-spec"].get("derivation_rules") or {}
        seq = as_text(rules.get("sequencing"))
        self.assertPhrase("architecture dependencies only", seq, "impl-spec sequencing")
        self.assertPhrase("CONSTRAINTS ONLY, no durations", seq, "impl-spec sequencing")
        self.assertPhrase("financial-story.md", as_text(rules.get("sequencing")),
                          "impl-spec sequencing forbidden authority")

    def test_proof_work_derives_from_proof_obligations_not_discovery_friction(self):
        self.requireYaml()
        rules = DELIVERABLES["implementation-spec"].get("derivation_rules") or {}
        tp = as_text(rules.get("test_and_proof_work"))
        self.assertPhrase("proof_obligations[]", tp, "impl-spec proof derivation")
        self.assertPhrase("ONE work package + ONE acceptance condition", tp, "impl-spec")
        self.assertPhrase("SCENARIOS ONLY, never the proof level", tp, "impl-spec")

    def test_migration_derives_from_a9_and_class14_not_raw_su(self):
        self.requireYaml()
        rules = DELIVERABLES["implementation-spec"].get("derivation_rules") or {}
        mg = as_text(rules.get("migration_and_cutover"))
        self.assertPhrase("A9 replacement", mg, "impl-spec migration")
        self.assertPhrase("class-14 outcome", mg, "impl-spec migration")
        self.assertPhrase("access_mode", mg, "impl-spec migration")
        self.assertPhrase("raw shared-understanding.md Risky rows", mg,
                          "impl-spec migration forbidden authority")

    def test_migration_boundary_split_is_declared_and_no_extra_deliverable(self):
        self.requireYaml()
        rules = DELIVERABLES["implementation-spec"].get("derivation_rules") or {}
        mg = as_text(rules.get("migration_and_cutover"))
        self.assertPhrase("Architecture Blueprint owns WHAT is replaced", mg, "impl-spec")
        self.assertPhrase("No separate migration deliverable exists", mg, "impl-spec")


# ══════════════════════════════════════════════════════════════════════════════════════
# T-D8 — Design Brief cannot re-select store or composition
# ══════════════════════════════════════════════════════════════════════════════════════

class TestTD8DesignBriefCannotSelect(Base):

    def test_design_brief_sources_never_name_record_authority_or_compositions(self):
        self.requireYaml()
        src = DELIVERABLES["claude-design-brief"].sources_text()
        for banned in ["record_authority", "compositions[]", "relocated_responsibilities"]:
            self.assertNotIn(banned, src,
                             "design brief must not source %s" % banned)

    def test_design_brief_architecture_source_is_the_digest(self):
        self.requireYaml()
        t = DELIVERABLES["claude-design-brief"]
        self.assertIn("architecture_constraints_digest", t.slots("conditional"))
        self.assertPhrase("architecture_constraints_digest",
                          t.field_text("conditional_sources"), "design brief")

    def test_full_architecture_core_is_forbidden(self):
        t = DELIVERABLES["claude-design-brief"]
        self.assertPhrase("architecture-templates/architecture-core.md in full",
                          t.field_text("forbidden_sources"), "design brief")
        self.assertPhrase("the resolved boundary fragments",
                          t.field_text("forbidden_sources"), "design brief")

    def test_design_brief_forbids_the_four_selections(self):
        t = DELIVERABLES["claude-design-brief"]
        self.assertPhrase("selecting store, composition, pattern or experience mode",
                          t.field_text("forbidden_transformations"), "design brief")

    def test_design_brief_may_not_reconsolidate_screens_or_add_nodes(self):
        t = DELIVERABLES["claude-design-brief"]
        fb = t.field_text("forbidden_transformations")
        self.assertPhrase("re-consolidating screens", fb, "design brief")
        self.assertPhrase("adding a persona, screen, journey, action or state absent from the approved blueprint",
                          fb, "design brief")
        self.assertPhrase("changing a requirement", fb, "design brief")

    def test_digest_includes_and_excludes_are_declared(self):
        self.requireYaml()
        dig = DELIVERABLES["claude-design-brief"].get("architecture_constraints_digest") or {}
        inc = as_text(dig.get("includes"))
        exc = as_text(dig.get("excludes"))
        for must in ["A1", "A3", "A5", "A7", "A12"]:
            self.assertPhrase(must, inc, "digest includes")
        for must in ["A2 architecture intent", "A8", "A9", "A10", "A11",
                     "the boundary-fragment six channels"]:
            self.assertPhrase(must, exc, "digest excludes")

    def test_digest_is_a_runtime_selection_not_a_new_artefact(self):
        t = DELIVERABLES["claude-design-brief"]
        self.assertPhrase("NOT a new artefact", t.fm_text, "design brief")
        self.assertPhrase("NOT an architecture reasoning layer", t.fm_text, "design brief")
        self.assertFalse(os.path.exists(os.path.join(DT_DIR, "architecture-constraints-digest.md")),
                         "the digest must NOT become a file")


# ══════════════════════════════════════════════════════════════════════════════════════
# T-D9 — Estimate cannot settle economic attractiveness
# ══════════════════════════════════════════════════════════════════════════════════════

class TestTD9EstimateNotEconomics(Base):

    def test_estimate_declares_s8_economics_forbidden(self):
        t = DELIVERABLES["estimate"]
        self.assertPhrase("options.md S8 comparative economics as an estimate input or output",
                          t.field_text("forbidden_sources"), "estimate")
        self.assertPhrase("settling economic attractiveness",
                          t.field_text("forbidden_transformations"), "estimate")
        self.assertPhrase("deciding whether this platform is cheaper",
                          t.field_text("forbidden_transformations"), "estimate")

    def test_estimate_cites_the_method_unit_as_method_only(self):
        t = DELIVERABLES["estimate"]
        self.assertPhrase("craft/estimation-model.md", t.field_text("method_authority"), "estimate")
        self.assertPhrase("METHOD ONLY", t.fm_text, "estimate")
        self.assertPhrase("used COMPARATIVELY", t.field_text("forbidden_sources"), "estimate")

    def test_estimate_carries_no_price_token(self):
        t = DELIVERABLES["estimate"]
        body_and_slots = t.body + " " + t.slot_sources_text()
        for tok in PRICE_TOKENS:
            if tok == "sku":
                continue  # 'SKU' appears only inside prohibitions
            self.assertNotIn(tok, body_and_slots.lower(),
                             "estimate must carry no price token: %s" % tok)

    def test_estimate_denominator_is_person_days(self):
        t = DELIVERABLES["estimate"]
        self.assertPhrase("PERSON-DAYS remain the canonical denominator",
                          t.field_text("denominator"), "estimate")
        self.assertPhrase("ENGAGEMENT INPUT WITH PROVENANCE", t.field_text("denominator"),
                          "estimate")

    def test_economics_separation_is_declared(self):
        t = DELIVERABLES["estimate"]
        sep = t.field_text("economics_separation")
        self.assertPhrase("S8 decision economics", sep, "estimate")
        self.assertPhrase("NOT the same question, and NOT merged", sep, "estimate")

    def test_executive_owns_decision_economics_and_only_projects_the_estimate_headline(self):
        t = DELIVERABLES["executive-report"]
        self.assertIn("decision_economics", t.slots("conditional"))
        self.assertIn("investment_summary", t.slots("conditional"))
        self.assertPhrase("ONE paragraph", t.slot_sources_text(), "executive investment_summary")
        self.assertPhrase("deriving a phase plan, an effort figure or a build sequence",
                          t.field_text("forbidden_transformations"), "executive")

    def test_estimate_recommendations_are_delivery_only(self):
        t = DELIVERABLES["estimate"]
        self.assertPhrase("DELIVERY recommendations only", t.slot_sources_text(), "estimate")
        self.assertPhrase("Nenhuma afirmação sobre opções", t.body, "estimate body")


# ══════════════════════════════════════════════════════════════════════════════════════
# T-D10 — Assumed / Unknown / Conflicted never promoted
# ══════════════════════════════════════════════════════════════════════════════════════

class TestTD10Epistemics(Base):

    FIVE = ["Confirmed", "Assumed", "Unknown", "Conflicted", "Risky"]

    def test_every_deliverable_declares_an_epistemic_projection_block(self):
        self.requireYaml()
        for rid, t in DELIVERABLES.items():
            ep = t.get("epistemic_projection")
            self.assertIsInstance(ep, dict, "%s must declare epistemic_projection" % rid)
            keys = " ".join(str(k) for k in ep.keys())
            for state in self.FIVE:
                self.assertIn(state, keys, "%s: epistemic_projection missing %s" % (rid, state))

    def test_expired_confirmed_is_never_a_fact(self):
        self.requireYaml()
        for rid, t in DELIVERABLES.items():
            ep = t.get("epistemic_projection") or {}
            val = as_text(ep.get("Confirmed_expired"))
            self.assertTrue(val.strip(), "%s must project expired Confirmed" % rid)
            self.assertFalse(re.search(r"\bas fact\b", val, re.I),
                             "%s: expired Confirmed rendered as fact" % rid)

    def test_conflicted_is_never_resolved_by_a_deliverable(self):
        self.requireYaml()
        for rid, t in DELIVERABLES.items():
            val = as_text((t.get("epistemic_projection") or {}).get("Conflicted")).lower()
            self.assertTrue(
                ("neither" in val) or ("no side" in val) or ("no value chosen" in val)
                or ("no figure" in val) or ("design neither" in val),
                "%s: Conflicted projection must choose no side (got %r)" % (rid, val))

    def test_no_template_instructs_an_epistemic_promotion(self):
        # A template legitimately FORBIDS these ("nunca marcar como satisfeita"), so what
        # must not exist is an occurrence that reads as an instruction.
        for rid, t in list(DELIVERABLES.items()) + list(SYNTH.items()):
            for phrase in EPISTEMIC_PROMOTION_PHRASES:
                self.assertOnlyProhibited(phrase, t.raw, rid)

    def test_discovery_projects_all_five_states_in_their_own_sections(self):
        t = DELIVERABLES["discovery-report"]
        req = t.slots("required")
        for s in ("open_questions_unknown", "conflicts_unresolved", "risks_observed",
                  "assumptions_in_play", "evidence_still_required"):
            self.assertIn(s, req, "discovery must carry %s as required" % s)

    def test_discovery_counts_residuals_for_the_four_open_states(self):
        self.requireYaml()
        t = DELIVERABLES["discovery-report"]
        rule = as_text((t.get("materiality") or {}).get("omission_rule"))
        self.assertPhrase("COUNTED RESIDUAL", rule, "discovery materiality")
        self.assertPhrase("NEVER silent for Unknown / Conflicted / Risky / Assumed", rule,
                          "discovery materiality")

    def test_discovery_materiality_has_the_seven_survival_classes(self):
        self.requireYaml()
        surv = (DELIVERABLES["discovery-report"].get("materiality") or {}).get("survives_if_any")
        self.assertIsInstance(surv, list)
        self.assertEqual(7, len(surv), "seven materiality classes")

    def test_estimate_declares_the_named_uncertainty_rule(self):
        t = DELIVERABLES["estimate"]
        ch = t.field_text("contingency_honesty")
        self.assertPhrase("NAMED uncertainty line", ch, "estimate")
        self.assertPhrase("never a substitute for them", ch, "estimate")
        self.assertPhrase("HIDING an architectural Unknown inside contingency",
                          t.field_text("forbidden_transformations"), "estimate")
        self.assertIn("named_uncertainties", t.slots("required"))

    def test_volatile_values_keep_their_stamps(self):
        self.assertPhrase("verificado_em", RENDER_SKILL, "aisa-render")
        self.assertPhrase("validade", RENDER_SKILL, "aisa-render")
        self.assertPhrase("renders as a verification obligation", RENDER_SKILL, "aisa-render")
        self.assertPhrase("never treat a template as a fact store", RENDER_SKILL, "aisa-render")

    def test_render_skill_states_the_binding_rule(self):
        self.assertPhrase("Deliverable brevity cannot upgrade epistemics", RENDER_SKILL,
                          "aisa-render")


# ══════════════════════════════════════════════════════════════════════════════════════
# T-D11 — Proof levels not re-graded
# ══════════════════════════════════════════════════════════════════════════════════════

PROOF_CARRIERS = ["discovery-report", "executive-report", "solution-blueprint",
                  "implementation-spec", "claude-design-brief", "estimate"]


class TestTD11ProofObligations(Base):

    def test_every_proof_carrying_template_declares_its_carriage(self):
        self.requireYaml()
        for rid in PROOF_CARRIERS:
            t = DELIVERABLES[rid]
            if rid == "discovery-report":
                # Discovery carries material EVIDENCE GAPS, not graded obligations.
                self.assertIn("evidence_still_required", t.slots("required"))
                continue
            poc = t.get("proof_obligation_carriage")
            self.assertIsInstance(poc, dict, "%s must declare proof_obligation_carriage" % rid)
            self.assertTrue(as_text(poc.get("rule")).strip(), "%s: carriage rule empty" % rid)

    def test_the_five_part_shape_is_quoted_where_obligations_are_carried(self):
        for rid in ("solution-blueprint", "implementation-spec", "estimate"):
            t = DELIVERABLES[rid]
            self.assertPhrase("V1", t.raw, rid)
            self.assertPhrase("V4", t.raw, rid)
            self.assertTrue(has("method", t.raw) and has("owner", t.raw)
                            and has("funded", t.raw),
                            "%s must quote method/owner/funded" % rid)

    def test_no_deliverable_regrades_or_satisfies_an_obligation(self):
        for rid, t in DELIVERABLES.items():
            self.assertNoPhrase("re-grade the level", t.raw, rid)
            self.assertNoPhrase("substitute the method", t.raw, rid)
            self.assertNoPhrase("mark the obligation satisfied", t.raw, rid)

    def test_each_deliverable_declares_the_no_regrading_prohibition(self):
        for rid in ("executive-report", "solution-blueprint", "implementation-spec",
                    "claude-design-brief", "estimate"):
            t = DELIVERABLES[rid]
            self.assertTrue(
                has("never re-graded", t.raw) or has("re-grading a proof obligation", t.raw)
                or has("never changed", t.raw),
                "%s must declare V1-V4 read-only" % rid)

    def test_impl_spec_translates_every_obligation_to_a_work_package(self):
        self.requireYaml()
        poc = DELIVERABLES["implementation-spec"].get("proof_obligation_carriage") or {}
        self.assertPhrase("ALL, translated", as_text(poc.get("scope")), "impl-spec")
        self.assertPhrase("one work package + one acceptance condition",
                          as_text(poc.get("form")), "impl-spec")
        self.assertIn("proof_work_packages", DELIVERABLES["implementation-spec"].slots("required"))

    def test_blueprint_carries_all_architecture_obligations(self):
        self.requireYaml()
        poc = DELIVERABLES["solution-blueprint"].get("proof_obligation_carriage") or {}
        self.assertPhrase("ALL architecture proof obligations", as_text(poc.get("scope")),
                          "blueprint")

    def test_executive_carries_only_decision_changing_obligations(self):
        self.requireYaml()
        poc = DELIVERABLES["executive-report"].get("proof_obligation_carriage") or {}
        self.assertPhrase("decision-changing", as_text(poc.get("scope")), "executive")

    def test_design_brief_carries_only_ux_validations(self):
        self.requireYaml()
        poc = DELIVERABLES["claude-design-brief"].get("proof_obligation_carriage") or {}
        self.assertPhrase("UX / design validations only", as_text(poc.get("scope")),
                          "design brief")

    def test_estimate_carries_only_the_effort_for_proof_work(self):
        self.requireYaml()
        poc = DELIVERABLES["estimate"].get("proof_obligation_carriage") or {}
        self.assertPhrase("EFFORT for the proof work", as_text(poc.get("scope")), "estimate")


# ══════════════════════════════════════════════════════════════════════════════════════
# T-D12 — Multiple architectures remain multiple
# ══════════════════════════════════════════════════════════════════════════════════════

class TestTD12MultipleArchitectures(Base):

    def test_blueprint_declares_the_candidate_conditional_choosing_neither(self):
        self.requireYaml()
        t = DELIVERABLES["solution-blueprint"]
        self.assertIn("candidate_architectures_note", t.slots("conditional"))
        cond = as_text((t.get("slot_conditions") or {}).get("candidate_architectures_note"))
        self.assertPhrase("structural:true", cond, "blueprint candidate condition")
        self.assertPhrase("escolhe nenhuma", t.body, "blueprint body")
        self.assertPhrase("Sem pontuação", t.body, "blueprint body")

    def test_blueprint_forbids_scoring_and_selecting(self):
        t = DELIVERABLES["solution-blueprint"]
        fb = t.field_text("forbidden_transformations")
        self.assertPhrase("scoring any architecture", fb, "blueprint")
        self.assertPhrase("selecting among candidate architectures", fb, "blueprint")

    def test_impl_spec_and_design_brief_are_blocked_on_a_structural_choice(self):
        for rid in ("implementation-spec", "claude-design-brief"):
            t = DELIVERABLES[rid]
            txt = t.field_text("blocked_when") + " " + t.fm_text
            self.assertPhrase("structural", txt, "%s blocked_when" % rid)
            self.assertPhrase("BLOCKED", t.fm_text, rid)

    def test_estimate_forbids_a_blended_candidate_figure(self):
        t = DELIVERABLES["estimate"]
        self.assertPhrase("blending candidate estimates into one figure",
                          t.field_text("forbidden_transformations"), "estimate")


# ══════════════════════════════════════════════════════════════════════════════════════
# T-D13 — No deliverable becomes source authority for another upstream concern
# ══════════════════════════════════════════════════════════════════════════════════════

class TestTD13ReadGraph(Base):

    # The frozen model authorizes exactly two deliverable->deliverable reads:
    #   impl-spec -> estimate   (6.5, inventory only)
    #   estimate  -> executive  (5 "effort estimate" row + 28.2, the headline, one paragraph)
    ALLOWED_EDGES = {
        ("estimate", "implementation-spec"),
        ("executive-report", "estimate"),
    }

    def _render_refs(self, t):
        refs = set()
        for m in re.findall(r"_render/<slug>_([a-z-]+)_v", t.sources_text()):
            refs.add(m)
        return refs

    def test_only_the_authorized_deliverable_to_deliverable_reads_exist(self):
        self.requireYaml()
        edges = set()
        for rid, t in DELIVERABLES.items():
            for target in self._render_refs(t):
                edges.add((rid, target))
            if rid == "estimate" and has("Implementation Specification's inventory",
                                         t.sources_text()):
                edges.add(("estimate", "implementation-spec"))
        self.assertTrue(edges <= self.ALLOWED_EDGES,
                        "unauthorized deliverable->deliverable reads: %s"
                        % sorted(edges - self.ALLOWED_EDGES))

    def test_the_spec_to_estimate_edge_is_inventory_only(self):
        self.requireYaml()
        t = DELIVERABLES["estimate"]
        modes = t.get("input_modes") or {}
        a = as_text(modes.get("A"))
        self.assertPhrase("Implementation Specification's inventory", a, "estimate mode A")
        for must in ["components", "obligations", "proof work", "migration steps",
                     "open work items"]:
            self.assertPhrase(must, a, "estimate mode A inventory payload")
        # The excluded payload must be named as excluded, never carried.
        self.assertPhrase("INVENTORY ONLY", a, "estimate mode A")
        self.assertPhrase("no narrative", a, "estimate mode A")
        self.assertPhrase("no acceptance text", a, "estimate mode A")

    def test_the_read_graph_has_no_cycle(self):
        edges = sorted(self.ALLOWED_EDGES)
        nodes = {n for e in edges for n in e}
        adj = {n: [] for n in nodes}
        for src, dst in edges:
            adj[src].append(dst)
        state = {}

        def visit(n):
            if state.get(n) == 1:
                self.fail("cycle through %s" % n)
            if state.get(n) == 2:
                return
            state[n] = 1
            for m in adj[n]:
                visit(m)
            state[n] = 2

        for n in nodes:
            visit(n)

    def test_no_deliverable_reads_another_deliverables_narrative_as_authority(self):
        for rid, t in DELIVERABLES.items():
            self.assertTrue(
                has("another deliverable", t.field_text("forbidden_sources"))
                or has("_render/", t.field_text("forbidden_sources"))
                or rid == "estimate",
                "%s must forbid another deliverable's narrative as authority" % rid)

    def test_impl_spec_forbids_reading_the_estimate(self):
        t = DELIVERABLES["implementation-spec"]
        self.assertPhrase("_render/<slug>_estimate_v<NN>.md",
                          t.field_text("forbidden_sources"), "impl-spec")

    def test_one_primary_authority_per_deliverable_is_declared(self):
        self.requireYaml()
        for rid, t in DELIVERABLES.items():
            self.assertTrue(as_text(t.get("authority_sources")).strip(),
                            "%s declares no authority" % rid)
        self.assertPhrase("itself, for the calculation",
                          DELIVERABLES["estimate"].field_text("authority_sources"), "estimate")

    def test_render_contract_lists_the_six_primary_authorities(self):
        self.assertPhrase("The six projection contracts", RENDER_CONTRACT, "render-contract")
        # DV-2 count correction: two bounded edges, and no third. T-D13's meaning is
        # unchanged -- bounded payloads, acyclic graph, one primary authority per class.
        self.assertPhrase("Exactly two bounded deliverable", RENDER_CONTRACT,
                          "render-contract")
        self.assertPhrase("and no third", RENDER_CONTRACT, "render-contract")


# ══════════════════════════════════════════════════════════════════════════════════════
# T-D14 — The two "blueprints" are never conflated
# ══════════════════════════════════════════════════════════════════════════════════════

UX_SLOT_OWNERS = {
    "claude-design-brief": ["surface_inventory", "persona_users", "page_navigation_map",
                            "screen_specifications", "ux_requirements", "excluded_from_ui"],
    "implementation-spec": ["screens_to_build"],
}


class TestTD14TwoBlueprints(Base):

    def test_every_ux_slot_names_the_approved_ux_blueprint(self):
        self.requireYaml()
        for rid, slots in UX_SLOT_OWNERS.items():
            srcs = DELIVERABLES[rid].get("slot_sources") or {}
            for s in slots:
                src = as_text(srcs.get(s))
                self.assertPhrase("_blueprint/ux-blueprint_v<approved>.yaml", src,
                                  "%s.%s" % (rid, s))

    def test_no_ux_content_is_sourced_from_the_rendered_architecture_blueprint(self):
        self.requireYaml()
        for rid, t in DELIVERABLES.items():
            src = t.sources_text()
            self.assertNotIn("_render/<slug>_solution-blueprint", src,
                             "%s must not source from the rendered Architecture Blueprint" % rid)

    def test_design_brief_forbids_the_rendered_architecture_blueprint_explicitly(self):
        t = DELIVERABLES["claude-design-brief"]
        self.assertPhrase("_render/<slug>_solution-blueprint_v<NN>.md",
                          t.field_text("forbidden_sources"), "design brief")
        self.assertPhrase("never confuse it", t.field_text("forbidden_sources"), "design brief")

    def test_architecture_blueprint_does_not_source_ux_screens(self):
        self.requireYaml()
        t = DELIVERABLES["solution-blueprint"]
        srcs = as_text(t.get("slot_sources"))
        self.assertNotIn("ux-blueprint_v<approved>.yaml# screens", srcs,
                         "the Architecture Blueprint is not a UX artefact")
        # P-18 / F08: the Architecture Blueprint reads the latest AUTHORIZED version and
        # declares its approval state; `v<approved>` could never show the candidate
        # architectures a structural choice keeps engaged (that choice blocks approval).
        self.assertPhrase("_blueprint/ux-blueprint_v<latest authorized>.yaml# architecture",
                          srcs, "blueprint architecture_block source")
        self.assertNotIn("ux-blueprint_v<approved>.yaml# architecture", srcs,
                         "the Architecture Blueprint must not require approval to render")

    def test_architecture_blueprint_declares_the_version_state_it_read(self):
        self.requireYaml()
        t = DELIVERABLES["solution-blueprint"]
        self.assertIn("architecture_version_state", t.slots("required"))
        self.assertIn("{{architecture_version_state}}", t.body)
        src = as_text((t.get("slot_sources") or {}).get("architecture_version_state"))
        for must in ("aprovada (D-NNN)", "escolha(s) estrutural(is) em aberto",
                     "aguarda aprovação do negócio"):
            self.assertPhrase(must, src, "architecture_version_state source")
        self.assertEqual("v<latest authorized>", str(t.get("blueprint_version_read")).strip())

    def test_spec_and_brief_still_read_the_approved_version_only(self):
        self.requireYaml()
        for rid in ("implementation-spec", "claude-design-brief"):
            srcs = DELIVERABLES[rid].sources_text()
            self.assertNotIn("v<latest authorized>", srcs,
                             "%s must keep requiring the approved blueprint" % rid)


# ══════════════════════════════════════════════════════════════════════════════════════
# T-D15 — Selective Domain Knowledge and CRAFT
# ══════════════════════════════════════════════════════════════════════════════════════

class TestTD15SelectiveKnowledge(Base):

    def test_discovery_and_executive_name_zero_knowledge_units(self):
        for rid in ("discovery-report", "executive-report"):
            t = DELIVERABLES[rid]
            hits = DK_UNIT_RE.findall(t.raw)
            self.assertEqual([], hits, "%s must name ZERO knowledge units, got %s" % (rid, hits))

    def test_discovery_and_executive_declare_knowledge_units_forbidden(self):
        for rid in ("discovery-report", "executive-report"):
            t = DELIVERABLES[rid]
            fs = t.field_text("forbidden_sources")
            self.assertPhrase("Domain Knowledge", fs, rid)
            self.assertPhrase("CRAFT", fs, rid)

    def test_blueprint_makes_no_fresh_knowledge_pull(self):
        t = DELIVERABLES["solution-blueprint"]
        self.assertPhrase("preloaded Domain Knowledge", t.field_text("forbidden_sources"),
                          "blueprint")
        self.assertPhrase("it does not re-pull", t.field_text("forbidden_sources"), "blueprint")
        self.assertEqual([], DK_UNIT_RE.findall(t.raw),
                         "the Blueprint cites; it names no unit path")

    def test_impl_spec_and_design_brief_declare_point_of_need(self):
        self.requireYaml()
        for rid in ("implementation-spec", "claude-design-brief"):
            sp = DELIVERABLES[rid].get("selective_pulls")
            self.assertIsInstance(sp, dict, "%s must declare selective_pulls" % rid)
            self.assertIs(True, sp.get("point_of_need"),
                          "%s must declare point_of_need: true" % rid)
            self.assertPhrase("POINT OF NEED", as_text(sp) + " " + DELIVERABLES[rid].fm_text,
                              rid)

    def test_no_template_names_more_than_two_units_without_point_of_need(self):
        self.requireYaml()
        for rid, t in DELIVERABLES.items():
            hits = set(DK_UNIT_RE.findall(t.raw))
            if len(hits) > 2:
                sp = t.get("selective_pulls") or {}
                self.assertIs(True, sp.get("point_of_need"),
                              "%s names %d units and declares no point_of_need"
                              % (rid, len(hits)))

    def test_the_characterised_six_row_dk_table_is_gone(self):
        t = DELIVERABLES["claude-design-brief"]
        self.assertNoPhrase("Domain knowledge cross-references", t.raw, "design brief")
        self.assertNoPhrase("carregam o contexto técnico denso", t.raw, "design brief")
        self.assertPhrase("the characterised Domain Knowledge table",
                          t.field_text("forbidden_sources"), "design brief")
        self.assertPhrase("preloading the Domain Knowledge catalogue",
                          t.field_text("forbidden_transformations"), "design brief")
        # No markdown table row whose first cell is a knowledge-unit path.
        self.assertFalse(re.search(r"^\|\s*`?[^|`]*domain-knowledge/", t.raw, re.M),
                         "design brief still tabulates knowledge units")

    def test_design_brief_carries_a_where_to_verify_pointer_list(self):
        t = DELIVERABLES["claude-design-brief"]
        self.assertIn("where_to_verify", t.slots("conditional"))
        self.assertPhrase("Sem caracterização, sem catálogo", t.body, "design brief body")

    def test_estimate_names_only_method_and_driver_units(self):
        hits = set(DK_UNIT_RE.findall(DELIVERABLES["estimate"].raw))
        self.assertTrue(hits <= {"domain-knowledge/craft/estimation-model.md",
                                 "domain-knowledge/economics/licensing-and-cost-drivers.md"},
                        "estimate may name only the method + driver units, got %s" % hits)

    def test_craft_never_overrides_research_or_architecture(self):
        for rid in ("implementation-spec", "claude-design-brief"):
            t = DELIVERABLES[rid]
            self.assertTrue(
                has("never asserts a platform limit", t.raw)
                or has("never overrides RESEARCH or architecture", t.raw)
                or has("never a control", t.raw),
                "%s must state the CRAFT boundary" % rid)
            self.assertPhrase("RESEARCH", t.raw, rid)


# ══════════════════════════════════════════════════════════════════════════════════════
# T-D16 — Manifest coherence
# ══════════════════════════════════════════════════════════════════════════════════════

class TestTD16Manifest(Base):

    def test_pack_lists_exactly_six_deliverables(self):
        self.requireYaml()
        self.assertEqual(6, len(PACK["deliverables"]))
        self.assertEqual(set(SIX), {d["id"] for d in PACK["deliverables"]})

    def test_every_manifest_template_path_exists(self):
        self.requireYaml()
        for d in PACK["deliverables"]:
            p = os.path.join(PACK_DIR, d["template"])
            self.assertTrue(os.path.exists(p), "missing template: %s" % d["template"])

    def test_manifest_canonical_deliverable_matches_the_template(self):
        self.requireYaml()
        for d in PACK["deliverables"]:
            self.assertIn("canonical_deliverable", d, "%s: missing canonical_deliverable" % d["id"])
            self.assertEqual(SIX[d["id"]], d["canonical_deliverable"])
            self.assertEqual(DELIVERABLES[d["id"]].get("canonical_deliverable"),
                             d["canonical_deliverable"],
                             "%s: manifest and template disagree" % d["id"])

    def test_applies_to_is_gone_and_activation_is_present(self):
        self.requireYaml()
        for d in PACK["deliverables"]:
            self.assertNotIn("applies_to", d, "%s still carries applies_to" % d["id"])
            self.assertIn("activation", d, "%s carries no activation" % d["id"])
            self.assertTrue(str(d["activation"]).strip())
        # The 1.8.0 rationale comment explains why `applies_to: [technology]` was the wrong
        # discriminator, so the string may appear -- but only inside a comment.
        for line in PACK_RAW.splitlines():
            if "applies_to" in line:
                self.assertTrue(line.lstrip().startswith("#"),
                                "applies_to survives as an ACTIVE key: %r" % line)

    def test_pack_version_bumped(self):
        """Step 6B put the manifest on the 1.8 line and left its rationale in the file.

        The assertion is on the MINOR line, not the patch: a later patch bump (Step 7
        made 1.8.1, an integrity cleanup with no semantic change) must not fail Step 6.
        A move off the 1.8/1.9 line means the deliverable-projection layer itself
        changed, and that is what this test exists to catch. 1.9.0 (P-19, platform
        forms named in Options) did not touch this layer: no template, no manifest
        entry, no activation rule, no slot source.
        """
        self.requireYaml()
        version = str(PACK["pack_version"])
        self.assertRegex(version, r"^1\.(?:8|9)\.\d+$",
                         "deliverable-projection layer left the 1.8/1.9 line: %s" % version)
        self.assertPhrase("pack_version 1.8.0 (Step 6B)", PACK_RAW, "pack.yaml rationale")

    def test_manifest_declares_the_estimate_calculation_owner(self):
        self.requireYaml()
        est = [d for d in PACK["deliverables"] if d["id"] == "estimate"][0]
        self.assertIs(True, est.get("owns_calculation"))

    def test_manifest_introduces_no_router(self):
        # pack.yaml states these as things it does NOT introduce, so each occurrence must
        # sit inside a prohibition.
        for banned in ["outcome->template", "concern->deliverable", "product map",
                       "load order", "state machine", "router"]:
            self.assertOnlyProhibited(banned, PACK_RAW, "pack.yaml")
        # And no active manifest key may declare routing.
        for line in PACK_RAW.splitlines():
            if line.lstrip().startswith("#"):
                continue
            for banned_key in ("router:", "routes:", "concern_map:", "outcome_map:",
                               "template_map:", "load_order:"):
                self.assertNotIn(banned_key, line, "pack.yaml declares %s" % banned_key)


# ══════════════════════════════════════════════════════════════════════════════════════
# T-D17 — Gap-class integrity
# ══════════════════════════════════════════════════════════════════════════════════════

GAP_CLASSES = ["not applicable", "optional", "open work item", "decision-blocking"]
GAP_OWNERS = ["architecture", "implementation", "design", "estimate", "evidence"]


class TestTD17GapClasses(Base):

    def test_exactly_four_gap_classes_in_the_render_contract(self):
        for c in GAP_CLASSES:
            self.assertPhrase(c, RENDER_CONTRACT, "render-contract")
        # The relabel note legitimately names the former label ("the former *architecture
        # work item*"). What must not survive is a CLASS ROW carrying it.
        self.assertOnlyProhibited("architecture work item", RENDER_CONTRACT, "render-contract")
        self.assertNotIn("| **architecture work item** |", RENDER_CONTRACT,
                         "class 3 must be relabelled in the table")

    def test_exactly_four_gap_classes_in_the_render_skill(self):
        for c in GAP_CLASSES:
            self.assertPhrase(c, RENDER_SKILL, "aisa-render")
        self.assertNoPhrase("| **architecture work item** |", RENDER_SKILL, "aisa-render")

    def test_no_fifth_class_is_introduced(self):
        for text, label in ((RENDER_CONTRACT, "render-contract"), (RENDER_SKILL, "aisa-render")):
            self.assertPhrase("No fifth class", text, label)
            self.assertPhrase("No parallel taxonomy", text, label)

    def test_class_three_carries_an_owner_enumeration(self):
        for text, label in ((RENDER_CONTRACT, "render-contract"), (RENDER_SKILL, "aisa-render")):
            self.assertPhrase("owner ∈", text, label)
            for o in GAP_OWNERS:
                self.assertPhrase(o, text, label)

    def test_deliverable_skips_go_to_render_log_and_never_to_render_gaps(self):
        for text, label in ((RENDER_CONTRACT, "render-contract"), (RENDER_SKILL, "aisa-render")):
            self.assertPhrase("render-log.md", text, label)
            self.assertTrue(has("never", text) and has("render-gaps.md", text))
        self.assertPhrase("Skips never pollute `render-gaps.md`", RENDER_SKILL, "aisa-render")

    def test_open_work_item_label_is_used_by_the_deliverables(self):
        t = DELIVERABLES["implementation-spec"]
        self.assertIn("open_work_items", t.slots("required"))
        for o in GAP_OWNERS:
            self.assertPhrase(o, t.body, "impl-spec open work items section")


# ══════════════════════════════════════════════════════════════════════════════════════
# T-D18 — Discovery neutrality survives
# ══════════════════════════════════════════════════════════════════════════════════════

class TestTD18DiscoveryNeutrality(Base):

    def test_discovery_names_no_vendor_or_product(self):
        raw = DELIVERABLES["discovery-report"].raw.lower()
        for term in NEUTRALITY_DENYLIST:
            self.assertNotIn(term, raw, "discovery-report must stay neutral: %r" % term)

    def test_discovery_declares_decision_architecture_and_options_forbidden(self):
        fs = DELIVERABLES["discovery-report"].field_text("forbidden_sources")
        self.assertPhrase("decisions.md# D-NNN", fs, "discovery")
        self.assertPhrase("architecture", fs, "discovery")
        self.assertPhrase("options.md", fs, "discovery")

    def test_discovery_forbids_recommendation_and_option_conclusions(self):
        fb = DELIVERABLES["discovery-report"].field_text("forbidden_transformations")
        self.assertPhrase("vendor/product name", fb, "discovery")
        self.assertPhrase("technology recommendation", fb, "discovery")
        self.assertPhrase("Options conclusion", fb, "discovery")

    def test_discovery_reads_no_architecture_and_no_estimate(self):
        self.requireYaml()
        t = DELIVERABLES["discovery-report"]
        src = t.sources_text()
        self.assertNotIn("architecture-core", src)
        self.assertNotIn("architecture block", src.lower())
        self.assertNotIn("_render/", src)

    def test_discovery_keeps_the_benign_source_inventory(self):
        self.requireYaml()
        t = DELIVERABLES["discovery-report"]
        self.assertIn("sources_analysed", t.slots("conditional"))
        self.assertPhrase("_capture/evidence-index.md", t.slot_sources_text(), "discovery")
        self.assertPhrase("INVENTORY, never a reinterpretation", t.slot_sources_text(),
                          "discovery")

    def test_render_skill_keeps_the_neutrality_hard_rule(self):
        self.assertPhrase("technology-neutral by construction", RENDER_SKILL, "aisa-render")


# ══════════════════════════════════════════════════════════════════════════════════════
# T-D19 (MANDATORY) — Deliverable-owned derivation executor
# ══════════════════════════════════════════════════════════════════════════════════════

class TestTD19EstimateOwnsCalculation(Base):

    def test_estimate_declares_owns_calculation_true(self):
        self.requireYaml()
        self.assertIs(True, DELIVERABLES["estimate"].get("owns_calculation"))

    def test_estimate_declares_the_four_structural_obligations(self):
        self.requireYaml()
        t = DELIVERABLES["estimate"]
        for field in ("input_inventory_authority", "method_authority",
                      "permitted_outputs", "forbidden_semantic_changes"):
            self.assertIn(field, t.fm, "estimate must declare %s" % field)
            self.assertTrue(as_text(t.fm[field]).strip(), "estimate: %s is empty" % field)

    def test_input_inventory_authority_names_both_modes(self):
        self.requireYaml()
        iia = DELIVERABLES["estimate"].get("input_inventory_authority")
        self.assertIsInstance(iia, dict)
        self.assertPhrase("Implementation Specification", as_text(iia.get("mode_a")), "estimate")
        self.assertPhrase("candidate architecture record", as_text(iia.get("mode_b")), "estimate")

    def test_method_authority_is_the_estimation_model_unit(self):
        self.requireYaml()
        ma = DELIVERABLES["estimate"].field_text("method_authority")
        self.assertPhrase("craft/estimation-model.md", ma, "estimate")
        p = os.path.join(PACK_DIR, "domain-knowledge", "craft", "estimation-model.md")
        self.assertTrue(os.path.exists(p), "the method authority unit must exist")

    def test_permitted_outputs_are_the_five(self):
        self.requireYaml()
        po = as_text(DELIVERABLES["estimate"].get("permitted_outputs"))
        for must in ["work breakdown", "effort bands", "ranges", "contingency", "confidence"]:
            self.assertPhrase(must, po, "estimate permitted_outputs")

    def test_forbidden_semantic_changes_cover_the_four_prohibitions(self):
        self.requireYaml()
        fsc = as_text(DELIVERABLES["estimate"].get("forbidden_semantic_changes"))
        for must in ["no scope change", "no epistemic promotion", "no comparator claim",
                     "no invented work unit", "no price"]:
            self.assertPhrase(must, fsc, "estimate forbidden_semantic_changes")

    def test_the_executor_is_aisa_render_and_nothing_else(self):
        self.requireYaml()
        t = DELIVERABLES["estimate"]
        self.assertEqual("aisa-render", str(t.get("calculation_executor")).strip())
        self.assertEqual("estimate", str(t.get("semantic_owner")).strip())
        self.assertPhrase("and NOTHING ELSE executes it", t.fm_text, "estimate")

    def test_render_skill_is_the_only_executor_and_only_of_declared_transformations(self):
        self.assertPhrase("permitted_transformations", RENDER_SKILL, "aisa-render")
        self.assertPhrase("execute only the projection transformations the active deliverable contract declares",
                          RENDER_SKILL, "aisa-render")
        self.assertPhrase("this skill is its executor, and the only one", RENDER_SKILL,
                          "aisa-render")
        self.assertPhrase("This skill is not an inference engine", RENDER_SKILL, "aisa-render")

    def test_render_skill_refuses_an_undeclared_computation(self):
        self.assertPhrase("A computed slot with no matching declared transformation is a **contract defect**",
                          RENDER_SKILL, "aisa-render")
        self.assertPhrase("A transformation not declared in `permitted_transformations` is not executed",
                          RENDER_SKILL, "aisa-render")

    def test_financial_synthesis_computes_no_implementation_effort_figure(self):
        self.requireYaml()
        t = SYNTH["financial-story.template.md"]
        self.assertIs(False, t.get("computes_implementation_effort"))
        self.assertIs(False, t.get("owns_calculation"))
        forb = as_text(t.get("forbidden_outputs"))
        for must in ["a phased build plan", "a per-phase effort table", "any person-day figure",
                     "a team-by-profile effort table", "an operational-impact delta table"]:
            self.assertPhrase(must, forb, "financial-story forbidden_outputs")
        self.assertPhrase("never where a figure first appears",
                          t.field_text("estimate_reference_rule"), "financial-story")

    def test_the_old_calculation_sections_are_gone_from_financial_synthesis(self):
        t = SYNTH["financial-story.template.md"]
        for gone in ["## Phased build plan", "## Detailed estimate by phase",
                     "## Effort summary by phase", "## Team and effort by profile",
                     "## Timeline", "## Estimate headline"]:
            self.assertNotIn(gone, t.raw,
                             "financial synthesis must not own %r any more" % gone)

    def test_no_second_estimate_authority_exists_anywhere(self):
        self.requireYaml()
        # No synthesis template may claim the calculation.
        for fn, t in SYNTH.items():
            self.assertNotEqual(True, t.get("owns_calculation"),
                                "%s must not own the calculation" % fn)
        # No other deliverable may claim it.
        for rid, t in DELIVERABLES.items():
            if rid == "estimate":
                continue
            self.assertNotEqual(True, t.get("owns_calculation"),
                                "%s must not own the calculation" % rid)
            self.assertNotIn("method_authority", t.fm,
                             "%s must not declare an estimation method authority" % rid)
        # The synthesize skill must disclaim it.
        self.assertPhrase("Synthesis computes no implementation estimate", SYNTH_SKILL,
                          "aisa-synthesize")
        self.assertPhrase("compute the implementation estimate", SYNTH_SKILL, "aisa-synthesize")

    def test_estimate_declares_no_second_authority_explicitly(self):
        t = DELIVERABLES["estimate"]
        self.assertPhrase("exactly ONE implementation-effort authority",
                          t.field_text("no_second_estimate_authority"), "estimate")

    def test_no_new_engine_or_skill_is_introduced(self):
        skills = sorted(d for d in os.listdir(SKILLS)
                        if os.path.isdir(os.path.join(SKILLS, d)))
        for banned in ("aisa-estimate", "aisa-project", "aisa-derive", "aisa-deliverable"):
            self.assertNotIn(banned, skills, "no new skill may be introduced")
        self.assertPhrase("No new engine", RENDER_CONTRACT, "render-contract")


# ══════════════════════════════════════════════════════════════════════════════════════
# T-D20 (MANDATORY) — Not-authorized authority / carriage split
# ══════════════════════════════════════════════════════════════════════════════════════

class TestTD20CarriageSplit(Base):

    def test_executive_declares_the_full_split(self):
        self.requireYaml()
        c = DELIVERABLES["executive-report"].get("not_authorized_carriage")
        self.assertIsInstance(c, dict)
        ob = c.get("outcome_basis") or {}
        ab = c.get("architectability_basis") or {}
        self.assertPhrase("Options", as_text(ob.get("semantic_owner")), "executive outcome basis")
        self.assertPhrase("decisions.md", as_text(ob.get("durable_source")),
                          "executive outcome basis")
        self.assertPhrase("architecture-entry gate", as_text(ab.get("semantic_owner")),
                          "executive architectability basis")
        self.assertPhrase("architecture-story.md", as_text(ab.get("durable_carrier")),
                          "executive architectability basis")

    def test_executive_states_carrier_not_authority(self):
        self.requireYaml()
        ab = (DELIVERABLES["executive-report"].get("not_authorized_carriage") or {}).get(
            "architectability_basis") or {}
        note = as_text(ab.get("note"))
        self.assertPhrase("DURABLE CARRIER, NOT SEMANTIC AUTHORITY", note, "executive")
        self.assertPhrase("never re-evaluates pack architectability", note, "executive")

    def test_architecture_story_declares_itself_carrier_not_authority(self):
        self.requireYaml()
        t = SYNTH["architecture-story.template.md"]
        self.assertIs(False, t.get("is_architecture_authority"))
        car = t.get("carriage") or {}
        ab = car.get("architectability_basis") or {}
        self.assertEqual("durable carrier", str(ab.get("role")).strip())
        self.assertIs(False, ab.get("is_semantic_authority"))
        self.assertPhrase("architecture-entry gate", as_text(ab.get("semantic_owner")),
                          "architecture-story")
        self.assertPhrase("this one basis only", as_text(ab.get("exception_scope")),
                          "architecture-story")

    def test_architecture_story_says_the_words_distinctly(self):
        t = SYNTH["architecture-story.template.md"]
        self.assertPhrase("DURABLE CARRIER — NOT SEMANTIC AUTHORITY", t.raw,
                          "architecture-story")
        self.assertPhrase("SEMANTIC OWNER of the architectability basis is the ARCHITECTURE-ENTRY GATE RULE",
                          t.raw, "architecture-story")
        self.assertPhrase("does NOT own the rule", t.raw, "architecture-story")
        self.assertPhrase("only carriage exception", t.raw, "architecture-story")

    def test_no_deliverable_re_evaluates_pack_architectability(self):
        for rid, t in DELIVERABLES.items():
            self.assertNoPhrase("evaluate whether this pack can architect", t.raw, rid)
            self.assertNoPhrase("re-evaluate architectability", t.raw, rid)
            self.assertNoPhrase("determine architectability", t.raw, rid)

    def test_blueprint_contract_carries_the_entry_gate_sentence(self):
        self.assertPhrase("Where the entry gate yields `not-authorized`", BLUEPRINT_CONTRACT,
                          "blueprint-contract")
        self.assertPhrase("semantic owner is this entry gate", BLUEPRINT_CONTRACT,
                          "blueprint-contract")
        self.assertPhrase("durably carried", BLUEPRINT_CONTRACT, "blueprint-contract")
        self.assertPhrase("never as a source of architectural truth", BLUEPRINT_CONTRACT,
                          "blueprint-contract")
        self.assertPhrase("no new artefact, no empty blueprint, no new field",
                          BLUEPRINT_CONTRACT, "blueprint-contract")

    def test_render_and_synthesize_skills_both_state_the_split(self):
        for text, label in ((RENDER_SKILL, "aisa-render"), (SYNTH_SKILL, "aisa-synthesize")):
            self.assertPhrase("durable carrier", text, label)
            self.assertPhrase("ARCHITECTURE-ENTRY GATE RULE", text, label)
            self.assertPhrase("re-evaluate", text, label)

    def test_positive_non_pp_outcome_is_never_relabelled_decision_blocked(self):
        t = DELIVERABLES["executive-report"]
        self.assertPhrase("relabelling a positive non-PP outcome as `Decision Blocked`",
                          t.field_text("forbidden_transformations"), "executive")
        self.assertPhrase("Decision Blocked", t.body, "executive body")
        self.assertPhrase("não significa que esta plataforma perdeu", t.body,
                          "executive body")
        self.assertPhrase("nada se infere", t.body, "executive body")

    def test_no_inference_about_the_selected_non_pp_solution(self):
        t = DELIVERABLES["executive-report"]
        self.assertPhrase("inferring anything about a non-PP selected solution",
                          t.field_text("forbidden_transformations"), "executive")


# ══════════════════════════════════════════════════════════════════════════════════════
# T-D21 (MANDATORY) — A structural open choice blocks the Design Brief
# ══════════════════════════════════════════════════════════════════════════════════════

class TestTD21StructuralBlock(Base):

    def test_design_brief_declares_the_whole_chain(self):
        t = DELIVERABLES["claude-design-brief"]
        rule = t.field_text("structural_block_rule")
        for must in ["structural: true", "blueprint approval blocked",
                     "Implementation Specification BLOCKED", "Claude Design Brief BLOCKED"]:
            self.assertPhrase(must, rule, "design brief structural_block_rule")

    def test_design_brief_declares_no_exception(self):
        t = DELIVERABLES["claude-design-brief"]
        rule = t.field_text("structural_block_rule")
        self.assertPhrase("NO materiality override", rule, "design brief")
        self.assertPhrase("NO partial approval", rule, "design brief")
        self.assertPhrase("NO UX-only approval", rule, "design brief")
        self.assertPhrase("NO exception based on whether the unresolved choice is judged UX-material",
                          rule, "design brief")

    def test_design_brief_activation_encodes_no_exception(self):
        t = DELIVERABLES["claude-design-brief"]
        act = t.field_text("activation")
        self.assertPhrase("structural:true", act, "design brief activation")
        self.assertPhrase("BLOCKED (NO EXCEPTION)", act, "design brief activation")

    def test_impl_spec_declares_the_same_block(self):
        t = DELIVERABLES["implementation-spec"]
        self.assertPhrase("structural:true", t.field_text("blocked_when"), "impl-spec")
        self.assertPhrase("no new machinery, no override", t.fm_text, "impl-spec")

    def test_no_partial_or_ux_only_approval_token_exists_anywhere(self):
        banned = ["partial approval", "partially approved", "ux-only approval",
                  "approve the ux only", "aprovação parcial",
                  "aprovação só-de-ux"]
        targets = [(t.raw, rid) for rid, t in DELIVERABLES.items()]
        targets += [(t.raw, fn) for fn, t in SYNTH.items()]
        targets += [(RENDER_SKILL, "aisa-render"), (SYNTH_SKILL, "aisa-synthesize"),
                    (RENDER_CONTRACT, "render-contract"),
                    (BLUEPRINT_CONTRACT, "blueprint-contract")]
        for text, label in targets:
            for b in banned:
                # Legal only inside an explicit prohibition ("no partial approval").
                self.assertOnlyProhibited(b, text, label)

    def test_blueprint_still_renders_both_candidates_while_blocked(self):
        t = DELIVERABLES["solution-blueprint"]
        self.assertPhrase("bloqueia a **aprovação** do blueprint — nunca a sua **produção**",
                          t.body, "blueprint body")
        self.assertPhrase("ficam **bloqueados**", t.body, "blueprint body")

    def test_render_skill_encodes_the_mechanical_chain(self):
        self.assertPhrase("Structural blocking is mechanical", RENDER_SKILL, "aisa-render")
        self.assertPhrase("no materiality override, no partial approval, no UX-only approval",
                          RENDER_SKILL, "aisa-render")
        self.assertPhrase("is **wrong**", RENDER_SKILL, "aisa-render")

    def test_blueprint_contract_hard_rule_five_is_intact(self):
        self.assertPhrase("A structural open architecture choice blocks approval",
                          BLUEPRINT_CONTRACT, "blueprint-contract")
        self.assertPhrase("it never blocks its **production**", BLUEPRINT_CONTRACT,
                          "blueprint-contract")


# ══════════════════════════════════════════════════════════════════════════════════════
# T-D22 (MANDATORY) — Estimate input modes: exactly two
# ══════════════════════════════════════════════════════════════════════════════════════

MODE_B_LABEL = ("Candidate planning estimate - pre-Implementation-Specification; "
                "lower-confidence; architecture choice unresolved.")


class TestTD22EstimateInputModes(Base):

    def test_exactly_two_input_modes_are_declared(self):
        self.requireYaml()
        t = DELIVERABLES["estimate"]
        modes = t.get("input_modes")
        self.assertIsInstance(modes, dict)
        self.assertEqual({"A", "B"}, set(modes.keys()), "exactly modes A and B")
        self.assertEqual(2, len(modes))
        self.assertEqual(2, int(t.get("input_modes_count")))

    def test_no_third_mode_is_declared(self):
        self.requireYaml()
        t = DELIVERABLES["estimate"]
        self.assertPhrase("There is no third input mode", t.field_text("no_third_mode"),
                          "estimate")
        self.assertPhrase("BLOCKED or", t.field_text("no_third_mode"), "estimate")
        self.assertNoPhrase("mode C", t.raw, "estimate")

    def test_mode_a_is_the_specification_inventory(self):
        self.requireYaml()
        a = as_text((DELIVERABLES["estimate"].get("input_modes") or {}).get("A"))
        self.assertPhrase("implementation estimate", a, "estimate mode A")
        self.assertPhrase("Implementation Specification's inventory", a, "estimate mode A")
        self.assertPhrase("MAY NOT ADD A WORK UNIT ABSENT FROM THAT", a, "estimate mode A")
        self.assertPhrase("OPEN WORK ITEM", a, "estimate mode A")

    def test_mode_b_is_the_candidate_planning_inventory(self):
        self.requireYaml()
        b = as_text((DELIVERABLES["estimate"].get("input_modes") or {}).get("B"))
        self.assertPhrase("candidate planning estimate", b, "estimate mode B")
        self.assertPhrase("candidate architecture components", b, "estimate mode B")
        self.assertPhrase("architecture candidates exist", b, "estimate mode B")
        self.assertPhrase("approval is blocked by the unresolved structural choice", b,
                          "estimate mode B")
        self.assertPhrase("sponsor materially needs comparative delivery magnitude", b,
                          "estimate mode B")

    def test_mode_b_carries_the_mandatory_label_verbatim(self):
        self.requireYaml()
        b = (DELIVERABLES["estimate"].get("input_modes") or {}).get("B") or {}
        label = as_text(b.get("mandatory_label"))
        self.assertTrue(label.strip(), "mode B must declare its mandatory label")
        norm = flat(label).replace("—", "-").replace("  ", " ").strip()
        self.assertEqual(MODE_B_LABEL.lower(), norm.lower(),
                         "mode B label must be verbatim; got %r" % norm)

    def test_the_mandatory_label_also_appears_in_the_rendered_body(self):
        body = flat(DELIVERABLES["estimate"].body).replace("—", "-")
        self.assertIn(MODE_B_LABEL.lower(), body.lower(),
                      "the body must carry the mode-B label verbatim")

    def test_per_candidate_isolation_is_declared(self):
        self.requireYaml()
        b = (DELIVERABLES["estimate"].get("input_modes") or {}).get("B") or {}
        iso = as_text(b.get("isolation"))
        for must in ["its own work inventory", "its own estimate", "its own uncertainty",
                     "its own confidence"]:
            self.assertPhrase(must, iso, "estimate mode B isolation")
        self.assertPhrase("NEVER blend candidates", iso, "estimate mode B isolation")
        self.assertPhrase("NEVER select a candidate", iso, "estimate mode B isolation")
        self.assertPhrase("NEVER rank them", iso, "estimate mode B isolation")

    def test_no_blended_figure_is_permitted_by_any_slot_or_transformation(self):
        self.requireYaml()
        t = DELIVERABLES["estimate"]
        self.assertPhrase("blending candidate estimates into one figure",
                          t.field_text("forbidden_transformations"), "estimate")
        srcs = t.slot_sources_text()
        self.assertPhrase("one separately labelled block per candidate", srcs,
                          "estimate candidate_estimates slot")
        self.assertNotIn("blended", srcs.lower())

    def test_mode_b_may_not_invent_spec_tasks(self):
        self.requireYaml()
        b = (DELIVERABLES["estimate"].get("input_modes") or {}).get("B") or {}
        mn = as_text(b.get("may_not_estimate"))
        for must in ["detailed implementation tasks not yet derivable",
                     "screen-level work while the UX blueprint is unapproved",
                     "an unevaluated far side"]:
            self.assertPhrase(must, mn, "estimate mode B may_not_estimate")
        self.assertPhrase("no spec != permission to invent a spec",
                          as_text(b.get("scope_control")), "estimate mode B")

    def test_both_modes_declare_their_scope_control(self):
        self.requireYaml()
        modes = DELIVERABLES["estimate"].get("input_modes") or {}
        for k in ("A", "B"):
            self.assertTrue(as_text((modes.get(k) or {}).get("scope_control")).strip(),
                            "mode %s must declare scope_control" % k)

    def test_candidate_estimates_slot_is_conditional_on_mode_b(self):
        self.requireYaml()
        t = DELIVERABLES["estimate"]
        self.assertIn("candidate_estimates", t.slots("conditional"))
        cond = as_text((t.get("slot_conditions") or {}).get("candidate_estimates"))
        self.assertPhrase("input mode == B", cond, "estimate candidate_estimates condition")

    def test_render_skill_selects_between_exactly_two_modes(self):
        self.assertPhrase("exactly two modes, and no third", RENDER_SKILL, "aisa-render")
        self.assertPhrase("MODE A", RENDER_SKILL, "aisa-render")
        self.assertPhrase("MODE B", RENDER_SKILL, "aisa-render")
        self.assertPhrase("no spec  ≠  permission to invent a spec", RENDER_SKILL,
                          "aisa-render")
        self.assertPhrase("NEVER blend", RENDER_SKILL, "aisa-render")


# ══════════════════════════════════════════════════════════════════════════════════════
# Complexity guard — no new reasoning layer, router or state machine
# ══════════════════════════════════════════════════════════════════════════════════════

class TestNoNewMachinery(Base):

    def test_no_projection_router_is_introduced(self):
        targets = [(t.raw, rid) for rid, t in DELIVERABLES.items()]
        targets += [(PACK_RAW, "pack.yaml"), (RENDER_SKILL, "aisa-render"),
                    (RENDER_CONTRACT, "render-contract")]
        for text, label in targets:
            self.assertOnlyProhibited("router", text, label)

    def test_no_new_state_machine_is_introduced(self):
        for text, label in ((RENDER_CONTRACT, "render-contract"), (RENDER_SKILL, "aisa-render"),
                            (PACK_RAW, "pack.yaml")):
            self.assertOnlyProhibited("state machine", text, label)

    def test_render_contract_states_the_execution_boundary(self):
        self.assertPhrase("Render executes a projection contract; it does not reason beyond that contract",
                          RENDER_CONTRACT, "render-contract")
        self.assertPhrase("Render executes a projection contract; it does not reason beyond that contract",
                          RENDER_SKILL, "aisa-render")

    def test_reasoning_versus_projection_distinction_is_declared(self):
        for text, label in ((RENDER_CONTRACT, "render-contract"), (RENDER_SKILL, "aisa-render")):
            self.assertPhrase("deterministic", text, label)
            self.assertPhrase("bounded", text, label)
            self.assertPhrase("declared", text, label)
            self.assertPhrase("traceable", text, label)

    def test_docs_no_longer_describe_the_branch_mechanism(self):
        for fn in ("ARCHITECTURE.md", "PACK_AUTHORING.md"):
            text = read(os.path.join(DOCS, fn))
            self.assertNotIn("chosen_architecture", text, "%s still documents the dead slot" % fn)
            self.assertNotIn("{{chosen_architecture}}", text)
            self.assertOnlyProhibited("<chosen>", text, fn)

    def test_docs_reflect_the_fixed_architecture_layer(self):
        arch = read(os.path.join(DOCS, "ARCHITECTURE.md"))
        pa = read(os.path.join(DOCS, "PACK_AUTHORING.md"))
        self.assertPhrase("architecture-templates/architecture-core.md", arch, "ARCHITECTURE.md")
        self.assertPhrase("Contratos de projecção", arch, "ARCHITECTURE.md")
        self.assertPhrase("Deliverable templates are projection contracts", pa,
                          "PACK_AUTHORING.md")
        self.assertPhrase("no per-branch sub-template", pa, "PACK_AUTHORING.md")


# ═══════════════════════════════════════════════════════════════════════════════════
# R-1 (BOUNDED REPAIR, outside the canonical T-D numbering) — the Estimate does not
#       consume the as-is synthesis.
#
# Step 6B DV-1 had given the Estimate a read edge to `_synthesis/as-is.md` (operational-impact
# timings). The frozen Step 6A Estimate source contract (§28.6, §14.1, §18.1) authorizes only:
#   MODE A: Implementation Specification inventory + craft/estimation-model.md + decision scope
#   MODE B: candidate architecture record + candidate-specific KNOWN obligations
#           + craft/estimation-model.md + decision scope
# `_synthesis/as-is.md` is NOT required, NOT conditional, NOT fallback, NOT point-of-need.
#
# T-D1...T-D22 coverage is UNCHANGED at 22/22 by this class.
# ═══════════════════════════════════════════════════════════════════════════════════

# Fields the renderer reads as a place the Estimate MAY take content from.
ESTIMATE_ALLOWED_SOURCE_FIELDS = [
    "authority_sources", "conditional_sources", "slot_sources", "slot_conditions",
    "input_modes", "input_inventory_authority", "method_authority", "selective_pulls",
    "permitted_transformations", "permitted_outputs",
]


class TestR1EstimateDoesNotConsumeAsIs(Base):

    def test_estimate_names_as_is_in_no_allowed_source_field(self):
        self.requireYaml()
        t = DELIVERABLES["estimate"]
        for field in ESTIMATE_ALLOWED_SOURCE_FIELDS:
            txt = t.field_text(field)
            self.assertNotIn("as-is", txt.lower(),
                             "estimate: %s names the as-is synthesis" % field)
            self.assertNotIn("_synthesis/as-is", txt,
                             "estimate: %s names the as-is synthesis" % field)

    def test_estimate_declares_as_is_forbidden_in_all_four_ways(self):
        self.requireYaml()
        fs = DELIVERABLES["estimate"].field_text("forbidden_sources")
        self.assertPhrase("_synthesis/as-is.md", fs, "estimate forbidden_sources")
        for must in ["NOT required", "NOT conditional", "NOT fallback", "NOT point-of-need"]:
            self.assertPhrase(must, fs, "estimate forbidden_sources")

    def test_estimate_forbids_discovery_narrative_as_a_work_unit_source(self):
        self.requireYaml()
        t = DELIVERABLES["estimate"]
        fb = t.field_text("forbidden_transformations")
        for must in ["as-is friction", "as-is timing", "as-is exception",
                     "discovery narrative"]:
            self.assertPhrase(must, fb, "estimate forbidden_transformations")
        self.assertPhrase("Estimate work unit", fb, "estimate forbidden_transformations")
        self.assertPhrase("any discovery narrative as the source of a work unit",
                          t.field_text("forbidden_sources"), "estimate forbidden_sources")

    def test_the_missing_fact_path_is_an_open_work_item_not_an_estimate_line(self):
        self.requireYaml()
        fb = DELIVERABLES["estimate"].field_text("forbidden_transformations")
        self.assertPhrase("OPEN WORK ITEM against the Implementation Specification", fb,
                          "estimate mode A escape hatch")
        self.assertPhrase("never an Estimate line", fb, "estimate mode A escape hatch")
        self.assertPhrase("candidate-specific KNOWN architecture obligation", fb,
                          "estimate mode B escape hatch")
        self.assertPhrase("the uncertainty is PRESERVED, not resolved", fb,
                          "estimate mode B escape hatch")

    def test_operational_impact_is_sourced_from_the_active_modes_inventory_only(self):
        self.requireYaml()
        t = DELIVERABLES["estimate"]
        # Still a CONDITIONAL slot -- the repair removed a source, not the section.
        self.assertIn("operational_impact", t.slots("conditional"))
        src = as_text((t.get("slot_sources") or {}).get("operational_impact"))
        self.assertPhrase("MODE A", src, "operational_impact source")
        self.assertPhrase("Implementation Specification's inventory", src,
                          "operational_impact source")
        self.assertPhrase("MODE B", src, "operational_impact source")
        self.assertPhrase("KNOWN obligations", src, "operational_impact source")
        self.assertPhrase("NOT APPLICABLE", src, "operational_impact source")
        # No replacement source edge was added.
        self.assertNotIn("shared-understanding.md", src)
        self.assertNotIn("_capture", src)
        self.assertNotIn("business-story", src)

    def test_no_new_source_edge_was_added_to_the_estimate(self):
        self.requireYaml()
        t = DELIVERABLES["estimate"]
        allowed = " ".join(t.field_text(f) for f in ESTIMATE_ALLOWED_SOURCE_FIELDS)
        # The Estimate reads exactly the frozen mode A / mode B inputs (+ its own conditionals).
        for banned in ["_synthesis/as-is.md", "_synthesis/business-story.md",
                       "_capture/evidence-index.md", "frame.md", "options.md",
                       "lens-outputs/"]:
            self.assertNotIn(banned, allowed,
                             "estimate source contract widened with %s" % banned)

    def test_estimate_body_does_not_anchor_to_the_as_is_narrative(self):
        t = DELIVERABLES["estimate"]
        # The body may state the prohibition; it may not name as-is as an anchor.
        self.assertOnlyProhibited("as-is", t.body, "estimate body")
        self.assertNoPhrase("ancorada aos tempos registados no as-is", t.body, "estimate body")

    def test_render_skill_does_not_use_as_is_as_an_estimate_input(self):
        # Locate the Estimate execution section and assert as-is appears only as prohibited.
        i = RENDER_SKILL.find("Estimate — bounded calculation execution")
        self.assertNotEqual(-1, i, "estimate execution section not found in aisa-render")
        section = RENDER_SKILL[i:]
        self.assertOnlyProhibited("as-is", section, "aisa-render estimate section")
        self.assertPhrase("No discovery re-read", section, "aisa-render")
        self.assertPhrase("not an Estimate input in either mode", section, "aisa-render")
        self.assertPhrase("calculates only over work whose authority it can name", section,
                          "aisa-render")

    def test_as_is_template_does_not_name_the_estimate_as_a_consumer(self):
        t = SYNTH["as-is.template.md"]
        # The CONSUMER declaration must name the Discovery Report and nothing else.
        m = re.search(r"CONSUMER[^:]*:(.*?)(?:FORBIDDEN CONSUMERS)", flat(t.raw), re.S)
        self.assertIsNotNone(m, "as-is must carry a CONSUMER declaration")
        consumer_decl = m.group(1)
        self.assertPhrase("Discovery Report", consumer_decl, "as-is CONSUMER declaration")
        self.assertNotIn("estimate", consumer_decl.lower(),
                         "as-is names the Estimate as a consumer")
        # And the Estimate is explicitly declared a forbidden consumer, four ways.
        self.assertPhrase("NOT an Estimate source in either input mode", t.raw,
                          "as-is.template.md")
        for must in ["not required", "not conditional", "not fallback", "not point-of-need"]:
            self.assertPhrase(must, t.raw, "as-is.template.md")
        self.assertPhrase("FORBIDDEN CONSUMERS", t.raw, "as-is.template.md")

    def test_as_is_states_the_authorized_effort_path(self):
        t = SYNTH["as-is.template.md"]
        self.assertPhrase("Implementation Specification's work inventory (mode A)", t.raw,
                          "as-is.template.md")
        self.assertPhrase("candidate-specific KNOWN architecture obligation (mode B)", t.raw,
                          "as-is.template.md")

    def test_as_is_labels_discovery_as_consumer_not_authority(self):
        t = SYNTH["as-is.template.md"]
        self.assertPhrase("the Discovery Report, which PROJECTS this narrative", t.raw,
                          "as-is.template.md")
        self.assertPhrase("NEITHER is source authority", t.raw, "as-is.template.md")
        self.assertPhrase("Authority stays upstream", t.raw, "as-is.template.md")
        # The upstream authorities Step 6A names.
        for must in ["Shared Understanding", "capture / evidence index", "framing record"]:
            self.assertPhrase(must, t.raw, "as-is.template.md")
        # And the old wording is gone.
        self.assertNoPhrase("the Discovery Report reads this as an authority source", t.raw,
                            "as-is.template.md")

    def test_no_deliverable_labels_the_discovery_report_as_source_authority(self):
        for rid, t in list(DELIVERABLES.items()) + list(SYNTH.items()):
            self.assertNoPhrase("Discovery Report is the authority", t.raw, rid)
            self.assertNoPhrase("Discovery Report as authority", t.raw, rid)
            self.assertNoPhrase("Discovery Report reads this as an authority", t.raw, rid)

    def test_as_is_content_was_not_redesigned(self):
        """The repair touched the consumer contract only -- the narrative shape is intact."""
        t = SYNTH["as-is.template.md"]
        for section in ["## End-to-end process today", "## Volume and cycle time",
                        "## Personas and their experience",
                        "## Exceptions, handoffs, and tribal knowledge",
                        "## Top friction points"]:
            self.assertIn(section, t.raw, "as-is lost %r" % section)
        self.assertNotIn("owns_calculation", t.raw, "as-is must own no calculation")
        # No effort CONTENT: the file may state the authorized effort PATH and its own
        # prohibitions, but it must carry no calculation, table shape or figure instruction.
        for banned in ["person-day", "effort table", "phase table", "day count",
                       "effort band", "contingency", "% buffer"]:
            self.assertNotIn(banned, t.raw.lower(),
                             "as-is must carry no estimate content: %r" % banned)
        for banned in ["work unit", "estimate line"]:
            self.assertOnlyProhibited(banned, t.raw, "as-is.template.md")


# ═══════════════════════════════════════════════════════════════════════════════════
# R-2 (BOUNDED REPAIR) — DV-2: exactly TWO bounded deliverable→deliverable edges.
# Documentation-count correction only; both edges were already authorized by the frozen model.
# ═══════════════════════════════════════════════════════════════════════════════════

class TestR2TwoBoundedReadEdges(Base):

    def test_render_contract_states_exactly_two_bounded_edges(self):
        self.assertPhrase("Exactly two bounded deliverable", RENDER_CONTRACT,
                          "render-contract")
        self.assertPhrase("and no third", RENDER_CONTRACT, "render-contract")
        self.assertNoPhrase("The one permitted deliverable", RENDER_CONTRACT,
                            "render-contract (stale count)")

    def test_docs_state_exactly_two_bounded_edges(self):
        arch = read(os.path.join(DOCS, "ARCHITECTURE.md"))
        self.assertPhrase("Exactamente duas arestas deliverable", arch, "ARCHITECTURE.md")
        self.assertNoPhrase("Uma única aresta deliverable", arch,
                            "ARCHITECTURE.md (stale count)")

    def test_each_edge_declares_its_bounded_payload(self):
        self.assertPhrase("inventory only", RENDER_CONTRACT, "render-contract")
        self.assertPhrase("the headline only", RENDER_CONTRACT, "render-contract")
        self.assertPhrase("one investment paragraph", RENDER_CONTRACT, "render-contract")

    def test_the_executive_estimate_read_is_not_expanded(self):
        """The Executive reads the headline ONLY -- never the Estimate's internals."""
        for excluded in ["phases", "work breakdown", "team mix", "detailed range derivation",
                         "contingency detail", "candidate inventories"]:
            self.assertPhrase(excluded, RENDER_CONTRACT,
                              "render-contract must name %r as excluded" % excluded)
        t = DELIVERABLES["executive-report"]
        src = as_text((t.get("slot_sources") or {}).get("investment_summary"))
        self.assertPhrase("headline", src, "executive investment_summary")
        self.assertPhrase("ONE paragraph", src, "executive investment_summary")
        self.assertPhrase("the Estimate owns the figure", src, "executive investment_summary")
        for banned in ["phases_table", "work_breakdown", "team_effort", "effort_bands",
                       "range_and_contingency", "candidate_estimates"]:
            self.assertNotIn(banned, src,
                             "executive must not read the Estimate's %s" % banned)

    def test_the_executive_stays_complete_without_an_estimate(self):
        t = DELIVERABLES["executive-report"]
        self.assertIn("investment_summary", t.slots("conditional"),
                      "the investment paragraph is conditional on an Estimate existing")
        self.assertNotIn("investment_summary", t.slots("required"))
        self.assertPhrase("complete without an implementation-effort paragraph",
                          RENDER_CONTRACT, "render-contract")
        self.assertPhrase("no gap, no placeholder", RENDER_CONTRACT, "render-contract")

    def test_no_third_deliverable_read_edge(self):
        self.requireYaml()
        edges = set()
        for rid, t in DELIVERABLES.items():
            for target in re.findall(r"_render/<slug>_([a-z-]+)_v", t.sources_text()):
                edges.add((rid, target))
            if rid == "estimate" and has("Implementation Specification's inventory",
                                         t.sources_text()):
                edges.add(("estimate", "implementation-spec"))
        self.assertEqual({("estimate", "implementation-spec"),
                          ("executive-report", "estimate")}, edges,
                         "exactly two bounded deliverable->deliverable edges")


# ══════════════════════════════════════════════════════════════════════════════════════
# R-3 (BOUNDED REPAIR, outside the canonical T-D numbering) — a build-gating condition
#       cannot disappear from the Implementation Specification.
#
# Step 6C initial gate, defect F-1: a condition recorded as gating build start
# ("validado com o auditor interno ANTES DO ARRANQUE DE CONSTRUÇÃO") rendered in the
# Executive Report and vanished from the Implementation Specification. Step 6A §17.1 states
# the non-negotiable; the runtime carried no structural guard for it, and conditions reached
# the Specification only through `slot_sources.open_work_items`.
#
# A condition with an owner, a funding state and a due date is NOT an open work item.
#
# T-D1...T-D22 coverage is UNCHANGED at 22/22 by this class.
# ══════════════════════════════════════════════════════════════════════════════════════


class TestR3BuildGatingConditionCarriage(Base):

    def spec(self):
        return DELIVERABLES["implementation-spec"]

    def test_spec_declares_non_omissible_content(self):
        self.requireYaml()
        no = self.spec().listy("non_omissible")
        self.assertTrue(no, "implementation-spec declares no non_omissible content")
        joined = " ".join(no).lower()
        self.assertIn("build_gating_conditions", joined,
                      "non_omissible must name build-gating conditions")
        self.assertIn("precondition", joined, "non_omissible must name preconditions")

    def test_spec_declares_a_dedicated_build_gate_carriage_path(self):
        self.requireYaml()
        bg = self.spec().get("build_gates")
        self.assertIsInstance(bg, dict, "no build_gates carriage path declared")
        for key in ["source", "include_if", "preserved_per_gate",
                    "identities_preserved", "satisfaction_rule"]:
            self.assertIn(key, bg, "build_gates missing %r" % key)

    def test_build_gate_source_is_the_decision_record(self):
        self.requireYaml()
        src = as_text(self.spec().get("build_gates").get("source"))
        self.assertIn("decisions.md", src)
        self.assertIn("Conditions", src)
        self.assertIn("Preconditions", src)

    def test_build_gate_preserves_owner_funding_date_and_what_it_gates(self):
        self.requireYaml()
        kept = as_text(self.spec().get("build_gates").get("preserved_per_gate")).lower()
        for field in ["condition text", "owner", "funded", "by_when", "gates"]:
            self.assertIn(field, kept, "preserved_per_gate must keep %r" % field)

    def test_build_gates_is_a_declared_slot_with_a_condition_source_and_body(self):
        self.requireYaml()
        t = self.spec()
        self.assertIn("build_gates", t.all_slots(), "build_gates is not a declared slot")
        self.assertIn("build_gates", as_text(t.get("slot_conditions")), "no slot condition")
        self.assertIn("build_gates", t.slot_sources_text(), "no slot source")
        self.assertIn("build_gates", t.body_slots(), "no body section")

    def test_build_gates_is_required_subject_to_existence(self):
        self.requireYaml()
        cond = as_text(self.spec().get("slot_conditions"))
        i = cond.find("build_gates")
        self.assertNotEqual(-1, i)
        self.assertIn("REQUIRED SUBJECT TO EXISTENCE", cond[i:i + 400].upper(),
                      "build_gates must be required subject to existence")

    def test_open_work_items_may_not_absorb_a_build_gate(self):
        self.requireYaml()
        txt = as_text(self.spec().get("build_gates").get("identities_preserved")).lower()
        self.assertIn("distinct", txt)
        ft = self.spec().field_text("forbidden_transformations").lower()
        self.assertIn("open work item", ft,
                      "forbidden_transformations must reject filing a gate as an open work item")

    def test_a_build_gate_cannot_be_satisfied_by_projection(self):
        self.requireYaml()
        rule = as_text(self.spec().get("build_gates").get("satisfaction_rule"))
        self.assertPhrase("engagement evidence", rule)
        self.assertIn("never satisfies", rule.lower())
        ft = self.spec().field_text("forbidden_transformations").lower()
        self.assertIn("satisfied", ft,
                      "forbidden_transformations must reject rendering a gate as satisfied")

    def test_body_section_states_the_non_negotiable(self):
        low = flat(self.spec().body).lower()
        self.assertIn("{{build_gates}}", self.spec().body)
        self.assertIn("nunca desaparece", low)
        self.assertIn("not named", low)


# ══════════════════════════════════════════════════════════════════════════════════════
# R-4 (BOUNDED REPAIR) — the Estimate -> Executive edge carries a BOUNDED headline payload.
#
# Step 6C initial gate, defect F-2: the approved edge projected more than its declared
# payload (team mix, contingency derivation/rate, calendar duration). The edge itself was
# never in question — "headline" was simply never defined as a field list in the contract
# the renderer reads; the exclusion list existed only in render-contract.md.
#
# This class asserts the RECEIVING contract defines the payload. It adds no edge, no source
# and no authority. T-D1...T-D22 coverage is UNCHANGED at 22/22.
# ══════════════════════════════════════════════════════════════════════════════════════

REQUIRED_PAYLOAD_INCLUDES = [
    "base_effort", "effort_range", "contingency_inclusive_total", "confidence_statement",
]
REQUIRED_PAYLOAD_EXCLUDES = [
    "phases", "work_breakdown", "team_mix", "contingency_rate_or_derivation",
    "effort_arithmetic", "duration_or_calendar_schedule", "candidate_inventories",
    "detailed_uncertainty_inventory",
]


class TestR4BoundedInvestmentPayload(Base):

    def exec_t(self):
        return DELIVERABLES["executive-report"]

    def payload(self):
        sp = self.exec_t().get("slot_payload")
        self.assertIsInstance(sp, dict, "executive-report declares no slot_payload")
        ip = sp.get("investment_summary")
        self.assertIsInstance(ip, dict, "slot_payload declares no investment_summary")
        return ip

    def test_investment_summary_declares_its_allowed_fields(self):
        self.requireYaml()
        inc = [str(x) for x in self.payload().get("includes", [])]
        self.assertEqual(REQUIRED_PAYLOAD_INCLUDES, inc,
                         "includes must be exactly the four headline fields")

    def test_investment_summary_declares_its_prohibited_fields(self):
        self.requireYaml()
        exc = set(str(x) for x in self.payload().get("excludes", []))
        for field in REQUIRED_PAYLOAD_EXCLUDES:
            self.assertIn(field, exc, "investment_summary must exclude %r" % field)

    def test_payload_is_one_paragraph_and_attributed(self):
        self.requireYaml()
        ip = self.payload()
        self.assertIn("ONE paragraph", as_text(ip.get("form")))
        attr = as_text(ip.get("attribution")).lower()
        for verb in ["recompute", "re-round", "recombine", "interpolate", "derive"]:
            self.assertIn(verb, attr, "attribution must forbid %r" % verb)

    def test_unresolved_architecture_may_not_be_blended_into_one_headline(self):
        self.requireYaml()
        rule = as_text(self.payload().get("unresolved_architecture_rule")).lower()
        for must in ["may not combine", "midpoint", "combined range", "best candidate"]:
            self.assertIn(must, rule, "unresolved_architecture_rule must forbid %r" % must)

    def test_forbidden_transformations_names_every_excluded_class(self):
        self.requireYaml()
        ft = flat(self.exec_t().field_text("forbidden_transformations")).lower()
        for phrase in ["phases", "work breakdown", "team mix", "contingency derivation",
                       "effort arithmetic", "delivery duration", "calendar schedule",
                       "uncertainty inventory", "candidate inventories"]:
            self.assertIn(phrase, ft, "forbidden_transformations must reject %r" % phrase)

    def test_executive_may_not_recalculate_or_blend(self):
        self.requireYaml()
        ft = flat(self.exec_t().field_text("forbidden_transformations")).lower()
        self.assertIn("recalculating", ft)
        self.assertIn("blending candidate planning estimates", ft)

    def test_slot_source_points_at_the_bounded_payload(self):
        self.requireYaml()
        self.assertIn("slot_payload.investment_summary", self.exec_t().slot_sources_text(),
                      "investment_summary slot source must name its bounded payload")

    def test_estimate_remains_the_effort_authority(self):
        self.requireYaml()
        est = DELIVERABLES["estimate"]
        self.assertTrue(est.get("owns_calculation") is True)
        self.assertIn("estimate", as_text(est.get("semantic_owner")).lower())
        self.assertNotIn("owns_calculation: true",
                         self.exec_t().contract_text().lower(),
                         "the Executive must not claim calculation ownership")

    def test_the_edge_itself_is_unchanged(self):
        self.requireYaml()
        targets = set(re.findall(r"_render/<slug>_([a-z-]+)_v", self.exec_t().sources_text()))
        self.assertEqual({"estimate"}, targets,
                         "the Executive still reads exactly one rendered deliverable")


# ═════════════════════════════════════════════════════════════════════════════════════
# P-8 — state transitions and preconditions with an owner (frente B, step-9d)
# ═════════════════════════════════════════════════════════════════════════════════════

class TestP8StateTransitionsAndPreconditions(unittest.TestCase):
    """A state machine with no async stream still owes §6 a transition block; a delivery
    precondition is never an estimate assumption."""

    def requireYaml(self):
        if yaml is None:
            self.skipTest("PyYAML not installed")

    # -- spec §6: the floor -----------------------------------------------------------
    def spec(self):
        return DELIVERABLES["implementation-spec"]

    def test_flows_slot_declares_the_state_transition_floor(self):
        self.requireYaml()
        cond = as_text(self.spec().get("slot_conditions", {}).get("flows_to_implement"))
        self.assertTrue(cond, "§6 must declare a slot_condition, not inherit `(none)` silently")
        for token in ("state_machine", "approval", "experience.mode != none"):
            self.assertTrue(has(token, cond),
                            "the §6 condition must name %r" % token)
        for element in ("who transitions", "what validates", "notifies whom",
                        "triggers the cycle"):
            self.assertTrue(has(element, cond),
                            "the §6 condition must carry %r" % element)

    def test_no_async_stream_is_not_an_excuse_for_none(self):
        self.requireYaml()
        cond = as_text(self.spec().get("slot_conditions", {}).get("flows_to_implement"))
        self.assertTrue(has("even with NO asynchronous stream in A6", cond),
                        "an empty A6 must not license `(none)` over a live state machine")
        self.assertTrue(has("`(none)` is legitimate ONLY where", cond),
                        "`(none)` must be bounded by an explicit condition")
        ft = self.spec().field_text("forbidden_transformations")
        self.assertTrue(has("rendering §6 as `(none)` while an entity of the APPROVED blueprint", ft),
                        "rendering `(none)` over a state machine must be forbidden outright")

    def test_the_transition_set_is_read_and_the_actor_is_projected(self):
        self.requireYaml()
        src = as_text(self.spec().get("slot_sources", {}).get("flows_to_implement"))
        self.assertTrue(has("entities[].state_machine", src),
                        "the transition set must be READ from the approved blueprint")
        self.assertTrue(has("A7 role and permission model", src),
                        "the actor must be projected from A7, not chosen")
        self.assertTrue(has("`not named`", src),
                        "an unnamed actor must render as `not named`")

    def test_the_actor_and_the_recipient_are_never_invented(self):
        self.requireYaml()
        ft = self.spec().field_text("forbidden_transformations")
        for token in ("inventing the actor", "the validation rule",
                      "the notification recipient", "open work item"):
            self.assertTrue(has(token, ft),
                            "forbidden_transformations must name %r" % token)
        self.assertTrue(has("never fills it by analogy", ft),
                        "filling a transition by analogy with another entity must be forbidden")

    def test_section_six_body_carries_the_four_elements(self):
        body = self.spec().body
        head = body.split("## 7.")[0].split("## 6.")[-1]
        for element in ("quem transiciona", "o que valida", "notifica quem", "dispara o ciclo"):
            self.assertTrue(has(element, head),
                            "§6 prose must carry %r" % element)
        self.assertTrue(has("mesmo sem stream em A6", head),
                        "§6 prose must state the floor holds with an empty A6")

    def test_the_transition_projection_is_declared_permitted(self):
        self.requireYaml()
        pt = self.spec().field_text("permitted_transformations")
        self.assertTrue(has("state-transition obligation", pt),
                        "the transition projection must be a DECLARED permitted transformation")

    # -- estimate: preconditions with an owner ----------------------------------------
    def est(self):
        return DELIVERABLES["estimate"]

    def test_estimate_declares_the_precondition_slot(self):
        self.requireYaml()
        t = self.est()
        self.assertIn("estimate_preconditions", t.slots("conditional"),
                      "delivery preconditions need their own slot")
        self.assertIn("estimate_preconditions", t.body_slots(),
                      "the slot must be placed in the body, not only declared")
        self.assertIn("estimate_preconditions", t.get("slot_conditions", {}))
        self.assertIn("estimate_preconditions", t.get("slot_sources", {}))

    def test_the_precondition_carriage_is_the_build_gate_carriage(self):
        self.requireYaml()
        t = self.est()
        both = (as_text(t.get("slot_conditions", {}).get("estimate_preconditions")) + " "
                + as_text(t.get("slot_sources", {}).get("estimate_preconditions")))
        for element in ("owner", "by when", "WHICH PHASE", "status"):
            self.assertTrue(has(element, both),
                            "the precondition carriage must carry %r" % element)
        self.assertTrue(has("REQUIRED SUBJECT TO EXISTENCE", both),
                        "a precondition present upstream must render, never be compressed away")
        self.assertTrue(has("`not named`", both),
                        "an unnamed owner renders as `not named`, never invented")

    def test_availability_and_access_are_preconditions_not_assumptions(self):
        self.requireYaml()
        t = self.est()
        assumptions = as_text(t.get("slot_sources", {}).get("estimate_assumptions"))
        self.assertTrue(has("METHOD PREMISES ONLY", assumptions),
                        "estimate assumptions must be restricted to method premises")
        for token in ("SME availability", "licences", "provisioning"):
            self.assertTrue(has(token, assumptions),
                            "the restriction must name %r as NOT an assumption" % token)
        self.assertTrue(has("DELIVERY PRECONDITIONS and render in that section", assumptions),
                        "the restriction must say where those go instead")

    def test_a_precondition_may_not_hide_in_contingency_or_uncertainty(self):
        self.requireYaml()
        ft = self.est().field_text("forbidden_transformations")
        self.assertTrue(has("filing a DELIVERY PRECONDITION", ft))
        for token in ("as an estimate assumption", "as a named uncertainty",
                      "inside contingency"):
            self.assertTrue(has(token, ft),
                            "forbidden_transformations must close %r" % token)
        self.assertTrue(has("rendering a delivery precondition as satisfied", ft),
                        "projection may never satisfy a precondition")

    def test_a_precondition_gates_a_phase_and_never_becomes_a_duration(self):
        self.requireYaml()
        pt = self.est().field_text("permitted_transformations")
        self.assertTrue(has("gate on a NAMED phase", pt))
        self.assertTrue(has("never a duration, never a work unit", pt),
                        "a precondition must not turn into effort")

    def test_the_dedication_is_declared_once_and_read_twice(self):
        self.requireYaml()
        src = as_text(self.est().get("slot_sources", {}).get("estimate_preconditions"))
        self.assertTrue(has("DEDICATION", src))
        self.assertTrue(has("profile-load calculation", src),
                        "the dedication declared here must be the profile-load input")

    def test_estimate_sections_stay_contiguous_after_the_insert(self):
        nums = [int(n) for n in re.findall(r"(?m)^## (\d+)\. ", self.est().body)]
        self.assertEqual(nums, list(range(1, len(nums) + 1)),
                         "section numbering must stay contiguous: %r" % nums)
        head = self.est().body.split("## 15.")[0].split("## 14.")[-1]
        self.assertTrue(has("que fase trava", head),
                        "§14 prose must ask which phase the precondition blocks")


# ═════════════════════════════════════════════════════════════════════════════════════
# P-9 — tasks in a planning interval, profile load; + F09 — intervals, not quantiles
# ═════════════════════════════════════════════════════════════════════════════════════

class TestP9BandsAndProfileLoad(unittest.TestCase):
    """A five-day phase owes its tasks; a profile owes its occupancy; neither owes a Gantt."""

    def requireYaml(self):
        if yaml is None:
            self.skipTest("PyYAML not installed")

    def est(self):
        return DELIVERABLES["estimate"]

    def cond(self, slot):
        return as_text(self.est().get("slot_conditions", {}).get(slot))

    # -- phases decompose, and the total does not move --------------------------------
    def test_a_five_day_phase_owes_a_task_sub_table(self):
        self.requireYaml()
        c = self.cond("phases_table")
        self.assertTrue(c, "phases_table must declare its decomposition floor")
        self.assertTrue(has("figure is >= 5 person-days", c), "the floor is five person-days")
        for token in ("task ·", "planning interval", "responsible profile"):
            self.assertTrue(has(token, c), "the sub-table must carry %r" % token)
        self.assertTrue(has("sum(min) <= phase figure <= sum(max)", c),
                        "the union of the intervals must CONTAIN the phase figure")
        self.assertTrue(has("under 5 person-days is NOT decomposed", c),
                        "granularity below the floor must not be fabricated")

    def test_decomposition_never_moves_a_figure(self):
        self.requireYaml()
        c = self.cond("phases_table")
        self.assertTrue(has("never changes the phase figure and never changes the global total", c))
        ft = self.est().field_text("forbidden_transformations")
        self.assertTrue(has("decomposing a phase in a way that changes its figure", ft))
        self.assertTrue(has("REDISTRIBUTES what the phase already carries", ft),
                        "the sub-table must be declared a redistribution, not new work")
        self.assertTrue(has("fabricating task granularity", ft))

    def test_the_phases_table_carries_the_responsible_profile(self):
        self.requireYaml()
        src = as_text(self.est().get("slot_sources", {}).get("phases_table"))
        self.assertTrue(has("responsible profile from `team_effort`", src),
                        "the profile column must be read from team_effort, not invented")

    # -- profile load ------------------------------------------------------------------
    def test_profile_load_is_declared_and_placed(self):
        self.requireYaml()
        t = self.est()
        self.assertIn("profile_load", t.slots("conditional"))
        self.assertIn("profile_load", t.body_slots(),
                      "profile_load must be placed in the body, not only declared")
        self.assertIn("profile_load", t.get("slot_conditions", {}))
        self.assertIn("profile_load", t.get("slot_sources", {}))

    def test_profile_load_is_arithmetic_over_a_declared_dedication(self):
        self.requireYaml()
        c = self.cond("profile_load")
        self.assertTrue(has("person-days / dedication -> minimum weeks", c),
                        "the calculation must be declared explicitly")
        self.assertTrue(has("ARITHMETIC ONLY", c))
        self.assertTrue(has("`dedication not named`", c),
                        "an undeclared dedication must render as such, with no week figure")
        src = as_text(self.est().get("slot_sources", {}).get("profile_load"))
        self.assertTrue(has("read from the preconditions section", src),
                        "the dedication is declared once, in the preconditions")

    def test_no_grid_no_gantt_no_derived_overlap(self):
        self.requireYaml()
        c = self.cond("profile_load")
        self.assertTrue(has("no grid, no calendar date, no derived overlap", c))
        self.assertTrue(has("CONSTRAINT ON PARALLELISM in prose", c),
                        "dependencies stay a prose constraint, never a schedule")
        ft = self.est().field_text("forbidden_transformations")
        for token in ("a weekly grid", "a Gantt", "a calendar date",
                      "derived overlap between profiles"):
            self.assertTrue(has(token, ft),
                            "forbidden_transformations must close %r" % token)

    # -- an uncertainty lands in the phase it threatens --------------------------------
    def test_each_uncertainty_lands_in_the_phase_it_threatens(self):
        self.requireYaml()
        c = self.cond("named_uncertainties")
        self.assertTrue(c, "named_uncertainties must declare the cross-reference")
        self.assertTrue(has("ALSO appears, on ONE line, in the phase", c))
        self.assertTrue(has("cross-referenced by its id", c))
        self.assertTrue(has("never a second uncertainty", c),
                        "the cross-reference must not duplicate the item")
        self.assertTrue(has("threatens no phase says so", c),
                        "an uncertainty that threatens no phase must still say so")

    # -- a repetition dimension earns a pilot over a NAMED subset ---------------------
    def test_a_repetition_dimension_earns_a_named_pilot(self):
        self.requireYaml()
        c = self.cond("delivery_recommendations")
        self.assertTrue(has("REPETITION DIMENSION", c))
        self.assertTrue(has("N >= 3", c), "the threshold must be stated, not left to taste")
        self.assertTrue(has("NAMED SUBSET", c))
        self.assertTrue(has("named FROM the inventory and never invented", c))
        self.assertTrue(has("Absent a repetition dimension, no pilot is manufactured", c),
                        "a pilot must not be recommended where nothing repeats")

    # -- F09: planning intervals, never quantiles -------------------------------------
    def test_the_estimate_emits_intervals_not_quantiles(self):
        self.requireYaml()
        t = self.est()
        voc = t.field_text("interval_vocabulary")
        self.assertTrue(voc, "the interval vocabulary must be declared, not implied")
        self.assertTrue(has("PLANNING INTERVAL", voc))
        self.assertTrue(has("carries NO distribution", voc),
                        "the reason the quantile is barred must be stated")
        self.assertTrue(has("A factor with no section that states it is NOT applied", voc),
                        "an unsourced multiplier must be barred")
        self.assertTrue(has("PLANNING INTERVALS (min-max)", t.field_text("permitted_outputs")))
        self.assertTrue(has("claiming a quantile", t.field_text("forbidden_transformations")))

    def test_no_quantile_reads_as_an_instruction_anywhere_in_the_estimate(self):
        for token in ("P50", "P80"):
            self.assertTrue(only_in_prohibition(token, self.est().raw),
                            "%s may appear only inside a prohibition" % token)

    def test_simulate_stopped_claiming_quantiles_and_the_unsourced_factor(self):
        sim = read(os.path.join(SKILLS, "aisa-simulate", "SKILL.md"))
        self.assertTrue(has("planning interval", sim),
                        "simulate must emit a planning interval")
        for token in ("P50", "P80"):
            self.assertTrue(only_in_prohibition(token, sim),
                            "%s may appear in simulate only inside a prohibition" % token)
        self.assertNotIn("×1.4", sim,
                         "the unsourced SAP multiplier example must be gone")
        self.assertTrue(has("cited to the section of `craft/estimation-model.md` that states it", sim),
                        "every factor must be cited to the section that states it")

    # -- the body says it too ---------------------------------------------------------
    def test_the_phases_prose_carries_the_rule(self):
        head = self.est().body.split("## 6.")[0].split("## 5.")[-1]
        self.assertTrue(has("perfil responsável", head))
        self.assertTrue(has("≥ 5 pessoa-dias", head))
        self.assertTrue(has("soma(min) ≤ figura da fase ≤ soma(max)", head),
                        "§5 prose must carry the containment inequality")
        self.assertTrue(has("redistribui, não acrescenta", head))

    def test_the_team_prose_carries_the_occupancy_and_refuses_the_calendar(self):
        head = self.est().body.split("## 17.")[0].split("## 16.")[-1]
        self.assertTrue(has("pessoa-dias ÷ dedicação → semanas mínimas", head))
        self.assertTrue(has("Sem grelha, sem Gantt, sem data de calendário", head))
        self.assertTrue(has("restrição ao paralelismo", head))
        self.assertIn("{{profile_load}}", head,
                      "profile_load must render inside the team section")

    def test_the_recommendations_prose_carries_the_repetition_rule(self):
        head = self.est().body.split("## 19.")[-1]
        self.assertTrue(has("N ≥ 3 instâncias", head))
        self.assertTrue(has("subconjunto nomeado", head))
        self.assertTrue(has("não se fabrica piloto nenhum", head))


if __name__ == "__main__":
    unittest.main(verbosity=2)
