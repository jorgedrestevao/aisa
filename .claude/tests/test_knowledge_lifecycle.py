# -*- coding: utf-8 -*-
"""L06-L10 — coerencia do conhecimento (P6).

As transicoes que NAO partem de `Unknown`. Todas contra `library/kernel/states.md`."""
import json
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "library" / "kernel" / "tools"
R = runpy.run_path(str(TOOLS / "resolve.py"))
G = runpy.run_path(str(TOOLS / "graph.py"))
O = runpy.run_path(str(TOOLS / "operation.py"))


def fresh(eng, expr):
    code = ("import runpy,json;G=runpy.run_path(r'{g}');R=runpy.run_path(r'{r}');"
            "eng=r'{e}';print(json.dumps({x}))").format(
        g=TOOLS / "graph.py", r=TOOLS / "resolve.py", e=eng, x=expr)
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=120)
    if out.returncode != 0:
        raise AssertionError(out.stderr[-500:])
    return json.loads(out.stdout)


class L06_Finding(unittest.TestCase):
    """Finding de comportamento manual, dispor/reabrir ->
    distincao, evidencia, criticidade e accao SOBREVIVEM ao reinicio."""

    F = dict(fid="F-001", behaviour="O operador reintroduz o preco a mao todas as sextas",
             evidence="_capture/process-model.md#PM-004", criticality="Critical",
             action="automatizar ou registar como excepcao aceite")

    def test_a_finding_needs_all_four_fields(self):
        for drop in ("behaviour", "evidence", "criticality", "action"):
            kw = dict(self.F); kw[drop] = ""
            with self.assertRaises(R["ResolveError"], msg=drop) as ctx:
                R["finding"](**kw)
            self.assertEqual(ctx.exception.code, "INCOMPLETE_FINDING")

    def test_the_four_fields_survive_a_restart(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = Path(tmp) / "eng"; eng.mkdir()
            n = R["finding"](**self.F)
            O["run"](eng, "op-f", G["write_set"]([n], []))
            st = fresh(eng, "G['read'](eng)")
        got = [x for x in st["nodes"] if x["id"] == "F-001"][0]["props"]
        for k in ("behaviour", "evidence", "criticality", "action"):
            self.assertEqual(got[k], self.F[k if k != "behaviour" else "behaviour"],
                             "`{}` nao sobreviveu".format(k))

    def test_disposing_keeps_the_history(self):
        n = R["finding"](**self.F)
        d = R["dispose_finding"](n, "disposed", "aceite como excepcao pelo dono")
        self.assertTrue(d["props"]["disposed"])
        self.assertEqual(len(d["props"]["history"]), 1)

    def test_reopening_appends_rather_than_replaces(self):
        n = R["dispose_finding"](R["finding"](**self.F), "disposed", "b1")
        r = R["dispose_finding"](n, "reopened", "b2")
        self.assertFalse(r["props"]["disposed"])
        self.assertEqual([h["disposition"] for h in r["props"]["history"]],
                         ["disposed", "reopened"], "a historia foi substituida")

    def test_disposing_without_a_basis_is_refused(self):
        with self.assertRaises(R["ResolveError"]) as ctx:
            R["dispose_finding"](R["finding"](**self.F), "disposed", "")
        self.assertEqual(ctx.exception.code, "NO_BASIS")


class L07_Contradicao(unittest.TestCase):
    """Fontes opostas -> dois lados e historia preservados, SEM escolher por recencia."""

    ROW = {"id": "X-001", "state": "Conflicted"}
    SIDES = ["fonte: contrato SAP diz 18h", "role: Operacoes diz 20h"]

    def test_an_owner_decision_gives_n_confirmed(self):
        out = R["resolve_conflict"](self.ROW, self.SIDES, by_owner=True)
        self.assertEqual(out["state"], "Confirmed")
        self.assertEqual(out["successors"], 2)

    def test_without_the_owner_it_is_assumed_not_confirmed(self):
        out = R["resolve_conflict"](self.ROW, self.SIDES, by_owner=False)
        self.assertEqual(out["state"], "Assumed",
                         "resolveu um conflito para Confirmed sem o dono")

    def test_both_sides_are_preserved_either_way(self):
        for by_owner in (True, False):
            out = R["resolve_conflict"](self.ROW, self.SIDES, by_owner=by_owner)
            self.assertEqual(out["sides_preserved"], self.SIDES,
                             "um lado desapareceu (by_owner={})".format(by_owner))

    def test_recency_is_never_the_criterion(self):
        out = R["resolve_conflict"](self.ROW, self.SIDES, by_owner=False)
        self.assertFalse(out["chose_by_recency"])
        # inverter a ordem nao muda o veredicto
        rev = R["resolve_conflict"](self.ROW, list(reversed(self.SIDES)), by_owner=False)
        self.assertEqual(out["state"], rev["state"])

    def test_a_conflict_needs_two_sides(self):
        with self.assertRaises(R["ResolveError"]) as ctx:
            R["resolve_conflict"](self.ROW, ["um lado so"], by_owner=True)
        self.assertEqual(ctx.exception.code, "TOO_FEW_SIDES")


class L08_NaAndRisco(unittest.TestCase):
    """Retirar por ambito ou aceitar risco ->
    base EXIGIDA registada; SEM converter em facto nem apagar historia."""

    def test_withdrawal_is_only_a_marker(self):
        out = R["withdraw"]({"id": "U-009"}, "fora dos eixos tecnicos")
        self.assertTrue(out["marker"].startswith(R["RETIRADA_MARK"]))
        self.assertFalse(out["creates_row"])
        self.assertFalse(out["becomes_fact"], "uma retirada virou facto")

    def test_withdrawal_requires_a_reason(self):
        with self.assertRaises(R["ResolveError"]) as ctx:
            R["withdraw"]({"id": "U-009"}, "   ")
        self.assertEqual(ctx.exception.code, "NO_BASIS")

    def test_the_reason_travels_in_the_marker(self):
        out = R["withdraw"]({"id": "U-009"}, "a organizacao nao saber nao e trabalho do projecto")
        self.assertIn("nao e trabalho do projecto", out["marker"])

    def test_accepting_a_risk_records_the_basis_and_stays_risky(self):
        out = R["accept_risk"]({"id": "R-003"}, "custo de mitigar excede o impacto estimado")
        self.assertFalse(out["becomes_fact"], "um risco aceite virou Confirmed")
        self.assertIn("custo de mitigar", out["basis"])

    def test_accepting_a_risk_without_a_basis_is_refused(self):
        with self.assertRaises(R["ResolveError"]) as ctx:
            R["accept_risk"]({"id": "R-003"}, "")
        self.assertEqual(ctx.exception.code, "NO_BASIS")


class L09_Validade(unittest.TestCase):
    """Expirar/revalidar/corrigir ->
    revalidacao SEM claim nova so quando inalterada; correccao usa transicao."""

    ROW = {"id": "C-014", "state": "Confirmed"}

    def test_an_unchanged_fact_is_a_sanctioned_edit_with_no_new_row(self):
        out = R["revalidate"](self.ROW, still_holds=True, today="2026-09-22")
        self.assertEqual(out["mode"], "sanctioned_edit")
        self.assertFalse(out["creates_row"], "revalidar criou linha nova")
        self.assertEqual(out["verificado_em"], "2026-09-22")

    def test_a_changed_fact_falls_back_to_the_normal_transition(self):
        out = R["revalidate"](self.ROW, still_holds=False)
        self.assertEqual(out["mode"], "transition")
        self.assertTrue(out["creates_row"])
        self.assertIn("was C-014", out["reason"])

    def test_a_changed_fact_is_never_renewed(self):
        out = R["revalidate"](self.ROW, still_holds=False)
        self.assertNotIn("verificado_em", out,
                         "renovou `verificado_em` de um facto que mudou")

    def test_the_two_modes_are_distinguishable(self):
        a = R["revalidate"](self.ROW, still_holds=True)
        b = R["revalidate"](self.ROW, still_holds=False)
        self.assertNotEqual(a["mode"], b["mode"])
        self.assertNotEqual(a["creates_row"], b["creates_row"])


class L10_Dependencias(unittest.TestCase):
    """Alterar premissa de decisao/blueprint e outra nao relacionada ->
    revalidacao DIRECCIONADA; decisao NAO reescrita por answer."""

    NODES = [{"id": "C-001", "type": "claim", "props": {}, "provenance": {}},
             {"id": "C-002", "type": "claim", "props": {}, "provenance": {}},
             {"id": "B-001", "type": "blueprint", "props": {}, "provenance": {}},
             {"id": "Z-999", "type": "claim", "props": {}, "provenance": {}}]
    EDGES = [{"src": "B-001", "rel": "depends_on", "dst": "C-001", "props": {}, "provenance": {}},
             {"src": "C-002", "rel": "depends_on", "dst": "B-001", "props": {}, "provenance": {}}]

    def test_only_the_dependent_chain_is_revalidated(self):
        got = R["dependents_of"](self.NODES, self.EDGES, ["C-001"])
        self.assertEqual(got, ["B-001", "C-002"])

    def test_an_unrelated_change_touches_nothing(self):
        self.assertEqual(R["dependents_of"](self.NODES, self.EDGES, ["Z-999"]), [])

    def test_revalidating_everything_would_be_the_same_as_nothing(self):
        """A afirmacao do caso: direccionada quer dizer que sobra alguem de fora."""
        got = set(R["dependents_of"](self.NODES, self.EDGES, ["C-001"]))
        allids = {n["id"] for n in self.NODES}
        self.assertTrue(allids - got - {"C-001"}, "revalidou tudo — nao e direccionada")

    def test_an_answer_never_rewrites_a_decision(self):
        out = R["decision_rewritten_by"](["U-001", "D-002"], ["D-001", "D-002"])
        self.assertTrue(out["would_rewrite"])
        self.assertEqual(out["decisions"], ["D-002"])
        self.assertIn("`/decide`", out["reason"])

    def test_an_answer_that_touches_no_decision_is_clean(self):
        out = R["decision_rewritten_by"](["U-001", "C-003"], ["D-001"])
        self.assertFalse(out["would_rewrite"])


SU_CICLO = """> Fase actual: Discovery

## Confirmed

| id | lens | claim | evidência | verificado_em | validade | ronda |
|---|---|---|---|---|---|---|
| C-001 | data | Os dados vivem numa base partilhada | fonte: inicial | 2024-01-01 | organizacional | R-01 |

## Assumed

| id | lens | claim | base da assumption | verificado_em | validade | ronda |
|---|---|---|---|---|---|---|

## Unknown

| id | lens | pergunta | quem responde | criticidade | custo | swing | ronda |
|---|---|---|---|---|---|---|---|
| U-001 | data | Fora de ambito? | role: dono dos dados | Low | reuniao | so muda detalhe | R-01 |

## Conflicted

| id | lens | conflito | partes | criticidade | ronda |
|---|---|---|---|---|---|
| X-001 | governance | Aprovacao: um passo ou dois? | operations-lead | Critical | R-01 |

## Risky

| id | lens | risco | impacto | mitigação proposta | ronda |
|---|---|---|---|---|---|
| R-001 | operations | Dependencia de pessoa-chave | alto | formar substituto | R-01 |
"""


def eng_ciclo(tmp, nome="eng"):
    eng = Path(tmp) / nome
    eng.mkdir(parents=True, exist_ok=True)
    (eng / "shared-understanding.md").write_text(SU_CICLO, encoding="utf-8", newline="\n")
    (eng / "_state.json").write_text('{"phase":"discovery","round":"R-01"}\n',
                                     encoding="utf-8", newline="\n")
    return eng


def linha_de(eng, rid):
    md = (eng / "shared-understanding.md").read_text(encoding="utf-8")
    return next(l for l in md.splitlines() if l.startswith("| " + rid + " "))


class L13_OCicloDeVidaPassaPeloCoordenador(unittest.TestCase):
    """W4 — as quatro operacoes ganham a metade que lhes faltava.

    Devolviam um dict de parecer e mais nada: decidiam o que devia acontecer e nunca
    produziam um `write_set`, logo nunca chegavam ao coordenador. As DECISOES nao mudam —
    os `plan_*` chamam as mesmas funcoes de parecer. O que passa a existir e quem escreve,
    e escreve-se por uma operacao, com recibo."""

    def test_revalidation_renews_the_date_on_the_row_itself(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_ciclo(tmp)
            out = R["apply_revalidate"](eng, row_id="C-001", still_holds=True,
                                        note="confirmado hoje", by="role: dono dos dados",
                                        today="2026-09-22")
            linha = linha_de(eng, "C-001")
            md = (eng / "shared-understanding.md").read_text(encoding="utf-8")
        self.assertIn("2026-09-22", linha, "a data nao foi renovada na propria linha")
        self.assertNotIn("2024-01-01", linha, "a data velha ficou")
        self.assertFalse(out["creates_row"], "revalidar nao cria linha")
        self.assertNotIn("| C-002 ", md, "revalidar criou uma linha nova")
        self.assertNotIn("resolved", md,
                         "revalidar nao resolve nada: nao ha sucessor para onde apontar")

    def test_revalidation_leaves_a_receipt_over_both_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_ciclo(tmp)
            out = R["apply_revalidate"](eng, row_id="C-001", still_holds=True,
                                        note="n", by="role: dono dos dados")
            recibo = O["receipt_path"](eng, out["operation_id"])
            self.assertTrue(recibo.is_file(), "sem recibo, nao houve operacao")
            dados = json.loads(recibo.read_text(encoding="utf-8"))
        self.assertEqual(set(dados["published"]), {"shared-understanding.md", "answers.md"})

    def test_revalidating_a_changed_fact_is_refused(self):
        """«Never renew a changed fact» — e nao se renova, recusa-se e diz-se o que e."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_ciclo(tmp)
            with self.assertRaises(R["ResolveError"]) as ctx:
                R["plan_revalidate"](eng, row_id="C-001", still_holds=False,
                                     note="afinal e outra base")
        self.assertEqual(ctx.exception.code, "FACT_CHANGED")
        self.assertIn("transicao", str(ctx.exception))

    def test_withdrawal_is_a_marker_and_nothing_else(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_ciclo(tmp)
            antes = (eng / "shared-understanding.md").read_text(encoding="utf-8")
            out = R["apply_withdraw"](eng, row_id="U-001", reason="fora do ambito acordado")
            depois = (eng / "shared-understanding.md").read_text(encoding="utf-8")
            linha = linha_de(eng, "U-001")
        self.assertIn("retirada P-21", linha)
        self.assertIn("fora do ambito acordado", linha)
        # o marcador ACRESCENTA; a celula nao e substituida por ele. Sem esta asserção um
        # `append_cell` que apagasse o que la estava passava despercebido.
        self.assertIn("R-01", linha, "a ronda desapareceu: o marcador substituiu a celula")
        self.assertFalse(out["becomes_fact"], "retirar nao vira facto")
        self.assertEqual(len(antes.splitlines()), len(depois.splitlines()),
                         "retirar acrescentou uma linha")
        self.assertIn("Fora de ambito?", depois, "a pergunta original foi apagada")

    def test_withdrawal_without_a_reason_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_ciclo(tmp)
            with self.assertRaises(R["ResolveError"]) as ctx:
                R["plan_withdraw"](eng, row_id="U-001", reason="   ")
        self.assertEqual(ctx.exception.code, "NO_BASIS")

    def test_accepting_a_risk_records_the_basis_and_keeps_it_risky(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_ciclo(tmp)
            out = R["apply_accept_risk"](eng, row_id="R-001",
                                         basis="o dono aceita; substituto entra no Q1")
            linha = linha_de(eng, "R-001")
            md = (eng / "shared-understanding.md").read_text(encoding="utf-8")
        self.assertIn("risco aceite", linha)
        self.assertIn("substituto entra no Q1", linha)
        self.assertIn("formar substituto", linha,
                      "a mitigacao proposta desapareceu: a base substituiu a celula")
        self.assertFalse(out["becomes_fact"], "aceitar um risco nao o transforma em facto")
        self.assertNotIn("| C-002 ", md, "aceitar criou uma linha Confirmed")

    def test_accepting_a_risk_without_a_basis_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_ciclo(tmp)
            with self.assertRaises(R["ResolveError"]) as ctx:
                R["plan_accept_risk"](eng, row_id="R-001", basis="")
        self.assertEqual(ctx.exception.code, "NO_BASIS")

    def test_an_owner_decision_writes_one_row_per_side(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_ciclo(tmp)
            out = R["apply_resolve_conflict"](
                eng, row_id="X-001", by_owner=True, by={"role": "dono do processo"},
                sides=["Acima de 10k: dois passos", "Abaixo de 10k: um passo"],
                today="2026-09-22")
            md = (eng / "shared-understanding.md").read_text(encoding="utf-8")
            original = linha_de(eng, "X-001")
        self.assertEqual(out["state"], "Confirmed")
        self.assertEqual(len(out["new_ids"]), 2, "os dois lados tinham de sobreviver")
        for nid, lado in zip(out["new_ids"], ["Acima de 10k", "Abaixo de 10k"]):
            linha = next(l for l in md.splitlines() if l.startswith("| " + nid + " "))
            self.assertIn(lado, linha)
            self.assertIn("was X-001", linha)
        for nid in out["new_ids"]:
            self.assertIn(nid, original, "a original nao aponta para os sucessores")

    def test_without_an_owner_it_is_assumed_and_never_confirmed(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_ciclo(tmp)
            out = R["apply_resolve_conflict"](
                eng, row_id="X-001", by_owner=False, by={"source": "C-001"},
                sides=["lado A", "lado B"], today="2026-09-22")
        self.assertEqual(out["state"], "Assumed",
                         "sem resposta do dono nao ha Confirmed — states.md L07")
        self.assertEqual(len(out["new_ids"]), 1)
        self.assertFalse(out["verdict"]["chose_by_recency"])

    def test_a_conflict_with_one_side_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_ciclo(tmp)
            with self.assertRaises(R["ResolveError"]) as ctx:
                R["plan_resolve_conflict"](eng, row_id="X-001", sides=["so um"],
                                           by_owner=True)
        self.assertEqual(ctx.exception.code, "TOO_FEW_SIDES")

    def test_every_operation_publishes_atomically_with_a_receipt(self):
        casos = [
            ("apply_withdraw", dict(row_id="U-001", reason="fora de ambito")),
            ("apply_accept_risk", dict(row_id="R-001", basis="aceite")),
            ("apply_revalidate", dict(row_id="C-001", still_holds=True, note="n")),
            ("apply_resolve_conflict", dict(row_id="X-001", sides=["a", "b"],
                                            by_owner=True, by={"role": "dono"})),
        ]
        for nome, kw in casos:
            with tempfile.TemporaryDirectory() as tmp:
                eng = eng_ciclo(tmp)
                out = R[nome](eng, **kw)
                recibo = O["receipt_path"](eng, out["operation_id"])
                self.assertTrue(recibo.is_file(), nome + " nao deixou recibo")
                self.assertEqual(json.loads(recibo.read_text(encoding="utf-8"))["result"],
                                 "committed", nome)
                self.assertIsNone(O["read_pending"](eng), nome + " deixou pendencia")

    def test_a_plan_publishes_nothing(self):
        casos = [("plan_withdraw", dict(row_id="U-001", reason="x")),
                 ("plan_accept_risk", dict(row_id="R-001", basis="x")),
                 ("plan_revalidate", dict(row_id="C-001", still_holds=True))]
        for nome, kw in casos:
            with tempfile.TemporaryDirectory() as tmp:
                eng = eng_ciclo(tmp)
                antes = (eng / "shared-understanding.md").read_text(encoding="utf-8")
                R[nome](eng, **kw)
                depois = (eng / "shared-understanding.md").read_text(encoding="utf-8")
            self.assertEqual(antes, depois, nome + " escreveu no ensaio")


class L14_ACLIChegaAsOperacoes(unittest.TestCase):
    """O guard `if __name__ == "__main__"` estava a MEIO do ficheiro.

    Tudo o que vinha depois — as quatro funcoes de parecer incluidas — existia para quem
    importava o modulo e nao existia para quem o corria. `runpy.run_path` nao dispara o
    guard, entao os testes em processo viam tudo e a CLI rebentava com `NameError`. E parte
    da razao por que estas operacoes nunca foram ligadas: pela linha de comandos, nunca la
    estiveram."""

    def corre(self, eng, *args):
        return subprocess.run(
            [sys.executable, str(TOOLS / "resolve.py"), "--engagement", str(eng), *args,
             "--json"], capture_output=True, text=True)

    def test_the_guard_is_the_last_thing_in_the_file(self):
        texto = (TOOLS / "resolve.py").read_text(encoding="utf-8")
        depois = texto.split('if __name__ == "__main__":', 1)[1]
        # o CORPO do guard e indentado e pertence-lhe; o que nao pode existir e codigo ao
        # nivel do modulo depois dele — e esse que a CLI nunca chega a executar.
        sobra = [l for l in depois.splitlines()[1:]
                 if l.strip() and not l.startswith((" ", "\t")) and not l.startswith("#")]
        self.assertEqual(sobra, [], "ha definicoes depois do guard: a CLI nao lhes chega")

    def test_each_operation_is_reachable_from_a_real_process(self):
        casos = [
            (["--op", "withdraw", "--row", "U-001", "--reason", "fora de ambito"], "withdraw"),
            (["--op", "accept-risk", "--row", "R-001", "--basis", "aceite"], "accept-risk"),
            (["--op", "revalidate", "--row", "C-001", "--note", "mantem-se"], "revalidate"),
            (["--op", "resolve-conflict", "--row", "X-001", "--side", "a", "--side", "b",
              "--by-owner", "--by", "role: dono"], "resolve-conflict"),
        ]
        for args, nome in casos:
            with tempfile.TemporaryDirectory() as tmp:
                eng = eng_ciclo(tmp)
                p = self.corre(eng, *args)
                self.assertEqual(p.returncode, 0, nome + ": " + p.stderr[-300:])
                out = json.loads(p.stdout)
            self.assertEqual(out["receipt"]["result"], "committed", nome)

    def test_a_missing_argument_is_named_not_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_ciclo(tmp)
            p = self.corre(eng, "--op", "withdraw", "--row", "U-001")
        self.assertEqual(p.returncode, 1)
        self.assertEqual(json.loads(p.stderr)["code"], "MISSING_ARG")

    def test_the_default_op_is_still_answer(self):
        """Retro-compatibilidade: toda a invocacao anterior significa o mesmo."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_ciclo(tmp)
            p = self.corre(eng, "--row", "U-001", "--answer", "Sim, fica de fora.",
                           "--by", "role: dono dos dados", "--locator", "answers.md#U-001",
                           "--dry-run")
            self.assertEqual(p.returncode, 0, p.stderr[-300:])
            out = json.loads(p.stdout)
        self.assertEqual(out["state"], "Confirmed")


if __name__ == "__main__":
    unittest.main(verbosity=2)
