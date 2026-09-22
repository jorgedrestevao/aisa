# -*- coding: utf-8 -*-
"""U01-U05 — projeccoes e UX de todo o workflow (P7).

LIMITE DECLARADO: o caso U01 pede «tempo observado registado» com um operador humano.
Isso NAO foi feito e nao se inventa. O que se testa aqui e o MECANISMO — que a explicacao
existe, e utilizavel sem ids internos e nomeia fase, bloqueio e proximo passo. O tempo de
compreensao por um operador real fica por medir, e o relatorio da fase di-lo."""
import json
import os
import re
import runpy
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "library" / "kernel" / "tools"
P = runpy.run_path(str(TOOLS / "projection.py"))
O = runpy.run_path(str(TOOLS / "operation.py"))
G = runpy.run_path(str(TOOLS / "graph.py"))
_MIG = runpy.run_path(str(TOOLS / "migrate.py"))

SU = """> Fase actual: Discovery

## Confirmed

| id | lens | claim | evidência | verificado_em | validade | ronda |
|---|---|---|---|---|---|---|
| C-001 | data | Base partilhada | inicial | 2026-09-01 | organizacional | R-01 |

## Assumed

| id | lens | claim | base da assumption | verificado_em | validade | ronda |
|---|---|---|---|---|---|---|

## Unknown

| id | lens | pergunta | quem responde | criticidade | custo | swing | ronda |
|---|---|---|---|---|---|---|---|
| U-001 | data | Quem e o dono da base? | role: dono dos dados | Critical | documento | dimensionante: muda o modelo de dados | R-01 |
| U-002 | ops | Qual a cor do botao? | role: Operacoes | Low | email | so muda detalhe | R-01 |

## Conflicted

| id | lens | conflito | partes | criticidade | ronda |
|---|---|---|---|---|---|

## Risky

| id | lens | risco | impacto | mitigação proposta | ronda |
|---|---|---|---|---|---|
"""


def new_eng(tmp, name="eng"):
    eng = Path(tmp) / name
    eng.mkdir(parents=True, exist_ok=True)
    (eng / "shared-understanding.md").write_text(SU, encoding="utf-8", newline="\n")
    (eng / "answers.md").write_text("# Respostas\n", encoding="utf-8", newline="\n")
    (eng / "decisions.md").write_text("# Decisoes\n", encoding="utf-8", newline="\n")
    (eng / "_state.json").write_text(
        '{"phase":"discovery","round":"R-01","engagement":"eng","pack":"pp"}\n',
        encoding="utf-8", newline="\n")
    (eng / "context.json").write_text('{}\n', encoding="utf-8", newline="\n")
    # Nasce com grafo, como o `/start` o deixa desde P7.5 §W8 (passo 9c). Sem isto a
    # fixture modelava um engagement que hoje nao existe — e que, desde que `LEGACY_MODE`
    # bloqueia, nao avancaria: o bloqueio de topo seria a ausencia de grafo, e nao o que
    # cada caso aqui quer exercer.
    _MIG["init"](eng)
    return eng


class U01_OperadorNovo(unittest.TestCase):
    """Pedir fase, bloqueio e proximo passo -> explicacao utilizavel SEM schema/grafo.

    A parte humana do caso — tempo observado — NAO foi feita. Ver o cabecalho."""

    def test_the_explanation_names_phase_blocker_and_next_step(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = P["explain"](new_eng(tmp))["text"]
        for needle in ("Onde estamos:", "O que falta:", "A seguir:"):
            self.assertIn(needle, out, "a explicacao nao tem `{}`".format(needle))

    def test_it_carries_no_schema_or_graph_vocabulary(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = P["explain"](new_eng(tmp))["text"]
        for forbidden in ("schema_version", "graph.jsonl", "_graph", "sha256",
                          "fingerprint", "operation_id", "jsonl", "node", "edge"):
            self.assertNotIn(forbidden, out,
                             "vocabulario interno `{}` chegou ao operador".format(forbidden))

    def test_an_id_never_stands_as_the_subject_of_a_line(self):
        """P-13 do CLAUDE.md: o id vai entre parenteses, depois da frase. Nunca sozinho."""
        with tempfile.TemporaryDirectory() as tmp:
            out = P["explain"](new_eng(tmp))["text"]
        for line in out.splitlines():
            body = line.split(":", 1)[-1].strip()
            self.assertFalse(re.match(r"^[CAUXRDF]-\d+\b", body),
                             "linha comeca por um id: {!r}".format(line))

    def test_the_blocker_is_the_critical_one_not_the_low_one(self):
        with tempfile.TemporaryDirectory() as tmp:
            st = P["operational_state"](new_eng(tmp))
        self.assertTrue(st["blockers"])
        self.assertIn("U-001", st["blockers"][0]["what"])

    def test_the_human_timing_is_not_claimed(self):
        """Guarda contra o proprio relatorio: nada aqui produz tempo observado."""
        with tempfile.TemporaryDirectory() as tmp:
            st = P["operational_state"](new_eng(tmp))
        self.assertNotIn("observed_seconds", st)
        self.assertNotIn("comprehension_time", st)


class U02_GateBloqueado(unittest.TestCase):
    """Tentar avancar sem evidencia material obrigatoria ->
    bloqueio explica MOTIVO e ACCAO; fase INALTERADA."""

    def test_the_gate_is_closed_with_a_critical_open(self):
        with tempfile.TemporaryDirectory() as tmp:
            st = P["operational_state"](new_eng(tmp))
        self.assertFalse(st["gate"]["open"])

    def test_every_blocker_has_all_four_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            st = P["operational_state"](new_eng(tmp))
        for b in st["blockers"]:
            for field in ("what", "why_it_matters", "evidence_needed", "action"):
                self.assertTrue(b.get(field),
                                "bloqueio sem `{}`: {}".format(field, b))

    def test_the_action_is_a_command_the_operator_can_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            st = P["operational_state"](new_eng(tmp))
        self.assertTrue(st["blockers"][0]["action"].startswith("/"),
                        "a accao nao e um comando")

    def test_the_phase_is_untouched_by_reading(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            before = (eng / "_state.json").read_text(encoding="utf-8")
            P["operational_state"](eng)
            P["explain"](eng)
            self.assertEqual((eng / "_state.json").read_text(encoding="utf-8"), before,
                             "consultar o estado mudou a fase")

    def test_a_pending_operation_closes_the_gate_before_any_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            O["_atomic_write"](O["pending_path"](eng), json.dumps(
                {"intent_version": 1, "operation_id": "x", "after": {"a": "b"}}))
            st = P["operational_state"](eng)
        self.assertFalse(st["gate"]["open"])
        self.assertEqual(st["blockers"][0]["kind"], "PENDING_OPERATION")
        self.assertIn("recover", st["blockers"][0]["action"])


class U03_IncertezaNaoBloqueante(unittest.TestCase):
    """Unknown de baixo impacto permitido -> avanco quando permitido; incerteza VISIVEL."""

    def test_the_low_impact_unknown_is_not_a_blocker(self):
        with tempfile.TemporaryDirectory() as tmp:
            st = P["operational_state"](new_eng(tmp))
        blocked = " ".join(b["what"] for b in st["blockers"])
        self.assertNotIn("U-002", blocked, "um Unknown de baixo impacto bloqueou")

    def test_but_it_stays_visible(self):
        with tempfile.TemporaryDirectory() as tmp:
            st = P["operational_state"](new_eng(tmp))
        ids = {u["id"] for u in st["visible_uncertainty"]}
        self.assertIn("U-002", ids, "a incerteza nao bloqueante desapareceu da vista")

    def test_visibility_is_stated_not_implied(self):
        with tempfile.TemporaryDirectory() as tmp:
            st = P["operational_state"](new_eng(tmp))
        u = [x for x in st["visible_uncertainty"] if x["id"] == "U-002"][0]
        self.assertIn("nao bloqueia", u["note"])

    def test_the_explanation_mentions_it_without_drowning_the_blocker(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = P["explain"](new_eng(tmp))["text"]
        self.assertIn("sem bloquear", out)


class U04_ComandosCompletos(unittest.TestCase):
    """Exercitar o workflow -> metodologia, historico, versoes e aprovacoes PRESERVADOS."""

    ENTRYPOINTS = ["start", "orient", "resume", "status", "answer", "frame", "options",
                   "decide", "premortem", "simulate", "synthesize", "blueprint",
                   "render", "revisit"]

    def test_every_entry_point_the_plan_names_exists(self):
        cmds = {p.stem for p in (ROOT / ".claude" / "commands").glob("*.md")}
        skills = {p.parent.name for p in (ROOT / ".claude" / "skills").glob("*/SKILL.md")}
        for name in self.ENTRYPOINTS:
            self.assertTrue(name in cmds or "aisa-" + name in skills,
                            "ponto de entrada `{}` do mapa P1 nao existe".format(name))

    def test_the_projection_never_invents_a_percentage(self):
        with tempfile.TemporaryDirectory() as tmp:
            st = P["operational_state"](new_eng(tmp))
        blob = json.dumps(st, ensure_ascii=False)
        self.assertNotIn("progress_pct", blob)
        self.assertNotIn("completion", blob)

    def test_no_resolve_or_advance_command_was_invented(self):
        """O plano proibe duplicar `/resolve` e `/advance` so porque o doador os tem."""
        cmds = {p.stem for p in (ROOT / ".claude" / "commands").glob("*.md")}
        self.assertNotIn("resolve", cmds)
        self.assertNotIn("advance", cmds)

    def test_reading_the_projection_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            before = {p.name: p.read_bytes() for p in eng.iterdir() if p.is_file()}
            P["operational_state"](eng)
            after = {p.name: p.read_bytes() for p in eng.iterdir() if p.is_file()}
            self.assertEqual(before, after, "consultar a projeccao escreveu")


class U05_Dashboard(unittest.TestCase):
    """Mutar por SUBPROCESSO e consultar -> projeccao actualizada ou indicada STALE;
    o gate usa a autoridade actual."""

    def test_a_missing_projection_is_reported_not_guessed(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = P["projection_freshness"](new_eng(tmp))
        self.assertFalse(f["exists"])
        self.assertFalse(f["stale"])

    def test_a_subprocess_mutation_makes_the_projection_stale(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            (eng / "dashboard.html").write_text("<html>velho</html>", encoding="utf-8")
            time.sleep(0.02)
            code = ("import runpy;O=runpy.run_path(r'{}');"
                    "O['run'](r'{}','op-sp',{{'answers.md':'novo\\n'}})").format(
                TOOLS / "operation.py", eng)
            r = subprocess.run([sys.executable, "-c", code], capture_output=True,
                               text=True, timeout=60)
            self.assertEqual(r.returncode, 0, r.stderr)
            f = P["projection_freshness"](eng)
        self.assertTrue(f["stale"], "mutacao por subprocesso nao marcou a projeccao stale")
        self.assertEqual(f["newer_authority"], "answers.md")

    def test_stale_is_not_gate_truth(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            (eng / "dashboard.html").write_text("<html>velho</html>", encoding="utf-8")
            time.sleep(0.02)
            (eng / "shared-understanding.md").write_text(SU + "\n", encoding="utf-8")
            st = P["operational_state"](eng)
        self.assertTrue(st["projection"]["stale"])
        self.assertIn("NAO e verdade de gate", st["projection"]["detail"])

    def test_the_gate_consults_the_full_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            st = P["operational_state"](new_eng(tmp))
        self.assertEqual(set(st["gate"]["consulted"]),
                         {"criterios de fase", "operacao pendente", "espelho do grafo"})

    def test_a_fresh_projection_is_reported_fresh(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = new_eng(tmp)
            time.sleep(0.02)
            (eng / "dashboard.html").write_text("<html>novo</html>", encoding="utf-8")
            f = P["projection_freshness"](eng)
        self.assertFalse(f["stale"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
