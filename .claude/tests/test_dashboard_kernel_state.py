# -*- coding: utf-8 -*-
"""A página viva não se apresenta limpa sobre estado que o kernel recusa.

Terceira perna do F10, e a que ninguém apontou. As duas rondas de auditoria olharam para o
`/status` e para o gate de fase; o `dashboard.py` não estava em nenhuma das listas.

Medido antes de existir esta correcção: engagement com operação pendente, `bootstrap` a
devolver `ready=False`, e a página a sair com **75 KB, exit 0 e nem uma palavra** sobre o
bloqueio. As contagens estavam todas certas — é esse o problema. Uma página que conta bem
sobre estado por reconstruir apresenta estado misto como estado, e a diferença não aparece
em contagem nenhuma.

É o pior sítio para isto acontecer, por três razões que se somam:

- é o que o sponsor lê, e ele não tem como saber que devia desconfiar;
- o hook `on-su-change.py` regenera-a a CADA escrita, por isso a página errada aparece
  sozinha, sem ninguém a pedir;
- o `/status` consulta a projecção no passo 1b — mas os números que apresenta vêm daqui.

O que isto NÃO faz: bloquear. A página continua a gerar-se e o comando continua a sair 0.
Um dashboard que se recusasse a desenhar seria um bloqueio de integridade — e isso é do
guarda de escrita, não de um leitor."""
import json
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "library" / "kernel" / "tools"
D = runpy.run_path(str(TOOLS / "dashboard.py"))
O = runpy.run_path(str(TOOLS / "operation.py"))
B = runpy.run_path(str(TOOLS / "bootstrap.py"))
M = runpy.run_path(str(TOOLS / "migrate.py"))
FIX = runpy.run_path(str(ROOT / ".claude" / "tests" / "test_migration.py"))

from datetime import date


def eng_migrado(tmp, su=None):
    eng = FIX["make"](tmp, su or FIX["NOVO"])
    M["apply"](eng)
    return eng


def com_pendencia(eng):
    O["_atomic_write"](O["pending_path"](eng), json.dumps(
        {"intent_version": 1, "operation_id": "op-x", "request_hash": "h", "owner": {},
         "before": {}, "after": {"shared-understanding.md": "f" * 64},
         "staging": "_ops/staging/op-x"}))
    return eng


def gera(eng):
    p = subprocess.run([sys.executable, str(TOOLS / "dashboard.py"),
                        "--engagement", str(eng), "--quiet", "--force"],
                       capture_output=True, text=True, timeout=300)
    return p, (eng / "dashboard.html").read_text(encoding="utf-8")


class D1_OModeloCarregaOEstadoDoKernel(unittest.TestCase):

    def test_the_model_says_whether_the_kernel_is_ready(self):
        with tempfile.TemporaryDirectory() as tmp:
            modelo = D["build_model"](eng_migrado(tmp), date.today())
        self.assertIn("kernel", modelo,
                      "o modelo não carrega o estado do kernel, por isso nada a jusante o "
                      "pode mostrar")
        self.assertTrue(modelo["kernel"].get("ready"))

    def test_a_pending_operation_shows_up_in_the_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            modelo = D["build_model"](com_pendencia(eng_migrado(tmp)), date.today())
        k = modelo["kernel"]
        self.assertFalse(k["ready"])
        self.assertIn("PENDING_OPERATION", [l.get("code") for l in k.get("limitations", [])])

    def test_it_names_the_action_that_clears_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            modelo = D["build_model"](com_pendencia(eng_migrado(tmp)), date.today())
        recuperacoes = [l.get("recovery", "") for l in modelo["kernel"]["limitations"]]
        self.assertTrue([r for r in recuperacoes if r],
                        "diz que está bloqueado e não diz o que fazer")

    def test_a_kernel_that_cannot_be_consulted_is_not_a_ready_one(self):
        """Falha fechada: não conseguir avaliar não é o mesmo que ter avaliado.

        A primeira versão deste caso punha o próprio `kernel_state` a rebentar e esperava
        que o `build_model` apanhasse — mas o «falha fechada» vive DENTRO do `kernel_state`,
        que é quem chama o bootstrap. Pedir a captura um nível acima testava outra coisa.
        Aqui rebenta o bootstrap, que é o caminho real.
        """
        cache = D["_KERNEL_MODULE"]
        guardado = dict(cache)

        class BootstrapQueRebenta(dict):
            def __getitem__(self, k):
                if k == "bootstrap":
                    return lambda eng: (_ for _ in ()).throw(
                        RuntimeError("kernel indisponível"))
                return super().__getitem__(k)

        cache["mod"] = BootstrapQueRebenta()
        try:
            with tempfile.TemporaryDirectory() as tmp:
                estado = D["kernel_state"](eng_migrado(tmp))
        finally:
            cache.clear()
            cache.update(guardado)
        self.assertFalse(estado["ready"], "não conseguiu consultar e deu-se por pronto")
        self.assertFalse(estado["consulted"],
                         "diz que consultou o kernel quando não conseguiu")
        self.assertIn("KERNEL_UNAVAILABLE",
                      [l["code"] for l in estado["limitations"]])


class D2_APaginaDiOloEmLinguagemDeNegocio(unittest.TestCase):

    def test_the_page_says_it_when_the_kernel_refuses(self):
        with tempfile.TemporaryDirectory() as tmp:
            p, html = gera(com_pendencia(eng_migrado(tmp)))
        self.assertEqual(p.returncode, 0, "a página deixou de se gerar; isto não bloqueia")
        self.assertIn("por reconstruir", html.lower(),
                      "gerou uma página normal sobre um engagement bloqueado")

    def test_a_clean_engagement_carries_no_alarm(self):
        """Um aviso que aparece sempre não é um aviso."""
        with tempfile.TemporaryDirectory() as tmp:
            _p, html = gera(eng_migrado(tmp))
        self.assertNotIn("por reconstruir", html.lower(),
                         "alarme sobre um engagement limpo")

    def test_the_warning_comes_before_the_numbers(self):
        with tempfile.TemporaryDirectory() as tmp:
            _p, html = gera(com_pendencia(eng_migrado(tmp)))
        i_aviso = html.lower().index("por reconstruir")
        corpo = html.lower().index("<body")
        self.assertLess(i_aviso - corpo, 12000,
                        "o aviso está enterrado a meio da página: quem lê o topo conclui "
                        "sobre estado misto na mesma")

    def test_it_is_business_language(self):
        """P-13: o utilizador lê negócio; o termo do kernel vai entre parênteses."""
        with tempfile.TemporaryDirectory() as tmp:
            _p, html = gera(com_pendencia(eng_migrado(tmp)))
        i = html.lower().index("por reconstruir")
        trecho = html[max(0, i - 400):i + 400]
        self.assertNotIn("PENDING_OPERATION", trecho.replace("(PENDING_OPERATION)", ""),
                         "o código do kernel aparece fora de parênteses")
        # O detalhe que o kernel escreve é vocabulário de kernel. Mostrá-lo tal e qual
        # punha «mutação» e «gate» à frente do sponsor — o caso anterior só olhava ao
        # código e deixava passar a frase inteira.
        for termo in ("mutação", "gate", "bootstrap", "snapshot", "drift"):
            self.assertNotIn(termo, trecho.lower(),
                             "vocabulário de kernel na página: " + termo)

    def test_the_page_still_renders_everything_else(self):
        """Declarar a limitação não é deixar de mostrar o resto."""
        with tempfile.TemporaryDirectory() as tmp:
            _p, html = gera(com_pendencia(eng_migrado(tmp)))
        self.assertGreater(len(html), 20000, "a página encolheu: deixou de mostrar o resto")
        self.assertIn("C-001", html, "as linhas da SU desapareceram")


if __name__ == "__main__":
    unittest.main(verbosity=1)
