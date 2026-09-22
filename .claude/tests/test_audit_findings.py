# -*- coding: utf-8 -*-
"""F01-F11 — os defeitos que a auditoria externa de `212cdc6` encontrou.

Auditoria independente ao commit `212cdc668d4cd9f55d7f550d4414bfb1653e3312`, 22-09-2026:
556 ficheiros versionados, hashes verificados, nove cenários adversariais sobre os módulos
reais. Reproduzidos aqui contra a mesma árvore: **nove em nove idênticos**, campo a campo,
incluindo digests. Não há falso positivo nenhum na lista.

Estes casos nascem **vermelhos**, de propósito. Cada um fixa um comportamento observado, não
uma teoria — e enquanto a correcção não existir, falham. É a única forma de garantir que
nenhum volta em silêncio, e é exactamente o que a suite existente não fazia: os 25 casos do
coordenador passavam com a exclusão partida, porque exerciam o ramo e não a corrida.

Dois dos defeitos são desta sessão (F05/F06 do W3-W5, F08 do W8, com uma hora de vida). Um
terceiro, F01, é a mesma classe que o W7 corrigiu no lock (`_held_by` distingue vazio de
ilegível) e que ninguém levou ao marcador de pendência.

F11 é o que mais custa admitir: a suite só é verde nesta máquina. `projects/` é gitignored e
`test_a_pre_v23_su_still_exists_untouched` depende dele, por isso num clone limpo falha
sempre — e todos os «0 falhas reais» desta sessão foram medidos com material privado
presente."""
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


def eng_migrado(tmp, su=None):
    """Um engagement real: SU com uma linha crítica aberta, já migrado."""
    eng = FIX["make"](tmp, su or FIX["NOVO"])
    M["apply"](eng)
    return eng


# =============================================================================
# F01 · P1 — pendência corrompida tratada como ausência
# =============================================================================

class F01_MarcadorIlegivel(unittest.TestCase):
    """`_read_json` devolve `None` para ausente E para ilegível. O marcador de pendência é
    a barreira; um marcador que não se entende não pode valer por «não há»."""

    MAUS = {"truncado": "{broken", "nulo": "null", "vazio": "{}",
            "lista": "[1, 2, 3]", "texto": "isto nao e json"}

    def _com_marcador(self, tmp, corpo):
        eng = Path(tmp) / "eng"
        (eng / "_ops").mkdir(parents=True)
        (eng / "shared-understanding.md").write_text("# SU\n", encoding="utf-8")
        O["pending_path"](eng).write_text(corpo, encoding="utf-8")
        return eng

    def test_an_unreadable_marker_never_reads_clean(self):
        for nome, corpo in self.MAUS.items():
            with self.subTest(marcador=nome), tempfile.TemporaryDirectory() as tmp:
                st = O["status"](self._com_marcador(tmp, corpo))
                self.assertNotEqual(st["state"], O["CLEAN"],
                                    "marcador `%s` leu-se como limpo" % nome)

    def test_an_unreadable_marker_closes_the_gate(self):
        for nome, corpo in self.MAUS.items():
            with self.subTest(marcador=nome), tempfile.TemporaryDirectory() as tmp:
                eng = self._com_marcador(tmp, corpo)
                self.assertFalse(O["gate_open"](eng),
                                 "marcador `%s` deixou o gate aberto" % nome)

    def test_an_unreadable_marker_refuses_a_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._com_marcador(tmp, "{broken")
            with self.assertRaises(O["OperationError"]) as ctx:
                O["run"](eng, "qualquer", {"a.txt": "novo"})
        self.assertIn(ctx.exception.code, ("PENDING_EXISTS", "PENDING_UNREADABLE"))

    def test_recovery_reports_the_problem_and_keeps_the_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._com_marcador(tmp, "{broken")
            with self.assertRaises(O["OperationError"]) as ctx:
                O["recover"](eng)
            self.assertEqual(O["pending_path"](eng).read_text(encoding="utf-8"), "{broken",
                             "a recuperação apagou o marcador que não conseguiu ler")
        self.assertEqual(ctx.exception.code, "PENDING_UNREADABLE")

    def test_the_bootstrap_is_not_ready_over_an_unreadable_marker(self):
        """Sobre um engagement MIGRADO, senão o que bloqueia é a ausência de grafo e o caso
        passava pela razão errada — medido: com grafo e marcador ilegível, `ready=True` e
        zero limitações."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_migrado(tmp)
            O["pending_path"](eng).write_text("{broken", encoding="utf-8")
            boot = B["bootstrap"](eng)
        self.assertFalse(boot["ready"],
                         "marcador ilegível num engagement migrado deixou o kernel pronto")
        self.assertNotIn("LEGACY_MODE", [l["code"] for l in boot["limitations"]],
                         "o caso está a medir a ausência de grafo, não o marcador")


# =============================================================================
# F02 · P1 — o leitor aceita uma escrita parcial começada depois da verificação
# =============================================================================

class F02_LeitorContraEscritaEmCurso(unittest.TestCase):
    """`bootstrap` verifica a pendência e só depois lê o conteúdo, sem exclusão. Entre as
    duas coisas cabe uma publicação inteira — e o snapshot sai com autoridades de revisões
    diferentes, a dizer `ready`."""

    def _leitura_com_escritor_a_meio(self, eng):
        """Força a ordem problemática: a escrita começa DEPOIS do `status` do bootstrap."""
        bg = B["bootstrap"].__globals__
        og = O["run"].__globals__
        snap_real, pub_real = bg["snapshot"], og["_publish"]

        def publica_e_morre(e, intent):
            O["_atomic_write"](e / "answers.md", "resposta a meio")
            raise RuntimeError("interrupção injectada")

        # A escrita entra UMA vez. Desde que a leitura valida a revisão (F02), o
        # `snapshot` é chamado mais do que uma vez por leitura — injectar sempre punha o
        # escritor a bater na sua própria pendência, que é outro cenário.
        injectado = []

        def snapshot_com_escritor(e):
            if not injectado:
                injectado.append(True)
                og["_publish"] = publica_e_morre
                try:
                    O["run"](e, "escritor-em-corrida",
                             {"answers.md": "resposta a meio",
                              "decisions.md": "decisao nova"})
                except RuntimeError:
                    pass
                finally:
                    og["_publish"] = pub_real
            return snap_real(e)

        bg["snapshot"] = snapshot_com_escritor
        try:
            return B["bootstrap"](eng)
        finally:
            bg["snapshot"] = snap_real

    def test_a_read_that_straddles_a_publication_is_never_declared_ready(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_migrado(tmp)
            boot = self._leitura_com_escritor_a_meio(eng)
            real = O["status"](eng)["state"]
        self.assertEqual(real, O["PENDING_OPERATION"], "o cenário não montou a corrida")
        self.assertFalse(boot["ready"],
                         "leu por cima de uma publicação a meio e declarou-se pronto")

    def test_it_does_not_report_a_clean_operation_that_is_pending(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_migrado(tmp)
            boot = self._leitura_com_escritor_a_meio(eng)
        self.assertNotEqual(boot["operation"]["state"], O["CLEAN"],
                            "reportou operação limpa sobre uma pendência real")


# =============================================================================
# F03 · P1 — a recuperação publica staging corrompido antes de o validar
# =============================================================================

class F03_RecuperacaoValidaAntesDePublicar(unittest.TestCase):
    """`recover` verifica que o staging EXISTE; não que os bytes são os prometidos. Publica
    primeiro, verifica depois — e a base válida já foi por cima."""

    def _pendencia_por_publicar(self, tmp, original="original"):
        eng = Path(tmp) / "eng"
        eng.mkdir()
        (eng / "a.txt").write_text(original, encoding="utf-8", newline="\n")
        og = O["run"].__globals__
        pub_real = og["_publish"]
        og["_publish"] = lambda *a: (_ for _ in ()).throw(RuntimeError("antes de publicar"))
        try:
            O["run"](eng, "staging-partido", {"a.txt": "pretendido"})
        except RuntimeError:
            pass
        finally:
            og["_publish"] = pub_real
        return eng

    def test_a_corrupted_staging_leaves_every_target_untouched(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._pendencia_por_publicar(tmp)
            intent = O["read_pending"](eng)
            (eng / intent["staging"] / "a.txt").write_text("CORROMPIDO", encoding="utf-8")
            with self.assertRaises(O["OperationError"]):
                O["recover"](eng)
            depois = (eng / "a.txt").read_text(encoding="utf-8")
        self.assertEqual(depois, "original",
                         "a recuperação destruiu a base válida com bytes que não validou")

    def test_it_names_the_file_it_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._pendencia_por_publicar(tmp)
            intent = O["read_pending"](eng)
            (eng / intent["staging"] / "a.txt").write_text("CORROMPIDO", encoding="utf-8")
            with self.assertRaises(O["OperationError"]) as ctx:
                O["recover"](eng)
        self.assertIn("a.txt", json.dumps(ctx.exception.detail, ensure_ascii=False))

    def test_the_pending_marker_survives(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._pendencia_por_publicar(tmp)
            intent = O["read_pending"](eng)
            (eng / intent["staging"] / "a.txt").write_text("CORROMPIDO", encoding="utf-8")
            try:
                O["recover"](eng)
            except O["OperationError"]:
                pass
            self.assertIsNotNone(O["read_pending"](eng))

    def test_an_intact_staging_still_recovers(self):
        """O controlo. Uma validação que recusasse tudo não seria uma validação."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._pendencia_por_publicar(tmp)
            out = O["recover"](eng)
            depois = (eng / "a.txt").read_text(encoding="utf-8")
        self.assertEqual(out["result"], "rolled_forward")
        self.assertEqual(depois, "pretendido")


# =============================================================================
# F04 · P1 — uma resolução apaga uma escrita concorrente no grafo
# =============================================================================

class F04_PrecondicaoSobreTudoOQueSeEscreve(unittest.TestCase):
    """`plan` escreve o GRAFO INTEIRO, mas só exige os digests da SU e do answers. Quem
    escreveu no grafo entre o planeamento e a publicação desaparece, com recibo `committed`."""

    def _plano_e_escrita_concorrente(self, eng):
        plano = R["plan"](eng, row_id="U-001", answer_text="Equipa de dados",
                          answered_by={"role": "dono dos dados"},
                          locator="answers.md#U-001")
        st = G["read"](eng)
        extra = {"id": "EXTRA", "type": "claim",
                 "props": {"state": "Assumed", "text": "facto concorrente"},
                 "provenance": {}}
        O["run"](eng, "grafo-paralelo", G["write_set"](st["nodes"] + [extra], st["edges"]))
        return plano

    def test_a_concurrent_graph_write_is_never_silently_erased(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_migrado(tmp)
            plano = self._plano_e_escrita_concorrente(eng)
            try:
                O["run"](eng, plano["operation_id"], plano["write_set"],
                         expected=plano["expected"])
                recusado = None
            except O["OperationError"] as exc:
                recusado = exc.code
            sobrevive = any(n["id"] == "EXTRA" for n in G["read"](eng)["nodes"])
        if recusado is None:
            self.assertTrue(sobrevive,
                            "publicou por cima de uma escrita concorrente e chamou-lhe "
                            "sucesso")
        else:
            self.assertEqual(recusado, "BASE_CHANGED",
                             "recusou por um motivo que não é a base ter mudado")

    def test_the_plan_declares_every_file_it_writes_as_a_precondition(self):
        """A causa, directamente: o que se escreve tem de estar no que se exige."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_migrado(tmp)
            plano = R["plan"](eng, row_id="U-001", answer_text="Equipa de dados",
                              answered_by={"role": "dono dos dados"},
                              locator="answers.md#U-001")
        em_falta = sorted(set(plano["write_set"]) - set(plano["expected"]))
        self.assertEqual(em_falta, [],
                         "escreve sem precondição: " + ", ".join(em_falta))


# =============================================================================
# F05 · P1 — divergência de autoridade só bloqueia na projecção
# =============================================================================

class F05_AMesmaAutoridadeEmTodasAsVias(unittest.TestCase):
    """A projecção bloqueia sobre `MIRROR_DRIFT`; o bootstrap devolve `ready` sem uma única
    limitação. Duas respostas incompatíveis para o mesmo estado — e `resolve.apply` e o
    guarda confiam na que não aplica a regra."""

    def _com_drift(self, tmp):
        eng = eng_migrado(tmp)
        su = eng / "shared-understanding.md"
        su.write_text(su.read_text(encoding="utf-8").replace("| Critical |", "| Low |"),
                      encoding="utf-8", newline="\n")
        return eng

    def test_material_drift_stops_the_bootstrap_too(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._com_drift(tmp)
            vista = P["operational_state"](eng)
            boot = B["bootstrap"](eng)
        self.assertTrue([d for d in vista["drift"] if d["code"] == "MIRROR_DRIFT"],
                        "o cenário não produziu divergência")
        self.assertFalse(boot["ready"],
                         "o bootstrap ignora a divergência que a projecção bloqueia")

    def test_the_same_state_gets_the_same_answer_everywhere(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = self._com_drift(tmp)
            boot_aberto = B["gate_open"](B["bootstrap"](eng))
            projeccao_aberta = P["operational_state"](eng)["gate"]["open"]
        self.assertEqual(boot_aberto, projeccao_aberta,
                         "o gate do bootstrap e o da projecção discordam sobre o mesmo "
                         "engagement")

    def test_text_only_drift_still_only_informs(self):
        """A decisão que fica: texto informa, campos materiais bloqueiam."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_migrado(tmp)
            su = eng / "shared-understanding.md"
            su.write_text(su.read_text(encoding="utf-8").replace("Quem e o dono?",
                                                                 "Quem e o dono disto?"),
                          encoding="utf-8", newline="\n")
            boot = B["bootstrap"](eng)
        self.assertTrue(boot["ready"],
                        "divergência só de texto passou a bloquear — não era isso que "
                        "estava decidido")


# =============================================================================
# F06 · P1 — a resposta resolve a SU e deixa o espelho anterior aberto
# =============================================================================

class F06_OEspelhoFechaComALinha(unittest.TestCase):
    """`/answer` marca `resolved ->` na SU e deixa o nó do grafo com `resolved=false`. O
    contexto volta a mostrar a pergunta como aberta, e a divergência é criada pela própria
    operação bem sucedida — corrigir F05 sozinho faria a primeira resposta bloquear a
    acção seguinte."""

    def _responde(self, eng):
        return R["apply"](eng, row_id="U-001", answer_text="A equipa de dados",
                          answered_by={"role": "dono dos dados"},
                          locator="answers.md#U-001")

    def test_the_mirrored_row_is_resolved_in_the_same_transaction(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_migrado(tmp)
            self._responde(eng)
            no = next(n for n in G["read"](eng)["nodes"] if n["id"] == "U-001")
        self.assertTrue(no["props"].get("resolved"),
                        "a SU deu a pergunta por resolvida e o grafo continua a mostrá-la "
                        "aberta")

    def test_a_successful_answer_produces_no_drift_of_its_own(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_migrado(tmp)
            self._responde(eng)
            vista = P["operational_state"](eng)
        bloqueante = [d for d in vista["drift"]
                      if d["code"] in ("MIRROR_DRIFT", "MIRROR_SOURCE_MISSING")]
        self.assertEqual(bloqueante, [],
                         "a operação bem sucedida deixou o estado divergente de si próprio")

    def test_the_history_survives_the_fix(self):
        """Fechar o espelho não pode apagar de onde a linha veio."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_migrado(tmp)
            self._responde(eng)
            ids = {n["id"] for n in G["read"](eng)["nodes"]}
            arestas = [e for e in G["read"](eng)["edges"] if e["rel"] == "was"]
        self.assertIn("U-001", ids, "a linha original desapareceu do grafo")
        self.assertTrue(arestas, "a ligação `was` ao sucessor não existe")

    def test_the_next_action_is_not_blocked_by_the_previous_answer(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_migrado(tmp)
            self._responde(eng)
            boot = B["bootstrap"](eng)
        self.assertTrue(boot["ready"],
                        "responder a uma pergunta bloqueou a acção seguinte")


def eng_nascido_e_povoado(tmp):
    """A sequencia real: nasce vazio com `init`, ganha conhecimento, e so depois migra.

    Escrever `init` sobre uma SU ja povoada deixou de ser possivel (F08) — e bem. O caso
    que o F07 exercita e outro: um engagement que JA TINHA grafo quando a migracao correu.
    """
    vazia = FIX["HEAD"].format(confirmed="", assumed="", unknown="", conflicted="")
    eng = FIX["make"](tmp, vazia)
    M["init"](eng)
    (eng / "shared-understanding.md").write_text(FIX["NOVO"], encoding="utf-8", newline="\n")
    return eng


# =============================================================================
# F07 · P1 — restore declara sucesso sem restaurar um grafo preexistente
# =============================================================================

class F07_RestoreDevolveTudoOQueAMigracaoMudou(unittest.TestCase):
    """`TOUCHED` só cobre as quatro autoridades textuais. Os ficheiros do grafo só entram
    em `new_files` quando NÃO existiam — e um grafo que já existia fica com o conteúdo da
    migração, com resultado `restored`."""

    def test_a_pre_existing_empty_graph_comes_back_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_nascido_e_povoado(tmp)
            antes = (eng / "_graph" / "graph.jsonl").read_bytes()
            M["apply"](eng)
            out = M["restore"](eng)
            depois = (eng / "_graph" / "graph.jsonl").read_bytes()
        self.assertEqual(out["result"], "restored")
        self.assertEqual(depois, antes,
                         "declarou restored e o grafo ficou com o conteúdo da migração")

    def test_the_node_count_returns_to_what_it_was(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_nascido_e_povoado(tmp)
            M["apply"](eng)
            M["restore"](eng)
            st = G["read"](eng)
        self.assertEqual(len(st["nodes"]), 0)

    def test_an_absent_graph_is_still_removed_on_restore(self):
        """O caso que já funcionava: não se pode perder ao arranjar o outro."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = FIX["make"](tmp, FIX["NOVO"])
            M["apply"](eng)
            M["restore"](eng)
            st = G["read"](eng)
        self.assertEqual(st["status"], G["ABSENT"])

    def test_restore_publishes_through_the_coordinator(self):
        """Escrever e apagar à mão é a única parte da migração fora da barreira."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_nascido_e_povoado(tmp)
            M["apply"](eng)
            M["restore"](eng)
            recibos = sorted(p.stem for p in (eng / "_ops" / "receipts").glob("*.json"))
        self.assertTrue([r for r in recibos if "restore" in r],
                        "o restore não deixou recibo: correu fora do coordenador")


# =============================================================================
# F08 · P1 — `init` contorna a migração de um projecto que já tem conhecimento
# =============================================================================

class F08_InitSoNoQueEstaVazio(unittest.TestCase):
    """Defeito introduzido no W8, nesta sessão. `init` só olha para o estado do GRAFO, e
    um engagement com SU povoada e sem grafo fica `ready` com contexto vazio e gate aberto
    — que é exactamente o que tornar o grafo obrigatório queria impedir."""

    def test_init_refuses_an_engagement_that_already_has_knowledge(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = FIX["make"](tmp, FIX["NOVO"])          # SU com C-001 e U-001 crítico
            with self.assertRaises(M["MigrationError"]) as ctx:
                M["init"](eng)
        self.assertEqual(ctx.exception.code, "NOT_EMPTY")

    def test_the_refusal_names_migration_as_the_action(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = FIX["make"](tmp, FIX["NOVO"])
            with self.assertRaises(M["MigrationError"]) as ctx:
                M["init"](eng)
        self.assertIn("apply", json.dumps(ctx.exception.detail, ensure_ascii=False)
                      + str(ctx.exception))

    def test_an_empty_scaffold_is_still_born_with_a_graph(self):
        """O controlo: a recusa não pode comer o caso para que `init` existe."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = FIX["make"](tmp, FIX["HEAD"].format(
                confirmed="", assumed="", unknown="", conflicted=""))
            out = M["init"](eng)
            boot = B["bootstrap"](eng)
        self.assertEqual(out["result"], "created")
        self.assertTrue(boot["ready"])

    def test_an_authority_row_with_no_node_is_never_a_complete_context(self):
        """A segunda metade: reconstruir a partir do grafo não vê o que a SU tem a mais."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_migrado(tmp)
            su = eng / "shared-understanding.md"
            texto = su.read_text(encoding="utf-8").replace(
                "| C-001 | data | Base partilhada | inicial | 2026-01-01 | organizacional | R-01 |",
                "| C-001 | data | Base partilhada | inicial | 2026-01-01 | organizacional | R-01 |\n"
                "| C-777 | data | Linha nova sem no | fonte: acta | 2026-03-01 | organizacional | R-02 |")
            su.write_text(texto, encoding="utf-8", newline="\n")
            boot = B["bootstrap"](eng)
        self.assertFalse(boot["ready"] and not boot["limitations"],
                         "uma linha da autoridade sem representação no grafo passou "
                         "despercebida e o contexto deu-se por completo")


# =============================================================================
# F09 · P2 — coverage depende de bytes globais e de recibos
# =============================================================================

class F09_BaseDeCoberturaPeloQueEConsumido(unittest.TestCase):
    """Uma aresta de navegação (`ve_tambem`) não muda o fingerprint semântico e mesmo assim
    torna a base `stale`, por causa de `graph.jsonl`, `meta.json` e do recibo novo. Erra
    para o lado conservador — obriga a rever trabalho que não mudou."""

    def _base_e_navegacao(self, eng):
        inv = C["build_inventory"](eng)
        base = C["compute_basis"](eng, inv, "reconciliation")
        st = G["read"](eng)
        arestas = st["edges"] + [{"src": "C-001", "rel": "ve_tambem", "dst": "U-001",
                                  "props": {}, "provenance": {}}]
        O["run"](eng, "so-navegacao", G["write_set"](st["nodes"], arestas))
        agora = C["compute_basis"](eng, C["build_inventory"](eng), "reconciliation")
        return base, agora

    def test_navigation_that_changes_no_meaning_keeps_the_basis_current(self):
        with tempfile.TemporaryDirectory() as tmp:
            base, agora = self._base_e_navegacao(eng_migrado(tmp))
            fresh = C["check_freshness"]({"basis": base}, agora)
        self.assertEqual(fresh["status"], "current",
                         "uma aresta sem efeito na revisão obrigou a rever tudo")

    def test_an_operation_receipt_is_not_a_source_of_the_revision(self):
        """As fontes vivem em `basis["sources"]`, não nas chaves de topo — que são
        fingerprints. Ler as chaves fazia o caso passar sem olhar para nada."""
        with tempfile.TemporaryDirectory() as tmp:
            _base, agora = self._base_e_navegacao(eng_migrado(tmp))
        caminhos = [f["path"] for f in agora.get("sources", [])]
        self.assertTrue(caminhos, "a base não declarou fonte nenhuma")
        recibos = [c for c in caminhos if "_ops/receipts" in c]
        self.assertEqual(recibos, [],
                         "a base de cobertura conta recibos operacionais como fontes: "
                         + ", ".join(recibos))

    def test_a_declared_graph_dependency_enters_by_fingerprint(self):
        """Excluir os bytes do grafo sem pôr nada no lugar perdia a dependência. `graph.py`
        já tinha `as_coverage_source` para isto; o `compute_basis` é que nunca a chamava."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_migrado(tmp)
            base = C["compute_basis"](eng, C["build_inventory"](eng), "reconciliation",
                                      graph_consumed=["C-001"])
        caminhos = [f["path"] for f in base["sources"]]
        self.assertIn("_graph#consumed", caminhos,
                      "uma revisão que declara consumir grafo ficou sem dependência nenhuma")
        self.assertEqual([c for c in caminhos if c.startswith("_graph/")], [],
                         "os bytes do grafo voltaram à base")

    def test_navigation_is_current_but_a_changed_consumed_node_is_stale(self):
        """As duas direcções no mesmo caso: sem isto, «nunca fica stale» passaria."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_migrado(tmp)
            consumido = ["C-001"]
            base = C["compute_basis"](eng, C["build_inventory"](eng), "reconciliation",
                                      graph_consumed=consumido)
            st = G["read"](eng)
            arestas = st["edges"] + [{"src": "C-001", "rel": "ve_tambem", "dst": "U-001",
                                      "props": {}, "provenance": {}}]
            O["run"](eng, "so-navegacao", G["write_set"](st["nodes"], arestas))
            depois_nav = C["compute_basis"](eng, C["build_inventory"](eng), "reconciliation",
                                            graph_consumed=consumido)
            nav = C["check_freshness"]({"basis": base}, depois_nav)["status"]

            nos = [dict(n, props=dict(n["props"], text="outro texto"))
                   if n["id"] == "C-001" else n for n in st["nodes"]]
            O["run"](eng, "muda-consumido", G["write_set"](nos, arestas))
            depois_mud = C["compute_basis"](eng, C["build_inventory"](eng), "reconciliation",
                                            graph_consumed=consumido)
            mudou = C["check_freshness"]({"basis": base}, depois_mud)["status"]
        self.assertEqual(nav, "current", "navegação tornou a base stale")
        self.assertEqual(mudou, "stale", "mudar o nó consumido não tornou a base stale")

    def test_a_consumed_dependency_that_changes_still_goes_stale(self):
        """O controlo: uma base que nunca fica stale não é uma base."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = eng_migrado(tmp)
            inv = C["build_inventory"](eng)
            base = C["compute_basis"](eng, inv, "reconciliation")
            su = eng / "shared-understanding.md"
            su.write_text(su.read_text(encoding="utf-8").replace("| Critical |", "| Low |"),
                          encoding="utf-8", newline="\n")
            agora = C["compute_basis"](eng, C["build_inventory"](eng), "reconciliation")
            fresh = C["check_freshness"]({"basis": base}, agora)
        self.assertEqual(fresh["status"], "stale")


# =============================================================================
# F10 · P2 — a integração dos entrypoints ainda é parcial
# =============================================================================

class F10_OsEntrypointsPelaMesmaReconstrucao(unittest.TestCase):
    """`/status` e `/resume` seguem `aisa-status`, que chama `dashboard.py` — que não passa
    pela reconstrução comum nem pela projecção. O guarda protege a escrita seguinte; não
    torna a leitura anterior consistente."""

    def test_the_status_skill_goes_through_the_common_reconstruction(self):
        texto = (ROOT / ".claude" / "skills" / "aisa-status" / "SKILL.md").read_text(
            encoding="utf-8")
        self.assertTrue("bootstrap.py" in texto or "projection.py" in texto,
                        "`/status` responde sem consultar as limitações do kernel")

    def test_the_phase_gate_hook_uses_the_current_engine(self):
        texto = (ROOT / ".claude" / "hooks" / "phase-gate-check.py").read_text(
            encoding="utf-8")
        self.assertTrue("bootstrap" in texto or "projection" in texto,
                        "o gate de fase decide pelo motor anterior")

    def test_the_authority_guard_covers_more_than_four_names(self):
        texto = (ROOT / ".claude" / "hooks" / "pre-authority-guard.py").read_text(
            encoding="utf-8")
        self.assertIn("_graph", texto,
                      "o grafo é autoridade operacional e não está protegido pelo guarda")


# =============================================================================
# F11 · P2 — a suite não é reproduzível num clone limpo
# =============================================================================

class F11_SuiteReprodutivelSemMaterialPrivado(unittest.TestCase):
    """`projects/` é gitignored (só `.gitkeep` é versionado). Um teste obrigatório depende
    dele, por isso a suite só é verde em máquinas que têm os engagements privados."""

    def test_a_versioned_pre_v23_fixture_exists(self):
        fixtures = ROOT / ".claude" / "tests" / "fixtures"
        candidatos = list(fixtures.rglob("*pre-v2.3*")) + list(fixtures.rglob("*pre_v23*"))
        self.assertTrue(candidatos,
                        "não há fixture versionada pré-v2.3; a garantia depende de "
                        "material privado")

    def test_no_mandatory_test_depends_on_the_private_engagements(self):
        texto = (ROOT / ".claude" / "tests" / "test_state_scaffold.py").read_text(
            encoding="utf-8")
        i = texto.index("def test_a_pre_v23_su_still_exists_untouched")
        corpo = texto[i:i + 900]
        self.assertIn("skip", corpo.lower(),
                      "o caso obrigatório não declara skip quando `projects/` está vazio")


if __name__ == "__main__":
    unittest.main(verbosity=1)
