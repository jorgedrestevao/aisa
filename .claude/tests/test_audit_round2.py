# -*- coding: utf-8 -*-
"""R2-01..R2-06 — a segunda ronda da auditoria externa, por inspecção de código.

A primeira ronda foi executada; esta foi lida. Seis pontos, **seis confirmados** contra a
árvore de `9bdf399`, cada um reproduzido antes de se escrever uma linha de correcção.

O que isso diz sobre a primeira ronda de correcções: fechei os onze e não auditei quem mais
tocava no que passei a exigir. O caso que o mostra é o R2-03 — desde que o bootstrap BLOQUEIA
sobre desvio de autoridade (F05), um escritor que não actualiza o espelho deixou de produzir
uma inconsistência tolerada e passou a **inutilizar o engagement**. Medido:
`apply_resolve_conflict` leva `ready` de `True` a `False`. A correcção do F06 fechou o caso
(`/answer`) e não a classe.

Estes casos nascem vermelhos, como os da primeira ronda."""
import json
import runpy
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "library" / "kernel" / "tools"
O = runpy.run_path(str(TOOLS / "operation.py"))
B = runpy.run_path(str(TOOLS / "bootstrap.py"))
G = runpy.run_path(str(TOOLS / "graph.py"))
M = runpy.run_path(str(TOOLS / "migrate.py"))
R = runpy.run_path(str(TOOLS / "resolve.py"))
P = runpy.run_path(str(TOOLS / "projection.py"))
C = runpy.run_path(str(TOOLS / "coverage.py"))
FIX = runpy.run_path(str(ROOT / ".claude" / "tests" / "test_migration.py"))

SU_FILE = "shared-understanding.md"


def eng_migrado(tmp, su=None):
    eng = FIX["make"](tmp, su or FIX["NOVO"])
    M["apply"](eng)
    return eng


# =============================================================================
# R2-01 · P1 — conteúdo e base de revisões diferentes
# =============================================================================

class R2_01_UmaRevisaoSo(unittest.TestCase):
    """O plano lê os ficheiros no princípio e tira os digests no fim.

    Entre as duas coisas cabe uma escrita — e ela fica registada como a BASE, enquanto o
    conteúdo preparado é o de antes dela. `expected` bate certo, o coordenador publica, e a
    alteração desaparece com recibo `committed`. É o mesmo defeito do F04 um passo mais
    acima: lá a lista de precondições não cobria tudo, aqui cobre tudo mas no instante
    errado."""

    def _plano_com_escrita_pelo_meio(self, eng):
        rg = R["plan"].__globals__
        real = rg["read_su"]
        disparado = []

        def le_e_deixa_outro_escrever(e):
            md, rows = real(e)
            if not disparado:
                disparado.append(True)
                su = Path(e) / SU_FILE
                su.write_text(su.read_text(encoding="utf-8").replace(
                    "Base partilhada", "BASE ALTERADA POR OUTRO"),
                    encoding="utf-8", newline="\n")
            return md, rows

        rg["read_su"] = le_e_deixa_outro_escrever
        try:
            return R["plan"](eng, row_id="U-001", answer_text="resposta",
                             answered_by={"role": "dono dos dados"},
                             locator="answers.md#U-001")
        finally:
            rg["read_su"] = real

    def test_the_base_it_declares_is_the_one_it_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_migrado(tmp)
            plano = self._plano_com_escrita_pelo_meio(eng)
            agora = O["digest"](eng / SU_FILE)
        declarada = plano["expected"][SU_FILE]
        self.assertNotEqual(
            declarada, agora,
            "declarou como base uma revisão que não é a que leu — publicar assim apaga a "
            "alteração concorrente sem uma única recusa")

    def test_publishing_such_a_plan_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_migrado(tmp)
            plano = self._plano_com_escrita_pelo_meio(eng)
            try:
                O["run"](eng, plano["operation_id"], plano["write_set"],
                         expected=plano["expected"])
                codigo = None
            except O["OperationError"] as exc:
                codigo = exc.code
            sobrevive = "BASE ALTERADA POR OUTRO" in (eng / SU_FILE).read_text(
                encoding="utf-8")
        self.assertTrue(codigo == "BASE_CHANGED" or sobrevive,
                        "publicou por cima da alteração concorrente e chamou-lhe sucesso")


# =============================================================================
# R2-02 · P1 — a leitura validada não cobre a operação toda
# =============================================================================

class R2_02_AValidacaoCobreOQueSeLe(unittest.TestCase):
    """`consistent_read` valida pendência, snapshot e grafo — e depois o bootstrap volta a
    abrir a SU em `authority_check`, fora da janela validada. A projecção faz pior: reabre
    tudo pelo `dashboard`. Validar uma parte da leitura e concluir sobre o todo é a mesma
    falha do F02 com outro alcance."""

    def test_the_authority_read_is_inside_the_validated_window(self):
        fonte = (TOOLS / "bootstrap.py").read_text(encoding="utf-8")
        i_val = fonte.index("consistent_read")
        # a comparação autoridade/espelho tem de consumir o que a validação já leu,
        # não reabrir o ficheiro por sua conta
        i_auth = fonte.index("def authority_check")
        corpo = fonte[i_auth:i_auth + 1200]
        self.assertNotIn('su.read_text(', corpo,
                         "`authority_check` reabre a SU por fora da revisão validada")
        self.assertGreater(i_val, 0)

    def test_the_reconstruction_publishes_the_rows_it_validated(self):
        """Quem já leu a SO dentro da janela não obriga o próximo a reabri-la."""
        with tempfile.TemporaryDirectory() as tmp:
            boot = B["bootstrap"](eng_migrado(tmp))
        self.assertIn("rows", boot.get("snapshot", {}),
                      "o snapshot não carrega as linhas que a validação leu, por isso cada "
                      "consumidor reabre o ficheiro e sai da revisão")


# =============================================================================
# R2-03 · P1 — resolver um conflito deixa o grafo por trás
# =============================================================================

class R2_03_TodoOEscritorFechaOEspelho(unittest.TestCase):
    """Medido: `apply_resolve_conflict` leva `ready` de `True` a `False` com
    `AUTHORITY_DRIFT`. Desde que o desvio bloqueia, um escritor que não actualiza o espelho
    deixou de produzir uma inconsistência tolerada e passou a inutilizar o engagement.

    A correcção do F06 fechou o `/answer`. Isto é a classe: **qualquer** plano que mude
    linhas da SU publica o espelho na mesma transacção."""

    def _conflito(self, eng):
        return R["apply_resolve_conflict"](eng, row_id="X-001",
                                           sides=["contrato diz 8h", "operacoes diz 9h"],
                                           by_owner=True, by={"role": "dono do processo"})

    def test_resolving_a_conflict_keeps_the_engagement_usable(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_migrado(tmp, FIX["RESOLVIDO"])
            self.assertTrue(B["bootstrap"](eng)["ready"], "o cenário não começou limpo")
            self._conflito(eng)
            boot = B["bootstrap"](eng)
        self.assertTrue(boot["ready"],
                        "resolver um conflito inutilizou o engagement: %s"
                        % [l["code"] for l in boot["limitations"]])

    def test_it_publishes_the_graph_too(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_migrado(tmp, FIX["RESOLVIDO"])
            plano = R["plan_resolve_conflict"](eng, row_id="X-001",
                                               sides=["a", "b"], by_owner=True,
                                               by={"role": "dono"})
        self.assertTrue([k for k in plano["write_set"] if k.startswith("_graph/")],
                        "muda linhas da SU e não toca no espelho: " + str(sorted(
                            plano["write_set"])))

    def test_every_lifecycle_writer_that_moves_a_mirror_field_publishes_it(self):
        """A classe, não o caso. Um escritor novo não pode esquecer-se."""
        casos = [
            ("resolve_conflict", lambda e: R["plan_resolve_conflict"](
                e, row_id="X-001", sides=["a", "b"], by_owner=True, by={"role": "d"})),
            ("withdraw", lambda e: R["plan_withdraw"](e, row_id="U-001", reason="fora")),
            ("accept_risk", lambda e: R["plan_accept_risk"](e, row_id="U-001",
                                                            basis="aceite")),
        ]
        for nome, fazer in casos:
            with self.subTest(escritor=nome), tempfile.TemporaryDirectory() as tmp:
                eng = eng_migrado(tmp, FIX["RESOLVIDO"])
                plano = fazer(eng)
                su_nova = plano["write_set"][SU_FILE]
                _h, linhas, _s, _d = runpy.run_path(
                    str(TOOLS / "dashboard.py"))["parse_su"](su_nova)
                nova = G["authority_from_rows"](linhas)
                antiga = G["authority_from_rows"](FIX["make"] and [])  # placeholder
                st = G["read"](eng)
                # o espelho publicado (ou o que fica) tem de concordar com a SU publicada
                nos = st["nodes"]
                if [k for k in plano["write_set"] if k.startswith("_graph/")]:
                    continue                      # publica o grafo: fica coberto
                desvio = G["drift"](nos, nova)
                bloqueante = [d for d in desvio
                              if d["code"] in ("MIRROR_DRIFT", "MIRROR_SOURCE_MISSING")]
                self.assertEqual(
                    bloqueante, [],
                    "`%s` muda a autoridade e deixa o espelho a discordar dela" % nome)


# =============================================================================
# R2-04 · P1 — restore sem precondição, e a remover por fora
# =============================================================================

class R2_04_RestoreCoordenado(unittest.TestCase):
    """A reposição passou a ir pelo coordenador — mas sem `expected`, por isso escreve por
    cima do que tiver aparecido depois da verificação inicial. E as remoções continuam à
    mão, fora da barreira."""

    def _migrado_com_grafo(self, tmp):
        vazia = FIX["HEAD"].format(confirmed="", assumed="", unknown="", conflicted="")
        eng = FIX["make"](tmp, vazia)
        M["init"](eng)
        (eng / SU_FILE).write_text(FIX["NOVO"], encoding="utf-8", newline="\n")
        M["apply"](eng)
        return eng

    def test_the_restore_declares_the_base_it_verified(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._migrado_com_grafo(tmp)
            M["restore"](eng)
            recibo = next((eng / "_ops" / "receipts").glob("restore-*.json"))
            corpo = json.loads(recibo.read_text(encoding="utf-8"))
        self.assertIn("expected", corpo,
                      "a reposição publicou sem precondição: escreve por cima do que "
                      "apareceu depois da verificação")

    def test_work_that_lands_after_the_check_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._migrado_com_grafo(tmp)
            mg = M["restore"].__globals__
            real = mg["_digests"]
            disparado = []

            def verifica_e_deixa_outro_escrever(e):
                out = real(e)
                if not disparado:
                    disparado.append(True)
                    ans = Path(e) / "answers.md"
                    ans.write_text("# Respostas\n\n## trabalho que chegou depois\n",
                                   encoding="utf-8", newline="\n")
                return out

            mg["_digests"] = verifica_e_deixa_outro_escrever
            try:
                try:
                    M["restore"](eng)
                    recusou = False
                except Exception:                                   # noqa: BLE001
                    recusou = True
            finally:
                mg["_digests"] = real
            sobrevive = "chegou depois" in (eng / "answers.md").read_text(encoding="utf-8")
        self.assertTrue(recusou or sobrevive,
                        "apagou trabalho que chegou depois da verificação, sem recusar")


# =============================================================================
# R2-05 · P2 — o parâmetro existe e ninguém o passa
# =============================================================================

class R2_05_ACoberturaUsaAQuePublicou(unittest.TestCase):
    """`compute_basis` aceita `graph_consumed` desde o F09 e os três chamadores reais não o
    passam. Uma revisão que declare a dependência fica com a fonte no registo e sem ela na
    comparação — e uma fonte que desaparece é `stale`, sem nada ter mudado."""

    def test_every_call_site_passes_what_the_record_declared(self):
        fonte = (TOOLS / "coverage.py").read_text(encoding="utf-8")
        chamadas = [l.strip() for l in fonte.splitlines()
                    if "compute_basis(" in l and not l.strip().startswith("def ")]
        self.assertTrue(chamadas, "não há chamadas a `compute_basis`")
        sem = [c for c in chamadas if "graph_consumed" not in c]
        self.assertEqual(sem, [],
                         "chamada que não passa a dependência declarada: " + " | ".join(sem))

    def test_a_declared_dependency_survives_a_freshness_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_migrado(tmp)
            inv = C["build_inventory"](eng)
            base = C["compute_basis"](eng, inv, "reconciliation", graph_consumed=["C-001"])
            agora = C["compute_basis"](eng, C["build_inventory"](eng), "reconciliation")
            fresh = C["check_freshness"]({"basis": base}, agora)
        self.assertEqual(
            fresh["status"], "current",
            "a dependência do grafo desapareceu da comparação e isso sozinho deu `stale`")


# =============================================================================
# R2-06 · P2 — os comandos, a sério; e um veredicto que não é veredicto
# =============================================================================

class R2_06_OsComandosASerio(unittest.TestCase):
    """Os casos do F10 procuram palavras nos ficheiros. `ACCEPTANCE.md` §1 já dizia que um
    teste de estrutura de prompts não prova comportamento de runtime — e foi isso que eu
    escrevi.

    E o gate continua a calcular o veredicto sobre estado indisponível, com um aviso ao
    lado. Um veredicto metodológico calculado sobre estado que não se consegue ler não é um
    veredicto mau: **não é um veredicto**. Isso não o torna um bloqueio — torna-o `não
    avaliável`, que é a terceira coisa e a que já existia no vocabulário do gate."""

    def _eng_com_pendencia(self, tmp):
        eng = eng_migrado(tmp)
        O["_atomic_write"](O["pending_path"](eng), json.dumps(
            {"intent_version": 1, "operation_id": "op-x", "request_hash": "h",
             "owner": {}, "before": {}, "after": {SU_FILE: "f" * 64},
             "staging": "_ops/staging/op-x"}))
        return eng

    def test_the_gate_does_not_issue_a_verdict_over_unreadable_state(self):
        import subprocess
        import sys
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._eng_com_pendencia(tmp)
            p = subprocess.run(
                [sys.executable, str(ROOT / ".claude" / "hooks" / "phase-gate-check.py"),
                 "--engagement", str(eng), "--skill", "aisa-frame"],
                capture_output=True, text=True, timeout=120,
                env={"PATH": "/usr/bin:/bin", "AISA_ENGAGEMENTS_ROOT": str(eng.parent)})
            linha = (eng / "gate-log.md").read_text(encoding="utf-8").strip().splitlines()[-1]
        self.assertEqual(p.returncode, 0, "o gate bloqueou; é soft por desenho")
        self.assertIn("nao avaliavel", linha.lower().replace("ã", "a").replace("á", "a"),
                      "emitiu um veredicto sobre estado que não se consegue ler: " + linha)

    def test_the_status_command_really_consults_the_kernel(self):
        """Executar, não procurar a palavra no SKILL.md."""
        import subprocess
        import sys
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._eng_com_pendencia(tmp)
            p = subprocess.run(
                [sys.executable, str(TOOLS / "projection.py"),
                 "--engagement", str(eng), "--json"],
                capture_output=True, text=True, timeout=120)
        self.assertEqual(p.returncode if p.returncode in (0, 1) else 99, p.returncode)
        saida = json.loads(p.stdout or "{}")
        self.assertFalse(saida.get("ready", True),
                         "o comando que o /status consulta declarou pronto sobre pendência")
        self.assertTrue(saida.get("blockers"),
                        "não nomeou bloqueio nenhum sobre uma operação pendente")


if __name__ == "__main__":
    unittest.main(verbosity=1)
