"""Step 7 — final PP pack integrity / consistency gate.

CROSS-LAYER structural integrity only. Each frozen layer already owns its own suite
(Step 3 options, Step 4 domain knowledge, Step 5 architecture, Step 6 deliverables);
this module proves the layers form ONE coherent chain of authority and that no layer
regressed, no manifest target dangles, no retired model is still reachable, and no
downstream artefact acquired an authority it does not own.

P-1  manifest targets resolve            P-10 headless has no mandatory surface
P-2  no active retired architecture      P-11 build-gating condition guard
P-3  15 RESEARCH + 10 CRAFT              P-12 Estimate->Executive payload guard
P-4  5 architecture runtime units        P-13 Estimate modes == 2
P-5  6 deliverable contracts             P-14 no active runtime price facts
P-6  no architecture-auth bypass         P-15 no broken active runtime references
P-7  exactly 2 deliverable read edges    P-16 no semantic authority cycles
P-8  no Domain Knowledge preload         P-17 scope-pair representation possible
P-9  CRAFT is non-authoritative          P-18 no deliverable owns epistemic state

    python .claude/tests/test_pp_pack_integrity.py
"""

import os
import re
import unittest

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PACK_DIR = os.path.join(ROOT, "library", "packs", "pp")
KERNEL_DIR = os.path.join(ROOT, "library", "kernel")
CLAUDE_DIR = os.path.join(ROOT, ".claude")
DK_DIR = os.path.join(PACK_DIR, "domain-knowledge")
ARCH_DIR = os.path.join(PACK_DIR, "architecture-templates")
DELIV_DIR = os.path.join(PACK_DIR, "deliverable-templates")

# `docs/pp-pack-authoring/` is HISTORICAL authoring evidence, never active runtime:
# it truthfully documents superseded models and is excluded from every sweep below.
ACTIVE_ROOTS = [CLAUDE_DIR, KERNEL_DIR, PACK_DIR, os.path.join(ROOT, "docs")]
EXCLUDED = ("__pycache__", os.path.join("docs", "pp-pack-authoring"))
TEXT_EXT = (".md", ".py", ".yaml", ".yml", ".json")


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _active_files(exts=TEXT_EXT):
    out = []
    for root in ACTIVE_ROOTS:
        for dirpath, _dirnames, filenames in os.walk(root):
            if any(x in dirpath for x in EXCLUDED):
                continue
            for name in filenames:
                if name.endswith(exts):
                    out.append(os.path.join(dirpath, name))
    return sorted(out)


def _rel(path):
    return os.path.relpath(path, ROOT).replace("\\", "/")


PACK = yaml.safe_load(_read(os.path.join(PACK_DIR, "pack.yaml")))

RESEARCH_UNITS = [p for p in PACK["domain_knowledge"]
                  if p != "domain-knowledge/README.md" and "/craft/" not in p]
CRAFT_UNITS = [p for p in PACK["domain_knowledge"] if "/craft/" in p]

ARCH_RUNTIME_UNITS = [
    "architecture-core.md",
    "fragment-experience-internal.md",
    "fragment-experience-external.md",
    "fragment-experience-inherited.md",
    "fragment-boundary-and-imports.md",
]

CANONICAL_DELIVERABLES = {
    "discovery-report",
    "executive-report",
    "architecture-blueprint",
    "implementation-specification",
    "claude-design-brief",
    "estimate",
}


def _frontmatter(path):
    body = _read(path)
    if not body.startswith("---"):
        raise AssertionError("%s has no frontmatter" % _rel(path))
    return yaml.safe_load(body.split("---", 2)[1])


DELIVERABLE_FM = {
    name: _frontmatter(os.path.join(DELIV_DIR, name))
    for name in sorted(os.listdir(DELIV_DIR)) if name.endswith(".template.md")
}


# --------------------------------------------------------- P-1 manifest integrity

class P01ManifestTargetsResolve(unittest.TestCase):
    """Every manifest target exists; no duplicate path; no retired target."""

    def _targets(self):
        t = [(d["id"], d["template"]) for d in PACK["deliverables"]]
        t += [("domain_knowledge", p) for p in PACK["domain_knowledge"]]
        t.append(("question_bank", PACK["question_bank"]))
        t.append(("glossary", PACK["glossary"]))
        t.append(("decision_tree", PACK["decision_tree"]["source"]))
        t += [("decision_model:" + k, v["source"])
              for k, v in PACK["decision_model"].items()]
        return t

    def test_every_target_exists(self):
        for key, rel in self._targets():
            self.assertTrue(os.path.isfile(os.path.join(PACK_DIR, rel)),
                            "manifest target %s -> %s does not exist" % (key, rel))

    def test_no_duplicate_manifest_path(self):
        paths = [rel for _k, rel in self._targets()]
        self.assertEqual(len(paths), len(set(paths)), "duplicate manifest path")

    def test_manifest_declares_no_routing_key(self):
        """No outcome->template, product->template or dynamic branch mapping.

        Checked on the PARSED manifest: the file's prose legitimately NAMES
        `applies_to` to record that it was replaced by `activation`.
        """
        for d in PACK["deliverables"]:
            self.assertNotIn("applies_to", d,
                             "%s reinstated the applies_to discriminator" % d["id"])
            for key in ("outcome", "outcomes", "product", "products", "branch",
                        "load_order", "state_machine", "route", "routes"):
                self.assertNotIn(key, d, "%s declares routing key %r" % (d["id"], key))
        for key in ("architecture_templates", "outcome_map", "product_map",
                    "load_order", "state_machine"):
            self.assertNotIn(key, PACK, "manifest declares routing key %r" % key)

    def test_no_dynamic_template_slot(self):
        """No template path is resolved from a runtime value."""
        for d in PACK["deliverables"]:
            self.assertNotRegex(d["template"], r"[{}<>*]",
                                "%s has a dynamic template path" % d["id"])
        raw = _read(os.path.join(PACK_DIR, "pack.yaml"))
        self.assertNotIn("{{chosen_architecture}}", raw)
        self.assertNotIn("architecture-templates/<", raw)

    def test_pack_version_recorded(self):
        self.assertRegex(str(PACK["pack_version"]), r"^\d+\.\d+\.\d+$")


# ------------------------------------------ P-2 no active retired architecture model

RETIRED_ARCH_TOKENS = [
    "sharepoint-first",
    "dataverse-first",
    "chosen_architecture",
    "{{chosen_architecture}}",
    "architecture-templates/<branch>",
    "architecture-templates/<chosen>",
    "Branch (if technology)",
    "Branch (decision-tree)",
]

# Files that legitimately carry a retired token: the guard suites that assert its
# ABSENCE, and the runtime README section that documents the retirement + the
# read-compatibility mapping (`architecture-templates/README.md` §11).
RETIRED_TOKEN_ALLOWED = {
    ".claude/tests/test_pp_pack_integrity.py",
    ".claude/tests/test_pp_architecture_templates.py",
    ".claude/tests/test_pp_deliverable_templates.py",
    ".claude/tests/test_pp_domain_knowledge.py",
    "library/packs/pp/architecture-templates/README.md",
    # Names the field only to record that it was REMOVED from the decision
    # serialization; the negation itself is asserted below.
    ".claude/skills/aisa-decide/SKILL.md",
}


class P02NoActiveRetiredArchitecture(unittest.TestCase):
    """No consumer derives architecture through the retired store-first branch model."""

    def test_no_retired_token_in_the_active_runtime(self):
        """No active runtime file carries retired architecture vocabulary.

        Scope: the pack, the kernel, the skills, the commands, the hooks, the agent
        definitions AND standing agent memory — standing memory is runtime. The only
        exemptions are the guard suites that assert absence and the architecture
        README section that documents the retirement itself.
        """
        for path in _active_files():
            rel = _rel(path)
            if rel in RETIRED_TOKEN_ALLOWED or rel.startswith("docs/"):
                continue
            body = _read(path)
            for token in RETIRED_ARCH_TOKENS:
                self.assertNotIn(token, body,
                                 "%s carries retired architecture token %r" % (rel, token))

    def test_retired_template_files_absent(self):
        for name in ("sharepoint-first.md", "dataverse-first.md", "hybrid.md"):
            self.assertFalse(os.path.exists(os.path.join(ARCH_DIR, name)),
                             "retired architecture template %s is back" % name)

    def test_readme_frames_them_as_retired(self):
        body = _read(os.path.join(ARCH_DIR, "README.md"))
        self.assertIn("retired", body.lower())

    def test_decide_names_the_field_only_to_remove_it(self):
        body = _read(os.path.join(CLAUDE_DIR, "skills", "aisa-decide", "SKILL.md"))
        flat = " ".join(body.split())
        self.assertIn("The obsolete `Branch (if technology)` field is **removed**", flat)
        self.assertNotIn("- **Branch (if technology)**:", body,
                         "aisa-decide re-emits the retired field")

    def test_no_agent_definition_owns_an_artefact_schema(self):
        """R-1 - one artefact, one serialization authority.

        `.claude/agents/chairman.md` previously carried a SECOND, pre-Step-3 copy of
        the `options.md` spec (including `Branch (if technology)`). It must now carry
        a POINTER to the canonical contract and own no artefact schema of its own.
        """
        agent = _read(os.path.join(CLAUDE_DIR, "agents", "chairman.md"))
        self.assertNotIn("Branch (if technology)", agent)
        self.assertIn(".claude/skills/chairman-synthesis/SKILL.md", agent,
                      "chairman.md must point at the canonical serialization authority")
        self.assertIn("does not maintain a second copy", agent)
        self.assertIn("one serialization authority", agent)

        # No local field schema: these were the pre-Step-3 Options field lines.
        for field in ("- **Pros**", "- **Cons**", "- **Reversibility**",
                      "- **Indicative effort band**", "- **Constraints checked**"):
            self.assertNotIn(
                field, agent,
                "chairman.md still owns an Options field schema (%r)" % field)

        # No other agent definition carries retired vocabulary either.
        agents_dir = os.path.join(CLAUDE_DIR, "agents")
        for name in sorted(os.listdir(agents_dir)):
            if not name.endswith(".md"):
                continue
            body = _read(os.path.join(agents_dir, name))
            for token in RETIRED_ARCH_TOKENS:
                self.assertNotIn(token, body,
                                 "agent %s carries retired token %r" % (name, token))

    def test_exactly_one_options_serialization_authority(self):
        """The skill-side options.md spec is the sole authority, Step-3 aligned."""
        skill = _read(os.path.join(CLAUDE_DIR, "skills", "chairman-synthesis",
                                   "SKILL.md"))
        for token in RETIRED_ARCH_TOKENS:
            self.assertNotIn(token, skill,
                             "chairman-synthesis carries retired token %r" % token)
        for required in ("## Concern coverage", "**Outcome**", "**Viability**",
                         "## Comparator status", "scope:", "**Disqualifiers**",
                         "**Preconditions**", "**Proof requirement**"):
            self.assertIn(required, skill,
                          "chairman-synthesis options spec lost %r" % required)

        # Count the files defining the options.md artefact shape. Exactly one.
        definers = []
        for path in _active_files((".md",)):
            rel = _rel(path)
            if rel.startswith("docs/") or rel.startswith(".claude/tests/"):
                continue
            body = _read(path)
            if "# Options " in body and "/ Round O-<NN>" in body:
                definers.append(rel)
        self.assertEqual(
            definers, [".claude/skills/chairman-synthesis/SKILL.md"],
            "duplicate Options serialization authorities: %s" % definers)

    def test_standing_agent_memory_is_free_of_retired_semantics(self):
        """R-2 / R-3 - standing memory is runtime; prefer absence, not prohibition."""
        retired = re.compile(
            r"sharepoint-first|dataverse-first|branch shortlisting"
            r"|architectural branch|branch winner|branch loser|\bR[0-6]\b"
            r"|pass ?/ ?risky ?/ ?blocker")
        offenders = []
        mem = os.path.join(CLAUDE_DIR, "agent-memory")
        for dirpath, _dn, filenames in os.walk(mem):
            for name in filenames:
                if not name.endswith(".md"):
                    continue
                path = os.path.join(dirpath, name)
                body = _read(path)
                if retired.search(body) or any(t in body for t in RETIRED_ARCH_TOKENS):
                    offenders.append(_rel(path))
        self.assertEqual(sorted(offenders), [],
                         "retired semantics in standing agent memory")

    def test_solution_architect_memory_uses_the_current_model(self):
        """The valid lessons survived, re-expressed against the frozen model."""
        body = _read(os.path.join(
            CLAUDE_DIR, "agent-memory", "_universal", "solution-architect",
            "universal-constraints.md"))
        for anchor in ("**S1**", "**S5**", "**S9**",
                       "settled hard disqualifier",
                       "never settles a hard exclusion",
                       "standing-attention floor"):
            self.assertIn(anchor, body,
                          "solution-architect memory lost the anchor %r" % anchor)
        self.assertIn("decision-tree.md", body,
                      "memory must point at the decision-status vocabulary owner")

class P03DomainKnowledgeTaxonomy(unittest.TestCase):

    def test_fifteen_research_units(self):
        self.assertEqual(len(RESEARCH_UNITS), 15, RESEARCH_UNITS)

    def test_ten_craft_units(self):
        self.assertEqual(len(CRAFT_UNITS), 10, CRAFT_UNITS)

    def test_one_readme(self):
        self.assertIn("domain-knowledge/README.md", PACK["domain_knowledge"])

    def test_filesystem_matches_manifest(self):
        on_disk = set()
        for dirpath, _dn, filenames in os.walk(DK_DIR):
            for name in filenames:
                if name.endswith(".md"):
                    rel = os.path.relpath(os.path.join(dirpath, name), PACK_DIR)
                    on_disk.add(rel.replace("\\", "/"))
        self.assertEqual(on_disk, set(PACK["domain_knowledge"]),
                         "domain-knowledge filesystem and manifest disagree")

    def test_no_resurrected_flat_legacy_unit(self):
        for legacy in ("azure-sql-first.md", "delegation-matrix.md", "excel-patterns.md",
                       "flows-patterns.md", "powerfx-patterns.md", "security-patterns.md",
                       "sharepoint-reference.md", "dataverse-reference.md",
                       "azure-sql-reference.md", "anti-patterns.md", "alternatives.md"):
            self.assertFalse(os.path.exists(os.path.join(DK_DIR, legacy)),
                             "legacy domain-knowledge file %s is back" % legacy)


# --------------------------------------------------- P-4 architecture runtime units

class P04ArchitectureRuntimeUnits(unittest.TestCase):

    def test_exactly_five_runtime_units(self):
        present = sorted(n for n in os.listdir(ARCH_DIR)
                         if n.endswith(".md") and n != "README.md")
        self.assertEqual(present, sorted(ARCH_RUNTIME_UNITS), present)

    def test_readme_is_positioning_not_a_runtime_unit(self):
        self.assertTrue(os.path.isfile(os.path.join(ARCH_DIR, "README.md")))

    def test_no_headless_fragment(self):
        self.assertFalse(
            os.path.exists(os.path.join(ARCH_DIR, "fragment-experience-none.md")),
            "experience.mode none must resolve ZERO fragments")

    def test_no_product_or_pattern_specific_template(self):
        for name in os.listdir(ARCH_DIR):
            self.assertNotRegex(
                name,
                r"(canvas|model-driven|dataverse|sharepoint|sql|api-facade|event-driven)",
                "product/pattern-specific architecture template %s" % name)


# ---------------------------------------------------- P-5 six deliverable contracts

class P05DeliverableContracts(unittest.TestCase):

    def test_six_manifest_deliverables(self):
        self.assertEqual(len(PACK["deliverables"]), 6)

    def test_six_templates_on_disk(self):
        self.assertEqual(len(DELIVERABLE_FM), 6, sorted(DELIVERABLE_FM))

    def test_canonical_names_are_the_six(self):
        names = {d["canonical_deliverable"] for d in PACK["deliverables"]}
        self.assertEqual(names, CANONICAL_DELIVERABLES)

    def test_no_duplicate_canonical_deliverable(self):
        names = [d["canonical_deliverable"] for d in PACK["deliverables"]]
        self.assertEqual(len(names), len(set(names)))

    def test_template_and_manifest_agree(self):
        for d in PACK["deliverables"]:
            fm = DELIVERABLE_FM[os.path.basename(d["template"])]
            self.assertEqual(fm["canonical_deliverable"], d["canonical_deliverable"])

    def test_every_contract_declares_its_source_edges(self):
        for name, fm in DELIVERABLE_FM.items():
            for key in ("authority_sources", "forbidden_sources"):
                self.assertIn(key, fm, "%s has no %s" % (name, key))
                self.assertTrue(fm[key], "%s has empty %s" % (name, key))


# ------------------------------------- P-6 no architecture-authorization bypass

class P06NoArchitectureAuthorizationBypass(unittest.TestCase):
    """architecture authorization = outcome reachability x active-pack architectability."""

    def test_readme_is_the_single_home_of_the_binding_rule(self):
        body = _read(os.path.join(ARCH_DIR, "README.md"))
        self.assertIn(
            "architecture authorization = outcome reachability "
            "× active-pack architectability", body)

    def test_blueprint_runs_both_factors(self):
        body = _read(os.path.join(CLAUDE_DIR, "skills", "aisa-blueprint", "SKILL.md"))
        self.assertIn("outcome reachability", body)
        self.assertIn("architectability", body)
        self.assertIn("Reachability alone is **never sufficient**", body)

    def test_decide_may_not_emit_authorization(self):
        body = _read(os.path.join(CLAUDE_DIR, "skills", "aisa-decide", "SKILL.md"))
        self.assertIn("architecture.authorization", body)
        self.assertIn("Must NEVER emit", body)

    def test_render_discriminator_is_authorization_not_outcome_polarity(self):
        body = _read(os.path.join(KERNEL_DIR, "render-contract.md"))
        self.assertIn(
            "does an architecture authorization exist for at least one scope?", body)
        self.assertIn(
            "A positive outcome over a solution the active pack cannot architect "
            "authorizes no architecture", body)

    def test_authorization_is_read_never_derived(self):
        for path in (os.path.join(ARCH_DIR, "README.md"),
                     os.path.join(CLAUDE_DIR, "skills", "aisa-synthesize", "SKILL.md")):
            body = _read(path)
            self.assertRegex(
                body, r"read, never derived|never derived, upgraded or downgraded",
                "%s lost the read-never-derive rule" % _rel(path))


# ------------------------------------------- P-7 exactly two deliverable read edges

class P07DeliverableReadEdges(unittest.TestCase):
    """Spec -> Estimate (inventory) and Estimate -> Executive (headline). No third."""

    def _authority_blob(self, name):
        fm = DELIVERABLE_FM[name]
        parts = []
        for key in ("authority_sources", "conditional_sources"):
            v = fm.get(key) or []
            parts.extend(str(x) for x in (v if isinstance(v, list) else [v]))
        return "\n".join(parts)

    def test_estimate_reads_the_specification_inventory(self):
        blob = self._authority_blob("estimate.template.md")
        self.assertIn("Implementation Specification's inventory", blob)

    def test_executive_reads_only_the_estimate_headline(self):
        blob = self._authority_blob("executive-report.template.md")
        self.assertIn("the Estimate's headline", blob)

    def test_no_other_deliverable_reads_a_rendered_deliverable(self):
        allowed = {"estimate.template.md", "executive-report.template.md"}
        for name in DELIVERABLE_FM:
            if name in allowed:
                continue
            blob = self._authority_blob(name)
            self.assertNotIn("_render/", blob,
                             "%s reads a rendered deliverable as authority" % name)

    def test_the_two_edges_are_declared_bounded(self):
        contract = _read(os.path.join(KERNEL_DIR, "render-contract.md"))
        self.assertIn("implementation-spec → estimate", contract)
        self.assertIn("inventory only", contract)
        self.assertIn("acyclic", contract)

    def test_reverse_edges_are_forbidden(self):
        spec = str(DELIVERABLE_FM["implementation-spec.template.md"]["forbidden_sources"])
        self.assertIn("_render/<slug>_estimate", spec)
        brief = str(DELIVERABLE_FM["claude-design-brief.template.md"]["forbidden_sources"])
        self.assertIn("_render/<slug>_solution-blueprint", brief)
        self.assertIn("_render/<slug>_implementation-spec", brief)


# ------------------------------------------------ P-8 no Domain Knowledge preload

class P08NoDomainKnowledgePreload(unittest.TestCase):

    PULL_CONSUMERS = [
        ("skills", "aisa-blueprint", "SKILL.md"),
        ("skills", "aisa-render", "SKILL.md"),
        ("skills", "aisa-synthesize", "SKILL.md"),
        ("skills", "lens-technology", "SKILL.md"),
    ]

    def test_manifest_declares_a_manifest_not_a_load_order(self):
        raw = _read(os.path.join(PACK_DIR, "pack.yaml"))
        self.assertIn("NOT a load order", raw)
        self.assertIn("PULL-BASED", raw)

    def test_readme_carries_the_pull_rule(self):
        body = _read(os.path.join(DK_DIR, "README.md"))
        self.assertIn("Never preloaded.", body)
        self.assertIn("pull ONE relevant knowledge unit", body)

    def test_every_research_unit_declares_never_preloaded(self):
        for rel in RESEARCH_UNITS + ["domain-knowledge/README.md"]:
            body = _read(os.path.join(PACK_DIR, rel))
            self.assertIn("Never preloaded", body, "%s lost its pull declaration" % rel)

    def test_every_craft_unit_declares_its_pull_boundary(self):
        for rel in CRAFT_UNITS:
            body = _read(os.path.join(PACK_DIR, rel))
            self.assertIn("Not an Options D3 pull target", body,
                          "%s lost its pull declaration" % rel)

    def test_consumers_forbid_preload(self):
        for parts in self.PULL_CONSUMERS:
            path = os.path.join(CLAUDE_DIR, *parts)
            body = _read(path)
            self.assertRegex(
                body, r"[Nn]ever preload|Never preloaded|never a preload|do not preload",
                "%s lost its no-preload rule" % _rel(path))

    def test_solution_architect_never_loads_the_base_by_default(self):
        body = _read(os.path.join(CLAUDE_DIR, "agents", "solution-architect.md"))
        self.assertIn("Never load the domain-knowledge base by default", body)

    def test_no_concern_to_unit_matrix(self):
        flat = " ".join(
            _read(os.path.join(PACK_DIR, "pack.yaml")).replace("#", " ").split())
        self.assertIn("NOT a concern map", flat)
        self.assertIn("NOT a routing table", flat)


# ----------------------------------------------- P-9 CRAFT is non-authoritative

class P09CraftNonAuthoritative(unittest.TestCase):

    def test_every_craft_unit_disclaims_research_authority(self):
        for rel in CRAFT_UNITS:
            body = _read(os.path.join(PACK_DIR, rel))
            self.assertIn("class: CRAFT", body, "%s lost its class marker" % rel)
            self.assertRegex(
                body,
                r"No independent research authority"
                r"|Sem autoridade própria de investigação",
                "%s lost its non-authority declaration" % rel)

    def test_craft_may_not_state_a_platform_limit(self):
        for rel in CRAFT_UNITS:
            flat = " ".join(_read(os.path.join(PACK_DIR, rel)).split())
            self.assertRegex(
                flat,
                r"must not state a platform limit"
                r"|não pode afirmar como facto um limite de plataforma",
                "%s lost its no-platform-limit rule" % rel)

    def test_craft_is_never_an_options_pull_target(self):
        for rel in CRAFT_UNITS:
            body = _read(os.path.join(PACK_DIR, rel))
            self.assertIn("Not an Options D3 pull target", body, rel)
        readme = _read(os.path.join(DK_DIR, "README.md"))
        self.assertIn("never a D3 Options pull target", readme)

    def test_manifest_records_the_craft_boundary(self):
        flat = " ".join(
            _read(os.path.join(PACK_DIR, "pack.yaml")).replace("#", " ").split())
        self.assertIn("Never an Options D3 pull target", flat)
        self.assertIn("no platform limit of their own", flat)

    def test_architecture_does_not_take_craft_as_technical_authority(self):
        body = _read(os.path.join(CLAUDE_DIR, "skills", "aisa-blueprint", "SKILL.md"))
        self.assertIn("the `craft/` files never restate it", body)


# ------------------------------------------------------------ P-10 headless survives

class P10Headless(unittest.TestCase):

    def test_none_is_a_first_class_mode(self):
        for path in (os.path.join(CLAUDE_DIR, "skills", "aisa-blueprint", "SKILL.md"),
                     os.path.join(ARCH_DIR, "README.md")):
            body = _read(path)
            self.assertIn("mode: none", body, _rel(path))

    def test_zero_experience_fragments_and_no_gap(self):
        body = _read(os.path.join(ARCH_DIR, "architecture-core.md"))
        self.assertIn("architecture.experience.mode == none", body)
        self.assertIn("ZERO includes", body)
        self.assertIn("Do NOT attempt to resolve", body)

    def test_design_brief_is_not_applicable_not_blocked(self):
        fm = DELIVERABLE_FM["claude-design-brief.template.md"]
        self.assertIn("experience.mode == none", fm["not_applicable_when"])

    def test_specification_never_invents_a_surface(self):
        fm = DELIVERABLE_FM["implementation-spec.template.md"]
        self.assertIn("inventing a user surface where experience.mode == none",
                      str(fm["forbidden_transformations"]))

    def test_headless_still_carries_the_non_ux_architecture(self):
        body = _read(os.path.join(ARCH_DIR, "README.md"))
        self.assertIn("A headless architecture still carries", body)

    def test_no_other_deliverable_excludes_headless(self):
        for name in ("solution-blueprint.template.md", "implementation-spec.template.md",
                     "discovery-report.template.md", "executive-report.template.md",
                     "estimate.template.md"):
            fm = DELIVERABLE_FM[name]
            self.assertNotIn("experience.mode == none",
                             str(fm.get("not_applicable_when", "")),
                             "%s wrongly excludes headless" % name)


# ------------------------------------------------------ P-11 build-gating guard (F-1)

class P11BuildGateGuard(unittest.TestCase):

    SPEC = "implementation-spec.template.md"

    def test_build_gates_are_non_omissible(self):
        body = _read(os.path.join(DELIV_DIR, self.SPEC))
        self.assertIn("non_omissible:", body)
        self.assertIn("BUILD GATES", body)

    def test_conditions_are_not_open_work_items(self):
        body = _read(os.path.join(DELIV_DIR, self.SPEC))
        self.assertIn(
            "A condition with an owner, a funding state and a due date is NOT an "
            "open work item", body)
        self.assertIn("THREE DISTINCT THINGS", body)

    def test_dropping_or_relabelling_a_gate_is_forbidden(self):
        fm = DELIVERABLE_FM[self.SPEC]
        blob = str(fm["forbidden_transformations"])
        self.assertIn(
            "dropping, compressing away or re-labelling a build-gating condition", blob)

    def test_projection_may_never_mark_a_gate_satisfied(self):
        blob = str(DELIVERABLE_FM[self.SPEC]["forbidden_transformations"])
        self.assertIn(
            "rendering a build gate as satisfied without recorded engagement evidence",
            blob)
        self.assertIn("marking a proof obligation satisfied", blob)

    def test_preconditions_and_proof_obligations_carried_in_full(self):
        body = _read(os.path.join(DELIV_DIR, self.SPEC))
        self.assertIn("preconditions", body)
        self.assertIn("proof obligation", body)
        self.assertIn("open work item", body.lower())

    def test_proof_level_may_not_be_regraded(self):
        blob = str(DELIVERABLE_FM[self.SPEC]["forbidden_transformations"])
        self.assertIn("re-grading a proof obligation (V1–V4)", blob)


# --------------------------------------- P-12 Estimate -> Executive payload (F-2)

class P12EstimateToExecutivePayloadGuard(unittest.TestCase):

    EXEC = "executive-report.template.md"

    def test_allowed_payload_is_the_four_bounded_fields(self):
        body = _read(os.path.join(DELIV_DIR, self.EXEC))
        for allowed in ("base effort", "range", "contingency_inclusive_total",
                        "confidence"):
            self.assertIn(allowed, body,
                          "executive lost allowed payload field %r" % allowed)

    def test_forbidden_payload_is_named(self):
        body = _read(os.path.join(DELIV_DIR, self.EXEC))
        for forbidden in ("phases", "work breakdown", "team mix",
                          "contingency_rate_or_derivation",
                          "duration_or_calendar_schedule"):
            self.assertIn(forbidden, body,
                          "executive lost the %r prohibition" % forbidden)

    def test_executive_is_not_a_second_effort_authority(self):
        contract = _read(os.path.join(KERNEL_DIR, "render-contract.md"))
        self.assertIn("The Executive Report never becomes a second Estimate authority",
                      contract)

    def test_candidates_are_never_blended_into_one_headline(self):
        blob = str(DELIVERABLE_FM[self.EXEC]["forbidden_transformations"])
        self.assertIn("blending candidate planning estimates into one headline figure",
                      blob)

    def test_estimate_owns_the_calculation_and_nothing_else_does(self):
        est = [d for d in PACK["deliverables"] if d["id"] == "estimate"][0]
        self.assertTrue(est["owns_calculation"])
        for d in PACK["deliverables"]:
            if d["id"] != "estimate":
                self.assertNotIn("owns_calculation", d,
                                 "%s claims calculation ownership" % d["id"])


# --------------------------------------------------- P-13 exactly two Estimate modes

class P13EstimateModes(unittest.TestCase):

    def setUp(self):
        self.fm = DELIVERABLE_FM["estimate.template.md"]

    def test_exactly_two_input_modes(self):
        self.assertEqual(sorted(self.fm["input_modes"]), ["A", "B"])

    def test_mode_a_is_the_specification_inventory(self):
        a = self.fm["input_modes"]["A"]
        self.assertIn("Implementation Specification", str(a["inputs"]))
        self.assertIn("MAY NOT ADD A WORK UNIT ABSENT FROM THAT", a["scope_control"])

    def test_mode_b_may_not_invent_a_specification(self):
        b = self.fm["input_modes"]["B"]
        self.assertIn("no spec != permission to invent a spec", b["scope_control"])
        self.assertIn("NEVER blend candidates into one figure", b["isolation"])
        self.assertIn("NEVER select a candidate", b["isolation"])

    def test_synthesis_calculates_no_implementation_effort(self):
        body = _read(os.path.join(KERNEL_DIR, "synthesis-templates",
                                  "financial-story.template.md"))
        self.assertIn("NO effort figure", body)

    def test_render_executes_and_never_invents_work(self):
        contract = _read(os.path.join(KERNEL_DIR, "render-contract.md"))
        self.assertIn("invent work", contract)


# ---------------------------------------------------- P-14 no active runtime prices

# A MONETARY AMOUNT is what §46 forbids in the runtime. The words "price", "SKU" and
# "rate card" DO appear in the pack — exclusively inside `forbidden_sources` /
# `forbidden_transformations` lists, where they are the thing being banned. So the
# token to match is not the vocabulary but an actual sum of money; the vocabulary is
# checked separately, by asserting it never appears on a SOURCE edge.
MONEY_RE = re.compile(
    r"(?:[€$£]\s?\d[\d.,]*"
    r"|\d[\d.,]*\s?(?:€|\$|£|USD|EUR|GBP)\b"
    r"|\d[\d.,]*\s?(?:€|\$|USD|EUR)\s?/\s?(?:user|utilizador|month|m[eê]s))")


def _money_offenders(root):
    offenders = []
    for dirpath, _dn, filenames in os.walk(root):
        if "__pycache__" in dirpath:
            continue
        for name in filenames:
            if not name.endswith((".md", ".yaml")):
                continue
            path = os.path.join(dirpath, name)
            for i, line in enumerate(_read(path).split("\n"), 1):
                if MONEY_RE.search(line):
                    offenders.append("%s:%d %s" % (_rel(path), i, line.strip()[:110]))
    return offenders


class P14NoActiveRuntimePrices(unittest.TestCase):

    def test_no_monetary_amount_in_the_pack(self):
        self.assertEqual(_money_offenders(PACK_DIR), [],
                         "monetary amount fossilized in the PP runtime")

    def test_no_monetary_amount_in_the_kernel_templates(self):
        self.assertEqual(_money_offenders(KERNEL_DIR), [],
                         "monetary amount fossilized in a kernel contract or template")

    def test_price_vocabulary_appears_only_as_a_prohibition(self):
        """`licence price` / `SKU price` / `rate card` may never sit on a SOURCE edge."""
        for name, fm in DELIVERABLE_FM.items():
            for key in ("authority_sources", "conditional_sources"):
                blob = str(fm.get(key, "")).lower()
                for token in ("licence price", "license price", "sku price", "rate card"):
                    self.assertNotIn(token, blob,
                                     "%s takes %r as a source" % (name, token))

    def test_volatility_register_supplies_no_figures(self):
        flat = " ".join(_read(os.path.join(
            PACK_DIR, "decision-model", "volatility-register.md")).split())
        self.assertIn("register still supplies no figures", flat)

    def test_estimate_forbids_price_emission(self):
        blob = str(DELIVERABLE_FM["estimate.template.md"]["forbidden_transformations"])
        self.assertIn("emitting any price, SKU, rate card or quota-derived cost", blob)


# ------------------------------------- P-15 no broken active runtime references

PATH_RE = re.compile(
    r"(?<![\w/.-])((?:library|\.claude)/[A-Za-z0-9_./<>{}*+-]+"
    r"\.(?:md|py|yaml|yml|json|html))")


class P15NoBrokenActiveReferences(unittest.TestCase):
    """Every concrete library/ or .claude/ path named by the runtime resolves."""

    def test_all_runtime_paths_resolve(self):
        broken = []
        for path in _active_files():
            rel = _rel(path)
            if rel.startswith("docs/"):
                continue          # docs carry historical planning references
            for match in PATH_RE.finditer(_read(path)):
                target = match.group(1)
                if any(ch in target for ch in "<>{}*"):
                    continue      # templated slot, resolved at runtime
                if not os.path.exists(os.path.join(ROOT, target)):
                    broken.append("%s -> %s" % (rel, target))
        self.assertEqual(sorted(set(broken)), [], "broken active runtime reference")

    def test_path_case_is_consistent(self):
        """No conceptual file referenced under two different casings."""
        seen = {}
        for path in _active_files():
            for match in PATH_RE.finditer(_read(path)):
                target = match.group(1)
                if any(ch in target for ch in "<>{}*"):
                    continue
                seen.setdefault(target.lower(), set()).add(target)
        clashes = {k: sorted(v) for k, v in seen.items() if len(v) > 1}
        self.assertEqual(clashes, {},
                         "same path referenced under inconsistent casing")


# ---------------------------------------------------- P-16 no semantic authority cycles

# The active semantic-authority graph: consumer -> the authorities it may read.
# Edges are taken from the declared source contracts, not inferred.
AUTHORITY_EDGES = {
    "shared-understanding": [],
    "options": ["shared-understanding"],
    "decision": ["options", "shared-understanding"],
    "architecture": ["decision", "shared-understanding"],
    "synthesis": ["decision", "architecture", "shared-understanding"],
    "ux-blueprint": ["architecture", "shared-understanding", "decision"],
    "discovery-report": ["shared-understanding", "synthesis"],
    "architecture-blueprint": ["architecture", "synthesis", "decision",
                               "shared-understanding"],
    "implementation-specification": ["architecture", "decision", "synthesis"],
    "claude-design-brief": ["ux-blueprint", "decision"],
    "estimate": ["implementation-specification", "architecture", "decision", "synthesis"],
    "executive-report": ["decision", "synthesis", "architecture", "estimate",
                         "shared-understanding"],
}


class P16NoAuthorityCycles(unittest.TestCase):

    def test_graph_is_acyclic(self):
        colour = {}

        def visit(node, stack):
            if colour.get(node) == "done":
                return
            if colour.get(node) == "open":
                raise AssertionError("authority cycle: %s" % " -> ".join(stack + [node]))
            colour[node] = "open"
            for nxt in AUTHORITY_EDGES.get(node, []):
                visit(nxt, stack + [node])
            colour[node] = "done"

        for node in AUTHORITY_EDGES:
            visit(node, [])

    def test_no_forbidden_inversion_is_declared(self):
        """The legal direction is downstream only; upstream layers read nothing below."""
        self.assertEqual(AUTHORITY_EDGES["shared-understanding"], [])
        self.assertNotIn("executive-report", AUTHORITY_EDGES["decision"])
        self.assertNotIn("estimate", AUTHORITY_EDGES["implementation-specification"])
        self.assertNotIn("claude-design-brief", AUTHORITY_EDGES["architecture"])
        self.assertNotIn("architecture-blueprint", AUTHORITY_EDGES["options"])

    def test_no_deliverable_takes_options_as_an_authority(self):
        for name, fm in DELIVERABLE_FM.items():
            authority = (str(fm.get("authority_sources", ""))
                         + str(fm.get("conditional_sources", "")))
            self.assertNotIn("options.md", authority,
                             "%s takes options.md as an authority" % name)

    def test_every_deliverable_forbids_options_as_a_source(self):
        for name, fm in DELIVERABLE_FM.items():
            self.assertIn("options.md", str(fm["forbidden_sources"]),
                          "%s does not forbid options.md" % name)

    def test_downstream_open_item_is_not_an_inversion(self):
        spec = _read(os.path.join(DELIV_DIR, "implementation-spec.template.md"))
        self.assertIn("OPEN WORK ITEM", spec)


# ------------------------------------------ P-17 scope-pair representation survives

class P17ScopePairs(unittest.TestCase):

    def test_outcome_classes_render_pairs_and_never_collapse(self):
        body = _read(os.path.join(PACK_DIR, "decision-model", "outcome-classes.md"))
        self.assertIn("One outcome per scope, not one per engagement", body)
        self.assertIn("never collapse them", body)

    def test_decision_tree_carries_the_normative_rule(self):
        body = _read(os.path.join(PACK_DIR, "decision-tree.md"))
        self.assertIn("Scope pairing (normative)", body)

    def test_architecture_carries_relocated_responsibilities(self):
        body = _read(os.path.join(CLAUDE_DIR, "skills", "aisa-blueprint", "SKILL.md"))
        self.assertIn("relocated_responsibilities:", body)
        self.assertIn("the scope-pair mechanism", body)

    def test_far_side_is_never_architectable_here(self):
        body = _read(os.path.join(ARCH_DIR, "README.md"))
        self.assertIn("The far side of a scope pair is never architectable here", body)

    def test_authorized_bounded_is_a_first_class_state(self):
        body = _read(os.path.join(CLAUDE_DIR, "skills", "aisa-render", "SKILL.md"))
        self.assertIn("PP authorized-bounded", body)
        self.assertIn("PP side only", body)

    def test_comparator_markers_survive_downstream(self):
        for name in ("executive-report.template.md", "solution-blueprint.template.md"):
            body = _read(os.path.join(DELIV_DIR, name))
            self.assertIn("UNEVALUATED", body,
                          "%s lost the comparator marker" % name)


# ------------------------------------- P-18 no deliverable owns epistemic state

class P18NoDeliverableOwnsEpistemics(unittest.TestCase):

    def test_su_is_the_declared_source_of_truth(self):
        rule = _read(os.path.join(CLAUDE_DIR, "rules",
                                  "shared-understanding-as-source-of-truth.md"))
        self.assertIn("authoritative current-state document", rule)
        self.assertIn("If SU and another file disagree, SU wins", rule)

    def test_render_may_not_promote_epistemics(self):
        contract = _read(os.path.join(KERNEL_DIR, "render-contract.md"))
        self.assertIn("promote epistemics", contract)

    def test_conflicted_never_becomes_one_value(self):
        spec = _read(os.path.join(DELIV_DIR, "implementation-spec.template.md"))
        self.assertIn("Conflicted: NO value chosen", spec)

    def test_expired_becomes_a_verification_obligation(self):
        spec = _read(os.path.join(DELIV_DIR, "implementation-spec.template.md"))
        self.assertIn("re-verification obligation", spec)
        disc = _read(os.path.join(DELIV_DIR, "discovery-report.template.md"))
        self.assertIn("EXPIRED rows as re-verification obligations", disc)

    def test_discovery_report_projects_all_five_states(self):
        disc = _read(os.path.join(DELIV_DIR, "discovery-report.template.md"))
        self.assertIn("ALL FIVE", disc)
        for state in ("Confirmed", "Assumed", "Unknown", "Conflicted", "Risky"):
            self.assertIn(state, disc)

    def test_no_deliverable_claims_epistemic_promotion(self):
        for name, fm in DELIVERABLE_FM.items():
            blob = str(fm.get("permitted_transformations", ""))
            for verb in ("promote", "upgrade an Assumed", "resolve an Unknown"):
                self.assertNotIn(verb, blob,
                                 "%s claims epistemic promotion (%r)" % (name, verb))

    def test_kernel_states_remain_the_single_epistemic_home(self):
        body = _read(os.path.join(PACK_DIR, "decision-tree.md"))
        self.assertIn("The five kernel states (`library/kernel/states.md`) carry all "
                      "epistemics", body)


if __name__ == "__main__":
    unittest.main(verbosity=2)
