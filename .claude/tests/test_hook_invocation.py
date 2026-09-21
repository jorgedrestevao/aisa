"""R7 / DEF-P1-02 — os hooks resolvem-se pela raiz do projecto, não pelo cwd.

`docs/PILOT_RUNTIME_CORRECTION_PLAN.md` → R7. Os nove hooks estavam registados por
caminho relativo (`python .claude/hooks/pre-write-guard.py`). O comando corre com o cwd
da **sessão**, e basta um `cd` numa chamada Bash para o cwd derivar: a partir daí o
Python procura o script numa pasta que não existe, o `PreToolUse` não arranca e a
ferramenta é **recusada por erro**. Falha fechada — nada se corrompe — mas o runtime
pára, e a mensagem fala de um ficheiro inexistente em vez de dizer o que se passa.

Medido ao vivo, na cópia descartável, com o cwd derivado por `cd projects/smoke`:

    baseline   PreToolUse:Write hook error: [python .claude/hooks/pre-write-guard.py]:
               can't open file '...\\projects\\smoke\\.claude\\hooks\\pre-write-guard.py'
    corrigido  permissionDecision: deny — "library/ is read-only at runtime"

`$CLAUDE_PROJECT_DIR` foi **verificado no ambiente real** antes de se escolher (sonda
com dois hooks registados no mesmo evento): o Claude Code fornece-a aos hooks e o shell
expande-a, inclusive em caminhos com espaços e acentos. A forma usada é
`"${CLAUDE_PROJECT_DIR:-.}/..."` — com a variável ausente degrada para o comportamento
antigo em vez de apontar para a raiz do disco.

Os scripts em si nunca dependeram do cwd (resolvem por `Path(__file__)`); o defeito
estava só na linha de registo, e é isso que estes testes seguram, em três camadas:

1. **forma** — como os nove comandos estão escritos em `settings.json`;
2. **script** — cada script a arrancar e a decidir de vários cwd (o caminho é resolvido
   pelo teste: prova o script, não a linha de registo);
3. **comando** — a linha de registo **tal como está escrita**, entregue a um shell com
   `CLAUDE_PROJECT_DIR` no ambiente, de vários cwd. É esta camada que exercita a
   expansão; sem ela o teste estaria a substituir aquilo que devia verificar.

A camada 3 usa `bash` porque é essa a semântica de que a forma registada depende
(`${VAR:-.}`); onde não houver `bash`, a camada declara-se ignorada em vez de fingir
que passou. O que nenhuma das três dá é o carregamento pelo próprio Claude Code — isso
é o smoke, com a evidência bruta em `docs/pilot-runtime-correction/R7-evidence/`.

Nota do que ISTO não cobre: uma sessão **começada** numa subpasta não carrega o
`.claude/settings.json` do repositório de todo (`hooks: null`), medido na mesma sonda.
São condições diferentes — hook não carregado contra hook carregado cujo comando não
resolve — e a segunda é a que este ficheiro trata.

    python .claude/tests/test_hook_invocation.py
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SETTINGS = ROOT / ".claude" / "settings.json"

# `python "${CLAUDE_PROJECT_DIR:-.}/.claude/hooks/<script>.py"`
CMD_RE = re.compile(
    r'^python "\$\{CLAUDE_PROJECT_DIR:-\.\}/(\.claude/hooks/[A-Za-z0-9_.-]+\.py)"$')


def registered():
    """-> [(evento, matcher, comando)]"""
    data = json.loads(SETTINGS.read_text(encoding="utf-8"))
    out = []
    for event, blocks in (data.get("hooks") or {}).items():
        for block in blocks:
            for h in block.get("hooks", []):
                out.append((event, block.get("matcher", ""), h.get("command", "")))
    return out


class ComoEstaoRegistados(unittest.TestCase):

    def test_ha_hooks_registados(self):
        self.assertGreaterEqual(len(registered()), 9)

    def test_nenhum_comando_depende_da_pasta_corrente(self):
        maus = [c for _e, _m, c in registered()
                if c.startswith("python .") or c.startswith("python ./")]
        self.assertEqual(maus, [], "comando por caminho relativo ao cwd")

    def test_todos_resolvem_pela_raiz_do_projecto(self):
        for event, _m, cmd in registered():
            with self.subTest(event=event, cmd=cmd):
                self.assertRegex(cmd, CMD_RE)

    def test_a_variavel_ausente_degrada_para_a_raiz_relativa(self):
        """`:-.` é o que impede que uma variável em falta aponte para a raiz do disco:
        sem ela o comando ficaria `python "/.claude/hooks/x.py"`."""
        for _e, _m, cmd in registered():
            self.assertIn("${CLAUDE_PROJECT_DIR:-.}", cmd)

    def test_o_script_de_cada_comando_existe(self):
        for event, _m, cmd in registered():
            m = CMD_RE.match(cmd)
            self.assertIsNotNone(m, cmd)
            with self.subTest(event=event):
                self.assertTrue((ROOT / m.group(1)).is_file(), m.group(1))

    def test_o_caminho_vai_entre_aspas(self):
        """A raiz do projecto pode ter espaços — e tem, neste repositório."""
        for _e, _m, cmd in registered():
            self.assertTrue(cmd.endswith('"'), cmd)
            self.assertIn(' "', cmd)


class RaizTemporaria(unittest.TestCase):
    """Uma raiz de projecto descartável, com espaço e acento no caminho.

    Só leitura do repositório: copia-se `.claude/hooks`, `settings.json` e `library/`
    para a raiz temporária, e é sobre ela que os hooks decidem — nunca sobre este
    repositório nem sobre engagement nenhum.
    """

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="aisa-r7-")
        # uma raiz com espaço e acento, como as que existem na vida real
        self.raiz = Path(self.tmp) / "raiz com espaço e acento ã"
        (self.raiz / ".claude").mkdir(parents=True)
        shutil.copytree(ROOT / ".claude" / "hooks", self.raiz / ".claude" / "hooks")
        shutil.copy2(SETTINGS, self.raiz / ".claude" / "settings.json")
        shutil.copytree(ROOT / "library", self.raiz / "library")
        (self.raiz / "projects" / "smoke").mkdir(parents=True)
        (self.raiz / "fora").mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def cwds(self):
        return [("raiz", self.raiz),
                ("pasta do engagement", self.raiz / "projects" / "smoke"),
                ("pasta externa", Path(self.tmp))]


class CorreDeQualquerPasta(RaizTemporaria):
    """Camada 2 — o SCRIPT de cada hook, com o caminho resolvido pelo teste."""

    def run_hook(self, cmd, cwd, payload):
        """Resolve o caminho do script e corre-o a partir de `cwd`. Prova o script;
        a linha de registo é a camada 3."""
        m = CMD_RE.match(cmd)
        script = str(self.raiz / m.group(1))
        return subprocess.run(
            [sys.executable, script], cwd=str(cwd), input=json.dumps(payload).encode(),
            capture_output=True,
            env=dict(os.environ, CLAUDE_PROJECT_DIR=str(self.raiz),
                     PYTHONIOENCODING="utf-8"))

    def test_cada_hook_arranca_de_qualquer_cwd_suportado(self):
        payload = {"hook_event_name": "PreToolUse", "tool_name": "Skill",
                   "tool_input": {"skill": "aisa-status"}}
        for event, _m, cmd in registered():
            for nome, cwd in self.cwds():
                with self.subTest(event=event, cwd=nome, cmd=cmd):
                    r = self.run_hook(cmd, cwd, payload)
                    self.assertNotIn(b"No such file or directory", r.stderr)
                    self.assertNotIn(b"can't open file", r.stderr)

    def test_o_guarda_recusa_library_a_partir_de_qualquer_cwd(self):
        cmd = next(c for _e, _m, c in registered() if "pre-write-guard" in c)
        alvo = str(self.raiz / "library" / "kernel" / "states.md")
        for nome, cwd in self.cwds():
            with self.subTest(cwd=nome):
                r = self.run_hook(cmd, cwd, {
                    "hook_event_name": "PreToolUse", "tool_name": "Write",
                    "tool_input": {"file_path": alvo, "content": "x"}})
                saida = (r.stdout + r.stderr).decode("utf-8", "replace")
                self.assertIn("deny", saida.lower(), saida[:300])

    def test_o_guarda_deixa_passar_o_engagement_a_partir_de_qualquer_cwd(self):
        cmd = next(c for _e, _m, c in registered() if "pre-write-guard" in c)
        alvo = str(self.raiz / "projects" / "smoke" / "shared-understanding.md")
        for nome, cwd in self.cwds():
            with self.subTest(cwd=nome):
                r = self.run_hook(cmd, cwd, {
                    "hook_event_name": "PreToolUse", "tool_name": "Write",
                    "tool_input": {"file_path": alvo, "content": "# SU\n"}})
                saida = (r.stdout + r.stderr).decode("utf-8", "replace")
                self.assertNotIn("deny", saida.lower(), saida[:300])
                self.assertEqual(r.returncode, 0, saida[:300])

    def test_stdin_invalido_nao_faz_o_hook_rebentar(self):
        for event, _m, cmd in registered():
            m = CMD_RE.match(cmd)
            with self.subTest(event=event):
                r = subprocess.run(
                    [sys.executable, str(self.raiz / m.group(1))],
                    cwd=str(self.raiz), input=b"isto nao e json",
                    capture_output=True,
                    env=dict(os.environ, CLAUDE_PROJECT_DIR=str(self.raiz),
                             PYTHONIOENCODING="utf-8"))
                self.assertNotEqual(r.returncode, 1,
                                    "stdin partido tem de ser fail-open ou deny limpo")

    def test_evento_que_nao_lhe_diz_respeito_e_ignorado(self):
        cmd = next(c for _e, _m, c in registered() if "pre-write-guard" in c)
        r = self.run_hook(cmd, self.raiz, {
            "hook_event_name": "PreToolUse", "tool_name": "Read",
            "tool_input": {"file_path": str(self.raiz / "library" / "kernel" / "states.md")}})
        self.assertEqual(r.returncode, 0)
        self.assertNotIn("deny", (r.stdout + r.stderr).decode("utf-8", "replace").lower())


def _find_bash():
    """O `bash` do PATH, ou o do Git for Windows, que existe em qualquer maquina onde
    este repositorio e clonado. Correr a suite a partir do PowerShell nao pode fazer
    desaparecer a unica camada que exercita a expansao do comando."""
    found = shutil.which("bash")
    if found:
        return found
    candidatos = []
    for var in ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA"):
        base = os.environ.get(var)
        if base:
            candidatos += [Path(base) / "Git" / "bin" / "bash.exe",
                           Path(base) / "Git" / "usr" / "bin" / "bash.exe",
                           Path(base) / "Programs" / "Git" / "bin" / "bash.exe"]
    candidatos += [Path("/usr/bin/bash"), Path("/bin/bash")]
    for c in candidatos:
        try:
            if c.is_file():
                return str(c)
        except OSError:
            continue
    return None


BASH = _find_bash()


@unittest.skipIf(not BASH, "sem bash em lado nenhum: a expansao nao e exercitada")
class OComandoRegistadoCorreNoShell(RaizTemporaria):
    """A linha de registo, verbatim, entregue a um shell — a camada que a anterior não
    dá. `CorreDeQualquerPasta` resolve o caminho do script em Python e prova o script;
    aqui não se toca no comando: `${CLAUDE_PROJECT_DIR:-.}` é expandido por quem o
    executa, como acontece no runtime."""

    def shell_hook(self, cmd, cwd, payload, com_variavel=True):
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        if com_variavel:
            env["CLAUDE_PROJECT_DIR"] = str(self.raiz)
        else:
            env.pop("CLAUDE_PROJECT_DIR", None)
        return subprocess.run([BASH, "-c", cmd], cwd=str(cwd),
                              input=json.dumps(payload).encode(),
                              capture_output=True, env=env)

    def test_o_comando_verbatim_arranca_de_qualquer_cwd(self):
        payload = {"hook_event_name": "PreToolUse", "tool_name": "Skill",
                   "tool_input": {"skill": "aisa-status"}}
        for event, _m, cmd in registered():
            for nome, cwd in self.cwds():
                with self.subTest(event=event, cwd=nome, cmd=cmd):
                    r = self.shell_hook(cmd, cwd, payload)
                    saida = (r.stdout + r.stderr).decode("utf-8", "replace")
                    self.assertNotIn("can't open file", saida)
                    self.assertNotIn("No such file or directory", saida)

    def test_o_comando_verbatim_recusa_library_do_cwd_derivado(self):
        cmd = next(c for _e, _m, c in registered() if "pre-write-guard" in c)
        alvo = str(self.raiz / "library" / "kernel" / "states.md")
        r = self.shell_hook(cmd, self.raiz / "projects" / "smoke", {
            "hook_event_name": "PreToolUse", "tool_name": "Write",
            "tool_input": {"file_path": alvo, "content": "x"}})
        saida = (r.stdout + r.stderr).decode("utf-8", "replace")
        self.assertIn("deny", saida.lower(), saida[:300])
        self.assertEqual(r.returncode, 2, saida[:300])

    def test_o_comando_verbatim_deixa_passar_o_engagement(self):
        cmd = next(c for _e, _m, c in registered() if "pre-write-guard" in c)
        alvo = str(self.raiz / "projects" / "smoke" / "shared-understanding.md")
        r = self.shell_hook(cmd, self.raiz / "projects" / "smoke", {
            "hook_event_name": "PreToolUse", "tool_name": "Write",
            "tool_input": {"file_path": alvo, "content": "# SU\n"}})
        saida = (r.stdout + r.stderr).decode("utf-8", "replace")
        self.assertEqual(r.returncode, 0, saida[:300])
        self.assertNotIn("deny", saida.lower())

    def test_sem_a_variavel_a_raiz_continua_a_funcionar(self):
        """A omissão `:-.` faz o comando degradar para o caminho relativo: com a
        variável ausente e o cwd na raiz, o hook ainda corre."""
        cmd = next(c for _e, _m, c in registered() if "pre-write-guard" in c)
        alvo = str(self.raiz / "library" / "kernel" / "states.md")
        r = self.shell_hook(cmd, self.raiz, {
            "hook_event_name": "PreToolUse", "tool_name": "Write",
            "tool_input": {"file_path": alvo, "content": "x"}}, com_variavel=False)
        saida = (r.stdout + r.stderr).decode("utf-8", "replace")
        self.assertIn("deny", saida.lower(), saida[:300])

    def test_sem_a_variavel_e_fora_da_raiz_e_que_se_perdia(self):
        """O contraponto, que mede o que a variável faz: sem ela, e com o cwd
        derivado, o script volta a não ser encontrado — exactamente o DEF-P1-02. É por
        isto que a fallback não substitui a variável, só evita o pior."""
        cmd = next(c for _e, _m, c in registered() if "pre-write-guard" in c)
        r = self.shell_hook(cmd, self.raiz / "projects" / "smoke", {
            "hook_event_name": "PreToolUse", "tool_name": "Write",
            "tool_input": {"file_path": "x", "content": "x"}}, com_variavel=False)
        saida = (r.stdout + r.stderr).decode("utf-8", "replace")
        self.assertNotEqual(r.returncode, 0)
        self.assertTrue("can't open file" in saida or "No such file" in saida, saida[:200])


class ACamadaDoShellExiste(unittest.TestCase):
    """Um `skip` silencioso na camada 3 e indistinguivel de um teste que passa. Este
    caso torna-o visivel: se o bash nao for encontrado, a suite diz onde procurou."""

    def test_o_bash_foi_encontrado(self):
        if BASH:
            self.assertTrue(Path(BASH).is_file() or shutil.which(BASH))
            return
        self.skipTest("bash nao encontrado no PATH nem na instalacao do Git for Windows "
                      "-- a camada 3 (comando verbatim) NAO correu nesta maquina")


class ADocumentacaoDizComoSeInvoca(unittest.TestCase):

    def test_hooks_md_explica_a_dependencia_da_raiz(self):
        txt = (ROOT / ".claude" / "hooks" / "HOOKS.md").read_text(encoding="utf-8")
        self.assertIn("CLAUDE_PROJECT_DIR", txt)


if __name__ == "__main__":
    unittest.main(verbosity=2)
