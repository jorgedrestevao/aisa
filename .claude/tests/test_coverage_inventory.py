"""Fase 2 da reconciliação/cobertura — o denominador, os locators e a CLI `inventory`.

O que estes testes protegem, e a falha observável de cada um:

  denominador     o inventário sai dos FICHEIROS. Um registo escrito pelo agente não o
                  define, não o encolhe e não o cala — se definisse, bastava omitir ao
                  mesmo tempo o requisito e a linha de revisão para obter falso verde.
                  O engagement da fixture não tem `_coverage/` nenhum, e o inventário
                  sai na mesma.
  expectativa     o motor reproduz, chave a chave e pela mesma ordem, as 79 unidades que
                  a fase 1 pinou em `inventory-expected.json`. São duas implementações
                  independentes da mesma derivação, e é isso que faz da expectativa uma
                  prova em vez de um eco.
  granularidade   colunas quando há rascunho de campos, folhas quando não há, nunca as
                  duas; entrada de dicionário sem dados conta; formato sem extractor
                  entra como limitação e nunca desaparece.
  aprovação       o registo de uma aprovação sai do inventário por inteiro, e nenhuma
                  outra linha `D-*` sai com ele.
  locators        resolvem para exactamente um nó, ou devolvem o código. Zero e dois
                  nunca são um fallback silencioso, e um caminho para fora da fronteira
                  é recusado sem ler.
  CLI             read-only de verdade: correr duas vezes não muda um byte.

    python .claude/tests/test_coverage_inventory.py
"""

import ast
import json
import os
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
C = runpy.run_path(str(ROOT / "library" / "kernel" / "tools" / "coverage.py"))
FIX = Path(__file__).resolve().parent / "fixtures" / "coverage"
ENG = FIX / "fx-coverage-f06"
CLI = ROOT / "library" / "kernel" / "tools" / "coverage.py"


def copy_engagement(tmp, name="fx-coverage-f06"):
    dst = Path(tmp) / name
    shutil.copytree(ENG, dst)
    return dst


def keys(inv):
    return [u["unit_key"] for u in inv["units"]]


def run_cli(args, cwd=None, env=None):
    e = dict(os.environ)
    e.update(env or {})
    # `text=True` sozinho descodifica com a codificacao local (cp1252 no Windows) e
    # transforma os acentos da CLI em mojibake -- a asserçao falhava por causa da
    # captura, nao do programa.
    return subprocess.run([sys.executable, "-B", str(CLI)] + args,
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace", cwd=cwd, env=e)


def tree_digest(root: Path) -> dict:
    import hashlib
    out = {}
    for p in sorted(Path(root).rglob("*")):
        if p.is_file():
            out[p.relative_to(root).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


# --------------------------------------------------------------- o denominador

class Denominator(unittest.TestCase):

    def setUp(self):
        self.inv = C["build_inventory"](ENG)

    def test_it_matches_the_phase_one_expectation_key_for_key(self):
        """Duas derivações independentes, o mesmo resultado — ou uma delas está errada."""
        expected = json.loads((FIX / "inventory-expected.json").read_text(encoding="utf-8"))
        self.assertEqual(keys(self.inv), [u["unit_key"] for u in expected["units"]])
        self.assertEqual(self.inv["total"], expected["total"])
        self.assertEqual(self.inv["counts_by_class"], expected["counts_by_class"])

    def test_it_is_built_without_any_coverage_record(self):
        self.assertFalse((ENG / "_coverage").exists())
        self.assertEqual(self.inv["total"], 79)

    def test_a_record_cannot_shrink_it(self):
        """Colocar um registo no engagement não tira uma única unidade ao denominador."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            (eng / "_coverage").mkdir()
            (eng / "_coverage" / "coverage_v01.json").write_text(
                json.dumps({"schema_version": 1, "stage": "reconciliation",
                            "coverage": [], "source_review": []}), encoding="utf-8")
            after = C["build_inventory"](eng)
        self.assertEqual(set(keys(after)), set(keys(self.inv)))

    def test_unit_keys_are_unique(self):
        self.assertEqual(len(keys(self.inv)), len(set(keys(self.inv))))

    def test_no_diagnostic_on_a_healthy_engagement(self):
        self.assertEqual(self.inv["diagnostics"], [])

    def test_the_identity_survives_a_content_change(self):
        """Contrato §5.2: a chave deriva do caminho e do selector, não do conteúdo."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            p = eng / "frame.md"
            p.write_text(p.read_text(encoding="utf-8") + "\numa linha nova\n",
                         encoding="utf-8")
            after = C["build_inventory"](eng)
        self.assertEqual(set(keys(after)), set(keys(self.inv)))
        was = {u["unit_key"]: u["sha256"] for u in self.inv["units"]}["frame.md"]
        now = {u["unit_key"]: u["sha256"] for u in after["units"]}["frame.md"]
        self.assertNotEqual(was, now, "o digest tem de mudar, a identidade não")


# ------------------------------------------------------------------ granularidade

class Granularity(unittest.TestCase):

    def setUp(self):
        self.inv = C["build_inventory"](ENG)
        self.keys = set(keys(self.inv))

    def test_a_workbook_with_a_fields_draft_enters_by_column(self):
        cols = [k for k in self.keys
                if k.startswith("_capture/registo-de-lotes.xlsx.fields-draft.json#")
                and "entries_without_data" not in k]
        self.assertEqual(len(cols), 18)

    def test_that_same_workbook_does_not_also_enter_by_sheet(self):
        """Contar folhas de um workbook que já entrou por coluna contaria duas vezes."""
        sheets = [k for k in self.keys
                  if k.startswith("_capture/registo-de-lotes.xlsx.extraction.json#")]
        self.assertEqual(sheets, [])

    def test_a_workbook_without_a_fields_draft_enters_by_sheet(self):
        sheets = sorted(k for k in self.keys
                        if k.startswith("_capture/registo-de-lotes-2024.xlsx"
                                        ".extraction.json#sheets["))
        self.assertEqual(len(sheets), 2)

    def test_homonymous_sheets_in_two_workbooks_do_not_collide(self):
        hits = [k for k in self.keys if k.endswith("#sheets[name=Resumo Aditivos]")]
        self.assertEqual(len(hits), 1)
        self.assertIn("registo-de-lotes-2024", hits[0])

    def test_a_dictionary_entry_without_data_is_a_unit(self):
        self.assertIn("_capture/registo-de-lotes.xlsx.fields-draft.json"
                      "#dictionary/entries_without_data/Custo_Posto_D", self.keys)

    def test_the_repeated_column_group_keeps_its_members_separate(self):
        """Agrupar é do revisor; o denominador enumera. Um membro omitido é detectável."""
        members = [k for k in self.keys if k.endswith(("/F", "/G", "/H"))
                   and "Entradas" in k]
        self.assertEqual(len(members), 3)

    def test_an_unsupported_format_is_a_limitation_never_a_disappearance(self):
        self.assertIn("inputs/fluxo-de-libertacao.pptx", self.keys)
        lims = [l for l in self.inv["limitations"]
                if l["unit_key"] == "inputs/fluxo-de-libertacao.pptx"]
        self.assertEqual(len(lims), 1)
        self.assertEqual(lims[0]["code"], "COV-CAPTURE-LIMIT")
        for field in ("reason", "impact", "action"):
            self.assertTrue(lims[0][field].strip(), field)

    def test_a_repeated_answer_section_gets_an_explicit_ordinal(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            p = eng / "answers.md"
            p.write_text(p.read_text(encoding="utf-8") +
                         "\n## U-004 — 2026-03-12 (segunda resposta)\n"
                         "- **Resposta**: \"Corrijo: também vai por email às terças.\"\n",
                         encoding="utf-8")
            after = set(keys(C["build_inventory"](eng)))
        self.assertIn("answers.md#U-004[1]", after)
        self.assertIn("answers.md#U-004[2]", after)
        self.assertNotIn("answers.md#U-004", after,
                         "com duas secções, citar sem ordinal deixa de ser uma chave")

    def test_every_input_file_is_a_unit(self):
        want = {"inputs/" + p.name for p in (ENG / "inputs").iterdir()}
        self.assertEqual(want - self.keys, set())


# -------------------------------------------------- o que a aprovação tira, e só isso

APPROVAL_BLOCK = """
## D-003 — Blueprint bp-v03 aprovado

- **Timestamp**: 2026-03-11T09:00:00+01:00
- **Validated by**: owner (Responsavel de Qualidade — fixture, via AskUserQuestion)
"""
APPROVAL_ROW = ("| D-003 | chair | Aprovação do desenho, versão 03; ver decisions.md#D-003 "
                "| decisions.md#D-003 | 2026-03-11 | organizacional | D-01 |\n")


def with_approval(eng: Path) -> Path:
    dec = eng / "decisions.md"
    dec.write_text(dec.read_text(encoding="utf-8") + APPROVAL_BLOCK, encoding="utf-8")
    su = eng / "shared-understanding.md"
    body = su.read_text(encoding="utf-8")
    anchor = "| D-002 | chair |"
    end = body.index("\n", body.index(anchor)) + 1
    su.write_text(body[:end] + APPROVAL_ROW + body[end:], encoding="utf-8")
    return eng


class ApprovalIsNotSourceMaterial(unittest.TestCase):
    """Contrato §6.1 — o registo de uma decisão humana é autoridade, não fonte."""

    def test_the_fixture_starts_without_any_approval(self):
        self.assertEqual(C["approval_ids"](ENG, C["ReaderAdapter"]()), set())

    def test_the_approval_adds_no_unit(self):
        before = set(keys(C["build_inventory"](ENG)))
        with tempfile.TemporaryDirectory() as tmp:
            eng = with_approval(copy_engagement(tmp))
            inv = C["build_inventory"](eng)
        self.assertEqual(set(keys(inv)) - before, set())
        self.assertEqual(before - set(keys(inv)), set())

    def test_both_halves_are_named_in_the_excluded_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = with_approval(copy_engagement(tmp))
            inv = C["build_inventory"](eng)
        excluded = {e["unit_key"] for e in inv["excluded"]}
        self.assertEqual(excluded, {"decisions.md#D-003",
                                    "shared-understanding.md#D-003"})
        for e in inv["excluded"]:
            self.assertIn("§6.1", e["reason"])

    def test_no_other_d_row_or_block_is_dropped(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = with_approval(copy_engagement(tmp))
            k = set(keys(C["build_inventory"](eng)))
        for kept in ("decisions.md#D-001", "decisions.md#D-002",
                     "shared-understanding.md#D-002"):
            self.assertIn(kept, k, kept + " saiu do inventário e não devia")

    def test_the_exclusion_is_by_block_kind_not_by_id_prefix(self):
        """Um bloco `D-004` que não seja aprovação continua no inventário."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            dec = eng / "decisions.md"
            dec.write_text(dec.read_text(encoding="utf-8") +
                           "\n## D-004 — Nota de âmbito\n\n- **Timestamp**: "
                           "2026-03-12T09:00:00+01:00\n", encoding="utf-8")
            k = set(keys(C["build_inventory"](eng)))
        self.assertIn("decisions.md#D-004", k)


# ------------------------------------------ segunda volta: as omissões silenciosas


def link_out(inside: Path, outside: Path) -> bool:
    """Cria uma ligação `inside` -> `outside` que atravessa a fronteira.

    Symlink onde há privilégio; junção de directório no Windows, que não precisa.
    Devolve False quando nenhuma das duas está disponível — e aí o teste salta, em vez
    de fingir que provou alguma coisa."""
    try:
        os.symlink(outside, inside, target_is_directory=outside.is_dir())
        return True
    except (OSError, NotImplementedError, AttributeError):
        pass
    if os.name == "nt" and outside.is_dir():
        r = subprocess.run(["cmd", "/c", "mklink", "/J", str(inside), str(outside)],
                           capture_output=True, text=True)
        return r.returncode == 0
    return False


class InputsAreWalkedRecursively(unittest.TestCase):
    """Achado A1 — `iterdir()` deixava as subpastas de `inputs/` fora do denominador.

    A assimetria era a parte perigosa: o manifesto usa `rglob`, por isso o ficheiro
    entrava no hash e não no inventário. O digest mudava, o denominador não, e ninguém
    via a fonte nova."""

    def _with_subfolder(self, tmp):
        eng = copy_engagement(tmp)
        (eng / "inputs" / "extra").mkdir()
        (eng / "inputs" / "extra" / "pedido.txt").write_text(
            "o pedido original, que o dono mandou por escrito\n", encoding="utf-8")
        return eng

    def test_a_file_in_a_subfolder_is_a_unit(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._with_subfolder(tmp)
            k = set(keys(C["build_inventory"](eng)))
        self.assertIn("inputs/extra/pedido.txt", k)

    def test_the_relative_path_is_preserved_in_the_key(self):
        """A subpasta faz parte da identidade: dois `pedido.txt` em pastas diferentes
        são unidades diferentes."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._with_subfolder(tmp)
            (eng / "inputs" / "outra").mkdir()
            (eng / "inputs" / "outra" / "pedido.txt").write_text("outro\n",
                                                                encoding="utf-8")
            k = set(keys(C["build_inventory"](eng)))
        self.assertIn("inputs/extra/pedido.txt", k)
        self.assertIn("inputs/outra/pedido.txt", k)

    def test_inventory_and_manifest_see_the_same_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._with_subfolder(tmp)
            inv = set(keys(C["build_inventory"](eng)))
            man = {s["path"] for s in C["build_manifest"](eng, "reconciliation")}
        self.assertIn("inputs/extra/pedido.txt", inv)
        self.assertIn("inputs/extra/pedido.txt", man)

    def test_it_still_carries_its_capture_limitation(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._with_subfolder(tmp)
            inv = C["build_inventory"](eng)
        lims = [l for l in inv["limitations"]
                if l["unit_key"] == "inputs/extra/pedido.txt"]
        self.assertEqual(len(lims), 1)
        self.assertEqual(lims[0]["code"], "COV-CAPTURE-LIMIT")

    def test_the_note_says_it_came_from_a_subfolder(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._with_subfolder(tmp)
            u = [x for x in C["build_inventory"](eng)["units"]
                 if x["unit_key"] == "inputs/extra/pedido.txt"][0]
        self.assertIn("subpasta", u["note"])


class UnreadableIsNotEmpty(unittest.TestCase):
    """Achado A2 — erro de leitura virava texto vazio, e a fonte desaparecia calada.

    Ausente, vazio e ilegível são três coisas diferentes. A terceira é a única que
    significa «isto existe e não entrou no denominador»."""

    BAD = b"\xff\xfe\x00 bytes que nao sao utf-8 \xc3\x28"

    def _corrupt(self, tmp, name):
        eng = copy_engagement(tmp)
        (eng / name).write_bytes(self.BAD)
        return eng

    def test_the_three_states_are_distinguished(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            (eng / "vazio.md").write_text("", encoding="utf-8")
            (eng / "mau.md").write_bytes(self.BAD)
            self.assertEqual(C["read_source"](eng / "nao-existe.md")[1], "absent")
            self.assertEqual(C["read_source"](eng / "vazio.md")[1], "empty")
            self.assertEqual(C["read_source"](eng / "mau.md")[1], "unreadable")
            self.assertEqual(C["read_source"](eng / "frame.md")[1], "ok")

    def test_an_unreadable_answers_file_is_a_blocking_diagnostic(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._corrupt(tmp, "answers.md")
            inv = C["build_inventory"](eng)
        self.assertEqual([k for k in keys(inv) if k.startswith("answers.md")], [])
        d = [x for x in inv["diagnostics"] if x["where"] == "answers.md"]
        self.assertEqual(len(d), 1)
        self.assertTrue(d[0]["blocking"])
        self.assertEqual(d[0]["level"], "error")
        self.assertFalse(inv["complete"])

    def test_the_same_holds_for_the_su_and_the_decisions(self):
        for name in ("shared-understanding.md", "decisions.md"):
            with tempfile.TemporaryDirectory() as tmp:
                eng = self._corrupt(tmp, name)
                inv = C["build_inventory"](eng)
            d = [x for x in inv["diagnostics"] if x["where"] == name]
            self.assertEqual(len(d), 1, name)
            self.assertTrue(d[0]["blocking"], name)
            self.assertFalse(inv["complete"], name)

    def test_an_unreadable_capture_artefact_blocks_too(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            (eng / "_capture" / "registo-de-lotes.xlsx.fields-draft.json").write_bytes(
                self.BAD)
            inv = C["build_inventory"](eng)
        self.assertEqual([k for k in keys(inv) if "fields-draft" in k], [])
        self.assertFalse(inv["complete"])
        self.assertTrue(any(x.get("blocking") for x in inv["diagnostics"]))

    def test_an_empty_source_is_visible_but_not_blocking(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            (eng / "answers.md").write_text("", encoding="utf-8")
            inv = C["build_inventory"](eng)
        d = [x for x in inv["diagnostics"] if x["where"] == "answers.md"]
        self.assertEqual(len(d), 1)
        self.assertFalse(d[0]["blocking"])
        self.assertTrue(inv["complete"])

    def test_a_healthy_engagement_is_complete(self):
        inv = C["build_inventory"](ENG)
        self.assertTrue(inv["complete"])
        self.assertEqual(inv["blocking_diagnostics"], 0)

    def test_the_cli_exits_four_on_an_incomplete_denominator(self):
        """Sair 0 com uma fonte ilegível era dar por bom um denominador já sabido
        incompleto."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._corrupt(tmp, "answers.md")
            r = run_cli(["inventory", "--engagement", str(eng)])
        self.assertEqual(r.returncode, 4)
        self.assertIn("DENOMINADOR INCOMPLETO", r.stdout)


class EveryReadCrossesTheBoundary(unittest.TestCase):
    """Achado A4 — a fronteira só protegia os locators; inventário e manifesto liam
    directo, e a lista de autoridades abrangia todo o kernel e todos os pacotes."""

    def _with_link(self, tmp):
        outside = Path(tmp) / "fora"
        outside.mkdir()
        (outside / "segredo.txt").write_text("conteudo de fora do engagement\n",
                                             encoding="utf-8")
        eng = copy_engagement(tmp)
        return eng, link_out(eng / "inputs" / "atalho", outside)

    def test_a_link_out_of_the_engagement_is_not_inventoried(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng, made = self._with_link(tmp)
            if not made:
                self.skipTest("ligações indisponíveis neste ambiente")
            inv = C["build_inventory"](eng)
        self.assertEqual([k for k in keys(inv) if "segredo" in k], [],
                         "conteúdo de fora entrou no denominador")

    def test_it_is_reported_instead_of_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng, made = self._with_link(tmp)
            if not made:
                self.skipTest("ligações indisponíveis neste ambiente")
            inv = C["build_inventory"](eng)
        out = [d for d in inv["diagnostics"] if "fora do engagement" in d["message"]]
        self.assertTrue(out, "a fuga foi ignorada em silêncio")
        self.assertTrue(all(d["blocking"] for d in out))
        self.assertFalse(inv["complete"])

    def test_it_is_not_hashed_into_the_manifest_either(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng, made = self._with_link(tmp)
            if not made:
                self.skipTest("ligações indisponíveis neste ambiente")
            man = {s["path"] for s in C["build_manifest"](eng, "reconciliation")}
        self.assertEqual([p for p in man if "segredo" in p], [])

    def test_the_authority_list_is_narrow(self):
        """Só os contratos e templates de síntese do kernel, e os templates do pacote
        ACTIVO. Um motor não é autoridade de leitura de uma revisão."""
        allowed = ("library/kernel/coverage-contract.md",
                   "library/kernel/blueprint-contract.md",
                   "library/packs/pp/deliverable-templates/solution-blueprint.template.md",
                   "library/packs/pp/architecture-templates/architecture-core.md")
        refused = ("library/kernel/tools/dashboard.py",
                   "library/kernel/tools/coverage.py",
                   "library/packs/pp/pack.yaml",
                   "library/packs/pp/question-bank.md")
        for rel in allowed:
            self.assertTrue((ROOT / rel).is_file(), rel)
            C["safe_path"](ENG, str(ROOT / rel))
        for rel in refused:
            if not (ROOT / rel).is_file():
                continue
            with self.assertRaises(C["CoverageError"], msg=rel):
                C["safe_path"](ENG, str(ROOT / rel))

    def test_another_pack_is_not_an_authority_for_this_engagement(self):
        other = ROOT / "library" / "packs" / "mendix" / "pack.yaml"
        if not other.is_file():
            self.skipTest("pacote mendix não montado")
        with self.assertRaises(C["CoverageError"]):
            C["safe_path"](ENG, str(other))


# ------------------------------------------------------------------ tier de texto

TEXT_MD = """<!-- aisa.capture.text-extraction | text_extract.py 1.0.1 -->
# Source: reuniao.vtt

- status: **ok**

---

[00:00:04-00:00:11] O resumo sai todos os dias antes das nove.

[00:01:20-00:01:31] O ficheiro fica gravado na area partilhada.

[00:02:05-00:02:12] Quem regista nao liberta, nunca.
"""


class TextTier(unittest.TestCase):
    """Uma fonte normalizada que ninguém inventaria nunca pode ser dada como não revista.

    A granularidade é **o documento**, não a passagem: 620 excertos de uma gravação são a
    versão textual de «uma pergunta por célula», que o contrato §6.2 proíbe no Excel pela
    mesma razão. As passagens continuam citáveis por locator — um locator resolúvel e uma
    unidade do denominador são coisas diferentes."""

    def _with_transcript(self, tmp):
        eng = copy_engagement(tmp)
        (eng / "inputs" / "reuniao.vtt").write_text(
            "WEBVTT\n\n00:00:04.000 --> 00:00:11.000\nO resumo sai todos os dias.\n",
            encoding="utf-8")
        (eng / "_capture" / "reuniao.vtt.text.md").write_text(TEXT_MD, encoding="utf-8")
        return eng

    def test_the_normalised_document_is_one_unit(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._with_transcript(tmp)
            inv = C["build_inventory"](eng)
        units = [u for u in inv["units"] if u["class"] == "text-extraction"]
        self.assertEqual(len(units), 1)
        self.assertEqual(units[0]["unit_key"], "_capture/reuniao.vtt.text.md")

    def test_the_note_says_how_many_passages_there_are(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._with_transcript(tmp)
            inv = C["build_inventory"](eng)
        note = [u for u in inv["units"] if u["class"] == "text-extraction"][0]["note"]
        self.assertIn("3 passagem", note)

    def test_the_raw_transcript_is_a_unit_too_and_is_supported(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._with_transcript(tmp)
            inv = C["build_inventory"](eng)
        k = {u["unit_key"] for u in inv["units"]}
        self.assertIn("inputs/reuniao.vtt", k)
        self.assertEqual([l for l in inv["limitations"]
                          if l["unit_key"] == "inputs/reuniao.vtt"], [],
                         "o .vtt tem extractor — não é uma limitação de captura")

    def test_a_passage_resolves_by_its_start_timestamp(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._with_transcript(tmp)
            r = C["resolve_target"](eng, {"file": "_capture/reuniao.vtt.text.md",
                                          "selector": "00:01:20"})
        self.assertTrue(r["ok"], r)

    def test_a_passage_that_does_not_exist_is_invalid_never_the_nearest_one(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._with_transcript(tmp)
            r = C["resolve_target"](eng, {"file": "_capture/reuniao.vtt.text.md",
                                          "selector": "09:99:99"})
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "COV-INVALID-TARGET")

    def test_the_document_itself_resolves_without_a_selector(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._with_transcript(tmp)
            r = C["resolve_unit"](eng, "_capture/reuniao.vtt.text.md")
        self.assertTrue(r["ok"], r)

    def test_a_changed_transcript_makes_the_inventory_digest_move(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._with_transcript(tmp)
            before = C["inventory_digest"](C["build_inventory"](eng))
            p = eng / "_capture" / "reuniao.vtt.text.md"
            p.write_text(p.read_text(encoding="utf-8") +
                         "\n[00:03:00-00:03:10] Mais uma obrigacao.\n", encoding="utf-8")
            after = C["inventory_digest"](C["build_inventory"](eng))
        self.assertNotEqual(before, after)


# --------------------------- terceira volta: a fronteira cobre TODAS as leituras


class NoReadEscapesTheGate(unittest.TestCase):
    """A correcção anterior validava a ENUMERAÇÃO e deixava as fontes principais a serem
    lidas por `eng / nome`. Um caminho recusado na enumeração voltava a entrar por outra
    via, e emitir um diagnóstico **depois** não cumpre a obrigação de recusar **antes**.

    `guarded_read`, `guarded_read_json` e `guarded_sha256` são agora a única porta, e
    `refused` é um estado de leitura como `absent`, `empty` e `unreadable`."""

    MAIN = ("context.json", "enquadramento.md", "answers.md",
            "shared-understanding.md", "decisions.md")

    def test_the_gate_refuses_an_escaping_path_for_every_main_source(self):
        for name in self.MAIN:
            text, state = C["guarded_read"](ENG, "../" + name)
            self.assertEqual(state, "refused", name)
            self.assertEqual(text, "", name + ": devolveu conteúdo de fora")

    def test_the_json_gate_refuses_too(self):
        data, state = C["guarded_read_json"](ENG, "../../setup.json")
        self.assertEqual(state, "refused")
        self.assertIsNone(data)

    def test_a_refused_file_is_never_hashed(self):
        sha, state = C["guarded_sha256"](ENG, "../../README.md")
        self.assertEqual(state, "refused")
        self.assertEqual(sha, "")

    def test_the_gate_still_lets_the_real_sources_through(self):
        for name in self.MAIN:
            _text, state = C["guarded_read"](ENG, name)
            self.assertEqual(state, "ok", name)

    def test_refused_is_a_blocking_diagnostic_not_a_silence(self):
        d = C["_source_diagnostic"]("x.md", "refused", "as coisas")
        self.assertIsNotNone(d)
        self.assertTrue(d["blocking"])
        self.assertIn("sem ler", d["message"])

    def test_the_state_file_is_checked_against_the_root(self):
        """`_state.json` declara o pacote de que a lista de autoridades depende, por isso
        leva a verificação que não depende dele: só a raiz."""
        data, state = C["engagement_state"](ENG)
        self.assertEqual(state, "ok")
        self.assertEqual(data.get("pack"), "pp")

    def test_the_capture_is_walked_from_the_validated_list_not_a_glob(self):
        """Um glob volta a enumerar o disco e dá a volta à fronteira."""
        src = (ROOT / "library" / "kernel" / "tools" / "coverage.py").read_text(
            encoding="utf-8")
        self.assertNotIn('cap.glob(', src,
                         "o inventário voltou a enumerar `_capture/` por glob")


class NoDirectReadSurvivesInTheEngine(unittest.TestCase):
    """A prova que falta às outras: **não sobra nenhuma leitura directa no motor**.

    Os testes de ligação apanham a fuga pela ENUMERAÇÃO, e os de caminho a fuga pela
    PORTA. Nenhum dos dois impede alguém de, amanhã, voltar a escrever
    `read_source(eng / "answers.md")` numa função nova — e foi exactamente assim que este
    defeito nasceu. Este teste lê a árvore sintáctica e falha nesse instante.

    As duas excepções são nomeadas e têm razão escrita no próprio motor:
    `engagement_state` (é ele que declara o pacote de que a lista de autoridades depende,
    por isso leva a verificação que não depende dele) e os helpers `guarded_*`, que são a
    porta."""

    ENGINE = ROOT / "library" / "kernel" / "tools" / "coverage.py"
    # Funções que lêem fontes do engagement e têm de passar pela porta.
    GUARDED_FUNCTIONS = ("build_inventory", "build_manifest", "su_fingerprint",
                         "decision_fingerprint", "compute_basis", "approval_ids",
                         "active_pack")
    # Leitores crus: legítimos dentro da porta, proibidos fora dela.
    RAW_READERS = {"read_source", "read_json_source", "sha256_file", "_read", "_read_json"}
    ALLOWED = {"guarded_read", "guarded_read_json", "guarded_sha256", "engagement_state",
               "engagement_files", "safe_path", "resolve_target", "resolve_unit",
               "current_target", "_resolve_yaml", "_resolve_md", "_resolve_json",
               "_resolve_passage", "_resolve_fields_draft",
               # Fase 3: a porta do rascunho. Um rascunho é um argumento EXPLÍCITO de uma
               # operação explícita (`finalize --draft`, `report --record`) e vive, por
               # desenho, num temporário fora do engagement -- `safe_path` recusaria todos.
               # A excepção é UMA função, nomeada, e tem disciplina própria testada em
               # `test_coverage_contract.py::TheDraftDoor`.
               "read_draft"}

    def _calls_in(self, tree, name):
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == name:
                for sub in ast.walk(node):
                    if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name):
                        yield sub.func.id, sub.lineno
                return
        self.fail("função %r não existe no motor" % name)

    def test_the_source_reading_functions_only_read_through_the_gate(self):
        tree = ast.parse(self.ENGINE.read_text(encoding="utf-8"))
        bad = []
        for fn in self.GUARDED_FUNCTIONS:
            for called, line in self._calls_in(tree, fn):
                if called in self.RAW_READERS:
                    bad.append("%s:%d chama %s()" % (fn, line, called))
        self.assertEqual(bad, [],
                         "leitura directa fora da porta — um caminho recusado na "
                         "enumeração volta a entrar por aqui")

    def test_the_gate_itself_is_the_only_place_that_reads_raw(self):
        """Quem chama os leitores crus tem de ser a porta, ou uma excepção nomeada."""
        tree = ast.parse(self.ENGINE.read_text(encoding="utf-8"))
        offenders = set()
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef):
                continue
            for sub in ast.walk(node):
                if (isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name)
                        and sub.func.id in self.RAW_READERS
                        and node.name not in self.ALLOWED
                        and node.name not in self.RAW_READERS):
                    offenders.add(node.name)
        self.assertEqual(offenders, set(),
                         "estas funções lêem sem passar pela porta: %s" % sorted(offenders))

    def test_the_named_exceptions_are_documented_in_the_engine(self):
        src = self.ENGINE.read_text(encoding="utf-8")
        self.assertIn("verificação de **raiz apenas**", src,
                      "`engagement_state` perdeu a razão escrita da sua excepção")
        self.assertIn("única porta de leitura", src)
        self.assertIn("ÚNICA porta para um ficheiro que o operador nomeia", src,
                      "`read_draft` perdeu a razão escrita da sua excepção")


class LinkedMainSourcesAreRefused(unittest.TestCase):
    """O mesmo, com ligações reais — não só com caminhos escritos à mão.

    Symlink de ficheiro precisa de um privilégio que o Windows não dá aqui; a junção de
    directório não precisa, e atravessa a fronteira da mesma maneira. Por isso o cenário
    é: **uma pasta do engagement é uma junção para fora**, e os ficheiros principais que
    lá vivem têm de ser recusados."""

    def _engagement_with_linked_dir(self, tmp, dirname, files):
        outside = Path(tmp) / ("fora-" + dirname.strip("/").replace("/", "-"))
        outside.mkdir()
        for name, body in files.items():
            (outside / name).write_text(body, encoding="utf-8")
        eng = copy_engagement(tmp)
        victim = eng / dirname
        if victim.exists():
            shutil.rmtree(victim)
        return eng, link_out(victim, outside), outside

    def test_a_linked_capture_directory_is_refused_and_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng, made, _out = self._engagement_with_linked_dir(
                tmp, "_capture", {"process-model.md": "# PM\n\nPM-001 regra\n"})
            if not made:
                self.skipTest("ligações indisponíveis neste ambiente")
            inv = C["build_inventory"](eng)
        self.assertEqual([k for k in keys(inv) if k.startswith("_capture/")], [],
                         "conteúdo de fora entrou pelo `_capture/`")
        self.assertFalse(inv["complete"])
        self.assertTrue(any("fora do engagement" in d["message"]
                            for d in inv["diagnostics"]))

    def test_a_linked_lens_outputs_directory_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng, made, _out = self._engagement_with_linked_dir(
                tmp, "lens-outputs", {"data.md": "# lente de fora\n"})
            if not made:
                self.skipTest("ligações indisponíveis neste ambiente")
            inv = C["build_inventory"](eng)
        self.assertEqual([k for k in keys(inv) if k.startswith("lens-outputs/")], [])
        self.assertFalse(inv["complete"])

    def test_the_manifest_refuses_the_same_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng, made, _out = self._engagement_with_linked_dir(
                tmp, "_capture", {"process-model.md": "# PM\n"})
            if not made:
                self.skipTest("ligações indisponíveis neste ambiente")
            man = {s["path"] for s in C["build_manifest"](eng, "reconciliation")}
        self.assertEqual([p for p in man if p.startswith("_capture/")], [],
                         "o manifesto hasheou o que o inventário recusou")

    def test_the_fingerprints_do_not_read_through_a_link_either(self):
        """A SU e as decisões entram na base por fingerprint: a porta tem de valer lá."""
        with tempfile.TemporaryDirectory() as tmp:
            outside = Path(tmp) / "fora-raiz"
            outside.mkdir()
            (outside / "shared-understanding.md").write_text(
                "# SU de fora\n\n## Confirmed\n\n| id | lens | claim |\n|---|---|---|\n"
                "| C-900 | x | inventado |\n", encoding="utf-8")
            (outside / "decisions.md").write_text(
                "# Decisions\n\n## D-900 — Adopt O-009\n\n- **Chosen option**: O-009\n",
                encoding="utf-8")
            eng = copy_engagement(tmp)
            sub = eng / "emprestado"
            if not link_out(sub, outside):
                self.skipTest("ligações indisponíveis neste ambiente")
            readers = C["ReaderAdapter"]()
            text, state = C["guarded_read"](eng, "emprestado/shared-understanding.md")
        self.assertEqual(state, "refused")
        self.assertEqual(text, "")


# ----------------------------------------------------------------------- locators

class Locators(unittest.TestCase):

    def resolve(self, file, selector):
        return C["resolve_target"](ENG, {"file": file, "selector": selector})

    def test_a_blueprint_node_resolves(self):
        r = self.resolve("_blueprint/ux-blueprint_v02.yaml",
                         "architecture/compositions[component=resumo-aditivos-publicacao]")
        self.assertTrue(r["ok"], r)
        self.assertEqual(r["count"], 1)

    def test_a_nested_field_resolves(self):
        r = self.resolve("_blueprint/ux-blueprint_v02.yaml",
                         "architecture/record_authority[key=publicacoes]"
                         "/fields[name=local_publicacao]")
        self.assertTrue(r["ok"], r)

    def test_a_node_that_does_not_exist_is_invalid_never_silent(self):
        r = self.resolve("_blueprint/ux-blueprint_v01.yaml",
                         "architecture/compositions[component=resumo-aditivos-publicacao]")
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "COV-INVALID-TARGET")
        self.assertEqual(r["count"], 0)
        self.assertTrue(r["reason"])

    def test_a_screen_resolves_and_a_missing_one_does_not(self):
        self.assertTrue(self.resolve("_blueprint/ux-blueprint_v02.yaml",
                                     "screens[name=ResumoAditivosConsultaScreen]")["ok"])
        bad = self.resolve("_blueprint/ux-blueprint_v01.yaml",
                           "screens[name=ResumoAditivosConsultaScreen]")
        self.assertEqual(bad["code"], "COV-INVALID-TARGET")

    def test_an_su_row_resolves_by_id(self):
        self.assertTrue(self.resolve("shared-understanding.md", "C-007")["ok"])

    def test_an_id_that_is_not_in_the_su_is_invalid(self):
        r = self.resolve("shared-understanding.md", "C-999")
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "COV-INVALID-TARGET")

    def test_a_deliverable_section_and_one_of_its_rows_resolve(self):
        self.assertTrue(self.resolve(
            "_render/fx-coverage-f06_solution-blueprint_v02.md", "A3")["ok"])
        self.assertTrue(self.resolve(
            "_render/fx-coverage-f06_solution-blueprint_v02.md",
            "A3/resumo-aditivos-publicacao")["ok"])

    def test_the_row_a_render_dropped_does_not_resolve(self):
        """O id num comentário não é a linha (contrato §8.2)."""
        r = self.resolve("_render/fx-coverage-f06_solution-blueprint_v01.md",
                         "A3/resumo-aditivos-publicacao")
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "COV-INVALID-TARGET")

    def test_an_ambiguous_section_is_a_dead_ref_not_the_first_one(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            p = eng / "answers.md"
            p.write_text(p.read_text(encoding="utf-8") +
                         "\n## U-004 — 2026-03-12 (segunda resposta)\n- x\n",
                         encoding="utf-8")
            r = C["resolve_target"](eng, {"file": "answers.md", "selector": "U-004"})
            ok = C["resolve_target"](eng, {"file": "answers.md", "selector": "U-004[2]"})
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "COV-DEAD-REF")
        self.assertEqual(r["count"], 2)
        self.assertTrue(ok["ok"], "o ordinal explícito resolve")

    def test_an_excel_column_resolves_and_a_missing_one_does_not(self):
        base = "_capture/registo-de-lotes.xlsx.fields-draft.json"
        self.assertTrue(self.resolve(base, "Resumo Aditivos/D")["ok"])
        self.assertFalse(self.resolve(base, "Resumo Aditivos/ZZ")["ok"])
        self.assertFalse(self.resolve(base, "Folha Que Nao Existe/A")["ok"])

    def test_every_inventory_unit_resolves(self):
        """Se o motor inventaria uma unidade, tem de a saber encontrar outra vez."""
        bad = []
        for u in C["build_inventory"](ENG)["units"]:
            if not C["resolve_unit"](ENG, u["unit_key"])["ok"]:
                bad.append(u["unit_key"])
        self.assertEqual(bad, [])


class PathBoundary(unittest.TestCase):
    """Contrato §5.3 — recusado **sem ler**."""

    def test_traversal_is_refused(self):
        r = C["resolve_target"](ENG, {"file": "../../../etc/passwd", "selector": ""})
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "COV-INVALID-TARGET")
        self.assertIn("fronteira", r["reason"])

    def test_a_relative_escape_inside_the_path_is_refused(self):
        r = C["resolve_target"](ENG, {"file": "_blueprint/../../../setup.py",
                                      "selector": ""})
        self.assertFalse(r["ok"])

    def test_an_absolute_path_outside_the_engagement_is_refused(self):
        r = C["resolve_target"](ENG, {"file": str(ROOT / "README.md"), "selector": ""})
        self.assertFalse(r["ok"])

    def test_a_repository_authority_is_allowed(self):
        p = "library/packs/pp/deliverable-templates/solution-blueprint.template.md"
        self.assertTrue((ROOT / p).is_file())
        self.assertTrue(C["safe_path"](ENG, str(ROOT / p)).is_file())

    def test_the_locator_text_is_never_executed(self):
        """Um selector com forma de expressão é dado desconhecido, não código."""
        r = C["resolve_target"](ENG, {"file": "shared-understanding.md",
                                      "selector": "__import__('os').system('echo x')"})
        self.assertFalse(r["ok"])


# ------------------------------------------------------------------------- a CLI

class Cli(unittest.TestCase):

    def test_it_prints_the_inventory_and_exits_zero(self):
        r = run_cli(["inventory", "--engagement", str(ENG)])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("unidades: 79", r.stdout)
        self.assertIn("não uma avaliação", r.stdout)

    def test_json_mode_is_parseable_and_carries_the_units(self):
        r = run_cli(["inventory", "--engagement", str(ENG), "--json"])
        self.assertEqual(r.returncode, 0, r.stderr)
        data = json.loads(r.stdout)
        self.assertEqual(data["total"], 79)
        self.assertEqual(data["artefact"], "aisa.coverage.inventory")
        self.assertEqual(data["contract_version"], "1")

    def test_it_runs_from_an_unrelated_working_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = run_cli(["inventory", "--engagement", str(ENG)], cwd=tmp)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("unidades: 79", r.stdout)

    def test_a_path_with_spaces_and_accents_resolves(self):
        with tempfile.TemporaryDirectory() as tmp:
            odd = Path(tmp) / "raiz com espaços e acentuação"
            odd.mkdir()
            eng = copy_engagement(odd)
            r = run_cli(["inventory", "--engagement", str(eng)])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("unidades: 79", r.stdout)

    def test_a_slug_resolves_under_the_engagements_root(self):
        r = run_cli(["inventory", "--engagement", "fx-coverage-f06"],
                    env={"AISA_ENGAGEMENTS_ROOT": str(FIX)})
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_an_unknown_engagement_exits_three(self):
        r = run_cli(["inventory", "--engagement", "nao-existe"],
                    env={"AISA_ENGAGEMENTS_ROOT": str(FIX)})
        self.assertEqual(r.returncode, 3)
        self.assertIn("não encontrado", r.stderr)

    def test_several_engagements_without_selection_fails_explicitly(self):
        """Contrato/plano: ambiguidade exige argumento. Nunca escolher o primeiro."""
        with tempfile.TemporaryDirectory() as tmp:
            copy_engagement(tmp, "eng-a")
            copy_engagement(tmp, "eng-b")
            r = run_cli(["inventory"], env={"AISA_ENGAGEMENTS_ROOT": tmp})
        self.assertEqual(r.returncode, 2)
        self.assertIn("eng-a", r.stderr)
        self.assertIn("eng-b", r.stderr)

    def test_it_writes_nothing_and_repeats_itself(self):
        """Read-only a sério, e determinístico: T38."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = copy_engagement(tmp)
            before = tree_digest(eng)
            first = run_cli(["inventory", "--engagement", str(eng), "--json"])
            mid = tree_digest(eng)
            second = run_cli(["inventory", "--engagement", str(eng), "--json"])
            after = tree_digest(eng)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(before, mid, "a primeira execução escreveu no engagement")
        self.assertEqual(before, after, "a segunda execução escreveu no engagement")
        self.assertEqual(first.stdout, second.stdout, "o resultado não é determinístico")


# ------------------------------------------------------- F16: patch entregue, bloqueado

class F16IsInstalled(unittest.TestCase):
    """F16 — a correcção está no leitor, não só num ficheiro de patch.

    O defeito: `bp_validate` aceitava `decision_ref` OU `concretizes_decision`, e
    `bp_read` só procurava a primeira. Um blueprint que escrevesse a segunda perdia a
    ligação à decisão na projecção do runtime, e foi assim que a revisão do caso real
    leu `current.decision_ref: ""` sobre um ficheiro que dizia `concretizes_decision:
    D-002`. Uma passagem anterior não pôde alterar o leitor e entregou a correcção como
    patch; este teste existe para que «entregue» e «instalado» não se confundam outra
    vez."""

    PATCH = ROOT / "docs" / "runtime-hardening" / "patches" / "f16-decision-ref-alias.patch"

    def setUp(self):
        self.D = runpy.run_path(str(ROOT / "library" / "kernel" / "tools" / "dashboard.py"))

    def test_the_reader_normalises_the_alias(self):
        bp = self.D["bp_read"](ENG / "_blueprint" / "ux-blueprint_v01.yaml")
        self.assertEqual(bp["decision_ref"], "D-002")
        self.assertEqual(bp["decision_id"], "D-002")

    def test_the_runtime_projection_recovers_the_link(self):
        """O sintoma exacto que a revisão do caso real registou."""
        blocks = self.D["classify_decisions"](
            (ENG / "decisions.md").read_text(encoding="utf-8"))
        rows = self.D["parse_su"](
            (ENG / "shared-understanding.md").read_text(encoding="utf-8"))[1]
        state = self.D["blueprint_state"](ENG, blocks, rows, "pp")
        self.assertEqual(state["current"]["decision_ref"], "D-002")

    def test_a_file_with_neither_key_gets_no_invented_id(self):
        """Normalizar não é inventar: sem chave nenhuma, o id é vazio."""
        self.assertEqual(self.D["bp_decision_id"]("version: v01\ndraft: false\n"), "")

    def test_the_patch_file_is_kept_as_the_record_of_the_change(self):
        self.assertTrue(self.PATCH.is_file())
        body = self.PATCH.read_text(encoding="utf-8")
        self.assertIn("concretizes_decision", body)
        self.assertIn("decision_id", body)


if __name__ == "__main__":
    unittest.main(verbosity=2)
