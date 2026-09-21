"""R1 / DEF-P1-04 — o leitor de tabelas da Shared Understanding não perde linhas.

`docs/PILOT_RUNTIME_CORRECTION_PLAN.md` → R1. Uma única linha em branco a meio de uma
tabela da SU fazia o motor parar de contar ali: as linhas seguintes desapareciam do
dashboard, do `/status`, da agenda, do portão de saída de Discovery e da saúde
epistémica, com `0 diagnostics`. Medido em P1 R-01: 21 perguntas → 10.

Duas metades, e as duas contam:

* **positivo** — nenhuma linha reconhecível da secção desaparece, em qualquer das cinco
  secções, com uma ou várias linhas em branco, em LF e CRLF. Comparação por **ids e
  conteúdo**, não por quantidade.
* **negativo** — a leitura não passa a engolir o que não é da tabela: cabeçalho
  seguinte, prosa intercalada, tabela nova sob a mesma secção, exemplo dentro de bloco
  de código.

E o teste de consequência: uma pergunta grave depois da interrupção continua visível e
o portão de saída de Discovery **não** fica verde por desaparecimento de linhas.

Fixtures sintéticas em tempdir — nenhum engagement real é lido ou escrito.

    python .claude/tests/test_su_table_reader.py
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
    spec = importlib.util.spec_from_file_location("aisa_dashboard_tables", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


D = load_dashboard()

# --------------------------------------------------------------------- fixtures

HEAD = """# Shared Understanding — fx

> Engagement: fx
> Fase actual: Discovery

"""

COLS = {
    "Confirmed": ["id", "lens", "claim", "evidência", "verificado_em", "validade", "ronda"],
    "Assumed": ["id", "lens", "claim", "base da assumption", "verificado_em", "validade",
                "ronda"],
    "Unknown": ["id", "lens", "pergunta", "quem responde", "criticidade", "custo", "swing",
                "ronda"],
    "Conflicted": ["id", "lens", "conflito", "partes", "criticidade", "ronda"],
    "Risky": ["id", "lens", "risco", "impacto", "mitigação proposta", "criticidade", "ronda"],
}

SWING = "decisivo: serve M-1. Duas respostas: interno ou externo. Move `tecnologia`."


def cells_for(state, n, crit="Med"):
    """Uma linha por secção, com id previsível e conteúdo próprio (para comparar texto)."""
    pid = {"Confirmed": "C", "Assumed": "A", "Unknown": "U", "Conflicted": "X",
           "Risky": "R"}[state]
    rid = "{}-{:03d}".format(pid, n)
    claim = "conteudo proprio de {}".format(rid)
    if state == "Confirmed":
        return [rid, "business", claim, "ficheiro.pdf · p.1", "2026-09-11",
                "organizacional", "R-01"]
    if state == "Assumed":
        return [rid, "operations", claim, "base declarada", "2026-09-11",
                "organizacional", "R-01"]
    if state == "Unknown":
        return [rid, "data", claim + "?", "o dono", crit, "email", SWING, "R-01"]
    if state == "Conflicted":
        return [rid, "governance", claim, "dono vs TI", crit, "R-01"]
    return [rid, "user", claim, "impacto alto", "mitigar", crit, "R-01"]


def table(state, rows_cells, blanks_after=None, blank_count=1):
    """Bloco `## <state>` com as linhas dadas; `blanks_after` = índice (0-based) da
    linha após a qual entram `blank_count` linhas em branco."""
    heads = COLS[state]
    out = ["## " + state, "", "| " + " | ".join(heads) + " |",
           "|" + "|".join(["---"] * len(heads)) + "|"]
    if blanks_after == -1:
        out.extend([""] * blank_count)
    for i, cells in enumerate(rows_cells):
        out.append("| " + " | ".join(str(c) for c in cells) + " |")
        if blanks_after is not None and i == blanks_after:
            out.extend([""] * blank_count)
    out.append("")
    return "\n".join(out) + "\n"


def su_doc(blocks):
    return HEAD + "\n".join(blocks)


def parse(md):
    """-> (rows, sections_meta, diagnostics)"""
    _h, rows, meta, diags = D.parse_su(md)
    return rows, meta["sections"], diags


def ids_of(rows, state):
    return [r["id"] for r in rows if r["state"] == state]


def claims_of(rows, state):
    return [r["claim"] for r in rows if r["state"] == state]


# ------------------------------------------------------- 1. positivo: não perde

class NaoPerdeLinhas(unittest.TestCase):
    """A linha em branco é um lapso de escrita; não é o fim da tabela."""

    def _compare(self, state, n=8, blank_count=1, newline="\n"):
        cells = [cells_for(state, i) for i in range(1, n + 1)]
        limpo = su_doc([table(state, cells)])
        sujo = su_doc([table(state, cells, blanks_after=n // 2 - 1,
                             blank_count=blank_count)])
        if newline != "\n":
            limpo = limpo.replace("\n", newline)
            sujo = sujo.replace("\n", newline)
        a_rows, a_sec, a_diag = parse(limpo)
        b_rows, b_sec, b_diag = parse(sujo)
        self.assertEqual(ids_of(a_rows, state), ids_of(b_rows, state),
                         "{}: ids perdidos com linha em branco".format(state))
        self.assertEqual(claims_of(a_rows, state), claims_of(b_rows, state),
                         "{}: conteúdo alterado com linha em branco".format(state))
        self.assertEqual(a_sec[state]["open"], b_sec[state]["open"])
        self.assertEqual(a_sec[state]["open"], n)
        return a_diag, b_diag

    def test_as_cinco_seccoes_sobrevivem_a_uma_linha_em_branco(self):
        for state in ("Confirmed", "Assumed", "Unknown", "Conflicted", "Risky"):
            with self.subTest(state=state):
                self._compare(state)

    def test_varias_linhas_em_branco_seguidas(self):
        for n_blanks in (2, 3, 5):
            with self.subTest(linhas=n_blanks):
                self._compare("Unknown", blank_count=n_blanks)

    def test_crlf_tem_o_mesmo_resultado_que_lf(self):
        for state in ("Confirmed", "Unknown"):
            with self.subTest(state=state):
                self._compare(state, newline="\r\n")

    def test_linha_em_branco_antes_da_primeira_linha_do_corpo(self):
        cells = [cells_for("Unknown", i) for i in range(1, 4)]
        sujo = su_doc([table("Unknown", cells, blanks_after=-1)])
        rows, sec, diag = parse(sujo)
        self.assertEqual(ids_of(rows, "Unknown"), ["U-001", "U-002", "U-003"])
        self.assertEqual(sec["Unknown"]["open"], 3)
        self.assertTrue(diag)

    def test_a_anomalia_emite_diagnostico_com_seccao_e_linha(self):
        limpo_diag, sujo_diag = self._compare("Unknown")
        self.assertEqual([d for d in limpo_diag], [],
                         "tabela contínua não é anomalia — não deve avisar")
        self.assertEqual(len(sujo_diag), 1)
        d = sujo_diag[0]
        self.assertEqual(d["level"], "warn")
        self.assertEqual(d["where"], "shared-understanding.md")
        self.assertIn("linha em branco", d["message"])
        self.assertIn("Unknown", d["message"])
        self.assertGreater(d["line"], 0)
        # localizável: a linha do diagnóstico é mesmo uma linha em branco do ficheiro
        cells = [cells_for("Unknown", i) for i in range(1, 9)]
        sujo = su_doc([table("Unknown", cells, blanks_after=3)])
        self.assertEqual(sujo.splitlines()[d["line"] - 1].strip(), "")

    def test_uma_linha_em_branco_em_cada_uma_das_cinco_seccoes(self):
        blocks = []
        for state in ("Confirmed", "Assumed", "Unknown", "Conflicted", "Risky"):
            cells = [cells_for(state, i) for i in range(1, 5)]
            blocks.append(table(state, cells, blanks_after=1))
        rows, sec, diag = parse(su_doc(blocks))
        for state in ("Confirmed", "Assumed", "Unknown", "Conflicted", "Risky"):
            self.assertEqual(sec[state]["open"], 4, state)
            self.assertEqual(len(ids_of(rows, state)), 4, state)
        self.assertEqual(len(diag), 5, "um aviso por secção anómala")

    def test_linha_malformada_depois_da_interrupcao_continua_a_avisar(self):
        cells = [cells_for("Unknown", i) for i in range(1, 4)]
        md = su_doc([table("Unknown", cells, blanks_after=0)])
        md = md.replace("| U-003 | data |", "| U-003 | data | a | b | c | d | e | f | g |")
        rows, sec, diag = parse(md)
        self.assertIn("U-003", ids_of(rows, "Unknown"))
        self.assertTrue(any("celulas" in d["message"] for d in diag))
        self.assertTrue(any("linha em branco" in d["message"] for d in diag))

    def test_tabela_vazia_com_linha_em_branco_nao_rebenta(self):
        md = su_doc([table("Unknown", []), table("Risky", [])])
        rows, sec, diag = parse(md)
        self.assertEqual(rows, [])
        self.assertEqual(sec["Unknown"]["open"], 0)


# ---------------------------------------------- 2. negativo: não engole o resto

class NaoEngoleOResto(unittest.TestCase):
    """A tolerância à linha em branco pára onde a tabela acaba de verdade."""

    def test_para_no_cabecalho_seguinte(self):
        u = [cells_for("Unknown", i) for i in range(1, 4)]
        r = [cells_for("Risky", i) for i in range(1, 3)]
        rows, sec, _d = parse(su_doc([table("Unknown", u), table("Risky", r)]))
        self.assertEqual(ids_of(rows, "Unknown"), ["U-001", "U-002", "U-003"])
        self.assertEqual(ids_of(rows, "Risky"), ["R-001", "R-002"])
        self.assertEqual(sec["Unknown"]["open"], 3)
        self.assertEqual(sec["Risky"]["open"], 2)

    def test_nao_absorve_a_tabela_da_seccao_seguinte_apos_linha_em_branco(self):
        u = [cells_for("Unknown", i) for i in range(1, 4)]
        r = [cells_for("Risky", i) for i in range(1, 3)]
        md = su_doc([table("Unknown", u, blanks_after=1), table("Risky", r)])
        rows, sec, _d = parse(md)
        self.assertEqual(ids_of(rows, "Unknown"), ["U-001", "U-002", "U-003"])
        self.assertEqual(ids_of(rows, "Risky"), ["R-001", "R-002"])
        self.assertEqual([r_["state"] for r_ in rows if r_["id"] == "R-001"], ["Risky"])

    def test_prosa_intercalada_nao_apaga_a_linha_que_vem_a_seguir(self):
        """O critério do plano é «nenhuma linha reconhecível desaparece em silêncio».
        Prosa a meio da secção é a mesma anomalia que a linha em branco: a linha
        seguinte é lida, e a interrupção avisa."""
        u = [cells_for("Unknown", i) for i in range(1, 3)]
        md = su_doc([table("Unknown", u)])
        md += "\nNota do consultor sobre a passagem.\n\n"
        md += ("| U-900 | data | linha orfa depois de prosa? | o dono | Critical | "
               "email | " + SWING + " | R-01 |\n")
        rows, sec, diag = parse(md)
        self.assertEqual(ids_of(rows, "Unknown"), ["U-001", "U-002", "U-900"])
        self.assertEqual(sec["Unknown"]["open"], 3)
        texto = [d for d in diag if "texto entre linhas" in d["message"]]
        self.assertEqual(len(texto), 1)
        self.assertIn("Unknown", texto[0]["message"])
        self.assertEqual(texto[0]["level"], "warn")

    def test_uma_pergunta_grave_depois_de_prosa_conta_para_o_portao(self):
        """A consequência do caso acima: era exactamente assim que o portão podia
        abrir sem ninguém responder nada."""
        conf = [cells_for("Confirmed", i) for i in range(1, 13)]
        unk = [cells_for("Unknown", i) for i in range(1, 4)]
        md = su_doc([table("Confirmed", conf), table("Unknown", unk)])
        md += "\nNota de meio de tabela.\n\n"
        md += ("| U-004 | data | pergunta grave orfa? | o dono | Critical | email | "
               + SWING + " | R-01 |\n")
        rows, sec, _d = parse(md)
        graves = [r_["id"] for r_ in rows
                  if r_["state"] == "Unknown" and r_["criticidade"] == "Critical"]
        self.assertEqual(graves, ["U-004"])

    def test_uma_nota_com_um_pipe_no_meio_nao_e_um_registo(self):
        """`A | B` numa frase é prosa. Um registo da SU abre a linha com `|` —
        medido nas 27 SU em disco: 5224 linhas, nenhuma sem o pipe inicial."""
        u = [cells_for("Unknown", i) for i in range(1, 3)]
        md = su_doc([table("Unknown", u)])
        linha2 = "| " + " | ".join(str(c) for c in cells_for("Unknown", 2)) + " |"
        md = md.replace(
            linha2,
            linha2 + "\nNota: o dono decide entre A | B na proxima passagem.")
        rows, sec, _d = parse(md)
        self.assertEqual(ids_of(rows, "Unknown"), ["U-001", "U-002"])
        self.assertEqual(sec["Unknown"]["open"], 2)
        self.assertFalse([r_ for r_ in rows if r_["id"].startswith("Nota")])

    def test_prosa_no_fim_da_seccao_fecha_a_tabela_sem_aviso(self):
        """Texto DEPOIS da última linha não é interrupção: é um documento normal.
        Avisar aqui seria o ruído que faz deixar de ler o canal."""
        u = [cells_for("Unknown", i) for i in range(1, 3)]
        md = su_doc([table("Unknown", u)])
        md += "\nNota final da passagem, sem mais linhas.\n"
        rows, sec, diag = parse(md)
        self.assertEqual(ids_of(rows, "Unknown"), ["U-001", "U-002"])
        self.assertEqual(diag, [])

    def test_linha_orfa_sem_forma_de_registo_nao_e_recuperada(self):
        """Para atravessar uma interrupção a prova tem de ser forte: pipe inicial e
        id na primeira célula (ou a largura do cabeçalho). Uma linha de tabela de
        outra coisa qualquer não volta para dentro da secção."""
        u = [cells_for("Unknown", i) for i in range(1, 3)]
        md = su_doc([table("Unknown", u)])
        md += "\nNota do consultor.\n\n| ficheiro | estado |\n"
        rows, sec, diag = parse(md)
        self.assertEqual(ids_of(rows, "Unknown"), ["U-001", "U-002"])
        self.assertEqual(sec["Unknown"]["open"], 2)
        self.assertEqual(diag, [])

    def test_tabela_nova_sob_a_mesma_seccao_nao_e_continuacao(self):
        heads = COLS["Unknown"]
        md = su_doc([table("Unknown", [cells_for("Unknown", 1)])])
        md += "\n| " + " | ".join(heads) + " |\n"
        md += "|" + "|".join(["---"] * len(heads)) + "|\n"
        md += "| " + " | ".join(str(c) for c in cells_for("Unknown", 2)) + " |\n"
        rows, sec, diag = parse(md)
        self.assertEqual(ids_of(rows, "Unknown"), ["U-001", "U-002"])
        self.assertEqual([], [d for d in diag if "linha em branco" in d["message"]],
                         "duas tabelas separadas por linha em branco não são anomalia")

    def test_exemplo_dentro_de_bloco_de_codigo_nao_entra_na_seccao(self):
        u = [cells_for("Unknown", i) for i in range(1, 3)]
        md = su_doc([table("Unknown", u, blanks_after=0)])
        md += "\n```markdown\n"
        md += "| U-999 | data | exemplo do template | o dono | Critical | email | x | R-01 |\n"
        md += "```\n"
        rows, sec, _d = parse(md)
        self.assertEqual(ids_of(rows, "Unknown"), ["U-001", "U-002"])
        self.assertNotIn("U-999", [r_["id"] for r_ in rows])

    def test_bloco_de_codigo_com_til_tambem_e_bloco(self):
        u = [cells_for("Unknown", 1)]
        md = su_doc([table("Unknown", u)])
        md += "\n~~~\n"
        md += "| U-998 | data | exemplo | o dono | Critical | email | x | R-01 |\n"
        md += "~~~\n"
        rows, _sec, _d = parse(md)
        self.assertEqual(ids_of(rows, "Unknown"), ["U-001"])


# ------------------------------------------ 2b. a forma legal mas invulgar

class RegistoSemPipeInicial(unittest.TestCase):
    """GFM aceita `U-001 | data | ...` sem o pipe inicial. Nenhuma das 27 SU em disco
    o faz, mas a forma é legal: lê-se — e diz-se que se leu. O que não pode acontecer
    é o que a revisão apanhou: 2 registos passarem a 0 sem diagnóstico nenhum."""

    def bare(self, state, n):
        """As mesmas linhas, sem o `|` inicial nem o final."""
        heads = COLS[state]
        out = ["## " + state, "", "| " + " | ".join(heads) + " |",
               "|" + "|".join(["---"] * len(heads)) + "|"]
        for i in range(1, n + 1):
            out.append(" | ".join(str(c) for c in cells_for(state, i)))
        out.append("")
        return "\n".join(out) + "\n"

    def test_os_registos_sao_lidos_e_nao_perdidos(self):
        for state in ("Confirmed", "Unknown", "Risky"):
            with self.subTest(state=state):
                rows, sec, _d = parse(su_doc([self.bare(state, 2)]))
                self.assertEqual(len(ids_of(rows, state)), 2)
                self.assertEqual(sec[state]["open"], 2)

    def test_o_conteudo_e_o_mesmo_da_forma_com_pipe(self):
        cells = [cells_for("Unknown", i) for i in range(1, 4)]
        com = su_doc([table("Unknown", cells)])
        sem = su_doc([self.bare("Unknown", 3)])
        a_rows, _sa, _da = parse(com)
        b_rows, _sb, _db = parse(sem)
        self.assertEqual(ids_of(a_rows, "Unknown"), ids_of(b_rows, "Unknown"))
        self.assertEqual(claims_of(a_rows, "Unknown"), claims_of(b_rows, "Unknown"))
        self.assertEqual([r_["criticidade"] for r_ in a_rows],
                         [r_["criticidade"] for r_ in b_rows])

    def test_a_forma_avisa_com_seccao_e_linhas(self):
        _rows, _sec, diag = parse(su_doc([self.bare("Unknown", 2)]))
        semp = [d for d in diag if "sem `|` inicial" in d["message"]]
        self.assertEqual(len(semp), 1, "um aviso agregado por secção")
        self.assertEqual(semp[0]["level"], "warn")
        self.assertIn("Unknown", semp[0]["message"])

    def test_a_forma_com_pipe_nao_avisa(self):
        cells = [cells_for("Unknown", i) for i in range(1, 4)]
        _rows, _sec, diag = parse(su_doc([table("Unknown", cells)]))
        self.assertEqual(diag, [])

    def test_uma_pergunta_grave_sem_pipe_inicial_continua_grave(self):
        heads = COLS["Unknown"]
        md = su_doc([table("Unknown", [cells_for("Unknown", 1)])])
        md += " | ".join(str(c) for c in cells_for("Unknown", 2, crit="Critical")) + "\n"
        rows, _sec, _d = parse(md)
        graves = [r_["id"] for r_ in rows if r_["criticidade"] == "Critical"]
        self.assertEqual(graves, ["U-002"])

    def test_prosa_com_pipe_continua_a_nao_ser_registo(self):
        md = su_doc([self.bare("Unknown", 2)])
        md += "Nota: o dono decide entre A | B na proxima passagem.\n"
        rows, sec, _d = parse(md)
        self.assertEqual(len(ids_of(rows, "Unknown")), 2)
        self.assertEqual(sec["Unknown"]["open"], 2)

    def test_registo_sem_pipe_depois_de_uma_interrupcao(self):
        md = su_doc([table("Unknown", [cells_for("Unknown", 1)])])
        md += "\n" + " | ".join(str(c) for c in cells_for("Unknown", 2)) + "\n"
        rows, sec, diag = parse(md)
        self.assertEqual(ids_of(rows, "Unknown"), ["U-001", "U-002"])
        self.assertTrue([d for d in diag if "sem `|` inicial" in d["message"]])
        self.assertTrue([d for d in diag if "linha em branco" in d["message"]])


# ------------------------------------------------- 3. consequência no modelo

def write(path, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    with io.open(path, "w", encoding="utf-8") as fh:
        fh.write(body)


class ConsequenciaNoModelo(unittest.TestCase):
    """O portão de Discovery não pode abrir por desaparecimento de linhas."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="aisa-r1-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def mk(self, slug, md):
        eng = Path(self.tmp) / slug
        write(eng / "_state.json", json.dumps({
            "engagement": slug, "pack": "pp", "phase": "discovery", "round": "R-01",
            "aisa_version": "0.1.0", "created": "2026-09-01T00:00:00Z"}))
        write(eng / "context.json", json.dumps(
            {"literal_request": "x", "requester": {"name": "n", "role": "r"}}))
        write(eng / "shared-understanding.md", md)
        write(eng / "decisions.md", "# Decisions\n")
        for lens in ("business", "operations", "user", "data", "governance", "financial"):
            write(eng / "lens-outputs" / ("R-01-{}.md".format(lens)),
                  "# {}\n\nU-001\n".format(lens))
        return eng

    def _docs(self):
        """12 Confirmed + 6 Unknown; a grave (U-006) e o conflito grave ficam DEPOIS
        da interrupção — exactamente o caso que abria o portão por perda de linhas."""
        conf = [cells_for("Confirmed", i) for i in range(1, 13)]
        unk = [cells_for("Unknown", i) for i in range(1, 6)]
        unk.append(cells_for("Unknown", 6, crit="Critical"))
        con = [cells_for("Conflicted", 1), cells_for("Conflicted", 2, crit="Critical")]
        limpo = su_doc([table("Confirmed", conf), table("Unknown", unk),
                        table("Conflicted", con)])
        sujo = su_doc([table("Confirmed", conf), table("Unknown", unk, blanks_after=4),
                       table("Conflicted", con, blanks_after=0)])
        return limpo, sujo

    def test_pergunta_grave_depois_da_interrupcao_continua_visivel(self):
        limpo, sujo = self._docs()
        m_a = D.build_model(self.mk("limpo", limpo), TODAY)
        m_b = D.build_model(self.mk("sujo", sujo), TODAY)
        ids_a = sorted(r["id"] for r in m_a["su"]["rows"])
        ids_b = sorted(r["id"] for r in m_b["su"]["rows"])
        self.assertEqual(ids_a, ids_b)
        self.assertIn("U-006", ids_b)
        self.assertIn("X-002", ids_b)

    def test_o_portao_nao_fica_verde_por_perda_de_linhas(self):
        limpo, sujo = self._docs()
        m_a = D.build_model(self.mk("limpo", limpo), TODAY)
        m_b = D.build_model(self.mk("sujo", sujo), TODAY)
        for m, nome in ((m_a, "limpo"), (m_b, "sujo")):
            red = ((m["status"].get("gates")) or {}).get("red") or []
            self.assertIn("Unknown Critical = 0", red, nome)
            self.assertIn("Conflicted Critical = 0", red, nome)
        self.assertEqual((m_a["status"]["gates"] or {}).get("red"), (m_b["status"]["gates"] or {}).get("red"))

    def test_agenda_e_saude_iguais_ao_controlo(self):
        limpo, sujo = self._docs()
        m_a = D.build_model(self.mk("limpo", limpo), TODAY)
        m_b = D.build_model(self.mk("sujo", sujo), TODAY)
        self.assertEqual(m_a["health"]["total"], m_b["health"]["total"])
        self.assertEqual([i["id"] for i in m_a["agenda"]["reuniao"]],
                         [i["id"] for i in m_b["agenda"]["reuniao"]])
        self.assertEqual([c["id"] for c in m_a["critical"]],
                         [c["id"] for c in m_b["critical"]])

    def test_a_forma_anomala_avisa_e_a_limpa_nao(self):
        limpo, sujo = self._docs()
        m_a = D.build_model(self.mk("limpo", limpo), TODAY)
        m_b = D.build_model(self.mk("sujo", sujo), TODAY)
        branco_a = [d for d in m_a["diagnostics"] if "linha em branco" in d["message"]]
        branco_b = [d for d in m_b["diagnostics"] if "linha em branco" in d["message"]]
        self.assertEqual(branco_a, [])
        self.assertEqual(len(branco_b), 2, "uma por secção anómala")

    def test_a_su_de_entrada_nao_e_reescrita(self):
        _limpo, sujo = self._docs()
        eng = self.mk("sujo", sujo)
        antes = (eng / "shared-understanding.md").read_bytes()
        D.build_model(eng, TODAY)
        self.assertEqual(antes, (eng / "shared-understanding.md").read_bytes())


if __name__ == "__main__":
    unittest.main(verbosity=2)
