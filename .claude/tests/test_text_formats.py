# -*- coding: utf-8 -*-
"""Os quatro formatos que a captura-lite nao sabia ler: `.srt`, `.txt`, `.md`, `.csv`.

Medido antes de existirem: `projects/kam-onboarding-pilot-4/inputs/` carrega um
`Requisitos_Onboarding_KAM_v1.txt` que o extractor recusava com exit 2 — um input real de
um piloto real, por ler.

A regra que estes casos existem para impor e **nao amostrar**. Um extractor que le 500
linhas e guarda 20 conta o ficheiro em vez de o preservar: as contagens ficam certas e o
conteudo de negocio desaparece. O contrato desta camada e perda minima com proveniencia
(`library/kernel/orchestration.md` -> Evidence contract), por isso cada caso de volume
verifica a PRIMEIRA e a ULTIMA unidade, nao so o total."""
import csv
import json
import os
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "library" / "kernel" / "tools"
T = runpy.run_path(str(TOOLS / "text_extract.py"))

SRT = (
    "1\n"
    "00:00:01,000 --> 00:00:04,000\n"
    "Bom dia a todos.\n"
    "\n"
    "2\n"
    "00:00:04,500 --> 00:00:09,200\n"
    "O processo de pricing corre em tres passos.\n"
    "\n"
    "3\n"
    "00:01:10,000 --> 00:01:14,000\n"
    "<i>A margem</i> e revista todas as semanas.\n"
)


def escreve(tmp, nome, texto, encoding="utf-8"):
    p = os.path.join(tmp, nome)
    with open(p, "w", encoding=encoding, newline="") as fh:
        fh.write(texto)
    return p


def corre(tmp, caminho):
    md = os.path.join(tmp, "out.text.md")
    js = os.path.join(tmp, "out.extraction.json")
    p = subprocess.run([sys.executable, str(TOOLS / "text_extract.py"), caminho, md, js,
                        "--force"], capture_output=True, text=True, timeout=180)
    corpo = Path(md).read_text(encoding="utf-8") if os.path.exists(md) else ""
    doc = json.loads(Path(js).read_text(encoding="utf-8")) if os.path.exists(js) else {}
    return p, corpo, doc


class T0_ORegisto(unittest.TestCase):
    """Um formato so esta suportado quando as QUATRO tabelas o conhecem."""

    NOVOS = (".srt", ".txt", ".md", ".csv")

    def test_the_four_formats_are_declared(self):
        for ext in self.NOVOS:
            self.assertIn(ext, T["TEXT_FORMATS"], "formato nao declarado: " + ext)

    def test_each_format_has_an_extractor(self):
        for ext in self.NOVOS:
            self.assertIn(ext, T["EXTRACTORS"], "sem extractor: " + ext)

    def test_each_format_says_how_to_cite_it(self):
        """Sem entrada em CITE o driver rebenta com KeyError ao montar o cabecalho."""
        for ext in self.NOVOS:
            self.assertIn(ext, T["CITE"], "sem locator declarado: " + ext)
            self.assertTrue(T["CITE"][ext].strip())

    def test_each_format_names_the_library_it_used(self):
        for ext in self.NOVOS:
            self.assertIn(ext, T["LIBRARIES"], "sem biblioteca declarada: " + ext)


class T1_Legendas(unittest.TestCase):

    def test_an_srt_is_extracted(self):
        with tempfile.TemporaryDirectory() as tmp:
            p, corpo, doc = corre(tmp, escreve(tmp, "reuniao.srt", SRT))
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(doc.get("status"), "ok", doc.get("reason"))
        self.assertIn("Bom dia a todos", corpo)
        self.assertIn("A margem", corpo, "o texto dentro de tags desapareceu")

    def test_the_timestamps_survive_as_locators(self):
        """O locator de uma legenda e a hora — sem ela nao ha como citar."""
        with tempfile.TemporaryDirectory() as tmp:
            _p, corpo, _d = corre(tmp, escreve(tmp, "reuniao.srt", SRT))
        self.assertIn("00:00:01", corpo)
        self.assertIn("00:01:10", corpo, "a ultima legenda perdeu a hora")

    def test_the_order_is_the_source_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            _p, corpo, _d = corre(tmp, escreve(tmp, "reuniao.srt", SRT))
        self.assertLess(corpo.index("Bom dia"), corpo.index("tres passos"))
        self.assertLess(corpo.index("tres passos"), corpo.index("A margem"))

    def test_every_cue_is_counted(self):
        with tempfile.TemporaryDirectory() as tmp:
            _p, _c, doc = corre(tmp, escreve(tmp, "reuniao.srt", SRT))
        self.assertEqual(doc["units"]["cues"], 3)

    def test_a_webvtt_signature_is_not_required_of_an_srt(self):
        """O .vtt exige a assinatura WEBVTT; um .srt nao a tem e nao e por isso invalido."""
        with tempfile.TemporaryDirectory() as tmp:
            _p, _c, doc = corre(tmp, escreve(tmp, "reuniao.srt", SRT))
        self.assertNotEqual(doc.get("status"), "failed", doc.get("reason"))

    def test_an_srt_with_no_cues_is_empty_not_failed(self):
        """Ausencia e evidencia: o ficheiro leu-se e nao tinha nada."""
        with tempfile.TemporaryDirectory() as tmp:
            _p, _c, doc = corre(tmp, escreve(tmp, "vazio.srt", "\n\n"))
        self.assertEqual(doc.get("status"), "empty")


class T2_TextoSimples(unittest.TestCase):

    def test_a_txt_is_extracted_with_numbered_paragraphs(self):
        conteudo = "Primeiro paragrafo.\n\nSegundo paragrafo.\n\nTerceiro paragrafo.\n"
        with tempfile.TemporaryDirectory() as tmp:
            p, corpo, doc = corre(tmp, escreve(tmp, "requisitos.txt", conteudo))
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(doc.get("status"), "ok")
        for n, texto in ((1, "Primeiro"), (2, "Segundo"), (3, "Terceiro")):
            self.assertIn("[¶{}]".format(n), corpo, "falta o paragrafo {}".format(n))
            self.assertIn(texto, corpo)

    def test_a_txt_keeps_every_paragraph_not_a_sample(self):
        """A armadilha: contar em vez de preservar. Primeiro e ULTIMO, nao so o total."""
        conteudo = "\n\n".join("Paragrafo numero {}.".format(i) for i in range(1, 201))
        with tempfile.TemporaryDirectory() as tmp:
            _p, corpo, doc = corre(tmp, escreve(tmp, "longo.txt", conteudo))
        self.assertEqual(doc["units"]["paragraphs"], 200)
        self.assertIn("Paragrafo numero 1.", corpo)
        self.assertIn("Paragrafo numero 200.", corpo, "o fim do ficheiro foi amostrado fora")

    def test_consecutive_lines_are_separate_paragraphs(self):
        """A regra, fixada: linha nao vazia = paragrafo. Agrupar por linha em branco
        juntava celulas de tabela numa frase que ninguem escreveu — medido no despejo de
        PDF do piloto de onboarding."""
        conteudo = "Campo Detalhe\nProjeto Onboarding\nSetor Comercial\n"
        with tempfile.TemporaryDirectory() as tmp:
            _p, corpo, doc = corre(tmp, escreve(tmp, "tabela.txt", conteudo))
        self.assertEqual(doc["units"]["paragraphs"], 3,
                         "linhas seguidas foram coladas num paragrafo so")
        self.assertIn("[\u00b62] Projeto Onboarding", corpo)

    def test_an_empty_txt_is_empty_not_failed(self):
        with tempfile.TemporaryDirectory() as tmp:
            _p, _c, doc = corre(tmp, escreve(tmp, "nada.txt", "   \n\n  \n"))
        self.assertEqual(doc.get("status"), "empty")

    def test_a_txt_that_is_not_utf8_still_reads(self):
        """Um ficheiro real vem como vier; recusa-lo e perder a fonte inteira."""
        with tempfile.TemporaryDirectory() as tmp:
            caminho = os.path.join(tmp, "latin.txt")
            with open(caminho, "wb") as fh:
                fh.write("Reunião de preços.".encode("latin-1"))
            _p, corpo, doc = corre(tmp, caminho)
        self.assertEqual(doc.get("status"), "ok", doc.get("reason"))
        self.assertIn("Reuni", corpo)


class T3_Markdown(unittest.TestCase):

    MD = ("# Requisitos\n\nO processo comeca no pedido.\n\n"
          "## Aprovacao\n\nO gestor aprova ate 10k.\n\n"
          "| campo | tipo |\n|---|---|\n| valor | numero |\n")

    def test_a_md_is_extracted(self):
        with tempfile.TemporaryDirectory() as tmp:
            p, corpo, doc = corre(tmp, escreve(tmp, "notas.md", self.MD))
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(doc.get("status"), "ok")
        self.assertIn("O processo comeca no pedido", corpo)
        self.assertIn("O gestor aprova ate 10k", corpo)

    def test_the_headings_survive_as_structure(self):
        """O locator de um `.md` e a seccao; sem cabecalhos nao ha como citar."""
        with tempfile.TemporaryDirectory() as tmp:
            _p, corpo, doc = corre(tmp, escreve(tmp, "notas.md", self.MD))
        self.assertIn("Requisitos", corpo)
        self.assertIn("Aprovacao", corpo)
        self.assertGreaterEqual(doc["units"].get("headings", 0), 2)

    def test_the_table_rows_are_kept(self):
        with tempfile.TemporaryDirectory() as tmp:
            _p, corpo, _d = corre(tmp, escreve(tmp, "notas.md", self.MD))
        self.assertIn("valor", corpo, "a tabela do markdown desapareceu")

    def test_the_order_is_the_source_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            _p, corpo, _d = corre(tmp, escreve(tmp, "notas.md", self.MD))
        self.assertLess(corpo.index("comeca no pedido"), corpo.index("aprova ate 10k"))


class T4_Csv(unittest.TestCase):

    def test_a_csv_is_extracted_as_a_table(self):
        linhas = "id,cliente,valor\n1,ACME,100\n2,Beta,250\n"
        with tempfile.TemporaryDirectory() as tmp:
            p, corpo, doc = corre(tmp, escreve(tmp, "registo.csv", linhas))
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(doc.get("status"), "ok")
        for valor in ("cliente", "ACME", "Beta", "250"):
            self.assertIn(valor, corpo, "perdeu-se: " + valor)

    def test_every_row_is_kept_never_sampled(self):
        """500 linhas entram, 500 saem. Este e o caso que separa preservar de contar."""
        linhas = ["id,texto"] + ["{},linha numero {}".format(i, i) for i in range(1, 501)]
        with tempfile.TemporaryDirectory() as tmp:
            _p, corpo, doc = corre(tmp, escreve(tmp, "grande.csv", "\n".join(linhas) + "\n"))
        self.assertEqual(doc["units"]["rows"], 500)
        self.assertIn("linha numero 1,", corpo.replace("| ", "").replace(" |", ","))
        self.assertIn("linha numero 500", corpo, "as ultimas linhas foram amostradas fora")

    def test_a_semicolon_delimiter_is_read_as_columns(self):
        """Excel em pt-PT escreve `;`. Ler isso como uma coluna so perde a tabela toda."""
        linhas = "id;cliente;valor\n1;ACME;100\n2;Beta;250\n"
        with tempfile.TemporaryDirectory() as tmp:
            _p, _c, doc = corre(tmp, escreve(tmp, "ponto.csv", linhas))
        self.assertEqual(doc["units"]["columns"], 3,
                         "o delimitador `;` nao foi reconhecido")

    def test_a_cell_with_a_pipe_does_not_break_the_table(self):
        linhas = "id,nota\n1,a|b\n"
        with tempfile.TemporaryDirectory() as tmp:
            _p, corpo, doc = corre(tmp, escreve(tmp, "pipe.csv", linhas))
        self.assertEqual(doc.get("status"), "ok")
        self.assertIn("a\\|b", corpo, "o `|` da celula partiu a tabela markdown")

    def test_an_empty_csv_is_empty_not_failed(self):
        with tempfile.TemporaryDirectory() as tmp:
            _p, _c, doc = corre(tmp, escreve(tmp, "vazio.csv", ""))
        self.assertEqual(doc.get("status"), "empty")


class T5_OQueNaoMuda(unittest.TestCase):

    def test_an_unsupported_format_is_still_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            p, _c, _d = corre(tmp, escreve(tmp, "coisa.xyz", "nada"))
        self.assertEqual(p.returncode, 2, "passou a aceitar um formato que nao sabe ler")

    def test_the_vtt_path_is_untouched(self):
        vtt = ("WEBVTT\n\n00:00:01.000 --> 00:00:03.000\n"
               "<v Ana>Comecamos pela margem.</v>\n")
        with tempfile.TemporaryDirectory() as tmp:
            _p, corpo, doc = corre(tmp, escreve(tmp, "r.vtt", vtt))
        self.assertEqual(doc.get("status"), "ok")
        self.assertIn("Ana", corpo)

    def test_a_file_without_the_webvtt_signature_is_still_refused_as_vtt(self):
        """Relaxar a assinatura para o `.srt` nao pode relaxa-la para o `.vtt`."""
        with tempfile.TemporaryDirectory() as tmp:
            _p, _c, doc = corre(tmp, escreve(tmp, "falso.vtt",
                                             "1\n00:00:01,000 --> 00:00:02,000\nOla\n"))
        self.assertEqual(doc.get("status"), "failed")


class T6_OInputRealQueEstavaPorLer(unittest.TestCase):

    def test_the_kam_pilot_txt_now_reads(self):
        alvo = ROOT / "projects" / "kam-onboarding-pilot-4" / "inputs" / \
            "Requisitos_Onboarding_KAM_v1.txt"
        if not alvo.exists():
            self.skipTest("piloto ausente neste ambiente")
        with tempfile.TemporaryDirectory() as tmp:
            p, corpo, doc = corre(tmp, str(alvo))
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(doc.get("status"), "ok", doc.get("reason"))
        self.assertGreater(doc["units"]["paragraphs"], 0)
        self.assertGreater(len(corpo), 500)


if __name__ == "__main__":
    unittest.main(verbosity=1)


class T7_OsLocatorsDosFormatosNovos(unittest.TestCase):
    """Acrescentar o extractor e nao acrescentar a classe de locator e meio trabalho.

    O guarda de locators (`audit_confirmed_locators`) le uma linha Confirmed e pergunta
    de que classe e a prova. Um `.csv` extraido cujo `linha 42` nao bate em classe
    nenhuma faz o guarda dizer «sem locator» sobre evidencia que o proprio motor
    produziu — o mesmo defeito que a classe 6 deste ficheiro ja teve de corrigir para o
    `enquadramento.md`."""

    D = runpy.run_path(str(TOOLS / "dashboard.py"))

    def classes(self, texto):
        return self.D["locator_classes"](texto)

    def test_an_srt_timestamp_is_a_transcript_locator(self):
        self.assertIn("transcricao", self.classes("reuniao.srt#[00:01:10]"))

    def test_a_txt_paragraph_is_a_document_locator(self):
        self.assertIn("documento", self.classes("Requisitos_v1.txt#¶12"))

    def test_a_md_paragraph_is_a_document_locator(self):
        self.assertIn("documento", self.classes("notas.md#¶5"))

    def test_a_csv_line_is_a_locator(self):
        self.assertTrue(self.classes("registo.csv#linha 42"),
                        "uma linha de `.csv` citada nao bate em classe nenhuma")

    def test_the_lite_forms_are_recognised_too(self):
        """A forma que o artefacto ensina a citar: `<file> · ¶NN` e `<file> · linha N`."""
        self.assertIn("documento", self.classes("`Requisitos_v1.txt` · ¶12"))
        self.assertTrue(self.classes("`registo.csv` · linha 42"))

    def test_the_old_classes_still_hold(self):
        self.assertIn("transcricao", self.classes("reuniao.vtt#[00:01:10]"))
        self.assertIn("documento", self.classes("doc.docx#¶3"))
        self.assertIn("xlsx-celula", self.classes("livro.xlsx#Folha1!B4"))
        self.assertIn("answers", self.classes("answers.md#U-012"))

    def test_an_engagement_with_these_sources_resolves_them(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = Path(tmp) / "eng"
            (eng / "inputs").mkdir(parents=True)
            (eng / "inputs" / "reuniao.srt").write_text(SRT, encoding="utf-8")
            (eng / "inputs" / "registo.csv").write_text("id,v\n1,2\n", encoding="utf-8")
            (eng / "inputs" / "reqs.txt").write_text("linha\n", encoding="utf-8")
            alvo = self.D["evidence_targets"](eng)
            for texto in ("`reuniao.srt` · [00:00:01]",
                          "`reqs.txt` · ¶1",
                          "`registo.csv` · linha 2"):
                gaps = self.D["locator_target_gaps"](texto, self.classes(texto), alvo)
                self.assertEqual(gaps, [], "{} -> {}".format(texto, gaps))
