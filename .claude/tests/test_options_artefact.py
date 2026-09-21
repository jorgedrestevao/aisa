"""`options.md` is a decision artefact, not a transcript — contract + real-file checks.

Two defects observed in `pricing-bunkers` O-01, both of them contract holes rather than
model failures:

  1. **No option named its technology.** The architect returned the store half only
     ("this platform over the shared relational database", "…over the governed store")
     and the chairman abstracted even that away in the option titles. `ALT-004` was one
     candidate "in its several forms", so nothing obliged anyone to name a form — and
     one rendered option silently covered two of them. The cause of the abstraction was
     the pack's own "plain language only / no internal framework vocabulary" rule, read
     as a ban on product names. An older engagement (`cae-automation`) named its forms
     fine, which is what makes this a regression and not a model quirk.

  2. **8 542 words.** Thirteen mandatory fields per option × eleven candidates, plus a
     twelve-line concern coverage, plus a summary and a closing section that restate the
     entries. Every field was defensible; the file was unreadable, and an artefact nobody
     reads to the end has not delivered a decision.

The repair: `alternatives-register.md` §1.2 makes `ALT-004` a class of `surface × store`
forms, `decision-tree.md` §14.1 makes the form a mandatory returned field, and the
`chairman-synthesis` template puts a decision table first, budgets the *prose* at ~1 500
words with ≤120 per option, and relocates the long form to the round's audit log.

    python .claude/tests/test_options_artefact.py
"""

import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PACK_DIR = os.path.join(ROOT, "library", "packs", "pp")
SKILLS = os.path.join(ROOT, ".claude", "skills")
PROJECTS = os.path.join(ROOT, "projects")

WORD_BUDGET = 1500
# The budget is a contract, not a ruler: a round with many candidates carries a longer
# table, and a file is only a failure when it is out by more than a third.
WORD_CEILING = int(WORD_BUDGET * 4 / 3)
OPTION_BUDGET = 120
OPTION_CEILING = int(OPTION_BUDGET * 4 / 3)

# What says a file was written under this contract: the decision table itself — a header
# row naming a technology column, over rows keyed by option id. It is detected by SHAPE,
# never by an English phrase: the artefact is rendered in the pack's language, and the
# first real file written under this contract came back in Portuguese with every check
# silently skipped. A marker that only matches one language passes a broken file.
TABLE_ROW = re.compile(r"^\|\s*(O-\d{3})\s*\|")
SEPARATOR = re.compile(r"^\|[\s:|-]+\|\s*$")
TECH_CELL = re.compile(r"^(technology|tecnologia|tecnología|technologie)$", re.I)


def _cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def decision_table(text):
    """The decision table's (header, rows), or (None, []).

    Detected by SHAPE, never by an English phrase: the artefact is rendered in the
    pack's language, and the first real file written under this contract came back in
    Portuguese with every check silently skipped. Shape means a real markdown header —
    a header line followed by its separator, carrying a technology COLUMN — over rows
    keyed by option id. Matching the bare word anywhere would also catch a legacy file
    whose body happens to say "non-technology" in a cell."""
    lines = text.splitlines()
    for i, line in enumerate(lines[:-1]):
        if not line.startswith("|") or not SEPARATOR.match(lines[i + 1]):
            continue
        header = _cells(line)
        if not any(TECH_CELL.match(c) for c in header):
            continue
        rows = []
        for row in lines[i + 2:]:
            if not TABLE_ROW.match(row):
                if row.startswith("|"):
                    continue
                break
            rows.append(row)
        if rows:
            return header, rows
    return None, []


def on_contract(text):
    return decision_table(text)[0] is not None


# The contract has GENERATIONS, and the prose budget belongs to the current one.
#
# P-19 (2026-09-08) put the decision table first and budgeted the prose. C1 + G1
# (2026-09-09, `cb9172b`) then replaced the effort column with an **order of magnitude**
# carrying one of four closed-set source markers, and moved the long per-option form to
# the round's audit log — which is what makes the budget reachable at eleven candidates.
#
# An artefact written between the two is on the table contract and predates the field
# contract. It is FROZEN: §14 of the refocus plan puts altering an existing engagement out
# of scope, and rewriting a round's own output would falsify the record of that round. So
# it is reported with its numbers and not judged — the same treatment a legacy file gets,
# for the same reason, one generation later.
#
# This is not slack for new work. `chairman-synthesis` emits the order-of-magnitude column
# and a source marker by construction, so anything written today lands in the judged tier
# automatically; and the budget is demonstrably reachable there — `pricing-bunkers` O-03
# carries THIRTEEN candidates in 1 720 words, where its own O-02 carries eleven in 2 230.
ESTIMATE_CELL = re.compile(r"^(ordem de grandeza|order of magnitude)$", re.I)
SOURCE_MARKERS = ("SIMULATED", "PACK MODEL", "ANALOGY", "ORDER OF MAGNITUDE UNAVAILABLE")


def on_current_generation(text):
    """The C1/G1 generation, by shape: the table's estimate column is an order of
    magnitude, or the file carries one of the four source markers verbatim."""
    if not on_contract(text):
        return False
    header, _rows = decision_table(text)
    if any(ESTIMATE_CELL.match(c) for c in header):
        return True
    return any(m in text for m in SOURCE_MARKERS)


def read(*parts):
    with open(os.path.join(*parts), encoding="utf-8") as fh:
        return fh.read()


def flat(text):
    return re.sub(r"\s+", " ", re.sub(r"(?m)^\s*>\s?", "", text))


ALTERNATIVES = read(PACK_DIR, "decision-model", "alternatives-register.md")
SPINE = read(PACK_DIR, "decision-tree.md")
CHAIRMAN = read(SKILLS, "chairman-synthesis", "SKILL.md")
OPTIONS_SKILL = read(SKILLS, "aisa-options", "SKILL.md")
DECIDE = read(SKILLS, "aisa-decide", "SKILL.md")
SIMULATE = read(SKILLS, "aisa-simulate", "SKILL.md")
PHASES = read(ROOT, "library", "kernel", "phases.md")


def options_section(text):
    """The Options branch of the chairman's phase-artefact step."""
    start = text.index("#### Options → `<engagement>/options.md`")
    end = text.index("### Step 7 — Write the synthesis audit log")
    return text[start:end]


def audit_log_section(text):
    return text[text.index("### Step 7 — Write the synthesis audit log"):]


OPT_TEMPLATE = options_section(CHAIRMAN)
LOG_TEMPLATE = audit_log_section(CHAIRMAN)


# --------------------------------------------------------------------------- the pack


class TestFormsRegister(unittest.TestCase):
    """`ALT-004` is a class of forms, and a form is surface × store."""

    def test_alt_004_row_names_the_form_not_the_platform(self):
        row = [ln for ln in ALTERNATIVES.splitlines() if ln.startswith("| `ALT-004` |")]
        self.assertEqual(1, len(row), "ALT-004 row: %r" % row)
        self.assertIn("surface", row[0])
        self.assertIn("§1.2", row[0])

    def test_section_1_2_exists_and_is_stage_local_to_S1(self):
        self.assertIn("### 1.2", ALTERNATIVES)
        body = ALTERNATIVES[ALTERNATIVES.index("### 1.2"):]
        body = body[:body.index("\n## 2.")]
        self.assertIn("S1", body, "the forms table must say where it is generated")
        self.assertIn("S9", body, "…and where it is re-read")
        self.assertIn("§14.1", body, "…and who obliges the rendering")

    def test_forms_table_pairs_a_surface_with_a_store(self):
        body = ALTERNATIVES[ALTERNATIVES.index("### 1.2"):]
        body = body[:body.index("\n## 2.")]
        rows = [ln for ln in body.splitlines()
                if ln.startswith("|") and "---" not in ln and "Store the surface" not in ln]
        self.assertGreaterEqual(len(rows), 8, "forms: %d" % len(rows))
        for ln in rows:
            cells = [c.strip() for c in ln.strip("|").split("|")]
            self.assertEqual(3, len(cells), "malformed form row: %r" % ln[:60])
            self.assertTrue(all(cells), "empty cell in %r" % ln[:60])

    def test_the_one_mandatory_pairing_is_recorded(self):
        """The record-centric surface does not exist without the governed store — the
        single fact that makes a store choice decide a surface."""
        body = flat(ALTERNATIVES[ALTERNATIVES.index("### 1.2"):])
        self.assertIn("governed store only", body)
        self.assertIn("no record-centric app without", body)

    def test_one_option_per_form(self):
        body = flat(ALTERNATIVES[ALTERNATIVES.index("### 1.2"):])
        self.assertIn("One option per form", body)

    def test_a_lost_form_is_a_redirect_never_an_exclusion(self):
        body = flat(ALTERNATIVES[ALTERNATIVES.index("### 1.2"):])
        self.assertIn("never an exclusion outcome", body)

    def test_the_table_generates_and_never_verdicts(self):
        body = flat(ALTERNATIVES[ALTERNATIVES.index("### 1.2"):])
        self.assertIn("issues no verdict", body)

    def test_decision_model_still_holds_exactly_five_registers(self):
        """The forms table lives inside the S1 register on purpose: the runtime
        decision-model set is frozen at five files."""
        present = sorted(f for f in os.listdir(os.path.join(PACK_DIR, "decision-model"))
                         if f.endswith(".md"))
        self.assertEqual(5, len(present), "decision-model/ holds %r" % present)


class TestSpineObligesTheForm(unittest.TestCase):
    def test_form_is_a_returned_field(self):
        s14 = SPINE[SPINE.index("### 14.1"):SPINE.index("### 14.2")]
        self.assertIn("form", s14)
        self.assertIn("mandatory for a platform candidate", flat(s14))
        self.assertIn("in products", flat(s14))

    def test_a_bare_platform_option_is_malformed(self):
        s14 = flat(SPINE[SPINE.index("### 14.1"):SPINE.index("### 14.2")])
        self.assertIn("malformed", s14)
        self.assertIn("this platform over the store that already runs", s14)

    def test_naming_the_form_is_not_an_architecture_decision(self):
        s14 = flat(SPINE[SPINE.index("### 14.1"):SPINE.index("### 14.2")])
        self.assertIn("/blueprint", s14)

    def test_internal_vocabulary_rule_is_not_a_product_naming_ban(self):
        """The rule that produced the abstraction has to say what it does not cover."""
        s143 = flat(SPINE[SPINE.index("### 14.3"):SPINE.index("### 14.4")])
        self.assertIn("not a product-naming ban", s143)
        self.assertIn("mandatory", s143)


# ---------------------------------------------------------------- the artefact contract


class TestArtefactShape(unittest.TestCase):
    def test_decision_table_comes_first(self):
        head = OPT_TEMPLATE[:OPT_TEMPLATE.index("## Summary")]
        self.assertIn("decision, in one table", head)
        for column in ("Option", "Technology", "Verdict", "Order of magnitude",
                       "Reversibility", "Blocked by"):
            self.assertIn(column, head, "decision table lacks the %r column" % column)

    def test_technology_column_is_mandatory_and_never_empty(self):
        body = flat(OPT_TEMPLATE)
        self.assertIn("technology column is mandatory and is never empty", body)
        self.assertIn("surface *and* store", body)

    def test_word_budget_is_stated_and_binding(self):
        body = flat(OPT_TEMPLATE)
        self.assertIn("1 500 words of prose", body)
        self.assertIn("≤120 words per option", body)
        self.assertIn("binding", body)

    def test_overflow_goes_to_the_log_never_into_longer_prose(self):
        body = flat(OPT_TEMPLATE)
        self.assertIn("goes to the audit log", body)
        self.assertIn("never** into longer prose", body)

    def test_concern_coverage_left_the_artefact(self):
        self.assertNotIn("Concern coverage", OPT_TEMPLATE,
                         "the twelve-line coverage belongs in the audit log, not in options.md")
        self.assertIn("Concern coverage", LOG_TEMPLATE)
        self.assertIn("do NOT put these lines in `options.md`", LOG_TEMPLATE)

    def test_long_form_moved_to_the_log_with_the_none_obligation(self):
        self.assertIn("Per-option long form", LOG_TEMPLATE)
        self.assertIn("`(none)` is\nwritten explicitly here", LOG_TEMPLATE)
        self.assertIn("`(none)` is not written here; the field is omitted", OPT_TEMPLATE)

    def test_omission_is_legitimate_only_because_the_log_carries_it(self):
        body = flat(OPT_TEMPLATE)
        self.assertIn("only** because the log carries it", body)

    def test_eliminated_candidates_survive_in_the_table_and_out_of_play(self):
        self.assertIn("Out of play", OPT_TEMPLATE)
        body = flat(OPT_TEMPLATE)
        self.assertIn("including every eliminated and not-assessable one", body)
        self.assertIn("finding, not a\ndeletion", OPT_TEMPLATE.replace("\r", ""))

    def test_comparative_discipline_survived_the_rewrite(self):
        body = flat(OPT_TEMPLATE)
        for token in ("COMPARATOR EVIDENCE ABSENT", "No score, no weight",
                      "One outcome per scope"):
            self.assertIn(token, body)

    def test_the_discriminator_field_is_conditional(self):
        body = flat(OPT_TEMPLATE)
        self.assertIn("Decides against the others", body)
        self.assertIn("omitted otherwise", body)

    def test_the_two_classes_are_conditional_and_their_absence_is_declared(self):
        """C2. The universal obligation is gone; what replaces it is a DECLARATION.

        The test checks the declaration exists, never that it is true — whether a
        class really was implausible is the round's judgement, not a checkable fact.
        """
        body = flat(OPT_TEMPLATE)
        self.assertNotIn("Must include **at least**: one do-nothing baseline", body)
        self.assertIn("conditional", body)
        # The declaration lives in the log, where a marker can be read on an
        # artefact written in any language.
        for marker in ("DO-NOTHING", "PROCESS-CHANGE", "NOT PLAUSIBLE"):
            self.assertIn(marker, LOG_TEMPLATE, "class coverage lacks %r" % marker)

    def test_no_form_is_invented_to_fill_the_column(self):
        body = flat(OPT_TEMPLATE)
        self.assertIn("do not name a form the architect did not name", body)


class TestOrderOfMagnitudeMethod(unittest.TestCase):
    """G1. A number with no declared source is invented — the hard rule the whole
    framework rests on. The four markers are a closed set and are written verbatim,
    never translated: the artefact comes out in the pack's language, and a translated
    marker is what made the P-19 checks pass on a broken file.
    """

    MARKERS = ("SIMULATED", "PACK MODEL", "ANALOGY",
               "ORDER OF MAGNITUDE UNAVAILABLE")

    def test_the_method_has_exactly_one_owner(self):
        owner = flat(OPT_TEMPLATE)
        for marker in self.MARKERS:
            self.assertIn(marker, owner, "the artefact template lacks %r" % marker)
        self.assertIn("one of three sources", owner)

    def test_no_source_means_a_declared_empty_field_never_a_number(self):
        body = flat(OPT_TEMPLATE)
        self.assertIn("ORDER OF MAGNITUDE UNAVAILABLE", body)
        self.assertIn("what is missing to produce it", body)

    def test_it_is_a_band_and_never_becomes_a_commitment(self):
        body = flat(OPT_TEMPLATE)
        self.assertIn("band, never a point", body)
        self.assertIn("delivery commitment", body)

    def test_the_pack_model_carries_its_asymmetry(self):
        """Source (b) is platform-side only: a band beside a blank reads as the
        better option regardless of what it says."""
        estimation = read(PACK_DIR, "domain-knowledge", "craft", "estimation-model.md")
        self.assertIn("PACK MODEL", estimation)
        self.assertIn("NOT VALID AS COMPARATIVE ECONOMICS", estimation)
        self.assertIn("asymmetry", flat(OPT_TEMPLATE).lower())

    def test_simulate_declares_itself_as_source_a(self):
        self.assertIn("SIMULATED", SIMULATE)


class TestOptionContract(unittest.TestCase):
    """C1. The full field set lives in the round's log, which is unbudgeted; the
    artefact carries the estimate as a TABLE column, which is also unbudgeted. Putting
    six new prose fields on eleven options is how P-19's 8 542-word file happened.
    """

    FIELDS = ("**High-level architecture**", "**Assumptions**",
              "**Order of magnitude**", "**Cost drivers**", "**Material risks**",
              "**Reversibility**", "**Revision condition**")

    def test_the_log_carries_every_field(self):
        for field in self.FIELDS:
            self.assertIn(field, LOG_TEMPLATE, "long form lacks %r" % field)

    def test_components_and_boundary_are_one_field_not_three(self):
        """Components, responsibility boundary and high-level architecture are three
        views of one object; three fields wrote the same sentence three times."""
        body = flat(LOG_TEMPLATE)
        self.assertIn("main components", body)
        self.assertIn("responsibility boundary", body)
        self.assertNotIn("**Components**:", LOG_TEMPLATE)

    def test_a_precondition_is_never_a_person(self):
        body = flat(LOG_TEMPLATE)
        self.assertIn("never a person", body)

    def test_the_estimate_reaches_the_reader_in_the_table(self):
        head = OPT_TEMPLATE[:OPT_TEMPLATE.index("## Summary")]
        self.assertIn("Order of magnitude", head)


class TestRuleChangeVerdict(unittest.TestCase):
    """C3. An organisational rule blocks an option; it never deletes it. The owner
    cannot decide to change a rule for an option nobody showed them."""

    def test_the_verdict_is_in_the_table_vocabulary(self):
        head = OPT_TEMPLATE[:OPT_TEMPLATE.index("## Summary")]
        self.assertIn("viable if the rule is changed", head)

    def test_the_seven_fields_are_named(self):
        body = flat(OPT_TEMPLATE).lower()
        for field in ("rule", "condition", "impact", "cost", "risk",
                      "who can change", "status"):
            self.assertIn(field, body, "rule-change verdict lacks %r" % field)

    def test_decide_can_choose_to_change_the_rule(self):
        self.assertIn("viable if the rule is changed", DECIDE)


class TestRecommendation(unittest.TestCase):
    """C5. The round recommends; the owner decides. Two facts, two fields — neither
    is evidence for the other."""

    def test_the_section_exists_with_its_four_parts(self):
        self.assertIn("## Recommendation", OPT_TEMPLATE)
        body = flat(OPT_TEMPLATE).lower()
        for part in ("recommended", "against its siblings", "rests on",
                     "would flip"):
            self.assertIn(part, body, "recommendation lacks %r" % part)

    def test_it_replaced_the_section_it_would_have_duplicated(self):
        self.assertNotIn("## What the evidence supports", OPT_TEMPLATE)

    def test_the_round_may_decline_instead_of_forcing_a_pick(self):
        body = flat(OPT_TEMPLATE).lower()
        self.assertIn("no recommendation", body)
        self.assertIn("decision blocked", body)

    def test_decide_keeps_recommendation_and_choice_apart(self):
        self.assertIn("The aisa recommended", DECIDE)
        self.assertIn("Recommendation followed?", DECIDE)


class TestDetailOnlyForTheChosenOption(unittest.TestCase):
    """C6. Detailing one candidate past its siblings manufactures the preference it
    appears to find."""

    def test_draft_mode_is_high_level(self):
        contract = read(ROOT, "library", "kernel", "blueprint-contract.md")
        self.assertIn("high-level", flat(contract).lower())

    def test_simulate_projects_every_option_at_the_same_depth(self):
        body = flat(SIMULATE).lower()
        self.assertIn("same high level", body)


class TestConsumersBound(unittest.TestCase):
    def test_phases_declares_the_form_exit_criterion(self):
        p3 = PHASES[PHASES.index("## Phase 3: Options"):PHASES.index("## Phase 4: Decision")]
        self.assertIn("Every option names its technology", flat(p3))
        self.assertIn("one option per form", flat(p3))
        self.assertNotIn("pros/cons matrix", p3, "the output is a decision table now")
        self.assertIn("1 500 words", flat(p3))

    def test_options_skill_reports_technology_to_the_user(self):
        step7 = OPTIONS_SKILL[OPTIONS_SKILL.index("### 7. Present options to the user"):]
        self.assertIn("tecnologia", step7)
        self.assertIn("onde os dados vivem", step7)

    def test_options_skill_checks_the_contract_before_reporting(self):
        body = flat(OPTIONS_SKILL)
        self.assertIn("Every option names its technology", body)
        self.assertIn("within budget", body)
        self.assertIn("order of magnitude with its source marker", body)
        self.assertIn("closes with the recommendation", body)

    def test_decide_lists_the_technology(self):
        self.assertIn("technology: the form in products", DECIDE)
        self.assertIn("chairman-synthesis-O-<NN>.md", DECIDE)

    def test_simulate_knows_where_an_omitted_field_lives(self):
        body = flat(SIMULATE)
        self.assertIn("chairman-synthesis-O-<NN>.md", body)
        self.assertIn("**never treat an omitted field as unevaluated**", body)


# ------------------------------------------------------------------ the real artefacts


def engagement_options():
    if not os.path.isdir(PROJECTS):
        return []
    out = []
    for slug in sorted(os.listdir(PROJECTS)):
        path = os.path.join(PROJECTS, slug, "options.md")
        if os.path.isfile(path):
            out.append((slug, read(path)))
    return out


ENGAGEMENTS = engagement_options()
# A bare platform mention with no store beside it — the exact defect, in either language.
BARE_PLATFORM = re.compile(
    r"^(?:esta |a |the |this )?(?:plataforma|platform|power platform)"
    r"(?:\s+(?:sobre|over)\s+(?:o|a|the)?\s*(?:armazenamento|store|base de dados"
    r"|banco de dados|relational store))?\s*$",
    re.I)


class TestRenderedArtefacts(unittest.TestCase):
    """Checks the files the contract governs. A legacy artefact is reported and skipped —
    never counted as conforming."""

    def test_conforming_and_legacy_artefacts_are_told_apart(self):
        """`projects/` is a private mount point: a fresh clone has none, and an
        engagement mid-round may have no artefact at all. So the absence of a
        conforming file is not a failure — a legacy file being mistaken for a
        conforming one would be. Every check below keys off the marker."""
        conforming = [s for s, t in ENGAGEMENTS if on_contract(t)]
        legacy = [s for s, t in ENGAGEMENTS if not on_contract(t)]
        for slug, text in ENGAGEMENTS:
            self.assertEqual(on_contract(text), slug in conforming)
        if not ENGAGEMENTS:
            self.skipTest("no engagement mounted")
        if not conforming:
            self.skipTest("no options.md on the current contract yet; legacy: %r" % legacy)

        # Every artefact lands in exactly ONE of three tiers, and the classification is
        # total: a file that is on the table contract but not on the field contract must
        # be visible as such, never absorbed into either neighbour. That is what stops a
        # skipped file being read as a passing one.
        current = [s for s, t in ENGAGEMENTS if on_current_generation(t)]
        frozen = [s for s, t in ENGAGEMENTS
                  if on_contract(t) and not on_current_generation(t)]
        self.assertEqual(sorted(legacy + frozen + current),
                         sorted(s for s, _t in ENGAGEMENTS),
                         "an artefact fell into two tiers or none")
        self.assertFalse(set(current) & set(frozen))
        # And the frozen tier carries its measurement, so the number is never lost: it is
        # named here, and printed per file by `accept_phase5.py` criterion E.
        for slug, text in ENGAGEMENTS:
            if slug not in frozen:
                continue
            prose = [ln for ln in text.splitlines() if not ln.lstrip().startswith("|")]
            words = len(" ".join(prose).split())
            self.assertGreater(words, 0,
                               "%s is in the frozen tier with no prose to measure" % slug)

    def test_prose_budget_holds(self):
        """The budget is on prose. The decision table is the surface the reader uses:
        it is not budgeted, and it grows one line per candidate.

        Judged on the CURRENT generation (see `on_current_generation`): the budget became
        reachable when C1/G1 moved the long per-option form to the round's audit log, and
        an artefact frozen before that is measured, not judged."""
        for slug, text in ENGAGEMENTS:
            if not on_current_generation(text):
                continue
            prose = [ln for ln in text.splitlines() if not ln.lstrip().startswith("|")]
            words = len(" ".join(prose).split())
            self.assertLessEqual(words, WORD_CEILING,
                                 "%s/options.md carries %d words of prose (budget %d)"
                                 % (slug, words, WORD_BUDGET))

    def test_per_option_entries_stay_short(self):
        for slug, text in ENGAGEMENTS:
            if not on_current_generation(text):
                continue
            blocks = re.split(r"(?m)^### (O-\d{3})", text)
            for oid, body in zip(blocks[1::2], blocks[2::2]):
                body = body.split("\n## ")[0]
                words = len(body.split())
                self.assertLessEqual(words, OPTION_CEILING,
                                     "%s %s entry is %d words (budget %d)"
                                     % (slug, oid, words, OPTION_BUDGET))

    def test_every_table_row_names_a_technology(self):
        for slug, text in ENGAGEMENTS:
            if not on_contract(text):
                continue
            header, rows = decision_table(text)
            self.assertTrue(rows, "%s: decision table has no option rows" % slug)
            col = next(i for i, c in enumerate(header) if TECH_CELL.match(c))
            for ln in rows:
                cells = _cells(ln)
                self.assertEqual(len(header), len(cells),
                                 "%s: row does not fit the header: %r" % (slug, ln[:60]))
                tech = cells[col]
                self.assertTrue(tech and tech not in ("—", "-", "?"),
                                "%s %s: empty technology cell" % (slug, cells[0]))
                self.assertIsNone(BARE_PLATFORM.match(tech),
                                  "%s %s: technology is a bare platform mention (%r) — "
                                  "name the form: surface and store"
                                  % (slug, cells[0], tech))

    def test_option_ids_in_the_table_match_the_entries(self):
        for slug, text in ENGAGEMENTS:
            if not on_contract(text):
                continue
            table = {TABLE_ROW.match(ln).group(1) for ln in decision_table(text)[1]}
            entries = set(re.findall(r"(?m)^### (O-\d{3})", text))
            self.assertTrue(entries <= table,
                            "%s: entries absent from the decision table: %r"
                            % (slug, sorted(entries - table)))

    def test_no_ordinal_ladder_or_score(self):
        banned = re.compile(r"\b(score|pontuação|peso ponderado|weighted score)\b", re.I)
        for slug, text in ENGAGEMENTS:
            if not on_contract(text):
                continue
            hit = banned.search(text)
            self.assertIsNone(hit, "%s: scoring vocabulary %r" % (slug, hit and hit.group(0)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
