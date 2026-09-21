# -*- coding: utf-8 -*-
"""Step 8C — consolidated post-pilot runtime repair (pack pp 1.8.2).

Bounded fixtures + contract assertions for the five repairs decided in Step 8B and its
semantic-continuity addendum. Two kinds of test live here:

  * CONTRACT — the runtime text (skills, kernel template, orchestration) carries the rule.
  * FIXTURE  — a small reference evaluator, written here from the contract, is run over
    fixtures in `.claude/tests/fixtures/step8c/`. The evaluators are test instruments,
    not runtime: they prove the contract is decidable on the semantic shapes Pilot 1
    produced (and would have failed on). No runtime router, scorer or ledger is added.

Groups:
  TC-1..TC-5   technical-claim closure (PR-1)            fact != fit
  CS-1..CS-5   comprehension survival (PR-4/PR-8)        cross-source synopsis, disposition
  PMU-1..PMU-5 PM-U disposition (PR-2A)                  Critical PM-U never disappears silently
  FS-1..FS-5   Framing survival block (PR-5)             id-anchored projection, no new authority
  SI-1..SI-5   semantic invalidation (PR-7)              targeted revalidation, no graph
  C-057        regression fixture                        record authority moves -> revalidate, no reversal
  RH-1..RH-5   rehydration (PR-6)                        derived Read to resume, no transcript
  PM static    pricing-marinha static proof              chain, four units, BIOS, Simulador, Mon/Tue
  Guards       nothing forbidden was introduced

    python .claude/tests/test_step8c_semantic_continuity.py
"""

import io
import json
import os
import re
import tempfile
import unittest

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIX = os.path.join(ROOT, ".claude", "tests", "fixtures", "step8c")


def read(*parts):
    with io.open(os.path.join(ROOT, *parts), encoding="utf-8") as fh:
        return fh.read()


def fixture(name):
    with io.open(os.path.join(FIX, name), encoding="utf-8") as fh:
        return fh.read()


ANSWER = read(".claude", "skills", "aisa-answer", "SKILL.md")
BLUEPRINT = read(".claude", "skills", "aisa-blueprint", "SKILL.md")
CAPTURE = read(".claude", "skills", "aisa-capture", "SKILL.md")
ROUND = read(".claude", "skills", "aisa-round", "SKILL.md")
FRAME = read(".claude", "skills", "aisa-frame", "SKILL.md")
CHAIRMAN = read(".claude", "skills", "chairman-synthesis", "SKILL.md")
STATUS = read(".claude", "skills", "aisa-status", "SKILL.md")
ORCH = read("library", "kernel", "orchestration.md")
STATES = read("library", "kernel", "states.md")
PHASES = read("library", "kernel", "phases.md")
TEMPLATE = read("library", "kernel", "capture-templates", "process-model.template.md")
PACK_TEXT = read("library", "packs", "pp", "pack.yaml")
PACK = yaml.safe_load(PACK_TEXT)

SU_ID = re.compile(r"\b([CAUXR]-\d{3})\b")
MARKERS = ("OBSERVED", "INFERRED", "HYPOTHESIS", "UNKNOWN")


# =============================================================================================
# Reference evaluators (test instruments)
# =============================================================================================

def synopsis_lines(text):
    """Every marked synopsis line: (marker, label or None, citation-bearing?)."""
    out = []
    for line in text.splitlines():
        m = re.match(r"^- (OBSERVED|INFERRED|HYPOTHESIS|UNKNOWN)\b(.*)$", line.strip())
        if not m:
            continue
        marker, rest = m.group(1), m.group(2)
        # a MATERIAL line carries its label in backticks immediately after the marker
        label = re.match(r"^\s*—\s*`([^`]+)`", rest)
        cited = bool(re.search(r"PM-\d{3}|¶\d+|\[\d\d:\d\d:\d\d|![A-Z]+\d+|p\.\d+", rest))
        out.append((marker, label.group(1) if label else None, cited))
    return out


def material_labels(text):
    return {lab for _m, lab, _c in synopsis_lines(text) if lab}


def pmu_rows(text):
    rows = {}
    for line in text.splitlines():
        m = re.match(r"^\|\s*(PM-U-\d{3})\s*\|(.*)$", line)
        if m:
            cells = [c.strip() for c in m.group(2).split("|")]
            rows[m.group(1)] = cells[3] if len(cells) > 3 else ""
    return rows


DISP = re.compile(
    r"^- (?:`(?P<label>[^`]+)`|(?P<pmu>PM-U-\d{3})) — "
    r"(?P<kind>MAP|ADOPT|DISMISS)"
    r"(?: (?P<map>[CAUXR]-\d{3})| → (?P<adopt>[CAUXR]-\d{3})| — (?P<reason>.+))?"
)


def dispositions(open_evidence_text):
    """Parse `Open evidence` disposition lines: subject -> (kind, target, reason)."""
    out = {}
    for line in open_evidence_text.splitlines():
        m = DISP.match(line.strip())
        if not m:
            continue
        subject = m.group("label") or m.group("pmu")
        target = m.group("map") or m.group("adopt")
        out[subject] = (m.group("kind"), target, (m.group("reason") or "").strip())
    return out


def undisposed(synopsis_text, pmu_text, disp):
    """What aisa-round step 5e reports: Critical PM-U + labelled material lines with no disposition."""
    missing = []
    for label in sorted(material_labels(synopsis_text)):
        if label not in disp:
            missing.append(label)
    for pmu, crit in sorted(pmu_rows(pmu_text).items()):
        if crit == "Critical" and pmu not in disp:
            missing.append(pmu)
    return missing


def disposition_defects(disp, su_ids):
    """MAP/ADOPT must point at a row that exists; DISMISS must carry a reason; one kind each."""
    defects = []
    for subject, (kind, target, reason) in disp.items():
        if kind in ("MAP", "ADOPT"):
            if not target or target not in su_ids:
                defects.append("%s: %s without an existing SU row (%s)" % (subject, kind, target))
        elif kind == "DISMISS" and not reason:
            defects.append("%s: DISMISS without a reason" % subject)
    return defects


def su_ids_of(su_text):
    ids = set()
    for line in su_text.splitlines():
        m = re.match(r"^\|\s*([CAUXR]-\d{3})\s*\|", line)
        if m:
            ids.add(m.group(1))
    return ids


def su_state_of(su_text, sid):
    section = None
    for line in su_text.splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
        if re.match(r"^\|\s*%s\s*\|" % re.escape(sid), line):
            return section
    return None


def survival_block(frame_text):
    """Parse `## What must survive into Options` -> {sub-list: [(id or None, text)]}."""
    m = re.search(r"^## What must survive into Options\s*$(.*?)(?=^## |\Z)", frame_text, re.M | re.S)
    if not m:
        return None
    block, out, current = m.group(1), {}, None
    for line in block.splitlines():
        if line.startswith("### "):
            current = line[4:].strip()
            out[current] = []
        elif line.startswith("- ") and current:
            entry = line[2:].strip()
            idm = re.match(r"^([CAUXR]-\d{3})\b", entry)
            out[current].append((idm.group(1) if idm else None, entry))
    return out


SURVIVAL_SUBLISTS = (
    "Process meaning",
    "Business invariants",
    "Structural constraints",
    "Decision-changing Unknowns",
    "Material scope / task obligations",
)


def survival_defects(frame_text, su_ids):
    """The frame may not create factual authority: every entry is an existing id or `(none) — reason`."""
    block = survival_block(frame_text)
    if block is None:
        return ["survival block absent"]
    defects = []
    for name in SURVIVAL_SUBLISTS:
        entries = block.get(name)
        if not entries:
            defects.append("%s: empty (write `(none) — <reason>`)" % name)
            continue
        for sid, text in entries:
            if sid:
                if sid not in su_ids:
                    defects.append("%s: %s is not an SU row — frame invents authority" % (name, sid))
            elif not re.match(r"^\(none\) — \S", text):
                defects.append("%s: entry without SU id and not `(none) — reason`: %r" % (name, text[:50]))
    return defects


# ---- Step 8C.1 — `(none)` validation under override -------------------------------------------

# synopsis dimension headings → the survival category their material lines project into
CATEGORY_DIMENSIONS = {
    "Process meaning": ("Purpose", "End-to-end flow", "Transformation / calculation stages",
                        "Intermediate state", "Decisions"),
    "Business invariants": ("Business invariants",),
    "Structural constraints": ("Structural constraints",),
    "Decision-changing Unknowns": (),      # from the SU: open Unknown rows with `swing: decisivo`
    "Material scope / task obligations": ("Outputs and consumers", "Material user tasks",
                                          "Exceptions and workarounds", "Variants"),
}
OVERRIDE_WORDS = re.compile(r"overrid|to proceed|gate|bypass", re.I)


def synopsis_by_dimension(text):
    """{dimension heading: [label, ...]} for the labelled (material) lines of a synopsis."""
    out, current = {}, None
    for line in text.splitlines():
        if line.startswith("### "):
            current = line[4:].strip()
            out.setdefault(current, [])
        elif current:
            m = re.match(r"^- (OBSERVED|INFERRED|HYPOTHESIS|UNKNOWN)\s*—\s*`([^`]+)`", line.strip())
            if m:
                out[current].append(m.group(2))
    return out


def decisive_unknowns(su_text):
    ids = set()
    section = None
    for line in su_text.splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
        m = re.match(r"^\|\s*(U-\d{3})\s*\|", line)
        if m and section == "Unknown" and "decisivo" in line and "resolved →" not in line:
            ids.add(m.group(1))
    return ids


def parse_gate_record(text):
    """The existing soft-gate output + D-001 override record, as aisa-frame prints them."""
    rec = {"result": "PASS", "missing": {}, "override": False, "reason": ""}
    for line in text.splitlines():
        s = line.strip()
        m = re.match(r"^gate:\s*(PASS|FAIL)", s)
        if m:
            rec["result"] = m.group(1)
        m = re.match(r"^missing understanding:\s*([^—]+?)\s*—\s*(.+)$", s)
        if m:
            rec["missing"].setdefault(m.group(1).strip(), []).append(m.group(2).strip())
        if re.match(r"^override:\s*YES", s) or re.match(r"^-\s*\*\*Override used at /frame\*\*:\s*(?!—\s*$)\S", s):
            rec["override"] = True
        m = re.match(r"^(?:override reason:|-\s*\*\*Override used at /frame\*\*:)\s*(.+)$", s)
        if m and m.group(1).strip() != "—":
            rec["reason"] = m.group(1).strip()
    return rec


def none_entry_defects(frame_text, su_text, synopsis_text, disp, gate_record):
    """Step 8C.1: `(none) — reason` is valid ONLY as a substantive conclusion —
    (1) category evaluated, (2) no known material SU item belongs to it, (3) no material synopsis line
    requiring disposition is unresolved for it, (4) no gate failure on it is hidden by the entry.
    Override ≠ evidence ≠ resolution ≠ absence."""
    block = survival_block(frame_text)
    if block is None:
        return ["survival block absent"]
    by_dim = synopsis_by_dimension(synopsis_text)
    defects = []
    for category in SURVIVAL_SUBLISTS:
        entries = block.get(category) or []
        none_entries = [t for sid, t in entries if sid is None and t.startswith("(none)")]
        if not none_entries:
            continue
        if not entries:                                     # (1) never evaluated
            defects.append("%s: not evaluated" % category)
        labels = [lab for dim in CATEGORY_DIMENSIONS[category] for lab in by_dim.get(dim, [])]
        known = {disp[lab][1] for lab in labels if lab in disp and disp[lab][0] in ("MAP", "ADOPT")}
        if category == "Decision-changing Unknowns":
            known |= decisive_unknowns(su_text)
        unresolved = [lab for lab in labels if lab not in disp]
        if known:                                           # (2)
            defects.append("%s: `(none)` while known material SU items exist (%s)"
                           % (category, ", ".join(sorted(known))))
        if unresolved:                                      # (3)
            defects.append("%s: `(none)` while material synopsis lines are undisposed (%s)"
                           % (category, ", ".join(unresolved)))
        if gate_record["missing"].get(category):            # (4)
            defects.append("%s: `(none)` hides a gate failure — %s"
                           % (category, "; ".join(gate_record["missing"][category])))
        for t in none_entries:
            if OVERRIDE_WORDS.search(t):
                defects.append("%s: override reason written as `(none)` reason: %r" % (category, t[:60]))
        if gate_record["override"] and gate_record["result"] == "FAIL" and \
                category in gate_record["missing"]:
            defects.append("%s: override may not stand in for the missing item" % category)
    return sorted(set(defects))


def survival_defects_full(frame_text, su_text, synopsis_text, disp, gate_record):
    """Base projection check + the Step 8C.1 `(none)` validation."""
    return survival_defects(frame_text, su_ids_of(su_text)) + \
        none_entry_defects(frame_text, su_text, synopsis_text, disp, gate_record)


# ---- PR-1 closure evaluator ------------------------------------------------------------------

def closure_verdict(basis, settles_named_fact, fit_recorded, tenant_dependent=False):
    """Encodes aisa-answer 4b / aisa-blueprint 11: (claim_state, structural_choice).

    basis: None | 'A' (RESEARCH/DK) | 'B' (engagement-verifiable) | 'C' (proof/measurement)
    """
    if basis is None:
        return ("Assumed-or-Unknown", "open")
    if tenant_dependent and basis == "A":
        return ("Unknown-verification-obligation", "open")
    if not settles_named_fact:
        return ("Confirmed-engagement-fact", "open")
    if not fit_recorded:
        return ("Confirmed-capability", "open")
    return ("Confirmed", "closed")


# ---- PR-7 dependents evaluator ---------------------------------------------------------------

FIELD_VOCAB = {
    "record_authority": ("store", "record authority", "autoridade"),
}


def changed_fields(prev, new):
    """Architecture-significant fields whose value changed between two versions."""
    changed = {}
    pa, na = prev["architecture"], new["architecture"]
    prev_ra = {d["domain"]: (d["authority"], d["access_mode"]) for d in pa.get("record_authority", [])}
    new_ra = {d["domain"]: (d["authority"], d["access_mode"]) for d in na.get("record_authority", [])}
    diff = [dom for dom in new_ra if prev_ra.get(dom) != new_ra[dom]]
    if diff:
        changed["record_authority"] = diff
    if pa["experience"].get("primary_surface") != na["experience"].get("primary_surface") or \
            pa["experience"].get("mode") != na["experience"].get("mode"):
        changed["experience"] = True
    prev_c = {c["component"]: c["pattern"] for c in pa.get("compositions", [])}
    new_c = {c["component"]: c["pattern"] for c in na.get("compositions", [])}
    if prev_c != new_c:
        changed["compositions"] = sorted(set(prev_c) ^ set(new_c) | {k for k in new_c if prev_c.get(k) != new_c[k]})
    return changed


def dependents_of_record_authority_change(prev, new, decisions_text, options_text):
    """What aisa-blueprint 11b must list when record authority moves. Uses ONLY existing references:
    su_refs overlap, rationale/forced_by prose naming the field's vocabulary, decision clauses and option
    strengths sharing that vocabulary. No graph, no depends_on."""
    pa, na = prev["architecture"], new["architecture"]
    changed_domains = changed_fields(prev, new).get("record_authority", [])
    if not changed_domains:
        return {"conclusions": [], "decision_layer": [], "route": None}
    changed_refs = set()
    for d in pa["record_authority"]:
        if d["domain"] in changed_domains:
            changed_refs.update(d.get("su_refs", []))
    vocab = FIELD_VOCAB["record_authority"]
    conclusions = []
    # (a) prose in the previous version naming the field's property
    rationale = pa["experience"].get("rationale", "")
    if any(v in rationale.lower() for v in vocab):
        conclusions.append("experience.rationale — surface basis (%s)" % pa["experience"]["primary_surface"])
        if "security" in rationale.lower() or "segurança" in rationale.lower():
            conclusions.append("security basis — row/column security inherited from the store")
        if "audit" in rationale.lower() or "auditoria" in rationale.lower():
            conclusions.append("audit basis — audit inherited from the store")
    # (b) su_refs overlap on other fields
    for c in pa.get("compositions", []):
        if set(c.get("su_refs", [])) & changed_refs or any(v in c.get("forced_by", "").lower() for v in vocab):
            conclusions.append("composition %s — pattern %s" % (c["component"], c["pattern"]))
    # (c) composition set / pattern change itself is a conclusion to revalidate
    for comp in changed_fields(prev, new).get("compositions", []):
        conclusions.append("composition %s — access pattern over the moved store" % comp)
    conclusions.append("record_authority.access_mode — mechanism per domain (%s)" % ", ".join(changed_domains))
    # (d) decision layer: option strengths and decision clauses sharing the dependent vocabulary
    decision_layer = []
    words = []
    if any("audit" in c for c in conclusions):
        words += ["audit", "auditab"]
    if any("security" in c for c in conclusions):
        words += ["security", "segurança"]
    for line in options_text.splitlines():
        if "strengths" in line.lower() and any(w in line.lower() for w in words):
            decision_layer.append("options.md#O-004 strengths — %s" % ", ".join(w for w in words if w in line.lower()))
    for line in decisions_text.splitlines():
        low = line.lower()
        if ("justification" in low or "conditions" in low or low.strip().startswith("- audit")) and \
                any(w in low for w in words):
            decision_layer.append("decisions.md#D-002 — %s" % line.strip()[:60])
    route = "tripwire check → /revisit" if decision_layer else None
    return {"conclusions": conclusions, "decision_layer": decision_layer, "route": route}


def revalidation_recorded(new, conclusions):
    """A dependent is 'revalidated' when the new version carries an explicit REVALIDATE note or an open
    structural choice covering it; a dependent silently carried as settled is a defect."""
    na = new["architecture"]
    text = json.dumps(na, ensure_ascii=False).lower()
    open_structural = [c for c in na.get("open_architecture_choices", []) if c.get("structural")]
    unrevalidated = []
    for concl in conclusions:
        key = concl.split(" — ")[0].lower()
        covered = "revalidate" in text and (
            "audit" in key and any("audit" in c["choice"].lower() for c in open_structural)
            or "security" in key and any("authorization" in c["choice"].lower() or "security" in c["choice"].lower()
                                          for c in open_structural)
            or "experience" in key and any("surface" in c["choice"].lower() for c in open_structural)
            or "composition" in key and any("mechanism" in c["would_be_settled_by"].lower()
                                            for c in open_structural)
            or "access_mode" in key and any("mechanism" in c["would_be_settled_by"].lower()
                                            for c in open_structural)
        )
        if not covered:
            unrevalidated.append(concl)
    return unrevalidated


def structural_closure_defects(bp):
    """aisa-blueprint step 11/15: a structural choice may not be closed on connectivity alone."""
    defects = []
    for c in bp["architecture"].get("open_architecture_choices", []):
        if "resolved" in c["choice"].lower():
            basis = (c.get("closure_basis") or "").lower()
            if not basis or re.search(r"connection|gateway|connectivity|ligação", basis) and \
                    not re.search(r"mechanism|virtual|replicat|spike|measured|RESEARCH|§", basis):
                defects.append("closed on connectivity, no mechanism/fit basis: %s" % c["choice"][:60])
    rat = bp["architecture"]["experience"].get("rationale", "").lower()
    if ("gateway" in rat or "connectivity" in rat) and "confirmed" in rat:
        defects.append("surface confirmed from connectivity in rationale")
    return defects


# ---- PR-6 read-to-resume evaluator -----------------------------------------------------------

READ_TO_RESUME = {
    "discovery": ["_state.json", "context.json", "shared-understanding.md", "_capture/evidence-index.md",
                  "_capture/process-model.md §4", "lens-outputs/<current round>"],
    "framing": ["_state.json", "shared-understanding.md", "_capture/process-model.md §4", "frame.md",
                "decisions.md#D-001"],
    "options": ["_state.json", "frame.md", "shared-understanding.md", "options.md",
                "_capture/process-model.md §4"],
    "decision": ["_state.json", "decisions.md", "options.md", "shared-understanding.md", "_synthesis/"],
    "decision-architecture": ["_state.json", "decisions.md", "_blueprint/ux-blueprint_v<NN>.yaml",
                              "_blueprint/blueprint-log.md", "_synthesis/architecture-story.md",
                              "shared-understanding.md"],
}
NEVER_DEFAULT = ("inputs/", ".text.md", "lens-outputs/*", "domain-knowledge/", "transcript")


def read_to_resume(engagement_dir):
    """Derived from _state.json + the file system — never persisted."""
    with io.open(os.path.join(engagement_dir, "_state.json"), encoding="utf-8") as fh:
        state = json.load(fh)
    phase = state["phase"]
    key = phase
    if phase == "decision" and os.path.isdir(os.path.join(engagement_dir, "_blueprint")):
        key = "decision-architecture"
    items = list(READ_TO_RESUME[key])
    if not os.path.isfile(os.path.join(engagement_dir, "_capture", "process-model.md")):
        items = [i for i in items if "process-model" not in i]
    return phase, items


# =============================================================================================
# TC — technical-claim closure (PR-1)
# =============================================================================================

class TC_TechnicalClaimClosure(unittest.TestCase):

    def test_contract_answer_carries_fact_vs_fit_guard(self):
        self.assertIn("Architecture-significant technical claims", ANSWER)
        for token in ("would_be_settled_by", "Closure basis", "**A**", "**B**", "**C**",
                      "Capability ≠ fit", "No automatic web lookup", "no three-source rule",
                      "no Domain Knowledge preload", "Verbatim boundary"):
            self.assertIn(token, ANSWER, token)
        # trigger is architecture significance + use, not the decay class alone
        self.assertIn("does **not** apply merely because a row carries `validade: plataforma-tecnica`", ANSWER)

    def test_contract_blueprint_carries_structural_closure_rule(self):
        self.assertIn("Closing a structural choice — fact ≠ fit", BLUEPRINT)
        for token in ("settles the fact named in its `would_be_settled_by`", "**A** authoritative RESEARCH",
                      "**B** engagement-verifiable", "**C** a proof / measurement / spike",
                      "Capability confirmed ≠ fit confirmed", "mechanism per data domain",
                      "never inferred from connectivity", "without a recorded closure basis"):
            self.assertIn(token, BLUEPRINT, token)

    def test_TC1_IT_names_mechanism_may_close_only_with_fit(self):
        # IT: "virtual tables over the shared server, directory identity, integer PKs, no triggers"
        self.assertEqual(closure_verdict("B", settles_named_fact=True, fit_recorded=True),
                         ("Confirmed", "closed"))
        self.assertEqual(closure_verdict("B", settles_named_fact=True, fit_recorded=False),
                         ("Confirmed-capability", "open"))

    def test_TC2_persona_or_executor_assertion_without_authority_cannot_confirm(self):
        self.assertEqual(closure_verdict(None, settles_named_fact=True, fit_recorded=True),
                         ("Assumed-or-Unknown", "open"))

    def test_TC3_domain_knowledge_section_settles_within_its_bounds(self):
        state, choice = closure_verdict("A", settles_named_fact=True, fit_recorded=True)
        self.assertEqual((state, choice), ("Confirmed", "closed"))
        # the runtime carries the volatility bound for DK-settled claims
        self.assertIn("plataforma-tecnica", STATES)
        self.assertIn("re-verify", BLUEPRINT)

    def test_TC4_tenant_dependent_value_needs_engagement_verification(self):
        self.assertEqual(closure_verdict("A", settles_named_fact=True, fit_recorded=True, tenant_dependent=True),
                         ("Unknown-verification-obligation", "open"))
        self.assertIn("Domain Knowledge alone is insufficient — basis B or C is required", BLUEPRINT)

    def test_TC5_capability_exists_but_limitation_defeats_requirement(self):
        # capability confirmed (basis A: virtual tables exist) + fit fails (no audit on virtual data)
        self.assertEqual(closure_verdict("A", settles_named_fact=True, fit_recorded=False),
                         ("Confirmed-capability", "open"))
        # and the C-062 shape itself: answer settles connectivity, not the named fact
        self.assertEqual(closure_verdict("B", settles_named_fact=False, fit_recorded=False),
                         ("Confirmed-engagement-fact", "open"))

    def test_pilot1_defect_shape_is_rejected(self):
        bad = yaml.safe_load(fixture("c057-blueprint-v03-defect.yaml"))
        self.assertTrue(structural_closure_defects(bad))
        good = yaml.safe_load(fixture("c057-blueprint-v02.yaml"))
        self.assertEqual(structural_closure_defects(good), [])


# =============================================================================================
# CS — comprehension survival (PR-4 / PR-8)
# =============================================================================================

class CS_ComprehensionSurvival(unittest.TestCase):
    SYN = fixture("pricing-marinha-synopsis.md")
    PMU = fixture("pricing-marinha-pmu.md")
    OE = fixture("pricing-marinha-open-evidence.md")
    SU = fixture("pricing-marinha-su-excerpt.md")

    def test_contract_L2_reads_all_normalized_evidence(self):
        self.assertNotIn("stays scoped to `.xlsx`/`.xlsm`", CAPTURE)
        self.assertNotIn("stays scoped to `.xlsx`/`.xlsm`", ORCH)
        self.assertNotIn("Work ONLY from the extraction", TEMPLATE)
        self.assertIn("_capture/*.text.md", TEMPLATE)
        self.assertIn("source-complete in coverage", ORCH)
        self.assertIn("never source-total in simultaneous context", ORCH)
        for tok in ("USED", "CHECKED", "TARGETED"):
            self.assertIn(tok, CAPTURE)
        self.assertIn("No maximum source count, no KB budget, no transcript-length threshold", CAPTURE)

    def test_contract_synopsis_dimensions_and_markers(self):
        self.assertIn("## 4. Process synopsis (cross-source)", TEMPLATE)
        for dim in ("Purpose", "End-to-end flow", "Actors", "Inputs", "Transformation / calculation stages",
                    "Intermediate state", "Decisions", "Outputs and consumers", "Variants",
                    "Exceptions and workarounds", "Business invariants", "Structural constraints",
                    "Material user tasks", "Genuine vs accidental complexity", "Material unresolved semantics"):
            self.assertIn(dim, TEMPLATE, dim)
        self.assertIn("an irrelevant\ndimension gets no heading, never an empty one", TEMPLATE)
        for mk in MARKERS:
            self.assertIn(mk, TEMPLATE)
        self.assertIn("NOT engagement states", TEMPLATE)
        self.assertIn("input → transformation/rule → intermediate stage → transformation → output → consumer", TEMPLATE)
        self.assertIn("No silent disappearance", TEMPLATE)
        self.assertIn("NEVER converted automatically into a repeated business requirement", TEMPLATE)

    def test_CS1_cross_source_synopsis_reconstructs_the_material_flow(self):
        lines = synopsis_lines(self.SYN)
        self.assertGreater(len(lines), 20)
        self.assertTrue(all(cited for _m, _l, cited in lines), "every synopsis line is cited")
        # at least three distinct source kinds are cited
        self.assertRegex(self.SYN, r"PM-\d{3}")
        self.assertIn("docx · ¶", self.SYN)
        self.assertRegex(self.SYN, r"vtt · \[\d\d:\d\d:\d\d")
        flow = re.search(r"^### End-to-end flow(.*?)^### ", self.SYN, re.M | re.S).group(1)
        for stage in ("arrive automatically", "typed", "committee", "checklist", "loads"):
            self.assertIn(stage, flow)

    def test_CS2_output_family_absent_from_workbook_structure_survives(self):
        # `Outputs BIOS` is a sheet, but its role as a deliverable output family lives in the docx
        self.assertIn("Outputs BIOS", material_labels(self.SYN))
        bios = [l for l in self.SYN.splitlines() if "`Outputs BIOS`" in l][0]
        self.assertIn("docx · ¶137-143", bios)
        disp = dispositions(self.OE)
        self.assertEqual(disp["Outputs BIOS"][0], "ADOPT")
        self.assertIn(disp["Outputs BIOS"][1], su_ids_of(self.SU))
        # and its unknown consumer projects as an Unknown, not as silence
        self.assertEqual(su_state_of(self.SU, "U-033"), "Unknown")

    def test_CS3_calculation_chain_survives_as_stages_not_formulas(self):
        chain = [l for l in self.SYN.splitlines() if "`chain: cedência → base → venda → mínimo`" in l][0]
        for stage in ("Preço Cedência", "Preço Base", "Preço de Venda", "Preço Mínimo"):
            self.assertIn(stage, chain)
        self.assertNotIn("=INDEX(", self.SYN)
        self.assertNotIn("=IF(", self.SYN)
        disp = dispositions(self.OE)
        self.assertEqual(disp["chain: cedência → base → venda → mínimo"], ("ADOPT", "C-072", ""))

    def test_CS4_implementation_vs_business_duplication_is_a_hypothesis(self):
        six = [l for l in self.SYN.splitlines() if "`six copies`" in l][0]
        self.assertTrue(six.strip().startswith("- HYPOTHESIS"))
        self.assertIn("genuine", six)
        self.assertIn("accident", six)
        # the four-unit REQUIREMENT is OBSERVED (docx) and separately adopted
        four = [l for l in self.SYN.splitlines() if "`four unit outputs`" in l][0]
        self.assertTrue(four.strip().startswith("- OBSERVED"))
        self.assertEqual(dispositions(self.OE)["four unit outputs"][0], "ADOPT")
        # a HYPOTHESIS never becomes a Confirmed row on its own
        self.assertIn("a `HYPOTHESIS` line never becomes Confirmed or Assumed", CHAIRMAN)

    def test_CS5_material_line_without_disposition_fails(self):
        full = dispositions(self.OE)
        self.assertEqual(undisposed(self.SYN, self.PMU, full), [])
        without_bios = "\n".join(l for l in self.OE.splitlines() if "`Outputs BIOS`" not in l)
        missing = undisposed(self.SYN, self.PMU, dispositions(without_bios))
        self.assertEqual(missing, ["Outputs BIOS"])

    def test_dispositions_point_at_existing_rows(self):
        self.assertEqual(disposition_defects(dispositions(self.OE), su_ids_of(self.SU) | {
            "C-029", "C-038", "C-024", "C-006", "R-008"}), [])

    def test_contract_round_and_frame_carry_the_disposition_step(self):
        self.assertIn("Comprehension survival:", ROUND)
        for tok in ("`MAP <SU id>`", "`ADOPT → <new id>`", "`DISMISS — <reason>`", "Disposition bookkeeping",
                    "undisposed", "Never dispose of one yourself"):
            self.assertIn(tok, ROUND, tok)
        self.assertIn("Comprehension survival test", FRAME)
        for q in ("without naming the future solution", "output family traceable", "cannot lose",
                  "known structural constraints", "suspected decision-changing structural constraints",
                  "scope / user-task obligations", "received a disposition"):
            self.assertIn(q, FRAME, q)
        self.assertIn("no score, no completeness percentage, no fixed question count", FRAME)
        self.assertIn("Do not pretend comprehension is sufficient", FRAME)


# =============================================================================================
# PMU — PM-U disposition (PR-2A)
# =============================================================================================

class PMU_Disposition(unittest.TestCase):
    SYN = fixture("pricing-marinha-synopsis.md")
    PMU = fixture("pricing-marinha-pmu.md")
    OE = fixture("pricing-marinha-open-evidence.md")
    SU = fixture("pricing-marinha-su-excerpt.md")

    def test_PMU1_critical_pmu_mapped_to_existing_row(self):
        d = dispositions(self.OE)["PM-U-009"]
        self.assertEqual(d[0], "MAP")
        self.assertEqual(d[1], "C-041")

    def test_PMU2_critical_pmu_adopted_as_new_unknown(self):
        d = dispositions(self.OE)["PM-U-002"]
        self.assertEqual((d[0], d[1]), ("ADOPT", "U-032"))
        self.assertEqual(su_state_of(self.SU, "U-032"), "Unknown")

    def test_PMU3_dismiss_carries_a_materiality_reason(self):
        d = dispositions(self.OE)["PM-U-004"]
        self.assertEqual(d[0], "DISMISS")
        self.assertTrue(len(d[2]) > 15)
        broken = self.OE.replace("- PM-U-004 — DISMISS — Med; a static lookup table with no formula consumer changes nothing material downstream",
                                 "- PM-U-004 — DISMISS")
        self.assertIn("PM-U-004: DISMISS without a reason", disposition_defects(dispositions(broken), su_ids_of(self.SU)))

    def test_PMU4_critical_pmu_silently_absent_fails(self):
        without = "\n".join(l for l in self.OE.splitlines() if "PM-U-002" not in l)
        self.assertIn("PM-U-002", undisposed(self.SYN, self.PMU, dispositions(without)))
        # a Med/Low row left undisposed is a lens judgement, not a gate failure
        without_med = "\n".join(l for l in self.OE.splitlines() if "PM-U-006" not in l)
        self.assertNotIn("PM-U-006", undisposed(self.SYN, self.PMU, dispositions(without_med)))

    def test_PMU5_adopted_critical_pmu_may_remain_unknown(self):
        # visibility mandatory, closure not
        for pmu, target in (("PM-U-002", "U-032"), ("PM-U-003", "U-037")):
            self.assertEqual(dispositions(self.OE)[pmu][1], target)
            self.assertEqual(su_state_of(self.SU, target), "Unknown")
        self.assertIn("may remain Unknown but never disappears silently", ROUND)
        self.assertIn("Visibility is mandatory, closure is not", ORCH)

    def test_every_critical_pmu_in_fixture_is_disposed(self):
        crit = [p for p, c in pmu_rows(self.PMU).items() if c == "Critical"]
        self.assertEqual(sorted(crit), ["PM-U-001", "PM-U-002", "PM-U-003", "PM-U-005", "PM-U-009", "PM-U-011"])
        self.assertEqual(undisposed(self.SYN, self.PMU, dispositions(self.OE)), [])


# =============================================================================================
# FS — Framing survival block (PR-5)
# =============================================================================================

class FS_FramingSurvival(unittest.TestCase):
    SU_IDS = su_ids_of(fixture("pricing-marinha-su-excerpt.md"))
    FRAME_FX = fixture("pricing-marinha-frame-survival.md")

    def test_contract_chairman_frame_template_carries_the_block(self):
        self.assertIn("## What must survive into Options", CHAIRMAN)
        for sub in SURVIVAL_SUBLISTS:
            self.assertIn("### " + sub, CHAIRMAN)
        for rule in ("ID-anchored or explicit Unknown", "SU first, then project", "`(none) — <reason>` is a legitimate entry",
                     "Generic, technology-neutral", "HYPOTHESIS never enters as fact",
                     "may not create new factual authority", "never a product-licensing question"):
            self.assertIn(rule, CHAIRMAN, rule)
        self.assertIn("What must survive into Options (projection of SU ids", FRAME)

    def test_FS1_business_invariant_is_id_anchored(self):
        block = survival_block(self.FRAME_FX)
        ids = [i for i, _ in block["Business invariants"]]
        self.assertIn("C-073", ids)   # Mon/Tue behaviour — the Pilot-1 loss
        self.assertTrue(all(i in self.SU_IDS for i in ids))

    def test_FS2_structural_constraint_is_id_anchored(self):
        block = survival_block(self.FRAME_FX)
        ids = [i for i, _ in block["Structural constraints"]]
        for expected in ("C-013", "C-036", "C-028", "C-052", "U-035"):
            self.assertIn(expected, ids)
        self.assertTrue(all(i in self.SU_IDS for i in ids))

    def test_FS3_decision_changing_unknown_is_visible(self):
        block = survival_block(self.FRAME_FX)
        ids = [i for i, _ in block["Decision-changing Unknowns"]]
        self.assertIn("U-028", ids)
        self.assertIn("U-032", ids)
        self.assertEqual(survival_defects(self.FRAME_FX, self.SU_IDS), [])

    def test_FS4_none_with_reason_is_valid(self):
        frame = self.FRAME_FX.replace(
            "### Structural constraints\n- C-013", "### Structural constraints\n- (none) — single internal population, data owned by the sponsor's team, no residency or entitlement condition recorded (C-013, C-036)\n- C-013")
        # only the `(none)` line remains material for the check when it is alone:
        frame_only_none = re.sub(r"(### Structural constraints\n- \(none\)[^\n]*\n)(- [^\n]*\n)+", r"\1", frame)
        self.assertEqual(survival_defects(frame_only_none, self.SU_IDS), [])
        # an EMPTY sub-list is not valid
        empty = re.sub(r"(### Structural constraints\n)(- [^\n]*\n)+", r"\1", self.FRAME_FX)
        self.assertTrue(any("Structural constraints: empty" in d for d in survival_defects(empty, self.SU_IDS)))

    def test_FS5_frame_inventing_a_constraint_fails(self):
        invented = self.FRAME_FX.replace(
            "### Structural constraints\n",
            "### Structural constraints\n- C-099 — data must stay on-premises for regulatory reasons\n- the platform must support offline use\n")
        defects = survival_defects(invented, self.SU_IDS)
        self.assertTrue(any("C-099 is not an SU row" in d for d in defects))
        self.assertTrue(any("entry without SU id" in d for d in defects))


class FS6_OverrideCannotMaskMissingUnderstanding(unittest.TestCase):
    """Step 8C.1 — one generic evaluator, run over all five survival categories."""
    SU = fixture("pricing-marinha-su-excerpt.md")
    SYN = fixture("pricing-marinha-synopsis.md")
    DISP = dispositions(fixture("pricing-marinha-open-evidence.md"))
    FRAME_FX = fixture("pricing-marinha-frame-survival.md")
    GATE_PASS = parse_gate_record("gate: PASS\n- **Override used at /frame**: —\n")

    @staticmethod
    def _gate_fail(category, gap, reason="sponsor deadline; proceed with the gap visible"):
        return parse_gate_record(
            "gate: FAIL\nmissing understanding: %s — %s\noverride: YES\noverride reason: %s\n"
            "proceed: allowed under existing soft-gate doctrine\n- **Override used at /frame**: %s\n"
            % (category, gap, reason, reason))

    def _with_none(self, category, text="(none) — overridden to proceed"):
        return re.sub(r"(### %s\n)(- [^\n]*\n)+" % re.escape(category), r"\1- %s\n" % text, self.FRAME_FX)

    def test_contract_override_is_not_evidence(self):
        for tok in ("Override ≠ evidence · override ≠ resolution · override ≠ absence",
                    "gate: FAIL", "missing understanding: <category> — <specific gap>", "override: YES",
                    "proceed: allowed under existing soft-gate doctrine",
                    "never writes `(none) — <override reason>`",
                    "no material item of that semantic class exists for this engagement"):
            self.assertIn(tok, FRAME, tok)
        for tok in ("only as a substantive conclusion", "(1) the category was evaluated",
                    "(2) no known material SU item belongs to it",
                    "(3) no material synopsis line requiring disposition remains unresolved",
                    "(4) no comprehension-survival gate failure on that category is being hidden",
                    "Override ≠ evidence, ≠ resolution, ≠ absence",
                    "`decisions.md` D-001 `Override used at /frame`"):
            self.assertIn(tok, CHAIRMAN, tok)
        # the override record reuses the existing soft-gate mechanism — no new frame field, no new state
        self.assertNotIn("### Gate override", CHAIRMAN)
        self.assertNotIn("### Override", CHAIRMAN)
        block = CHAIRMAN.split("## What must survive into Options")[1].split("```")[0]
        self.assertEqual(re.findall(r"^### (.+)$", block, re.M), list(SURVIVAL_SUBLISTS))
        self.assertIn("**Override used at /frame**", FRAME)

    def test_FS6_override_masking_the_output_family_consumer_fails(self):
        # material output family exists (`Outputs BIOS`) + consumer Unknown (U-033) + gate FAIL + override
        gate = self._gate_fail("Material scope / task obligations",
                               "`Outputs BIOS` has no identified consumer (U-033)")
        masked = self._with_none("Material scope / task obligations", "(none) — overridden to proceed")
        defects = survival_defects_full(masked, self.SU, self.SYN, self.DISP, gate)
        # the output family itself (C-071) is a known material item of the category; its consumer (U-033)
        # is the gate's named gap — both make `(none)` a defect
        self.assertTrue(any("known material SU items exist" in d and "C-071" in d for d in defects))
        self.assertTrue(any("hides a gate failure" in d and "U-033" in d for d in defects))
        self.assertTrue(any("override reason written as `(none)` reason" in d for d in defects))

    def test_FS6_correct_shape_passes_with_the_gap_visible(self):
        gate = self._gate_fail("Material scope / task obligations",
                               "`Outputs BIOS` has no identified consumer (U-033)")
        # the fixture frame names U-033 under scope/task obligations; the override lives in D-001
        self.assertIn("U-033", [i for i, _ in survival_block(self.FRAME_FX)["Material scope / task obligations"]])
        self.assertEqual(survival_defects_full(self.FRAME_FX, self.SU, self.SYN, self.DISP, gate), [])
        self.assertTrue(gate["override"])
        self.assertEqual(gate["result"], "FAIL")   # the override did not change what is known

    def test_FS6_generic_over_all_five_categories(self):
        gaps = {
            "Process meaning": "calculation chain not reconstructed (C-072)",
            "Business invariants": "Mon/Tue behaviour not stated as a behaviour to keep (C-073)",
            "Structural constraints": "where pricing data must live is absent (U-035)",
            "Decision-changing Unknowns": "U-028 not surfaced",
            "Material scope / task obligations": "`Outputs BIOS` has no identified consumer (U-033)",
        }
        for category, gap in gaps.items():
            gate = self._gate_fail(category, gap)
            masked = self._with_none(category)
            defects = survival_defects_full(masked, self.SU, self.SYN, self.DISP, gate)
            self.assertTrue(any(d.startswith(category) for d in defects), category)
            self.assertTrue(any("hides a gate failure" in d for d in defects), category)
            # the honest shape — ids kept, override recorded in D-001 — passes for every category
            self.assertEqual(survival_defects_full(self.FRAME_FX, self.SU, self.SYN, self.DISP, gate), [],
                             category)

    def test_FS6_genuine_none_remains_valid(self):
        # an engagement whose synopsis carries NO structural-constraint dimension, whose SU has no such item
        # and whose gate passed: `(none) — <substantive reason>` is a legitimate conclusion
        syn = re.sub(r"### Structural constraints\n(?:- [^\n]*\n)+", "", self.SYN)
        disp = {k: v for k, v in self.DISP.items()
                if k not in ("internal audience", "parallel Spain process", "where pricing data must live",
                             "term contracts priced in SAP")}
        frame = self._with_none(
            "Structural constraints",
            "(none) — no constraint has been identified that materially eliminates or reshapes solution classes")
        self.assertEqual(survival_defects_full(frame, self.SU, syn, disp, self.GATE_PASS), [])
        # the same wording with an override behind it, or with the dimension still present, is not
        gate = self._gate_fail("Structural constraints", "where pricing data must live is absent (U-035)")
        self.assertTrue(survival_defects_full(frame, self.SU, syn, disp, gate))
        self.assertTrue(survival_defects_full(frame, self.SU, self.SYN, self.DISP, self.GATE_PASS))

    def test_FS6_override_does_not_resolve_an_unknown(self):
        gate = self._gate_fail("Material scope / task obligations",
                               "`Outputs BIOS` has no identified consumer (U-033)")
        # after the override the SU row is untouched: still an open Unknown, still projected
        self.assertEqual(su_state_of(self.SU, "U-033"), "Unknown")
        self.assertIn("U-033", self.FRAME_FX)
        self.assertNotIn("resolved →", [l for l in self.SU.splitlines() if l.startswith("| U-033 ")][0])


# =============================================================================================
# SI — semantic invalidation (PR-7) + C-057 regression
# =============================================================================================

class SI_SemanticInvalidation(unittest.TestCase):
    V01 = yaml.safe_load(fixture("c057-blueprint-v01.yaml"))
    V02 = yaml.safe_load(fixture("c057-blueprint-v02.yaml"))
    V03_BAD = yaml.safe_load(fixture("c057-blueprint-v03-defect.yaml"))
    DEC = fixture("c057-decisions-excerpt.md")
    OPT = fixture("c057-options-excerpt.md")

    def test_contract_answer_and_blueprint_carry_targeted_revalidation(self):
        self.assertIn("Targeted revalidation", ANSWER)
        self.assertIn("Cross-field architecture change — targeted revalidation", BLUEPRINT)
        self.assertIn("which existing architecture conclusions were materially based on the previous value?", BLUEPRINT)
        for tok in ("still valid", "revalidate", "No automatic reversal", "No dependency graph",
                    "architecture never rewrites the Decision", "/revisit"):
            self.assertIn(tok, BLUEPRINT, tok)
        self.assertIn("an unrelated answer produces `(none)`", ANSWER)
        self.assertIn("the Decision is never rewritten here", ANSWER)

    def test_SI1_record_authority_change_lists_dependents(self):
        dep = dependents_of_record_authority_change(self.V01, self.V02, self.DEC, self.OPT)
        joined = " | ".join(dep["conclusions"]).lower()
        for expected in ("security basis", "audit basis", "access_mode", "composition", "experience.rationale"):
            self.assertIn(expected, joined, expected)

    def test_SI2_unrelated_fact_triggers_no_broad_revalidation(self):
        # a terminology correction changes nothing architecture-significant
        same = yaml.safe_load(fixture("c057-blueprint-v01.yaml"))
        same["architecture"]["compositions"][1]["forced_by"] += " (system correctly named X-Author)"
        dep = dependents_of_record_authority_change(self.V01, same, self.DEC, self.OPT)
        self.assertEqual(dep["conclusions"], [])
        self.assertIsNone(dep["route"])

    def test_SI3_decision_basis_threatened_routes_to_revisit_not_rewrite(self):
        dep = dependents_of_record_authority_change(self.V01, self.V02, self.DEC, self.OPT)
        self.assertTrue(dep["decision_layer"])
        self.assertEqual(dep["route"], "tripwire check → /revisit")
        # nothing rewrites decisions.md: the evaluator returns a recommendation only
        self.assertIn("auditability (R-005)", self.DEC)

    def test_SI4_prose_dependence_is_caught_without_a_schema_field(self):
        # experience.su_refs do not name the store rows; the dependency is in the rationale prose
        self.assertFalse(set(self.V01["architecture"]["experience"]["su_refs"]) & {"C-017", "C-035", "C-006", "C-016", "C-018", "R-004"})
        dep = dependents_of_record_authority_change(self.V01, self.V02, self.DEC, self.OPT)
        self.assertTrue(any("experience.rationale" in c for c in dep["conclusions"]))
        self.assertNotIn("depends_on", BLUEPRINT)
        self.assertNotIn("depends_on", fixture("c057-blueprint-v02.yaml"))

    def test_SI5_premise_changed_but_conclusion_silently_settled_fails(self):
        dep = dependents_of_record_authority_change(self.V01, self.V03_BAD, self.DEC, self.OPT)
        self.assertTrue(revalidation_recorded(self.V03_BAD, dep["conclusions"]),
                        "the defect version must show unrevalidated dependents")
        # the correct version revalidates every dependent
        dep_ok = dependents_of_record_authority_change(self.V01, self.V02, self.DEC, self.OPT)
        self.assertEqual(revalidation_recorded(self.V02, dep_ok["conclusions"]), [])

    def test_C057_regression_fixture(self):
        dep = dependents_of_record_authority_change(self.V01, self.V02, self.DEC, self.OPT)
        joined = " | ".join(dep["conclusions"]).lower()
        # record authority changes
        self.assertEqual(sorted(changed_fields(self.V01, self.V02)["record_authority"]),
                         sorted(["Pricing master data", "Target margins and daily logistics costs", "Daily price history"]))
        # security / audit / access / composition / surface implications listed
        for implication in ("security", "audit", "access_mode", "composition", "experience.rationale"):
            self.assertIn(implication, joined)
        # no automatic reversal: the surface value is unchanged, the choice is OPEN and structural
        self.assertEqual(self.V02["architecture"]["experience"]["primary_surface"],
                         self.V01["architecture"]["experience"]["primary_surface"])
        surface_choice = [c for c in self.V02["architecture"]["open_architecture_choices"] if "Surface" in c["choice"]][0]
        self.assertTrue(surface_choice["structural"])
        self.assertIn("mechanism", surface_choice["would_be_settled_by"].lower())
        self.assertIn("Connectivity alone does not settle it", surface_choice["would_be_settled_by"])
        # structural choices remain open where evidence is insufficient
        self.assertGreaterEqual(len([c for c in self.V02["architecture"]["open_architecture_choices"] if c["structural"]]), 3)
        # decision layer routes to /revisit
        self.assertEqual(dep["route"], "tripwire check → /revisit")


# =============================================================================================
# RH — rehydration (PR-6)
# =============================================================================================

class RH_Rehydration(unittest.TestCase):

    def _engagement(self, phase, with_capture=True, with_blueprint=False):
        d = tempfile.mkdtemp(prefix="aisa-rh-")
        with io.open(os.path.join(d, "_state.json"), "w", encoding="utf-8") as fh:
            json.dump({"engagement": "fx", "pack": "pp", "phase": phase, "round": "R-01"}, fh)
        for name in ("context.json", "shared-understanding.md", "frame.md", "decisions.md", "options.md"):
            with io.open(os.path.join(d, name), "w", encoding="utf-8") as fh:
                fh.write("x")
        if with_capture:
            os.makedirs(os.path.join(d, "_capture"))
            with io.open(os.path.join(d, "_capture", "process-model.md"), "w", encoding="utf-8") as fh:
                fh.write("## 4. Process synopsis (cross-source)\n- OBSERVED — x — PM-001\n")
        if with_blueprint:
            os.makedirs(os.path.join(d, "_blueprint"))
        return d

    def test_contract_status_carries_read_to_resume(self):
        self.assertIn("Derive the `Read to resume` set", STATUS)
        self.assertIn("PHASE ≠ SESSION", STATUS)
        self.assertIn("never persisted", STATUS)
        self.assertIn("not a handoff summary", STATUS)
        self.assertIn("must not depend on the previous transcript", STATUS)
        for phase in ("discovery", "framing", "options", "decision (pre-blueprint)", "decision (architecture)", "deliverables"):
            self.assertIn("| %s |" % phase, STATUS, phase)
        self.assertIn("Read to resume (<phase>)", STATUS)
        self.assertIn("never all raw evidence, all transcripts, all lens outputs or all Domain Knowledge", STATUS)

    def test_RH1_fresh_session_derives_current_phase(self):
        for phase in ("discovery", "framing", "options", "decision"):
            got, _items = read_to_resume(self._engagement(phase))
            self.assertEqual(got, phase)

    def test_RH2_read_set_contains_current_authorities(self):
        _p, items = read_to_resume(self._engagement("options"))
        for auth in ("frame.md", "shared-understanding.md", "options.md"):
            self.assertIn(auth, items)
        _p, items = read_to_resume(self._engagement("decision", with_blueprint=True))
        self.assertIn("decisions.md", items)
        self.assertTrue(any("_blueprint/ux-blueprint" in i for i in items))

    def test_RH3_no_previous_transcript_required(self):
        for phase in ("discovery", "framing", "options", "decision"):
            _p, items = read_to_resume(self._engagement(phase))
            self.assertFalse(any("transcript" in i or "conversation" in i for i in items))
        self.assertNotIn("previous session", STATUS.lower().replace("the previous transcript", ""))

    def test_RH4_no_handoff_summary_artefact(self):
        for skill in (STATUS, FRAME, ROUND, CAPTURE, CHAIRMAN, ANSWER, BLUEPRINT):
            for forbidden in ("handoff-summary.md", "session-summary", "discovery-handoff.md", "process-understanding.md"):
                self.assertNotIn(forbidden, skill, forbidden)
        skills = os.listdir(os.path.join(ROOT, ".claude", "skills"))
        self.assertFalse(any(re.search(r"handoff|rehydrat|resume-summary", s) for s in skills))

    def test_RH5_detailed_process_evidence_pulled_only_when_synopsis_insufficient(self):
        _p, items = read_to_resume(self._engagement("options"))
        self.assertIn("_capture/process-model.md §4", items)
        for never in NEVER_DEFAULT:
            self.assertFalse(any(never in i for i in items), never)
        self.assertIn("pulled **only** when the synopsis and the SU do not answer a material question", STATUS)
        # without a process model the synopsis line is simply absent — no error, no invented pointer
        _p, items = read_to_resume(self._engagement("options", with_capture=False))
        self.assertFalse(any("process-model" in i for i in items))


# =============================================================================================
# Pricing-marinha static proof (fixture derived from the existing evidence; engagement untouched)
# =============================================================================================

class PricingMarinhaStaticProof(unittest.TestCase):
    SYN = fixture("pricing-marinha-synopsis.md")
    OE = fixture("pricing-marinha-open-evidence.md")
    SU = fixture("pricing-marinha-su-excerpt.md")
    FR = fixture("pricing-marinha-frame-survival.md")

    def test_engagement_not_modified_by_this_step(self):
        # the proof runs on fixtures under .claude/tests; no fixture points into an engagement folder
        self.assertTrue(os.path.isdir(FIX))
        for name in os.listdir(FIX):
            if name == "README.md":
                continue      # the README explains, in prose, that the engagement folder is NOT touched
            body = fixture(name)
            self.assertNotIn("projects/", body, name)
            self.assertNotIn("$AISA_ENGAGEMENTS_ROOT", body, name)

    def test_chain_four_units_bios_simulador_monday_survive(self):
        labels = material_labels(self.SYN)
        for lab in ("chain: cedência → base → venda → mínimo", "four unit outputs", "Outputs BIOS", "Simulador",
                    "Mon/Tue pricing must remain possible", "missing quotes", "what-if projection", "conservative rule"):
            self.assertIn(lab, labels, lab)
        disp = dispositions(self.OE)
        for lab in ("chain: cedência → base → venda → mínimo", "four unit outputs", "Outputs BIOS", "Simulador",
                    "Mon/Tue pricing must remain possible"):
            self.assertIn(disp[lab][0], ("MAP", "ADOPT"), lab)
        block = survival_block(self.FR)
        flat = [i for entries in block.values() for i, _ in entries]
        for sid in ("C-072", "C-070", "C-071", "C-074", "C-073"):
            self.assertIn(sid, flat, sid)

    def test_structural_constraints_visible_pre_options(self):
        labels = material_labels(self.SYN)
        for lab in ("internal audience", "parallel Spain process", "where pricing data must live", "term contracts priced in SAP"):
            self.assertIn(lab, labels)
        # the Pilot-1 invisible constraint (where must pricing data live) is an explicit Unknown, swing decisivo
        self.assertEqual(dispositions(self.OE)["where pricing data must live"], ("ADOPT", "U-035", ""))
        row = [l for l in self.SU.splitlines() if l.startswith("| U-035 ")][0]
        self.assertIn("decisivo", row)
        self.assertIn("U-035", [i for i, _ in survival_block(self.FR)["Structural constraints"]])

    def test_incomplete_input_behaviour_is_invariant_and_task_not_only_exposure(self):
        self.assertEqual(su_state_of(self.SU, "C-073"), "Confirmed")
        self.assertIn("C-073", [i for i, _ in survival_block(self.FR)["Business invariants"]])
        self.assertIn("U-032", [i for i, _ in survival_block(self.FR)["Decision-changing Unknowns"]])

    def test_synopsis_is_technology_neutral(self):
        low = self.SYN.lower()
        for vendor in ("power platform", "power apps", "dataverse", "canvas app", "model-driven", "outsystems", "mendix",
                       "sharepoint", "azure"):
            self.assertNotIn(vendor, low, vendor)
        self.assertNotIn("model-driven", TEMPLATE.lower())
        self.assertNotIn("dataverse", TEMPLATE.lower())


# =============================================================================================
# Guards — nothing forbidden was introduced; frozen surfaces untouched
# =============================================================================================

class Guards(unittest.TestCase):

    def test_pack_version_moved_only_for_a_recorded_reason(self):
        """Step 8C froze the model at 1.8.2. The pin stays — it moves only when the
        changelog in pack.yaml says what moved and why. 1.9.0 is the platform-forms
        addition (P-19): this pack's platform became a class of `surface x store`
        members, and the Options artefact gained the obligation to name the form.
        Nothing this file guards — stage, concern, outcome class, composed row,
        blocking entry, knowledge unit, architecture unit, deliverable contract —
        was touched by it, and the 8C rationale must survive in the changelog."""
        self.assertEqual(str(PACK["pack_version"]), "1.9.0")
        self.assertIn("pack_version 1.9.0", PACK_TEXT)
        self.assertIn("PLATFORM FORMS ARE NAMED IN OPTIONS", PACK_TEXT)
        self.assertIn("pack_version 1.8.2 (Step 8C)", PACK_TEXT)

    def test_no_new_epistemic_state(self):
        rows = re.findall(r"^\| \*\*(Confirmed|Assumed|Unknown|Conflicted|Risky)\*\* \|", STATES, re.M)
        self.assertEqual(len(rows), 5)
        self.assertNotIn("| **OBSERVED**", STATES)
        self.assertIn("These are markers on normalized evidence, NOT engagement states", TEMPLATE)

    def test_no_new_phase_agent_router_ledger(self):
        self.assertEqual(len(re.findall(r"^## Phase \d", PHASES, re.M)), 4)
        agents = sorted(a for a in os.listdir(os.path.join(ROOT, ".claude", "agents")) if a.endswith(".md"))
        self.assertEqual(agents, ["business-analyst.md", "cfo-lens.md", "chairman.md", "compliance-officer.md",
                                  "data-steward.md", "operations-lead.md", "solution-architect.md", "user-advocate.md"])
        for text, name in ((ORCH, "orchestration"), (ROUND, "aisa-round"), (STATUS, "aisa-status"), (FRAME, "aisa-frame")):
            self.assertNotIn("dependency graph:", text.lower(), name)
            self.assertNotIn("compression matrix", text.lower().replace("no compression matrix", "").replace("compression matrix warranted", ""), name)
        self.assertIn("No new state, no new field, no register, no matrix", ORCH)
        self.assertNotIn("depends_on", BLUEPRINT)

    def test_no_new_process_comprehension_artefact(self):
        for text in (CAPTURE, ROUND, FRAME, CHAIRMAN, STATUS, ORCH, TEMPLATE):
            self.assertNotIn("process-understanding.md", text)
        self.assertIn("output_path: _capture/process-model.md", TEMPLATE)

    def test_PR3_not_implemented(self):
        low = BLUEPRINT.lower()
        for forbidden in ("task matrix", "each screen names the task", "interaction-shape evaluation is mandatory",
                          "mandatory interaction-shape"):
            self.assertNotIn(forbidden, low, forbidden)
        # step 4 unchanged: entities <- data rows, personas <- user rows
        self.assertIn("`entities` ← `lens=data` rows", BLUEPRINT)
        self.assertIn("`personas` ← `lens=user` rows", BLUEPRINT)

    def test_no_mockup_solution_presumption(self):
        for text in (TEMPLATE, ORCH, CAPTURE, ROUND, FRAME, CHAIRMAN):
            low = text.lower()
            self.assertNotIn("complex process → canvas", low)
            self.assertNotIn("record-oriented data → model-driven", low)

    def test_parse_once_boundary_preserved(self):
        self.assertIn("Parse once. Reason many.", ORCH)
        # Options/Architecture are not told to re-read the capture model; the synopsis is a pointer only
        self.assertNotIn("re-read the capture", BLUEPRINT.lower())
        self.assertIn("open its detail sections or a raw source only when material to your confidence", CHAIRMAN)

    def test_no_product_licensing_question_pre_options(self):
        self.assertIn("never a product-licensing question", CHAIRMAN)
        self.assertIn("No product-licensing question is asked pre-Options because a pack is active", ORCH)
        for text in (TEMPLATE, FRAME, CHAIRMAN.split("#### Options")[0]):
            low = text.lower()
            for tok in ("premium licen", "per-user licen", "licence sku", "license sku"):
                self.assertNotIn(tok, low, tok)

    def test_teach_back_groups_without_collapsing(self):
        self.assertIn("Process teach-back (materiality-triggered, never mandatory)", STATUS)
        self.assertIn("each underlying Unknown keeps its own identity and closure criterion", STATUS)
        self.assertIn("never collapses them into one", STATUS)

    def test_doctrine_lives_where_guidance_owns_it(self):
        shorthand = "reason deeply → persist selectively → claim conservatively → rehydrate selectively → revalidate when premises change"
        self.assertIn(shorthand, ORCH)
        self.assertIn(shorthand.replace("reason deeply", "reason deeply"), read("docs", "ARCHITECTURE.md"))
        self.assertIn("phase ≠ session", ORCH.lower())
        self.assertIn("disposable cache", ORCH)
        self.assertNotIn("reasoning sequence:", ORCH.lower())

    def test_step_8b_final_corrections_recorded(self):
        report = read("docs", "pp-pack-authoring", "pilot", "step-8b-post-pilot-adjudication-report.md")
        for line in ("SPECIFIC SQL ACCESS MECHANISM IDENTIFIED: NO",
                     "MODEL-DRIVEN + EXTERNAL SQL CAN BE DEFENSIBLE WITH PRECONDITIONS: YES",
                     "A-009 FINAL STATUS: UNKNOWN"):
            self.assertIn(line, report, line)
        self.assertNotIn("SPECIFIC SQL ACCESS MECHANISM IDENTIFIED: YES", report)
        self.assertNotIn("A-009 FINAL STATUS: DEFENSIBLE-WITH-PRECONDITIONS", report)


if __name__ == "__main__":
    unittest.main(verbosity=1)
