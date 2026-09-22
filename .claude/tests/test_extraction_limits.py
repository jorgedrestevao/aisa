# -*- coding: utf-8 -*-
"""E05 — limites de extracção (P8).

Caso: «Usar fonte com conteúdo não suportado/material».
Esperado: «Limitação/Unknown explícitos; não inventa VBA/regra/dados».

A fonte é construída aqui, com o conteúdo que o motor NÃO consegue ler e que é material
para o cálculo: macros (`vbaProject.bin`), funções de add-in (`_xll.`), Power Query e um
livro externo. O que se afirma é o contrário do habitual — não que o motor leia tudo, mas
que declare com precisão o que não leu, e não preencha o buraco.

O piloto real de pricing tem exactamente esta forma (VBA + 176 chamadas `_xll.Storm`), pelo
que a última classe corre contra o ficheiro real quando ele está presente."""
import json
import os
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
XLSX_PY = ROOT / "library" / "kernel" / "tools" / "xlsx_extract.py"

try:
    import openpyxl  # noqa: F401
    HAVE_OPENPYXL = True
except ImportError:
    HAVE_OPENPYXL = False


def livro_com_conteudo_nao_suportado(destino: Path) -> Path:
    """Um .xlsm com macros, add-in, Power Query e livro externo — tudo material.

    `PRECO` depende de uma função de add-in, logo o seu valor não é calculável a partir do
    ficheiro. É esse o ponto: o motor tem de dizer que não sabe, não arranjar um número.
    """
    from openpyxl import Workbook

    wb = Workbook()
    ws = wb.active
    ws.title = "Motor"
    ws["A1"] = "produto"
    ws["B1"] = "cotacao"
    ws["C1"] = "margem"
    ws["D1"] = "preco"
    ws["A2"] = "VLSFO"
    # a cotação vem de fora do livro: o motor não a pode calcular
    ws["B2"] = "=_xll.Storm.Quote(\"PLATTS\",\"VLSFO\")"
    ws["C2"] = 12.5
    # uma fórmula perfeitamente legível, para provar que o resto continua a ser lido
    ws["D2"] = "=B2+C2"
    ws["A3"] = "MGO"
    ws["B3"] = "=_xll.Storm.Quote(\"PLATTS\",\"MGO\")"
    ws["C3"] = 9.0
    ws["D3"] = "=B3+C3"
    # a regra de arredondamento vive numa macro; aqui só se vê a chamada
    ws["E1"] = "arredondado"
    ws["E2"] = "=ROUND(D2,2)"

    xlsx = destino / "motor.xlsx"
    wb.save(xlsx)

    xlsm = destino / "motor.xlsm"
    with zipfile.ZipFile(xlsx) as origem, zipfile.ZipFile(xlsm, "w", zipfile.ZIP_DEFLATED) as saida:
        for item in origem.infolist():
            saida.writestr(item, origem.read(item.filename))
        # macros: presentes no pacote, ilegíveis pelo motor
        saida.writestr("xl/vbaProject.bin", b"\x00CMG_FAKE_VBA_BINARY\x00")
        # Power Query: o DataMashup é detectado pelos primeiros bytes
        saida.writestr("customXml/itemProps3.xml",
                       b'<?xml version="1.0"?><ds:datastoreItem xmlns:ds="x">DataMashup AAAA</ds:datastoreItem>')
        # livro externo: o precedente vive noutro ficheiro
        saida.writestr("xl/externalLinks/_rels/externalLink1.xml.rels",
                       b'<?xml version="1.0"?><Relationships><Relationship Id="rId1" '
                       b'Target="file:///C:/Temp/CEntriC-Runtime.xlsx"/></Relationships>')
    xlsx.unlink()
    return xlsm


def extrai(fonte: Path, calc_chain=False) -> dict:
    """L1 em processo real. Com `calc_chain`, a segunda passagem escreve a cadeia ao lado."""
    saida = fonte.with_suffix(".extraction.json")
    p = subprocess.run([sys.executable, str(XLSX_PY), str(fonte), str(saida), "--force"],
                       capture_output=True, text=True)
    if not saida.exists():
        raise AssertionError("extracção não produziu artefacto: rc={} {}".format(
            p.returncode, p.stderr[-800:]))
    if calc_chain:
        cadeia = fonte.with_suffix(".calc-chain.json")
        c = subprocess.run([sys.executable, str(XLSX_PY), "--calc-chain",
                            str(fonte), str(saida), str(cadeia)],
                           capture_output=True, text=True)
        if not cadeia.exists():
            raise AssertionError("calc-chain não produzida: rc={} {}".format(
                c.returncode, c.stderr[-800:]))
    return json.loads(saida.read_text(encoding="utf-8"))


@unittest.skipUnless(HAVE_OPENPYXL, "openpyxl not installed")
class E05a_ALimitacaoEDeclarada(unittest.TestCase):
    """Cada mecanismo não suportado presente é declarado, com onde está."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="e05-"))
        cls.doc = extrai(livro_com_conteudo_nao_suportado(cls.tmp))
        cls.cb = cls.doc.get("capability_boundary") or {}

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_the_boundary_block_exists_at_all(self):
        self.assertTrue(self.cb, "sem bloco de fronteira, a limitação não está declarada")

    def test_macros_are_declared_present_and_not_decompiled(self):
        vba = self.cb["vba"]
        self.assertTrue(vba["present"])
        self.assertEqual(vba["locator"], "xl/vbaProject.bin", "diz onde está")
        self.assertIn("not decompiled", vba["detail"], "e diz que não as leu")

    def test_the_addin_call_is_declared_with_its_signature(self):
        add = self.cb["addin_functions"]
        self.assertTrue(add["present"])
        self.assertIn("_xll.Storm", add["detail"])
        self.assertIn("×2", add["detail"], "conta as chamadas que viu, não estima")

    def test_power_query_and_the_external_workbook_are_declared(self):
        self.assertTrue(self.cb["power_query"]["present"])
        ext = self.cb["external_links"]
        self.assertTrue(ext["present"])
        self.assertIn("CEntriC-Runtime.xlsx", ext["detail"], "nomeia o livro que falta")

    def test_a_limitation_is_not_a_failure(self):
        self.assertEqual(self.doc["status"], "ok",
                         "conteúdo não suportado não invalida a extracção do que é legível")


@unittest.skipUnless(HAVE_OPENPYXL, "openpyxl not installed")
class E05b_NaoInventa(unittest.TestCase):
    """O que não se lê não aparece lido. É esta classe que E05 existe para provar."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="e05-inv-"))
        cls.doc = extrai(livro_com_conteudo_nao_suportado(cls.tmp))
        cls.cb = cls.doc.get("capability_boundary") or {}
        cls.bruto = json.dumps(cls.doc, ensure_ascii=False)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_no_vba_module_name_is_invented(self):
        modulos = (self.doc.get("workbook") or {}).get("flags", {}).get("vba_modules", [])
        self.assertEqual(modulos, [],
                         "o .bin não foi descompilado: nenhum nome de módulo pode existir")

    def test_the_fake_binary_content_is_never_echoed_as_logic(self):
        self.assertNotIn("CMG_FAKE_VBA_BINARY", self.bruto,
                         "o conteúdo do binário não entra no artefacto como se fosse regra")

    def test_the_addin_value_is_not_fabricated(self):
        """`_xll.Storm.Quote` não é calculável aqui. Nenhum número pode aparecer no seu lugar."""
        motor = next(s for s in self.doc["sheets"] if s["name"] == "Motor")
        coluna_b = next((c for c in motor["columns"] if c["column"] == "B"), None)
        self.assertIsNotNone(coluna_b, "a coluna da cotação tem de existir no perfil")
        bruto_b = json.dumps(coluna_b, ensure_ascii=False)
        self.assertNotIn("Platts", bruto_b, "não se inventa a origem do valor")
        for inventado in ("450", "620", "0.9"):
            self.assertNotIn(inventado, bruto_b,
                             "nenhuma cotação plausível pode ser escrita onde não há valor")

    def test_absent_mechanisms_stay_absent(self):
        """Este livro não tem modelo de dados nem RTD. Declarar presença seria inferir."""
        for mecanismo in ("data_model", "rtd", "iterative", "pivot_caches"):
            self.assertFalse(self.cb[mecanismo]["present"],
                             "{} não está no pacote: `present` tem de ser falso".format(mecanismo))
            self.assertEqual(self.cb[mecanismo]["detail"], "",
                             "mecanismo ausente não ganha detalhe")

    def test_what_is_readable_is_still_read(self):
        """A limitação não é desculpa para não extrair o resto."""
        motor = next(s for s in self.doc["sheets"] if s["name"] == "Motor")
        colunas = {c["column"] for c in motor["columns"]}
        self.assertIn("D", colunas, "a fórmula legível `=B2+C2` continua a ser extraída")


@unittest.skipUnless(HAVE_OPENPYXL, "openpyxl not installed")
class E05c_AFronteiraChegaAQuemLe(unittest.TestCase):
    """Declarar no JSON não chega: a consequência tem de aparecer onde o humano lê (§4bis)."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="e05-chain-"))
        fonte = livro_com_conteudo_nao_suportado(cls.tmp)
        cls.doc = extrai(fonte, calc_chain=True)
        cadeia = fonte.with_suffix(".calc-chain.json")
        cls.chain = json.loads(cadeia.read_text(encoding="utf-8")) if cadeia.exists() else None

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_the_calc_chain_carries_the_same_boundary(self):
        if self.chain is None:
            self.skipTest("calc-chain não produzida neste ambiente")
        cb = self.chain.get("capability_boundary") or {}
        self.assertTrue(cb.get("vba", {}).get("present"),
                        "a cadeia de cálculo não pode perder a fronteira pelo caminho")

    def test_the_rendered_section_declares_the_boundary_before_the_chain(self):
        if self.chain is None:
            self.skipTest("calc-chain não produzida neste ambiente")
        X = runpy.run_path(str(XLSX_PY))
        md = X["render_calc_chain_md"](self.chain)
        pos_fronteira = md.find("Fronteira de capacidade")
        self.assertGreater(pos_fronteira, -1, "a secção declara a fronteira")
        self.assertIn("TO-READ manual", md, "a macro fica como leitura manual explícita")
        self.assertIn("feed externo", md, "a chamada de add-in fica como terminal declarado")


class E05d_OFicheiroRealDoPiloto(unittest.TestCase):
    """O piloto de pricing É uma fonte com conteúdo não suportado material."""

    FONTE = ROOT / "projects" / "pricing-bunkers-pilot-4" / "inputs"

    def livro(self):
        if not self.FONTE.is_dir():
            return None
        livros = sorted(self.FONTE.glob("*.xls[mx]"))
        return livros[0] if livros else None

    @unittest.skipUnless(HAVE_OPENPYXL, "openpyxl not installed")
    def test_the_real_workbook_declares_macros_and_an_addin(self):
        livro = self.livro()
        if livro is None:
            self.skipTest("input do piloto ausente neste ambiente (dados de cliente)")
        tmp = Path(tempfile.mkdtemp(prefix="e05-real-"))
        try:
            copia = tmp / livro.name
            shutil.copy2(livro, copia)
            doc = extrai(copia)
            cb = doc.get("capability_boundary") or {}
            self.assertTrue(cb.get("vba", {}).get("present"),
                            "o livro real tem macros e tem de o dizer")
            self.assertTrue(cb.get("addin_functions", {}).get("present"),
                            "o motor de preço chama uma função de add-in: é fronteira, não omissão")
            self.assertEqual((doc.get("workbook") or {}).get("flags", {}).get("vba_modules"), [],
                             "nem no ficheiro real se inventa o conteúdo das macros")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_the_stored_capture_is_compared_not_trusted(self):
        """A extracção guardada do piloto é anterior ao bloco de fronteira.

        Não se corrige aqui — corrige-se recapturando. O teste existe para que a lacuna
        seja visível em vez de passar por cobertura."""
        cap = (ROOT / "projects" / "pricing-bunkers-pilot-4" / "_capture")
        if not cap.is_dir():
            self.skipTest("captura do piloto ausente neste ambiente")
        artefactos = sorted(cap.glob("*.xls[mx].extraction.json"))
        if not artefactos:
            self.skipTest("sem artefacto de extracção guardado")
        doc = json.loads(artefactos[0].read_text(encoding="utf-8"))
        tem_fronteira = "capability_boundary" in doc
        tem_vba = (doc.get("workbook") or {}).get("flags", {}).get("vba_present")
        self.assertTrue(
            tem_fronteira or tem_vba,
            "a captura guardada não declara macros de forma nenhuma — recapturar antes de E02")


if __name__ == "__main__":
    unittest.main(verbosity=1)
