"""R3–R6 — o árbitro das declarações P-26 lê o que a linha declara, e só isso.

`docs/PILOT_RUNTIME_CORRECTION_PLAN.md` → R3, R4, R5, R6.

* **R3 / DEF-P2-01** — a anotação que `states.md` manda escrever quando o árbitro
  rebaixa uma linha por falta da declaração (i) cita `TO-BE DIVERGENCE` **dentro de
  uma frase que diz que a linha não a declara**. Uma correspondência de presença sobre
  a célula inteira lê a nota de auditoria como sendo a declaração: assim que uma linha
  é correctamente rebaixada, a corrida seguinte deixa de a ver como problema. Corpo e
  anotação passam a separar-se antes da avaliação — e os dois ficam no ficheiro e no
  modelo.
* **R4 / DEF-P1-03** — orações paralelas com consequências distintas são duas
  alternativas; um ponto-e-vírgula entre duas consequências da **mesma** resposta não
  é. O caso comparativo (U-021) tem teste próprio.
* **R6 / DEF-P3-01** — um tecto de volume não é um tecto de verba: termos polissémicos
  exigem contexto financeiro.

Fixtures sintéticas — nenhum engagement real é lido ou escrito.

    python .claude/tests/test_arbiter_declarations.py
"""

import importlib.util
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_dashboard():
    path = os.path.join(ROOT, "library", "kernel", "tools", "dashboard.py")
    spec = importlib.util.spec_from_file_location("aisa_dashboard_arbiter", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


D = load_dashboard()

SU = """# Shared Understanding — fx

> Engagement: fx
> Fase actual: Discovery

## Unknown

| id | lens | pergunta | quem responde | criticidade | custo | swing | ronda |
|----|------|----------|---------------|-------------|-------|-------|-------|
{rows}
"""

ANOT_I = " — reclassificado P-26 (R-01): não cita `M-n` nem declara TO-BE DIVERGENCE"
ANOT_EIXO = " — reclassificado P-26 (R-02): o swing não nomeia o eixo técnico que muda"
ANOT_CRIT = " — criticidade baixada P-26 (R-01): sustentava-se em Critical"


def rows_for(swings, claims=None, crit="Low"):
    out = []
    for i, sw in enumerate(swings, start=1):
        claim = (claims or {}).get(i, "Pergunta {}?".format(i))
        out.append("| U-{:03d} | business | {} | o dono | {} | email | {} | R-01 |"
                   .format(i, claim, crit, sw))
    return SU.format(rows="\n".join(out))


def arb(swings, claims=None, crit="Low"):
    _h, rows, _m, _d = D.parse_su(rows_for(swings, claims, crit))
    return rows, D.arbiter_declarations(rows)


def falta(a, rid):
    return rid in {x["id"] for x in a["sem_declaracao"]}


# ------------------------------------------- R3: anotação sancionada vs corpo

CORPO_SEM_DECL = ("cosmético: serve enquadramento.md#T4 (não acumular pendentes antigos). "
                  "Respostas: (a) há prazos por classe — acrescenta relógio, move `modelo "
                  "de dados`; (b) não há prazo formal — move `esforço de alto nível`")
CORPO_TOBE = ("decisivo: serve TO-BE DIVERGENCE — o alvo tem de escolher. Duas respostas: "
              "(a) manter (b) automatizar. Move `esforço de alto nível`.")
CORPO_M = ("decisivo: serve M-1. Duas respostas: (a) um perfil (b) dois perfis. "
           "Move `plano de imposição de permissões`.")


class AnotacaoSancionada(unittest.TestCase):

    def test_a_anotacao_nao_faz_a_declaracao_que_ela_diz_faltar(self):
        _r, a = arb([CORPO_SEM_DECL + ANOT_I])
        self.assertIn("U-001", {x["id"] for x in a["sem_citacao_m"]})
        self.assertTrue(falta(a, "U-001"))

    def test_declaracao_genuina_com_anotacao_continua_aceite(self):
        for corpo in (CORPO_TOBE, CORPO_M):
            with self.subTest(corpo=corpo[:12]):
                _r, a = arb([corpo + ANOT_I])
                self.assertEqual(a["sem_citacao_m"], [])
                self.assertFalse(falta(a, "U-001"))

    def test_controlo_sem_anotacao_nenhuma(self):
        _r, a = arb([CORPO_M])
        self.assertEqual(a["sem_citacao_m"], [])
        self.assertEqual(a["sem_declaracao"], [])

    def test_anotacao_que_cita_um_m_n_tambem_nao_conta(self):
        anot = " — reclassificado P-26 (R-01): não cita `M-n`; o M-1 que invocava não é seu"
        _r, a = arb([CORPO_SEM_DECL + anot])
        self.assertIn("U-001", {x["id"] for x in a["sem_citacao_m"]})

    def test_varias_anotacoes_acumuladas_cortam_na_primeira(self):
        _r, a = arb([CORPO_SEM_DECL + ANOT_I + ANOT_EIXO])
        self.assertIn("U-001", {x["id"] for x in a["sem_citacao_m"]})
        corpo, anot = D.split_annotation(CORPO_SEM_DECL + ANOT_I + ANOT_EIXO)
        self.assertEqual(corpo, CORPO_SEM_DECL)
        self.assertIn("R-01", anot)
        self.assertIn("R-02", anot)

    def test_o_marcador_no_corpo_e_diferente_do_marcador_na_anotacao(self):
        """`TO-BE DIVERGENCE` escrito na frase da linha é declaração; escrito dentro
        do sufixo sancionado é auditoria."""
        corpo, anot = D.split_annotation(CORPO_TOBE + ANOT_I)
        self.assertIn("TO-BE DIVERGENCE", corpo)
        self.assertIn("TO-BE DIVERGENCE", anot)
        self.assertTrue(D.ARB_TOBE_RE.search(corpo))

    def test_texto_que_apenas_menciona_p26_nao_e_anotacao(self):
        frase = ("decisivo: serve M-1 e cumpre P-26. Duas respostas: a ou b. "
                 "Move `custo`.")
        corpo, anot = D.split_annotation(frase)
        self.assertEqual(corpo, frase)
        self.assertEqual(anot, "")

    def test_a_linha_ja_rebaixada_nao_volta_a_ser_promovida(self):
        rows, _a = arb([CORPO_SEM_DECL + ANOT_I])
        self.assertEqual(rows[0]["swing_class"], "cosmetico")

    def test_o_ficheiro_e_o_modelo_guardam_a_anotacao(self):
        rows, _a = arb([CORPO_SEM_DECL + ANOT_I])
        self.assertIn("reclassificado P-26", rows[0]["swing_text"])
        self.assertIn("reclassificado P-26", rows[0]["swing_annot"])
        self.assertNotIn("reclassificado P-26", rows[0]["swing_body"])

    def test_a_anotacao_da_criticidade_nao_muda_a_criticidade_lida(self):
        _h, rows, _m, _d = D.parse_su(SU.format(rows=(
            "| U-001 | business | Pergunta? | o dono | Low" + ANOT_CRIT
            + " | email | " + CORPO_SEM_DECL + ANOT_I + " | R-01 |")))
        self.assertEqual(rows[0]["criticidade"], "Low")


# ------------------------------ R3 (2a parte): o sufixo reconhece-se INTEIRO

class SufixoSancionadoInteiro(unittest.TestCase):
    """Duas palavras nao chegavam para identificar a anotacao: uma frase do corpo que
    mencionasse a regra era cortada ai, e o `M-n` legitimo que vinha a seguir deixava
    de contar. O sufixo e `— reclassificado P-26 (<ronda>): <razão>` — verbo, regra,
    ronda entre parênteses e dois-pontos (states.md → «The arbiter's two effects»)."""

    CORPO_COM_MENCAO = ("decisivo: o campo reclassificado P-26 integra o histórico. "
                        "Serve M-1 e duas respostas: (a) manter (b) mudar. "
                        "Move `modelo de dados`.")

    def test_mencao_no_corpo_nao_e_anotacao_e_o_m_n_conta(self):
        corpo, anot = D.split_annotation(self.CORPO_COM_MENCAO)
        self.assertEqual(anot, "")
        self.assertIn("M-1", corpo)
        _r, a = arb([self.CORPO_COM_MENCAO])
        self.assertEqual(a["sem_citacao_m"], [])
        self.assertFalse(falta(a, "U-001"))

    def test_mencao_sem_ronda_nem_dois_pontos_nao_e_anotacao(self):
        for txt in ("decisivo: reclassificado P-26 no passado; serve M-2. "
                    "Duas respostas: a ou b. Move `custo`.",
                    "decisivo: serve M-2 — reclassificado P-26 R-01 sem parênteses. "
                    "Duas respostas: a ou b. Move `custo`."):
            with self.subTest(txt=txt[:30]):
                _corpo, anot = D.split_annotation(txt)
                self.assertEqual(anot, "")

    def test_o_sufixo_completo_continua_a_ser_anotacao(self):
        for txt in (CORPO_SEM_DECL + ANOT_I,
                    CORPO_SEM_DECL + " -- reclassificado P-26 (R-02): sem eixo",
                    CORPO_SEM_DECL + " — criticidade baixada P-26 (F-01): sustentava-se"):
            with self.subTest(txt=txt[-40:]):
                _corpo, anot = D.split_annotation(txt)
                self.assertTrue(anot, "sufixo prescrito tem de ser reconhecido")

    def test_o_m_n_que_esta_so_na_anotacao_continua_a_nao_contar(self):
        txt = (CORPO_SEM_DECL
               + " — reclassificado P-26 (R-01): não cita `M-n`; o M-1 que invocava "
                 "não é seu")
        _r, a = arb([txt])
        self.assertIn("U-001", {x["id"] for x in a["sem_citacao_m"]})


# --------------------------------- R4: duas respostas, em oracoes paralelas

PARALELA = ("dimensionante: serve M-2 — tradução implica um conteúdo com variantes de "
            "língua; percurso próprio implica conteúdo versionado por geografia. "
            "Move `modelo de dados`.")
PARALELA_COND = ("decisivo: serve M-2 — sem essa lista o módulo 7 não é construível; "
                 "se existir já estruturada, o trabalho é de carregamento. "
                 "Move `modelo de dados`.")
COMPARATIVA = ("dimensionante: serve M-1 — sete módulos com três mecânicas distintas "
               "custam várias vezes o que custa um percurso com a Fase 2. "
               "Move `esforço de alto nível` e `custo`.")


class DuasRespostas(unittest.TestCase):

    def vered(self, swing):
        rows, a = arb([swing])
        rid = rows[0]["id"]
        if rid in {x["id"] for x in (a["alternativas_nao_avaliadas"] or [])}:
            return "nao-avaliado"
        return "nao" if falta(a, rid) else "sim"

    def test_oracoes_paralelas_com_consequencias_distintas(self):
        for sw in (PARALELA, PARALELA_COND):
            with self.subTest(sw=sw[:24]):
                self.assertEqual(self.vered(sw), "sim")

    def test_as_formas_classicas_continuam_a_valer(self):
        base = "decisivo: serve M-1 — {} Move `componentes`."
        for nome, frase in (
                ("ou", "repositório novo ou apontadores para os existentes."),
                ("(a)/(b)", "(a) construir próprio (b) apontar para o existente."),
                ("vs", "um idioma vs dois idiomas."),
                ("se/se", "se existir, carrega-se; se não existir, constrói-se."),
                ("contra", "identidade corporativa contra perfis próprios."),
                ("entre/e", "entre um perfil e dois perfis.")):
            with self.subTest(forma=nome):
                self.assertEqual(self.vered(base.format(frase)), "sim")

    def test_o_caso_comparativo_fica_nao_avaliado(self):
        """U-021 de P1: a frase compara o custo de dois âmbitos — mas nomear duas
        coisas comparadas não é nomear duas respostas, e as duas respostas de U-021
        estão na pergunta, não no swing. O motor não decide: declara que não avaliou,
        e por isso a linha também não é dada como estando em falta."""
        self.assertEqual(self.vered(COMPARATIVA), "nao-avaliado")
        _r, a = arb([COMPARATIVA])
        self.assertFalse(falta(a, "U-001"))
        self.assertEqual(a["alternativas_nao_avaliadas"][0]["id"], "U-001")

    def test_ponto_e_virgula_entre_consequencias_da_mesma_resposta(self):
        """A regra universal `tem ; => duas alternativas` é a que NÃO se aplicou:
        aqui o ponto-e-vírgula separa duas consequências de uma só resposta, e o
        segundo ramo não tem antecedente nenhum."""
        self.assertEqual(self.vered(
            "decisivo: serve M-1 — acrescenta relógio, alerta e medição; "
            "move `modelo de dados` e `esforço de alto nível`."), "nao")

    def test_o_mesmo_antecedente_duas_vezes_nao_sao_duas_respostas(self):
        """Reproduzido em revisão: dois verbos de consequência e um só antecedente —
        «a automatização reduz erros; a automatização aumenta a rastreabilidade» —
        são duas consequências da MESMA resposta. Um ramo só conta quando traz
        alguma coisa que o outro não tem."""
        self.assertEqual(self.vered(
            "decisivo: serve M-1 — a automatização reduz erros; a automatização "
            "aumenta a rastreabilidade. Move `esforço de alto nível`."), "nao")

    def test_o_mesmo_antecedente_com_acentos_e_artigos_diferentes(self):
        self.assertEqual(self.vered(
            "decisivo: serve M-1 — a automatização reduz erros; automatização aumenta "
            "a rastreabilidade. Move `custo`."), "nao")

    def test_com_e_sem_sao_ramos_diferentes(self):
        """Reproduzido em revisão: «com validação exige aprovação; sem validação
        permite publicação imediata» são dois ramos, e a diferença está toda no
        qualificador. `com`/`sem`, como `não`, `só`, `mais` e `menos`, não são
        palavras vazias — são o que separa as respostas."""
        self.assertEqual(self.vered(
            "decisivo: serve M-1 — com validação exige aprovação; sem validação "
            "permite publicação imediata. Move `padrão arquitetural`."), "sim")

    def test_qualificadores_de_quantidade_tambem_distinguem(self):
        self.assertEqual(self.vered(
            "dimensionante: serve M-1 — só o resumo exige um ecrã; o detalhe completo "
            "exige três ecrãs. Move `esforço de alto nível`."), "sim")

    def test_um_demonstrativo_nao_faz_um_ramo_novo(self):
        """O contraponto: trocar «a» por «esta» não cria uma resposta nova."""
        self.assertEqual(self.vered(
            "decisivo: serve M-1 — a automatização reduz erros; esta automatização "
            "aumenta a rastreabilidade. Move `custo`."), "nao")

    def test_antecedentes_que_so_diferem_por_acrescimo_ficam_por_avaliar(self):
        """Um lado contém o outro («o contador» / «o contador diário»): pode ser um
        ramo novo ou a mesma resposta dita com mais detalhe. O motor não decide."""
        self.assertEqual(self.vered(
            "dimensionante: serve M-1 — o contador exige um campo derivado; o contador "
            "diário exige o mesmo campo. Move `modelo de dados`."), "nao-avaliado")

    def test_antecedentes_distintos_com_uma_palavra_em_comum(self):
        """«confirmação em mobilidade» contra «confirmação ao computador»: partilham
        uma palavra e cada um traz a sua — são dois ramos."""
        self.assertEqual(self.vered(
            "dimensionante: serve M-1 — confirmação em mobilidade obriga a desenhar "
            "primeiro para ecrã pequeno; confirmação ao computador dispensa esse "
            "cuidado. Move `esforço de alto nível`."), "sim")

    def test_a_negacao_distingue_o_ramo(self):
        """«mostrar» contra «não mostrar» são dois ramos: a negação é a diferença,
        e por isso `não` não é palavra vazia."""
        self.assertEqual(self.vered(
            "dimensionante: serve M-1 — mostrar o contador exige um campo derivado "
            "novo; não mostrar mantém a superfície como está. Move `modelo de dados`."),
            "sim")

    def test_lista_de_campos_nao_e_alternativa(self):
        self.assertEqual(self.vered(
            "dimensionante: serve M-1 — os campos em falta: nome; morada; NIF. "
            "Move `modelo de dados`."), "nao")

    def test_uma_so_alternativa(self):
        self.assertEqual(self.vered(
            "dimensionante: serve M-1 — implica guardar a melhor tentativa. "
            "Move `custo`."), "nao")

    def test_pontuacao_dentro_de_citacao(self):
        self.assertEqual(self.vered(
            'cosmético: serve M-1 — o dono diz "isto fecha; aquilo não". '
            "Move `custo`."), "nao")

    def test_um_pronome_relativo_nao_e_uma_comparacao(self):
        """`o que a auditoria quer` não é `mais do que`: a forma comparativa exige a
        comparação, senão o «não avaliado» virava a resposta a tudo."""
        self.assertEqual(self.vered(
            "dimensionante: serve M-1 — é o passo mais repetido e o que a auditoria "
            "quer retirar à equipa. Move `esforço de alto nível`."), "nao")

    def test_a_declaracao_ausente_continua_a_pesar_no_conjunto(self):
        """P-26 é conjunção: reconhecer a segunda declaração não dispensa as outras."""
        _r, a = arb(["dimensionante: tradução implica variantes de língua; percurso "
                     "próprio implica conteúdo versionado. Move `modelo de dados`."])
        self.assertTrue(falta(a, "U-001"), "sem `M-n` nem TO-BE continua em falta")
        self.assertIn("nao cita M-n", a["sem_declaracao"][0]["motivo"])


# ------------------------------------ R6: tecto de volume nao e tecto de verba

SWING_OK = ("decisivo: serve M-1. Duas respostas: (a) sim (b) não. "
            "Move `esforço de alto nível` e `custo`.")


def fin(perguntas, gate=False):
    """Perguntas da lente financeira, medidas pela faceta do modelo."""
    linhas = []
    for i, p in enumerate(perguntas, start=1):
        linhas.append("| U-{:03d} | financial | {} | o dono | Med | email | {} | R-01 |"
                      .format(i, p, SWING_OK))
    _h, rows, _m, _d = D.parse_su(SU.format(rows="\n".join(linhas)))
    ctx = {} if gate is None else {"funding_gate": gate}
    return D.funding_gate_audit(rows, ctx)


class PortaOrcamental(unittest.TestCase):
    """Com `funding_gate=false` a lente financeira não constrói envelope — mas
    `tecto`, `limiar` e `envelope` são palavras polissémicas, e a verificação
    assinalava o tecto de volume tal como o tecto de verba."""

    def assinaladas(self, perguntas, gate=False):
        return [x["id"] for x in fin(perguntas, gate)["infracoes"]]

    def test_tecto_de_volume_nao_e_tecto_de_verba(self):
        self.assertEqual(self.assinaladas(
            ["Qual é o tecto de volume que a solução tem de aguentar por mês?"]), [])
        self.assertEqual(self.assinaladas(
            ["Qual é o tecto de verba disponível para este projecto?"]), ["U-001"])

    def test_limiar_de_tolerancia_nao_e_limiar_de_aprovacao_orcamental(self):
        self.assertEqual(self.assinaladas(
            ["Qual é o limiar de tolerância a erros de classificação?"]), [])
        self.assertEqual(self.assinaladas(
            ["A partir de que limiar sobe a aprovação orçamental de nível?"]), ["U-001"])

    def test_envelope_de_tempo_nao_e_envelope_de_orcamento(self):
        self.assertEqual(self.assinaladas(
            ["Qual é o envelope de tempo até estar em produção?"]), [])
        self.assertEqual(self.assinaladas(
            ["Qual é o envelope de orçamento para o primeiro ano?"]), ["U-001"])

    def test_os_termos_inequivocos_continuam_a_valer_sozinhos(self):
        for p in ("Isto entra em CAPEX ou em OPEX?",
                  "Qual é o payback esperado?",
                  "Que verba está cabimentada?",
                  "Como se imputa o custo às direcções?",
                  "Qual é o ROI ao fim de dois anos?"):
            with self.subTest(pergunta=p[:26]):
                self.assertEqual(self.assinaladas([p]), ["U-001"], p)

    def test_aprovacao_sozinha_nao_e_contexto_financeiro(self):
        """Reproduzido em revisão: aprova-se conteúdo, classificação e acesso tanto
        como verba. Só `aprovação orçamental` conta — e conta pelo `orçamental`."""
        self.assertEqual(self.assinaladas(
            ["Qual é o limiar de confiança para aprovação automática da "
             "classificação?"]), [])
        self.assertEqual(self.assinaladas(
            ["Qual é o envelope de tempo para aprovação do conteúdo?"]), [])

    def test_aprovacao_orcamental_continua_a_contar(self):
        self.assertEqual(self.assinaladas(
            ["A partir de que limiar sobe a aprovação orçamental de nível?"]),
            ["U-001"])
        self.assertEqual(self.assinaladas(
            ["Que tecto de aprovação de despesa existe para este projecto?"]),
            ["U-001"])

    def test_capacidade_mensal_nao_e_pergunta_de_verba(self):
        self.assertEqual(self.assinaladas(
            ["Qual é a capacidade mensal do processo actual?"]), [])

    def test_custo_no_eixo_do_swing_nao_prova_que_a_pergunta_e_orcamental(self):
        """O eixo diz o que MUDA com a resposta, não de que a pergunta trata. Todas as
        perguntas deste ficheiro trazem `custo` no swing; só as de verba contam."""
        self.assertEqual(self.assinaladas(
            ["Quantas classes de prioridade existem hoje?"]), [])

    def test_o_termo_encontrado_vai_no_resultado_para_se_poder_contestar(self):
        infra = fin(["Qual é o tecto de verba disponível?"])["infracoes"]
        self.assertEqual(len(infra), 1)
        self.assertIn("verba", infra[0]["termo"].lower())

    def test_com_a_porta_aberta_ou_ausente_nao_ha_nada_a_verificar(self):
        for gate in (True, None):
            with self.subTest(gate=gate):
                a = fin(["Qual é o tecto de verba disponível?"], gate)
                self.assertFalse(a["aplicavel"])
                self.assertEqual(a["infracoes"], [])

    def test_so_a_lente_financeira_entra_na_verificacao(self):
        linhas = ["| U-001 | operations | Qual é o tecto de verba? | o dono | Med | "
                  "email | " + SWING_OK + " | R-01 |"]
        _h, rows, _m, _d = D.parse_su(SU.format(rows="\n".join(linhas)))
        a = D.funding_gate_audit(rows, {"funding_gate": False})
        self.assertEqual(a["infracoes"], [])
        self.assertEqual(a["financeiras_abertas"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
