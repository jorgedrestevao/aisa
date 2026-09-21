"""Step 3B1 — PP Options runtime decision model.

Mechanical/structural assertions only. These prove IMPLEMENTATION FIDELITY against the
approved Step 3A design; they do NOT prove decision behaviour — that is the T-01…T-18
semantic replay of Step 3B2.

    python .claude/tests/test_pp_options_decision_model.py
"""

import os
import re
import unittest

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PACK_DIR = os.path.join(ROOT, "library", "packs", "pp")
DM_DIR = os.path.join(PACK_DIR, "decision-model")

DISCOVERY = ["business", "operations", "user", "data", "governance", "financial"]

APPROVED_FLOOR = [
    "deployment_model_and_residency",
    "regulatory_and_control_mandates",
    "service_permissibility_and_egress",
    "entitlement_fit",
    "throughput_and_capacity_envelope",
    "environment_and_release_topology",
    "reversibility_mechanism",
    "operator_and_support_availability",
    "observability_and_evidence_retention",
    "authorization_enforcement_point",
]

RUNTIME_REGISTERS = [
    "alternatives-register.md",
    "blocking-set.md",
    "composed-disqualifiers.md",
    "outcome-classes.md",
    "volatility-register.md",
]

# Registers Step 3A explicitly did NOT create at runtime.
NOT_RUNTIME = [
    "criteria-register.md",
    "exit-classes.md",
    "comparator-rules.md",
    "validation-levels.md",
    "anti-pattern-register.md",
]


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def pack_file(name):
    return read(os.path.join(PACK_DIR, name))


def register(name):
    return read(os.path.join(DM_DIR, name))


def flat(text):
    """Whitespace- and blockquote-normalised view, so an assertion is not a hostage
    to line wrapping or to a `>` continuation marker."""
    return re.sub(r"\s+", " ", re.sub(r"(?m)^\s*>\s?", "", text))


SPINE = pack_file("decision-tree.md")
PACK_TEXT = pack_file("pack.yaml")
PACK = yaml.safe_load(PACK_TEXT)
GLOSSARY = pack_file("glossary.md")
QBANK = pack_file("question-bank.md")
ALTERNATIVES = register("alternatives-register.md")
BLOCKING = register("blocking-set.md")
COMPOSED = register("composed-disqualifiers.md")
OUTCOMES = register("outcome-classes.md")
VOLATILITY = register("volatility-register.md")

LENS_TECH = read(os.path.join(ROOT, ".claude", "skills", "lens-technology", "SKILL.md"))
PERSONA = read(os.path.join(ROOT, ".claude", "agents", "solution-architect.md"))
CHAIRMAN = read(os.path.join(ROOT, ".claude", "skills", "chairman-synthesis", "SKILL.md"))


# --------------------------------------------------------------------------- spine


class TestSpine(unittest.TestCase):
    def test_twelve_material_concerns_present(self):
        found = sorted({int(m) for m in re.findall(r"\*\*C(\d{1,2})\*\*", SPINE)})
        self.assertEqual(list(range(1, 13)), found, "concerns found: %r" % found)

    def test_ten_stages_present_and_in_order(self):
        stages = re.findall(r"\*\*(S[0-9])\*\*", SPINE)
        ordered = []
        for s in stages:
            if s not in ordered:
                ordered.append(s)
        self.assertEqual(["S%d" % i for i in range(10)], ordered,
                         "stage order: %r" % ordered)

    def test_phase_gate_is_options_only(self):
        self.assertIn("applies_to_phase: options", SPINE)
        self.assertIn("never before", SPINE)

    def test_no_scored_verdict_ladder(self):
        # The only places the spine may mention scoring are the prohibitions themselves.
        low = flat(SPINE).lower()
        prohibitions = [
            "no numeric fit score, no weight, no aggregated verdict, no ordinal ladder "
            "(`forte`/`adequada`/…) enters this procedure at any point",
            "never a score",
            "it replaces the scored three-branch tree",
            "a weighted average passes all of them",
            "**states, not scores.**",
            "they are not a checklist, not scored",
        ]
        for text in prohibitions:
            self.assertIn(text, low, "spine lost a scoring prohibition: %r" % text[:40])
            low = low.replace(text, "")
        for token in ("forte", "adequada", "inadequada", "intermédia",
                      "score", "weighted", "weighting", "fit rating"):
            self.assertNotIn(token, low, "spine carries a scoring token: %r" % token)

    def test_no_hardcoded_platform_threshold(self):
        # a figure with a unit is a dated service limit disguised as a rule
        bad = re.findall(
            r"\b\d[\d,\.]*\s*(?:rows|records|items|users|GB|MB|KB|seconds|minutes|hours|days|%)\b",
            SPINE)
        self.assertEqual([], bad, "spine hardcodes a platform figure: %r" % bad)

    def test_evidence_grade_rule_present(self):
        self.assertIn("`Assumed` evidence alone never settles a hard exclusion", SPINE)
        self.assertIn("evidence grade", SPINE)
        self.assertIn("materiality / swing", SPINE)
        self.assertIn("cannot be emitted from `Assumed` evidence alone", SPINE)

    def test_d0_requires_affirmative_rationale(self):
        f = flat(SPINE)
        self.assertIn("affirmative rationale", f)
        self.assertIn("Absence of evidence is never a D0 rationale", f)
        self.assertIn("evidence gap, not D0", f)
        # and a gap must not be forced to block
        self.assertIn("Do not force every gap to become decision-blocking", f)

    def test_blocking_set_membership_alone_does_not_block(self):
        """Step 3B2 finding F-1: an entry EXISTING in the blocking set is not the same
        thing as that entry being ENGAGED by the engagement. Only an engaged entry
        escalates a gap to *decision blocked* (blocking-set.md §0)."""
        f = flat(SPINE)
        # the escalation clause carries the engaged-entry qualification
        self.assertIn(
            "membership of the blocking set **where the entry is engaged by the engagement**, "
            "escalates to *decision blocked*", f)
        # and membership alone is explicitly insufficient
        self.assertIn("presence in the register is not engagement", f)
        # the unqualified form must not survive anywhere in the spine
        self.assertNotIn("membership of the blocking set, escalates", f)
        # the owning register is the one that governs engagement
        self.assertIn("`decision-model/blocking-set.md` §0", f)

    def test_emergent_concern_obligation_present(self):
        f = flat(SPINE)
        self.assertIn("emergent-concern obligation", f.lower())
        self.assertIn("or in the twelve concerns above", f)
        self.assertIn("Silent omission is a defect", f)
        self.assertIn("outside all twelve", f.lower())

    def test_constraints_declared_as_floor_not_ceiling(self):
        self.assertIn("floor, never a ceiling", SPINE)

    def test_no_branch_option_space(self):
        self.assertNotIn("branches:", SPINE)
        self.assertNotIn("inputs_used:", SPINE)
        self.assertIn("Architecture shapes are not the option space", SPINE)

    def test_no_second_state_machine(self):
        self.assertIn("No new state machine", SPINE)

    def test_all_sixteen_required_sections_present(self):
        for heading in ("Purpose and phase gate", "Governing doctrine", "Decision semantics",
                        "Evidence grade required for a disqualifier",
                        "The 12 material decision concerns", "The 10 ordered stages",
                        "Broad coverage, selective depth", "Depth ladder",
                        "The emergent-concern obligation", "Stage-local registers",
                        "Domain-knowledge pull rule", "Cross-domain and composed reasoning",
                        "Volatile-fact boundary", "Proof requirement",
                        "Comparator discipline", "Outcome and render handoff"):
            self.assertIn(heading, SPINE, "spine missing section: %r" % heading)

    def test_validation_levels_v1_to_v4(self):
        for lvl in ("**V1**", "**V2**", "**V3**", "**V4**"):
            self.assertIn(lvl, SPINE)


# ----------------------------------------------------------------------- registers


class TestRegisterInventory(unittest.TestCase):
    def test_exactly_five_runtime_registers(self):
        present = sorted(f for f in os.listdir(DM_DIR) if f.endswith(".md"))
        self.assertEqual(sorted(RUNTIME_REGISTERS), present, "decision-model/ holds %r" % present)

    def test_the_five_deferred_artifacts_were_not_created(self):
        for name in NOT_RUNTIME:
            self.assertFalse(os.path.exists(os.path.join(DM_DIR, name)),
                             "%s must stay an authoring artifact" % name)

    def test_no_router_file(self):
        for f in os.listdir(DM_DIR):
            self.assertNotIn("rout", f.lower(), "a routing subsystem was created: %r" % f)


class TestAlternativesRegister(unittest.TestCase):
    def test_eleven_option_classes(self):
        ids = sorted({m for m in re.findall(r"ALT-0\d\d", ALTERNATIVES)})
        self.assertEqual(11, len(ids), "ALT classes: %r" % ids)
        self.assertEqual(["ALT-%03d" % i for i in range(1, 12)], ids)

    def test_trigger_map_is_candidate_generation_not_verdict(self):
        self.assertIn("A trigger generates a candidate. It never produces a verdict", ALTERNATIVES)

    def test_process_change_and_do_nothing_are_conditional_members(self):
        self.assertIn("are conditional members of the candidate set", ALTERNATIVES)
        self.assertIn("`ALT-002`", ALTERNATIVES)
        self.assertIn("`ALT-010`", ALTERNATIVES)

    def test_platform_is_not_the_default_candidate(self):
        self.assertIn("`ALT-004` is not the default candidate", ALTERNATIVES)

    def test_trigger_rows_present(self):
        rows = re.findall(r"^\|\s*(\d{1,2})\s*\|", ALTERNATIVES, re.M)
        self.assertGreaterEqual(len(rows), 29, "trigger map rows: %d" % len(rows))

    def test_forbidden_universals_registered(self):
        for claim in ("Custom development is more expensive", "Low-code is faster",
                      "does not scale", "Building it yourself gives you control"):
            self.assertIn(claim, ALTERNATIVES)

    def test_symmetric_unknowns_registered(self):
        self.assertIn("Symmetrically unknown", ALTERNATIVES)
        self.assertIn("**All eleven classes.**", ALTERNATIVES)


class TestBlockingSet(unittest.TestCase):
    def test_twenty_eight_blocking_entries(self):
        ids = sorted({m for m in re.findall(r"\bB-\d\d\b", BLOCKING)})
        self.assertEqual(28, len(ids), "blocking entries: %r" % ids)
        self.assertEqual(["B-%02d" % i for i in range(1, 29)], ids)

    def test_three_scope_blockers(self):
        ids = sorted({m for m in re.findall(r"\bBS-\d\d\b", BLOCKING)})
        self.assertEqual(["BS-01", "BS-02", "BS-03"], ids)

    def test_engagement_neutral(self):
        self.assertIn("never** here", BLOCKING.replace("**never** here", "never** here"))
        for banned in ("due date:", "by 2026-", "owner: J", "days elapsed"):
            self.assertNotIn(banned, BLOCKING)
        self.assertIn("The **actual due date**", BLOCKING)
        # What the engagement resolves is a ROLE or a SOURCE, never a person (P-21 / F1.1).
        self.assertIn("The **actual role or source**", BLOCKING)
        self.assertIn("`role:`", BLOCKING)
        self.assertIn("`fonte:`", BLOCKING)
        self.assertNotIn("named owner", " ".join(BLOCKING.split()))

    def test_every_entry_carries_a_custo_default(self):
        rows = [ln for ln in BLOCKING.splitlines() if re.match(r"\|\s*B-\d\d\s*\|", ln)]
        self.assertEqual(28, len(rows))
        for ln in rows:
            self.assertRegex(ln, r"`(email|documento|reuniao|spike)`",
                             "entry without a custo default: %r" % ln[:40])

    def test_swing_is_decisivo_by_construction(self):
        self.assertIn("`swing: decisivo` by construction", BLOCKING)

    def test_not_a_questionnaire(self):
        self.assertIn("NOT a questionnaire", BLOCKING)


class TestComposedDisqualifiers(unittest.TestCase):
    def test_exactly_twelve_registered_rows(self):
        ids = sorted({m for m in re.findall(r"\bCD-\d\d\b", COMPOSED)})
        self.assertEqual(["CD-%02d" % i for i in range(1, 13)], ids,
                         "composed rows: %r" % ids)

    def test_no_thirteenth_row(self):
        self.assertNotIn("CD-13", COMPOSED)
        self.assertIn("The register is closed at twelve", COMPOSED)

    def test_conditional_rows_six_and_nine_kept_conditional(self):
        self.assertIn("CD-06 and CD-09", COMPOSED.replace("**CD-06** and **CD-09**", "CD-06 and CD-09"))
        self.assertIn("Never an exclusion outcome", COMPOSED)
        self.assertIn("Never a platform exclusion", COMPOSED)

    def test_migration_row_is_not_an_exclusion(self):
        f = flat(COMPOSED)
        self.assertIn("cannot be brought to the required class in place", f)
        self.assertIn("In-place remediation unavailable — migration required", f)
        self.assertIn("CD-11 is a migration, not an exclusion", f)

    def test_emergent_is_evaluated_but_never_registered(self):
        self.assertIn("does not become a registered row merely because it occurred", COMPOSED)

    def test_every_row_names_a_reachable_outcome(self):
        rows = [ln for ln in COMPOSED.splitlines() if re.match(r"\|\s*\*\*CD-\d\d\*\*", ln)]
        self.assertEqual(12, len(rows))
        for ln in rows:
            self.assertTrue(ln.rstrip().endswith("|"))
            self.assertGreater(len(ln.split("|")[-2].strip()), 10,
                               "row without a reachable outcome: %r" % ln[:30])


class TestOutcomeClasses(unittest.TestCase):
    def test_closed_set_of_fifteen(self):
        nums = [int(m) for m in re.findall(r"^\|\s*\*\*(\d{1,2})\*\*\s*\|", OUTCOMES, re.M)]
        self.assertEqual(list(range(1, 16)), nums, "outcome classes: %r" % nums)

    def test_class_fifteen_keeps_an_option_on_the_table(self):
        """An organisational rule is a decision someone can unmake, so it reaches a
        conditional verdict — never one of the evidence-based exclusions."""
        row = [ln for ln in OUTCOMES.splitlines() if ln.startswith("| **15** |")]
        self.assertEqual(1, len(row), "class 15 rows: %d" % len(row))
        cell = flat(row[0]).lower()
        for field in ("rule", "condition", "impact", "cost", "risk",
                      "who can change", "status"):
            self.assertIn(field, cell, "class 15 lacks %r" % field)
        self.assertIn("never followed by class 8", cell)

    def test_an_organisational_rule_never_reaches_an_exclusion(self):
        self.assertIn("### 1.0", OUTCOMES)
        body = flat(OUTCOMES[OUTCOMES.index("### 1.0"):OUTCOMES.index("### 1.1")])
        self.assertIn("never emits classes 5, 6, 7, 9 or", body)
        self.assertIn("imposed technology is a rule", body)

    def test_closure_is_stated_as_testable(self):
        self.assertIn("defect in the emitter, not a new class", OUTCOMES)

    def test_class_seven_reason_discriminator(self):
        self.assertIn("7-INFEASIBLE", OUTCOMES)
        self.assertIn("7-UNATTRACTIVE", OUTCOMES)
        self.assertIn("economically infeasible", OUTCOMES)
        self.assertIn("economically unattractive", OUTCOMES)
        self.assertIn("The disjunction is never rendered", OUTCOMES)
        self.assertIn("chosen from the trigger, not from tone", OUTCOMES)

    def test_class_seven_implies_nothing_about_price_elsewhere(self):
        self.assertIn("may imply another class is cheaper", OUTCOMES)

    def test_class_thirteen_two_forms_never_merge(self):
        self.assertIn("two forms that never merge", OUTCOMES)
        self.assertIn("(a) documented sufficiency", OUTCOMES)
        self.assertIn("(b) candidate, not documented sufficiency", OUTCOMES)
        self.assertIn("graduation trigger", OUTCOMES.lower())
        self.assertIn("never in form\n> (b)", OUTCOMES)

    def test_scope_pairs_are_normative(self):
        self.assertIn("One outcome per scope, not one per engagement", OUTCOMES)
        self.assertIn("never collapse them", OUTCOMES)

    def test_migration_not_remediation(self):
        self.assertIn("MIGRATION REQUIRED", OUTCOMES)
        self.assertIn("migration, not a remediation", OUTCOMES)

    def test_settled_exclusions_need_decision_grade_evidence(self):
        self.assertIn("Classes 5, 6, 7, 9 and 14 are settled exclusions", OUTCOMES)
        self.assertIn("cannot be emitted from `Assumed` evidence alone", OUTCOMES)

    def test_comparator_default_is_absent(self):
        self.assertIn("COMPARATOR EVIDENCE ABSENT", OUTCOMES)
        self.assertIn("part of the outcome, not a footnote", OUTCOMES)

    def test_preference_is_licensed_on_one_axis_only(self):
        self.assertIn("One axis only: the deployment model", OUTCOMES)


class TestVolatilityRegister(unittest.TestCase):
    def test_ten_commercial_entries(self):
        ids = sorted({m for m in re.findall(r"\bVC-\d\d\b", VOLATILITY)})
        self.assertEqual(["VC-%02d" % i for i in range(1, 11)], ids, "commercial: %r" % ids)

    def test_service_entries_are_contiguous_from_the_step_3_baseline(self):
        """Step 3B1 authored VS-01..VS-20; later steps may ADD ownership rows.

        Pinned to exactly twenty, this asserted that no later authoring step had extended
        volatility OWNERSHIP — which is not what it was for. The Step 4B pre-4C bounded
        repair added VS-21..VS-39 and split VS-04 to close the ownership gap Step 4B found;
        that amendment changes no decision semantic. What must hold is that the Step 3
        baseline survives and the id space stays contiguous with no holes.
        """
        ids = sorted({m for m in re.findall(r"\bVS-\d\d\b", VOLATILITY)})
        for i in range(1, 21):
            self.assertIn("VS-%02d" % i, ids,
                          "the Step 3 baseline row VS-%02d is gone" % i)
        self.assertEqual(["VS-%02d" % i for i in range(1, len(ids) + 1)], ids,
                         "service ids are not contiguous: %r" % ids)

    def test_every_entry_states_a_re_verify_trigger(self):
        rows = [ln for ln in VOLATILITY.splitlines()
                if re.match(r"\|\s*\*\*V[CS]-\d\d\*\*", ln)]
        self.assertGreaterEqual(len(rows), 30,
                                "the Step 3 baseline of 30 entries must survive")
        for ln in rows:
            self.assertGreater(len(ln.split("|")[-2].strip()), 5,
                               "entry without a re-verify trigger: %r" % ln[:30])

    def test_live_conflict_recorded(self):
        self.assertIn("CONFLICTED", VOLATILITY)
        self.assertIn("20×", VOLATILITY)
        self.assertIn("not** a penalty against this platform", VOLATILITY)

    def test_dated_tripwires_present(self):
        ids = sorted({m for m in re.findall(r"\bTW-V\d\b", VOLATILITY)})
        self.assertGreaterEqual(len(ids), 3, "tripwires: %r" % ids)
        for token in ("February 2026", "1 November 2026", "February 2027"):
            self.assertIn(token, VOLATILITY)

    def test_not_a_standing_checklist(self):
        self.assertIn("Do not walk the register", VOLATILITY)


class TestStageLocalLoading(unittest.TestCase):
    def test_spine_declares_the_consuming_stage_per_register(self):
        for stage, name in (("S1", "alternatives-register.md"),
                            ("S3", "blocking-set.md"),
                            ("S6", "composed-disqualifiers.md"),
                            ("S9", "outcome-classes.md")):
            lines = [ln for ln in SPINE.splitlines()
                     if name in ln and "decision-model/" in ln]
            self.assertTrue(lines, "spine does not name %s" % name)
            self.assertTrue(any(stage in ln for ln in lines),
                            "%s not bound to %s" % (name, stage))

    def test_volatility_is_on_demand_only(self):
        self.assertIn("Only** where an active decision question depends on a volatile fact", SPINE)

    def test_six_stages_load_no_register(self):
        self.assertIn("S0, S2, S4, S5, S7, S8 | **none**", SPINE)

    def test_no_preloading_and_no_router(self):
        self.assertIn("No preloading, and no router", SPINE)

    def test_pack_yaml_binds_each_register_to_its_stage(self):
        dm = PACK["decision_model"]
        self.assertEqual("S1", dm["alternatives"]["stage"])
        self.assertEqual("S3", dm["blocking"]["stage"])
        self.assertEqual("S6", dm["composed"]["stage"])
        self.assertEqual("S9", dm["outcomes"]["stage"])
        self.assertEqual("on-demand", dm["volatility"]["loading"])
        self.assertNotIn("stage", dm["volatility"])

    def test_every_declared_register_resolves(self):
        for key, cfg in PACK["decision_model"].items():
            path = os.path.join(PACK_DIR, cfg["source"])
            self.assertTrue(os.path.exists(path), "%s -> %s missing" % (key, cfg["source"]))


# ------------------------------------------------------------------------ contracts


class TestPackContract(unittest.TestCase):
    def test_pack_yaml_is_valid_and_bumped(self):
        """Step 3B1 bumped the pack to 1.5.0; later steps bump it further.

        Pinned to an exact version this asserted that no later authoring step had run, which
        is not what it was for. It is a FLOOR: the Step 3 line must have landed. Step 4B
        (domain-knowledge re-taxonomy) legitimately took it to 1.6.0.
        """
        self.assertEqual("pp", PACK["pack_id"])
        version = tuple(int(p) for p in str(PACK["pack_version"]).split("."))
        self.assertGreaterEqual(version, (1, 5, 0),
                                "pack_version regressed below the Step 3 line: %r"
                                % (PACK["pack_version"],))

    def test_constraint_floor_is_the_approved_ten(self):
        floor = PACK["lenses_config"]["technology"]["constraints_to_check"]
        self.assertEqual(APPROVED_FLOOR, floor)

    def test_floor_is_documented_as_non_limiting(self):
        self.assertIn("STANDING-ATTENTION FLOOR, never a ceiling", PACK_TEXT)
        self.assertIn("NOT by this list", PACK_TEXT)

    def test_decision_tree_still_options_gated(self):
        self.assertEqual("decision-tree.md", PACK["decision_tree"]["source"])
        self.assertEqual("options", PACK["decision_tree"]["consulted_in_phase"])

    def test_discovery_extra_signals_stay_at_thirty_six(self):
        total = sum(len(PACK["lenses_config"][l]["extra_signals"]) for l in DISCOVERY)
        self.assertEqual(36, total, "Phase G signal set changed: %d" % total)

    def test_technology_lens_still_has_no_discovery_cues(self):
        self.assertNotIn("extra_signals", PACK["lenses_config"]["technology"])


class TestLensAndPersona(unittest.TestCase):
    def test_lens_emits_a_verdict_per_material_concern(self):
        self.assertIn("a verdict per material concern, at proportional depth", LENS_TECH)
        self.assertNotIn("a constraint verdict per constraint", LENS_TECH)

    def test_lens_states_floor_not_ceiling(self):
        self.assertIn("floor, never the ceiling", LENS_TECH)
        self.assertIn("standing-attention floor, never a ceiling", LENS_TECH)

    def test_lens_generates_option_classes_not_branches(self):
        self.assertIn("generate the candidate option classes", LENS_TECH)
        self.assertNotIn("identify the candidate branches", LENS_TECH)

    def test_lens_keeps_what_step_3a_said_to_keep(self):
        self.assertIn("**Active in**: Options, Decision.", LENS_TECH)
        self.assertIn("Cues, not coverage", LENS_TECH)
        self.assertIn("pull-based, not push-based", LENS_TECH)
        self.assertIn("conditional members", LENS_TECH)
        for n in range(1, 6):
            self.assertIn("%d. **" % n, LENS_TECH)

    def test_lens_stays_small(self):
        self.assertLess(len(LENS_TECH.splitlines()), 90,
                        "lens grew past its size budget")

    def test_persona_uses_option_classes(self):
        self.assertIn("option-class trigger map", PERSONA)
        self.assertNotIn("constraint verdicts (pass / risky / blocker)", PERSONA)

    def test_persona_stays_concise(self):
        self.assertLess(len(PERSONA.splitlines()), 45,
                        "persona duplicated the decision procedure")

    def test_persona_does_not_restate_the_procedure(self):
        for token in ("S0", "S5", "S9", "C1", "C12", "ALT-0"):
            self.assertNotIn(token, PERSONA,
                             "persona restates the procedure: %r" % token)


class TestChairmanOutput(unittest.TestCase):
    def test_options_template_supports_the_approved_fields(self):
        for field in ("**Viability**", "**Outcome**", "**Material strengths**",
                      "**Disqualifiers**", "**Preconditions**", "**Material trade-offs**",
                      "**Material risks**", "**Cost drivers**",
                      "**Decision-changing uncertainties**", "**Proof requirement**",
                      "**Concern notes**"):
            self.assertIn(field, CHAIRMAN, "options.md template missing %r" % field)

    def test_round_level_structure(self):
        for heading in ("## Concern coverage", "## Class coverage", "## Comparison",
                        "## Recommendation", "## Comparator status"):
            self.assertIn(heading, CHAIRMAN)

    def test_no_giant_matrix(self):
        self.assertIn("do NOT render a 12×N grid", CHAIRMAN)

    def test_old_pros_cons_block_is_gone(self):
        self.assertNotIn("- **Pros**:", CHAIRMAN)
        self.assertNotIn("- **Cons**:", CHAIRMAN)
        self.assertNotIn("**Constraints checked**", CHAIRMAN)

    def test_comparator_discipline_carried(self):
        self.assertIn("COMPARATOR EVIDENCE ABSENT", CHAIRMAN)
        self.assertIn("does not prove another is superior", CHAIRMAN)

    def test_no_scoring_in_the_artefact(self):
        self.assertIn("No score, no weight, no ordinal ladder", CHAIRMAN)

    def test_the_two_classes_are_conditional_with_a_declared_absence(self):
        """C2: the floor became a declaration. What is checked is that the round has
        to SAY something about each class — never that its answer is right."""
        self.assertNotIn("Must include **at least**: one do-nothing baseline", CHAIRMAN)
        for marker in ("DO-NOTHING", "PROCESS-CHANGE", "NOT PLAUSIBLE"):
            self.assertIn(marker, CHAIRMAN, "class coverage lacks %r" % marker)


class TestInternalVocabularyStaysInternal(unittest.TestCase):
    def test_glossary_has_the_four_new_options_terms(self):
        part_c = GLOSSARY.split("# Part C", 1)[1]
        for term in ("**Option class**", "**Disqualifier**",
                     "**Comparator evidence absent**", "**Graduation trigger**"):
            self.assertIn(term, part_c)

    def test_glossary_exposes_no_internal_code(self):
        part_c = GLOSSARY.split("# Part C", 1)[1]
        for code in ("Xp", "Xr", "Xe", "Xc", "`Ri`", "`Cf`",
                     "D0", "D1", "D2", "D3", "7-INFEASIBLE", "7-UNATTRACTIVE",
                     "ALT-", "CD-", "DC-D-", "class 5", "class 13"):
            self.assertNotIn(code, part_c, "Part C exposes internal code %r" % code)

    def test_proof_requirement_is_the_single_shared_term(self):
        part_c = GLOSSARY.split("# Part C", 1)[1]
        self.assertIn("*Validation level* is not a second term", part_c)

    def test_precondition_is_reused_not_restated(self):
        part_c = GLOSSARY.split("# Part C", 1)[1]
        self.assertIn("Precondition** (A5)", part_c)

    def test_spine_forbids_rendering_internal_vocabulary(self):
        self.assertIn("Internal vocabulary stays internal", SPINE)
        self.assertIn("Never rendered as engagement vocabulary", SPINE)


class TestQuestionBank(unittest.TestCase):
    def test_no_technology_questionnaire_was_created(self):
        self.assertEqual([], re.findall(r"\b[QP]-TEC-\d\d\b", QBANK))
        codes = {m for m in re.findall(r"\*\*[QP]-([A-Z]{3})-\d\d\*\*", QBANK)}
        self.assertEqual({"BUS", "OPS", "USR", "DAT", "GOV", "FIN"}, codes)

    def test_reachable_outcomes_carry_the_two_missing_terminals(self):
        low = QBANK.lower()
        self.assertIn("the decision is blocked and more evidence is required", low)
        self.assertIn("an alternative is sufficient and this platform is not excluded", low)

    def test_original_reachability_guards_survived(self):
        low = QBANK.lower()
        for phrase in ("another kind of technology is preferable",
                       "process change without new technology",
                       "doing nothing"):
            self.assertIn(phrase, low)

    def test_scope_pairing_is_stated_on_the_elicitation_side(self):
        self.assertIn("must not be collapsed", QBANK)


class TestArchitectureTemplatesRescoped(unittest.TestCase):
    """The Options-side guarantee only: no architecture shape is an option class.

    Step 5B replaced the three store-first branch shapes with one fixed entry point plus
    fragments. The taxonomy, authorization and fragment-invariant assertions live in
    .claude/tests/test_pp_architecture_templates.py — this class keeps only what Step 3
    needs to stay true: the architecture layer never presents itself as the option space.
    """

    def test_readme_states_the_positioning(self):
        readme = read(os.path.join(PACK_DIR, "architecture-templates", "README.md"))
        self.assertIn("It is not an option, not an option class", readme)
        self.assertIn("one option class presented as the whole", readme)
        self.assertIn("Compare option classes first", readme)

    def test_no_architecture_template_claims_to_be_an_option_class(self):
        d = os.path.join(PACK_DIR, "architecture-templates")
        units = [f for f in os.listdir(d) if f.endswith(".md") and f != "README.md"]
        self.assertEqual(5, len(units), "runtime template units: %r" % units)
        for f in units:
            text = read(os.path.join(d, f))
            self.assertIn("NOT an option class", text, "%s: missing the disclaimer" % f)
            # The retired branch model must not survive anywhere in the layer.
            self.assertNotIn("applies_to_branch", text)
            self.assertNotIn("available_after_outcome", text)

    def test_options_layer_carries_no_architecture_vocabulary(self):
        """Architecture belongs downstream; the option space stays option classes."""
        for skill in ("aisa-options", "aisa-simulate"):
            body = read(os.path.join(ROOT, ".claude", "skills", skill, "SKILL.md"))
            self.assertNotIn("<branch>", body)
            for token in ("experience.mode", "record_authority",
                          "architecture.authorization"):
                self.assertNotIn(token, body, "%s: %s leaked upward" % (skill, token))


class TestNeutrality(unittest.TestCase):
    def test_every_non_platform_outcome_is_reachable(self):
        for outcome in ("PROCESS REDESIGN", "DO NOTHING / DEFER",
                        "DECISION BLOCKED", "ALTERNATIVE SUFFICIENT",
                        "CANDIDATE SET", "DEPLOYMENT MODEL EXCLUDES THIS PLATFORM"):
            self.assertIn(outcome, OUTCOMES)

    def test_reachability_floor_is_enforced(self):
        f = flat(SPINE)
        self.assertIn("the procedure failed at S1 and must be re-run", f)
        self.assertIn("never eliminated by a platform disqualifier", f)

    def test_the_floor_does_not_fire_inside_an_imposed_boundary(self):
        """A set of one platform's forms is the correct result of a constrained
        generation, not evidence that S1 failed."""
        f = flat(SPINE)
        self.assertIn("unless the platform is a declared imposed constraint", f)
        self.assertIn("§6.2", SPINE)

    def test_an_imposed_technology_never_produces_a_platform_swap(self):
        body = flat(SPINE[SPINE.index("### 6.2"):SPINE.index("## 7.")])
        self.assertIn("No candidate proposes changing platform", body)
        self.assertIn("class 15", body)

    def test_gates_are_symmetric_and_stated_as_such(self):
        self.assertIn("never an advantage of\n> `ALT-004`", ALTERNATIVES)
        self.assertIn("The gates cut both ways", SPINE)

    def test_no_silent_comparator_claim_permitted(self):
        self.assertIn("Being able to exclude this platform\ndoes not prove the replacement is superior",
                      SPINE)
        for word in ("*better*", "*cheaper*", "*faster*"):
            self.assertIn(word, SPINE)


if __name__ == "__main__":
    unittest.main(verbosity=2)
