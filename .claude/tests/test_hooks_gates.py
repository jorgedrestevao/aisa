"""Endurecimento do runtime, bloco C — o portão de fase é avaliado, e o veredicto fica escrito.

O que substituiu: `phase-gate-check.py` era um stub que imprimia «v0.2.0 will validate…» e
saía 0. Registar que uma skill correu não estabelece que o seu portão foi verificado.

O que estes testes afirmam, e porquê cada um existe:

  identidade      o `G-id` é a impressão digital do ESTADO julgado, não das contagens.
                  Trocar `U-001` por `U-002` deixa todos os números onde estavam; se o id
                  não mudasse, um override de hoje ligar-se-ia à avaliação de outra
                  realidade. Acrescentar uma aprovação a `decisions.md` muda o veredicto
                  sem tocar na SU — por isso `decisions.md` entra na impressão digital.
  ciclo de vida   o override chega numa SEGUNDA invocação; as duas linhas ligam-se por
                  `refers` quando o estado não mexeu, e `refers: none` quando mexeu.
  cobertura       cada critério traz o seu modo; `n/a` nunca se lê como OK, e um critério
                  por opção com zero opções não é verdade vazia.
  engagement      explícito. Com vários montados e sem slug, não se escreve nada — um
                  veredicto no projecto errado é pior do que veredicto nenhum.

    python .claude/tests/test_hooks_gates.py
"""

import json
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
D = runpy.run_path(str(ROOT / "library" / "kernel" / "tools" / "dashboard.py"))
HOOK = ROOT / ".claude" / "hooks" / "phase-gate-check.py"

SU_HEAD = """# Shared Understanding — {slug}

**Engagement**: {slug}
**Phase**: discovery
**Pack**: pp
**Last updated**: 2026-09-10

"""
COLS = {
    "Confirmed": ["id", "lens", "claim", "evidência", "verificado_em", "validade", "ronda"],
    "Assumed": ["id", "lens", "claim", "base da assumption", "verificado_em", "validade", "ronda"],
    "Unknown": ["id", "lens", "pergunta", "quem responde", "criticidade", "custo", "swing", "ronda"],
    "Conflicted": ["id", "lens", "conflito", "partes", "criticidade", "ronda"],
    "Risky": ["id", "lens", "risco", "impacto", "mitigação proposta", "ronda"],
}


def su_text(slug, sections=None):
    out = [SU_HEAD.format(slug=slug)]
    for name, cols in COLS.items():
        out.append("## " + name + "\n")
        out.append("| " + " | ".join(cols) + " |")
        out.append("|" + "|".join(["---"] * len(cols)) + "|")
        for cells in (sections or {}).get(name, []):
            out.append("| " + " | ".join(str(c) for c in cells) + " |")
        out.append("")
    return "\n".join(out) + "\n"


def confirmed(n):
    return [["C-{:03d}".format(i), "business", "facto {}".format(i), "inputs/x.xlsx#S!A{}".format(i),
             "2026-09-01", "organizacional", "R-01"] for i in range(1, n + 1)]


def unknown(ids, crit="Critical"):
    return [[i, "data", "pergunta?", "role: IT", crit, "baixo", "decisivo", "R-01"] for i in ids]


def mk(tmp, slug="fx", *, phase="discovery", sections=None, decisions="# Decisions\n",
       lenses=True, options="", frame="", files=None):
    eng = Path(tmp) / slug
    eng.mkdir(parents=True, exist_ok=True)
    (eng / "_state.json").write_text(json.dumps(
        {"engagement": slug, "pack": "pp", "phase": phase, "round": "R-01"}), encoding="utf-8")
    (eng / "shared-understanding.md").write_text(su_text(slug, sections), encoding="utf-8")
    (eng / "decisions.md").write_text(decisions, encoding="utf-8")
    (eng / "options.md").write_text(options, encoding="utf-8")
    (eng / "frame.md").write_text(frame, encoding="utf-8")
    (eng / "council-log.md").write_text("# Council log\n", encoding="utf-8")
    lo = eng / "lens-outputs"
    lo.mkdir(exist_ok=True)
    if lenses:
        for lens in D["LENSES_6"]:
            (lo / (lens + ".md")).write_text("# {}\n\nC-001 lido.\n".format(lens), encoding="utf-8")
    for rel, body in (files or {}).items():
        p = eng / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")
    return eng


def run_hook(payload=None, argv=None, cwd=None, env_root=None):
    import os
    env = dict(os.environ)
    if env_root:
        env["AISA_ENGAGEMENTS_ROOT"] = str(env_root)
    return subprocess.run([sys.executable, str(HOOK)] + (argv or []),
                          input=json.dumps(payload) if payload is not None else "",
                          text=True, capture_output=True, encoding="utf-8",
                          errors="replace", cwd=str(cwd or ROOT), env=env)


class Coverage(unittest.TestCase):
    """Cada critério traz o seu modo, e a cobertura diz-se."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def test_discovery_criteria_carry_their_mode(self):
        eng = mk(self.tmp.name, sections={"Confirmed": confirmed(12)})
        g = D["gate_state"](eng, "discovery→framing")
        modes = {c["criterion"]: c["mode"] for c in g["criteria"]}
        self.assertEqual(modes["teste de compreensão"], "juizo")
        self.assertTrue(all(m in ("codigo", "juizo", "n/a") for m in modes.values()))
        for c in g["criteria"]:
            if c["mode"] != "codigo":
                self.assertIsNone(c["ok"], c["criterion"])

    def test_a_judgement_criterion_is_never_reported_as_ok(self):
        eng = mk(self.tmp.name, sections={"Confirmed": confirmed(12)})
        g = D["gate_state"](eng, "discovery→framing")
        self.assertIn("teste de compreensão", g["judgement"])
        self.assertNotIn("teste de compreensão", g["red"])
        self.assertEqual(g["total"], sum(1 for c in g["criteria"] if c["mode"] == "codigo"))

    def test_the_note_declares_coverage_not_a_verdict(self):
        eng = mk(self.tmp.name, sections={"Confirmed": confirmed(12)})
        g = D["gate_state"](eng, "discovery→framing")
        self.assertIn("por código", g["note"])
        self.assertNotIn("OK", g["note"])

    def test_counts_and_presence_are_actually_computed(self):
        few = mk(self.tmp.name, "few", sections={"Confirmed": confirmed(3)})
        g = D["gate_state"](few, "discovery→framing")
        red = {c["criterion"]: c for c in g["criteria"] if c["mode"] == "codigo" and not c["ok"]}
        self.assertIn("Confirmed >= 10", red)
        self.assertEqual(red["Confirmed >= 10"]["value"], "3")

    def test_a_critical_unknown_is_red_and_named(self):
        eng = mk(self.tmp.name, "crit", sections={
            "Confirmed": confirmed(12), "Unknown": unknown(["U-001"])})
        g = D["gate_state"](eng, "discovery→framing")
        row = next(c for c in g["criteria"] if c["criterion"] == "Unknown Critical = 0")
        self.assertFalse(row["ok"])
        self.assertIn("U-001", row["value"])

    def test_a_lens_file_without_ids_is_not_content(self):
        eng = mk(self.tmp.name, "nolens", sections={"Confirmed": confirmed(12)})
        (eng / "lens-outputs" / "data.md").write_text("# data\n\nsem ids.\n", encoding="utf-8")
        g = D["gate_state"](eng, "discovery→framing")
        row = next(c for c in g["criteria"] if c["criterion"].startswith("6 lentes"))
        self.assertFalse(row["ok"])
        self.assertIn("presença", row["note"])

    def test_options_criteria_with_zero_options_are_not_vacuously_ok(self):
        """Uma verdade vazia (0/0) reportada como OK é o padrão que esta frente remove."""
        eng = mk(self.tmp.name, "noopt", phase="options", options="# Options\n")
        g = D["gate_state"](eng, "options→decision")
        per_option = [c for c in g["criteria"]
                      if c["criterion"].startswith("cada opção")]
        self.assertTrue(per_option)
        for c in per_option:
            self.assertEqual(c["mode"], "n/a", c["criterion"])
            self.assertIsNone(c["ok"])

    def test_the_technology_criterion_reads_the_column_not_the_prose(self):
        table = ("# Options\n\n"
                 "| # | Alternativa | Tecnologia | Veredicto |\n"
                 "|---|---|---|---|\n"
                 "| O-001 | Mudar o processo | sem tecnologia — mudança de processo | viável |\n"
                 "| O-002 | App sobre a base | canvas app + Azure SQL | viável |\n"
                 "| O-003 | Não fazer nada | sem tecnologia — não fazer | viável |\n")
        eng = mk(self.tmp.name, "tbl", phase="options", options=table)
        g = D["gate_state"](eng, "options→decision")
        row = next(c for c in g["criteria"] if c["criterion"].startswith("cada opção nomeia"))
        self.assertEqual(row["mode"], "codigo")
        self.assertTrue(row["ok"], row["value"])       # nenhuma das três diz "tecnologia"
        empty = table.replace("| sem tecnologia — não fazer |", "|  |")
        eng2 = mk(self.tmp.name, "tbl2", phase="options", options=empty)
        row2 = next(c for c in D["gate_state"](eng2, "options→decision")["criteria"]
                    if c["criterion"].startswith("cada opção nomeia"))
        self.assertFalse(row2["ok"])
        self.assertIn("O-003", row2["value"])

    def test_without_a_decision_table_the_criterion_is_not_evaluable(self):
        eng = mk(self.tmp.name, "notbl", phase="options",
                 options="# Options\n\n### O-001\n### O-002\n### O-003\n")
        row = next(c for c in D["gate_state"](eng, "options→decision")["criteria"]
                   if c["criterion"].startswith("cada opção nomeia"))
        self.assertEqual(row["mode"], "n/a")

    def test_decision_tree_consulted_is_declared_unevaluable(self):
        eng = mk(self.tmp.name, "dt", phase="options", options="# Options\n")
        g = D["gate_state"](eng, "options→decision")
        self.assertIn("decision-tree.md do pacote consultado", g["na"])


class Identity(unittest.TestCase):
    """O id é do estado julgado, não das contagens."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def test_same_counts_different_ids_give_different_fingerprints(self):
        a = mk(self.tmp.name, "a", sections={"Confirmed": confirmed(12),
                                             "Unknown": unknown(["U-001"])})
        b = mk(self.tmp.name, "b", sections={"Confirmed": confirmed(12),
                                             "Unknown": unknown(["U-002"])})
        ga = D["gate_state"](a, "discovery→framing")
        gb = D["gate_state"](b, "discovery→framing")
        red_a = next(c for c in ga["criteria"] if c["criterion"] == "Unknown Critical = 0")
        red_b = next(c for c in gb["criteria"] if c["criterion"] == "Unknown Critical = 0")
        self.assertEqual(red_a["value"].split(" ")[0], red_b["value"].split(" ")[0])  # contagens iguais
        self.assertNotEqual(ga["fingerprint"], gb["fingerprint"])
        self.assertNotEqual(ga["id"], gb["id"])

    def test_an_approval_alone_changes_the_id(self):
        """O veredicto de Framing vem de decisions.md; sem ele na impressão digital, uma
        aprovação nova reutilizaria o id da avaliação anterior."""
        frame = "# Frame\n\nThe problem is X, felt by Y, costs Z, evidence W.\n"
        eng = mk(self.tmp.name, "fr", phase="framing", frame=frame)
        before = D["gate_state"](eng, "framing→options")
        (eng / "decisions.md").write_text(
            "# Decisions\n\n## D-001 — Frame agreed\n- **Validated by**: sponsor\n"
            "- **Timestamp**: 2026-09-10T10:00:00Z\n", encoding="utf-8")
        after = D["gate_state"](eng, "framing→options")
        self.assertNotEqual(before["id"], after["id"])
        v_before = next(c for c in before["criteria"] if c["criterion"].startswith("`Validated"))
        v_after = next(c for c in after["criteria"] if c["criterion"].startswith("`Validated"))
        self.assertFalse(v_before["ok"])
        self.assertTrue(v_after["ok"])

    def test_the_same_state_gives_the_same_id(self):
        eng = mk(self.tmp.name, "same", sections={"Confirmed": confirmed(12)})
        self.assertEqual(D["gate_state"](eng, "discovery→framing")["id"],
                         D["gate_state"](eng, "discovery→framing")["id"])

    def test_a_lens_edit_changes_the_id(self):
        eng = mk(self.tmp.name, "lens", sections={"Confirmed": confirmed(12)})
        before = D["gate_state"](eng, "discovery→framing")["id"]
        (eng / "lens-outputs" / "data.md").write_text("# data\n\nC-002 novo.\n", encoding="utf-8")
        self.assertNotEqual(before, D["gate_state"](eng, "discovery→framing")["id"])


class LifeCycle(unittest.TestCase):
    """Duas invocações, uma avaliação — e a ligação diz a verdade quando o estado mexeu."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.eng = mk(self.root, "fx", sections={"Confirmed": confirmed(3)})

    def _fire(self, args):
        return run_hook({"tool_name": "Skill",
                         "tool_input": {"skill": "aisa-frame", "args": args}},
                        env_root=self.root)

    def _log(self):
        return (self.eng / "gate-log.md").read_text(encoding="utf-8")

    def test_a_first_run_writes_one_line_with_coverage(self):
        r = self._fire("--engagement fx")
        self.assertEqual(r.returncode, 0)
        lines = [l for l in self._log().splitlines() if l.startswith("2")]
        self.assertEqual(len(lines), 1)
        self.assertIn("discovery→framing", lines[0])
        self.assertIn("por código", lines[0])
        self.assertIn("override: no", lines[0])
        self.assertIn("Confirmed >= 10", lines[0])          # o vermelho é nomeado

    def test_an_override_on_the_same_state_refers_to_the_first(self):
        self._fire("--engagement fx")
        first = [l for l in self._log().splitlines() if l.startswith("2")][0]
        gid = next(c for c in first.split(" · ") if c.startswith("G-"))
        self._fire('--engagement fx --override "o sponsor aceita avançar"')
        lines = [l for l in self._log().splitlines() if l.startswith("2")]
        self.assertEqual(len(lines), 2)
        self.assertIn('override: yes "o sponsor aceita avançar"', lines[1])
        self.assertIn("refers: " + gid, lines[1])

    def test_an_override_after_the_state_moved_says_refers_none(self):
        self._fire("--engagement fx")
        (self.eng / "shared-understanding.md").write_text(
            su_text("fx", {"Confirmed": confirmed(12)}), encoding="utf-8")
        self._fire('--engagement fx --override "avançar"')
        last = [l for l in self._log().splitlines() if l.startswith("2")][-1]
        self.assertIn("refers: none", last)

    def test_the_hook_never_blocks(self):
        for args in ("--engagement fx", '--engagement fx --override "x"', "--engagement fx"):
            self.assertEqual(self._fire(args).returncode, 0)

    def test_a_non_transition_skill_is_ignored(self):
        r = run_hook({"tool_name": "Skill", "tool_input": {"skill": "aisa-round", "args": ""}},
                     env_root=self.root)
        self.assertEqual(r.returncode, 0)
        self.assertFalse((self.eng / "gate-log.md").is_file())

    def test_broken_stdin_is_fail_open(self):
        r = run_hook(None, env_root=self.root)
        self.assertEqual(r.returncode, 0)


class EngagementResolution(unittest.TestCase):
    """Escrever no projecto errado é pior do que não escrever."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_one_mounted_is_inferred_and_said_so(self):
        eng = mk(self.root, "solo", sections={"Confirmed": confirmed(12)})
        r = run_hook({"tool_name": "Skill", "tool_input": {"skill": "aisa-frame", "args": ""}},
                     env_root=self.root)
        self.assertEqual(r.returncode, 0)
        self.assertIn("engagement: only", (eng / "gate-log.md").read_text(encoding="utf-8"))

    def test_several_mounted_and_no_slug_writes_nothing(self):
        a = mk(self.root, "a", sections={"Confirmed": confirmed(12)})
        b = mk(self.root, "b", sections={"Confirmed": confirmed(12)})
        r = run_hook({"tool_name": "Skill", "tool_input": {"skill": "aisa-frame", "args": ""}},
                     env_root=self.root)
        self.assertEqual(r.returncode, 0)
        self.assertIn("ambiguous engagement", r.stderr)
        self.assertFalse((a / "gate-log.md").is_file())
        self.assertFalse((b / "gate-log.md").is_file())

    def test_the_slug_disambiguates(self):
        a = mk(self.root, "a", sections={"Confirmed": confirmed(12)})
        b = mk(self.root, "b", sections={"Confirmed": confirmed(12)})
        run_hook({"tool_name": "Skill",
                  "tool_input": {"skill": "aisa-frame", "args": "--engagement b"}},
                 env_root=self.root)
        self.assertFalse((a / "gate-log.md").is_file())
        self.assertTrue((b / "gate-log.md").is_file())

    def test_find_engagement_refuses_to_guess_when_asked_not_to(self):
        C = runpy.run_path(str(ROOT / ".claude" / "hooks" / "_common.py"))
        mk(self.root, "a")
        mk(self.root, "b")
        eng, how = C["find_engagement"](None, allow_ambiguous=False, base=self.root)
        self.assertIsNone(eng)
        self.assertEqual(how, "ambiguous")
        eng2, how2 = C["find_engagement"](None, allow_ambiguous=True, base=self.root)
        self.assertIsNotNone(eng2)
        self.assertEqual(how2, "recent")


class CommandPath(unittest.TestCase):
    """O percurso do comando, nao so a chamada sintetica com o slug ja preenchido.

    Defeito real (revisao da fase 3, 2026-09-10): os tres comandos encaminhavam apenas
    `$ARGUMENTS`. Uma invocacao normal de `/options` com varios engagements montados fazia o
    hook recusar avaliar -- correctamente -- e NENHUM `gate-log.md` era escrito. A recusa
    estava certa; faltava a resolucao do lado do comando.

    O que se pode afirmar por codigo: que o comando manda resolver, que a resolucao existe e
    devolve o que deve, e que o hook escreve quando recebe o slug. O que a suite NAO pode
    afirmar e o modelo a executar essas instrucoes -- isso e dos cenarios ponta-a-ponta.
    """

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_the_three_commands_resolve_and_pass_the_engagement(self):
        for name in ("frame", "options", "decide"):
            md = (ROOT / ".claude" / "commands" / (name + ".md")).read_text(encoding="utf-8")
            self.assertIn("--which-engagement", md, name)
            self.assertIn("--engagement <slug>", md, name)
            self.assertIn("AskUserQuestion", md, name)      # ambiguo pergunta, nao adivinha

    def _which(self, *args):
        import os
        env = dict(os.environ)
        env["AISA_ENGAGEMENTS_ROOT"] = str(self.root)
        return subprocess.run(
            [sys.executable, str(ROOT / "library" / "kernel" / "tools" / "dashboard.py"),
             "--which-engagement", *args],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            cwd=str(ROOT), env=env)

    def test_one_mounted_resolves_to_its_slug(self):
        mk(self.root, "solo", sections={"Confirmed": confirmed(12)})
        r = self._which()
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout.strip(), "solo")

    def test_several_mounted_refuses_and_lists_the_candidates(self):
        mk(self.root, "a")
        mk(self.root, "b")
        r = self._which()
        self.assertEqual(r.returncode, 4)
        self.assertEqual(r.stdout.strip(), "")
        self.assertIn("a", r.stderr)
        self.assertIn("b", r.stderr)

    def test_an_explicit_slug_resolves_even_with_several_mounted(self):
        mk(self.root, "a")
        mk(self.root, "b")
        r = self._which("--engagement", "b")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout.strip(), "b")

    def test_none_mounted_is_loud(self):
        self.assertEqual(self._which().returncode, 3)

    def test_the_resolved_slug_makes_the_hook_write(self):
        """A ponta que faltava: resolver -> passar -> o veredicto no projecto certo."""
        a = mk(self.root, "a", sections={"Confirmed": confirmed(12)})
        b = mk(self.root, "b", sections={"Confirmed": confirmed(12)})
        blind = run_hook({"tool_name": "Skill",
                          "tool_input": {"skill": "aisa-options", "args": ""}},
                         env_root=self.root)
        self.assertIn("ambiguous engagement", blind.stderr)
        self.assertFalse((a / "gate-log.md").is_file())
        slug = self._which("--engagement", "b").stdout.strip()
        run_hook({"tool_name": "Skill",
                  "tool_input": {"skill": "aisa-options",
                                 "args": "--engagement " + slug}},
                 env_root=self.root)
        self.assertTrue((b / "gate-log.md").is_file())
        self.assertFalse((a / "gate-log.md").is_file())


class Wiring(unittest.TestCase):

    def test_the_hook_is_pre_tool_use_on_skill(self):
        st = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
        pre = [h["command"] for e in st["hooks"]["PreToolUse"]
               if e.get("matcher") == "Skill" for h in e["hooks"]]
        post = [h["command"] for e in st["hooks"].get("PostToolUse", [])
                if e.get("matcher") == "Skill" for h in e["hooks"]]
        # Por FORMA, nao pela frase: a maneira de invocar mudou em R7
        # (`python "${CLAUDE_PROJECT_DIR:-.}/..."`, DEF-P1-02) e o que este teste
        # segura e o script estar registado neste evento e nao no outro.
        # `test_hook_invocation.py` e que segura a forma do comando.
        self.assertTrue(any("phase-gate-check.py" in c for c in pre), pre)
        self.assertFalse(any("phase-gate-check.py" in c for c in post), post)

    def test_the_stub_language_is_gone(self):
        for name in ("phase-gate-check.py", "synthesis-validate.py"):
            text = (ROOT / ".claude" / "hooks" / name).read_text(encoding="utf-8")
            self.assertNotIn("v0.2.0 will validate", text, name)
            self.assertNotIn("log-only", text.lower(), name)

    def test_hooks_md_describes_what_they_evaluate(self):
        md = (ROOT / ".claude" / "hooks" / "HOOKS.md").read_text(encoding="utf-8")
        self.assertNotIn("**Log only.**", md)
        self.assertIn("gate-log.md", md)
        self.assertIn("_synthesis-checks.md", md)

    def test_the_transition_skills_point_at_the_log(self):
        for name in ("aisa-frame", "aisa-options", "aisa-decide"):
            md = (ROOT / ".claude" / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("gate-log.md", md, name)

    def test_phases_md_stops_saying_warnings_only(self):
        md = (ROOT / "library" / "kernel" / "phases.md").read_text(encoding="utf-8")
        self.assertIn("evaluated** by the `phase-gate-check.py` hook", md)

    def test_the_model_exposes_the_gate_of_the_current_phase(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = mk(tmp, "m", sections={"Confirmed": confirmed(12)})
            from datetime import date
            model = D["build_model"](eng, date(2026, 9, 10))
            g = model["status"]["gates"]
            self.assertIsNotNone(g)
            self.assertEqual(g["transition"], "discovery→framing")
            self.assertTrue(all("mode" in c for c in g["criteria"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
