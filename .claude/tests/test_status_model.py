"""Step A0 — the deterministic half of `/status` (docs/STATUS_IMPROVEMENT_PLAN.md).

Covers the scenarios that plan marks **M** (mechanically verifiable) in section 9.
The S scenarios are semantic and are validated in step C against working copies of
real engagements; searching for phrases in a SKILL.md would not prove them.

Fixtures are SYNTHETIC and built in a tempdir by `mk_eng()` below: engagement
content lives in `projects/`, which is a gitignored mount point to the private
engagement repo, so no real engagement may be committed here as a fixture. Each
scenario therefore carries the smallest tree that exercises it, and reads as its
own documentation.

    python .claude/tests/test_status_model.py
"""

import importlib.util
import io
import json
import os
import shutil
import tempfile
import unittest
from datetime import date
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TODAY = date(2026, 9, 7)


def load_dashboard():
    path = os.path.join(ROOT, "library", "kernel", "tools", "dashboard.py")
    spec = importlib.util.spec_from_file_location("aisa_dashboard_status", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


D = load_dashboard()


# ------------------------------------------------------------------- fixtures

SU_HEAD = """# Shared Understanding — {slug}

> Engagement: {slug}
> Fase actual: {phase}

"""

SU_COLS = {
    "Confirmed": "| id | lens | claim | evidência | verificado_em | validade | ronda |",
    "Assumed": "| id | lens | claim | base da assumption | verificado_em | validade | ronda |",
    "Unknown": ("| id | lens | pergunta | quem responde | criticidade | custo | "
                "swing | ronda |"),
    "Conflicted": "| id | lens | conflito | partes | criticidade | ronda |",
    "Risky": "| id | lens | risco | impacto | mitigação proposta | ronda |",
}


def write(path, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    with io.open(path, "w", encoding="utf-8") as fh:
        fh.write(body)


def su(slug, phase, sections):
    """sections: {"Unknown": [[...cells...], ...], ...} -- cells without pipes."""
    out = [SU_HEAD.format(slug=slug, phase=phase)]
    for name in ("Confirmed", "Assumed", "Unknown", "Conflicted", "Risky"):
        out.append("## " + name + "\n")
        out.append(SU_COLS[name])
        out.append("|" + "|".join(["---"] * (SU_COLS[name].count("|") - 1)) + "|")
        for cells in sections.get(name, []):
            out.append("| " + " | ".join(str(c) for c in cells) + " |")
        out.append("")
    return "\n".join(out) + "\n"


# What each phase expects on disk (dashboard.EXPECTED_BY_PHASE). A tree missing
# these legitimately reports "retomar a fase", which would mask every phase rule
# under test, so mk_eng supplies them unless a scenario overrides one.
PHASE_BASELINE = {
    "framing": {"frame.md": "# Frame\n"},
    "options": {"frame.md": "# Frame\n",
                "options.md": "# Options\n"},
    "decision": {"frame.md": "# Frame\n",
                 "options.md": "# Options\n",
                 "decisions.md": "# Decisions\n",
                 "_synthesis/business-story.md": "# Business story\n"},
}


def mk_eng(tmp, slug="fx", phase="decision", files=None, sections=None, state=None,
           baseline=True):
    eng = Path(tmp) / slug
    eng.mkdir(parents=True, exist_ok=True)
    st = {"engagement": slug, "pack": "pp", "phase": phase, "round": "D-01",
          "aisa_version": "0.1.0", "created": "2026-09-01T00:00:00Z"}
    st.update(state or {})
    write(eng / "_state.json", json.dumps(st))
    write(eng / "context.json",
          json.dumps({"literal_request": "x", "requester": {"name": "n", "role": "r"}}))
    write(eng / "shared-understanding.md", su(slug, phase, sections or {}))
    tree = dict(PHASE_BASELINE.get(phase, {})) if baseline else {}
    tree.update(files or {})
    for rel, body in tree.items():
        write(eng / rel, body)
    return eng


def model(eng):
    return D.build_model(eng, TODAY)


# The two D-NNN roles the kernel gives the same shape. Tripwires belong to the
# solution decision; the approvals that follow carry none.
DECISIONS_SOLUTION_THEN_APPROVALS = """# Decisions — fx

## D-001 — Frame agreed

- **Timestamp**: 2026-09-01T10:00:00Z

## D-002 — Adopt O-004 — plataforma purpose-built

- **Chosen option**: O-004
- **Revision conditions / Tripwires (estruturados)**:
  - TW-1: Se o esforço de build ultrapassar o período estimado → parar (fonte: R-010)
  - TW-2: Se U-025 continuar aberta ao arranque → reavaliar
  - (Os outros candidatos do premortem — X-006, R-012 — foram considerados e NÃO
    adoptados como tripwires formais nesta decisão; continuam nas suas rows SU.)
- **Timestamp**: 2026-09-02T10:00:00Z

## D-003 — Blueprint bp-v01 aprovado

- **Timestamp**: 2026-09-03T10:00:00Z

## D-004 — Blueprint bp-v02 aprovado

- **Timestamp**: 2026-09-04T10:00:00Z
"""

BP_WITH_STRUCTURAL = """version: v03
engagement: fx
decision_ref: decisions.md#D-002
draft: false
architecture:
  scope: "whole solution"
  authorization: authorized
  authorization_basis: "outcome sentence, verbatim (fixture)"
  architectability_basis: "PP application built from scratch (fixture)"
  experience:
    mode: owned-internal
    primary_surface: "Record-centric app (model-driven)"
  record_authority: []
  compositions: []
  relocated_responsibilities: []
  proof_obligations:
    - claim: "Inspecção do arranjo efectivo; resultado entra no SU via /answer U-036"
      level: V1
      method: "inspecção documental com o IT"
      owner: "IT centralizado"
      funded: false
  open_architecture_choices:
    - choice: "Mecanismo de acesso a dados por domínio e o seu fit"
      structural: true
      would_be_settled_by: >
        O mecanismo por domínio estabelecido por base B e o fit registado
        por domínio. A conectividade por si não fecha nada.
      su_ref: U-032
    - choice: "Ponto de imposição da autorização"
      structural: true
      would_be_settled_by: "U-036 confirmada pelo IT"
      su_ref: U-036
      owner: not recorded
    - choice: "Dono do controlo de release"
      structural: false
      would_be_settled_by: "confirmação directa"
      su_ref: U-030
entities: []
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

BP_CLEAN_V02 = """version: v02
engagement: fx
decision_ref: decisions.md#D-002
draft: false
architecture:
  scope: "whole solution"
  authorization: authorized
  authorization_basis: "outcome sentence, verbatim (fixture)"
  architectability_basis: "PP application built from scratch (fixture)"
  experience:
    mode: owned-internal
    primary_surface: "Record-centric app (model-driven)"
  record_authority: []
  compositions: []
  relocated_responsibilities: []
  proof_obligations: []
  open_architecture_choices: []
entities: []
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

BP_V01 = BP_CLEAN_V02.replace("version: v02", "version: v01")


# --------------------------------------------------------------------- tests

class Harness(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="aisa-status-")
        self.addCleanup(shutil.rmtree, self.tmp, True)


class TestDecisionRoles(Harness):
    """A blueprint approval is not a solution decision, and tripwires live on
    the latter. Reading the LAST D-NNN block returns none for every engagement
    that approved a blueprint afterwards -- the defect this step fixes."""

    def _m(self):
        eng = mk_eng(self.tmp, files={
            "decisions.md": DECISIONS_SOLUTION_THEN_APPROVALS,
            "_blueprint/ux-blueprint_v01.yaml": BP_V01,
            "_blueprint/ux-blueprint_v02.yaml": BP_CLEAN_V02,
        }, sections={
            "Unknown": [["U-025", "governance", "pergunta", "sponsor", "Critical",
                         "reuniao", "decisivo: muda o branch", "R-01"]],
            "Risky": [["R-010", "business", "risco", "impacto", "mitigação", "R-01"]],
        })
        return model(eng)

    def test_roles_are_classified(self):
        st = self._m()["status"]
        kinds = {d["id"]: d["kind"] for d in st["decisions"]}
        self.assertEqual(kinds, {"D-001": "frame", "D-002": "solution",
                                 "D-003": "blueprint-approval",
                                 "D-004": "blueprint-approval"})

    def test_tripwires_come_from_the_solution_decision(self):
        tw = self._m()["status"]["tripwires"]
        self.assertEqual(tw["source_decision"], "D-002")
        self.assertEqual(tw["source_kind"], "solution")
        self.assertEqual(tw["total"], 2)
        self.assertEqual(tw["approvals_after"], ["D-003", "D-004"])

    def test_the_old_reader_is_the_one_that_loses_them(self):
        # Regression anchor: parse_tripwires reads the LAST block and finds none.
        # Kept so nobody "simplifies" the status layer back onto it.
        self.assertEqual(D.parse_tripwires(DECISIONS_SOLUTION_THEN_APPROVALS), [])

    def test_no_solution_decision_is_incomplete_never_ok(self):
        eng = mk_eng(self.tmp, slug="fx2", files={
            "decisions.md": "# Decisions\n\n## D-003 — Blueprint bp-v01 aprovado\n"})
        m = model(eng)
        self.assertEqual(m["status"]["tripwires"]["source_decision"], "")
        self.assertIn("verificação incompleta", m["status"]["tripwires"]["note"])
        self.assertTrue(any("decisão-solução" in d["message"]
                            for d in m["diagnostics"]))


class TestTripwireVerdictBoundary(Harness):
    """The motor reports evidence, never a verdict. 'no-evidence' must not be
    renderable as 'OK': whether a condition is evaluable at all is semantic."""

    def _tw(self):
        eng = mk_eng(self.tmp, files={
            "decisions.md": DECISIONS_SOLUTION_THEN_APPROVALS,
        }, sections={
            "Unknown": [["U-025", "governance", "p", "sponsor", "Critical", "reuniao",
                         "decisivo: x", "R-01"]],
            "Risky": [["R-010", "business", "r", "i", "m", "R-01"]],
        })
        return model(eng)["status"]["tripwires"]

    def test_watch_when_a_cited_row_is_open_critical(self):
        items = {t["tw"]: t for t in self._tw()["items"]}
        self.assertEqual(items["TW-2"]["status"], "watch")
        self.assertEqual([e["id"] for e in items["TW-2"]["evidence"]], ["U-025"])

    def test_no_evidence_is_not_ok(self):
        tw = self._tw()
        items = {t["tw"]: t for t in tw["items"]}
        # TW-1 cites R-010, which is neither Critical nor expired.
        self.assertEqual(items["TW-1"]["status"], "no-evidence")
        self.assertEqual(items["TW-1"]["evidence"], [])
        self.assertEqual(tw["verdict_owner"], "skill")
        self.assertIn("nunca 'OK'", tw["note"])

    def test_fired_is_never_emitted(self):
        blob = json.dumps(self._tw(), ensure_ascii=False)
        self.assertNotIn("fired", blob)
        self.assertNotIn('"ok"', blob.lower())

    def test_a_bullet_without_a_TW_id_is_never_numbered_into_one(self):
        # Found on the live pricing-marinha D-002: a note saying the other
        # premortem candidates were considered and deliberately NOT adopted was
        # auto-numbered TW-2, so the view announced a tripwire the decision
        # declined -- and reported it as "watch", since the note cites X-006.
        tw = self._tw()
        self.assertEqual([t["tw"] for t in tw["items"]], ["TW-1", "TW-2"])
        self.assertEqual(tw["total"], 2)
        self.assertNotIn("TW-3", json.dumps(tw, ensure_ascii=False))
        self.assertFalse(any("NÃO" in t["text"] for t in tw["items"]))

    def test_the_declined_note_is_reported_not_dropped(self):
        notes = self._tw()["unlabelled_notes"]
        self.assertEqual(len(notes), 1)
        self.assertIn("NÃO", notes[0])

    def test_a_cited_id_absent_from_the_su_is_reported_not_ignored(self):
        eng = mk_eng(self.tmp, slug="fx3", files={
            "decisions.md": DECISIONS_SOLUTION_THEN_APPROVALS})
        items = {t["tw"]: t for t in model(eng)["status"]["tripwires"]["items"]}
        self.assertEqual(items["TW-1"]["unresolvable_ids"], ["R-010"])


class TestBlueprintApproval(Harness):
    """blueprint-contract.md rule 5: a structural open choice blocks APPROVAL of a
    version, never its production. And an old approval does not cover a new version."""

    def _m(self):
        eng = mk_eng(self.tmp, files={
            "decisions.md": DECISIONS_SOLUTION_THEN_APPROVALS,
            "_blueprint/ux-blueprint_v01.yaml": BP_V01,
            "_blueprint/ux-blueprint_v02.yaml": BP_CLEAN_V02,
            "_blueprint/ux-blueprint_v03.yaml": BP_WITH_STRUCTURAL,
        }, sections={
            "Unknown": [
                ["U-032", "data", "mecanismo?", "IT / dono da BD", "Critical", "spike",
                 "decisivo: muda a arquitectura", "R-02"],
                ["U-036", "data", "identidade?", "IT centralizado", "Critical",
                 "documento", "decisivo: muda o ponto de imposição", "R-02"],
                ["U-030", "governance", "dono do release?", "", "Med", "email",
                 "cosmético: nada material", "R-02"],
                ["U-025", "governance", "p", "compliance-officer", "Critical",
                 "reuniao", "decisivo: x", "R-01"],
            ],
            "Risky": [["R-010", "business", "r", "i", "m", "R-01"]],
        })
        return model(eng)

    def test_approved_version_read_from_decisions_not_from_the_yaml(self):
        bp = self._m()["status"]["blueprint"]
        self.assertEqual(bp["approved"]["version"], "v02")
        self.assertEqual(bp["approved_by"], "D-004")

    def test_old_approval_does_not_cover_the_new_version(self):
        bp = self._m()["status"]["blueprint"]
        self.assertEqual(bp["current"]["version"], "v03")
        self.assertFalse(bp["approval_covers_current"])

    def test_structural_choices_block_approval_and_are_counted(self):
        bp = self._m()["status"]["blueprint"]
        self.assertEqual(bp["structural_open_count"], 2)
        self.assertEqual(sorted(r for c in bp["structural_open"] for r in c["su_refs"]),
                         ["U-032", "U-036"])

    def test_milestone_names_the_approval_block_not_render(self):
        ms = self._m()["status"]["milestone"]
        self.assertIn("aprovar blueprint v03", ms["marco"])
        self.assertIn("v02", ms["marco"])
        self.assertIn("regra 5", ms["text"])
        self.assertNotIn("/render", ms["command"])
        self.assertIn("/blueprint --refresh", ms["command"])
        self.assertEqual(sorted(ms["blocking"]), ["U-032", "U-036"])

    def test_a_non_structural_choice_does_not_block(self):
        items = {i["id"]: i for i in self._m()["status"]["items"]}
        self.assertFalse(items["U-030"]["blocks_approval"])

    def test_version_table_carries_per_version_structural_counts(self):
        vers = {v["version"]: v for v in self._m()["status"]["blueprint"]["versions"]}
        self.assertEqual(vers["v02"]["structural_open"], 0)
        self.assertEqual(vers["v03"]["structural_open"], 2)


class TestMalformedBlueprint(Harness):
    """An LIVE approved blueprint (`pricing-marinha` v05) fails yaml.safe_load. A
    strict parse would lose the whole record; the extractor keeps what is sound."""

    def test_a_malformed_sibling_section_does_not_destroy_the_needed_ones(self):
        broken = BP_WITH_STRUCTURAL + """  irreversible_choices:
    - choice: "a"
      fixed_as: "b"
    su_refs: [C-001]
      dangling: "this indentation is wrong on purpose"
"""
        eng = mk_eng(self.tmp, files={
            "decisions.md": DECISIONS_SOLUTION_THEN_APPROVALS,
            "_blueprint/ux-blueprint_v03.yaml": broken})
        bp = model(eng)["status"]["blueprint"]
        self.assertEqual(bp["structural_open_count"], 2)
        self.assertEqual(bp["current"]["authorization"], "authorized")
        self.assertEqual(len(bp["proof_obligations"]), 1)

    def test_an_approval_naming_a_missing_file_is_incomplete_not_silent(self):
        eng = mk_eng(self.tmp, files={
            "decisions.md": DECISIONS_SOLUTION_THEN_APPROVALS,
            "_blueprint/ux-blueprint_v01.yaml": BP_V01})
        m = model(eng)
        self.assertIsNone(m["status"]["blueprint"]["approved"])
        self.assertTrue(any("verificação incompleta" in d["message"]
                            for d in m["diagnostics"]))


class TestSynthesisAge(Harness):
    """Fixed 2026-09-07: approving a blueprint re-runs /synthesize, because
    architecture-story.md projects the APPROVED version's architecture block."""

    _n = 0

    def _mk(self, syn_when, complete=False):
        TestSynthesisAge._n += 1
        files = {
            "decisions.md": DECISIONS_SOLUTION_THEN_APPROVALS,
            "_blueprint/ux-blueprint_v01.yaml": BP_V01,
            "_blueprint/ux-blueprint_v02.yaml": BP_CLEAN_V02,
            "_synthesis/architecture-story.md": "# arch\n",
            "_synthesis/_synthesis-log.md":
                "# Synthesis Log\n\n{} — architecture-story — sources: x\n".format(
                    syn_when),
        }
        if complete:
            # P-18 / F04: "entregas" needs all five packs logged; one topic never
            # speaks for another, and a pack without a log line is unknown.
            topics = ["business-story", "as-is", "risks-and-assumptions",
                      "financial-story"]
            for t in topics:
                files["_synthesis/" + t + ".md"] = "# " + t + "\n"
            files["_synthesis/_synthesis-log.md"] += "".join(
                "{} — {} — sources: x\n".format(syn_when, t) for t in topics)
        return mk_eng(self.tmp, slug="fx-syn{}".format(TestSynthesisAge._n), files=files)

    def test_synthesis_before_the_approval_is_stale(self):
        st = model(self._mk("2026-09-03T12:00:00Z"))["status"]
        self.assertTrue(st["synthesis"]["stale_vs_approval"])
        self.assertEqual(st["synthesis"]["approval_id"], "D-004")
        self.assertEqual(st["milestone"]["command"], "/synthesize")

    def test_synthesis_after_the_approval_releases_the_deliverables(self):
        st = model(self._mk("2026-09-05T12:00:00Z", complete=True))["status"]
        self.assertFalse(st["synthesis"]["stale_vs_approval"])
        self.assertEqual(st["synthesis"]["verdict"], "fresh")
        self.assertEqual(st["milestone"]["command"], "/render --all")

    def test_a_fresh_architecture_story_alone_does_not_release_the_deliverables(self):
        # Only architecture-story is logged; business-story exists with no log line.
        st = model(self._mk("2026-09-05T12:00:00Z"))["status"]
        self.assertFalse(st["synthesis"]["stale_vs_approval"])
        self.assertEqual(st["synthesis"]["verdict"], "desconhecido")
        self.assertIn("business-story", st["synthesis"]["unknown_topics"])
        self.assertNotEqual(st["milestone"]["command"], "/render --all")
        self.assertIn("verificação incompleta", st["milestone"]["marco"])

    def test_no_approval_yet_means_no_staleness_claim(self):
        eng = mk_eng(self.tmp, slug="fx-noap", files={
            "decisions.md": "# D\n\n## D-002 — Adopt O-001\n\n- **Chosen option**: O-001\n",
            "_synthesis/architecture-story.md": "# a\n"})
        self.assertIsNone(model(eng)["status"]["synthesis"]["stale_vs_approval"])


class TestOwnerAndClosure(Harness):
    """Never invent a responsible party or a closure criterion; a council persona
    is a lens, not somebody who can be asked."""

    def _items(self):
        eng = mk_eng(self.tmp, phase="discovery", sections={"Unknown": [
            ["U-001", "business", "p1", "Pedro O. / compliance-officer", "Critical",
             "reuniao", "decisivo: elimina O-004", "R-01"],
            ["U-002", "data", "p2", "compliance-officer", "Critical", "reuniao",
             "decisivo: muda o branch", "R-01"],
            ["U-003", "user", "p3", "", "Med", "email", "", "R-01"],
        ]})
        return {i["id"]: i for i in model(eng)["status"]["items"]}

    def test_a_persona_is_separated_from_a_human(self):
        it = self._items()["U-001"]
        self.assertEqual(it["owner"]["humans"], ["Pedro O."])
        self.assertEqual(it["owner"]["personas"], ["compliance-officer"])
        self.assertFalse(it["owner"]["unassigned"])

    def test_a_persona_alone_is_unassigned_not_an_owner(self):
        it = self._items()["U-002"]
        self.assertEqual(it["owner"]["humans"], [])
        self.assertTrue(it["owner"]["unassigned"])

    def test_an_empty_owner_is_unassigned(self):
        self.assertTrue(self._items()["U-003"]["owner"]["unassigned"])

    def test_pre_blueprint_closure_falls_back_to_swing_and_says_so(self):
        it = self._items()["U-001"]
        self.assertEqual(it["closes_when"], "")
        self.assertIn("elimina O-004", it["closes_when_substitute"])
        self.assertIn("critério formal por definir", it["closes_when_source"])

    def test_a_structural_choice_supplies_the_real_criterion(self):
        eng = mk_eng(self.tmp, slug="fx-crit", files={
            "decisions.md": DECISIONS_SOLUTION_THEN_APPROVALS,
            "_blueprint/ux-blueprint_v03.yaml": BP_WITH_STRUCTURAL},
            sections={"Unknown": [
                ["U-032", "data", "p", "IT", "Critical", "spike", "decisivo: x", "R-02"]]})
        it = {i["id"]: i for i in model(eng)["status"]["items"]}["U-032"]
        self.assertIn("base B", it["closes_when"])
        self.assertIn("open_architecture_choices", it["closes_when_source"])
        self.assertEqual(it["closes_when_substitute"], "")

    def test_an_unrecorded_choice_owner_is_unassigned(self):
        eng = mk_eng(self.tmp, slug="fx-own", files={
            "decisions.md": DECISIONS_SOLUTION_THEN_APPROVALS,
            "_blueprint/ux-blueprint_v03.yaml": BP_WITH_STRUCTURAL},
            sections={"Unknown": [
                ["U-036", "data", "p", "IT", "Critical", "documento", "decisivo: x",
                 "R-02"]]})
        it = {i["id"]: i for i in model(eng)["status"]["items"]}["U-036"]
        obl = next(o for o in it["obligations"] if o["kind"] == "structural-choice")
        self.assertTrue(obl["owner"]["unassigned"])          # `owner: not recorded`

    def test_a_proof_owner_citation_does_not_become_an_open_item(self):
        # `owner: "IT centralizado (C-063)"` cites an id to identify a team.
        # Scanning it pulled Confirmed evidence rows in as if they were open work.
        bp = BP_WITH_STRUCTURAL.replace('owner: "IT centralizado"',
                                        'owner: "IT centralizado (C-063)"')
        eng = mk_eng(self.tmp, slug="fx-powner", files={
            "decisions.md": DECISIONS_SOLUTION_THEN_APPROVALS,
            "_blueprint/ux-blueprint_v03.yaml": bp,
        }, sections={
            "Confirmed": [["C-063", "governance", "IT central opera as integrações",
                           "kickoff", "2026-09-01", "organizacional", "R-01"]],
            "Unknown": [["U-036", "data", "identidade?", "IT", "Critical", "documento",
                         "decisivo: x", "R-02"]]})
        ids = {i["id"] for i in model(eng)["status"]["items"]}
        self.assertNotIn("C-063", ids)
        self.assertIn("U-036", ids)          # the id the proof's method names
        self.assertNotIn("U-032", ids)       # a su_ref with no row invents nothing

    def test_a_confirmed_fact_a_proof_cites_as_its_spec_is_not_open_work(self):
        bp = BP_WITH_STRUCTURAL.replace(
            'method: "inspecção documental com o IT"',
            'method: "provar o ciclo diário conforme C-070 e C-071"')
        eng = mk_eng(self.tmp, slug="fx-spec", files={
            "decisions.md": DECISIONS_SOLUTION_THEN_APPROVALS,
            "_blueprint/ux-blueprint_v03.yaml": bp,
        }, sections={"Confirmed": [
            ["C-070", "operations", "regra até/após", "docx", "2026-09-01",
             "organizacional", "R-01"],
            ["C-071", "operations", "quatro variantes", "docx", "2026-09-01",
             "organizacional", "R-01"]]})
        ids = {i["id"] for i in model(eng)["status"]["items"]}
        self.assertNotIn("C-070", ids)
        self.assertNotIn("C-071", ids)

    def test_an_expired_row_a_proof_cites_does_seed(self):
        bp = BP_WITH_STRUCTURAL.replace(
            'method: "inspecção documental com o IT"',
            'method: "provar o ciclo diário conforme C-070"')
        eng = mk_eng(self.tmp, slug="fx-spec2", files={
            "decisions.md": DECISIONS_SOLUTION_THEN_APPROVALS,
            "_blueprint/ux-blueprint_v03.yaml": bp,
        }, sections={"Confirmed": [
            ["C-070", "operations", "regra até/após", "docx", "2024-01-01",
             "organizacional", "R-01"]]})
        self.assertIn("C-070", {i["id"] for i in model(eng)["status"]["items"]})

    def test_evidence_of_a_confirmed_row_is_never_read_as_an_owner(self):
        # `quem responde` and `evidência` are the same parsed column; only
        # Unknown/Conflicted carry an owner there.
        eng = mk_eng(self.tmp, slug="fx-ev", files={
            "decisions.md": DECISIONS_SOLUTION_THEN_APPROVALS,
            "_blueprint/ux-blueprint_v03.yaml": BP_WITH_STRUCTURAL.replace(
                "su_ref: U-032", "su_ref: C-001")},
            sections={"Confirmed": [
                ["C-001", "data", "claim", "kickoff [00:12] Pedro", "2026-09-01",
                 "organizacional", "R-01"]]})
        it = {i["id"]: i for i in model(eng)["status"]["items"]}["C-001"]
        self.assertTrue(it["owner"]["unassigned"])
        self.assertEqual(it["owner"]["raw"], "")


class TestGroupingAndOrder(Harness):
    """One item per SU id (plan section 3), with the distinct obligations kept."""

    def _st(self):
        eng = mk_eng(self.tmp, files={
            "decisions.md": DECISIONS_SOLUTION_THEN_APPROVALS,
            "options.md": "# Options\n\nO-004 depende de U-036 e U-025.\n",
            "_blueprint/ux-blueprint_v03.yaml": BP_WITH_STRUCTURAL,
        }, sections={"Unknown": [
            ["U-036", "data", "identidade?", "IT", "Critical", "documento",
             "decisivo: muda o ponto de imposição", "R-02"],
            ["U-032", "data", "mecanismo?", "IT", "Critical", "spike",
             "dimensionante: muda o esforço", "R-02"],
            ["U-025", "governance", "p", "sponsor", "Critical", "reuniao",
             "decisivo: x", "R-01"],
            ["U-050", "user", "p", "sponsor", "Low", "email", "cosmético: nada",
             "R-02"],
        ]})
        return model(eng)["status"]

    def test_one_item_per_id_with_every_obligation_kept(self):
        items = self._st()["items"]
        self.assertEqual(len(items), len({i["id"] for i in items}))
        u036 = next(i for i in items if i["id"] == "U-036")
        self.assertEqual(sorted(o["kind"] for o in u036["obligations"]),
                         ["proof-obligation", "structural-choice"])
        self.assertEqual(u036["agenda"], "outro_canal")
        self.assertIn("options.md", u036["cited_by"])

    def test_a_citation_by_the_phase_artefact_seeds_an_actionable_row(self):
        # The item set is: material rows (Critical / expired / Risky) + the whole
        # agenda (every open Unknown lands in one of its buckets) + blueprint and
        # tripwire references + actionable rows the phase artefact cites. A Med
        # `Conflicted` row belongs to none of those until something cites it.
        eng = mk_eng(self.tmp, slug="fx-cite", phase="options",
                     files={"options.md": "# Options\n\nO-001 tropeça em X-010.\n"},
                     sections={"Conflicted": [
                         ["X-010", "data", "conflito", "A vs B", "Med", "R-02"],
                         ["X-011", "data", "conflito", "C vs D", "Med", "R-02"]]})
        items = {i["id"]: i for i in model(eng)["status"]["items"]}
        self.assertIn("X-010", items)                    # cited -> material
        self.assertNotIn("X-011", items)                 # neither cited nor Critical
        self.assertIn("options.md", items["X-010"]["cited_by"])

    def test_every_open_unknown_stays_visible_through_the_agenda(self):
        eng = mk_eng(self.tmp, slug="fx-ag", phase="discovery", sections={"Unknown": [
            ["U-070", "user", "p", "sponsor", "Low", "email", "cosmético: nada",
             "R-02"]]})
        items = {i["id"]: i for i in model(eng)["status"]["items"]}
        self.assertEqual(items["U-070"]["agenda"], "nao_gastar")

    def test_a_confirmed_row_cited_in_a_justification_is_not_an_open_item(self):
        eng = mk_eng(self.tmp, slug="fx-conf", files={
            "decisions.md": (DECISIONS_SOLUTION_THEN_APPROVALS
                             + "\nJustifica-se por C-001.\n"),
        }, sections={"Confirmed": [
            ["C-001", "data", "c", "e", "2026-09-01", "organizacional", "R-01"]]})
        self.assertNotIn("C-001", {i["id"] for i in model(eng)["status"]["items"]})

    def test_a_tripwire_citation_is_recorded_on_the_item(self):
        u025 = next(i for i in self._st()["items"] if i["id"] == "U-025")
        self.assertIn("TW-2 (D-002)", u025["cited_by"])

    def test_approval_blockers_come_first_then_criticidade_then_swing(self):
        ids = [i["id"] for i in self._st()["items"]]
        self.assertEqual(ids[:2], ["U-036", "U-032"])   # blockers, decisivo first
        self.assertEqual(ids[-1], "U-050")

    def test_every_material_blocker_is_present_even_beyond_three(self):
        st = self._st()
        self.assertGreaterEqual(len([i for i in st["items"]
                                     if i["criticidade"] == "Critical"]), 3)
        self.assertEqual(len(st["milestone"]["blocking"]), 2)
        # the ids the command names are the ones priority picked
        self.assertIn("U-036", st["milestone"]["command"])

    def test_an_open_critical_conflicted_row_is_never_dropped(self):
        # Regression: seeding items from meeting_agenda() alone lost every open
        # Critical `Conflicted` row, because the agenda is built from Unknowns.
        # Found on a working copy of a live Discovery engagement, not in a fixture.
        eng = mk_eng(self.tmp, slug="fx-confl", phase="discovery", sections={
            "Unknown": [["U-001", "b", "p", "s", "Critical", "reuniao", "decisivo: x",
                         "R-01"]],
            "Conflicted": [["X-001", "data", "conflito", "A vs B", "Critical", "R-01"],
                           ["X-002", "user", "conflito", "C vs D", "Med", "R-01"]],
            "Risky": [["R-001", "b", "risco", "impacto", "mitigação", "R-01"]],
        })
        st = model(eng)["status"]
        ids = {i["id"] for i in st["items"]}
        self.assertIn("X-001", ids)
        self.assertIn("R-001", ids)                      # Risky is material too
        self.assertIn("X-001", st["milestone"]["blocking"])
        # a Med row enters only when something material cites it, not by default
        self.assertNotIn("X-002", ids)

    def test_a_resolved_row_is_never_resurrected(self):
        eng = mk_eng(self.tmp, slug="fx-res", files={
            "decisions.md": DECISIONS_SOLUTION_THEN_APPROVALS,
            "_blueprint/ux-blueprint_v03.yaml": BP_WITH_STRUCTURAL,
        }, sections={"Unknown": [
            ["U-032", "data", "mecanismo?", "IT", "Critical", "spike",
             "decisivo: x", "R-02 — resolved → C-090"]]})
        st = model(eng)["status"]
        self.assertEqual([i["id"] for i in st["items"]], [])
        # the choice still blocks approval; it simply has no open row to hang on
        self.assertEqual(st["blueprint"]["structural_open_count"], 2)


class TestSimulationCoherence(Harness):
    """Coherence of a simulation is a mechanical check on the ids it cites, not a
    judgement about whether the comparison still reads well."""

    def test_a_simulation_citing_a_resolved_or_absent_id_is_stale(self):
        eng = mk_eng(self.tmp, phase="options", files={
            "_simulation/options-comparison_v01.md":
                "# sim\n\nO-004 assenta em U-032, U-070 e C-001.\n"},
            sections={"Unknown": [
                ["U-032", "data", "p", "IT", "Critical", "spike",
                 "decisivo: x", "R-02 — resolved → C-090"]],
                "Confirmed": [["C-001", "data", "c", "e", "2026-09-01",
                               "organizacional", "R-01"]]})
        sims = model(eng)["status"]["simulations"]
        self.assertEqual(len(sims), 1)
        self.assertEqual(sims[0]["cited_resolved"], ["U-032"])
        self.assertEqual(sims[0]["cited_absent"], ["U-070"])
        self.assertTrue(sims[0]["stale"])

    def test_no_simulation_directory_is_not_a_finding(self):
        self.assertEqual(model(mk_eng(self.tmp, slug="fx-nosim"))["status"]
                         ["simulations"], [])


class TestPhaseMilestones(Harness):
    """Plan section 5.1 as a table. The old fixed map sent a Decision engagement
    to `/render --all` with an unapproved blueprint."""

    def test_a_phase_missing_its_expected_artefact_says_so_first(self):
        eng = mk_eng(self.tmp, slug="fx-bare", baseline=False)
        ms = model(eng)["status"]["milestone"]
        self.assertIn("em falta", ms["marco"])
        self.assertIn("não existe", ms["text"])

    def test_it_names_the_command_that_produces_the_artefact_not_resume(self):
        # `/resume` re-invokes /status, which said `/resume`: a loop, not a step.
        # Found on working copies of a Framing and an Options engagement whose
        # phase was flipped in _state.json before the round wrote its artefact.
        for phase, missing, cmd in (("framing", "frame.md", "/frame"),
                                    ("options", "options.md", "/options")):
            base = dict(PHASE_BASELINE[phase])
            del base[missing]
            eng = mk_eng(self.tmp, slug="fx-noart-" + phase, phase=phase,
                         baseline=False, files=base)
            ms = model(eng)["status"]["milestone"]
            self.assertEqual(ms["command"], cmd, phase)
            self.assertNotIn("/resume", ms["command"], phase)
            self.assertEqual(ms["blocking"], [missing], phase)

    def test_discovery_with_a_critical_unknown_points_at_the_human(self):
        eng = mk_eng(self.tmp, phase="discovery", state={"round": "R-02"},
                     sections={"Unknown": [
                         ["U-001", "business", "p", "sponsor", "Critical", "reuniao",
                          "decisivo: x", "R-01"]]})
        ms = model(eng)["status"]["milestone"]
        self.assertIn("Discovery", ms["marco"])
        self.assertIn("/answer U-001", ms["command"])
        self.assertNotIn("/frame", ms["command"])

    def test_clean_discovery_is_ready_to_frame(self):
        eng = mk_eng(self.tmp, slug="fx-clean", phase="discovery",
                     state={"round": "R-02"})
        self.assertEqual(model(eng)["status"]["milestone"]["command"], "/frame")

    def test_decision_without_a_solution_decision_asks_for_one(self):
        eng = mk_eng(self.tmp, slug="fx-nodec", files={
            "decisions.md": "# D\n\n## D-001 — Frame agreed\n"})
        self.assertEqual(model(eng)["status"]["milestone"]["command"], "/decide")

    def test_authorized_without_a_blueprint_asks_for_one(self):
        eng = mk_eng(self.tmp, slug="fx-nobp", files={
            "decisions.md": DECISIONS_SOLUTION_THEN_APPROVALS.split("## D-003")[0]})
        self.assertEqual(model(eng)["status"]["milestone"]["command"], "/blueprint")

    def test_unauthorized_architecture_is_a_result_not_a_gap(self):
        eng = mk_eng(self.tmp, slug="fx-noauth", files={
            "decisions.md": DECISIONS_SOLUTION_THEN_APPROVALS.split("## D-003")[0],
            "_synthesis/architecture-story.md":
                "## Authorized scope and outcome basis\n\n`not-authorized`\n"})
        ms = model(eng)["status"]["milestone"]
        self.assertEqual(ms["command"], "/render --all")
        self.assertIn("não uma falha", ms["text"])


class TestReadToResume(Harness):
    """aisa-status step 8b, computed so /status and /resume cannot drift. The
    decision/architecture line gains options.md and answers.md (Step 8D §3)."""

    def test_decision_architecture_lists_options_and_answers(self):
        eng = mk_eng(self.tmp, files={
            "decisions.md": DECISIONS_SOLUTION_THEN_APPROVALS,
            "_blueprint/ux-blueprint_v01.yaml": BP_V01})
        r2r = model(eng)["status"]["read_to_resume"]
        paths = [e["path"] for e in r2r["entries"]]
        self.assertEqual(r2r["key"], "decision-architecture")
        self.assertIn("options.md", paths)
        self.assertIn("answers.md", paths)

    def test_decision_before_a_blueprint_uses_the_other_line(self):
        eng = mk_eng(self.tmp, slug="fx-pre", files={
            "decisions.md": DECISIONS_SOLUTION_THEN_APPROVALS.split("## D-003")[0]})
        self.assertEqual(model(eng)["status"]["read_to_resume"]["key"],
                         "decision-pre-blueprint")

    def test_material_rows_include_critical_expired_and_risky(self):
        eng = mk_eng(self.tmp, slug="fx-mat", phase="discovery", sections={
            "Unknown": [["U-001", "b", "p", "s", "Critical", "reuniao", "decisivo: x",
                         "R-01"]],
            "Risky": [["R-001", "b", "r", "i", "m", "R-01"]],
            "Confirmed": [["C-001", "b", "c", "e", "2020-01-01", "volatil", "R-01"]],
        })
        mats = model(eng)["status"]["read_to_resume"]["material_rows"]
        self.assertEqual(mats, ["C-001", "R-001", "U-001"])

    def test_it_is_derived_never_persisted(self):
        eng = mk_eng(self.tmp, slug="fx-der")
        model(eng)
        self.assertFalse((eng / "read-to-resume.md").exists())


class TestEpistemicsAndAbsence(Harness):
    """100% health is evidence in date, not readiness. Absent data is never a
    green light."""

    def test_full_health_with_open_unknowns_is_not_readiness(self):
        eng = mk_eng(self.tmp, phase="discovery", sections={
            "Confirmed": [["C-001", "b", "c", "e", "2026-09-01", "organizacional",
                           "R-01"]],
            "Unknown": [["U-001", "b", "p", "s", "Critical", "reuniao", "decisivo: x",
                         "R-01"]]})
        m = model(eng)
        self.assertEqual(m["health"]["pct"], 100)
        self.assertIn("/answer U-001", m["status"]["milestone"]["command"])

    def test_an_expired_row_is_material_never_declared_false(self):
        eng = mk_eng(self.tmp, slug="fx-exp", phase="discovery", sections={
            "Confirmed": [["C-001", "b", "c", "e", "2024-01-01", "organizacional",
                           "R-01"]]})
        m = model(eng)
        self.assertEqual(m["health"]["expired"], 1)
        self.assertIn("C-001", m["status"]["read_to_resume"]["material_rows"])
        self.assertNotIn("falso", json.dumps(m["revalidate"], ensure_ascii=False))

    def test_an_empty_engagement_produces_no_false_zeros(self):
        st = model(mk_eng(self.tmp, slug="fx-empty"))["status"]
        self.assertIsNone(st["blueprint"]["approval_covers_current"])
        self.assertIsNone(st["synthesis"]["stale_vs_approval"])
        self.assertIsNone(st["render"]["stale_vs_approval"])
        self.assertEqual(st["tripwires"]["total"], 0)
        self.assertIn("verificação incompleta", st["tripwires"]["note"])

    def test_a_legacy_su_with_no_swing_names_the_absent_criterion(self):
        # Pre-v2.3 SUs have no swing column, so there is no substitute criterion
        # either. Blank would read as "nothing to close".
        eng = mk_eng(self.tmp, slug="fx-nocrit", phase="discovery")
        io.open(eng / "shared-understanding.md", "w", encoding="utf-8").write(
            "# SU\n\n## Unknown\n\n| id | lens | pergunta | quem responde | "
            "criticidade | ronda |\n|---|---|---|---|---|---|\n"
            "| U-001 | business | p | sponsor | Critical | R-01 |\n")
        it = {i["id"]: i for i in model(eng)["status"]["items"]}["U-001"]
        self.assertEqual(it["closes_when"], "")
        self.assertEqual(it["closes_when_substitute"], "")
        self.assertIn("critério por definir", it["closes_when_source"])

    def test_no_solution_decision_is_only_a_finding_in_the_decision_phase(self):
        decisions = "# D\n\n## D-001 — Frame agreed\n\n- **Timestamp**: 2026-09-01T10:00:00Z\n"
        base = dict(PHASE_BASELINE["options"])
        base["decisions.md"] = decisions
        opts = mk_eng(self.tmp, slug="fx-optnodec", phase="options", files=base)
        self.assertFalse(any("decisão-solução" in d["message"]
                             for d in model(opts)["diagnostics"]))
        dec = mk_eng(self.tmp, slug="fx-decnodec", files={"decisions.md": decisions})
        self.assertTrue(any("decisão-solução" in d["message"]
                            for d in model(dec)["diagnostics"]))

    def test_a_legacy_su_still_yields_an_agenda(self):
        eng = mk_eng(self.tmp, slug="fx-legacy")
        io.open(eng / "shared-understanding.md", "w", encoding="utf-8").write(
            "# SU\n\n## Unknown\n\n| id | lens | pergunta | quem responde | "
            "criticidade | ronda |\n|---|---|---|---|---|---|\n"
            "| U-001 | business | p | sponsor | Critical | R-01 |\n")
        m = model(eng)
        self.assertEqual(m["su"]["schema_flavour"], "legacy")
        self.assertTrue(any(i["id"] == "U-001" for i in m["status"]["items"]))
        self.assertTrue(any("pre-v2.2" in d["message"] for d in m["diagnostics"]))


class TestRenderAge(Harness):
    def test_render_behind_the_current_blueprint_is_visible(self):
        eng = mk_eng(self.tmp, files={
            "decisions.md": DECISIONS_SOLUTION_THEN_APPROVALS,
            "_blueprint/ux-blueprint_v01.yaml": BP_V01,
            "_blueprint/ux-blueprint_v02.yaml": BP_CLEAN_V02,
            "_blueprint/ux-blueprint_v03.yaml": BP_WITH_STRUCTURAL,
            "_render/render-log.md":
                "# Render Log\n\n## 2026-09-04T12:00:00Z — `/render --all`\n\n"
                "- estimate v01 — 0 gaps. `operational_impact`: skip.\n",
        })
        r = model(eng)["status"]["render"]
        self.assertEqual(r["renders_blueprint_version"], "v02")
        self.assertEqual(r["current_blueprint_version"], "v03")
        self.assertTrue(r["behind_current_blueprint"])
        self.assertEqual(r["skip_mentions"], 1)


class TestMarkdownRenderProgress(Harness):
    """block_md() must consume at least one line per pass.

    Regression: a line starting with "|" that the table branch declined consumed
    nothing, so `while i < n` spun forever appending an empty paragraph until the
    process died of MemoryError — whose message is empty, so the tool printed
    "[dashboard] build falhou: " with no reason and replaced the page with an
    error page. Found on a live Discovery engagement after /capture regenerated
    process-model.md and the 220-line inline cap landed on a table header row,
    separating it from its separator row.

    Each case below hung indefinitely before the fix, so a timeout is the assertion.
    """

    CASES = {
        "table header at end of file": ("| a | b |", None),
        "table header then a blank line": ("| a | b |\n\ntexto", None),
        "table cut by max_lines": ("x\n| a | b |\n|---|---|\n| 1 | 2 |", 2),
        "orphan pipe line": ("antes\n\n| solto |\n\ndepois", None),
        "header with a missing separator row": ("| a | b |\n| 1 | 2 |", None),
    }

    def _render(self, md, cap):
        import threading
        box = {}

        def run():
            box["html"] = D.block_md(md, {}, max_lines=cap)

        t = threading.Thread(target=run, daemon=True)
        t.start()
        t.join(10)
        return box.get("html")

    def test_no_input_can_stall_the_renderer(self):
        for name, (md, cap) in self.CASES.items():
            html = self._render(md, cap)
            self.assertIsNotNone(html, "block_md stalled on: " + name)
            self.assertNotIn("<p></p>", html, name)

    def test_the_undecided_pipe_line_is_rendered_as_text_not_dropped(self):
        html = self._render("antes\n\n| solto |\n\ndepois", None)
        self.assertIn("| solto |", html)
        self.assertIn("antes", html)
        self.assertIn("depois", html)

    def test_a_well_formed_table_is_still_a_table(self):
        html = self._render("| a | b |\n|---|---|\n| 1 | 2 |", None)
        self.assertIn("<table>", html)
        self.assertIn("<th>a</th>", html)
        self.assertIn("<td>1</td>", html)

    def test_every_branch_advances_on_the_shapes_a_lens_writes(self):
        md = ("# H1\n\ntexto\n\n---\n\n> citação\n\n- item um\n- item dois\n\n"
              "```\ncode\n```\n\n| a | b |\n|---|---|\n| 1 | 2 |\n\n| orfã |\n")
        html = self._render(md, None)
        self.assertIsNotNone(html)
        for frag in ("<h3", "<hr>", "<blockquote>", "<ul>", "<pre><code>", "<table>"):
            self.assertIn(frag, html, frag)
        self.assertIn("| orfã |", html)      # the undecided line, rendered not dropped


class TestBackwardCompatibility(Harness):
    def test_the_html_page_still_builds(self):
        eng = mk_eng(self.tmp, files={
            "decisions.md": DECISIONS_SOLUTION_THEN_APPROVALS,
            "_blueprint/ux-blueprint_v03.yaml": BP_WITH_STRUCTURAL})
        html = D.render_html(model(eng), 0)
        self.assertIn("<html", html.lower())
        self.assertGreater(len(html), 10000)

    def test_next_action_mirrors_the_milestone(self):
        eng = mk_eng(self.tmp, slug="fx-mirror", files={
            "decisions.md": DECISIONS_SOLUTION_THEN_APPROVALS,
            "_blueprint/ux-blueprint_v03.yaml": BP_WITH_STRUCTURAL})
        m = model(eng)
        self.assertEqual(m["next_action"]["command"],
                         m["status"]["milestone"]["command"])

    def test_schema_version_was_bumped(self):
        self.assertGreaterEqual(D.SCHEMA_VERSION, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
