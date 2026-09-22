# -*- coding: utf-8 -*-
"""L01-L05 — primeira operacao completa de negocio (P4).

A sequencia que o plano exige: resolver -> persistir -> TERMINAR A SESSAO ->
sessao nova sem historico -> mesmo estado, proveniencia e proximo passo.
A "sessao nova" e um subprocesso: processo novo, zero memoria."""
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
_MIG = runpy.run_path(str(TOOLS / "migrate.py"))

SU = """> Fase actual: Discovery

## Confirmed

| id | lens | claim | evidência | verificado_em | validade | ronda |
|---|---|---|---|---|---|---|
| C-001 | data | Os dados vivem numa base partilhada | inicial | 2026-01-01 | organizacional | R-01 |

## Assumed

| id | lens | claim | base da assumption | verificado_em | validade | ronda |
|---|---|---|---|---|---|---|

## Unknown

| id | lens | pergunta | quem responde | criticidade | custo | swing | ronda |
|---|---|---|---|---|---|---|---|
| U-001 | data | Quem e o dono da base partilhada? | role: dono dos dados | Critical | documento | dimensionante: muda o modelo de dados | R-01 |
| U-002 | operations | Qual o horario de corte? | role: Operacoes | Med | reuniao | so muda detalhe | R-01 |

## Conflicted

| id | lens | conflito | partes | criticidade | ronda |
|---|---|---|---|---|---|

## Risky

| id | lens | risco | impacto | mitigação proposta | ronda |
|---|---|---|---|---|---|
"""


def _nascer_migrado(eng):
    """O engagement fica com grafo, pela via que lhe corresponde.

    `init` e para um scaffold vazio; um engagement com linhas na SU migra-se. A fixture
    tinha `init` fixo e passou a rebentar quando `init` deixou de aceitar conhecimento
    (F08) — que e exactamente a recusa que se quer.
    """
    try:
        return _MIG["init"](eng)
    except _MIG["MigrationError"] as exc:
        if exc.code != "NOT_EMPTY":
            raise
        return _MIG["apply"](eng)


def new_eng(tmp, name="eng"):
    eng = Path(tmp) / name
    eng.mkdir(parents=True, exist_ok=True)
    (eng / "shared-understanding.md").write_text(SU, encoding="utf-8", newline="\n")
    (eng / "answers.md").write_text("# Respostas\n", encoding="utf-8", newline="\n")
    (eng / "_state.json").write_text('{"phase":"discovery","round":"R-01"}\n',
                                     encoding="utf-8", newline="\n")
    # Nasce com grafo, como o `/start` o deixa desde P7.5 §W8 (passo 9c). Sem isto a
    # fixture modelava um engagement que hoje nao existe — e que, desde que `LEGACY_MODE`
    # bloqueia, nao avancaria: o bloqueio de topo seria a ausencia de grafo, e nao o que
    # cada caso aqui quer exercer.
    _nascer_migrado(eng)
    return eng


def fresh_session(eng, expr):
    """Um processo NOVO le o engagement. Sem historico, sem memoria."""
    code = ("import runpy,json;"
            "G=runpy.run_path(r'{g}');B=runpy.run_path(r'{b}');R=runpy.run_path(r'{r}');"
            "eng=r'{e}';print(json.dumps({x}))").format(
        g=TOOLS / "graph.py", b=TOOLS / "bootstrap.py", r=TOOLS / "resolve.py",
        e=eng, x=expr)
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=120)
    if out.returncode != 0:
        raise AssertionError("sessao nova falhou: " + out.stderr[-600:])
    return json.loads(out.stdout)


class L01_ResolucaoInferida(unittest.TestCase):
    """Resolver U por inferencia, reiniciar sessao ->
    U permanece resolvido, sucessor Assumed activo, historico preservado."""

    def _resolve(self, eng):
        return R["apply"](eng, row_id="U-001", answer_text="Infiro que e a equipa de dados.",
                          answered_by={"role": "dono dos dados"}, inference=True,
                          today="2026-09-22")

    def test_inference_resolves_to_assumed_never_confirmed(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = self._resolve(new_eng(tmp))
        self.assertEqual(out["state"], "Assumed")
        self.assertIn("inferencia declarada", out["verdict"]["reason"])

    def test_after_a_fresh_session_the_unknown_is_still_resolved(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            out = self._resolve(eng)
            rows = fresh_session(eng, "R['read_su'](eng)[1]")
        u = [r for r in rows if r.get("id") == "U-001"][0]
        # `parse_su` move o marcador da ultima coluna para `resolved`/`resolved_to`
        self.assertEqual(str(u.get("resolved")), "True",
                         "a resolucao nao sobreviveu a sessao nova")
        self.assertIn(out["new_id"], str(u.get("resolved_to", "")))

    def test_the_assumed_successor_is_active_in_a_fresh_session(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            out = self._resolve(eng)
            rows = fresh_session(eng, "R['read_su'](eng)[1]")
        succ = [r for r in rows if r.get("id") == out["new_id"]]
        self.assertEqual(len(succ), 1, "o sucessor nao existe na sessao nova")

    def test_history_is_preserved_the_original_row_is_not_deleted(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            self._resolve(eng)
            md = (eng / "shared-understanding.md").read_text(encoding="utf-8")
        self.assertIn("| U-001 |", md, "a linha original foi apagada")
        self.assertIn("Quem e o dono da base partilhada?", md)

    def test_provenance_survives_in_the_graph(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            out = self._resolve(eng)
            st = fresh_session(eng, "G['read'](eng)")
        node = [n for n in st["nodes"] if n["id"] == out["new_id"]][0]
        self.assertEqual(node["provenance"]["lens"], "data")
        self.assertEqual(node["provenance"]["answered_by"], "dono dos dados")
        edge = [e for e in st["edges"] if e["src"] == out["new_id"]][0]
        self.assertEqual((edge["rel"], edge["dst"]), ("was", "U-001"))


class L02_Confirmacao(unittest.TestCase):
    """Resolver U com fonte valida e autoridade adequada ->
    resposta literal, locator, was/resolved e estado correctos."""

    def _resolve(self, eng):
        return R["apply"](eng, row_id="U-001",
                          answer_text="O dono e a equipa de dados, por delegacao formal.",
                          answered_by={"role": "dono dos dados"},
                          locator="answers.md#U-001", today="2026-09-22")

    def test_state_is_confirmed(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = self._resolve(new_eng(tmp))
        self.assertEqual(out["state"], "Confirmed")
        self.assertTrue(out["verdict"]["authority"]["matched"])

    def test_the_verbatim_answer_is_kept(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            self._resolve(eng)
            ans = (eng / "answers.md").read_text(encoding="utf-8")
        self.assertIn("O dono e a equipa de dados, por delegacao formal.", ans,
                      "a resposta literal perdeu-se")
        self.assertIn("## U-001", ans)

    def test_was_and_locator_are_in_the_evidence_cell(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            out = self._resolve(eng)
            md = (eng / "shared-understanding.md").read_text(encoding="utf-8")
        line = [l for l in md.splitlines() if l.startswith("| " + out["new_id"] + " ")][0]
        self.assertIn("was U-001", line)
        self.assertIn("answers.md#U-001", line)

    def test_the_original_is_marked_resolved(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            out = self._resolve(eng)
            md = (eng / "shared-understanding.md").read_text(encoding="utf-8")
        line = [l for l in md.splitlines() if l.startswith("| U-001 ")][0]
        self.assertIn("resolved", line)
        self.assertIn(out["new_id"], line)

    def test_everything_lands_as_one_operation(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            out = self._resolve(eng)
        published = set(out["receipt"]["published"])
        self.assertEqual(published,
                         {"shared-understanding.md", "answers.md",
                          "_graph/graph.jsonl", "_graph/meta.json"},
                         "a SU, a resposta e o grafo nao foram publicados juntos")
        self.assertTrue(O["gate_open"](Path(tmp) / "eng"))


class L03_Terceiro(unittest.TestCase):
    """Responder com declaracao FORA da autoridade -> sem promocao silenciosa a Confirmed."""

    def test_a_third_party_with_a_locator_is_still_only_assumed(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = R["apply"](new_eng(tmp), row_id="U-001",
                             answer_text="Ouvi dizer que e a equipa de dados.",
                             answered_by={"role": "estagiario de outra equipa"},
                             locator="answers.md#U-001", today="2026-09-22")
        self.assertEqual(out["state"], "Assumed",
                         "um terceiro foi promovido a Confirmed")
        self.assertIn("terceiro", out["verdict"]["reason"])

    def test_the_reason_is_written_not_implied(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = R["apply"](new_eng(tmp), row_id="U-001", answer_text="x",
                             answered_by={"other": "alguem"}, locator="L",
                             today="2026-09-22")
        self.assertFalse(out["verdict"]["authority"]["matched"])
        self.assertIn("nao corresponde", out["verdict"]["authority"]["reason"])

    def test_the_declared_authority_is_read_from_the_row_itself(self):
        with tempfile.TemporaryDirectory() as tmp:
            _md, rows = R["read_su"](new_eng(tmp))
            row = R["find_row"](rows, "U-001")
            decl = R["declared_authority"](row)
        self.assertEqual(decl["role"], ["dono dos dados"])

    def test_a_matching_authority_without_a_locator_is_also_assumed(self):
        """Autoridade certa nao basta: `states.md` exige locator para Confirmed."""
        with tempfile.TemporaryDirectory() as tmp:
            out = R["apply"](new_eng(tmp), row_id="U-001", answer_text="x",
                             answered_by={"role": "dono dos dados"}, today="2026-09-22")
        self.assertEqual(out["state"], "Assumed")
        self.assertIn("sem locator", out["verdict"]["reason"])


class L04_IdempotenciaDeCapture(unittest.TestCase):
    """Reprocessar fonte igual e repetir resolucao recuperada -> sem efeitos duplicados."""

    ARGS = dict(row_id="U-001", answer_text="O dono e a equipa de dados.",
                answered_by={"role": "dono dos dados"}, locator="answers.md#U-001",
                today="2026-09-22")

    def test_repeating_the_same_resolution_is_the_same_operation(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            a = R["apply"](eng, **self.ARGS)
            b = R["apply"](eng, **self.ARGS)
        self.assertEqual(a["operation_id"], b["operation_id"])
        self.assertTrue(b["replayed"], "a repeticao nao foi reconhecida")

    def test_repeating_does_not_add_a_second_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            R["apply"](eng, **self.ARGS)
            md1 = (eng / "shared-understanding.md").read_text(encoding="utf-8")
            R["apply"](eng, **self.ARGS)
            md2 = (eng / "shared-understanding.md").read_text(encoding="utf-8")
        self.assertEqual(md1, md2, "a repeticao mudou a SU")

    def test_repeating_does_not_duplicate_the_answer(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            R["apply"](eng, **self.ARGS)
            R["apply"](eng, **self.ARGS)
            ans = (eng / "answers.md").read_text(encoding="utf-8")
        self.assertEqual(ans.count("## U-001"), 1, "a resposta entrou duas vezes")

    def test_repeating_does_not_multiply_graph_nodes(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            R["apply"](eng, **self.ARGS)
            R["apply"](eng, **self.ARGS)
            st = G["read"](eng)
        ids = [n["id"] for n in st["nodes"]]
        self.assertEqual(len(ids), len(set(ids)), "fonte repetida multiplicou nos")

    def test_a_recovered_operation_replays_to_the_same_result(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            first = R["apply"](eng, **self.ARGS)
            self.assertEqual(O["recover"](eng)["result"], "nothing_pending")
            again = R["apply"](eng, **self.ARGS)
        self.assertEqual(first["receipt"]["revision"], again["receipt"]["revision"])


class L05_FactoVersusAdequacao(unittest.TestCase):
    """Confirmar gateway sem provar adequacao ->
    facto registado; escolha estrutural MANTEM condicao aberta."""

    def test_a_connectivity_answer_leaves_the_structural_choice_open(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = R["apply"](new_eng(tmp), row_id="U-001",
                             answer_text="Existe um gateway que liga aos dois sistemas.",
                             answered_by={"role": "dono dos dados"},
                             locator="answers.md#U-001", settles="fact", today="2026-09-22")
        self.assertEqual(out["state"], "Confirmed", "o facto nao foi registado")
        self.assertTrue(out["structural"]["choice_open"],
                        "um facto de conectividade fechou uma escolha estrutural")
        self.assertIn("nao o mecanismo nem a sua adequacao", out["structural"]["note"])

    def test_the_open_choice_is_visible_in_the_graph(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            out = R["apply"](eng, row_id="U-001", answer_text="Ha gateway.",
                             answered_by={"role": "dono dos dados"},
                             locator="L", settles="fact", today="2026-09-22")
            st = G["read"](eng)
        node = [n for n in st["nodes"] if n["id"] == out["new_id"]][0]
        self.assertTrue(node["props"]["structural_choice_open"])

    def test_an_answer_that_settles_fit_may_close_the_choice(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = R["apply"](new_eng(tmp), row_id="U-001",
                             answer_text="O gateway suporta o requisito de auditoria.",
                             answered_by={"role": "dono dos dados"}, locator="L",
                             settles="fit", today="2026-09-22")
        self.assertFalse(out["structural"]["choice_open"])

    def test_a_non_structural_question_has_no_open_choice(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = R["apply"](new_eng(tmp), row_id="U-002", answer_text="As 18h.",
                             answered_by={"role": "Operacoes"}, locator="L",
                             today="2026-09-22")
        self.assertFalse(out["structural"]["structural"])
        self.assertIn("nao se aplica", out["structural"]["note"])

    def test_the_next_step_names_the_open_choice(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = R["apply"](new_eng(tmp), row_id="U-001", answer_text="Ha gateway.",
                             answered_by={"role": "dono dos dados"}, locator="L",
                             settles="fact", today="2026-09-22")
        self.assertIn("adequacao", out["summary"]["proximo passo"])
        self.assertIn("em aberto", out["summary"]["estado"])


class SequenciaEntreSessoes(unittest.TestCase):
    """O que o P4 exige de ponta a ponta, num processo NOVO sem historico."""

    def test_a_fresh_session_recovers_state_provenance_and_next_step(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            out = R["apply"](eng, row_id="U-001", answer_text="Ha gateway.",
                             answered_by={"role": "dono dos dados"}, locator="answers.md#U-001",
                             settles="fact", today="2026-09-22")
            boot = fresh_session(eng, "B['bootstrap'](eng)")
        self.assertTrue(boot["ready"], "a sessao nova nao arrancou")
        # A contagem era 2 porque a fixture nascia com um grafo VAZIO. Desde que `init`
        # recusa um engagement com conhecimento (F08), a fixture migra — e o grafo traz
        # tambem as linhas que a SU ja tinha. O que este caso guarda nao e o numero: e que
        # a resposta acrescenta os seus dois nos ao que la estava.
        self.assertGreaterEqual(boot["graph"]["nodes"], 2)
        ids = {i["id"] for i in boot["context"]["included"]}
        self.assertIn(out["new_id"], ids, "o facto novo nao esta no contexto da sessao nova")
        self.assertIn("U-001", ids, "a pergunta original desapareceu do contexto")

    def test_the_gate_is_open_after_a_clean_operation(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            R["apply"](eng, row_id="U-002", answer_text="As 18h.",
                       answered_by={"role": "Operacoes"}, locator="L", today="2026-09-22")
            boot = fresh_session(eng, "B['bootstrap'](eng)")
        self.assertTrue(boot["ready"])
        self.assertEqual([l for l in boot["limitations"] if l.get("blocking")], [])

    def test_an_operation_is_refused_while_recovery_is_pending(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            O["_atomic_write"](O["pending_path"](eng), json.dumps(
                {"intent_version": 1, "operation_id": "op-x", "after": {"a": "b"}}))
            with self.assertRaises(R["ResolveError"]) as ctx:
                R["apply"](eng, row_id="U-001", answer_text="x",
                           answered_by={"role": "dono dos dados"}, locator="L")
        self.assertEqual(ctx.exception.code, "NOT_READY")


class L11_OQueOAnswerPrecisaDaCLI(unittest.TestCase):
    """W3 — as duas lacunas que impediam o `/answer` de usar o motor sem escrever a SU a mao.

    `--claim`: a regra dura 1 do `/answer` e «Verbatim in, structured out» — `answers.md`
    guarda a resposta tal como foi dada, a linha da SU carrega o facto extraido. Sem passar
    a claim, a linha ficava com a primeira linha da resposta e a regra morria.

    `--to`: o `/answer` deixa forcar o estado. Descer e legitimo — quem responde pode querer
    afirmar menos do que as provas dao. Subir e a «promocao silenciosa» que `states.md`
    proibe e que a regra dura 3 repete."""

    RESP = "Sao cinco. O Joao acha que as vezes sao seis, mas nunca editam ao mesmo tempo."
    FACTO = "Cinco utilizadores em simultaneo; sem edicao concorrente"

    def test_the_claim_is_the_extracted_fact_not_the_first_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            p = R["plan"](eng, row_id="U-001", answer_text=self.RESP,
                          answered_by={"role": "dono dos dados"}, locator="L",
                          claim=self.FACTO)
            su = p["write_set"]["shared-understanding.md"]
            ans = p["write_set"]["answers.md"]
        self.assertIn(self.FACTO, su, "a linha da SU carrega o facto extraido")
        self.assertNotIn("O Joao acha", su, "a SU nao leva a conversa toda")
        self.assertIn("O Joao acha", ans, "`answers.md` guarda o verbatim, inteiro")

    def test_without_a_claim_the_first_line_is_the_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            p = R["plan"](eng, row_id="U-001", answer_text="Linha um\nLinha dois",
                          answered_by={"role": "dono dos dados"}, locator="L")
            su = p["write_set"]["shared-understanding.md"]
        self.assertIn("Linha um", su)
        self.assertNotIn("Linha dois", su)

    def test_forcing_a_weaker_state_is_allowed_and_recorded(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            p = R["plan"](eng, row_id="U-001", answer_text="x",
                          answered_by={"role": "dono dos dados"}, locator="L", to="assumed")
        self.assertEqual(p["state"], "Assumed")
        self.assertEqual(p["verdict"]["forced_from"], "Confirmed")
        self.assertIn("declaracao do operador", p["verdict"]["reason"])

    def test_forcing_a_stronger_state_is_refused(self):
        """O caso que a regra dura 3 existe para impedir."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            with self.assertRaises(R["ResolveError"]) as ctx:
                R["plan"](eng, row_id="U-001", answer_text="x",
                          answered_by={"role": "dono dos dados"},
                          locator="", to="confirmed")       # sem locator -> Assumed
        self.assertEqual(ctx.exception.code, "SILENT_UPGRADE")
        self.assertIn("promocao silenciosa", str(ctx.exception))

    def test_forcing_the_state_it_already_is_changes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            a = R["plan"](eng, row_id="U-001", answer_text="x",
                          answered_by={"role": "dono dos dados"}, locator="L")
            b = R["plan"](eng, row_id="U-001", answer_text="x",
                          answered_by={"role": "dono dos dados"}, locator="L", to="confirmed")
        self.assertEqual(a["verdict"], b["verdict"])
        self.assertNotIn("forced_from", b["verdict"])

    def test_an_unknown_state_is_named_not_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            with self.assertRaises(R["ResolveError"]) as ctx:
                R["plan"](eng, row_id="U-001", answer_text="x",
                          answered_by={"role": "dono dos dados"}, locator="L", to="confirmado")
        self.assertEqual(ctx.exception.code, "UNKNOWN_STATE")

    def test_the_cli_exposes_both_and_a_real_process_honours_them(self):
        """A skill invoca a CLI, nao a funcao. O que a CLI nao expoe, nao existe para ela."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            p = subprocess.run(
                [sys.executable, str(TOOLS / "resolve.py"),
                 "--engagement", str(eng), "--row", "U-001",
                 "--answer", self.RESP, "--claim", self.FACTO,
                 "--by", "role: dono dos dados", "--locator", "L",
                 "--to", "assumed", "--dry-run", "--json"],
                capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            out = json.loads(p.stdout)
        self.assertEqual(out["state"], "Assumed")
        self.assertEqual(out["verdict"]["forced_from"], "Confirmed")

    def test_the_cli_exits_nonzero_on_a_refused_upgrade(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            p = subprocess.run(
                [sys.executable, str(TOOLS / "resolve.py"),
                 "--engagement", str(eng), "--row", "U-001", "--answer", "x",
                 "--by", "role: dono dos dados", "--to", "confirmed", "--dry-run", "--json"],
                capture_output=True, text=True)
        self.assertEqual(p.returncode, 1, "a recusa tem de sair diferente de zero")
        self.assertIn("SILENT_UPGRADE", p.stderr)


class L12_OAnswerPassaPeloMotor(unittest.TestCase):
    """O criterio de fecho do W3: «uma execucao real de `/answer` deixa recibo».

    Corrido pela CLI, em processo real — que e como a skill a invoca. Nao se afirma aqui
    que a skill a chamou; afirma-se que o caminho que ela passou a mandar chamar produz
    uma transicao completa e auditavel, e que produzi-la a mao produziria menos."""

    def corre_cli(self, eng, *extra):
        return subprocess.run(
            [sys.executable, str(TOOLS / "resolve.py"),
             "--engagement", str(eng), "--row", "U-001",
             "--answer", "Cinco pessoas, sem edicao concorrente.",
             "--claim", "Cinco utilizadores em simultaneo",
             "--by", "role: dono dos dados", "--locator", "answers.md#U-001",
             "--json", *extra],
            capture_output=True, text=True)

    def test_a_real_run_leaves_a_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            p = self.corre_cli(eng)
            self.assertEqual(p.returncode, 0, p.stderr)
            out = json.loads(p.stdout)
            recibo = O["receipt_path"](eng, out["operation_id"])
            self.assertTrue(recibo.is_file(), "sem recibo, nao houve operacao")
            dados = json.loads(recibo.read_text(encoding="utf-8"))
        self.assertEqual(dados["result"], "committed")
        self.assertIn("shared-understanding.md", dados["published"])
        self.assertIn("answers.md", dados["published"],
                      "a SU e o `answers.md` saem na MESMA operacao, nao em duas")

    def test_the_transition_is_complete_on_disk(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            out = json.loads(self.corre_cli(eng).stdout)
            su = (eng / "shared-understanding.md").read_text(encoding="utf-8")
            ans = (eng / "answers.md").read_text(encoding="utf-8")
            nodes = {n["id"] for n in G["read"](eng)["nodes"]}
        # o motor escreve a seta em ASCII; `RESOLVED_RE` aceita as duas, o ficheiro usa uma
        self.assertIn("resolved -> " + out["new_id"], su, "a original fica marcada")
        self.assertIn("Cinco utilizadores em simultaneo", su, "a linha nova carrega o facto")
        self.assertIn("answers.md#U-001", su, "o locator que `Confirmed` exige")
        self.assertEqual(su.count("answers.md#U-001"), 1,
                         "a ancora e o locator sao a mesma coisa; escrever duas vezes e ruido")
        self.assertIn("Cinco pessoas, sem edicao concorrente.", ans, "o verbatim fica inteiro")
        self.assertIn(out["new_id"], nodes, "o espelho no grafo sai da mesma operacao")

    def test_a_dry_run_publishes_nothing(self):
        """Nada de novo — e «nada de novo» nao e «nenhum».

        O engagement nasce com grafo desde P7.5 §W8, e nascer e uma operacao: ha um recibo
        (`graph-init`) antes de o ensaio comecar. Comparar com lista vazia mediria o
        nascimento em vez do ensaio. Compara-se com o que la estava, que e mais apertado:
        apanha um recibo a mais **e** um recibo a menos."""
        def recibos_de(eng):
            d = eng / "_ops" / "receipts"
            return sorted(p.name for p in d.glob("*.json")) if d.is_dir() else []

        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            antes = (eng / "shared-understanding.md").read_text(encoding="utf-8")
            recibos_antes = recibos_de(eng)
            p = self.corre_cli(eng, "--dry-run")
            depois = (eng / "shared-understanding.md").read_text(encoding="utf-8")
            recibos_depois = recibos_de(eng)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(antes, depois, "o ensaio escreveu na SU")
        self.assertEqual(recibos_depois, recibos_antes, "o ensaio deixou recibo")
        self.assertEqual(len(recibos_antes), 1,
                         "a fixture deixou de nascer com grafo por UMA operacao, e o caso "
                         "passou a medir outra coisa: " + str(recibos_antes))

    def test_repeating_the_same_answer_does_not_transition_twice(self):
        """Idempotencia pelo coordenador: o mesmo pedido nao cria uma segunda linha."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            a = json.loads(self.corre_cli(eng).stdout)
            su1 = (eng / "shared-understanding.md").read_text(encoding="utf-8")
            segunda = self.corre_cli(eng)
            su2 = (eng / "shared-understanding.md").read_text(encoding="utf-8")
        self.assertEqual(su1, su2, "a repeticao escreveu outra vez")
        self.assertEqual(su1.count(a["new_id"]), su2.count(a["new_id"]))

    def test_the_skill_tells_the_agent_to_use_the_engine(self):
        """Guarda de fio, nao prova de runtime.

        `ACCEPTANCE.md` §1 diz que estrutura de prompt nao prova comportamento — e nao
        prova. O que este caso guarda e o oposto: que o fio nao seja desfeito sem se dar por
        isso. A prova de comportamento sao os tres casos acima."""
        skill = (ROOT / ".claude" / "skills" / "aisa-answer" / "SKILL.md").read_text(
            encoding="utf-8")
        self.assertIn("library/kernel/tools/resolve.py", skill,
                      "a skill deixou de mandar chamar o motor")
        self.assertIn("Never write these files directly", skill,
                      "sem esta frase, o caminho a mao volta por omissao")
        self.assertIn("_ops/receipts", skill, "o recibo e o criterio de fecho; tem de constar")


if __name__ == "__main__":
    unittest.main(verbosity=2)
