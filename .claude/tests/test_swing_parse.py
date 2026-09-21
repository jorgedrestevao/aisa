"""R2 / DEF-P4-01 — a classe do `swing` só se separa onde ela existe.

`docs/PILOT_RUNTIME_CORRECTION_PLAN.md` → R2. `parse_swing` partia no **primeiro**
dois-pontos, onde quer que ele estivesse, e não validava o prefixo. Uma célula escrita
`decisivo — serve M-1 (…). Duas respostas: (a) …` era cortada em `respostas:`: a classe
ficava a frase inteira colada (`decisivo—servem-1(…)`) e o texto perdia tudo o que vinha
antes — incluindo `serve M-1` e o marcador `TO-BE DIVERGENCE`, as duas formas da primeira
declaração de P-26. Em P4 R-01: 20 de 20 linhas dadas como não declarando nenhuma das
duas, `decisivas = 0`, `0 diagnostics`.

Duas metades:

* **positivo** — as três classes, com e sem acento, com espaços, com dois-pontos a mais
  no corpo, com travessão e com hífen: a classe lê-se, o texto fica inteiro e as
  declarações sobrevivem. A forma canónica dá exactamente o mesmo resultado de antes.
* **negativo** — uma classe desconhecida **não** é inventada nem parte a frase: fica
  `não avaliada`, com o texto inteiro, e o motor diz que não a avaliou. Um caso não
  conforme nunca conta como ausência comprovada de `M-n`.

Fixtures sintéticas — nenhum engagement real é lido ou escrito.

    python .claude/tests/test_swing_parse.py
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
TODAY = date(2026, 9, 11)


def load_dashboard():
    path = os.path.join(ROOT, "library", "kernel", "tools", "dashboard.py")
    spec = importlib.util.spec_from_file_location("aisa_dashboard_swing", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


D = load_dashboard()

CORPO = ("serve M-1 (separação de funções). Duas respostas: (a) um perfil (b) dois "
         "perfis. Move `plano de imposição de permissões`.")


# ------------------------------------------------------ 1. a função, isolada

class ParseSwing(unittest.TestCase):

    def test_forma_canonica_das_tres_classes(self):
        for cls in ("decisivo", "dimensionante", "cosmetico"):
            with self.subTest(cls=cls):
                c, t, f = D.parse_swing("{}: {}".format(cls, CORPO))
                self.assertEqual(c, cls)
                self.assertEqual(t, CORPO)
                self.assertEqual(f, "canonica")

    def test_cosmetico_com_acento_e_a_mesma_classe(self):
        c, t, f = D.parse_swing("cosmético: não muda nada de material.")
        self.assertEqual(c, "cosmetico")
        self.assertEqual(t, "não muda nada de material.")
        self.assertEqual(f, "canonica")

    def test_dois_pontos_a_mais_no_corpo_nao_cortam_a_frase(self):
        raw = "dimensionante: muda o esforço: entre 2 e 5 ecrãs. Duas respostas: a ou b."
        c, t, f = D.parse_swing(raw)
        self.assertEqual(c, "dimensionante")
        self.assertEqual(t, "muda o esforço: entre 2 e 5 ecrãs. Duas respostas: a ou b.")
        self.assertEqual(f, "canonica")

    def test_espacos_e_marcacao_a_volta_da_classe(self):
        for raw in ("  decisivo :  " + CORPO, "**decisivo**: " + CORPO,
                    "`decisivo`: " + CORPO):
            with self.subTest(raw=raw[:18]):
                c, t, f = D.parse_swing(raw)
                self.assertEqual(c, "decisivo")
                self.assertIn("serve M-1", t)

    def test_travessao_e_hifen_recuperam_a_classe_e_guardam_o_texto(self):
        for sep in ("—", "–", "-"):
            with self.subTest(sep=sep):
                c, t, f = D.parse_swing("decisivo {} {}".format(sep, CORPO))
                self.assertEqual(c, "decisivo")
                self.assertEqual(t, CORPO)
                self.assertEqual(f, "separador", "a forma desviada tem de ser assinalada")

    def test_m_n_e_tobe_sobrevivem_antes_do_segundo_separador(self):
        c, t, _f = D.parse_swing("decisivo — serve M-1 e M-2. Duas respostas: a ou b.")
        self.assertIn("M-1", t)
        self.assertIn("M-2", t)
        c, t, _f = D.parse_swing("decisivo — TO-BE DIVERGENCE. Duas respostas: a ou b.")
        self.assertIn("TO-BE DIVERGENCE", t)

    def test_classe_desconhecida_nao_e_inventada_nem_corta_a_frase(self):
        raw = "serve M-1 e por isso é decisivo. Duas respostas: a ou b."
        c, t, f = D.parse_swing(raw)
        self.assertEqual(c, "", "classificação não avaliada, não fabricada")
        self.assertEqual(t, raw, "o texto fica inteiro")
        self.assertEqual(f, "nao-lida")

    def test_prefixo_que_apenas_comeca_por_uma_palavra_de_classe(self):
        # `decisivamente` não é `decisivo`: a fronteira da palavra tem de valer.
        c, t, f = D.parse_swing("decisivamente: isto não é uma classe.")
        self.assertEqual(c, "")
        self.assertEqual(f, "nao-lida")
        self.assertEqual(t, "decisivamente: isto não é uma classe.")

    def test_celula_vazia_e_o_caminho_de_compatibilidade(self):
        for raw in ("", "   ", None):
            with self.subTest(raw=repr(raw)):
                c, t, f = D.parse_swing(raw)
                self.assertEqual((c, t, f), ("", "", "vazia"))

    def test_classe_sozinha_sem_frase(self):
        c, t, f = D.parse_swing("decisivo")
        self.assertEqual(c, "decisivo")
        self.assertEqual(t, "")
        self.assertEqual(f, "canonica")


# ------------------------------------------------- 2. a linha e o árbitro

SU = """# Shared Understanding — fx

> Engagement: fx
> Fase actual: Discovery

## Unknown

| id | lens | pergunta | quem responde | criticidade | custo | swing | ronda |
|----|------|----------|---------------|-------------|-------|-------|-------|
{rows}
"""


def su_with(swings, crit="Med"):
    rows = []
    for i, sw in enumerate(swings, start=1):
        rows.append("| U-{:03d} | data | Pergunta {}? | o dono | {} | email | {} | R-01 |"
                    .format(i, i, crit, sw))
    return SU.format(rows="\n".join(rows))


class LinhaEArbitro(unittest.TestCase):

    def arb(self, swings, **kw):
        _h, rows, _m, diags = D.parse_su(su_with(swings))
        return rows, D.arbiter_declarations(rows, **kw), diags

    def test_a_forma_desviada_declara_o_mesmo_que_a_canonica(self):
        canon = ["decisivo: " + CORPO]
        desvio = ["decisivo — " + CORPO]
        r_a, a_a, _d = self.arb(canon)
        r_b, a_b, _d = self.arb(desvio)
        self.assertEqual(r_a[0]["swing_class"], r_b[0]["swing_class"])
        self.assertEqual(r_a[0]["swing_text"], r_b[0]["swing_text"])
        self.assertEqual(a_a["decisivas"], a_b["decisivas"], 1)
        self.assertEqual(a_a["sem_citacao_m"], a_b["sem_citacao_m"], [])
        self.assertEqual(a_a["sem_declaracao"], a_b["sem_declaracao"], [])

    def test_o_marcador_tobe_sobrevive_na_forma_desviada(self):
        _r, arb, _d = self.arb(
            ["decisivo — TO-BE DIVERGENCE. Duas respostas: (a) manter (b) separar. "
             "Move `modelo de dados`."])
        self.assertEqual(arb["sem_citacao_m"], [])
        self.assertEqual(arb["sem_declaracao"], [])

    def test_um_caso_nao_conforme_nao_prova_ausencia_de_m_n(self):
        # classe ilegível, mas a frase traz `M-1`: a citação continua a ser lida.
        _r, arb, _d = self.arb(
            ["o que muda: serve M-1. Duas respostas: (a) um (b) dois. Move `custo`."])
        self.assertEqual(arb["sem_citacao_m"], [])
        self.assertEqual(arb["classe_nao_avaliada"][0]["id"], "U-001")
        self.assertEqual(arb["decisivas"], 0, "não avaliada não é decisiva")

    def test_classe_nao_lida_nao_herda_o_default_de_compatibilidade(self):
        rows, _a, _d = self.arb(["texto sem classe nenhuma. Duas respostas: a ou b."])
        self.assertEqual(rows[0]["swing_class"], "")
        self.assertEqual(rows[0]["swing_form"], "nao-lida")
        self.assertFalse(rows[0]["swing_inferred"], "a célula não está vazia")

    def test_celula_vazia_continua_a_valer_dimensionante(self):
        rows, _a, _d = self.arb([""])
        self.assertEqual(rows[0]["swing_class"], D.DEFAULT_SWING)
        self.assertTrue(rows[0]["swing_inferred"])
        self.assertEqual(rows[0]["swing_form"], "vazia")

    def test_decisivas_conta_as_quatro_formas_que_abrem_por_decisivo(self):
        _r, arb, _d = self.arb([
            "decisivo: " + CORPO,
            "decisivo — " + CORPO,
            "decisivo - " + CORPO,
            "**decisivo**: " + CORPO,
            "dimensionante: muda o tamanho. Duas respostas: a ou b. Move `custo`.",
        ])
        self.assertEqual(arb["decisivas"], 4)

    def test_diagnostico_agregado_por_forma_com_ids(self):
        _r, _a, diags = self.arb([
            "decisivo — " + CORPO,
            "decisivo - " + CORPO,
            "isto não abre por classe nenhuma. Duas respostas: a ou b.",
        ])
        msgs = [d["message"] for d in diags]
        sep = [m for m in msgs if "separador" in m]
        nao = [m for m in msgs if "NAO avaliada" in m]
        self.assertEqual(len(sep), 1, "um aviso agregado, não um por linha")
        self.assertEqual(len(nao), 1)
        self.assertIn("U-001", sep[0])
        self.assertIn("U-002", sep[0])
        self.assertIn("U-003", nao[0])
        self.assertTrue(all(d["where"] == "shared-understanding.md" for d in diags))

    def test_a_forma_canonica_nao_gera_diagnostico(self):
        _r, _a, diags = self.arb(["decisivo: " + CORPO,
                                  "cosmético: não muda nada. Duas respostas: a ou b."])
        self.assertEqual([d for d in diags if "swing" in d["message"]], [])

    def test_rotulo_de_negocio_da_classe_por_ler(self):
        self.assertEqual(D.swing_label("decisivo"), "muda o caminho")
        self.assertEqual(D.swing_label(""), "peso por classificar")


# ------------------------------------------------------ 3. consumidores

def write(path, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    with io.open(path, "w", encoding="utf-8") as fh:
        fh.write(body)


class Consumidores(unittest.TestCase):
    """Agenda, itens e JSON do motor — medidos no modelo, não no regex."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="aisa-r2-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def mk(self, slug, swings):
        eng = Path(self.tmp) / slug
        write(eng / "_state.json", json.dumps({
            "engagement": slug, "pack": "pp", "phase": "discovery", "round": "R-01",
            "aisa_version": "0.1.0", "created": "2026-09-01T00:00:00Z"}))
        write(eng / "context.json", json.dumps(
            {"literal_request": "x", "requester": {"name": "n", "role": "r"}}))
        write(eng / "shared-understanding.md", su_with(swings))
        write(eng / "decisions.md", "# Decisions\n")
        return D.build_model(eng, TODAY)

    def test_a_agenda_e_os_itens_leem_a_mesma_classe_nas_duas_formas(self):
        m_a = self.mk("canon", ["decisivo: " + CORPO])
        m_b = self.mk("desvio", ["decisivo — " + CORPO])
        self.assertEqual([i["swing_class"] for i in m_a["agenda"]["reuniao"]
                          + m_a["agenda"]["outro_canal"]],
                         [i["swing_class"] for i in m_b["agenda"]["reuniao"]
                          + m_b["agenda"]["outro_canal"]])
        it_a = {i["id"]: i for i in m_a["status"]["items"]}
        it_b = {i["id"]: i for i in m_b["status"]["items"]}
        self.assertEqual(it_a["U-001"]["swing_class"], it_b["U-001"]["swing_class"])
        self.assertEqual(it_a["U-001"]["swing_text"], it_b["U-001"]["swing_text"])

    def test_o_json_do_motor_expoe_a_forma_lida(self):
        m = self.mk("formas", ["decisivo: " + CORPO, "decisivo — " + CORPO,
                               "sem classe nenhuma aqui. Duas respostas: a ou b."])
        formas = {r["id"]: r["swing_form"] for r in m["su"]["rows"]}
        self.assertEqual(formas, {"U-001": "canonica", "U-002": "separador",
                                  "U-003": "nao-lida"})
        self.assertEqual(len([d for d in m["diagnostics"] if "swing" in d["message"]]), 2)

    def test_uma_linha_por_classificar_nao_desaparece_da_agenda(self):
        m = self.mk("porler", ["sem classe nenhuma aqui. Duas respostas: a ou b."])
        ids = [i["id"] for i in m["agenda"]["reuniao"] + m["agenda"]["outro_canal"]
               + m["agenda"]["nao_gastar"]]
        self.assertIn("U-001", ids)


if __name__ == "__main__":
    unittest.main(verbosity=2)
