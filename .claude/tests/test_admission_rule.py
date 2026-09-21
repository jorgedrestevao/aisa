"""Fase 1 do refoco em decisão técnica (docs/TECHNICAL_DECISION_REFOCUS_IMPLEMENTATION_PLAN.md).

Bloco A — a admissão de uma pergunta passa a **conjunção**: `M-n` **e** ≥ 2 respostas **e** qual dos
oito eixos técnicos muda. Citar um `M-n` deixa de dispensar a consequência técnica.

**A maior parte deste módulo é executável, não textual.** Cada cenário constrói uma Shared
Understanding sintética, corre o parser e o árbitro do motor por cima dela, e verifica o que sai —
não que uma frase existe num SKILL.md. Restam os testes de prosa da penúltima classe, e existem por
uma razão só: a dispensa por `M-n` era uma **instrução**, e o único modo de provar que morreu em
cada canal é procurar a instrução antiga em cada canal. São anti-regressão, não contrato.

    python .claude/tests/test_admission_rule.py
"""

import importlib.util
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as fh:
        return fh.read()


def load_dashboard():
    path = os.path.join(ROOT, "library", "kernel", "tools", "dashboard.py")
    spec = importlib.util.spec_from_file_location("aisa_dashboard_admission", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


D = load_dashboard()

# Os oito eixos. A ordem é a do plano §1.2 regra 3 e a da regra no kernel.
AXES = ("tecnologia", "padrão arquitetural", "componentes", "modelo de dados",
        "plano de imposição de permissões", "esforço de alto nível", "custo", "risco técnico")


# ------------------------------------------------------------------ fixtures executáveis

SU_HEAD = """# Shared Understanding — fixture

> Engagement: fixture
> Última actualização: 2026-09-09T00:00:00Z

## Unknown

| id | lens | pergunta | quem responde | criticidade | custo | swing | ronda |
|----|------|----------|---------------|-------------|-------|-------|-------|
"""

# Uma SU anterior à v2.3: sem colunas `custo` e `swing`. Nenhuma linha PODE declarar nada.
SU_HEAD_LEGACY = """# Shared Understanding — fixture legado

## Unknown

| id | lens | pergunta | quem responde | criticidade | ronda |
|----|------|----------|---------------|-------------|-------|
"""


def su(*rows, **kw):
    """Uma SU sintética com as linhas dadas, já parseada pelo motor."""
    head = SU_HEAD_LEGACY if kw.get("legacy") else SU_HEAD
    _h, parsed, _s, _d = D.parse_su(head + "".join(r.rstrip() + "\n" for r in rows))
    return parsed


def unknown(uid, pergunta, swing, quem="papel de dono do processo",
            criticidade="Med", custo="email", ronda="R-01"):
    return "| %s | data | %s | %s | %s | %s | %s | %s |" % (
        uid, pergunta, quem, criticidade, custo, swing, ronda)


def ids(entries):
    return [e["id"] for e in entries]


# Frases da mesma família das cinco perguntas escritas em pilot-3 R-05 sob a regra nova.
SWING_COMPLETO = ("dimensionante: serve M-5. Se o par tem de existir, o modelo de dados ganha a "
                  "entidade «projecção emitida» e os componentes ganham a vista de comparação; se "
                  "basta a valorização fechada, nada disso entra e o esforço de alto nível desce")
SWING_SO_MECANISMO = "dimensionante: serve M-2 e confirma o mecanismo de valorização"
SWING_SEM_M = ("dimensionante: ou muda o modelo de dados, ou não muda nada de estrutural no "
               "que se vai construir")
SWING_ADMINISTRATIVO = ("dimensionante: serve M-1. Se assinar o responsável, avança; se não "
                        "assinar, fica pendente")
# Segunda forma admissível da declaração (i) — veredicto do dono, 2026-09-10. Uma pergunta
# de âmbito que nenhum `M-n` estreito serve, mas que muda o alvo.
SWING_TOBE = ("dimensionante: TO-BE DIVERGENCE — o alvo tem de decidir a cobertura. Se cobrir "
              "os três produtos, o modelo de dados ganha a dimensão produto; se cobrir um, não "
              "ganha e o esforço de alto nível desce")


class TheMotorEnforcesTheConjunction(unittest.TestCase):
    """O comportamento, corrido: SU sintética → parser → árbitro."""

    def test_a_row_that_only_cites_an_invariant_is_now_reported(self):
        """Era o coração da dispensa: `M-n` citado bastava. Deixou de bastar."""
        out = D.arbiter_declarations(su(unknown("U-001", "qual é o mecanismo?", SWING_SO_MECANISMO)))
        self.assertEqual(["U-001"], ids(out["sem_declaracao"]))
        self.assertIn("eixo", out["sem_declaracao"][0]["motivo"])
        self.assertEqual(["U-001"], ids(out["sem_eixo"]))

    def test_a_row_with_all_three_declarations_passes(self):
        out = D.arbiter_declarations(su(unknown("U-002", "guarda-se o par?", SWING_COMPLETO)))
        self.assertEqual([], out["sem_declaracao"])
        self.assertEqual([], out["sem_eixo"])
        self.assertEqual([], out["sem_citacao_m"])

    def test_two_answers_and_an_axis_but_no_invariant_is_reported(self):
        out = D.arbiter_declarations(su(unknown("U-003", "que grão?", SWING_SEM_M)))
        self.assertEqual(["U-003"], ids(out["sem_declaracao"]))
        self.assertIn("M-n", out["sem_declaracao"][0]["motivo"])
        self.assertEqual([], out["sem_eixo"], "o eixo está declarado; só falta o invariante")

    def test_the_marker_is_the_second_admissible_form_of_declaration_i(self):
        """Saída (b), 2026-09-10: um enquadramento estreito não põe a zero uma pergunta
        técnica legítima. `TO-BE DIVERGENCE` satisfaz (i) COM enquadramento declarado."""
        out = D.arbiter_declarations(su(unknown("U-005", "que cobertura?", SWING_TOBE)))
        self.assertEqual([], out["sem_declaracao"])
        self.assertEqual([], out["sem_citacao_m"], "o marcador satisfaz (i)")

    def test_the_marker_does_not_waive_the_other_two_declarations(self):
        """Não é passe: as declarações 2 e 3 continuam a ser o travão real."""
        out = D.arbiter_declarations(su(unknown(
            "U-006", "que cobertura?", "dimensionante: TO-BE DIVERGENCE — falta decidir")))
        self.assertEqual(["U-006"], ids(out["sem_declaracao"]))
        motivo = out["sem_declaracao"][0]["motivo"]
        self.assertIn(">= 2 respostas", motivo)
        self.assertIn("eixo", motivo)
        self.assertNotIn("M-n", motivo, "(i) está satisfeita pelo marcador")

    def test_the_marker_is_a_closed_set_token_not_a_translated_phrase(self):
        """P-19: a SU sai em português e uma frase traduzida faz o teste passar em falso.
        Só o token verbatim conta."""
        traduzido = ("dimensionante: divergência no alvo — se cobrir os três produtos muda o "
                     "modelo de dados, se cobrir um desce o esforço de alto nível")
        out = D.arbiter_declarations(su(unknown("U-007", "que cobertura?", traduzido)))
        self.assertEqual(["U-007"], ids(out["sem_declaracao"]))
        self.assertIn("TO-BE DIVERGENCE", out["sem_declaracao"][0]["motivo"])

    def test_with_no_enquadramento_the_invariant_half_is_not_owed(self):
        out = D.arbiter_declarations(su(unknown("U-003", "que grão?", SWING_SEM_M)),
                                     has_enq=False)
        self.assertEqual([], out["sem_declaracao"])
        self.assertFalse(out["enquadramento_declarado"])

    def test_an_administrative_question_names_no_axis(self):
        """Cenário obrigatório §12.3: `Unknown` que cita `M-n` sem eixo técnico."""
        out = D.arbiter_declarations(su(
            unknown("U-004", "quem assina a autorização?", SWING_ADMINISTRATIVO,
                    criticidade="Critical")))
        self.assertEqual(["U-004"], ids(out["sem_eixo"]))
        self.assertEqual(["U-004"], ids(out["sem_declaracao"]))

    def test_a_decisivo_without_a_referent_is_named_apart(self):
        out = D.arbiter_declarations(su(unknown(
            "U-005", "as séries chegam?",
            "decisivo: serve M-4. Se chegarem, muda o modelo de dados; se não chegarem, "
            "muda o esforço de alto nível")))
        self.assertEqual(["U-005"], ids(out["decisivo_sem_referente"]))
        self.assertEqual([], out["sem_declaracao"], "as três declarações estão lá")

    def test_a_decisivo_with_a_referent_is_clean(self):
        out = D.arbiter_declarations(su(unknown(
            "U-006", "as séries chegam?",
            "decisivo: serve M-4. Se chegarem, muda o modelo de dados; se não chegarem, "
            "elimina a opção de modelo e o esforço cai")))
        self.assertEqual([], out["decisivo_sem_referente"])
        self.assertEqual([], out["sem_declaracao"])

    def test_the_two_branch_shape_with_a_semicolon_is_not_a_false_positive(self):
        """Regressão do defeito que P-26 tornou consequente: a janela `[^|;]{2,80}` entre os
        dois «se» rejeitava a forma que as SU reais escrevem. 7 falsos positivos em
        pricing-bunkers R-01; voltou em pilot-3 R-05, onde a conjunção já não perdoa."""
        swing = ("dimensionante: serve M-1. Se o grão é a emissão, o modelo de dados ganha chave "
                 "temporal e a substituída fica retida, e os componentes ganham a leitura «qual "
                 "valia quando»; se o grão é o dia sobrescrito, nada disso entra e o esforço desce")
        out = D.arbiter_declarations(su(unknown("U-007", "que grão?", swing)))
        self.assertEqual([], out["sem_declaracao"],
                         "a frase declara os dois ramos; rejeitá-la é falso positivo")

    def test_a_pre_v23_su_is_counted_apart_and_never_read_as_a_finding(self):
        """Sem coluna `swing` nenhuma linha PODE declarar: é ausência de esquema."""
        rows = su("| U-008 | data | quem recebe o preço? | papel de dono | Critical | R-01 |",
                  legacy=True)
        out = D.arbiter_declarations(rows, has_enq=False)
        self.assertEqual(1, out["avaliadas"])
        self.assertEqual(1, out["sem_coluna_swing"])
        self.assertEqual(1, out["sem_eixo_sem_coluna"])
        self.assertEqual(len(out["sem_eixo"]), out["sem_eixo_sem_coluna"],
                         "todas as marcas vêm da coluna ausente, nenhuma é achado")

    def test_resolved_and_withdrawn_rows_are_not_evaluated(self):
        rows = su(
            unknown("U-009", "pergunta fechada", SWING_SO_MECANISMO,
                    ronda="R-01 — resolved → C-010"),
            unknown("U-010", "pergunta retirada", SWING_SO_MECANISMO,
                    ronda="R-01 — retirada P-21 (fora de âmbito)"),
            unknown("U-011", "pergunta viva", SWING_SO_MECANISMO))
        out = D.arbiter_declarations(rows)
        self.assertEqual(1, out["avaliadas"])
        self.assertEqual(["U-011"], ids(out["sem_declaracao"]))

    def test_the_round_filter_reads_only_the_round_just_run(self):
        rows = su(unknown("U-012", "antiga", SWING_SO_MECANISMO, ronda="R-01"),
                  unknown("U-013", "desta ronda", SWING_SO_MECANISMO, ronda="R-02"))
        out = D.arbiter_declarations(rows, ronda="R-02")
        self.assertEqual(1, out["avaliadas"])
        self.assertEqual(["U-013"], ids(out["sem_declaracao"]))

    def test_each_of_the_eight_axes_is_recognised_on_its_own(self):
        """Um eixo declarado sozinho basta — não se exige a lista toda."""
        for axis in AXES:
            swing = ("dimensionante: serve M-1. Se for por A, muda o %s; se for por B, "
                     "não muda" % axis)
            out = D.arbiter_declarations(su(unknown("U-014", "?", swing)))
            self.assertEqual([], out["sem_eixo"], "eixo não reconhecido: %s" % axis)

    def test_the_motor_publishes_its_own_limits(self):
        out = D.arbiter_declarations(su())
        self.assertIn("PRESENCA de declaracao", out["julgamento"])
        self.assertIn("ACEITES por desenho", out["falsos_negativos"])
        self.assertIn("eixo", out["regex"])
        self.assertIn("nao dispensa", out["conjuncao"])


class TheDowngradeIsBoundedInBehaviour(unittest.TestCase):
    """A descida de `criticidade` é consequência da reclassificação, nunca opinião. O motor
    NÃO a executa — é edição de linha, e o motor não edita. O que se verifica aqui é que ele
    entrega ao árbitro o que este precisa para decidir, e que não toca em nada."""

    def test_the_class_travels_with_the_finding_so_the_arbiter_knows_what_to_lower(self):
        rows = su(unknown("U-015", "?", "cosmético: não muda nada", criticidade="Low"),
                  unknown("U-016", "?", SWING_SO_MECANISMO, criticidade="Critical"))
        out = D.arbiter_declarations(rows)
        classes = {e["id"]: e["swing_class"] for e in out["sem_declaracao"]}
        # o motor normaliza o token sem acento; asserta-se o vocabulário dele, não o da prosa
        self.assertEqual({"U-015": "cosmetico", "U-016": "dimensionante"}, classes)

    def test_the_motor_never_edits_criticidade_nor_swing(self):
        rows = su(unknown("U-017", "?", SWING_SO_MECANISMO, criticidade="Critical"))
        before = (rows[0]["criticidade"], rows[0]["swing_class"])
        D.arbiter_declarations(rows)
        self.assertEqual(before, (rows[0]["criticidade"], rows[0]["swing_class"]),
                         "o motor verifica presença; não julga e não edita")


class TheWaiverIsGoneFromEveryChannel(unittest.TestCase):
    """Anti-regressão textual — e só. A dispensa era uma instrução escrita; o único modo de
    provar que morreu em cada canal é procurar a instrução antiga em cada canal."""

    CHANNELS = {
        "kernel": ("library", "kernel", "states.md"),
        "CLAUDE.md": ("CLAUDE.md",),
        "aisa-round": (".claude", "skills", "aisa-round", "SKILL.md"),
        "chairman-synthesis": (".claude", "skills", "chairman-synthesis", "SKILL.md"),
        "aisa-answer": (".claude", "skills", "aisa-answer", "SKILL.md"),
        "aisa-capture": (".claude", "skills", "aisa-capture", "SKILL.md"),
        "lens-business": (".claude", "skills", "lens-business", "SKILL.md"),
        "lens-operations": (".claude", "skills", "lens-operations", "SKILL.md"),
        "lens-user": (".claude", "skills", "lens-user", "SKILL.md"),
        "lens-data": (".claude", "skills", "lens-data", "SKILL.md"),
        "lens-governance": (".claude", "skills", "lens-governance", "SKILL.md"),
        "lens-financial": (".claude", "skills", "lens-financial", "SKILL.md"),
    }

    def test_no_channel_still_waives_or_offers_the_choice(self):
        for name, parts in self.CHANNELS.items():
            text = read(*parts)
            self.assertNotIn("waived when it cites an `M-n`", text, name)
            self.assertNotIn("cites an `M-n` **or** its `swing` names", text, name)
            self.assertNotIn("Divergence test before every", text, name)

    def test_every_channel_names_the_eight_axes(self):
        for name, parts in self.CHANNELS.items():
            flat = " ".join(read(*parts).split())
            for axis in AXES:
                self.assertIn(axis, flat, "%s não nomeia o eixo %s" % (name, axis))

    def test_the_two_writers_outside_the_round_are_covered(self):
        """`chairman-synthesis` (`F-`/`O-`) e `/answer` nunca passavam pelo árbitro."""
        chair = " ".join(read(".claude", "skills", "chairman-synthesis", "SKILL.md").split())
        self.assertIn("`F-` and `O-` rounds are arbitrated here", chair)
        answer = " ".join(read(".claude", "skills", "aisa-answer", "SKILL.md").split())
        self.assertIn("passes the same admission rule", answer)

    def test_every_channel_carries_the_second_admissible_form(self):
        """Um canal esquecido repõe o portão antigo — o modo de falha do plano §2."""
        for name, parts in self.CHANNELS.items():
            if name == "aisa-capture":
                continue  # não reafirma a declaração (i); só preça (ii) e (iii)
            self.assertIn("TO-BE DIVERGENCE", read(*parts), name)

    def test_the_lenses_do_not_turn_the_organisation_gap_into_pending_work(self):
        """B2.1, a metade que a fase 1 não fez: a lente escreve o facto técnico."""
        for lens in ("business", "operations", "user", "data", "governance", "financial"):
            flat = " ".join(read(".claude", "skills", "lens-" + lens, "SKILL.md").split())
            self.assertIn("the organisation's ignorance is not pending work", flat, lens)
            self.assertIn("that is a **requirement** of the to-be", flat, lens)

    def test_the_lenses_stopped_restating_the_admission_rule_in_their_steps(self):
        """Uma regra em dois sítios diverge. O passo 5 aponta; a regra dura enuncia."""
        for lens in ("business", "operations", "user", "data", "governance", "financial"):
            flat = " ".join(read(".claude", "skills", "lens-" + lens, "SKILL.md").split())
            self.assertNotIn("passes admission (Hard rule 7)", flat, lens)
            self.assertIn("passes admission, whole, as the Hard rules state it", flat, lens)

    def test_the_kernel_owns_the_organisation_gap_rule(self):
        states = " ".join(read("library", "kernel", "states.md").split())
        self.assertIn("The organisation's ignorance is not the project's work", states)
        self.assertIn("two admissible forms", states)

    def test_the_sixth_sanctioned_edit_is_declared_where_edits_are_declared(self):
        states = " ".join(read("library", "kernel", "states.md").split())
        self.assertIn("Sanctioned edits to existing rows are exactly six", states)
        self.assertIn("never upwards", states)


class OrganisationalGapsProduceRequirementsNotExclusions(unittest.TestCase):
    """C7 — as três linhas do registo composto que contradiziam o `blocking-set`."""

    COMPOSED = read("library", "packs", "pp", "decision-model", "composed-disqualifiers.md")

    def row(self, row_id):
        found = [ln for ln in self.COMPOSED.splitlines() if ln.startswith("| **%s**" % row_id)]
        self.assertEqual(1, len(found), row_id)
        return found[0]

    def test_the_three_rows_no_longer_exclude(self):
        for row_id in ("CD-02", "CD-08", "CD-09"):
            ln = self.row(row_id)
            self.assertNotIn("Poor fit — excluded, whole scope", ln, row_id)
            self.assertIn("**Fit with constraints**", ln, row_id)
            self.assertIn("`Risky` row", ln, row_id)

    def test_each_row_points_at_the_blocking_set_entry_it_now_agrees_with(self):
        for row_id, entry in {"CD-02": "B-17", "CD-08": "B-02", "CD-09": "B-26"}.items():
            self.assertIn(entry, self.row(row_id), "%s não cita %s" % (row_id, entry))

    def test_a_name_is_not_a_participating_condition(self):
        self.assertNotIn("named operator", self.row("CD-02"))
        self.assertNotIn("reconciliation owner", self.row("CD-08"))

    def test_technical_blocking_is_untouched(self):
        flat = " ".join(self.COMPOSED.split())
        self.assertIn("seven technical axes", flat)
        self.assertIn("neither is touched here", flat)


if __name__ == "__main__":
    unittest.main(verbosity=2)
