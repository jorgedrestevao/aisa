"""R5 / DEF-P1-01 — os localizadores que o próprio framework escreve resolvem-se.

`docs/PILOT_RUNTIME_CORRECTION_PLAN.md` → R5. Uma linha `Confirmed` assente numa
declaração do dono recolhida no enquadramento cita as âncoras de tema `T1..T7` que o
próprio `aisa-start` escreve — e essas âncoras não correspondiam a classe nenhuma, pelo
que o guarda reportava «evidência sem locator das cinco classes» sobre evidência que o
framework tinha produzido. O mesmo para os factos de arranque que só vivem em
`context.json` (`funding_gate`, `requester.authority`): a única excepção prevista era
`literal_request`.

Duas metades, e as duas contam:

* **forma** — o localizador é reconhecido.
* **resolução** — e é verificado: a secção tem de estar no ficheiro, a chave tem de
  estar no JSON. Nem todo o caminho `context.json` passa a excepção sem validação.

Um localizador inexistente continua a avisar; o contrato do hook não muda (avisa, não
bloqueia).

Fixtures sintéticas em tempdir — nenhum engagement real é lido ou escrito.

    python .claude/tests/test_locator_resolution.py
"""

import importlib.util
import io
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_dashboard():
    path = os.path.join(ROOT, "library", "kernel", "tools", "dashboard.py")
    spec = importlib.util.spec_from_file_location("aisa_dashboard_locator", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


D = load_dashboard()

ENQ = """# Enquadramento — fx

## T1 · actors
Quem faz.

## T2 · trigger
O que começa.

## T3 · activities
Os passos.

## T7 · change_requested
O que se pede.

## Invariantes declaradas

| id | invariante | orienta | fonte |
|----|-----------|---------|-------|
| M-1 | Quem faz o preço não valida a venda. | governance | dono |
"""

CTX = {
    "engagement": "fx",
    "literal_request": "quero automatizar isto",
    "funding_gate": False,
    "requester": {"name": "dono", "role": "dono do processo", "authority": "decide"},
}


def write(path, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    with io.open(path, "w", encoding="utf-8") as fh:
        fh.write(body)


class Base(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="aisa-r5-")
        self.eng = Path(self.tmp) / "fx"
        write(self.eng / "enquadramento.md", ENQ)
        write(self.eng / "context.json", json.dumps(CTX, ensure_ascii=False))
        write(self.eng / "answers.md", "# Prazos por classe — R-01\n\nresposta.\n")
        write(self.eng / "inputs" / "Requisitos.pdf", "%PDF fake")
        write(self.eng / "inputs" / "reuniao.vtt", "WEBVTT")
        write(self.eng / "inputs" / "mapa.xlsx", "fake")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def verd(self, txt, eng=None):
        """-> (forma, resolve, gaps)"""
        tgt = D.evidence_targets(eng or self.eng)
        classes = D.locator_classes(txt)
        forma = bool(classes) or bool(D.LOCATOR_EXCEPTION.search(txt))
        gaps = D.locator_target_gaps(txt, classes, tgt) if classes else []
        return forma, forma and not gaps, gaps


# ------------------------------------------------------- temas do enquadramento

class TemasDoEnquadramento(Base):

    def test_temas_existentes_resolvem(self):
        for t in ("T1", "T2", "T3", "T7"):
            with self.subTest(tema=t):
                forma, resolve, gaps = self.verd(
                    "declaração do dono, 2026-09-11 · enquadramento.md#" + t)
                self.assertTrue(forma)
                self.assertTrue(resolve, gaps)

    def test_tema_ausente_do_ficheiro_avisa(self):
        forma, resolve, gaps = self.verd("declaração do dono · enquadramento.md#T4")
        self.assertTrue(forma, "a forma é de localizador")
        self.assertFalse(resolve)
        self.assertIn("sem a seccao #T4", "; ".join(gaps))

    def test_t0_e_t8_estao_fora_dos_sete_temas(self):
        for t in ("T0", "T8", "T99"):
            with self.subTest(tema=t):
                forma, resolve, gaps = self.verd("dono · enquadramento.md#" + t)
                self.assertTrue(forma)
                self.assertFalse(resolve)
                self.assertIn("fora dos sete temas", "; ".join(gaps))

    def test_o_intervalo_dos_temas_vale_mesmo_com_o_cabecalho_no_ficheiro(self):
        """Reproduzido em revisão: escrever `## T8 · extra` no enquadramento não cria
        um tema novo. O contrato tem sete, e o intervalo é verificado antes de se ir
        ver o ficheiro."""
        write(self.eng / "enquadramento.md",
              ENQ + "\\n## T8 \u00b7 extra\\nInventado.\\n")
        forma, resolve, gaps = self.verd("dono · enquadramento.md#T8")
        self.assertTrue(forma)
        self.assertFalse(resolve)
        self.assertIn("fora dos sete temas", "; ".join(gaps))
        # e um tema do contrato continua a resolver no mesmo ficheiro
        _f, resolve3, _g = self.verd("dono · enquadramento.md#T3")
        self.assertTrue(resolve3)

    def test_sem_enquadramento_no_engagement(self):
        eng2 = Path(self.tmp) / "sem-enq"
        write(eng2 / "context.json", json.dumps(CTX))
        forma, resolve, gaps = self.verd("dono · enquadramento.md#T1", eng2)
        self.assertTrue(forma)
        self.assertFalse(resolve)
        self.assertIn("enquadramento.md nao existe", "; ".join(gaps))

    def test_o_invariante_m_n_continua_a_valer(self):
        forma, resolve, _g = self.verd("dono · enquadramento.md#M-1")
        self.assertTrue(forma)
        self.assertTrue(resolve)
        _f, resolve9, gaps9 = self.verd("dono · enquadramento.md#M-9")
        self.assertFalse(resolve9)
        self.assertIn("sem M-9", "; ".join(gaps9))


# ------------------------------------------------------- campos de context.json

class CamposDeArranque(Base):

    def test_funding_gate_false_e_um_valor_presente(self):
        forma, resolve, gaps = self.verd("dono · context.json#funding_gate")
        self.assertTrue(forma)
        self.assertTrue(resolve, gaps)

    def test_funding_gate_true_tambem(self):
        write(self.eng / "context.json", json.dumps(dict(CTX, funding_gate=True)))
        _f, resolve, gaps = self.verd("dono · context.json#funding_gate")
        self.assertTrue(resolve, gaps)

    def test_funding_gate_ausente_do_ficheiro(self):
        ctx = dict(CTX)
        ctx.pop("funding_gate")
        write(self.eng / "context.json", json.dumps(ctx))
        _f, resolve, gaps = self.verd("dono · context.json#funding_gate")
        self.assertFalse(resolve)
        self.assertIn("sem a chave funding_gate", "; ".join(gaps))

    def test_chave_aninhada_existente(self):
        _f, resolve, gaps = self.verd("dono · context.json#requester.authority")
        self.assertTrue(resolve, gaps)

    def test_chave_aninhada_ausente(self):
        _f, resolve, gaps = self.verd("dono · context.json#requester.telefone")
        self.assertFalse(resolve)
        self.assertIn("sem a chave requester.telefone", "; ".join(gaps))

    def test_autoridade_vazia_tem_tratamento_explicito(self):
        """A chave existe e não diz nada: o localizador aponta para o vazio, e isso
        é dito — não é o mesmo que a chave faltar, nem passa por evidência."""
        ctx = json.loads(json.dumps(CTX))
        ctx["requester"]["authority"] = ""
        write(self.eng / "context.json", json.dumps(ctx))
        _f, resolve, gaps = self.verd("dono · context.json#requester.authority")
        self.assertFalse(resolve)
        self.assertIn("esta vazio", "; ".join(gaps))

    def test_autoridade_so_com_espacos_e_vazia(self):
        """Reproduzido em revisão: `" "` não é uma autoridade declarada."""
        for valor in (" ", "   ", "\t", "\n "):
            with self.subTest(valor=repr(valor)):
                ctx = json.loads(json.dumps(CTX))
                ctx["requester"]["authority"] = valor
                write(self.eng / "context.json", json.dumps(ctx))
                _f, resolve, gaps = self.verd("dono · context.json#requester.authority")
                self.assertFalse(resolve)
                self.assertIn("esta vazio", "; ".join(gaps))

    def test_um_valor_com_espacos_a_volta_continua_a_ser_um_valor(self):
        ctx = json.loads(json.dumps(CTX))
        ctx["requester"]["authority"] = "  decide  "
        write(self.eng / "context.json", json.dumps(ctx))
        _f, resolve, gaps = self.verd("dono · context.json#requester.authority")
        self.assertTrue(resolve, gaps)

    def test_context_json_invalido_nao_passa_por_bom(self):
        write(self.eng / "context.json", "{ isto nao e json")
        _f, resolve, gaps = self.verd("dono · context.json#funding_gate")
        self.assertFalse(resolve)
        self.assertIn("nao e JSON valido", "; ".join(gaps))

    def test_context_json_ausente(self):
        os.remove(self.eng / "context.json")
        _f, resolve, gaps = self.verd("dono · context.json#funding_gate")
        self.assertFalse(resolve)
        self.assertIn("context.json nao existe", "; ".join(gaps))

    def test_literal_request_continua_a_resolver_pelas_duas_formas(self):
        for txt in ("context.json.literal_request", "context.json#literal_request"):
            with self.subTest(txt=txt):
                forma, resolve, gaps = self.verd(txt)
                self.assertTrue(forma)
                self.assertTrue(resolve, gaps)


# ------------------------------------------------------------------- controlos

class ControlosDasCincoClasses(Base):

    def test_as_classes_antigas_continuam_a_resolver(self):
        casos = [
            ("documento", "Requisitos.pdf · p.2"),
            ("transcricao", "reuniao.vtt#[00:12:03]"),
            ("xlsx-celula", "mapa.xlsx#Folha1!B12"),
            ("answers", "answers.md#Prazos-por-classe"),
        ]
        for nome, txt in casos:
            with self.subTest(classe=nome):
                forma, resolve, gaps = self.verd(txt)
                self.assertTrue(forma, nome)
                self.assertTrue(resolve, "{}: {}".format(nome, gaps))

    def test_ficheiro_citado_que_nao_esta_no_engagement_continua_a_avisar(self):
        _f, resolve, gaps = self.verd("Inexistente.pdf#¶4")
        self.assertFalse(resolve)
        self.assertIn("nao esta em inputs/", "; ".join(gaps))

    def test_a_forma_lite_continua_a_ser_verificada_por_classe(self):
        """`· p.4` não nomeia ficheiro nenhum dentro do span do localizador: o alvo
        verifica-se pela classe (o engagement tem um documento), como antes."""
        _f, resolve, _g = self.verd("Inexistente.pdf · p.4")
        self.assertTrue(resolve)
        eng2 = Path(self.tmp) / "sem-doc"
        write(eng2 / "context.json", json.dumps(CTX))
        _f2, resolve2, gaps2 = self.verd("· p.4", eng2)
        self.assertFalse(resolve2)
        self.assertIn("nao tem documento", "; ".join(gaps2))

    def test_evidencia_sem_locator_continua_sem_locator(self):
        forma, _r, _g = self.verd("o dono disse que sim")
        self.assertFalse(forma)

    def test_um_caminho_context_json_nao_e_excepcao_cega(self):
        """A excepção literal continua a ser só `literal_request`; os outros campos
        passam pelo resolvedor e podem falhar."""
        self.assertTrue(D.LOCATOR_EXCEPTION.search("context.json.literal_request"))
        self.assertFalse(D.LOCATOR_EXCEPTION.search("context.json#requester.authority"))


# --------------------------------------------- índices posicionais do resolvedor

class IndicesDoResolvedor(unittest.TestCase):
    """O resolvedor indexava `LOCATOR_PATTERNS[5]` e `[6]` — acrescentar uma classe no
    sítio errado mudava silenciosamente o significado de duas verificações. Passa a
    procurar por nome; este teste segura as duas pontas."""

    def test_o_resolvedor_procura_por_nome(self):
        for nome in ("answers", "enquadramento", "enquadramento-tema", "contexto"):
            self.assertIn(nome, D.LOCATOR_BY_NAME)

    def test_os_nomes_e_as_posicoes_nao_divergiram(self):
        nomes = [n for n, _rx in D.LOCATOR_PATTERNS]
        self.assertEqual(nomes[5], "answers")
        self.assertEqual(nomes[6], "enquadramento")
        self.assertEqual(len(set(nomes)), len(nomes), "nomes de classe duplicados")

    ORIGINAIS = ["xlsx-celula", "extraction-json", "replay", "transcricao",
                 "documento", "answers", "enquadramento", "extraccao-directa"]
    ACRESCENTADAS = ["enquadramento-tema", "contexto", "tabela-csv"]

    def test_as_classes_novas_ficam_no_fim(self):
        """A invariante, nao o retrato.

        A versao anterior fixava a cauda literal (`[-2:]`) e por isso falhava a cada
        classe nova — inclusive quando a classe estava CERTA e no sitio certo. O que
        tem de se segurar e outra coisa: o bloco original nao se mexe (as posicoes 5 e
        6 eram indexadas), e tudo o que se acrescenta vai para depois dele, pela ordem
        em que foi acrescentado."""
        nomes = [n for n, _rx in D.LOCATOR_PATTERNS]
        self.assertEqual(nomes[:len(self.ORIGINAIS)], self.ORIGINAIS,
                         "o bloco original de classes mudou de posicao")
        self.assertEqual(nomes[len(self.ORIGINAIS):], self.ACRESCENTADAS,
                         "uma classe nova foi inserida no meio, nao acrescentada ao fim")


# ------------------------------------------------------- o guarda, ponta a ponta

class GuardaDeConfirmed(Base):

    def rows(self, support):
        return [{"id": "C-001", "state": "Confirmed", "resolved": False,
                 "lens": "business", "ronda": "R-01", "support": support, "extra": ""}]

    def test_a_linha_do_enquadramento_deixa_de_aparecer_sem_locator(self):
        a = D.audit_confirmed_locators(
            self.rows("declaração do dono, 2026-09-11 · enquadramento.md#T3"), self.eng)
        self.assertEqual(a["sem_locator"], [])
        self.assertEqual(a["alvo_ausente"], [])
        self.assertEqual(a["com_locator"], 1)

    def test_a_linha_com_alvo_inexistente_continua_a_avisar(self):
        a = D.audit_confirmed_locators(
            self.rows("declaração do dono · enquadramento.md#T4"), self.eng)
        self.assertEqual(a["sem_locator"], [])
        self.assertEqual([x["id"] for x in a["alvo_ausente"]], ["C-001"])

    def test_o_campo_de_arranque_conta_como_locator(self):
        a = D.audit_confirmed_locators(
            self.rows("declaração do dono · context.json#requester.authority"), self.eng)
        self.assertEqual(a["com_locator"], 1)
        self.assertEqual(a["sem_locator"], [])

    def test_o_relatorio_publica_as_classes_novas(self):
        a = D.audit_confirmed_locators(self.rows("dono · enquadramento.md#T1"), self.eng)
        self.assertIn("enquadramento-tema", a["regex"])
        self.assertIn("contexto", a["regex"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
