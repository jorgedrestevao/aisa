"""Fase 5 — os 13 cenários obrigatórios de §12.3 do refoco em decisão técnica.

Regras de desenho, de §12.1, e são o que faz destes testes utilizáveis:

  * **Por forma, nunca por frase.** Um artefacto sai na língua do pacote e um marcador
    inglês fá-lo passar em falso — foi o defeito do P-19. Onde a regra é estrutural,
    verifica-se a estrutura (o campo existe, a condição está declarada, o conjunto é
    fechado). Onde a regra é executável, corre-se o **motor** contra um fixture, que é
    prova mais forte que qualquer procura de texto.
  * **Comportamento, não vocabulário.** Onde a regra é semântica, verifica-se que a
    **declaração existe** — o eixo nomeado, a fonte da estimativa, a razão da classe
    ausente — nunca que a declaração é verdadeira. Distinguir *papel* de *pessoa* em
    texto livre é julgamento, e nem o motor nem este ficheiro o fazem.

Cada teste é um cenário da tabela, pela mesma ordem, e o seu nome diz qual.

    python .claude/tests/test_technical_decision_refocus.py
"""

import importlib.util
import io
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PP = os.path.join(ROOT, "library", "packs", "pp")
KERNEL = os.path.join(ROOT, "library", "kernel")
SKILLS = os.path.join(ROOT, ".claude", "skills")
FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures",
                        "technical-decision-refocus")

LENSES = ("business", "operations", "user", "data", "governance", "financial")

# Os oito eixos técnicos (§1.2 regra 3). Conjunto fechado: um eixo fora dele é defeito
# do emissor, e é por isso que se conta em vez de se procurar por palavras.
AXES = ("tecnologia", "padrão arquitetural", "componentes", "modelo de dados",
        "plano de imposição de permissões", "esforço de alto nível", "custo",
        "risco técnico")

# Marcadores de conjunto fechado. Tokens verbatim, nunca traduzidos: o artefacto sai na
# língua do pacote (§16.3, G1 e A2).
MARKERS = ("SIMULATED", "PACK MODEL", "ANALOGY", "ORDER OF MAGNITUDE UNAVAILABLE",
           "TO-BE DIVERGENCE")


def read(*parts):
    p = os.path.join(*parts)
    if not os.path.isfile(p):
        return ""
    with io.open(p, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def flat(text):
    """Forma normalizada. A varredura por linha não chega: na fase 3 dois veredictos
    escaparam ao grep por serem bullets partidos, e na fase 4 duas ocorrências estavam
    partidas por quebra de linha."""
    return " ".join(text.split()).lower()


def load_motor():
    path = os.path.join(KERNEL, "tools", "dashboard.py")
    spec = importlib.util.spec_from_file_location("aisa_dashboard_p5", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


D = load_motor()

STATES = read(KERNEL, "states.md")
PHASES = read(KERNEL, "phases.md")
BP_CONTRACT = read(KERNEL, "blueprint-contract.md")
SECURITY_CRAFT = read(PP, "domain-knowledge", "craft", "security-craft.md")
SECURITY_CONTROLS = read(PP, "domain-knowledge", "security", "security-controls.md")
ESTIMATION = read(PP, "domain-knowledge", "craft", "estimation-model.md")
DELIVERY = read(PP, "domain-knowledge", "craft", "delivery-conventions.md")
SQL_DELIVERY = read(PP, "domain-knowledge", "craft", "sql-delivery-conventions.md")
DECISION_TREE = read(PP, "decision-tree.md")
OUTCOME_CLASSES = read(PP, "decision-model", "outcome-classes.md")
BLOCKING_SET = read(PP, "decision-model", "blocking-set.md")
DISQUALIFIERS = read(PP, "decision-model", "composed-disqualifiers.md")
CORE = read(PP, "architecture-templates", "architecture-core.md")
F_BND = read(PP, "architecture-templates", "fragment-boundary-and-imports.md")
LENS_GOV = read(SKILLS, "lens-governance", "SKILL.md")
LENS_TECH = read(SKILLS, "lens-technology", "SKILL.md")
CHAIRMAN = read(SKILLS, "chairman-synthesis", "SKILL.md")
COMPLIANCE_MEM = read(ROOT, ".claude", "agent-memory", "_universal",
                      "compliance-officer", "universal-constraints.md")
FIXTURE = read(FIXTURES, "admission-cases.md")


def fixture_rows():
    """As linhas do fixture, parseadas pelo MOTOR — não por um parser deste ficheiro.
    Um parser próprio testaria o parser próprio."""
    _h, rows, _s, _d = D.parse_su(FIXTURE)
    return {r["id"]: r for r in rows}


class Scenarios(unittest.TestCase):
    """Um teste por linha de §12.3, pela ordem da tabela."""

    def a10(self):
        self.assertIn("### A10", CORE)
        self.assertIn("### A11", CORE)
        return flat(CORE.split("### A10", 1)[1].split("### A11", 1)[0])

    # ---------------------------------------------------------------- 1
    def test_s01_role_based_value_adjustment_never_asks_for_a_person(self):
        """Ajuste de valores por role: RBAC define role, dados, acção e imposição;
        não pergunta pessoa."""
        f = flat(SECURITY_CRAFT)
        # a matriz DERIVA-SE, e a derivação está declarada com os quatro termos
        self.assertIn("action × resource × scope × role", f)
        self.assertIn("derived from a **requirement**", f)
        # nome e cargo são hipótese, nunca autorização
        self.assertIn("a name or a job title is a hypothesis about a role", f)
        # e a imposição é na camada de dados/API — esconder ecrã não basta
        self.assertIn("authorization is enforced in the data or api layer", f)
        # a lente pergunta que PAPEL pode o quê, nunca que pessoa
        self.assertIn("never which person", flat(LENS_GOV))
        # nenhum papel começa com acesso total
        self.assertNotIn("full access to everything — every solution needs one",
                         flat(SECURITY_CRAFT))

    # ---------------------------------------------------------------- 2
    def test_s02_legacy_folder_with_no_target_contract_creates_no_row(self):
        """Pasta diária legada sem contrato no alvo: não cria `Unknown` de acesso,
        localização ou retenção."""
        # a regra vive no kernel e nas 6 lentes, pela mesma forma
        # O kernel di-lo do PROJECTO, as lentes do TRABALHO PENDENTE: dois enunciados da
        # mesma regra, e cada canal é verificado pelo seu, nunca pelo do outro.
        self.assertIn("the organisation's ignorance is not the project's work", flat(STATES))
        self.assertIn("never a question waiting on the organisation", flat(STATES))
        for name in LENSES:
            f = flat(read(SKILLS, "lens-%s" % name, "SKILL.md"))
            self.assertIn("the organisation's ignorance is not pending work", f,
                          "lens-%s não carrega a regra" % name)
            self.assertIn("describes the organisation", f)
        # e o motor confirma-o no fixture: a pergunta de localização é `cosmético`.
        # O motor normaliza a classe para ASCII, e é essa a forma que se afirma —
        # afirmar a acentuada testava o encoding deste ficheiro, não a regra.
        row = fixture_rows()["U-904"]
        self.assertEqual("cosmetico", row["swing_class"])

    # ---------------------------------------------------------------- 3
    def test_s03_required_retention_becomes_a_technical_requirement(self):
        """Retenção/auditoria explicitamente necessária: requisito técnico com dados
        abrangidos, mecanismo, retenção e custo."""
        f = flat(SECURITY_CRAFT)
        # a trilha é engajada por um requisito, e o requisito cita-se
        self.assertIn("where an audit requirement covers the action", f)
        self.assertIn("cite the requirement next to the pattern", f)
        # os quatro objectos que o requisito deve
        for owed in ("retention period", "mechanism", "cost driver"):
            self.assertIn(owed, f, "falta %r" % owed)
        # a retenção é requisito, nunca valor deste ficheiro
        self.assertIn("the retention period is a requirement, never a value this file", f)
        # e o mecanismo é do dono do controlo, não do craft
        self.assertIn("security/security-controls.md", SECURITY_CRAFT)

    # ---------------------------------------------------------------- 4
    def test_s04_a_process_without_approvals_gets_no_matrix_no_sod_no_signoff(self):
        """Processo sem aprovações: não cria matriz de approvals, SoD ou sign-off."""
        f = flat(SECURITY_CRAFT)
        # a matriz 4 é condicional, e a ausência declara-se
        self.assertIn("matrix 4 is engaged **only** where an approval workflow is behaviour",
                      f)
        self.assertIn("a process with no approvals gets no approval matrix", f)
        # SoD exige obrigação citada; sem citação não se impõe
        self.assertIn("uncited, no split is imposed", f)
        self.assertIn("never a default constraint", flat(COMPLIANCE_MEM))
        # e sign-off não sobrevive em nenhum dos dois canais
        for name, text in (("security-craft", SECURITY_CRAFT),
                           ("architecture-core", CORE),
                           ("blueprint-contract", BP_CONTRACT)):
            self.assertNotIn("sign-off", flat(text), "%s ainda pede sign-off" % name)

    # ---------------------------------------------------------------- 5
    def test_s05_an_approval_workflow_in_scope_is_modelled_as_transitions_and_roles(self):
        """Workflow de aprovação em âmbito: transições, roles e separação — só se o
        requisito pedir."""
        f = flat(SECURITY_CRAFT)
        self.assertIn("one row per transition the process actually has", f)
        self.assertIn("the role(s) the requirement authorises", f)
        # a separação é modelo de permissões, e só com a obrigação citada
        self.assertIn("record the split as a permission model", f)
        # aprovação como comportamento do processo: estados, transições, papel autorizado
        g = flat(COMPLIANCE_MEM)
        self.assertIn("the states, the transitions, the **role** authorised at each", g)
        self.assertIn("outside this engagement and no row is written", g)

    # ---------------------------------------------------------------- 6
    def test_s06_imposed_technology_generates_inside_the_boundary(self):
        """Tecnologia fixa: Options avalia padrões compatíveis; não recomenda outra
        plataforma."""
        self.assertIn("§6.2", DECISION_TREE)
        f = flat(DECISION_TREE)
        # a fronteira de geração existe e é declarada
        self.assertIn("imposed", f)
        # a lente aponta para lá em vez de repetir a regra (item 19)
        self.assertIn("decision-tree.md", LENS_TECH)
        self.assertIn("§6.2", LENS_TECH)
        # e a própria imposição é alterável — como classe 15, nunca como recomendação
        self.assertIn("viable if the rule is changed", flat(OUTCOME_CLASSES))

    # ---------------------------------------------------------------- 7
    def test_s07_a_hybrid_option_needs_the_external_boundary_permitted(self):
        """Opção híbrida: recomendável só com a fronteira externa permitida; caso
        contrário C3."""
        f = flat(LENS_TECH)
        # a fronteira de uma composição é restrição a validar, com os seus quatro objectos
        for owed in ("place", "identity", "role", "network path"):
            self.assertIn(owed, f, "a regra da fronteira não nomeia %r" % owed)
        # uma fronteira não verificada é recomendação assente em permissão de terceiro
        self.assertIn("an unverified boundary is a recommendation", f)
        # a recusa POR REGRA rende classe 15; a recusa TÉCNICA é que desqualifica
        self.assertIn("viable if the rule is changed", f)
        self.assertIn("the option is not eliminated", f)
        # o fragmento de fronteira não emite veredicto de disponibilidade
        self.assertNotIn("composition is unavailable", flat(F_BND))

    # ---------------------------------------------------------------- 8
    def test_s08_an_incompatible_org_rule_keeps_the_option_as_class_15(self):
        """Regra da organização incompatível: opção presente como «viável se a regra
        for alterada», com os campos."""
        f = flat(OUTCOME_CLASSES)
        self.assertIn("viable if the rule is changed", f)
        # os sete campos que o bloco normativo de C3 escreve (§16.3: C8 dizia seis)
        for owed in ("**rule**", "**condition**", "**impact**", "**cost**", "**risk**",
                     "**who can change it**", "**status**"):
            self.assertIn(owed, f, "a classe 15 não deve %r" % owed)
        # e nunca é seguida de classe 8: a opção fica condicional, não excluída
        self.assertIn("never followed by class 8", f)
        # e é encaminhada dos dois sítios que antes excluíam
        self.assertIn("15", flat(BLOCKING_SET))
        # falta de nome ou de maturidade não exclui: produz requisito/condição/custo/risco
        g = flat(DISQUALIFIERS)
        for gone in ("release owner → exclusion", "reconciliation owner → exclusion"):
            self.assertNotIn(gone, g)

    # ---------------------------------------------------------------- 9
    def test_s09_uncertain_but_non_decisive_volume_is_assumed_and_proceeds(self):
        """Volume incerto mas não decisivo: assume intervalo e avança."""
        # os três destinos são do kernel e das 6 lentes
        f = flat(STATES)
        self.assertIn("changes detail, configuration or a band", f)
        self.assertIn("it only settles at implementation", f)
        # e o fixture mostra o comportamento pelo motor, não por leitura:
        rows = fixture_rows()
        # a faixa vive como `Assumed` com base e condição de revisão
        self.assertEqual("Assumed", rows["A-901"]["state"])
        self.assertIn("condição de revisão", flat(rows["A-901"]["support"]))
        # e a pergunta de volume que resta é `dimensionante`, não `decisivo`
        self.assertEqual("dimensionante", rows["U-901"]["swing_class"])
        # passa a admissão: nomeia o eixo do esforço
        out = D.arbiter_declarations([rows["U-901"]], has_enq=False)
        self.assertEqual([], [e["id"] for e in out["sem_eixo"]])

    # ---------------------------------------------------------------- 10
    def test_s10_uncertain_external_identity_opens_a_decisive_question(self):
        """Identidade externa incerta: abre pergunta decisiva se alterar superfície,
        identidade ou padrão."""
        rows = fixture_rows()
        row = rows["U-902"]
        self.assertEqual("decisivo", row["swing_class"])
        # o eixo que muda é o plano de imposição — um dos oito, e está no conjunto
        self.assertIn("plano de imposição de permissões", flat(row["swing_text"]))
        # e passa a admissão inteira pelo motor: eixo, ≥2 respostas, e a 2.ª forma de (i)
        out = D.arbiter_declarations([row], has_enq=False)
        for crivo in ("sem_eixo", "sem_declaracao", "decisivo_sem_referente"):
            self.assertEqual([], [e["id"] for e in out[crivo]],
                             "U-902 assinalada em %s" % crivo)

    # ---------------------------------------------------------------- 11
    def test_s11_no_operating_model_adds_requirements_and_keeps_the_option(self):
        """Sem modelo operacional definido: opção continua comparável; acrescenta
        requisitos de telemetria, recuperação e roles."""
        a10 = self.a10()
        # A10 deve os seis objectos do modelo de operação
        for owed in ("role", "identity", "permission", "mechanism",
                     "alert destination", "recovery procedure"):
            self.assertIn(owed, a10, "A10 não deve %r" % owed)
        # o que conta como estrutural é o MODELO ausente, não o operador sem nome
        self.assertIn("operating model is absent", a10)
        self.assertIn("not named", a10)
        # e a opção não desaparece: o fragmento já não emite indisponibilidade
        self.assertNotIn("composition is unavailable", flat(F_BND))
        # o kernel diz quem é dono da definição, e que pessoa nunca é escolha estrutural
        f = flat(BP_CONTRACT)
        self.assertIn("decided by the pack's architecture template", f)
        self.assertIn("a missing *person* is never a structural choice", f)

    # ---------------------------------------------------------------- 12
    def test_s12_an_m_without_a_technical_axis_is_reclassified_in_r_f_and_o(self):
        """`Unknown` que cita `M-n` sem eixo técnico: reclassificada `cosmético` pelo
        árbitro, em ronda `R-`, `F-` **e** `O-`."""
        rows = fixture_rows()
        # as três linhas que citam um `M-n` e não nomeiam eixo, uma por prefixo de ronda
        cases = {"U-903": "R-", "U-907": "F-", "U-906": "O-"}
        for rid, prefix in cases.items():
            row = rows[rid]
            self.assertTrue(row["ronda"].startswith(prefix),
                            "%s não é ronda %s" % (rid, prefix))
            out = D.arbiter_declarations([row], has_enq=True)
            self.assertEqual([rid], [e["id"] for e in out["sem_eixo"]],
                             "%s não foi assinalada sem eixo" % rid)
        # e a cobertura: o `M-n` não dispensa o eixo, nos três escritores
        # o kernel enuncia-o como necessidade-sem-suficiência, e diz que a dispensa morreu
        f0 = flat(STATES)
        self.assertIn("necessary context and never sufficient", f0)
        self.assertIn("stand in for declaration 3 is gone", f0)
        # as 6 lentes enunciam-no como a dispensa que já não existe
        for name in LENSES:
            self.assertIn("never** waives the eixo",
                          flat(read(SKILLS, "lens-%s" % name, "SKILL.md")),
                          "lens-%s dispensa o eixo" % name)
        # `chairman-synthesis` cobre `F-` e `O-`, que é a metade que o 5f não via
        f = flat(CHAIRMAN)
        self.assertIn("f-", f)
        self.assertIn("o-", f)

    # ---------------------------------------------------------------- 13
    def test_s13_an_option_with_no_basis_declares_the_field_missing(self):
        """Opção sem base para estimativa: campo declarado em falta, nunca número
        inventado."""
        f = flat(CHAIRMAN)
        # o conjunto fechado das três fontes, mais a saída declarada
        for marker in ("simulated", "pack model", "analogy",
                       "order of magnitude unavailable"):
            self.assertIn(marker, f, "falta o marcador %r" % marker)
        # a banda, nunca o ponto
        self.assertIn("always a range", flat(ESTIMATION))
        # e o marcador é token verbatim: não traduzido em nenhum canal que o cite
        for label, text in (("chairman-synthesis", CHAIRMAN),
                            ("estimation-model", ESTIMATION)):
            if "ORDER OF MAGNITUDE" in text or "order of magnitude unavailable" in flat(text):
                self.assertIn("ORDER OF MAGNITUDE UNAVAILABLE", text,
                              "%s traduziu o marcador" % label)


class DesignRules(unittest.TestCase):
    """§12.1 — as regras de desenho, aplicadas a este próprio ficheiro e aos marcadores."""

    def test_every_closed_set_marker_is_verbatim_and_untranslated(self):
        """Um marcador que um teste lê tem de ser token verbatim: o artefacto sai na
        língua do pacote, e uma frase traduzida faz o teste passar em falso (P-19)."""
        for m in MARKERS:
            self.assertEqual(m, m.upper(), "marcador não é token verbatim: %r" % m)
        # e cada um tem um dono declarado que o escreve
        owned = flat(CHAIRMAN) + flat(STATES)
        for m in MARKERS:
            self.assertIn(m.lower(), owned, "marcador sem dono: %r" % m)

    def test_the_eight_axes_are_a_closed_set_stated_by_the_kernel(self):
        f = flat(STATES)
        for axis in AXES:
            self.assertIn(axis.lower(), f, "o kernel não enuncia o eixo %r" % axis)

    def test_the_thirteen_scenarios_are_all_covered(self):
        """Um cenário sem teste é um cenário não coberto — a contagem é a medida de
        §11.2, e vive aqui para não poder divergir dela."""
        tests = [m for m in dir(Scenarios) if re.match(r"^test_s\d\d_", m)]
        self.assertEqual(13, len(tests),
                         "cenários cobertos: %d/13 — %s" % (len(tests), sorted(tests)))
        nums = sorted(int(re.match(r"^test_s(\d\d)_", m).group(1)) for m in tests)
        self.assertEqual(list(range(1, 14)), nums, "numeração com lacuna: %s" % nums)


if __name__ == "__main__":
    unittest.main(verbosity=2)
