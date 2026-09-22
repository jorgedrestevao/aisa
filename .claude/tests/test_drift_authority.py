# -*- coding: utf-8 -*-
"""W5 — o espelho comparado com a autoridade REAL (P7.5).

Até aqui `projection.py` chamava `drift(nodes, {})`. Não era só não detectar desvio: com o
mapa vazio, **todos** os nós espelhados saíam como `MIRROR_SOURCE_MISSING` — 225 nos dois
pilotos — e a linha seguinte filtrava-os fora. Um falso positivo sobre a população inteira,
calculado e deitado ao lixo.

Decisões do operador (2026-09-22), e é isto que cada classe afirma:
  - comparam-se os campos que MOVEM O GATE: `state`, `criticidade`, `resolved`;
  - desvio num deles **bloqueia**;
  - `MIRROR_SOURCE_MISSING` **bloqueia** — o grafo afirma o que a autoridade já não diz;
  - `text` diverge, diz-se, e não bloqueia.

Os mutantes foram escritos antes destes testes, de propósito: em W2, W3 e W4 o que
sobreviveu sobreviveu sempre por fraqueza do teste, nunca do código."""
import json
import runpy
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "library" / "kernel" / "tools"
G = runpy.run_path(str(TOOLS / "graph.py"))
P = runpy.run_path(str(TOOLS / "projection.py"))


def no(nid, **props):
    base = {"state": "Unknown", "criticidade": "Critical", "resolved": False, "text": "t"}
    base.update(props)
    return {"id": nid, "type": "su-row", "props": base,
            "provenance": {"mirror_of": "SU:" + nid}}


def auth(nid, **campos):
    base = {"state": "Unknown", "criticidade": "Critical", "resolved": False, "text": "t"}
    base.update(campos)
    return {"SU:" + nid: base}


def codigos(ds):
    return sorted(d["code"] for d in ds)


class W5a_OsCamposQueMovemOGate(unittest.TestCase):
    """`state`, `criticidade` e `resolved` — os que `gate_open` consome por `omitted_critical`."""

    def test_a_state_that_diverges_is_blocking_drift(self):
        d = G["drift"]([no("U-001", state="Unknown")], auth("U-001", state="Confirmed"))
        self.assertEqual(codigos(d), ["MIRROR_DRIFT"])
        self.assertEqual(d[0]["field"], "state")
        self.assertEqual((d[0]["graph"], d[0]["authority"]), ("Unknown", "Confirmed"))

    def test_a_criticality_that_diverges_is_blocking_drift(self):
        """O campo que o W1 mostrou decidir o gate — e que o `drift` não olhava."""
        d = G["drift"]([no("U-001", criticidade="Med")], auth("U-001", criticidade="Critical"))
        self.assertEqual(codigos(d), ["MIRROR_DRIFT"])
        self.assertEqual(d[0]["field"], "criticidade")

    def test_a_resolved_flag_that_diverges_is_blocking_drift(self):
        d = G["drift"]([no("U-001", resolved=False)], auth("U-001", resolved=True))
        self.assertEqual(codigos(d), ["MIRROR_DRIFT"])
        self.assertEqual(d[0]["field"], "resolved")

    def test_every_gate_field_is_actually_compared(self):
        """Guarda contra encolher `GATE_FIELDS` sem ninguém dar por isso."""
        for campo, outro in (("state", "Confirmed"), ("criticidade", "Low"),
                             ("resolved", True)):
            d = G["drift"]([no("U-001", **{campo: outro})], auth("U-001"))
            self.assertEqual([x["field"] for x in d], [campo],
                             "`{}` deixou de ser comparado".format(campo))

    def test_no_divergence_means_no_finding(self):
        d = G["drift"]([no("U-001")], auth("U-001"))
        self.assertEqual(d, [], "reportou desvio onde os valores são iguais")


class W5b_OQueDivergeSemBloquear(unittest.TestCase):
    """«uma correcção de redacção não muda decisão nenhuma» — diz-se, não fecha."""

    def test_text_drift_is_reported_but_not_blocking(self):
        d = G["drift"]([no("U-001", text="antigo")], auth("U-001", text="novo"))
        self.assertEqual(codigos(d), ["MIRROR_DRIFT_INFO"])
        self.assertEqual(d[0]["field"], "text")
        self.assertIn("não move o gate", d[0]["detail"])

    def test_text_is_not_silently_added_to_the_gate_fields(self):
        self.assertNotIn("text", G["GATE_FIELDS"],
                         "`text` entrou nos campos que bloqueiam")
        self.assertIn("text", G["INFO_FIELDS"])


class W5c_FonteEmFalta(unittest.TestCase):
    """O grafo afirma o que a autoridade já não diz."""

    def test_a_node_whose_row_vanished_is_reported(self):
        d = G["drift"]([no("U-001")], {})
        self.assertEqual(codigos(d), ["MIRROR_SOURCE_MISSING"])
        self.assertEqual(d[0]["mirror_of"], "SU:U-001")
        self.assertIn("já não tem", d[0]["detail"])

    def test_a_node_without_a_mirror_is_not_a_finding(self):
        """Nem tudo no grafo espelha a SU; o que não espelha não tem autoridade a bater."""
        solto = {"id": "F-001", "type": "finding", "props": {"state": "x"}, "provenance": {}}
        self.assertEqual(G["drift"]([solto], {}), [])


class W5d_ACompatibilidadeDaFormaAntiga(unittest.TestCase):
    """Um chamador anterior passava o valor escalar. Tem de continuar a significar o mesmo."""

    def test_a_scalar_authority_is_read_as_the_state(self):
        d = G["drift"]([no("U-001", state="Unknown")], {"SU:U-001": "Confirmed"})
        self.assertEqual(codigos(d), ["MIRROR_DRIFT"])
        self.assertEqual(d[0]["field"], "state")

    def test_a_matching_scalar_authority_reports_nothing(self):
        self.assertEqual(G["drift"]([no("U-001", state="Unknown")], {"SU:U-001": "Unknown"}), [])


class W5e_AProjeccaoEntregaAAutoridade(unittest.TestCase):
    """O defeito central do W5: a projecção passava `{}`."""

    LINHAS = [{"id": "U-001", "state": "Unknown", "criticidade": "Critical",
               "resolved": False, "claim": "pergunta"},
              {"id": "C-001", "state": "Confirmed", "criticidade": "", "resolved": False,
               "claim": "facto"}]

    def test_the_authority_carries_every_mirrored_field(self):
        a = P["authority_from_rows"](self.LINHAS)
        self.assertEqual(sorted(a), ["SU:C-001", "SU:U-001"])
        self.assertEqual(a["SU:U-001"],
                         {"state": "Unknown", "criticidade": "Critical",
                          "resolved": False, "text": "pergunta"})

    def test_criticality_is_in_the_authority(self):
        """Sem ela, o campo que decide o gate ficava sem guarda."""
        self.assertIn("criticidade", P["authority_from_rows"](self.LINHAS)["SU:U-001"])

    def test_a_row_without_an_id_is_skipped_not_keyed_as_empty(self):
        a = P["authority_from_rows"](self.LINHAS + [{"id": "  ", "state": "x"}])
        self.assertEqual(sorted(a), ["SU:C-001", "SU:U-001"])

    def test_the_authority_and_the_graph_agree_on_a_freshly_migrated_pilot(self):
        """Medido: zero desvio nos dois pilotos depois de migrar. Se isto ficar vermelho,
        ou alguém editou a SU sem o grafo, ou a projecção da migração mudou."""
        for slug in ("dpt-galp-jp-pilot-4", "pricing-bunkers-pilot-4"):
            eng = ROOT / "projects" / slug
            if not (eng / "shared-understanding.md").is_file():
                self.skipTest("engagement ausente neste ambiente")
            st = P["operational_state"](eng)
            bloqueantes = [d for d in (st.get("drift") or [])
                           if d["code"] in ("MIRROR_DRIFT", "MIRROR_SOURCE_MISSING")]
            self.assertEqual(bloqueantes, [], "{}: {}".format(slug, bloqueantes[:3]))

    def test_the_projection_publishes_what_it_found(self):
        eng = ROOT / "projects" / "dpt-galp-jp-pilot-4"
        if not (eng / "shared-understanding.md").is_file():
            self.skipTest("engagement ausente neste ambiente")
        st = P["operational_state"](eng)
        self.assertIn("drift", st, "a projecção calcula o desvio e não o mostra")


class W5f_ODesvioFechaOGate(unittest.TestCase):
    """A decisão do operador: desvio num campo que move o gate bloqueia."""

    SU = """> Fase actual: Discovery

## Confirmed

| id | lens | claim | evidência | verificado_em | validade | ronda |
|---|---|---|---|---|---|---|
| C-001 | data | facto | fonte: inicial | 2026-01-01 | organizacional | R-01 |

## Assumed

| id | lens | claim | base da assumption | verificado_em | validade | ronda |
|---|---|---|---|---|---|---|

## Unknown

| id | lens | pergunta | quem responde | criticidade | custo | swing | ronda |
|---|---|---|---|---|---|---|---|

## Conflicted

| id | lens | conflito | partes | criticidade | ronda |
|---|---|---|---|---|---|

## Risky

| id | lens | risco | impacto | mitigação proposta | ronda |
|---|---|---|---|---|---|
"""

    def eng_com_grafo(self, tmp, estado_no_grafo):
        eng = Path(tmp) / "eng"
        eng.mkdir(parents=True)
        (eng / "shared-understanding.md").write_text(self.SU, encoding="utf-8", newline="\n")
        (eng / "_state.json").write_text('{"phase":"discovery","round":"R-01"}\n',
                                         encoding="utf-8", newline="\n")
        nodes = [{"id": "C-001", "type": "su-row",
                  "props": {"state": estado_no_grafo, "criticidade": "", "resolved": False,
                            "text": "facto"},
                  "provenance": {"mirror_of": "SU:C-001"}}]
        body, meta = G["serialize"](nodes, [])
        (eng / "_graph").mkdir()
        (eng / "_graph" / "graph.jsonl").write_text(body, encoding="utf-8", newline="\n")
        (eng / "_graph" / "meta.json").write_text(meta, encoding="utf-8", newline="\n")
        return eng

    def test_an_agreeing_mirror_produces_no_drift_blocker(self):
        with tempfile.TemporaryDirectory() as tmp:
            st = P["operational_state"](self.eng_com_grafo(tmp, "Confirmed"))
        kinds = [b["kind"] for b in st["blockers"]]
        self.assertNotIn("MIRROR_DRIFT", kinds)

    def test_a_diverging_mirror_blocks_and_names_what_diverges(self):
        with tempfile.TemporaryDirectory() as tmp:
            st = P["operational_state"](self.eng_com_grafo(tmp, "Unknown"))
        drift_blockers = [b for b in st["blockers"] if b["kind"] == "MIRROR_DRIFT"]
        self.assertEqual(len(drift_blockers), 1, "o desvio não bloqueou")
        b = drift_blockers[0]
        self.assertIn("state", b["what"], "o bloqueio não diz que campo diverge")
        self.assertIn("C-001", b["evidence_needed"])   # o campo chama-se assim no _blocker
        self.assertFalse(st["gate"]["open"], "o gate abriu sobre duas verdades")

    def test_a_vanished_row_blocks_too(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = self.eng_com_grafo(tmp, "Confirmed")
            # a linha sai da SU; o nó fica no grafo a afirmá-la
            sem = self.SU.replace(
                "| C-001 | data | facto | fonte: inicial | 2026-01-01 | organizacional | R-01 |\n",
                "")
            (eng / "shared-understanding.md").write_text(sem, encoding="utf-8", newline="\n")
            st = P["operational_state"](eng)
        kinds = [b["kind"] for b in st["blockers"]]
        self.assertIn("MIRROR_SOURCE_MISSING", kinds,
                      "o grafo afirma uma linha que a SU já não tem, e passou")


if __name__ == "__main__":
    unittest.main(verbosity=1)
