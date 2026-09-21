"""Frente C (P-13 / P-14) — two languages: the kernel in the files, business language to the user.

The contract lives in `library/kernel/glossary.md` (section *Two languages*): every **bold** or
`code` token in the first column of the glossary table is a kernel term; in user-facing text it may
appear only between parentheses after the business phrase. Ids (`U-nnn`, `D-001`, `TW-n`, ...) obey
the same rule. Commands and paths in backticks stay literal.

User-facing text is what the command skills mark as ```user-output fenced blocks, the labels the
dashboard renders (tooltips excepted — that is where the kernel term goes), and `docs/COMO-USAR.md`.
This module is also the motor behind `docs/pp-pack-authoring/pilot/step-9e-evidence/accept_frente_c.py`
(before/after counts): the functions below are imported there, so the acceptance and the regression
test cannot disagree.

    python .claude/tests/test_user_language.py
"""

import importlib.util
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as fh:
        return fh.read()


GLOSSARY = read("library", "kernel", "glossary.md")
CLAUDE_MD = read("CLAUDE.md")

# Every command skill that talks to the user. Each must carry >= 1 ```user-output block and its last
# block must close with the "A seguir:" line (P-14 rule 2: the user never memorises commands).
COMMAND_SKILLS = (
    "aisa-start", "aisa-round", "aisa-answer", "aisa-status", "aisa-frame", "aisa-options",
    "aisa-decide", "aisa-blueprint", "aisa-render", "aisa-synthesize", "aisa-simulate",
    "aisa-premortem", "aisa-capture", "aisa-revisit", "aisa-retro", "aisa-orient",
)

# Words the glossary lists in code for their machine value but that are ordinary Portuguese in a
# sentence. Kept minimal and explicit; anything else in the first column is jargon.
ORDINARY_WORDS = frozenset({"email", "documento"})

# Ids may appear only between parentheses. Placeholders (`U-nnn`, `R-NN`) count as ids too: a
# template that writes an id alone teaches the model to print one alone.
ID_RE = re.compile(r"(?<![\w-])(?:C|A|U|X|R|D|O|F|M|TW|PM-U)-(?:\d+|n{1,3}|N{1,3})(?![\w-])")
PAREN_RE = re.compile(r"\([^()]*\)")
CODE_RE = re.compile(r"`([^`]*)`")
HTML_TITLE_RE = re.compile(r'\stitle="[^"]*"')
TAG_RE = re.compile(r"<[^<>]+>")


# ------------------------------------------------------------------ glossary contract


def glossary_terms(md=GLOSSARY):
    """Lint tokens -> business phrase, from the first and third columns of the glossary table."""
    terms = {}
    for line in md.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or cells[0] == "Term" or set(cells[0]) <= set("-: "):
            continue
        col1, phrase = cells[0], cells[2]
        toks = re.findall(r"\*\*(.+?)\*\*", col1) + re.findall(r"`([^`]+)`", col1)
        for tok in toks:
            for part in re.split(r"\s*[·/]\s*", tok):
                part = part.strip()
                if part and part not in ORDINARY_WORDS and not ID_RE.fullmatch(part):
                    terms.setdefault(part, phrase)
    return terms


def _token_pattern(tok):
    forms = [re.escape(tok)]
    # An English kernel word is jargon in either case: `Pack` in the glossary, `pack: pp` in output.
    if re.fullmatch(r"[A-Z][a-z]+", tok):
        forms.append(re.escape(tok.lower()))
    return re.compile(r"(?<![\w-])(?:" + "|".join(forms) + r")(?![\w-])")


def visible(line):
    """What the user actually reads as prose: parentheses gone (that is where kernel terms and ids
    belong), commands/paths/flags in backticks gone (they are literal), other backticked text kept —
    jargon in backticks is still jargon."""
    s = line
    for _ in range(3):
        s = PAREN_RE.sub(" ", s)

    def keep(m):
        t = m.group(1)
        if t.startswith("/") or t.startswith("--") or "/" in t or "." in t or "=" in t:
            return " "
        return " " + t + " "

    return CODE_RE.sub(keep, s)


def violations(text, terms=None):
    """[(line_no, offending token, line)] for every kernel term or id outside parentheses."""
    terms = glossary_terms() if terms is None else terms
    patterns = [(tok, _token_pattern(tok)) for tok in terms]
    out = []
    for i, raw in enumerate(text.splitlines(), 1):
        s = visible(raw)
        for tok, pat in patterns:
            if pat.search(s):
                out.append((i, tok, raw.strip()))
        for m in ID_RE.finditer(s):
            out.append((i, m.group(0), raw.strip()))
    return out


def user_output_blocks(md):
    """The ```user-output fenced blocks of a skill, in order."""
    return re.findall(r"```user-output\n(.*?)```", md, flags=re.S)


def forbidden_paraphrases(md=GLOSSARY):
    """Literal -> [paraphrase, ...] from the glossary's *Forbidden paraphrases* table (P-20).

    Technical terminology is never translated: a product, vendor, service, surface, store or
    control name is a literal in every user-facing text. The table is the machine-readable half
    of rule 5 of *Two languages*.
    """
    out = {}
    table = re.search(r"\*\*Forbidden paraphrases\*\*.*?\n\n(\|.*?)(?:\n\n|\Z)", md, flags=re.S)
    if not table:
        return out
    for line in table.group(1).splitlines():
        if not line.startswith("|") or line.startswith("|---") or "Never written as" in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 2:
            continue
        literal = cells[0].strip("`").strip()
        out[literal] = [p.strip() for p in cells[1].split("·") if p.strip()]
    return out


def paraphrase_violations(text, table=None):
    """(paraphrase, literal) pairs found in user-facing text — case-insensitive."""
    table = forbidden_paraphrases() if table is None else table
    low = text.lower()
    return [(p, lit) for lit, paras in table.items() for p in paras if p.lower() in low]


def dashboard_labels(src):
    """Literal labels the dashboard renders as headings, tabs and table headers — tooltips stripped."""
    src = HTML_TITLE_RE.sub("", src)
    labels = []
    labels += re.findall(r'<h2 class="sec">(.*?)(?:<span|</h2>)', src)
    labels += re.findall(r"<h3>(.*?)</h3>", src)
    labels += re.findall(r"<th>(.*?)</th>", src)
    labels += re.findall(r'data-title="([^"]+)"', src)
    labels += re.findall(r'aria-selected="(?:true|false)">([^<{]+?)(?:\s*<span class="cnt">|</button>)', src)
    for name in ("STATE_LABEL", "SWING_LABEL", "CUSTO_LABEL", "PHASE_LABEL", "SUPPORT_LABEL"):
        block = re.search(name + r"\s*=\s*\{(.*?)\}", src, flags=re.S)
        if block:
            labels += re.findall(r':\s*"([^"]*)"', block.group(1))
    return [TAG_RE.sub("", l).replace("&middot;", "·").strip() for l in labels if l.strip()]


# ------------------------------------------------------------------ tests


class TestGlossaryContract(unittest.TestCase):
    def test_glossary_declares_the_user_column_and_the_rules(self):
        self.assertIn("| Term | Definition | Como se diz ao utilizador |", GLOSSARY)
        self.assertIn("## Two languages (P-13)", GLOSSARY)
        self.assertIn("only between parentheses, after the business phrase", GLOSSARY)

    def test_every_row_carries_a_business_phrase(self):
        for line in GLOSSARY.splitlines():
            if line.startswith("| **") or line.startswith("| Custo"):
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                self.assertEqual(len(cells), 3, line)
                self.assertTrue(cells[2] and cells[2] != "—", line)

    def test_the_plan_terms_are_all_tokens(self):
        terms = glossary_terms()
        for tok in ("Unknown", "Assumed", "Confirmed", "Conflicted", "Risky", "decisivo",
                    "dimensionante", "cosmético", "spike", "PM-U", "undisposed", "Tripwire",
                    "Saúde epistémica", "expirada", "Lens", "Council", "Chairman", "SU",
                    "Shared Understanding", "ronda", "Frame", "Blueprint", "Render", "gate",
                    "Override", "Discovery", "Framing", "Options", "Decision", "Pack", "Engagement"):
            self.assertIn(tok, terms, tok)
        for word in ("email", "documento", "custo", "validade"):
            self.assertNotIn(word, terms, word)

    def test_business_phrases_carry_no_kernel_term(self):
        terms = glossary_terms()
        for tok, phrase in terms.items():
            bad = [t for t, pat in ((t, _token_pattern(t)) for t in terms) if pat.search(visible(phrase))]
            self.assertEqual(bad, [], "phrase for %s reuses kernel terms %s" % (tok, bad))


class TestVisibleText(unittest.TestCase):
    def test_parentheses_and_commands_are_exempt(self):
        self.assertEqual(violations("pergunta em aberto (Unknown U-012) → `/answer U-012 \"…\"`"), [])

    def test_jargon_alone_is_caught(self):
        v = violations("Unknown U-012 — swing decisivo")
        self.assertIn("Unknown", [t for _, t, _ in v])
        self.assertIn("U-012", [t for _, t, _ in v])
        self.assertIn("decisivo", [t for _, t, _ in v])

    def test_english_kernel_words_are_jargon_in_lower_case_too(self):
        self.assertIn("Pack", [t for _, t, _ in violations("Fase: discovery · pack: pp")])
        self.assertIn("Discovery", [t for _, t, _ in violations("Fase: discovery · pack: pp")])

    def test_jargon_in_backticks_is_still_jargon(self):
        self.assertIn("Unknown", [t for _, t, _ in violations("linhas `Unknown` abertas: 3")])
        self.assertEqual(violations("ver `shared-understanding.md` e `/status --check`"), [])


class TestCommandOutputs(unittest.TestCase):
    def test_every_command_skill_marks_its_user_output(self):
        for name in COMMAND_SKILLS:
            md = read(".claude", "skills", name, "SKILL.md")
            blocks = user_output_blocks(md)
            self.assertTrue(blocks, name + " has no ```user-output block")

    def test_user_output_speaks_business_language(self):
        terms = glossary_terms()
        for name in COMMAND_SKILLS:
            md = read(".claude", "skills", name, "SKILL.md")
            for block in user_output_blocks(md):
                v = violations(block, terms)
                self.assertEqual(v, [], "%s: %s" % (name, v[:5]))

    def test_the_last_block_closes_with_a_seguir(self):
        for name in COMMAND_SKILLS:
            md = read(".claude", "skills", name, "SKILL.md")
            last = user_output_blocks(md)[-1]
            tail = [l for l in last.splitlines() if l.strip()][-1]
            self.assertTrue(tail.lstrip().startswith("A seguir:"), "%s ends with: %s" % (name, tail))

    def test_status_opens_with_the_three_lines(self):
        md = read(".claude", "skills", "aisa-status", "SKILL.md")
        first = [l.strip() for l in user_output_blocks(md)[0].splitlines() if l.strip()][:3]
        self.assertTrue(first[0].startswith("Onde estamos:"), first)
        self.assertTrue(first[1].startswith("O que falta para o próximo passo:"), first)
        self.assertTrue(first[2].startswith("O que tens de fazer tu:"), first)

    def test_resume_inherits_the_language_and_the_opening(self):
        cmd = read(".claude", "commands", "resume.md")
        self.assertIn("Onde estamos", cmd)
        self.assertIn("como se diz", cmd.lower())

    def test_claude_md_carries_both_rules(self):
        self.assertIn("## Duas línguas", CLAUDE_MD)
        self.assertIn("## Entrada sem comando", CLAUDE_MD)
        self.assertIn("aisa-orient", CLAUDE_MD)
        self.assertIn("A seguir:", CLAUDE_MD)


class TestDashboardLabels(unittest.TestCase):
    SRC = read("library", "kernel", "tools", "dashboard.py")

    def test_rendered_labels_speak_business_language(self):
        terms = glossary_terms()
        bad = []
        for label in dashboard_labels(self.SRC):
            for _, tok, _ in violations(label, terms):
                bad.append((label, tok))
        self.assertEqual(bad, [], bad[:10])

    def test_kernel_terms_survive_in_tooltips(self):
        # The kernel term is not deleted — it moves to the tooltip (P-13 mechanics 5).
        self.assertTrue(re.search(r'title="[^"]*Unknown[^"]*"', self.SRC), "no Unknown tooltip")
        self.assertTrue(re.search(r'title="[^"]*[Tt]ripwire[^"]*"', self.SRC), "no tripwire tooltip")


class TestComoUsar(unittest.TestCase):
    def test_exists_fits_one_page_and_speaks_business_language(self):
        md = read("docs", "COMO-USAR.md")
        body = re.sub(r"```.*?```", "", md, flags=re.S)
        self.assertLessEqual(len([l for l in body.splitlines() if l.strip()]), 70, "more than one page")
        v = violations(body)
        self.assertEqual(v, [], v[:8])
        for needle in ("o que é", "o que se espera de", "como começ", "a seguir"):
            self.assertIn(needle, body.lower(), needle)


class TestOrient(unittest.TestCase):
    ORIENT = read(".claude", "skills", "aisa-orient", "SKILL.md")
    START = read(".claude", "skills", "aisa-start", "SKILL.md")

    def test_orient_never_writes_and_never_names_a_vendor(self):
        low = self.ORIENT.lower()
        self.assertIn("never creates or writes", low)
        self.assertIn("`aisa-start` writes", low)
        for vendor in ("power platform", "dataverse", "outsystems", "mendix", "canvas app", "power automate"):
            self.assertNotIn(vendor, low, vendor)

    def test_orient_covers_the_five_mechanics(self):
        for needle in ("cinco linhas", "AskUserQuestion", "enquadramento", "slug", "já existe"):
            self.assertIn(needle.lower(), self.ORIENT.lower(), needle)

    def test_start_accepts_a_pre_collected_enquadramento(self):
        self.assertIn("aisa-orient", self.START)
        self.assertIn("do not ask again", self.START.lower())


class TestTechnicalTerminologyIsNeverTranslated(unittest.TestCase):
    """P-20 — a product name is a literal; paraphrasing it is a defect."""

    def test_glossary_declares_the_rule_and_the_table(self):
        self.assertIn("Technical terminology is never translated", GLOSSARY)
        self.assertIn("**Forbidden paraphrases**", GLOSSARY)
        table = forbidden_paraphrases()
        self.assertTrue(table, "the forbidden-paraphrase table did not parse")
        for literal in ("Dataverse", "Azure SQL", "SharePoint"):
            self.assertIn(literal, table, literal)

    def test_a_paraphrase_is_caught_and_the_literal_is_not(self):
        self.assertEqual(
            [p for p, _ in paraphrase_violations("a app model-driven sobre a loja governada")],
            ["loja governada"],
        )
        self.assertEqual(paraphrase_violations("a app model-driven sobre Dataverse"), [])

    def test_no_command_skill_paraphrases_a_product_name(self):
        table = forbidden_paraphrases()
        for name in COMMAND_SKILLS:
            md = read(".claude", "skills", name, "SKILL.md")
            for block in user_output_blocks(md):
                v = paraphrase_violations(block, table)
                self.assertEqual(v, [], "%s: %s" % (name, v))

    def test_the_dashboard_paraphrases_no_product_name(self):
        table = forbidden_paraphrases()
        src = read("library", "kernel", "tools", "dashboard.py")
        for label in dashboard_labels(src):
            v = paraphrase_violations(label, table)
            self.assertEqual(v, [], "dashboard label %r: %s" % (label, v))

    def test_the_user_page_paraphrases_no_product_name(self):
        table = forbidden_paraphrases()
        v = paraphrase_violations(read("docs", "COMO-USAR.md"), table)
        self.assertEqual(v, [], v)


if __name__ == "__main__":
    unittest.main()
