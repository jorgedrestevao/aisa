# -*- coding: utf-8 -*-
"""O formulario e o juiz tem de concordar.

Primeira corrida real de E01, checkpoint `cp1-discovery`: **NO-GO, 5 criticos**, todos
`LOST_CRITICAL` sobre A-001..A-005. A sessao nao perdeu nada. Seguiu o schema do protocolo
a letra, e o schema nao tinha onde por uma `Assumed`:

    PROTOCOLO.md §2.3   facts          -> Confirmed
                        open_questions -> Unknown
    compare.py          exige recuperar linhas materiais em
                        Unknown · Conflicted · Risky · Confirmed · Assumed

O juiz pedia cinco estados; o formulario oferecia dois lugares. Pior: `compare.py` nao
olhava a que campo vinha cada linha, so ao id e ao estado — uma sessao que DESOBEDECESSE e
metesse as Assumed em `facts` passava. O protocolo premiava quem nao o seguia.

A correccao proposta na altura foi copiar A-001..A-005 do `truth.json` para o report. Isso
e preencher o candidato a partir da referencia (`ACCEPTANCE.md` §5) e daria GO sem medir
nada. O defeito estava no harness; e no harness que se corrige, e a sessao repete-se.

Este ficheiro fixa as duas metades: o juiz le todos os campos que o formulario oferece, e o
formulario oferece um campo para cada estado que o juiz exige."""
import json
import re
import runpy
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P8 = ROOT / "docs" / "evolution" / "p8"
C = runpy.run_path(str(P8 / "compare.py"))
T = runpy.run_path(str(ROOT / ".claude" / "tests" / "test_p8_comparator.py"))
verdade, relatorio, codigos = T["verdade"], T["relatorio"], T["codigos"]


def linha(rid, estado, material=True):
    return {"id": rid, "state": estado,
            "criticidade": "critical" if material else "noncritical",
            "swing_class": "dimensionante" if material else "cosmetico",
            "resolved": False, "resolved_to": [], "support": "x"}


def verdade_com(**estados):
    """Uma verdade com linhas materiais nos estados pedidos, alem do caso base."""
    v = verdade()
    for estado, ids in estados.items():
        v["by_state"].setdefault(estado, [])
        for rid in ids:
            v["by_state"][estado].append(linha(rid, estado))
            v["all_ids"].append(rid)
    return v


ASSUMIDAS = ["A-001", "A-002", "A-003", "A-004", "A-005"]


class S1_OTeuNoGo(unittest.TestCase):

    def test_assumptions_in_their_own_field_are_recovered(self):
        """O caso exacto da corrida 1: cinco Assumed materiais, agora com lugar."""
        v = verdade_com(Assumed=ASSUMIDAS)
        r = relatorio(assumptions=[{"id": a, "state": "Assumed"} for a in ASSUMIDAS])
        perdidas = [a for a in C["check"](v, r)["findings"] if a["code"] == "LOST_CRITICAL"]
        self.assertEqual(perdidas, [], "as Assumed vieram no campo delas e o juiz nao as viu")

    def test_the_judge_still_bites_when_they_are_really_missing(self):
        """Dar-lhes lugar nao pode desligar a perda: se nao vierem, e critico na mesma."""
        v = verdade_com(Assumed=ASSUMIDAS)
        perdidas = [a["id"] for a in C["check"](v, relatorio())["findings"]
                    if a["code"] == "LOST_CRITICAL"]
        self.assertEqual(sorted(perdidas), ASSUMIDAS)

    def test_risky_rows_have_a_place(self):
        v = verdade_com(Risky=["R-001"])
        r = relatorio(risks=[{"id": "R-001", "state": "Risky"}])
        self.assertNotIn("LOST_CRITICAL", codigos(C["check"](v, r)))

    def test_conflicted_rows_have_a_place(self):
        v = verdade_com(Conflicted=["X-001"])
        r = relatorio(risks=[{"id": "X-001", "state": "Conflicted"}])
        self.assertNotIn("LOST_CRITICAL", codigos(C["check"](v, r)))


class S2_OCampoCerto(unittest.TestCase):
    """O estado decide a gaveta. Gaveta errada e aviso — o id foi recuperado, e perder
    nao e o mesmo que arrumar mal."""

    def test_an_assumed_filed_as_an_open_question_is_a_warning(self):
        v = verdade_com(Assumed=["A-001"])
        r = relatorio(open_questions=relatorio()["open_questions"] +
                      [{"id": "A-001", "state": "Assumed"}])
        achados = [a for a in C["check"](v, r)["findings"] if a.get("id") == "A-001"]
        self.assertEqual([a["code"] for a in achados], ["FIELD_MISMATCH"])
        self.assertEqual(achados[0]["severity"], C["AVISO"])

    def test_an_assumed_filed_as_a_fact_is_a_warning_not_a_silent_pass(self):
        """Antes disto, meter a Assumed em `facts` passava em silencio."""
        v = verdade_com(Assumed=["A-001"])
        r = relatorio(facts=relatorio()["facts"] + [{"id": "A-001", "state": "Assumed"}])
        self.assertIn("FIELD_MISMATCH", codigos(C["check"](v, r)))

    def test_a_blocker_can_be_in_any_state(self):
        """`blockers` e uma vista transversal, nao uma gaveta de estado."""
        v = verdade_com(Assumed=["A-001"])
        r = relatorio(assumptions=[{"id": "A-001", "state": "Assumed"}],
                      blockers=[{"id": "A-001"}])
        self.assertNotIn("FIELD_MISMATCH", codigos(C["check"](v, r)))

    def test_a_row_only_in_blockers_is_not_misfiled(self):
        """O caso anterior punha a linha em `assumptions` E em `blockers`, e a gaveta certa
        estava sempre la — contar `blockers` como gaveta nao mudava nada e o mutante
        sobrevivia. Aqui a linha so aparece como bloqueio."""
        v = verdade_com(Assumed=["A-001"])
        r = relatorio(blockers=[{"id": "A-001", "state": "Assumed"}])
        cods = codigos(C["check"](v, r))
        self.assertNotIn("FIELD_MISMATCH", cods)
        self.assertNotIn("LOST_CRITICAL", cods, "listada como bloqueio e dada por perdida")

    def test_a_wrong_state_is_reported_once_not_twice(self):
        """Estado errado ja e FALSE_CONFIRMED/STATE_DRIFT; nao se soma FIELD_MISMATCH."""
        v = verdade_com(Assumed=["A-001"])
        r = relatorio(facts=relatorio()["facts"] + [{"id": "A-001", "state": "Confirmed"}])
        cods = [a["code"] for a in C["check"](v, r)["findings"] if a.get("id") == "A-001"]
        self.assertEqual(cods, ["FALSE_CONFIRMED"])


class S3_OQueNaoPodeRegredir(unittest.TestCase):

    def test_an_invented_id_in_the_new_fields_is_critical(self):
        r = relatorio(assumptions=[{"id": "A-999", "state": "Assumed"}])
        self.assertIn("INVENTED", codigos(C["check"](verdade(), r)))

    def test_a_false_confirmed_from_the_new_fields_is_caught(self):
        v = verdade_com(Assumed=["A-001"])
        r = relatorio(assumptions=[{"id": "A-001", "state": "Confirmed"}])
        self.assertIn("FALSE_CONFIRMED", codigos(C["check"](v, r)))

    def test_an_old_report_without_the_new_fields_is_not_incomplete(self):
        """As corridas ja gravadas nao passam a REPORT_INCOMPLETE por o schema crescer."""
        self.assertNotIn("REPORT_INCOMPLETE", codigos(C["check"](verdade(), relatorio())))

    def test_a_leak_is_caught_in_the_new_fields(self):
        # `decisions=[]`: a primeira versao herdava D-001 da fixture base e o LEAK vinha
        # dai — o caso passava sem o juiz alguma vez olhar para `assumptions`.
        outro = verdade(engagement="eng-b", all_ids=["A-777"], decisions=[],
                        by_state={"Assumed": [linha("A-777", "Assumed")]})
        r = relatorio(assumptions=[{"id": "A-777", "state": "Assumed"}])
        fugas = [a.get("id") for a in C["leak"](outro, r)["findings"] if a["code"] == "LEAK"]
        self.assertEqual(fugas, ["A-777"])


class S4_OFormularioEOJuizConcordam(unittest.TestCase):
    """A metade que faltava: nao chega o juiz ler os campos — o formulario tem de os pedir."""

    def bloco(self):
        texto = (P8 / "PROTOCOLO.md").read_text(encoding="utf-8")
        m = re.search(r"### 2\.3.*?```json\s*\n(.*?)```", texto, re.S)
        self.assertIsNotNone(m, "o bloco JSON do §2.3 desapareceu do protocolo")
        corpo = "\n".join(l.lstrip("> ").rstrip() if l.startswith(">") else l
                          for l in m.group(1).splitlines())
        return json.loads(corpo)

    def test_the_template_offers_a_field_for_every_state_the_judge_demands(self):
        pedidos = set(C["CAMPO_DO_ESTADO"].values())
        oferecidos = set(self.bloco())
        self.assertEqual(pedidos - oferecidos, set(),
                         "o juiz exige campos que o formulario nao oferece")

    def test_the_judge_reads_every_row_field_the_template_offers(self):
        listas = {k for k, v in self.bloco().items()
                  if isinstance(v, list) and v and isinstance(v[0], dict) and "id" in v[0]
                  and k != "decisions"}
        self.assertEqual(listas - set(C["CAMPOS_LINHAS"]), set(),
                         "o formulario oferece um campo que o juiz ignora")

    def test_each_example_row_carries_the_state_of_its_field(self):
        """O exemplo do formulario e o que uma sessao literal copia: tem de estar certo."""
        bloco = self.bloco()
        for estado, campo in C["CAMPO_DO_ESTADO"].items():
            exemplos = [x.get("state") for x in bloco.get(campo, [])]
            self.assertTrue(exemplos, "o campo {} nao tem exemplo".format(campo))
            validos = {e for e, c in C["CAMPO_DO_ESTADO"].items() if c == campo}
            self.assertTrue(set(exemplos) <= validos,
                            "o exemplo de {} mostra um estado que la nao pertence".format(campo))


if __name__ == "__main__":
    unittest.main(verbosity=1)
