#!/usr/bin/env python3
"""coverage.py — aisa: inventário, resolução de referências e atualidade da cobertura.

Motor determinístico do kernel (`library/kernel/tools/`). Lido e executado em runtime,
nunca editado em runtime. Dependências: Python 3.11+, **stdlib apenas**.

Normativo: [`library/kernel/coverage-contract.md`](../coverage-contract.md). Este ficheiro
implementa; o contrato define. Onde os dois discordarem, o contrato manda e isto é um bug.

O que este motor entrega (plano §12, fases 2 e 3)
-------------------------------------------------
  build_inventory   o DENOMINADOR, derivado das fontes -- nunca do registo que o agente
                    escreve. Se fosse o registo a defini-lo, bastava omitir ao mesmo tempo
                    o requisito e a linha de revisão para obter falso verde (§6.1).
  compute_basis     o manifesto POR ETAPA + os três digests derivados (§6.3, §6.5).
  check_freshness   `current` | `stale`, com a razão de cada diferença (§6.3, §6.4).
  resolve_unit /    resolução de locators por travessia, sem JSONPath e sem `eval`,
  resolve_target    com a fronteira de caminhos da §5.3.
  CLI `inventory`   stdout, zero escrita.

  validate_record   o registo contra o contrato §4 -- forma, disposições, destinos,
                    herança de obrigações e revisão declarada. O veredicto é RECALCULADO em
                    cada leitura: um `valid: true` escrito no ficheiro não é veredicto.
  select_record     a revisão aplicável por etapa + identidade do alvo; entre as do mesmo
                    par vale a mais recente, nunca uma antiga que esconda a nova (§6.6).
  coverage_state    o resultado computado da §7, com `not_evaluated` como resultado
                    legítimo -- ausência de revisão não é aprovação nem reprovação.
  render_report     a projecção Markdown determinística, que NÃO é autoridade.
  finalize          a ÚNICA operação de escrita, e escreve só em `_coverage/`.
  CLI               `inventory`, `check`, `report` (read-only) e `finalize`.

O que este motor NÃO faz, e não finge fazer: não escreve na Shared Understanding, não
escreve decisões, não aprova nada e não resolve perguntas em aberto. Um engagement sem
registos dá `not_evaluated`.

Quem o chama (fase 4 do plano): `aisa-blueprint` nos passos 1e, 13b e 15, `aisa-answer` e
`aisa-capture` para calcular atualidade, `dashboard.py::coverage_status` para `status.coverage`,
e o hook `blueprint-validate.py` para reportar ao lado da estrutura. Todos leem; só `finalize`
escreve, e só quem o invoca explicitamente. A etapa `render` está implementada e **continua
por ligar** — é a fase 5.

**Escrita:** só `finalize`, só dentro de `_coverage/`, e só por reserva exclusiva de uma
versão nova. Não existe `os.replace` sobre uma versão publicada em lado nenhum deste
ficheiro; `inventory`, `check` e `report` não abrem nada para escrita.

Uso:
  python coverage.py inventory --engagement <slug|caminho> [--json]
  python coverage.py check     --engagement <slug> --stage reconciliation [--json]
  python coverage.py check     --engagement <slug> --stage blueprint --target <ficheiro>
  python coverage.py check     --engagement <slug> --stage render --target <f> --deliverable <id>
  python coverage.py report    --engagement <slug> [--stage <etapa>] [--record <ficheiro>]
  python coverage.py finalize  --engagement <slug> --draft <rascunho.json>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import runpy
import sys
import unicodedata
from pathlib import Path

TOOL_VERSION = "0.1.0"
ARTEFACT = "aisa.coverage.inventory"
CONTRACT_VERSION = "1"          # coverage-contract.md §4.2; sobe quando o SIGNIFICADO muda
SCHEMA_VERSION = 1

# --------------------------------------------------------------------------- códigos
# Tabela ÚNICA do contrato §8, usada pelo motor, pela linha de comandos e por quem der
# feedback. Ter variantes entre hooks e CLI era ter duas tabelas.
COV_SCHEMA = "COV-SCHEMA"
COV_NO_REVIEW = "COV-NO-REVIEW"
COV_STALE = "COV-STALE"
COV_UNREVIEWED = "COV-UNREVIEWED"
COV_DEAD_REF = "COV-DEAD-REF"
COV_MISSING_TARGET = "COV-MISSING-TARGET"
COV_INVALID_TARGET = "COV-INVALID-TARGET"
COV_EXCLUSION_NO_DECISION = "COV-EXCLUSION-NO-DECISION"
COV_REVIEW_INCOMPLETE = "COV-REVIEW-INCOMPLETE"
COV_KNOWN_GAP = "COV-KNOWN-GAP"
COV_CAPTURE_LIMIT = "COV-CAPTURE-LIMIT"
COV_AUTHORITY_MISMATCH = "COV-AUTHORITY-MISMATCH"
COV_UNEXPECTED = "COV-UNEXPECTED"

# ------------------------------------------------------------------ caminhos e base
# §6.3: excluídos da base por serem histórico ou derivados. Lista EXPLÍCITA -- um padrão
# («tudo o que acaba em -log.md») apanharia amanhã um ficheiro que é fonte.
DERIVED_FILES = (
    "dashboard.html", "story.md", "council-log.md", "gate-log.md",
    "_capture/_capture-log.md", "_blueprint/blueprint-log.md",
    "_render/render-log.md", "_render/render-gaps.md",
    "_synthesis/_synthesis-checks.md",
)
DERIVED_SUFFIXES = (".tmp", ".bak")
DERIVED_DIRS = ("__pycache__/",)

# §6.3: os alvos ficam fora do manifesto -- entram por `target.sha256` e por `based_on`.
TARGET_DIRS = ("_blueprint/", "_render/")
COVERAGE_DIR = "_coverage/"
SYNTHESIS_DIR = "_synthesis/"

# Estado OPERACIONAL: recibos, marcador de pendência, staging. Não é fonte de conclusão
# nenhuma — é o registo de que uma escrita aconteceu. Entrava como fonte `freshness` pela
# regra por defeito, e bastava uma operação qualquer para tornar `stale` uma revisão que
# nada do que ela leu tinha mudado.
OPERATIONAL_DIRS = ("_ops/", "_migration/")

# O grafo NÃO entra por bytes. Uma aresta de navegação muda `graph.jsonl` e não muda nada
# do que a revisão consumiu; comparar os bytes fazia disso um `stale`. O que entra — quando
# entra — é o fingerprint canónico do subconjunto declarado como consumido
# (`graph.as_coverage_source`, contrato C4). Excluir sem substituir seria perder a
# dependência; por isso a substituição é explícita e não uma omissão.
GRAPH_DIR = "_graph/"

# §6.3: comparados por fingerprint semântico, nunca pelos bytes.
INFORMATIVE = ("shared-understanding.md", "decisions.md")

STAGES = ("reconciliation", "blueprint", "render")

# §8.2 e `render-contract.md` -> *Applicability*: os MESMOS quatro estados do render, sem
# taxonomia paralela. `not_applicable` e `blocked` são ausências legítimas: skip com
# razão, nunca lacuna.
APPLICABILITY = ("required", "conditional", "not_applicable", "blocked")

# §5.3: a única excepção à fronteira do engagement -- e é estreita. Os contratos e os
# templates de síntese do kernel, e os templates de deliverable e de arquitectura do
# PACOTE ACTIVO. Nem todo o `library/kernel/` (os motores não são autoridade de leitura de
# uma revisão) e nem todos os packs (um pacote que o engagement não usa não o condiciona).
KERNEL_AUTHORITIES = ("library/kernel/synthesis-templates",
                      "library/kernel/capture-templates")
KERNEL_AUTHORITY_FILES = ("library/kernel/coverage-contract.md",
                          "library/kernel/blueprint-contract.md",
                          "library/kernel/render-contract.md",
                          "library/kernel/phases.md",
                          "library/kernel/states.md",
                          "library/kernel/orchestration.md",
                          "library/kernel/glossary.md")
PACK_AUTHORITIES = ("deliverable-templates", "architecture-templates")

# §8.3: qual a versão do desenho que CADA deliverable lê. O template é que declara, no
# campo `blueprint_version_read` do seu frontmatter; o motor traduz o token e VERIFICA.
# Não é uma tabela kernel «requisito -> deliverable»: é a mesma selecção de versão que o
# `render-contract.md` já define, lida de onde ela está escrita.
VERSION_TOKENS = {
    "v<latest authorized>": "latest-authorized",
    "v<approved>": "approved",
    "none": None,
    "null": None,
    "": None,
}

# §8.2: «um id num comentário não prova preservação semântica». A única forma de
# comentário que o Markdown tem é a do HTML, e uma linha que é só isso é uma referência ao
# requisito -- nunca a sua projecção. Um cabeçalho (`# A3`) NÃO é comentário: por isso o
# padrão é estreito de propósito, e não apanha `#`, `//` nem `%`.
COMMENT_LINE = re.compile(r"^\s*<!--.*?-->\s*$")


class CoverageError(Exception):
    """Erro de uso ou de resolução. A CLI traduz para código de saída."""

    def __init__(self, message: str, exit_code: int = 2):
        super().__init__(message)
        self.exit_code = exit_code


# =============================================================== canonicalização §6.5

_WS_RE = re.compile(r"\s+")


def norm_text(value) -> str:
    """NFC → espaço branco colapsado → strip. Ausente serializa como "", nunca null.

    Contrato §6.5: "campo vazio" e "campo ausente" não podem produzir digests diferentes
    por acidente de leitura."""
    if value is None:
        return ""
    if not isinstance(value, str):
        value = str(value)
    return _WS_RE.sub(" ", unicodedata.normalize("NFC", value)).strip()


def _canon(obj):
    """Normaliza recursivamente as strings de uma estrutura antes de serializar."""
    if isinstance(obj, str):
        return norm_text(obj)
    if obj is None:
        # Contrato §6.5: ausente serializa como "", nunca null -- senão "campo vazio" e
        # "campo ausente" davam digests diferentes por acidente de leitura.
        return ""
    if isinstance(obj, bool) or isinstance(obj, (int, float)):
        return obj
    if isinstance(obj, dict):
        return {norm_text(k): _canon(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_canon(v) for v in obj]
    return norm_text(obj)


def canonical_json(obj) -> str:
    """JSON canónico do contrato §6.5: chaves ordenadas, sem espaço insignificante,
    sem escapes não-ASCII, strings normalizadas."""
    return json.dumps(_canon(obj), sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"))


def digest(obj) -> str:
    """sha256 do JSON canónico, em UTF-8."""
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


# ==================================================================== adapter §4.1
# `coverage.py` NÃO importa `dashboard.py` no topo: o plano §4.1 proíbe o import
# circular, e o dashboard já carrega este módulo quando precisar. Os leitores chegam
# por um adapter que os carrega quando -- e se -- forem precisos.

class ReaderAdapter:
    """Os leitores que já existem, carregados sob procura.

    Não é um framework de plugins (plano §8): é um objecto com os métodos que este
    módulo usa, e um ponto único onde trocá-los num teste."""

    def __init__(self, repo: Path | None = None, module: dict | None = None):
        self.repo = Path(repo) if repo else repo_root()
        self._module = module

    @property
    def d(self) -> dict:
        if self._module is None:
            path = self.repo / "library" / "kernel" / "tools" / "dashboard.py"
            if not path.is_file():
                raise CoverageError(
                    "leitores do kernel não encontrados: {}".format(path), 3)
            self._module = runpy.run_path(str(path))
        return self._module

    # -- leitores usados aqui, um método por leitor, para o ponto de troca ser claro
    def parse_su(self, md: str):
        return self.d["parse_su"](md)

    def classify_decisions(self, md: str):
        return self.d["classify_decisions"](md)

    def live_solution_decision(self, md: str):
        return self.d["live_solution_decision"](md)

    def decision_block_span(self, md: str, did: str) -> str:
        return self.d["decision_block_span"](md, did)

    def yl_find_block(self, text: str, key: str, parent: str | None = None):
        return self.d["yl_find_block"](text, key, parent)

    def yl_list_of_maps(self, block):
        return self.d["yl_list_of_maps"](block)

    def yl_scalar_at(self, text: str, key: str, parent: str | None = None):
        return self.d["yl_scalar_at"](text, key, parent)

    # -- verificação estrutural do desenho (contrato §8.1.4): chamada, nunca reescrita
    def bp_validate(self, text: str, filename: str = "", pack_cfg=None, su_ids=None,
                    loader=None):
        return self.d["bp_validate"](text, filename, pack_cfg, su_ids, loader)

    def bp_pack_cfg(self, pack: str):
        return self.d["bp_pack_cfg"](pack)

    def bp_loader(self, eng: Path):
        return self.d["bp_loader"](eng)

    # -- versões do desenho e o seu estado de autorização/aprovação (§8.3): o motor da
    # dashboard já as calcula, e recalculá-las aqui era criar uma segunda verdade.
    def blueprint_state(self, eng: Path, blocks: list, rows=None, pack: str = ""):
        return self.d["blueprint_state"](eng, blocks, rows, pack)


def repo_root() -> Path:
    """<repo>/library/kernel/tools/coverage.py -> <repo>.

    Derivada de `__file__`, nunca de `sys.argv`: este módulo é importável, e um módulo
    que lê os argumentos de quem o importa passa a depender da forma de execução."""
    return Path(__file__).resolve().parents[3]


# ============================================================= resolução de engagement

def engagements_root(repo: Path | None = None) -> Path:
    env = os.environ.get("AISA_ENGAGEMENTS_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    return (repo or repo_root()) / "projects"


def _is_engagement(path: Path) -> bool:
    return (path / "_state.json").is_file()


def find_engagement(spec: str | None, repo: Path | None = None) -> Path:
    """Resolve `--engagement`: um caminho, ou um slug sob a raiz de engagements.

    Ambiguidade exige argumento (plano §8): com mais do que um engagement e sem
    `--engagement`, falha e nomeia-os. **Nunca escolhe o primeiro.**"""
    root = engagements_root(repo)
    if spec:
        cand = Path(spec).expanduser()
        if not cand.is_absolute():
            direct = (Path.cwd() / cand).resolve()
            if _is_engagement(direct):
                return direct
        elif _is_engagement(cand.resolve()):
            return cand.resolve()
        under = (root / spec).resolve()
        if _is_engagement(under):
            return under
        raise CoverageError(
            "engagement não encontrado: {!r} (procurado como caminho e como slug sob {})"
            .format(spec, root), 3)
    if not root.is_dir():
        raise CoverageError("raiz de engagements não encontrada: {}".format(root), 3)
    found = sorted(p for p in root.iterdir() if p.is_dir() and _is_engagement(p))
    if not found:
        raise CoverageError("nenhum engagement em {}".format(root), 3)
    if len(found) > 1:
        raise CoverageError(
            "mais do que um engagement em {} ({}) — indicar --engagement; "
            "escolher o primeiro seria escolher por acaso"
            .format(root, ", ".join(p.name for p in found)), 2)
    return found[0]


# =================================================================== caminhos §5.3

_GRAPH_MODULE = {}


def _graph_module(eng: Path):
    """`graph.py`, carregado à conta-gotas — só quando uma revisão declara consumir grafo.

    Preguiçoso de propósito: a esmagadora maioria das revisões não consome relações do
    grafo, e este módulo é chamado dezenas de vezes por corrida. Pagar o carregamento
    sempre por causa de um caso raro seria o mesmo erro que hashear o grafo inteiro por
    causa de uma aresta.
    """
    caminho = Path(__file__).resolve().parent / "graph.py"
    if "mod" not in _GRAPH_MODULE:
        _GRAPH_MODULE["mod"] = runpy.run_path(str(caminho))
    return _GRAPH_MODULE["mod"]


GRAPH_CONSUMED_PATH = "_graph#consumed"


def declared_graph_consumed(record) -> tuple:
    """As relações do grafo que uma revisão declara consumir.

    Entra pela mesma porta que as `authorities`: `basis.graph_consumed` do registo ou do
    rascunho. Um registo antigo não tem o campo — aí lê-se do que ele próprio publicou
    (`basis.sources` → a entrada `_graph#consumed` carrega a lista), para uma revisão
    publicada antes disto continuar a comparar contra o que comparou.

    Sem declaração, tupla vazia: uma revisão que não consome relações não pode ficar `stale`
    por causa delas — e também não pode ficar `stale` por a fonte desaparecer da comparação,
    que era o que acontecia quando `compute_basis` aceitava o parâmetro e ninguém o passava.
    """
    base = _as_dict((record or {}).get("basis"))
    declarado = _as_list(base.get("graph_consumed"))
    if declarado:
        return tuple(str(x) for x in declarado)
    for src in _as_list(base.get("sources")):
        d = _as_dict(src)
        if d.get("path") == GRAPH_CONSUMED_PATH:
            return tuple(str(x) for x in _as_list(d.get("consumed")))
    return ()


def graph_dependency(eng: Path, consumed) -> dict | None:
    """A dependência do grafo como FONTE, pelo fingerprint do que foi consumido.

    `graph.py` já tinha `as_coverage_source` para isto — e `compute_basis` nunca a
    chamava, por isso o que entrava eram os bytes de `graph.jsonl` e `meta.json`. Excluir
    esses bytes sem pôr isto no lugar perdia a dependência em vez de a arrumar.

    Sem `consumed` declarado não há entrada nenhuma: uma revisão que não consome relações
    não deve ficar `stale` por causa delas.
    """
    if not consumed:
        return None
    g = _graph_module(eng)
    st = g["read"](Path(eng))
    if st.get("status") != g["OK"]:
        return None
    return g["as_coverage_source"](st["nodes"], st["edges"], consumed)


def engagement_state(eng: Path) -> tuple[dict, str]:
    """`_state.json`, com verificação de **raiz apenas** — e essa é a razão de ser.

    É este ficheiro que declara o pacote activo, e é do pacote activo que depende a lista
    de autoridades da §5.3. Fazê-lo passar pela verificação completa seria pedir-lhe que
    se validasse a si próprio. A verificação que se lhe aplica é a que não depende dele:
    o caminho resolvido tem de ficar dentro da raiz do engagement. Nunca é autoridade
    externa, por isso não perde nada."""
    eng_real = eng.resolve()
    p = eng_real / "_state.json"
    try:
        real = p.resolve()
    except OSError:
        return {}, "unreadable"
    if not _within(real, eng_real):
        return {}, "refused"
    text, state = read_source(real)
    if state != "ok":
        return {}, state
    try:
        data = json.loads(text)
    except ValueError:
        return {}, "unreadable"
    return (data if isinstance(data, dict) else {}), "ok"


def active_pack(eng: Path) -> str:
    return engagement_state(eng)[0].get("pack", "")


def authority_roots(repo: Path, pack: str) -> list[Path]:
    """As autoridades de leitura permitidas fora do engagement (§5.3), e só essas."""
    roots = [repo / p for p in KERNEL_AUTHORITIES]
    roots += [repo / f for f in KERNEL_AUTHORITY_FILES]
    if pack:
        roots += [repo / "library" / "packs" / pack / p for p in PACK_AUTHORITIES]
    return roots


def safe_path(eng: Path, rel: str, repo: Path | None = None,
              pack: str | None = None) -> Path:
    """Resolve `rel` dentro do engagement, ou numa autoridade permitida do repositório.

    A verificação é sobre o caminho REALMENTE resolvido, com symlinks seguidos:
    traversal, symlink para fora e absoluto fora da raiz são recusados **sem ler**.

    Achado A4: isto passou a ser a ÚNICA porta de leitura. O inventário e o manifesto
    liam por caminho directo, e a protecção só cobria os locators — um symlink dentro de
    `inputs/` a apontar para fora era lido e hasheado sem ninguém verificar nada."""
    repo = repo or repo_root()
    eng_real = eng.resolve()
    pack = active_pack(eng) if pack is None else pack
    raw = Path(rel)
    # Duas leituras possíveis de um caminho relativo, e são ambas reais no contrato: o
    # engagement escreve `inputs/x.xlsx`; um registo cita a autoridade que leu por
    # `library/packs/<pack>/deliverable-templates/...`, que é relativa ao REPOSITÓRIO.
    # A segunda leitura não alarga a fronteira: só é aceite se cair dentro de uma
    # autoridade permitida pela §5.3 — `library/kernel/tools/dashboard.py` continua
    # recusado, e o motor não é autoridade de leitura de uma revisão.
    candidates = [raw] if raw.is_absolute() else [eng_real / raw, repo / raw]
    reals = []
    for cand in candidates:
        try:
            reals.append(cand.resolve())
        except OSError as exc:                                      # noqa: BLE001
            raise CoverageError("caminho irresolúvel: {} ({})".format(rel, exc), 3)
    # O engagement tem precedência, mas só quando o ficheiro lá está: `_within` é uma
    # verificação de caminho, não de existência, e sem isto `library/...` resolveria
    # sempre para um ficheiro inexistente DENTRO do engagement e a autoridade real nunca
    # seria lida.
    if _within(reals[0], eng_real) and reals[0].exists():
        return reals[0]
    for root in authority_roots(repo, pack):
        rr = root.resolve()
        for real in reals:
            if (real == rr or _within(real, rr)) and real.exists():
                return real
    if _within(reals[0], eng_real):
        return reals[0]          # dentro do engagement e ausente: `absent`, não recusa
    raise CoverageError(
        "caminho fora da fronteira do engagement, recusado sem ler: {} -> {}"
        .format(rel, reals[0]), 3)


def engagement_files(eng: Path) -> tuple[list[tuple[str, Path]], list[dict]]:
    """Os ficheiros do engagement que é seguro ler, e o diagnóstico dos que não são.

    Cada caminho é validado contra a fronteira ANTES de qualquer leitura ou hash: um
    symlink dentro do engagement a apontar para fora não é lido nem hasheado, é
    reportado."""
    eng_real = eng.resolve()
    ok: list[tuple[str, Path]] = []
    bad: list[dict] = []
    for p in sorted(eng_real.rglob("*")):
        rel = p.relative_to(eng_real).as_posix()
        # A fronteira decide-se ANTES de se perguntar o que a entrada é. Uma PASTA que é
        # ligação para fora falha o `is_file()` e sairia calada: `rglob` não desce nela, por
        # isso o conteúdo de fora nunca entra no denominador, mas a fuga ficava por reportar
        # e `complete` continuava verdadeiro. Em Windows a junção resolve-se da mesma forma;
        # em POSIX era silenciosa.
        try:
            real = p.resolve()
        except OSError:
            bad.append({"level": "error", "blocking": True, "where": rel,
                        "message": "caminho irresolúvel — não lido"})
            continue
        if not _within(real, eng_real):
            bad.append({"level": "error", "blocking": True, "where": rel,
                        "message": "aponta para fora do engagement ({}) — recusado sem "
                                   "ler (contrato §5.3)".format(real)})
            continue
        try:
            if not p.is_file():
                continue
        except OSError as exc:
            # Um caminho que não se consegue sequer `stat` não desaparece: é reportado como
            # impeditivo, tal como o irresolúvel acima (achado A2 — nada some calado).
            bad.append({"level": "error", "blocking": True, "where": rel,
                        "message": "caminho que não se consegue inspeccionar ({}) — não "
                                   "lido".format(type(exc).__name__)})
            continue
        ok.append((rel, real))
    return ok, bad


def _within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def guarded_read(eng: Path, rel: str, pack: str | None = None) -> tuple[str, str]:
    """Lê `rel` SÓ depois de a fronteira o aceitar. `refused` é um estado como os outros.

    Esta é a única porta de leitura do módulo. A versão anterior validava a enumeração
    dos ficheiros e depois lia as fontes principais por `eng / nome`, o que deixava um
    caminho recusado voltar a entrar por outra via — e emitir um diagnóstico **depois**
    não cumpre a obrigação de recusar **antes** de ler."""
    try:
        path = safe_path(eng, rel, pack=pack)
    except CoverageError:
        return "", "refused"
    return read_source(path)


def guarded_read_json(eng: Path, rel: str, pack: str | None = None) -> tuple[object, str]:
    text, state = guarded_read(eng, rel, pack)
    if state != "ok":
        return None, state
    try:
        return json.loads(text), "ok"
    except ValueError:
        return None, "unreadable"


def guarded_sha256(eng: Path, rel: str, pack: str | None = None) -> tuple[str, str]:
    """Digest só depois da fronteira. Um ficheiro recusado não é hasheado."""
    try:
        path = safe_path(eng, rel, pack=pack)
    except CoverageError:
        return "", "refused"
    if not path.is_file():
        return "", "absent"
    try:
        return sha256_file(path), "ok"
    except OSError:
        return "", "unreadable"


def read_source(path: Path) -> tuple[str, str]:
    """-> (texto, estado) com `estado ∈ {ok, absent, empty, unreadable}`.

    Os três estados negativos são DIFERENTES e não podem colapsar (achado A2): um ficheiro
    ausente é uma coisa, um ficheiro vazio é evidência de ausência de conteúdo, e um
    ficheiro que existe e não se lê é uma fonte que **desapareceu da revisão sem ninguém
    dar por isso**. Era esse o defeito: erro de leitura devolvia texto vazio, e o
    inventário saía com menos unidades e zero diagnósticos."""
    if not path.exists():
        return "", "absent"
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError, ValueError):
        return "", "unreadable"
    return (text, "ok") if text.strip() else (text, "empty")


def _read(path: Path) -> str:
    """Leitura tolerante, só para onde o estado já foi avaliado à parte."""
    return read_source(path)[0]


def read_json_source(path: Path) -> tuple[object, str]:
    """-> (dados, estado). `unreadable` cobre tanto o erro de I/O como o JSON inválido:
    nos dois casos o ficheiro existe e o seu conteúdo não entrou no denominador."""
    text, state = read_source(path)
    if state in ("absent", "empty"):
        return None, state
    if state == "unreadable":
        return None, "unreadable"
    try:
        return json.loads(text), "ok"
    except ValueError:
        return None, "unreadable"


def _read_json(path: Path):
    return read_json_source(path)[0]


def _source_diagnostic(rel: str, state: str, what: str) -> dict | None:
    """O diagnóstico que um estado negativo obriga a emitir, ou None quando não há."""
    if state == "refused":
        return {"level": "error", "blocking": True, "where": rel,
                "message": "aponta para fora do engagement — recusado **sem ler** "
                           "(contrato §5.3); {} ficaram fora do denominador".format(what)}
    if state == "unreadable":
        return {"level": "error", "blocking": True, "where": rel,
                "message": "existe e não se lê (I/O ou codificação) — {} ficaram fora do "
                           "denominador; a revisão não pode ser completa sobre esta base"
                           .format(what)}
    if state == "empty":
        return {"level": "warn", "blocking": False, "where": rel,
                "message": "existe e está vazio — {} não produziram unidades; ausência de "
                           "conteúdo é evidência, mas tem de ser visível".format(what)}
    return None


# ============================================ o que a aprovação retira do inventário

def approval_ids(eng: Path, readers: ReaderAdapter, pack: str | None = None) -> set[str]:
    """Ids dos blocos de aprovação de blueprint (contrato §6.1).

    Identificação POSITIVA pelo tipo que o leitor de decisões atribui ao bloco, nunca
    pelo prefixo do id: nenhuma outra linha `D-*` sai do inventário, porque mudar a
    decisão-solução tem de continuar a invalidar.

    Lê pela porta: era chamada antes da verificação de caminhos e lia `decisions.md`
    directamente."""
    md, state = guarded_read(eng, "decisions.md", pack)
    if state != "ok" or not md:
        return set()
    return {b["id"] for b in readers.classify_decisions(md)
            if b.get("kind") == "blueprint-approval"}


# ===================================================================== inventário §6.1

def _unit(key: str, cls: str, sha: str, note: str = "") -> dict:
    return {"unit_key": key, "class": cls, "sha256": sha, "note": note}


CONTEXT_FIELDS = ("literal_request", "requester", "inputs", "funding_gate")
AUX_ARTEFACTS = ("frame.md", "options.md", "premortem.md")
SU_FP_FIELDS = ("id", "state", "claim", "support", "extra", "criticidade",
                "verificado_em", "validade", "resolved", "retired")


def _answer_headings(md: str) -> list[str]:
    """Cabeçalhos `## <id>` de `answers.md`, na ordem do ficheiro.

    O id é o primeiro segmento antes de ` — `: o mesmo corte que `states.md` usa para a
    âncora, e é por isso que duas respostas ao mesmo id colidem e precisam de ordinal."""
    out = []
    for line in md.splitlines():
        if line.startswith("## "):
            out.append(re.split(r"\s+—\s+|\s+--\s+", line[3:].strip())[0].strip())
    return out


def _section_text(md: str, heading_re: str) -> str:
    m = re.search(heading_re + r"(.*?)(?=^#{1,6}\s|\Z)", md, re.M | re.S)
    return m.group(0) if m else ""


def build_inventory(eng: Path, readers: ReaderAdapter | None = None) -> dict:
    """O denominador, derivado dos FICHEIROS (contrato §6.1).

    Granularidade (§6.2): um workbook com rascunho de campos entra por COLUNA — o
    rascunho é o inventário L1 e já cobre as folhas; um workbook sem rascunho entra por
    FOLHA, que é a granularidade que a captura produziu. Acrescentar unidades de folha a
    um workbook que já entrou por coluna contaria a mesma coisa duas vezes.
    """
    readers = readers or ReaderAdapter()
    eng = eng.resolve()
    units: list[dict] = []
    excluded: list[dict] = []
    limitations: list[dict] = []
    diagnostics: list[dict] = []

    # O pacote activo resolve-se UMA vez: `safe_path` precisa dele, e relê-lo por cada
    # unidade seria mil leituras de `_state.json` num engagement real.
    state_data, state_state = engagement_state(eng)
    d = _source_diagnostic("_state.json", state_state, "o pacote activo e o estado")
    if d:
        diagnostics.append(d)
    pack = state_data.get("pack", "")

    safe_files, unsafe = engagement_files(eng)
    diagnostics.extend(unsafe)
    readable = {rel: real for rel, real in safe_files}

    skip = approval_ids(eng, readers, pack)

    def note_state(rel: str, state: str, what: str) -> None:
        d = _source_diagnostic(rel, state, what)
        if d:
            diagnostics.append(d)

    # ---------------------------------------------------------------- context.json
    ctx, ctx_state = guarded_read_json(eng, "context.json", pack)
    note_state("context.json", ctx_state, "os campos de contexto")
    for field in CONTEXT_FIELDS:
        if isinstance(ctx, dict) and field in ctx:
            units.append(_unit("context.json#" + field, "context-field",
                               digest(ctx[field])))

    # ------------------------------------------------------------- enquadramento.md
    enq, enq_state = guarded_read(eng, "enquadramento.md", pack)
    note_state("enquadramento.md", enq_state, "os temas e invariantes")
    for m in re.finditer(r"^##\s+(T\d)\s*·", enq, re.M):
        body = _section_text(enq, r"^##\s+" + m.group(1) + r"\s*·.*?$")
        units.append(_unit("enquadramento.md#" + m.group(1), "enquadramento-theme",
                           digest(body)))
    for mid in sorted(set(re.findall(r"\bM-\d+\b", enq))):
        rows = [ln for ln in enq.splitlines() if re.search(r"\|\s*" + mid + r"\s*\|", ln)]
        units.append(_unit("enquadramento.md#" + mid, "invariant",
                           digest(rows or mid)))

    # ------------------------------------------------------------------ answers.md
    ans, ans_state = guarded_read(eng, "answers.md", pack)
    note_state("answers.md", ans_state, "as secções de resposta")
    heads = _answer_headings(ans)
    seen: dict[str, int] = {}
    for h in heads:
        seen[h] = seen.get(h, 0) + 1
        key = "answers.md#" + h + (("[%d]" % seen[h]) if heads.count(h) > 1 else "")
        body = _nth_section(ans, h, seen[h])
        units.append(_unit(key, "answer-section", digest(body),
                           "secção repetida: ordinal explícito" if heads.count(h) > 1
                           else ""))

    # -------------------------------------------------------- shared-understanding
    su_md, su_state = guarded_read(eng, "shared-understanding.md", pack)
    note_state("shared-understanding.md", su_state, "as linhas de conhecimento")
    if su_md:
        _h, rows, _meta, su_diag = readers.parse_su(su_md)
        diagnostics.extend(su_diag or [])
        for row in rows:
            rid = row.get("id", "")
            if not rid:
                continue
            key = "shared-understanding.md#" + rid
            if rid in skip:
                excluded.append({"unit_key": key, "reason": "espelho de aprovação de "
                                                            "blueprint (contrato §6.1)"})
                continue
            units.append(_unit(key, "su-row", digest(_su_row_fp(row))))

    # ----------------------------------------------------------------- decisions.md
    dec_md, dec_state = guarded_read(eng, "decisions.md", pack)
    note_state("decisions.md", dec_state, "os blocos de decisão")
    for m in re.finditer(r"^##\s+(D-\d{2,4})\b", dec_md, re.M):
        did = m.group(1)
        key = "decisions.md#" + did
        if did in skip:
            excluded.append({"unit_key": key, "reason": "registo de aprovação de "
                                                        "blueprint (contrato §6.1)"})
            continue
        units.append(_unit(key, "decision-block",
                           digest(readers.decision_block_span(dec_md, did))))

    # --------------------------------------------------------------------- inputs/
    # Achado A1: percorrido RECURSIVAMENTE. Com `iterdir()`, um ficheiro em
    # `inputs/extra/pedido.txt` entrava no manifesto (que usa rglob) e ficava fora do
    # inventário -- o hash mudava e o denominador não, que é a pior assimetria possível.
    # O caminho relativo preserva-se por inteiro: a subpasta faz parte da identidade.
    for rel in sorted(r for r in readable if r.startswith("inputs/")):
            p = readable[rel]
            sha, sha_state = guarded_sha256(eng, rel, pack)
            if sha_state != "ok":
                note_state(rel, sha_state, "este ficheiro de entrada")
                continue
            supported = p.suffix.lower() in (".xlsx", ".xlsm", ".vtt", ".docx", ".pdf")
            note = "" if supported else "formato fora dos tiers de captura"
            if "/" in rel[len("inputs/"):]:
                note = (note + "; " if note else "") + "em subpasta de `inputs/`"
            units.append(_unit(rel, "input-file", sha, note))
            if not supported:
                # §6.2: não desaparece do denominador e não é `not_applicable` por falta
                # de suporte -- é uma LIMITAÇÃO, e quem revê tem de a tratar.
                limitations.append({
                    "code": COV_CAPTURE_LIMIT,
                    "unit_key": rel,
                    "reason": "sem extractor para {}".format(p.suffix or "ficheiro sem extensão"),
                    "impact": "obrigações descritas só neste ficheiro podem não estar no "
                              "denominador",
                    "action": "leitura humana; a revisão declara-o `unverifiable`",
                })

    # -------------------------------------------------------------------- _capture/
    # O `_capture/` percorre-se pela lista JÁ VALIDADA, não por glob: um glob volta a
    # enumerar o disco e dá a volta à fronteira.
    cap_files = sorted(r for r in readable if r.startswith("_capture/"))
    if cap_files:
        drafted: set[str] = set()
        for rel in [r for r in cap_files if r.endswith(".fields-draft.json")]:
            p = readable[rel]
            data, state = guarded_read_json(eng, rel, pack)
            if state != "ok" or not isinstance(data, dict):
                diagnostics.append({"level": "error", "blocking": True, "where": rel,
                                    "message": "rascunho de campos {} — as colunas desse "
                                               "workbook ficaram fora do denominador"
                                               .format({"unreadable": "ilegível",
                                                        "empty": "vazio",
                                                        "absent": "ausente",
                                                        "refused": "fora da fronteira"}
                                                       .get(state, "malformado"))})
                continue
            workbook = p.name[:-len(".fields-draft.json")]
            drafted.add(workbook)
            base = rel + "#"
            for sheet in data.get("sheets") or []:
                for col in sheet.get("columns") or []:
                    units.append(_unit(
                        base + sheet.get("name", "") + "/" + col.get("column", ""),
                        "xlsx-column", digest(col)))
            for entry in (data.get("dictionary") or {}).get("entries_without_data") or []:
                units.append(_unit(
                    base + "dictionary/entries_without_data/" + entry.get("name", ""),
                    "xlsx-dictionary-entry", digest(entry),
                    "nome sem dados: entra no denominador"))
        for rel in [r for r in cap_files if r.endswith(".extraction.json")]:
            p = readable[rel]
            workbook = p.name[:-len(".extraction.json")]
            if workbook in drafted:
                continue          # já entrou por coluna; contar folhas duplicaria
            data, state = guarded_read_json(eng, rel, pack)
            if state != "ok" or not isinstance(data, dict):
                diagnostics.append({"level": "error", "blocking": True, "where": rel,
                                    "message": "extracção {} — as folhas desse workbook "
                                               "ficaram fora do denominador"
                                               .format({"unreadable": "ilegível",
                                                        "empty": "vazia",
                                                        "absent": "ausente",
                                                        "refused": "fora da fronteira"}
                                                       .get(state, "malformada"))})
                continue
            for sheet in data.get("sheets") or []:
                units.append(_unit(
                    rel + "#sheets[name=" + sheet.get("name", "") + "]",
                    "xlsx-sheet", digest(sheet),
                    "mesmo nome de folha noutro workbook: chave distinta pelo ficheiro"))
        pm, pm_state = guarded_read(eng, "_capture/process-model.md", pack)
        if "_capture/process-model.md" in readable or pm_state == "refused":
            note_state("_capture/process-model.md", pm_state,
                       "as regras e perguntas do modelo")
        if pm:
            for pid in sorted(set(re.findall(r"\bPM-U-\d{3}\b", pm))):
                units.append(_unit("_capture/process-model.md#" + pid, "process-question",
                                   digest(_id_lines(pm, pid))))
            for pid in sorted(set(re.findall(r"\bPM-\d{3}\b", pm))):
                units.append(_unit("_capture/process-model.md#" + pid, "process-rule",
                                   digest(_id_lines(pm, pid))))
        if "_capture/evidence-index.md" in readable:
            sha, st = guarded_sha256(eng, "_capture/evidence-index.md", pack)
            if st == "ok":
                units.append(_unit("_capture/evidence-index.md", "capture-index", sha))
            else:
                note_state("_capture/evidence-index.md", st, "o índice de evidência")
        for rel in [r for r in cap_files if r.endswith(".replay.md")]:
            sha, st = guarded_sha256(eng, rel, pack)
            if st != "ok":
                note_state(rel, st, "o relatório de replay")
                continue
            units.append(_unit(rel, "replay-report", sha,
                               "limitações de replay entram como limitação, não como "
                               "facto novo"))
        # Tier de texto (.vtt / .docx / .pdf normalizados). UMA unidade por documento,
        # não uma por passagem: 620 excertos de uma gravação são a versão textual de
        # «uma pergunta por célula», e o contrato §6.2 proíbe essa granularidade no
        # Excel pela mesma razão. As passagens continuam CITÁVEIS -- `resolve_target`
        # resolve `#HH:MM:SS` -- porque um locator resolúvel e uma unidade do
        # denominador são coisas diferentes (§5.1 vs §6.1).
        for rel in [r for r in cap_files if r.endswith(".text.md")]:
            body, st = guarded_read(eng, rel, pack)
            if st not in ("ok", "empty"):
                note_state(rel, st, "o documento normalizado")
                continue
            sha, _st = guarded_sha256(eng, rel, pack)
            n = len(re.findall(r"^\[\d{2}:\d{2}:\d{2}", body, re.M)) or \
                len(re.findall(r"^##\s", body, re.M))
            units.append(_unit(
                rel, "text-extraction", sha,
                "{} passagem(ns) determinística(s), citáveis por locator; a unidade é o "
                "documento".format(n)))

    # --------------------------------------------------------- fontes auxiliares §6.1
    for name in AUX_ARTEFACTS:
        sha, st = guarded_sha256(eng, name, pack)
        if st == "ok":
            units.append(_unit(name, "phase-artefact", sha,
                               "fonte auxiliar: não cria verdade mais forte que a SU"))
        elif st != "absent":
            note_state(name, st, "este artefacto de fase")
    for rel in sorted(r for r in readable
                      if r.startswith("lens-outputs/") and r.endswith(".md")):
        sha, st = guarded_sha256(eng, rel, pack)
        if st != "ok":
            note_state(rel, st, "esta saída de lente")
            continue
        units.append(_unit(rel, "lens-output", sha,
                           "fonte auxiliar: não cria verdade mais forte que a SU"))

    dup = _duplicate_keys(units)
    for key in dup:
        diagnostics.append({"level": "error", "where": key,
                            "message": "chave de unidade duplicada — a identidade tem de "
                                       "ser única (contrato §5.2)"})

    blocking = [d for d in diagnostics if d.get("blocking")]
    return {
        "artefact": ARTEFACT,
        "tool": {"name": "coverage.py", "version": TOOL_VERSION},
        "contract_version": CONTRACT_VERSION,
        "engagement": eng.name,
        # Um denominador incompleto não é um denominador. Quem o consome tem de poder
        # saber isso sem reler a lista de diagnósticos.
        "complete": not blocking,
        "blocking_diagnostics": len(blocking),
        "total": len(units),
        "counts_by_class": {c: sum(1 for u in units if u["class"] == c)
                            for c in sorted({u["class"] for u in units})},
        "units": units,
        "excluded": excluded,
        "limitations": limitations,
        "diagnostics": diagnostics,
    }


def _nth_section(md: str, heading_id: str, n: int) -> str:
    """O n-ésimo (1-based) bloco `## <heading_id>...` do ficheiro."""
    hits = []
    for m in re.finditer(r"^##\s+" + re.escape(heading_id) + r"(?:\s|$).*?$",
                         md, re.M):
        nxt = re.search(r"^#{1,6}\s", md[m.end():], re.M)
        hits.append(md[m.start():m.end() + (nxt.start() if nxt else len(md))])
    return hits[n - 1] if 0 < n <= len(hits) else ""


def _id_lines(md: str, ident: str) -> list[str]:
    return [ln.strip() for ln in md.splitlines()
            if re.search(r"\b" + re.escape(ident) + r"\b", ln)]


def _su_row_fp(row: dict) -> dict:
    """Os campos da linha que o fingerprint lê (contrato §6.5)."""
    out = {}
    for f in SU_FP_FIELDS:
        v = row.get(f)
        out[f] = bool(v) if f in ("resolved", "retired") else norm_text(v)
    return out


def _duplicate_keys(units: list[dict]) -> list[str]:
    seen, dup = set(), []
    for u in units:
        if u["unit_key"] in seen:
            dup.append(u["unit_key"])
        seen.add(u["unit_key"])
    return dup


# =============================================================== base e manifesto §6.3

def _manifest_use(rel: str, stage: str, synthesis_authorities: set[str]) -> str | None:
    """`freshness` | `informative` | None (fora do manifesto). Contrato §6.3."""
    if rel in DERIVED_FILES or rel.endswith(DERIVED_SUFFIXES):
        return None
    if any(seg in rel for seg in DERIVED_DIRS):
        return None
    if rel.startswith(COVERAGE_DIR) or rel.startswith(TARGET_DIRS):
        return None
    if rel.startswith(OPERATIONAL_DIRS) or rel.startswith(GRAPH_DIR):
        return None
    if rel.startswith(SYNTHESIS_DIR):
        return "freshness" if (stage == "render" and rel in synthesis_authorities) else None
    if rel in INFORMATIVE:
        return "informative"
    return "freshness"


def _role(rel: str) -> str:
    if rel.startswith("inputs/"):
        return "input"
    if rel.startswith("_capture/"):
        return "capture"
    return "engagement"


def build_manifest(eng: Path, stage: str, synthesis_authorities=()) -> list[dict]:
    """O manifesto de fontes da etapa, ordenado por caminho.

    Inclui o CONJUNTO de ficheiros, não só os digests dos já conhecidos: acrescentar ou
    remover um ficheiro é detectado (§6.3)."""
    eng = eng.resolve()
    pack = engagement_state(eng)[0].get("pack", "")
    wanted = set(synthesis_authorities)
    out = []
    # Os mesmos ficheiros que o inventário viu, pela mesma porta, e hasheados por ela.
    # Um caminho que a fronteira recusa não é lido nem hasheado aqui.
    safe_files, _unsafe = engagement_files(eng)
    for rel, _real in safe_files:
        use = _manifest_use(rel, stage, wanted)
        if use is None:
            continue
        sha, sha_state = guarded_sha256(eng, rel, pack)
        if sha_state != "ok":
            continue
        out.append({"path": rel, "sha256": sha, "role": _role(rel), "use": use})
    return sorted(out, key=lambda e: e["path"])


def su_fingerprint(eng: Path, readers: ReaderAdapter) -> str:
    """Digest semântico da Shared Understanding (contrato §6.4, §6.5).

    Fora ficam **apenas** as linhas que espelham aprovações de blueprint, e os
    cabeçalhos derivados do ficheiro. Nenhuma outra linha `D-*` sai."""
    pack = active_pack(eng)
    md, state = guarded_read(eng, "shared-understanding.md", pack)
    if state != "ok" or not md:
        return digest([])
    _h, rows, _m, _d = readers.parse_su(md)
    skip = approval_ids(eng, readers, pack)
    payload = [_su_row_fp(r) for r in rows if r.get("id") and r["id"] not in skip]
    payload.sort(key=lambda r: (r["state"], r["id"]))
    return digest(payload)


def decision_fingerprint(eng: Path, readers: ReaderAdapter) -> str:
    """Digest semântico da decisão-solução EM VIGOR (contrato §6.4, §6.5).

    Os blocos de aprovação ficam de fora: são lidos à parte, como autoridade humana."""
    md, state = guarded_read(eng, "decisions.md", active_pack(eng))
    if state != "ok" or not md:
        return digest({})
    live = readers.live_solution_decision(md)
    if live is None:
        return digest({})
    block = "\n".join(ln.rstrip() for ln in
                      readers.decision_block_span(md, live["id"]).splitlines())
    return digest({"id": live.get("id", ""),
                   "supersedes": live.get("supersedes", ""),
                   "superseded_by": live.get("superseded_by", ""),
                   "block": block})


def inventory_digest(inventory: dict) -> str:
    """Contrato §6.5: array `{unit_key, class, sha256}` ordenado por `unit_key`."""
    payload = sorted(({"unit_key": u["unit_key"], "class": u["class"],
                       "sha256": u["sha256"]} for u in inventory["units"]),
                     key=lambda u: u["unit_key"])
    return digest(payload)


def _sources_with_graph(eng: Path, stage: str, synthesis_authorities, graph_consumed):
    """As fontes de ficheiro mais, se declarada, a dependência do grafo — ordenadas."""
    fontes = build_manifest(eng, stage, synthesis_authorities)
    dep = graph_dependency(eng, graph_consumed)
    if dep:
        fontes = sorted(fontes + [dep], key=lambda e: e["path"])
    return fontes


def compute_basis(eng: Path, inventory: dict, stage: str, target: dict | None = None,
                  authorities=(), readers: ReaderAdapter | None = None,
                  synthesis_authorities=(), graph_consumed=()) -> dict:
    """A base que uma revisão desta etapa declararia agora (contrato §4.2).

    `target` entra na assinatura porque a etapa o exige, e é validado aqui; a comparação
    do seu digest faz-se em `check_freshness`, junto com o resto da base."""
    if stage not in STAGES:
        raise CoverageError("etapa desconhecida: {!r} (contrato §2)".format(stage), 2)
    if stage == "reconciliation" and target is not None:
        raise CoverageError("etapa `reconciliation` não tem target (contrato §4.6)", 2)
    if stage != "reconciliation" and target is None:
        raise CoverageError("etapa {!r} exige target (contrato §4.6)".format(stage), 2)
    diag_auth: list[dict] = []
    readers = readers or ReaderAdapter()
    eng = eng.resolve()
    # Achado A3: o sha256 de uma autoridade é SEMPRE recalculado a partir do ficheiro.
    # Copiar o valor recebido fazia a base "actual" transportar evidência antiga, e uma
    # alteração de template passava despercebida por essa via. O que o chamador declara
    # é histórico; isto é o presente.
    state = engagement_state(eng)[0]
    pack = state.get("pack", "")
    auth = []
    for a in authorities:
        rel = a.get("path", "") if isinstance(a, dict) else str(a)
        if not str(rel).strip():
            diag_auth.append({"level": "error", "blocking": True, "where": "",
                              "message": "autoridade declarada sem `path`"})
            continue
        sha, sha_state = guarded_sha256(eng, rel, pack)
        auth.append({"path": rel, "sha256": sha,
                     "state": "ok" if sha_state == "ok" else sha_state})
        if sha_state != "ok":
            diag_auth.append({
                "level": "error", "blocking": True, "where": rel,
                "message": {"refused": "autoridade fora da fronteira permitida — "
                                       "recusada sem ler (contrato §5.3)",
                            "absent": "autoridade declarada que não existe",
                            "unreadable": "autoridade que existe e não se lê"}
                           .get(sha_state, "autoridade não lida ({})".format(sha_state))})
    live = readers.live_solution_decision(guarded_read(eng, "decisions.md", pack)[0])
    return {
        "inventory_sha256": inventory_digest(inventory),
        "su_fingerprint": su_fingerprint(eng, readers),
        "decision_fingerprint": decision_fingerprint(eng, readers),
        "sources": _sources_with_graph(eng, stage, synthesis_authorities, graph_consumed),
        "authorities": sorted(auth, key=lambda a: a["path"]),
        "decision_ref": (live or {}).get("id", ""),
        "contract_version": CONTRACT_VERSION,
        "pack": state.get("pack", ""),
        "diagnostics": diag_auth,
    }


def current_target(eng: Path, target: dict | None) -> dict | None:
    """O digest actual do ficheiro alvo, para comparar com o que a revisão declarou."""
    if not target or not target.get("file"):
        return None
    path = safe_path(eng, target["file"])
    if not path.is_file():
        return {"file": target["file"], "sha256": "", "missing": True}
    return {"file": target["file"], "sha256": sha256_file(path), "missing": False}


# ==================================================================== atualidade §6.3

def check_freshness(record: dict, current: dict, target_now: dict | None = None) -> dict:
    """`current` | `stale`, com a razão de cada diferença (contrato §6.3, §6.4).

    Só entram na comparação as fontes com `use: freshness`. As `informative` ficam
    registadas para a auditoria e comparam-se pelos fingerprints — é essa separação que
    impede a aprovação de invalidar a revisão que ela própria consome."""
    old = record.get("basis")
    old = old if isinstance(old, dict) else {}
    if not old:
        return {"status": "not_evaluated", "changed": [], "reasons": [
            "registo sem `basis` — nada para comparar"]}

    changed: list[dict] = []

    for field, label in (("inventory_sha256", "inventário"),
                         ("su_fingerprint", "Shared Understanding"),
                         ("decision_fingerprint", "decisão-solução")):
        if old.get(field) != current.get(field):
            changed.append({"kind": "digest", "what": field,
                            "message": "{} mudou desde a revisão".format(label),
                            "was": old.get(field, ""), "now": current.get(field, "")})

    was = {e["path"]: e for e in _as_list(old.get("sources"))
           if isinstance(e, dict) and e.get("use") == "freshness" and "path" in e}
    now = {e["path"]: e for e in _as_list(current.get("sources"))
           if isinstance(e, dict) and e.get("use") == "freshness" and "path" in e}
    for path in sorted(set(now) - set(was)):
        changed.append({"kind": "source-added", "what": path,
                        "message": "fonte nova depois da revisão"})
    for path in sorted(set(was) - set(now)):
        changed.append({"kind": "source-removed", "what": path,
                        "message": "fonte que a revisão leu desapareceu"})
    for path in sorted(set(was) & set(now)):
        if was[path]["sha256"] != now[path]["sha256"]:
            changed.append({"kind": "source-changed", "what": path,
                            "message": "conteúdo mudou desde a revisão",
                            "was": was[path]["sha256"], "now": now[path]["sha256"]})

    wa = {a["path"]: a.get("sha256") for a in _as_list(old.get("authorities"))
          if isinstance(a, dict) and "path" in a}
    na = {a["path"]: a.get("sha256") for a in _as_list(current.get("authorities"))
          if isinstance(a, dict) and "path" in a}
    for path in sorted(set(wa) | set(na)):
        if wa.get(path) != na.get(path):
            changed.append({"kind": "authority-changed", "what": path,
                            "message": "template ou regra de pacote mudou (T39)",
                            "was": wa.get(path, ""), "now": na.get(path, "")})

    # Achado A5: a versão do contrato NÃO entra em `changed`, porque `changed` decide
    # `stale` e isto não é atualidade — é o motor não saber ler aquele schema. Sai num
    # campo próprio, e quem valida registos (fase 3) traduz para `unsupported`.
    contract_mismatch = None
    if old.get("contract_version") != current.get("contract_version"):
        contract_mismatch = {
            "declared": old.get("contract_version", ""),
            "implemented": current.get("contract_version", ""),
            "verdict": "unsupported",
            "message": "a revisão declara uma versão do contrato que este motor não "
                       "implementa — `contract_validity: unsupported`, nunca lida por "
                       "aproximação e nunca `stale` (T41)",
        }

    tgt = record.get("target")
    tgt = tgt if isinstance(tgt, dict) else None
    if tgt and target_now is not None:
        if target_now.get("missing"):
            changed.append({"kind": "target-missing", "what": tgt.get("file", ""),
                            "message": "o ficheiro alvo desapareceu"})
        elif tgt.get("sha256") and tgt["sha256"] != target_now.get("sha256"):
            changed.append({"kind": "target-changed", "what": tgt.get("file", ""),
                            "message": "o alvo mudou depois da revisão (T21)",
                            "was": tgt.get("sha256", ""),
                            "now": target_now.get("sha256", "")})

    return {
        "status": "stale" if changed else "current",
        "code": COV_STALE if changed else "",
        "contract_version_mismatch": contract_mismatch,
        "changed": changed,
        "reasons": [c["message"] + " — " + str(c["what"]) for c in changed],
        # §6.5: `stale` não prova que uma conclusão ficou falsa; obriga a rever.
        "note": ("stale obriga a rever os impactos e produzir nova revisão; não declara "
                 "falsa nenhuma conclusão" if changed else
                 "a base que a revisão declarou é a base actual"),
    }


# ================================================================== locators §5.1/5.2

_SEG_RE = re.compile(r"^(?P<name>[^\[/]+)(?:\[(?P<disc>[^\]]+)\])?$")


def _segments(selector: str) -> list[dict]:
    out = []
    for raw in selector.split("/"):
        m = _SEG_RE.match(raw)
        if not m:
            return []
        out.append({"name": m.group("name"), "disc": m.group("disc")})
    return out


def _pick(items: list, disc: str | None) -> list:
    """Selecciona pelos discriminadores do contrato §5.1: `chave=valor` ou inteiro."""
    if disc is None:
        return items
    if disc.isdigit():
        i = int(disc)
        return [items[i]] if 0 <= i < len(items) else []
    key, _, val = disc.partition("=")
    hits = []
    for it in items:
        if not isinstance(it, dict):
            continue
        got = it.get(key)
        if isinstance(got, list):
            if val in [str(x) for x in got]:
                hits.append(it)
        elif str(got) == val:
            hits.append(it)
    return hits


def _resolve_yaml(text: str, selector: str, readers: ReaderAdapter) -> dict:
    segs = _segments(selector)
    if not segs:
        return {"count": 0, "reason": "selector malformado"}
    if segs[0]["name"] == "architecture" and len(segs) > 1 and segs[0]["disc"] is None:
        block = readers.yl_find_block(text, segs[1]["name"], "architecture")
        rest, cur_disc = segs[2:], segs[1]["disc"]
    else:
        block = readers.yl_find_block(text, segs[0]["name"])
        rest, cur_disc = segs[1:], segs[0]["disc"]
    if not block:
        return {"count": 0, "reason": "bloco `{}` não existe".format(selector.split("/")[0])}
    nodes = readers.yl_list_of_maps(block)
    hits = _pick(nodes, cur_disc)
    if cur_disc is None and not rest:
        return {"count": 1 if nodes else 0,
                "reason": "" if nodes else "bloco vazio"}
    for seg in rest:
        if len(hits) != 1:
            break
        sub = hits[0].get(seg["name"])
        if not isinstance(sub, list):
            return {"count": 0,
                    "reason": "`{}` não é uma lista neste nó".format(seg["name"])}
        hits = _pick(sub, seg["disc"])
    return {"count": len(hits),
            "reason": "" if len(hits) == 1 else
                      ("nenhum nó corresponde" if not hits else
                       "{} nós correspondem — ambíguo".format(len(hits)))}


_PASSAGE_RE = re.compile(r"^\[(?P<from>\d{2}:\d{2}:\d{2})(?:[–-]\d{2}:\d{2}:\d{2})?\]",
                         re.M)


def _resolve_passage(text: str, selector: str) -> dict:
    """`#HH:MM:SS` -> a passagem que começa nesse instante (contrato §5.1)."""
    hits = [m for m in _PASSAGE_RE.finditer(text) if m.group("from") == selector.strip()]
    if len(hits) == 1:
        return {"count": 1, "reason": ""}
    if not hits:
        return {"count": 0, "reason": "nenhuma passagem começa em {}".format(selector)}
    return {"count": len(hits),
            "reason": "{} passagens começam no mesmo instante — ambíguo".format(len(hits))}


def _resolve_md(text: str, selector: str) -> dict:
    """`A3` = a secção; `A3/<token>` = uma linha dentro dela; `C-007` = uma linha de
    tabela ou uma secção com esse id."""
    head, _, row = selector.partition("/")
    ordinal = 1
    m = re.match(r"^(?P<id>.+?)\[(?P<n>\d+)\]$", head)
    if m:
        head, ordinal = m.group("id"), int(m.group("n"))
    sections = []
    for sm in re.finditer(r"^#{1,6}\s+" + re.escape(head) + r"(?:\s|$).*?$", text, re.M):
        nxt = re.search(r"^#{1,6}\s", text[sm.end():], re.M)
        sections.append(text[sm.end():sm.end() + (nxt.start() if nxt else len(text))])
    if sections:
        if ordinal > len(sections):
            return {"count": 0, "reason": "ordinal {} além das {} secções".format(
                ordinal, len(sections))}
        if len(sections) > 1 and not m:
            return {"count": len(sections),
                    "reason": "{} secções com este id — citar sem ordinal é ambíguo "
                              "(contrato §5.1)".format(len(sections))}
        body = sections[ordinal - 1]
        if not row:
            return {"count": 1, "reason": ""}
        hits = [ln for ln in body.splitlines() if row in ln]
        # §8.2: uma linha que é só um comentário é uma REFERÊNCIA ao requisito, não a sua
        # projecção. Resolve na mesma — é um nó, e existe — e sai marcada, para que seja a
        # regra da âncora a decidir, e não a resolução a mentir.
        return {"count": len(hits),
                "comment_only": len(hits) == 1 and bool(COMMENT_LINE.match(hits[0])),
                "reason": "" if len(hits) == 1 else
                          ("nenhuma linha contém {!r}".format(row) if not hits else
                           "{} linhas contêm {!r} — ambíguo".format(len(hits), row))}
    rows = [ln for ln in text.splitlines()
            if re.search(r"^\|\s*" + re.escape(head) + r"\s*\|", ln)]
    if rows:
        return {"count": len(rows),
                "reason": "" if len(rows) == 1 else
                          "{} linhas com este id — ambíguo".format(len(rows))}
    return {"count": 0, "reason": "nenhuma secção nem linha com este id"}


def _resolve_json(data, selector: str) -> dict:
    segs = _segments(selector)
    if not segs:
        return {"count": 0, "reason": "selector malformado"}
    cur = data
    for i, seg in enumerate(segs):
        if isinstance(cur, dict) and seg["name"] in cur:
            cur = cur[seg["name"]]
        elif isinstance(cur, dict) and seg["disc"] is None and i == len(segs) - 1:
            return {"count": 0, "reason": "campo `{}` não existe".format(seg["name"])}
        elif isinstance(cur, list):
            # `<Folha>/<Coluna>` sobre um rascunho de campos
            hits = [x for x in cur if isinstance(x, dict)
                    and str(x.get("name", x.get("column", ""))) == seg["name"]]
            if len(hits) != 1:
                return {"count": len(hits),
                        "reason": "nenhum" if not hits else "ambíguo"}
            cur = hits[0]
            continue
        else:
            return {"count": 0, "reason": "campo `{}` não existe".format(seg["name"])}
        if seg["disc"] is not None:
            if not isinstance(cur, list):
                return {"count": 0,
                        "reason": "`{}` não é uma lista".format(seg["name"])}
            hits = _pick(cur, seg["disc"])
            if len(hits) != 1:
                return {"count": len(hits),
                        "reason": "nenhum nó corresponde" if not hits else "ambíguo"}
            cur = hits[0]
    return {"count": 1, "reason": ""}


def _resolve_fields_draft(data: dict, selector: str) -> dict:
    """`<Folha>/<Coluna>` e `dictionary/entries_without_data/<Nome>`."""
    parts = selector.split("/")
    if parts[:2] == ["dictionary", "entries_without_data"] and len(parts) == 3:
        hits = [e for e in (data.get("dictionary") or {}).get("entries_without_data") or []
                if e.get("name") == parts[2]]
        return {"count": len(hits), "reason": "" if len(hits) == 1 else "nenhum ou ambíguo"}
    if len(parts) >= 2:
        col = parts[-1]
        sheet_name = "/".join(parts[:-1])
        for sheet in data.get("sheets") or []:
            if sheet.get("name") != sheet_name:
                continue
            hits = [c for c in sheet.get("columns") or [] if c.get("column") == col]
            return {"count": len(hits),
                    "reason": "" if len(hits) == 1 else
                              "coluna `{}` não existe na folha `{}`".format(col, sheet_name)}
        return {"count": 0, "reason": "folha `{}` não existe".format(sheet_name)}
    return {"count": 0, "reason": "selector malformado"}


def resolve_target(eng: Path, target: dict, readers: ReaderAdapter | None = None) -> dict:
    """Resolve `{file, selector}` para EXACTAMENTE um nó (contrato §5.1).

    Zero, ou mais do que um, nunca é um fallback silencioso: devolve o código."""
    readers = readers or ReaderAdapter()
    rel = (target or {}).get("file", "")
    selector = (target or {}).get("selector", "")
    try:
        path = safe_path(eng, rel)
    except CoverageError as exc:
        return {"ok": False, "count": 0, "code": COV_INVALID_TARGET,
                "reason": str(exc)}
    if not path.is_file():
        return {"ok": False, "count": 0, "code": COV_INVALID_TARGET,
                "reason": "ficheiro não existe: {}".format(rel)}
    if not selector:
        return {"ok": True, "count": 1, "code": "", "reason": ""}
    try:
        if path.suffix in (".yaml", ".yml"):
            res = _resolve_yaml(_read(path), selector, readers)
        elif path.name.endswith(".fields-draft.json"):
            res = _resolve_fields_draft(_read_json(path) or {}, selector)
        elif path.suffix == ".json":
            res = _resolve_json(_read_json(path), selector)
        elif path.name.endswith(".text.md") and re.fullmatch(r"\d{2}:\d{2}:\d{2}",
                                                            selector.strip()):
            res = _resolve_passage(_read(path), selector)
        else:
            res = _resolve_md(_read(path), selector)
    except Exception as exc:                                        # noqa: BLE001
        return {"ok": False, "count": 0, "code": COV_UNEXPECTED,
                "reason": "falha a resolver {!r}: {}".format(selector, type(exc).__name__)}
    count = res["count"]
    if count == 1:
        return {"ok": True, "count": 1, "code": "", "reason": "",
                "comment_only": bool(res.get("comment_only"))}
    code = COV_DEAD_REF if count > 1 else COV_INVALID_TARGET
    return {"ok": False, "count": count, "code": code, "reason": res["reason"]}


def resolve_unit(eng: Path, unit_key: str, readers: ReaderAdapter | None = None) -> dict:
    """Resolve uma chave de unidade `<caminho>[#<selector>]`."""
    rel, _, selector = unit_key.partition("#")
    return resolve_target(eng, {"file": rel, "selector": selector}, readers)


# ==================================================== registos: leitura e selecção §3

_RECORD_RE = re.compile(r"^coverage_v(\d{2,4})\.json$")
_BP_VER_RE = re.compile(r"_v(\d{2,4})\.(?:yaml|yml)$")


def record_files(eng: Path) -> list[str]:
    """Os registos de `_coverage/`, pela lista JÁ VALIDADA — nunca por `glob`.

    Achado A7 da fase 2: um `glob` volta a enumerar o disco e dá a volta à fronteira."""
    ok, _bad = engagement_files(eng)
    return sorted(rel for rel, _p in ok
                  if rel.startswith(COVERAGE_DIR)
                  and _RECORD_RE.match(rel.rsplit("/", 1)[-1]))


def _version_num(version: str) -> int:
    m = re.match(r"^v(\d+)$", str(version or ""))
    return int(m.group(1)) if m else -1


def load_records(eng: Path, pack: str | None = None) -> list[dict]:
    """Todos os registos de `_coverage/`, por ordem de versão.

    Um registo ilegível **não desaparece**: entra com o seu estado, para que a ausência de
    revisão e a revisão que não se lê sejam resultados diferentes (contrato §6.6)."""
    out = []
    for rel in record_files(eng):
        name = rel.rsplit("/", 1)[-1]
        data, state = guarded_read_json(eng, rel, pack)
        rec = data if isinstance(data, dict) else None
        if state == "ok" and rec is None:
            state = "unreadable"          # JSON válido que não é um objecto
        out.append({"file": rel, "name": name,
                    "version": "v" + _RECORD_RE.match(name).group(1),
                    "record": rec, "state": state})
    return sorted(out, key=lambda e: _version_num(e["version"]))


def target_identity(eng: Path, stage: str, target_file: str) -> str:
    """A identidade do alvo, a partir do nome do ficheiro (contrato §4.6).

    `_blueprint/ux-blueprint_v03.yaml` -> `v03`;
    `_render/<slug>_solution-blueprint_v02.md` -> `solution-blueprint_v02`."""
    name = str(target_file or "").rsplit("/", 1)[-1]
    if stage == "blueprint":
        m = _BP_VER_RE.search(name)
        return "v" + m.group(1) if m else ""
    if stage == "render":
        stem = re.sub(r"\.[A-Za-z0-9]+$", "", name)
        slug = engagement_state(eng)[0].get("engagement", "")
        if slug and stem.startswith(slug + "_"):
            stem = stem[len(slug) + 1:]
        return stem
    return ""


def _cannot_situate(rec: dict | None, identity_of=None) -> str:
    """Porque é que este registo não se consegue situar, ou `""` quando se consegue.

    Situar é saber **a que par (etapa, alvo) pertence**. Enquanto não se souber, ele pode
    ser a revisão mais recente do par que está a ser avaliado, e ignorá-lo é escolher a
    anterior porque convém. Contrato §6.6: cada um destes é impeditivo, em todas as
    etapas — não só na que o registo diria ser a sua."""
    if rec is None:
        return "não se lê (JSON inválido ou não é um objecto)"
    # A versão do schema NÃO entra aqui. Situar é só saber a que par pertence, e para
    # isso bastam `stage` e `target.identity`; se elas lá estiverem, o registo é
    # seleccionado e a validação traduz a versão desconhecida para `unsupported`
    # (§6.6, T41). Bloquear aqui transformaria `unsupported` em `invalid`, que são
    # coisas diferentes. Se nem essas chaves tem — `{}` ou um schema que lhes mudou o
    # nome — não se situa, e aí bloqueia.
    stage = rec.get("stage")
    if stage not in STAGES:
        return "declara a etapa {!r}, que não existe".format(stage)
    if stage != "reconciliation":
        tgt = rec.get("target")
        if not isinstance(tgt, dict):
            return ("é da etapa {!r} e o seu `target` não é um mapa ({})"
                    .format(stage, type(tgt).__name__))
        if not str(tgt.get("identity") or "").strip():
            return ("é da etapa {!r} e não diz a que versão se aplica (`target.identity` "
                    "ausente)".format(stage))
        if not str(tgt.get("file") or "").strip():
            return ("é da etapa {!r} e não diz que ficheiro reviu (`target.file` ausente)"
                    .format(stage))
        if identity_of is not None:
            want = identity_of(stage, str(tgt["file"]))
            if want and str(tgt["identity"]) != want:
                # Mente sobre si próprio: diz rever uma versão e aponta para outra. Sem
                # isto ficava apenas fora de toda a selecção -- seguro, e INVISÍVEL.
                return ("diz rever {!r} e aponta para {!r}, que é {!r}"
                        .format(tgt["identity"], tgt["file"], want))
    return ""


def select_record(eng: Path, stage: str, identity: str | None = None,
                  records=None, pack: str | None = None,
                  target_file: str | None = None) -> dict:
    """Contrato §6.6: etapa + identidade do target + autoridade; vale a MAIS RECENTE.

    Uma revisão mais antiga **nunca** é escolhida para esconder que a mais recente do
    mesmo par (etapa, target) falhou — se falhou, é a que se reporta (T23).

    A identidade **e** o ficheiro têm de bater. Cruzar só a identidade deixava uma
    revisão da `v03` com `identity: "v01"` escrito à mão passar por revisão da `v01`:
    o digest do alvo confere (é o da `v03`, e o registo aponta para a `v03`), a
    identidade confere (foi trocada), e o ficheiro revisto não é o que se pediu."""
    entries = load_records(eng, pack) if records is None else records
    cands = []
    for e in entries:
        rec = e["record"]
        # PRIMEIRO situar, só DEPOIS filtrar. Filtrar por `stage` antes de saber se o
        # registo se consegue situar deixava passar tudo o que não tem etapa legível --
        # `{}`, um `schema_version` desconhecido, uma etapa inventada, um registo de
        # desenho sem alvo. Todos «não eram desta etapa», todos desapareciam em silêncio,
        # e a revisão anterior ficava a valer: falso verde pela porta do lado.
        why = _cannot_situate(rec, lambda st, f: target_identity(eng, st, f))
        if why:
            cands.append(dict(e, match="undetermined", why=why))
            continue
        if rec.get("stage") != stage:
            continue
        tgt = _as_dict(rec.get("target"))
        if identity is not None and (tgt.get("identity") or "") != identity:
            continue
        if target_file is not None and (tgt.get("file") or "") != target_file:
            # Mesma identidade, outro ficheiro: não é a revisão deste alvo.
            continue
        cands.append(dict(e, match="ok"))
    typed = [c for c in cands if c["match"] == "ok"]
    broken = [c for c in cands if c["match"] != "ok"]
    typed.sort(key=lambda e: _version_num(e["version"]))
    selected = typed[-1] if typed else None
    return {
        "selected": selected,
        "superseded": typed[:-1] if typed else [],
        "unreadable": broken,          # os que não se conseguem situar — impeditivos
        "stage": stage,
        "identity": identity,
    }


# ======================================================== validação de registos §4

def _as_dict(value) -> dict:
    """O mapa, ou um mapa vazio. **Nunca** rebenta por o registo trazer outro tipo.

    Um registo é dado, não código: `target: "bad"` ou `basis: "x"` têm de sair como
    diagnóstico de schema e saída 2, nunca como `COV-UNEXPECTED` e saída 5 sem JSON
    nenhum. Quem valida a forma é `_check_root`; isto garante que se chega lá."""
    return value if isinstance(value, dict) else {}


def _as_list(value) -> list:
    """A lista, ou uma lista vazia. Uma string **não** é uma lista de caracteres aqui."""
    return value if isinstance(value, list) else []


def _diag(code: str, severity: str, message: str, file: str = "", locator: str = "",
          item: str = "", resolves: str = "") -> dict:
    """A forma única do diagnóstico (plano §8.1): `{code, severity, file, locator,
    item, message, resolves}`. `resolves` diz o que o fecha, não o que o causou."""
    return {"code": code, "severity": severity, "file": file, "locator": locator,
            "item": item, "message": message, "resolves": resolves}


ASSESSMENTS = ("reviewed", "unverifiable", "not_applicable")
MATERIALITY = ("material", "not-material", "undetermined")
DISPOSITIONS = ("preserve", "change", "retire", "clarify")
STATUSES = ("covered", "partial", "missing", "excluded")
ROLES = ("su_row", "decision", "implementation", "projection", "open_choice",
         "proof_obligation")
# §4.4.3: a âncora que `covered` exige, por etapa. Um papel fora da etapa NÃO é erro
# próprio: simplesmente não conta como âncora, e é a regra de `covered` que o apanha.
ANCHOR_ROLE = {"blueprint": "implementation", "render": "projection"}
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}(?::\d{2})?"
                  r"(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?)?$")
ROOT_FIELDS = ("schema_version", "version", "engagement", "stage", "generated_at",
               "based_on", "target", "deliverable", "basis", "source_review",
               "coverage", "semantic_review")


def obligation_identity(item: dict) -> tuple:
    """Contrato §4.4.4: a identidade que atravessa etapas é o conjunto ORDENADO dos
    `requirement_refs`. O `id` do item é local ao registo e não atravessa nada."""
    refs = _as_list(item.get("requirement_refs"))
    return tuple(sorted({str(r) for r in refs if str(r).strip()}))


def record_context(eng: Path, inventory: dict, readers: ReaderAdapter | None = None,
                   pack: str | None = None) -> dict:
    """O que a validação precisa de saber sobre o engagement, lido uma vez.

    Os ids de requisito resolvem contra a SU e as decisões, **não** contra o inventário:
    a §6.1 tira do inventário o registo de uma aprovação, e resolver por lá faria de um
    id legítimo uma referência morta."""
    readers = readers or ReaderAdapter()
    pack = active_pack(eng) if pack is None else pack
    su_md = guarded_read(eng, "shared-understanding.md", pack)[0]
    dec_md = guarded_read(eng, "decisions.md", pack)[0]
    rows = readers.parse_su(su_md)[1] if su_md else []
    return {
        "identity_of": lambda stage, f: target_identity(eng, stage, f),
        "su_ids": {r["id"] for r in rows if r.get("id")},
        "decision_ids": set(re.findall(r"^##\s+(D-\d{2,4})\b", dec_md or "", re.M)),
        "unit_keys": {u["unit_key"] for u in inventory.get("units", [])},
        "limitation_units": {l["unit_key"] for l in inventory.get("limitations", [])},
        "engagement": engagement_state(eng)[0].get("engagement", ""),
        "pack": pack,
    }


def _check_root(rec: dict, filename: str | None, ctx: dict, diags: list) -> str:
    """Campos de raiz (§4.1). Devolve `valid` | `invalid` | `unsupported`."""
    sv = rec.get("schema_version")
    if sv != SCHEMA_VERSION:
        diags.append(_diag(COV_SCHEMA, "error",
                           "o registo declara `schema_version: {!r}`; este motor "
                           "implementa {} — não é lido por aproximação"
                           .format(sv, SCHEMA_VERSION),
                           resolves="produzir a revisão com o schema implementado"))
        return "unsupported"
    bad = False
    for field in ("version", "engagement", "stage", "generated_at", "basis",
                  "source_review", "coverage", "semantic_review"):
        if field not in rec:
            diags.append(_diag(COV_SCHEMA, "error",
                               "campo obrigatório ausente: `{}`".format(field)))
            bad = True
    if "based_on" not in rec:
        diags.append(_diag(COV_SCHEMA, "error", "campo obrigatório ausente: `based_on` "
                                                "(pode ser vazio, nunca ausente)"))
        bad = True
    if "target" not in rec:
        diags.append(_diag(COV_SCHEMA, "error", "campo obrigatório ausente: `target` "
                                                "(`null` em reconciliation)"))
        bad = True
    for field, kind in (("based_on", list), ("source_review", list),
                        ("coverage", list), ("basis", dict), ("semantic_review", dict)):
        if field in rec and not isinstance(rec[field], kind):
            diags.append(_diag(COV_SCHEMA, "error",
                               "`{}` tem de ser {}, e é {}"
                               .format(field, kind.__name__,
                                       type(rec[field]).__name__)))
            bad = True
    if "target" in rec and rec["target"] is not None \
            and not isinstance(rec["target"], dict):
        diags.append(_diag(COV_SCHEMA, "error",
                           "`target` tem de ser um mapa ou `null`, e é {}"
                           .format(type(rec["target"]).__name__)))
        bad = True
    mine = _version_num(str(rec.get("version", "")))
    for i, name in enumerate(_as_list(rec.get("based_on"))):
        if not isinstance(name, str) or not name.strip():
            diags.append(_diag(COV_SCHEMA, "error",
                               "`based_on[{}]` tem de ser o nome de um registo, e é {}"
                               .format(i, type(name).__name__)))
            bad = True
            continue
        m = _RECORD_RE.match(name.rsplit("/", 1)[-1])
        if not m:
            diags.append(_diag(COV_SCHEMA, "error",
                               "`based_on[{}]` não tem a forma `coverage_vNN.json`: {!r}"
                               .format(i, name)))
            bad = True
            continue
        # Só versões ESTRITAMENTE ANTERIORES. Mata a auto-referência e qualquer ciclo por
        # construção -- as versões são imutáveis e crescem, por isso uma cadeia que só
        # aponta para trás não pode fechar-se sobre si própria. Verificar «não sou eu» e
        # deixar o resto obrigava a percorrer o grafo à procura de ciclos; isto não.
        if mine > 0 and int(m.group(1)) >= mine:
            diags.append(_diag(COV_SCHEMA, "error",
                               "`based_on` só pode citar versões anteriores: {} cita {}"
                               .format(rec.get("version"), name), file=name,
                               resolves="corrigir a cadeia — uma revisão não se baseia em "
                                        "si própria nem no que veio depois"))
            bad = True
    stage = rec.get("stage")
    if stage not in STAGES:
        diags.append(_diag(COV_SCHEMA, "error",
                           "etapa desconhecida: {!r} (contrato §2)".format(stage)))
        bad = True
    if not _ISO.match(str(rec.get("generated_at", ""))):
        diags.append(_diag(COV_SCHEMA, "error",
                           "`generated_at` não é uma data ISO-8601: {!r}"
                           .format(rec.get("generated_at"))))
        bad = True
    if filename is not None:
        m = _RECORD_RE.match(filename.rsplit("/", 1)[-1])
        want = "v" + m.group(1) if m else ""
        if want and rec.get("version") != want:
            diags.append(_diag(COV_SCHEMA, "error",
                               "`version: {!r}` não corresponde ao ficheiro {!r}"
                               .format(rec.get("version"), filename),
                               file=filename))
            bad = True
    if ctx.get("engagement") and rec.get("engagement") != ctx["engagement"]:
        diags.append(_diag(COV_SCHEMA, "error",
                           "`engagement: {!r}` não é o deste engagement ({!r})"
                           .format(rec.get("engagement"), ctx["engagement"])))
        bad = True
    tgt = rec.get("target") if isinstance(rec.get("target"), (dict, type(None))) else None
    if stage == "reconciliation" and tgt not in (None, {}):
        diags.append(_diag(COV_SCHEMA, "error",
                           "`reconciliation` não tem target (contrato §4.6)"))
        bad = True
    if stage in ("blueprint", "render"):
        if not isinstance(tgt, dict) or not tgt.get("file"):
            diags.append(_diag(COV_SCHEMA, "error",
                               "a etapa {!r} exige `target` com `file` (§4.6)"
                               .format(stage)))
            bad = True
        else:
            for f in ("kind", "identity", "sha256"):
                if not str(tgt.get(f, "")).strip():
                    diags.append(_diag(COV_SCHEMA, "error",
                                       "`target.{}` ausente (§4.6)".format(f)))
                    bad = True
            if tgt.get("sha256") and not _HEX64.match(str(tgt["sha256"])):
                diags.append(_diag(COV_SCHEMA, "error",
                                   "`target.sha256` não é um digest sha256"))
                bad = True
            want = ctx.get("identity_of", lambda _s, _f: "")(stage, str(tgt.get("file")))
            if want and tgt.get("identity") and tgt["identity"] != want:
                diags.append(_diag(COV_SCHEMA, "error",
                                   "`target.identity: {!r}` não é a identidade do "
                                   "ficheiro que o registo diz ter revisto ({!r} → {!r})"
                                   .format(tgt.get("identity"), tgt.get("file"), want),
                                   file=str(tgt.get("file", "")),
                                   resolves="corrigir a identidade, ou o ficheiro"))
                bad = True
    if stage == "render" and not isinstance(rec.get("deliverable"), dict):
        diags.append(_diag(COV_SCHEMA, "error",
                           "a etapa `render` exige o bloco `deliverable` (§4.5)"))
        bad = True
    if stage != "render" and rec.get("deliverable") is not None:
        diags.append(_diag(COV_SCHEMA, "error",
                           "`deliverable` só existe na etapa `render` (§4.5)"))
        bad = True
    seen = [f for f in rec if f not in ROOT_FIELDS]
    for field in sorted(seen):
        diags.append(_diag(COV_SCHEMA, "warn",
                           "campo de raiz desconhecido, não lido: `{}`".format(field),
                           resolves="retirar o campo ou levá-lo ao contrato"))
    bo = rec.get("based_on")
    if isinstance(bo, list):
        names = [n for n in bo if isinstance(n, str)]
        if len(set(names)) != len(names):
            diags.append(_diag(COV_SCHEMA, "error", "`based_on` tem entradas repetidas"))
            bad = True
        if stage == "blueprint" and not bo:
            diags.append(_diag(COV_SCHEMA, "error",
                               "a etapa `blueprint` referencia ≥1 registo de "
                               "`reconciliation` em `based_on` (§4.6)"))
            bad = True
        if stage == "render" and not bo:
            diags.append(_diag(COV_SCHEMA, "error",
                               "a etapa `render` referencia ≥1 registo anterior em "
                               "`based_on` (§4.6)"))
            bad = True
        # §4.6: não basta citar alguma coisa -- tem de se citar uma revisão DA ETAPA que
        # o contrato exige. Uma cadeia só de desenhos nunca tocou na reconciliação.
        chain = ctx.get("chain") or {}
        if chain and stage in ("blueprint", "render"):
            want = "reconciliation" if stage == "blueprint" else ("blueprint",
                                                                  "reconciliation")
            stages = {(_as_dict(chain.get(n)).get("stage") or "")
                      for n in bo if isinstance(n, str)}
            need = {want} if isinstance(want, str) else set(want)
            if not (stages & need):
                diags.append(_diag(COV_SCHEMA, "error",
                                   "`based_on` não cita nenhuma revisão de {} (§4.6); "
                                   "cita {}".format(" nem ".join(sorted(need)),
                                                    ", ".join(sorted(stages)) or "nada"),
                                   resolves="citar a revisão a montante que esta etapa "
                                            "consome"))
                bad = True
    return "invalid" if bad else "valid"


def _check_basis(rec: dict, diags: list, ctx: dict | None = None) -> bool:
    basis = rec.get("basis")
    if not isinstance(basis, dict):
        return False
    ok = True
    # O pacote sob o qual a revisão foi feita decide contra que templates e regras as
    # autoridades se resolvem. Declarado diferente do activo, a revisão fala de outro
    # conjunto de contratos -- e o snapshot não se corrige sozinho (§4.2).
    now = (ctx or {}).get("pack") or ""
    was = str(basis.get("pack", "")).strip()
    if now and was and was != now:
        diags.append(_diag(COV_STALE, "error",
                           "a revisão foi feita com o pacote `{}` e o activo é `{}`: as "
                           "autoridades que ela diz ter lido são as de outro conjunto de "
                           "contratos (§4.2)".format(was, now),
                           resolves="rever com o pacote activo"))
        ok = False
    for field in ("inventory_sha256", "su_fingerprint", "decision_fingerprint"):
        if not _HEX64.match(str(basis.get(field, ""))):
            diags.append(_diag(COV_SCHEMA, "error",
                               "`basis.{}` não é um digest sha256".format(field)))
            ok = False
    for field in ("decision_ref", "contract_version", "pack"):
        if field not in basis:
            diags.append(_diag(COV_SCHEMA, "error",
                               "`basis.{}` ausente (§4.2)".format(field)))
            ok = False
    if basis.get("decision_ref") and not re.match(r"^D-\d{2,4}$",
                                                  str(basis["decision_ref"])):
        diags.append(_diag(COV_SCHEMA, "error",
                           "`basis.decision_ref` não tem a forma `D-NNN`: {!r}"
                           .format(basis["decision_ref"])))
        ok = False
    for name, req in (("sources", ("path", "sha256", "role", "use")),
                      ("authorities", ("path", "sha256"))):
        seq = basis.get(name)
        if not isinstance(seq, list):
            diags.append(_diag(COV_SCHEMA, "error",
                               "`basis.{}` tem de ser lista (§4.2)".format(name)))
            ok = False
            continue
        for entry in seq:
            if not isinstance(entry, dict) or any(f not in entry for f in req):
                diags.append(_diag(COV_SCHEMA, "error",
                                   "entrada de `basis.{}` sem {}".format(
                                       name, "/".join("`%s`" % f for f in req))))
                ok = False
                continue
            if not _HEX64.match(str(entry.get("sha256", ""))):
                diags.append(_diag(COV_SCHEMA, "error",
                                   "`basis.{}[{}].sha256` não é um digest"
                                   .format(name, entry.get("path", "")),
                                   file=str(entry.get("path", ""))))
                ok = False
            if name == "sources" and entry.get("use") not in ("freshness", "informative"):
                diags.append(_diag(COV_SCHEMA, "error",
                                   "`use` de {!r} tem de ser `freshness` ou "
                                   "`informative` (§6.3)".format(entry.get("path", "")),
                                   file=str(entry.get("path", ""))))
                ok = False
            if name == "sources" and entry.get("role") not in ("input", "capture",
                                                               "engagement"):
                diags.append(_diag(COV_SCHEMA, "error",
                                   "`role` de {!r} fora de input/capture/engagement"
                                   .format(entry.get("path", "")),
                                   file=str(entry.get("path", ""))))
                ok = False
    return ok


def _check_source_review(rec: dict, ctx: dict, eng: Path | None,
                         readers: ReaderAdapter | None, diags: list) -> dict:
    """§4.3. Devolve `{units, by_unit, ids, ok}` para as regras que dependem disto."""
    entries = rec.get("source_review")
    entries = entries if isinstance(entries, list) else []
    units: set[str] = set()
    by_unit: dict[str, dict] = {}
    ids: set[str] = set()
    ok = True
    for i, sr in enumerate(entries):
        where = "source_review[{}]".format(i)
        if not isinstance(sr, dict):
            diags.append(_diag(COV_SCHEMA, "error",
                               "{} não é um mapa".format(where), item=where))
            ok = False
            continue
        sid = str(sr.get("id", "")).strip()
        where = sid or where
        if not sid:
            diags.append(_diag(COV_SCHEMA, "error", "entrada de revisão sem `id`",
                               item=where))
            ok = False
        elif sid in ids:
            diags.append(_diag(COV_SCHEMA, "error",
                               "`id` repetido em `source_review`: {}".format(sid),
                               item=sid))
            ok = False
        ids.add(sid)
        refs = sr.get("unit_refs")
        if refs is not None and not isinstance(refs, list):
            # Uma string é iterável e daria uma unidade por CARÁCTER. Tipo errado é erro
            # de FORMA (§4.3), não revisão pobre: são coisas diferentes (D36).
            diags.append(_diag(COV_SCHEMA, "error",
                               "`unit_refs` tem de ser lista, e é {}"
                               .format(type(refs).__name__), item=where))
            ok = False
            refs = []
        elif not refs:
            diags.append(_diag(COV_REVIEW_INCOMPLETE, "error",
                               "entrada de revisão sem `unit_refs` (§4.3 exige ≥1)",
                               item=where,
                               resolves="enumerar as unidades que esta entrada cobre"))
            ok = False
            refs = []
        assessment = sr.get("assessment")
        if assessment not in ASSESSMENTS:
            diags.append(_diag(COV_REVIEW_INCOMPLETE, "error",
                               "`assessment: {!r}` fora de {} (§4.3)"
                               .format(assessment, "/".join(ASSESSMENTS)), item=where))
            ok = False
        materiality = sr.get("materiality", "undetermined")
        if materiality not in MATERIALITY:
            diags.append(_diag(COV_REVIEW_INCOMPLETE, "error",
                               "`materiality: {!r}` fora de {} (§4.3)"
                               .format(materiality, "/".join(MATERIALITY)), item=where))
            ok = False
            materiality = "undetermined"
        if not str(sr.get("rationale", "")).strip():
            diags.append(_diag(COV_REVIEW_INCOMPLETE, "error",
                               "entrada de revisão sem `rationale` (§4.3)", item=where,
                               resolves="escrever o julgamento, nem que seja uma linha"))
            ok = False
        links = sr.get("links")
        if not isinstance(links, dict) or any(
                not isinstance(links.get(k), list)
                for k in ("su_refs", "coverage_items", "obligations")):
            diags.append(_diag(COV_SCHEMA, "error",
                               "`links` tem de trazer as três listas `su_refs`, "
                               "`coverage_items` e `obligations` (§4.3)", item=where))
            ok = False
        if assessment == "unverifiable":
            lim = sr.get("limitation")
            if not isinstance(lim, dict) or any(
                    not str(lim.get(k, "")).strip()
                    for k in ("reason", "impact", "action")):
                diags.append(_diag(COV_CAPTURE_LIMIT, "error",
                                   "`unverifiable` exige `limitation` com `reason`, "
                                   "`impact` e `action` (§4.3)", item=where,
                                   resolves="escrever o motivo, o impacto e a acção"))
                ok = False
        for ref in refs:
            ref = str(ref)
            units.add(ref)
            by_unit[ref] = {"id": sid, "assessment": assessment,
                            "materiality": materiality}
            if ctx["unit_keys"] and ref not in ctx["unit_keys"]:
                diags.append(_diag(COV_DEAD_REF, "error",
                                   "unidade que não existe no inventário: {}".format(ref),
                                   locator=ref, item=where,
                                   resolves="corrigir a chave ou retirar a entrada"))
                ok = False
            elif ref in ctx["limitation_units"] and assessment != "unverifiable":
                diags.append(_diag(COV_CAPTURE_LIMIT, "error",
                                   "{} é uma fonte sem extractor: é `unverifiable` com "
                                   "limitação, nunca {!r} — falta de extractor não é "
                                   "não-aplicabilidade (§4.3)".format(ref, assessment),
                                   locator=ref, item=where,
                                   resolves="declarar `unverifiable` com `limitation`"))
                ok = False
    return {"units": units, "by_unit": by_unit, "ids": ids, "ok": ok}


def _resolve_refs(eng: Path | None, readers, item_targets, diags, where, stage,
                  target_file: str = ""):
    """Resolve os `targets[]` de um item e devolve os papéis que RESOLVERAM.

    Um destino com o papel-âncora da etapa tem de estar **no ficheiro que a revisão diz
    estar a rever**. Sem isto, uma revisão da `v01` podia provar a sua cobertura com nós
    da `v03`: os locators resolvem (a `v03` existe e tem-nos), o alvo confere, e o que se
    está a dar por coberto não está lá."""
    roles: list[str] = []
    anchor = ANCHOR_ROLE.get(stage, "")
    for j, tgt in enumerate(item_targets or []):
        loc = "targets[{}]".format(j)
        if not isinstance(tgt, dict) or not tgt.get("file"):
            diags.append(_diag(COV_SCHEMA, "error",
                               "target sem `file` (§4.4.2)", item=where, locator=loc))
            continue
        role = tgt.get("role")
        if role not in ROLES:
            diags.append(_diag(COV_SCHEMA, "error",
                               "`role: {!r}` fora da tabela da §4.4.2".format(role),
                               item=where, locator=loc))
            continue
        locator = tgt["file"] + ("#" + tgt["selector"] if tgt.get("selector") else "")
        if eng is None:
            roles.append(role)
            continue
        if anchor and role == anchor and target_file \
                and str(tgt["file"]) != target_file:
            diags.append(_diag(COV_AUTHORITY_MISMATCH, "error",
                               "o destino que devia provar a cobertura está noutro "
                               "artefacto ({}) e não no que esta revisão diz rever ({})"
                               .format(tgt["file"], target_file),
                               file=str(tgt["file"]), locator=locator, item=where,
                               resolves="apontar para o nó da versão revista, ou rever "
                                        "a versão onde o nó está"))
            continue                    # não conta como âncora: está noutra versão
        res = resolve_target(eng, tgt, readers)
        if res["ok"] and res.get("comment_only") and anchor and role == anchor:
            # §8.2: «um id num comentário não prova preservação semântica». O nó existe,
            # e é por isso que isto não é um locator morto: o que não existe é a
            # projecção. Não conta como âncora, e a §4.4.3 apanha o `covered`.
            diags.append(_diag(COV_INVALID_TARGET, "error",
                               "o destino é uma linha de comentário: um id citado em "
                               "comentário é uma referência ao requisito, não a sua "
                               "projecção (§8.2)",
                               file=str(tgt["file"]), locator=locator, item=where,
                               resolves="projectar a obrigação no corpo do documento, ou "
                                        "declarar o item como `partial`/`missing`"))
            continue
        if res["ok"]:
            roles.append(role)
            continue
        message = ("o locator resolve para {} nós, e tem de resolver para exactamente "
                   "um: {}".format(res["count"], res["reason"]) if res["count"] > 1 else
                   "o locator não resolve: {}".format(res["reason"]))
        diags.append(_diag(res["code"], "error", message,
                           file=tgt["file"], locator=locator, item=where,
                           resolves="corrigir o desenho ou a ligação"))
    return roles


def _check_coverage(rec: dict, ctx: dict, eng: Path | None, readers, sr: dict,
                    diags: list) -> dict:
    """§4.4. Devolve as obrigações tratadas e as lacunas."""
    stage = rec.get("stage")
    items = rec.get("coverage")
    items = items if isinstance(items, list) else []
    ids: set[str] = set()
    handled: dict[tuple, dict] = {}
    gaps: list[dict] = []
    ok = True
    for i, item in enumerate(items):
        where = "coverage[{}]".format(i)
        if not isinstance(item, dict):
            diags.append(_diag(COV_SCHEMA, "error", "{} não é um mapa".format(where),
                               item=where))
            ok = False
            continue
        iid = str(item.get("id", "")).strip()
        where = iid or where
        if not iid:
            diags.append(_diag(COV_SCHEMA, "error", "item sem `id`", item=where))
            ok = False
        elif iid in ids:
            diags.append(_diag(COV_SCHEMA, "error",
                               "`id` repetido em `coverage`: {}".format(iid), item=iid))
            ok = False
        ids.add(iid)
        refs = item.get("requirement_refs")
        if refs is not None and not isinstance(refs, list):
            diags.append(_diag(COV_SCHEMA, "error",
                               "`requirement_refs` tem de ser lista, e é {}"
                               .format(type(refs).__name__), item=where))
            ok = False
            refs = []
        elif not refs:
            diags.append(_diag(COV_REVIEW_INCOMPLETE, "error",
                               "item sem `requirement_refs` (§4.4 exige ≥1)", item=where))
            ok = False
            refs = []
        for ref in refs:
            if ctx["su_ids"] or ctx["decision_ids"]:
                if str(ref) not in ctx["su_ids"] and str(ref) not in ctx["decision_ids"]:
                    diags.append(_diag(COV_DEAD_REF, "error",
                                       "requisito que não existe na Shared Understanding "
                                       "nem nas decisões: {}".format(ref),
                                       locator=str(ref), item=where,
                                       resolves="corrigir o id ou escrever a linha"))
                    ok = False
        if item.get("source_unit_refs") is not None \
                and not isinstance(item.get("source_unit_refs"), list):
            diags.append(_diag(COV_SCHEMA, "error",
                               "`source_unit_refs` tem de ser lista, e é {}"
                               .format(type(item["source_unit_refs"]).__name__),
                               item=where))
            ok = False
        for ref in _as_list(item.get("source_unit_refs")):
            if ctx["unit_keys"] and str(ref) not in ctx["unit_keys"]:
                diags.append(_diag(COV_DEAD_REF, "error",
                                   "unidade de origem que não existe no inventário: {}"
                                   .format(ref), locator=str(ref), item=where,
                                   resolves="corrigir a chave da unidade"))
                ok = False
        disposition = item.get("disposition")
        if disposition not in DISPOSITIONS:
            diags.append(_diag(COV_SCHEMA, "error",
                               "`disposition: {!r}` fora de {} (§4.4)"
                               .format(disposition, "/".join(DISPOSITIONS)), item=where))
            ok = False
        scope = item.get("scope_basis_refs")
        if not isinstance(scope, list):
            diags.append(_diag(COV_SCHEMA, "error",
                               "`scope_basis_refs` tem de ser lista (pode ser vazia)",
                               item=where))
            ok = False
            scope = []
        assessment = item.get("assessment")
        if not isinstance(assessment, dict) or assessment.get("status") not in STATUSES:
            diags.append(_diag(COV_REVIEW_INCOMPLETE, "error",
                               "item sem `assessment.status` válido — campo ausente é "
                               "revisão incompleta, nunca `missing` por defeito (§4.4)",
                               item=where,
                               resolves="declarar o estado e escrever o julgamento"))
            ok = False
            continue
        status = assessment["status"]
        if not str(assessment.get("rationale", "")).strip():
            diags.append(_diag(COV_REVIEW_INCOMPLETE, "error",
                               "`assessment.rationale` vazio (§4.4)", item=where))
            ok = False
        unresolved = item.get("unresolved_refs")
        if not isinstance(unresolved, list):
            diags.append(_diag(COV_SCHEMA, "error",
                               "`unresolved_refs` tem de ser lista (pode ser vazia)",
                               item=where))
            ok = False
            unresolved = []
        if status != "covered":
            for field in ("required_action", "responsible_role"):
                if not str(item.get(field, "")).strip():
                    diags.append(_diag(COV_REVIEW_INCOMPLETE, "error",
                                       "`{}` é obrigatório quando o estado não é "
                                       "`covered` (§4.4)".format(field), item=where,
                                       resolves="dizer o que falta e a que papel toca"))
                    ok = False
        if unresolved and status == "covered":
            diags.append(_diag(COV_REVIEW_INCOMPLETE, "error",
                               "`covered` com `unresolved_refs` preenchido: um item que "
                               "ainda aponta para algo por resolver é, no máximo, "
                               "`partial` (§4.4)", item=where))
            ok = False
        if item.get("targets") is not None and not isinstance(item.get("targets"), list):
            diags.append(_diag(COV_SCHEMA, "error", "`targets` tem de ser lista",
                               item=where))
            ok = False
            roles = []
        else:
            n0 = len(diags)
            roles = _resolve_refs(eng, readers, item.get("targets"), diags, where, stage,
                                  str(_as_dict(rec.get("target")).get("file") or ""))
            ok = ok and len(diags) == n0
        # §4.4.3 -- a âncora que `covered` exige, e que muda com a etapa.
        if status == "covered":
            if stage == "reconciliation":
                anchored = any(str(r) in ctx["su_ids"] or str(r) in ctx["decision_ids"]
                               for r in refs)
                if not anchored:
                    diags.append(_diag(COV_MISSING_TARGET, "error",
                                       "`covered` em reconciliação exige um requisito que "
                                       "resolva para uma linha da Shared Understanding ou "
                                       "um bloco de decisão (§4.4.3)", item=where))
                    ok = False
            else:
                want = ANCHOR_ROLE[stage]
                if want not in roles:
                    diags.append(_diag(COV_MISSING_TARGET, "error",
                                       "`covered` sem destino `role: {}` que resolva — "
                                       "uma ligação a uma pergunta, a uma prova futura ou "
                                       "a um nó decorativo não é cobertura (§4.4.3)"
                                       .format(want), item=where,
                                       resolves="apontar para o nó que concretiza a "
                                                "obrigação, ou baixar o estado"))
                    ok = False
        # §4.4.1 -- autoridade de âmbito, pela positiva.
        if status == "excluded" or disposition in ("retire", "change"):
            linked = [str(u) for u in _as_list(item.get("source_unit_refs"))]
            mats = [sr["by_unit"].get(u, {}).get("materiality", "undetermined")
                    for u in linked]
            if not linked or "undetermined" in mats:
                diags.append(_diag(COV_REVIEW_INCOMPLETE, "error",
                                   "retirar ou alterar uma obrigação sem que a "
                                   "materialidade das unidades ligadas esteja declarada: "
                                   "desconhecer a materialidade não é o mesmo que saber "
                                   "que a unidade não é material (§4.4.1)", item=where,
                                   resolves="ligar as unidades e declarar a materialidade"))
                ok = False
            elif "material" in mats and not scope:
                diags.append(_diag(COV_EXCLUSION_NO_DECISION, "error",
                                   "obrigação material retirada ou alterada sem "
                                   "autoridade de âmbito (§4.4.1)", item=where,
                                   resolves="citar a decisão que autoriza a remoção"))
                ok = False
        for ref in scope:
            if ctx["su_ids"] or ctx["decision_ids"]:
                if str(ref) not in ctx["su_ids"] and str(ref) not in ctx["decision_ids"]:
                    diags.append(_diag(COV_DEAD_REF, "error",
                                       "autoridade de âmbito que não resolve: {}"
                                       .format(ref), locator=str(ref), item=where))
                    ok = False
        # §8: uma fonte sem extractor nunca vira coberta por omissão.
        if status == "covered":
            for u in _as_list(item.get("source_unit_refs")):
                if str(u) in ctx["limitation_units"]:
                    diags.append(_diag(COV_CAPTURE_LIMIT, "error",
                                       "obrigação declarada coberta a partir de uma fonte "
                                       "que não se consegue ler ({}) — o limite de captura "
                                       "mostra-se, nunca se transforma em cobertura"
                                       .format(u), locator=str(u), item=where))
                    ok = False
        if status in ("partial", "missing"):
            gaps.append({"item": iid, "status": status,
                         "requirement_refs": list(refs),
                         "required_action": str(item.get("required_action", "")).strip(),
                         "responsible_role": str(item.get("responsible_role", "")).strip()})
            diags.append(_diag(COV_KNOWN_GAP, "warn",
                               "lacuna declarada ({}) sobre {}"
                               .format(status, ", ".join(str(r) for r in refs)),
                               item=where,
                               resolves=str(item.get("required_action", "")).strip()))
        handled[obligation_identity(item)] = {
            "item": iid, "status": status, "disposition": disposition,
            "scope_basis_refs": list(scope), "refs": set(str(r) for r in refs),
        }
    return {"handled": handled, "gaps": gaps, "ids": ids, "ok": ok}


def _check_links(rec: dict, ctx: dict, cov: dict, diags: list) -> bool:
    """§4.3 — `links` liga uma entrada de revisão ao que ela alimenta. Uma ligação para o
    que não existe é uma referência morta, como qualquer outra: um item que foi apagado,
    uma linha da SU que não há. É a protecção que o PRÓPRIO revisor tem contra o
    esvaziamento posterior do registo — quando a preenche."""
    ok = True
    known_ids = ctx.get("su_ids", set()) | ctx.get("decision_ids", set())
    for sr in _as_list(rec.get("source_review")):
        if not isinstance(sr, dict):
            continue
        links = _as_dict(sr.get("links"))
        where = str(sr.get("id") or "")
        for ref in _as_list(links.get("coverage_items")):
            if str(ref) not in cov["ids"]:
                diags.append(_diag(COV_DEAD_REF, "error",
                                   "`links.coverage_items` aponta para um item que não "
                                   "existe no registo: {}".format(ref),
                                   locator=str(ref), item=where,
                                   resolves="corrigir a ligação ou repor o item"))
                ok = False
        for field in ("su_refs", "obligations"):
            for ref in _as_list(links.get(field)):
                if known_ids and str(ref) not in known_ids:
                    diags.append(_diag(COV_DEAD_REF, "error",
                                       "`links.{}` aponta para um id que não existe na "
                                       "Shared Understanding nem nas decisões: {}"
                                       .format(field, ref), locator=str(ref), item=where,
                                       resolves="corrigir o id"))
                    ok = False
    return ok


def _check_not_hollow(rec: dict, sr: dict, cov: dict, diags: list) -> bool:
    """Um registo sem uma única obrigação tratada, sobre um denominador com unidades
    materiais lidas, não é uma revisão que encontrou «nada a preservar» — é uma revisão
    por acabar. Zero obrigações só é coerente quando nenhuma unidade foi declarada
    material. Não decide QUAIS unidades geram obrigações (isso é do revisor, §9); decide
    que material lido e nenhuma obrigação não podem ser verdade ao mesmo tempo."""
    if cov["handled"]:
        return True
    material = [u for u, info in sr["by_unit"].items()
                if info.get("materiality") == "material"
                and info.get("assessment") == "reviewed"]
    if not material:
        return True
    diags.append(_diag(COV_REVIEW_INCOMPLETE, "error",
                       "nenhuma obrigação tratada em `coverage[]`, com {} unidade(s) "
                       "declarada(s) material(is) e lida(s) — ou não há nada a preservar, "
                       "e então nada é material, ou a revisão não acabou"
                       .format(len(material)),
                       resolves="escrever as obrigações, ou declarar as unidades "
                                "não-materiais com razão"))
    return False


def _check_inheritance(rec: dict, chain: dict, cov: dict, diags: list) -> dict:
    """§4.4.4 — nenhuma obrigação desaparece entre etapas.

    A única subtracção legítima é a de `render`, declarada em `deliverable.not_selected`.

    Devolve DOIS veredictos, porque são duas coisas: `structural` é erro de contrato
    (`based_on` que não resolve, subtracção onde não a há) e torna o registo inválido;
    `review` é revisão incompleta (uma obrigação que se perdeu) e deixa o registo válido
    e a cobertura com lacunas. Misturar os dois faria de um requisito perdido um erro de
    ficheiro, e um requisito perdido é exactamente o que este mecanismo existe para ver."""
    stage = rec.get("stage")
    if stage == "reconciliation":
        return {"structural": True, "review": True}
    upstream: dict[tuple, dict] = {}
    ok = True
    structural = True
    for name in _as_list(rec.get("based_on")):
        if not isinstance(name, str):
            continue                    # já reportado como erro de schema em `_check_root`
        up = chain.get(name)
        if up is None:
            diags.append(_diag(COV_SCHEMA, "error",
                               "`based_on` nomeia um registo que não existe ou não se lê: "
                               "{}".format(name), file=name,
                               resolves="corrigir a ligação ou publicar o registo"))
            ok = structural = False
            continue
        for item in _as_list(_as_dict(up).get("coverage")):
            if isinstance(item, dict):
                ident = obligation_identity(item)
                if ident:
                    upstream[ident] = {
                        "status": (item.get("assessment") or {}).get("status", ""),
                        "disposition": item.get("disposition", ""),
                        "scope_basis_refs": list(item.get("scope_basis_refs") or []),
                        "from": name}
    not_selected = {}
    if stage == "render":
        for entry in _as_list(_as_dict(rec.get("deliverable")).get("not_selected")):
            if isinstance(entry, dict):
                ident = tuple(sorted({str(r) for r in
                                      _as_list(entry.get("requirement_refs"))}))
                if not str(entry.get("reason", "")).strip():
                    diags.append(_diag(COV_REVIEW_INCOMPLETE, "error",
                                       "`not_selected` sem razão escrita: ausência "
                                       "declarada exige a razão (§4.4.4)",
                                       item="deliverable.not_selected"))
                    ok = False
                not_selected[ident] = entry
    for ident, up in sorted(upstream.items()):
        label = ", ".join(ident)
        if ident in not_selected:
            continue
        down = cov["handled"].get(ident)
        if down is None:
            merged = [h for h in cov["handled"].values() if set(ident) <= h["refs"]]
            down = merged[0] if merged else None
        if down is None:
            diags.append(_diag(COV_UNREVIEWED, "error",
                               "obrigação herdada de {} que este registo não trata: {} — "
                               "é assim que um requisito se perde entre etapas (§4.4.4)"
                               .format(up["from"], label), locator=label,
                               resolves="tratar a obrigação, ou declará-la em "
                                        "`not_selected` quando o contrato de projecção "
                                        "não a selecciona"))
            ok = False
            continue
        if up["status"] == "excluded" and down["status"] == "excluded" \
                and up["scope_basis_refs"] and not down["scope_basis_refs"]:
            diags.append(_diag(COV_EXCLUSION_NO_DECISION, "error",
                               "exclusão herdada que perdeu a autoridade que a permitia "
                               "({}): uma exclusão autorizada continua a citá-la (§4.4.4)"
                               .format(label), locator=label, item=down["item"]))
            ok = False
    if stage == "blueprint":
        for _entry in _as_list(_as_dict(rec.get("deliverable")).get("not_selected")):
            diags.append(_diag(COV_SCHEMA, "error",
                               "não existe subtracção legítima na etapa `blueprint` "
                               "(§4.4.4)"))
            ok = structural = False
    return {"structural": structural, "review": ok}


def _check_semantic(rec: dict, cov: dict, diags: list) -> str:
    sem = rec.get("semantic_review")
    if not isinstance(sem, dict):
        diags.append(_diag(COV_REVIEW_INCOMPLETE, "error",
                           "`semantic_review` ausente (§4.7)"))
        return "pending"
    status = sem.get("status")
    if status not in ("completed", "pending", "not_started"):
        diags.append(_diag(COV_REVIEW_INCOMPLETE, "error",
                           "`semantic_review.status: {!r}` fora de completed/pending/"
                           "not_started (§4.7)".format(status)))
        return "pending"
    who = sem.get("performed_by")
    if not isinstance(who, dict) or who.get("kind") not in ("agent", "human") \
            or not str(who.get("name", "")).strip():
        diags.append(_diag(COV_REVIEW_INCOMPLETE, "error",
                           "`performed_by` exige `kind` (agent|human) e `name` — o autor "
                           "é o executor efectivo, nunca o sponsor inferido (§4.7)"))
        status = "pending" if status == "completed" else status
    if not isinstance(sem.get("limitations"), list):
        diags.append(_diag(COV_REVIEW_INCOMPLETE, "error",
                           "`limitations` é obrigatória; vazia é uma afirmação, ausente "
                           "é uma omissão (§4.7)"))
        status = "pending" if status == "completed" else status
    passes = sem.get("passes")
    if status == "completed":
        if not isinstance(passes, dict) or passes.get("source_to_target") is not True \
                or passes.get("target_to_source") is not True:
            diags.append(_diag(COV_REVIEW_INCOMPLETE, "error",
                               "`completed` exige as duas passagens declaradas em "
                               "`passes` (§4.7, §9)"))
            status = "pending"
        if not str(sem.get("method", "")).strip():
            diags.append(_diag(COV_REVIEW_INCOMPLETE, "error",
                               "`completed` exige `method` (§4.7)"))
            status = "pending"
        if not _ISO.match(str(sem.get("completed_at", ""))):
            diags.append(_diag(COV_REVIEW_INCOMPLETE, "error",
                               "`completed` exige `completed_at` em ISO-8601 (§4.7)"))
            status = "pending"
    # `findings` é condição de `completed`, não do registo: uma revisão em curso ainda não
    # tem os achados todos, e exigi-los dela seria acusar duas vezes a mesma pendência.
    if status == "completed":
        findings = set(str(f) for f in _as_list(sem.get("findings")))
        for _ident, h in sorted(cov["handled"].items()):
            if h["status"] in ("partial", "missing", "excluded")                     and h["item"] not in findings:
                diags.append(_diag(COV_REVIEW_INCOMPLETE, "error",
                                   "item {} está {} e não consta de "
                                   "`semantic_review.findings` (§4.7)"
                                   .format(h["item"], h["status"]), item=h["item"],
                                   resolves="nomear o achado na revisão semântica"))
                status = "pending"
    return "pending" if status == "not_started" else status


def _check_deliverable(rec: dict, eng: Path | None, chain: dict, diags: list,
                       readers=None, cov: dict | None = None) -> dict:
    """§4.5 e §8.3 — a versão de autoridade que a projecção diz ter lido.

    Três perguntas distintas, e nenhuma responde pela outra: o bloco está bem formado; a
    versão declarada é a que o TEMPLATE manda ler; e a revisão a montante que se consome é
    a dessa mesma versão. A segunda é a que faltava: sem ela, um registo coerente consigo
    próprio podia ler a versão autorizada onde o contrato exige a aprovada."""
    if rec.get("stage") != "render":
        return {"structural": True, "review": True, "applicability": "",
                "expected_version": None}
    dl = rec.get("deliverable")
    if not isinstance(dl, dict):
        return {"structural": False, "review": False, "applicability": "",
                "expected_version": None}
    ok = True
    structural = True
    for field in ("id", "template", "template_sha256", "authority_sources",
                  "blueprint_version_read", "not_selected"):
        if field not in dl:
            diags.append(_diag(COV_SCHEMA, "error",
                               "`deliverable.{}` ausente (§4.5)".format(field)))
            ok = structural = False
    if dl.get("template_sha256") and not _HEX64.match(str(dl["template_sha256"])):
        diags.append(_diag(COV_SCHEMA, "error",
                           "`deliverable.template_sha256` não é um digest"))
        ok = structural = False
    if not isinstance(dl.get("authority_sources"), list) \
            or not isinstance(dl.get("not_selected"), list):
        diags.append(_diag(COV_SCHEMA, "error",
                           "`authority_sources` e `not_selected` são listas (§4.5)"))
        ok = structural = False
    read = dl.get("blueprint_version_read")
    if read is not None:
        for name in rec.get("based_on") or []:
            up = chain.get(name)
            if not isinstance(up, dict) or up.get("stage") != "blueprint":
                continue
            ident = (up.get("target") or {}).get("identity", "")
            if ident and read != ident:
                diags.append(_diag(COV_AUTHORITY_MISMATCH, "error",
                                   "a projecção diz ter lido o desenho {} e consome a "
                                   "revisão de {}, que é do desenho {} (§8.3)"
                                   .format(read, name, ident), file=name,
                                   resolves="rever contra a versão que o deliverable "
                                            "lê, ou consumir a revisão dessa versão"))
                ok = False   # autoridade errada NÃO é erro de ficheiro
    applicability = ""
    app = dl.get("applicability")
    if app is not None:
        if not isinstance(app, dict) or app.get("state") not in APPLICABILITY:
            diags.append(_diag(COV_SCHEMA, "error",
                               "`deliverable.applicability.state` fora de {} (§4.5)"
                               .format("/".join(APPLICABILITY))))
            ok = structural = False
        else:
            applicability = app["state"]
            if not str(app.get("reason", "")).strip():
                diags.append(_diag(COV_REVIEW_INCOMPLETE, "error",
                                   "`applicability: {}` exige `reason` — ausência "
                                   "legítima é declarada, nunca silenciosa (§8.2)"
                                   .format(applicability),
                                   resolves="escrever a razão da aplicabilidade"))
                ok = False
    # ---- A: o ficheiro revisto é deste deliverable? (§4.6: identidade é `<id>_vNN`)
    # `id` e `template` podem concordar um com o outro e nenhum deles com o ALVO. É o
    # mesmo defeito por outra porta: a revisão diz ser de um deliverable e revê o
    # documento de outro.
    ident = str(_as_dict(rec.get("target")).get("identity", "")).strip()
    did = str(dl.get("id", "")).strip()
    if ident and did and not ident.startswith(did + "_"):
        diags.append(_diag(COV_AUTHORITY_MISMATCH, "error",
                           "a revisão diz ser do deliverable `{}` e o documento que revê "
                           "é `{}` (§4.5, §4.6)".format(did, ident),
                           file=str(_as_dict(rec.get("target")).get("file", "")),
                           resolves="rever o documento deste deliverable, ou corrigir o "
                                    "`id` do registo"))
        ok = False

    # ---- G: o que não se produz não projectou nada
    # A aplicabilidade é declarada, e o motor não a deriva (§8.2) -- mas um registo que
    # diz que o deliverable não se produz e ao mesmo tempo dá obrigações por projectadas
    # contradiz-se a si próprio, e isso vê-se sem derivar nada.
    if applicability in ("not_applicable", "blocked"):
        covered = sorted(h["item"] for h in (cov or {}).get("handled", {}).values()
                         if h.get("status") == "covered")
        if covered:
            diags.append(_diag(COV_REVIEW_INCOMPLETE, "error",
                               "o registo declara o deliverable `{}` e mesmo assim dá {} "
                               "obrigação(ões) por projectada(s) ({}): um documento que "
                               "não se produz não projecta nada (§8.2)"
                               .format(applicability, len(covered),
                                       ", ".join(covered[:5])),
                               resolves="corrigir a aplicabilidade, ou retirar as "
                                        "obrigações dadas por cobertas"))
            ok = False

    expected = None
    if eng is not None and dl.get("template") and dl.get("template_sha256"):
        sha, state = guarded_sha256(eng, str(dl["template"]))
        if state != "ok":
            # Era um aviso, e o aviso era o buraco: sem ler o template, a identidade e a
            # versão de autoridade ficam ambas por verificar, e o registo passava por
            # essa porta. O caminho de erro é o que menos pode ser permissivo.
            diags.append(_diag(COV_SCHEMA, "error",
                               "o template declarado não se lê ({}): {} — sem ele não há "
                               "como confirmar de quem é o contrato de projecção nem que "
                               "versão ele manda ler (§8.3)"
                               .format(state, dl["template"]), file=str(dl["template"]),
                               resolves="apontar para um template do pacote activo"))
            ok = False
        elif sha != dl["template_sha256"]:
            diags.append(_diag(COV_STALE, "error",
                               "o template do deliverable mudou depois da revisão (T39)",
                               file=str(dl["template"]),
                               resolves="rever contra o template actual"))
            ok = False
    # ---- B: o template consumido entra na base, ou a atualidade fica cega
    # `basis.authorities` é o que `check_freshness` recalcula e compara. Um template fora
    # dessa lista pode mudar sem que a revisão alguma vez fique stale por essa via (§4.2).
    if dl.get("template"):
        listed = {str(_as_dict(a).get("path", ""))
                  for a in _as_list(_as_dict(rec.get("basis")).get("authorities"))}
        # Sem `listed and`: a lista vazia é precisamente o caso a apanhar. Numa revisão de
        # `render` o template é sempre consumido, por isso nunca pode faltar aqui — e um
        # guarda que tolerasse a lista vazia deixava passar a versão mais limpa do defeito.
        if str(dl["template"]) not in listed:
            diags.append(_diag(COV_SCHEMA, "error",
                               "o template `{}` foi consumido e não consta de "
                               "`basis.authorities`: a atualidade da revisão não repara "
                               "numa alteração a ele (§4.2)".format(dl["template"]),
                               file=str(dl["template"]),
                               resolves="declarar o template nas autoridades da base"))
            ok = False

    # §8.3: a versão que o TEMPLATE manda ler, resolvida agora. `COV-AUTHORITY-MISMATCH`
    # é o código quando a projecção leu outra -- e a ausência de versão é razão, não
    # lacuna: um deliverable cuja autoridade ainda não existe está bloqueado, não em falta.
    if eng is not None and dl.get("template"):
        auth = template_authority(eng, str(dl["template"]))
        # §8.3, e primeiro de tudo: o contrato de projecção que a revisão leu é mesmo o
        # DESTE deliverable? Sem esta pergunta, `deliverable.id` é decorativo e a revisão
        # de uma especificação apoiada no template de arquitectura herda `v<latest
        # authorized>` -- sai completa sem existir versão aprovada nenhuma.
        declared_id = str(dl.get("id", "")).strip()
        tid = (auth.get("template_id") or "").strip()
        if auth["state"] == "ok" and declared_id and tid and declared_id != tid:
            diags.append(_diag(COV_AUTHORITY_MISMATCH, "error",
                               "a revisão diz ser do deliverable `{}` e o template que "
                               "leu é o de `{}` ({}) — cada deliverable é revisto contra "
                               "o seu próprio contrato de projecção, e a versão de "
                               "autoridade vem de lá (§8.3)"
                               .format(declared_id, tid, dl["template"]),
                               file=str(dl["template"]),
                               resolves="rever contra o template de `{}`, ou corrigir o "
                                        "`id` do registo".format(declared_id)))
            ok = False
            auth = dict(auth, known=False, token=None, why="wrong-template")
        elif auth["state"] == "ok" and declared_id and not tid:
            diags.append(_diag(COV_SCHEMA, "error",
                               "o template não declara `template_id` (§8.3): não há como "
                               "confirmar que é o contrato de projecção de `{}`"
                               .format(declared_id), file=str(dl["template"]),
                               resolves="declarar `template_id` no template"))
            ok = False
            auth = dict(auth, known=False, token=None, why="no-template-id")
        if auth["state"] == "ok" and auth.get("why") in ("wrong-template", "no-template-id"):
            pass                 # já acusado acima; não se acusa duas vezes o mesmo facto
        elif auth["state"] == "ok":
            if not auth["known"]:
                diags.append(_diag(COV_SCHEMA, "error",
                                   "o template não declara uma versão de autoridade "
                                   "legível em `blueprint_version_read` (§8.3)",
                                   file=str(dl["template"]),
                                   resolves="declarar o token no template"))
                ok = False
            else:
                exp = expected_version(blueprint_versions(eng, readers), auth["token"])
                expected = exp
                declared = read if read is None else str(read)
                want = exp.get("version")
                if auth["token"] is not None and want is None \
                        and applicability not in ("not_applicable", "blocked"):
                    # A autoridade exigida não existe, e o registo mesmo assim revê um
                    # documento produzido. Quem declara `not_applicable`/`blocked` já disse
                    # que ele não se produziu, e não é acusado outra vez aqui.
                    diags.append(_diag(COV_AUTHORITY_MISMATCH, "error",
                                       "o contrato deste deliverable lê `{}` e não existe "
                                       "nenhuma ({}): o documento não podia ser produzido "
                                       "sem a sua autoridade, e declarar que não se leu "
                                       "versão nenhuma não a substitui (§8.2, §8.3)"
                                       .format(auth["declared"], exp["reason"]),
                                       file=str(dl["template"]),
                                       resolves="declarar a aplicabilidade "
                                                "(`blocked`/`not_applicable`) ou obter a "
                                                "versão que o contrato exige"))
                    ok = False
                elif auth["token"] is None and declared is not None:
                    diags.append(_diag(COV_AUTHORITY_MISMATCH, "error",
                                       "a revisão diz ter lido o desenho {} e este "
                                       "deliverable não lê versão nenhuma (§8.3)"
                                       .format(declared), file=str(dl["template"]),
                                       resolves="pôr `blueprint_version_read: null` no "
                                                "registo, ou rever o deliverable certo"))
                    ok = False
                elif auth["token"] is not None and declared != want:
                    diags.append(_diag(COV_AUTHORITY_MISMATCH, "error",
                                       "o contrato deste deliverable lê `{}` = {} e a "
                                       "revisão diz ter lido {} (§8.3){}".format(
                                           auth["declared"], want or "nenhuma versão",
                                           declared or "nenhuma",
                                           "" if want else " — " + exp["reason"]),
                                       file=str(dl["template"]),
                                       resolves="rever contra a versão que o contrato "
                                                "manda ler"))
                    ok = False
    return {"structural": structural, "review": ok, "applicability": applicability,
            "expected_version": expected}


def _no_verdict(validity: str, diags: list) -> dict:
    """O resultado de uma validação que não chegou a acontecer — com as MESMAS chaves.

    Uma saída antecipada com menos chaves do que a normal faz o consumidor rebentar
    exactamente no caminho de erro, que é onde ele menos pode rebentar."""
    return {"contract_validity": validity, "diagnostics": diags, "handled": {},
            "gaps": [], "source_units": set(), "source_review_ok": False,
            "coverage_ok": False, "semantic_review": "not_evaluated",
            "inheritance_ok": False, "deliverable_ok": False}


def validate_record(record: dict, inventory: dict, eng: Path | None = None,
                    readers: ReaderAdapter | None = None, chain: dict | None = None,
                    filename: str | None = None, context: dict | None = None) -> dict:
    """Valida um registo contra o contrato §4 e devolve veredicto + diagnósticos.

    `contract_validity` é **recalculado** em cada leitura: um `valid: true` escrito no
    ficheiro não é veredicto de ninguém (contrato §3)."""
    diags: list[dict] = []
    if not isinstance(record, dict):
        return _no_verdict("invalid", [
            _diag(COV_SCHEMA, "error", "o registo não é um objecto JSON")])
    readers = readers or ReaderAdapter()
    ctx = context or (record_context(eng, inventory, readers) if eng is not None else
                      {"su_ids": set(), "decision_ids": set(),
                       "unit_keys": {u["unit_key"] for u in inventory.get("units", [])},
                       "limitation_units": {l["unit_key"] for l in
                                            inventory.get("limitations", [])},
                       "engagement": "", "pack": ""})
    validity = _check_root(record, filename, ctx, diags)
    if validity == "unsupported":
        # Não se lê por aproximação: nada deste registo é interpretado a seguir.
        return _no_verdict("unsupported", diags)
    basis_ok = _check_basis(record, diags, ctx)
    sr = _check_source_review(record, ctx, eng, readers, diags)
    cov = _check_coverage(record, ctx, eng, readers, sr, diags)
    _check_links(record, ctx, cov, diags)
    _check_not_hollow(record, sr, cov, diags)
    inh = _check_inheritance(record, chain or {}, cov, diags)
    dl = _check_deliverable(record, eng, chain or {}, diags, readers, cov)
    sem = _check_semantic(record, cov, diags)
    # Erro de contrato é forma: campos, tipos, ligações da §4.6. Uma revisão POBRE é
    # válida como registo e incompleta como revisão -- não se misturam os dois.
    schema_errors = [d for d in diags
                     if d["code"] == COV_SCHEMA and d["severity"] == "error"]
    if validity == "valid" and (schema_errors or not basis_ok
                                or not inh["structural"] or not dl["structural"]):
        validity = "invalid"
    return {"contract_validity": validity, "diagnostics": diags,
            "handled": cov["handled"], "gaps": cov["gaps"],
            "source_units": sr["units"], "source_review_ok": sr["ok"],
            "coverage_ok": cov["ok"], "semantic_review": sem,
            "inheritance_ok": inh["review"], "deliverable_ok": dl["review"]}


# ========================================================== resultado computado §7

def _unreviewed_units(inventory: dict, seen: set, diags: list) -> int:
    missing = sorted({u["unit_key"] for u in inventory.get("units", [])} - set(seen))
    for key in missing:
        diags.append(_diag(COV_UNREVIEWED, "error",
                           "unidade do inventário sem tratamento: {}".format(key),
                           locator=key,
                           resolves="rever a unidade, ou declará-la não aplicável com "
                                    "razão escrita"))
    return len(missing)


def structural_check(eng: Path, rel: str, readers: ReaderAdapter | None = None) -> dict:
    """A verificação estrutural que já existe, sobre o desenho alvo (contrato §8.1.4).

    Não substitui nem duplica `bp_validate`: chama-o. Uma versão que falha a estrutura
    continua não aprovável, e a cobertura não a salva."""
    readers = readers or ReaderAdapter()
    text, state = guarded_read(eng, rel)
    if state != "ok":
        return {"evaluated": False, "state": state, "blocking": 0, "warn": 0,
                "issues": []}
    su_md = guarded_read(eng, "shared-understanding.md")[0]
    su_ids = {r["id"] for r in readers.parse_su(su_md)[1] if r.get("id")} if su_md \
        else None
    try:
        issues = readers.bp_validate(text, rel.rsplit("/", 1)[-1],
                                     readers.bp_pack_cfg(active_pack(eng)), su_ids,
                                     readers.bp_loader(eng))
    except Exception as exc:                                        # noqa: BLE001
        return {"evaluated": False, "state": "error:" + type(exc).__name__,
                "blocking": 0, "warn": 0, "issues": []}
    nb = sum(1 for i in issues if i.get("severity") == "block")
    return {"evaluated": True, "state": "ok", "blocking": nb,
            "warn": len(issues) - nb, "issues": issues}


def template_path_for(pack: str, deliverable_id: str) -> str:
    """O caminho do template daquele deliverable, pela convenção do pacote (§5.3).

    Convenção, não nome de caso: `<pacote>/deliverable-templates/<id>.template.md`. Quem
    chamar pode passar o caminho explicitamente e esta função não é usada."""
    return "library/packs/{}/deliverable-templates/{}.template.md".format(
        pack, deliverable_id)


def _fm_value(line: str) -> str:
    """O valor de um campo de frontmatter: sem comentário de fim de linha, sem aspas."""
    return line.split(":", 1)[1].split("#", 1)[0].strip().strip('"\'')


def template_authority(eng: Path, template_rel: str, pack: str | None = None) -> dict:
    """Que versão do desenho é que ESTE template declara ler (§8.3).

    O template declara, no campo `blueprint_version_read` do seu frontmatter; o motor
    traduz o token e verifica. Um template que não declara nada lê-se como «não lê
    nenhuma versão de desenho» -- e isso é uma afirmação sobre o deliverable, não um
    defeito: o Discovery Report não lê desenho nenhum."""
    text_, state = guarded_read(eng, template_rel, pack)
    if state != "ok":
        return {"state": state, "declared": None, "token": None, "known": False,
                "template_id": None, "file": template_rel}
    raw = None
    tid = None
    lines = text_.splitlines()
    # Só o frontmatter: uma menção ao campo no corpo do template é prosa, não declaração.
    body = lines[1:] if lines and lines[0].strip() == "---" else lines
    for line in body:
        if line.strip() == "---":
            break
        if raw is None and line.startswith("blueprint_version_read:"):
            raw = _fm_value(line)
        elif tid is None and line.startswith("template_id:"):
            # A identidade que o template dá a si próprio. É contra esta que o `id` do
            # registo tem de bater: sem isso, um registo diz ser de um deliverable e herda
            # a autoridade de versão de outro.
            tid = _fm_value(line)
    key = (raw or "").strip().lower()
    if raw is None:
        # Ausente NÃO se lê como «não lê desenho nenhum»: seria a leitura errada em
        # silêncio, exactamente no campo que decide qual a versão de autoridade. Quem não
        # lê desenho declara-o (`none`), e quem lê declara qual.
        return {"state": "ok", "declared": None, "token": None, "known": False,
                "why": "absent", "template_id": tid, "file": template_rel}
    if key not in VERSION_TOKENS:
        return {"state": "ok", "declared": raw, "token": None, "known": False,
                "why": "unknown-token", "template_id": tid, "file": template_rel}
    return {"state": "ok", "declared": raw, "token": VERSION_TOKENS[key], "known": True,
            "why": "", "template_id": tid, "file": template_rel}


def blueprint_versions(eng: Path, readers: ReaderAdapter | None = None) -> dict:
    """As versões do desenho e o seu estado, lidas pelo motor que já as calcula.

    `latest_authorized` e `approved` são conceitos distintos e o resultado nomeia os dois:
    autorização é um facto de arquitectura registado, aprovação é uma decisão humana."""
    readers = readers or ReaderAdapter()
    out = {"present": False, "latest_authorized": None, "approved": None,
           "approved_by": "", "structural_open": 0, "authorized_any": False,
           "evaluated": False, "reason": ""}
    dec, state = guarded_read(eng, "decisions.md")
    su = guarded_read(eng, "shared-understanding.md")[0]
    try:
        blocks = readers.classify_decisions(dec) if state == "ok" and dec else []
        rows = readers.parse_su(su)[1] if su else None
        bp = readers.blueprint_state(eng, blocks, rows, active_pack(eng))
    except Exception as exc:                                        # noqa: BLE001
        out["reason"] = "{}: {}".format(type(exc).__name__, exc)
        return out
    la = bp.get("latest_authorized") or {}
    appr = bp.get("approved") or {}
    out.update({
        "present": bool(bp.get("present")),
        "evaluated": True,
        "latest_authorized": la.get("version") or None,
        "latest_authorized_state": la.get("state", ""),
        "approved": appr.get("version") or None,
        "approved_by": bp.get("approved_by", ""),
        "structural_open": int(bp.get("structural_open_count") or 0),
        "authorized_any": bool(la.get("version")),
    })
    return out


def expected_version(versions: dict, token: str | None) -> dict:
    """A versão que o token exige, e porque é que ela existe ou não existe (§8.3).

    Ausência tem razões diferentes e elas NÃO se confundem: não há autorização de
    arquitectura nenhuma é uma coisa; há autorização e o negócio ainda não aprovou é
    outra; há aprovação e uma escolha estrutural em aberto é uma terceira."""
    if token is None:
        return {"token": None, "version": None, "state": "no-blueprint-read",
                "reason": "este deliverable não lê nenhuma versão de desenho"}
    if not versions.get("evaluated"):
        return {"token": token, "version": None, "state": "not_evaluated",
                "reason": versions.get("reason")
                or "o estado do desenho não se conseguiu ler"}
    if token == "latest-authorized":
        v = versions.get("latest_authorized")
        if v:
            return {"token": token, "version": v, "state": "available",
                    "reason": versions.get("latest_authorized_state", "")}
        return {"token": token, "version": None, "state": "no-authorization",
                "reason": "não existe autorização de arquitectura para nenhum âmbito"}
    v = versions.get("approved")
    if v:
        return {"token": token, "version": v, "state": "available",
                "reason": "aprovada ({})".format(versions.get("approved_by") or "")}
    if versions.get("structural_open"):
        return {"token": token, "version": None, "state": "structurally-blocked",
                "reason": "{} escolha(s) estrutural(is) em aberto impedem a aprovação"
                          .format(versions["structural_open"])}
    if versions.get("authorized_any"):
        return {"token": token, "version": None, "state": "not-approved",
                "reason": "há versão autorizada e o negócio ainda não aprovou nenhuma"}
    return {"token": token, "version": None, "state": "no-authorization",
            "reason": "não existe autorização de arquitectura para nenhum âmbito"}


def render_precheck(eng: Path, deliverable_id: str, template_rel: str | None = None,
                    readers: ReaderAdapter | None = None) -> dict:
    """A pergunta PRÉ-render da §8.2: as autoridades que ESTE deliverable exige.

    Devolve factos, nunca uma decisão de aplicabilidade: quem decide se o deliverable se
    produz é a declaração do template (`activation` / `blocked_when` /
    `not_applicable_when`), e este resultado é o que essa declaração lê. Ausência
    legítima é *não aplicável*, e não lacuna -- e por isso a ausência de versão sai com
    a razão, não com um código de erro.

    Read-only: não escreve nada, não abre `inputs/` para preencher campo nenhum."""
    readers = readers or ReaderAdapter()
    eng = Path(eng).resolve()
    pack = active_pack(eng)
    rel = template_rel or template_path_for(pack, deliverable_id)
    out = {"artefact": "aisa.coverage.render_precheck",
           "contract_version": CONTRACT_VERSION,
           "engagement": engagement_state(eng)[0].get("engagement", ""),
           "deliverable": deliverable_id, "template": rel,
           "template_sha256": "", "diagnostics": []}
    sha, state = guarded_sha256(eng, rel, pack)
    out["template_state"] = state
    if state != "ok":
        out["diagnostics"].append(_diag(
            COV_DEAD_REF, "error",
            "o template do deliverable não se lê ({}): {}".format(state, rel), file=rel,
            resolves="confirmar o id do deliverable e o pacote activo"))
    else:
        out["template_sha256"] = sha
    auth = template_authority(eng, rel, pack)
    out["declared"] = auth["declared"]
    out["template_id"] = auth.get("template_id")
    # A mesma pergunta que a validação do registo faz, e pela mesma razão: um template que
    # não é o deste deliverable traz a autoridade de versão de outro. Com `--template`
    # explícito isto é o que separa «li o contrato certo» de «li um contrato».
    tid = (auth.get("template_id") or "").strip()
    if auth["state"] == "ok" and tid and tid != deliverable_id:
        out["diagnostics"].append(_diag(
            COV_AUTHORITY_MISMATCH, "error",
            "o pré-render é de `{}` e o template indicado é o de `{}` ({}) — a versão de "
            "autoridade vem do contrato de projecção do próprio deliverable (§8.3)"
            .format(deliverable_id, tid, rel), file=rel,
            resolves="indicar o template de `{}`".format(deliverable_id)))
        auth = dict(auth, known=False, token=None, why="wrong-template")
    elif auth["state"] == "ok" and not tid:
        out["diagnostics"].append(_diag(
            COV_SCHEMA, "error",
            "o template não declara `template_id` (§8.3): não há como confirmar que é o "
            "contrato de projecção de `{}`".format(deliverable_id), file=rel,
            resolves="declarar `template_id` no template"))
        auth = dict(auth, known=False, token=None, why="no-template-id")
    elif auth["state"] == "ok" and not auth["known"]:
        out["diagnostics"].append(_diag(
            COV_SCHEMA, "error",
            "o template não declara `blueprint_version_read` (§8.3)" if
            auth.get("why") == "absent" else
            "`blueprint_version_read: {}` não é um token conhecido (§8.3): {}".format(
                auth["declared"], ", ".join(sorted(k for k in VERSION_TOKENS if k))),
            file=rel, resolves="declarar `v<latest authorized>`, `v<approved>` ou `none`"))
    out["versions"] = blueprint_versions(eng, readers)
    if auth.get("why") in ("wrong-template", "no-template-id"):
        out["expected"] = {"token": None, "version": None, "state": "not_evaluated",
                           "reason": "o contrato de projecção deste deliverable não foi "
                                     "confirmado; nenhuma versão é resolvida a partir do "
                                     "contrato de outro"}
    else:
        out["expected"] = expected_version(out["versions"], auth["token"])
    # As revisões a montante que a etapa `render` exige (§4.6): desenho quando há
    # arquitectura autorizada, reconciliação sempre.
    need = "blueprint" if out["versions"].get("authorized_any") else "reconciliation"
    out["upstream_stage_required"] = need
    # A revisão que se consegue avaliar AGORA: sem versão resolvida não há desenho para
    # rever, e o que resta é a reconciliação. O campo diz qual foi, e `upstream_stage_
    # required` diz qual seria a exigida — confundir as duas escondia a diferença.
    checked = "blueprint" if (need == "blueprint" and out["expected"].get("version"))         else "reconciliation"
    upstream = {"stage": checked, "evaluated": False}
    if checked == "blueprint":
        bp_rel = "_blueprint/ux-blueprint_{}.yaml".format(out["expected"]["version"])
        st = coverage_state(eng, "blueprint", {
            "file": bp_rel, "identity": target_identity(eng, "blueprint", bp_rel)},
            readers)
    else:
        st = coverage_state(eng, "reconciliation", None, readers)
    upstream.update({"evaluated": True, "contract_validity": st["contract_validity"],
                     "freshness": st["freshness"], "source_review": st["source_review"],
                     "semantic_review": st["semantic_review"],
                     "coverage": st["coverage"], "eligible": st["eligible"],
                     "record": (st.get("record") or {}).get("file", "")})
    out["upstream"] = upstream
    if upstream["contract_validity"] == "not_evaluated":
        out["diagnostics"].append(_diag(
            COV_NO_REVIEW, "warn",
            "não há revisão de {} para consumir -- `not_evaluated`, que não é aprovação "
            "nem reprovação (§10)".format(checked),
            resolves="produzir a revisão a montante antes de declarar o deliverable "
                     "completo"))
    elif not upstream["eligible"]:
        out["diagnostics"].append(_diag(
            COV_UNREVIEWED, "error",
            "a revisão de {} que este deliverable consome não está fechada ({})"
            .format(checked, upstream["record"] or "sem registo"),
            file=upstream["record"],
            resolves="fechar a revisão a montante antes de renderizar"))
    out["blocking"] = sum(1 for d in out["diagnostics"] if d["severity"] == "error")
    out["note"] = ("factos para a declaração do template decidir; a aplicabilidade é "
                   "declarada pelo contrato de projecção, e a ausência legítima é *não "
                   "aplicável*, nunca lacuna (§8.2)")
    return out


def _earlier_same_pair(entries: list, record: dict, identity, given: bool = False) -> list:
    """TODAS as revisões publicadas anteriores do mesmo par (etapa, alvo), por versão.

    Todas, e não só a imediatamente anterior — e a razão é o defeito que aqui se fechou:
    comparando só com a anterior, repetir uma revisão incompleta **lavava** as lacunas.
    v01 tratava seis obrigações; v02 tratava uma e saía com lacunas; v03 repetia a v02 e
    saía completa, porque «a anterior» já só tinha uma. Uma obrigação que apareceu em
    qualquer versão do par fica exigida em todas as seguintes, até receber disposição.

    Para um registo publicado: versões estritamente menores. Para um rascunho em
    pré-visualização (`given`): todas as publicadas, porque um rascunho é posterior a tudo."""
    mine = _version_num(str(record.get("version", "")))
    stage = record.get("stage")
    out = []
    for e in entries:
        rec = e["record"]
        if not isinstance(rec, dict) or rec.get("stage") != stage:
            continue
        if identity is not None and (_as_dict(rec.get("target")).get("identity") or "") \
                != identity:
            continue
        v = _version_num(e["version"])
        if not given and (mine <= 0 or v >= mine):
            continue
        if given and e["record"] is record:
            continue
        out.append(e)
    return sorted(out, key=lambda e: _version_num(e["version"]))


def _dropped_identities(earlier: list, handled: dict) -> list:
    """As identidades de obrigação que ALGUMA revisão anterior do par tratou e esta não
    trata — um a um nem por fusão (§4.4.4). Devolve `(identidade, versão onde apareceu)`,
    com a versão mais recente que a tratava, para o diagnóstico dizer de onde vem."""
    seen: dict[tuple, str] = {}
    for e in earlier:
        for item in _as_list(_as_dict(e.get("record")).get("coverage")):
            if isinstance(item, dict):
                ident = obligation_identity(item)
                if ident:
                    seen[ident] = e["file"]       # a última versão que a tratou ganha
    lost = []
    for ident, origin in seen.items():
        if ident in handled:
            continue
        if any(set(ident) <= h["refs"] for h in handled.values()):
            continue
        lost.append((ident, origin))
    return sorted(lost)


UPSTREAM_STAGE = {"blueprint": ("reconciliation",),
                  "render": ("blueprint", "reconciliation")}


def upstream_health(eng: Path, record: dict, chain: dict, readers: ReaderAdapter,
                    inventory: dict, _depth: int = 0) -> list[dict]:
    """A revisão de jusante não pode valer mais do que aquela em que diz assentar.

    §8.1: produzir uma versão exige a reconciliação **completa e actual**. Sem isto, uma
    reconciliação pobre — meia dúzia de unidades revistas, zero obrigações — deixava
    declarar um desenho sem cobertura nenhuma como completo: a herança de obrigações
    passava por vacuidade, porque não havia obrigações nenhumas a herdar.

    Avalia-se cada registo citado em `based_on` **pelo seu próprio nome**, com o mesmo
    motor. A recursão é limitada: render → blueprint → reconciliation, e mais nada."""
    out: list[dict] = []
    if _depth > 2:
        return out
    stage = record.get("stage")
    if stage not in UPSTREAM_STAGE:
        return out
    for name in _as_list(record.get("based_on")):
        up = _as_dict(chain.get(name)) if isinstance(name, str) else {}
        if not up or up.get("stage") not in UPSTREAM_STAGE[stage]:
            continue
        entry = {"file": str(name), "stage": up.get("stage", ""), "error": ""}
        try:
            res = coverage_state(eng, up["stage"], _as_dict(up.get("target")) or None,
                                 readers, inventory, record=up,
                                 record_name="_coverage/" + str(name),
                                 record_filename=str(name), _depth=_depth + 1)
        except CoverageError as exc:
            # A revisão de montante NÃO se consegue avaliar. Engolir isto era o falso
            # verde mais silencioso de todos: a de jusante ficava sem nada a apontar-lhe,
            # e uma lista de montante vazia lê-se como «não havia nada a verificar».
            # Contrato §8: falha de avaliação é «não avaliado», nunca sucesso silencioso.
            entry.update({"error": str(exc), "code": COV_SCHEMA,
                          "contract_validity": "invalid", "freshness": "not_evaluated",
                          "source_review": "not_evaluated",
                          "coverage": "not_evaluated"})
            out.append(entry)
            continue
        except Exception as exc:                                    # noqa: BLE001
            entry.update({"error": "{}: {}".format(type(exc).__name__, exc),
                          "code": COV_UNEXPECTED,
                          "contract_validity": "invalid", "freshness": "not_evaluated",
                          "source_review": "not_evaluated",
                          "coverage": "not_evaluated"})
            out.append(entry)
            continue
        entry.update({"contract_validity": res["contract_validity"],
                      "freshness": res["freshness"],
                      "source_review": res["source_review"],
                      "coverage": res["coverage"]})
        out.append(entry)
    return out


ACTION_BY_STAGE = {"reconciliation": "produce_blueprint",
                   "blueprint": "approve_blueprint",
                   "render": "complete_deliverable"}


def coverage_state(eng: Path, stage: str, target: dict | None = None,
                   readers: ReaderAdapter | None = None,
                   inventory: dict | None = None, record: dict | None = None,
                   record_name: str = "", record_filename: str | None = None,
                   _depth: int = 0) -> dict:
    """O resultado computado do contrato §7, para uma etapa e um alvo.

    Sem revisão aplicável o resultado é `not_evaluated` em toda a linha — nunca
    «completo» e nunca «reprovado retroactivamente» (contrato §10).

    Com `record`, avalia **esse** registo em vez de seleccionar o publicado: é como se
    pré-visualiza um rascunho antes de o finalizar. Mostrar as obrigações de um rascunho
    debaixo dos veredictos de outro registo seria a pior mistura possível."""
    readers = readers or ReaderAdapter()
    eng = Path(eng).resolve()
    if stage not in STAGES:
        raise CoverageError("etapa desconhecida: {!r} (contrato §2)".format(stage), 2)
    if target is not None and not isinstance(target, dict):
        raise CoverageError(
            "`target` tem de ser um mapa `{{file, ...}}` ou `None`, e é {} — um argumento "
            "com o tipo errado é erro de uso, nunca falha interna"
            .format(type(target).__name__), 2)
    inventory = inventory or build_inventory(eng, readers)
    identity = None
    requested_file = None
    if stage != "reconciliation":
        if not target or not target.get("file"):
            raise CoverageError(
                "a etapa {!r} exige `--target <ficheiro>` (contrato §4.6): sem alvo não "
                "há revisão aplicável a seleccionar".format(stage), 2)
        identity = target.get("identity") or target_identity(eng, stage, target["file"])
        requested_file = str(target["file"])
    result = {
        "artefact": "aisa.coverage.state",
        "contract_version": CONTRACT_VERSION,
        "engagement": engagement_state(eng)[0].get("engagement", ""),
        "stage": stage,
        "target": dict(target or {}, identity=identity) if target else None,
        "record": None,
        "superseded": [],
        "contract_validity": "invalid",
        "freshness": "not_evaluated",
        "source_review": "not_evaluated",
        "semantic_review": "not_evaluated",
        "coverage": "not_evaluated",
        "action": ACTION_BY_STAGE[stage],
        "eligible": False,
        "reasons": [],
        "diagnostics": [],
        "limitations": inventory.get("limitations", []),
        "inventory": {"total": inventory.get("total", 0),
                      "complete": inventory.get("complete", True),
                      "counts_by_class": inventory.get("counts_by_class", {})},
        "structural": None,
        "note": "cobertura revista não é correcção garantida por código, não é aprovação "
                "do negócio e não é prova de que a solução funciona ponta-a-ponta — "
                "estrutura, cobertura, aprovação e ponta-a-ponta são quatro perguntas "
                "separadas (contrato §1, §7).",
    }
    diags: list[dict] = list(inventory.get("diagnostics_as_coverage", []))
    for d in inventory.get("diagnostics", []):
        if d.get("blocking"):
            diags.append(_diag(COV_UNEXPECTED if d.get("level") == "error" else COV_SCHEMA,
                               "error", d.get("message", ""), file=d.get("where", ""),
                               resolves="tornar a fonte legível antes de rever"))
    if record is not None:
        entry = {"file": record_name or "(registo indicado)",
                 "name": record_filename or "",
                 "version": record.get("version", ""), "record": record, "state": "ok"}
        # Um rascunho não tem nome de versão nenhum; um registo já publicado tem, e
        # verifica-se contra ele (§4.1).
        result["given_record"] = record_filename is None
    else:
        selection = select_record(eng, stage, identity,
                                  target_file=(requested_file
                                               if stage != "reconciliation" else None))
        for broken in selection["unreadable"]:
            diags.append(_diag(COV_SCHEMA, "error",
                               "registo de cobertura que não se consegue situar: {} — {}"
                               .format(broken["file"],
                                       broken.get("why") or broken["state"]),
                               file=broken["file"],
                               resolves="corrigir o ficheiro ou publicar nova revisão"))
        entry = selection["selected"]
        result["superseded"] = [e["file"] for e in selection["superseded"]]
        result["unreadable_records"] = [e["file"] for e in selection["unreadable"]]
    if entry is None:
        result["contract_validity"] = "invalid" if selection["unreadable"] else \
            "not_evaluated"          # §7: sem registo não há contrato para julgar
        diags.append(_diag(COV_NO_REVIEW, "error",
                           "não há revisão de cobertura para a etapa {!r}{} — resultado "
                           "`not_evaluated`, que não é aprovação nem reprovação"
                           .format(stage, " do alvo " + identity if identity else ""),
                           resolves="produzir a revisão e finalizá-la"))
        result["diagnostics"] = diags
        result["reasons"] = ["Ainda não há nenhuma revisão registada para este passo."]
        return result
    record = entry["record"]
    result["record"] = {"file": entry["file"], "version": entry["version"],
                        "generated_at": record.get("generated_at", "")}
    if result.get("unreadable_records"):
        # §6.6: registo ilegível → `invalid`. E invalida TUDO, não só ele: enquanto
        # houver um registo que ninguém consegue ler em `_coverage/`, não se pode dizer
        # que a revisão escolhida é a que vale -- o ficheiro partido pode ser a mais
        # recente deste par. Um falso verde por ficheiro corrompido é o pior dos dois
        # mundos: o registo que impediria o verde é exactamente o que não se lê.
        result["contract_validity"] = "invalid"
        result["coverage"] = "not_evaluated"
        result["gaps"] = []
        result["diagnostics"] = diags
        result["eligible"] = False
        result["reasons"] = [
            "Há {} registo(s) de revisão que não se conseguem situar ({}). Enquanto isso "
            "durar, nenhuma revisão pode ser dada como a que vale — o ficheiro que não se "
            "consegue situar pode ser o mais recente."
            .format(len(result["unreadable_records"]),
                    ", ".join(result["unreadable_records"]))]
        return result
    entries = load_records(eng)
    chain = {e["name"]: e["record"] for e in entries if e["record"] is not None}
    ctx = record_context(eng, inventory, readers)
    # O nome do ficheiro só se verifica contra `version` quando o registo ESTÁ publicado:
    # um rascunho vive num temporário e não tem nome de versão nenhum.
    ctx = dict(ctx, chain=chain)
    val = validate_record(record, inventory, eng, readers, chain,
                          entry["name"] if record is not None and not
                          result.get("given_record") else None, ctx)
    diags += val["diagnostics"]
    result["contract_validity"] = val["contract_validity"]

    # ---- atualidade: a base que a revisão declarou contra a base de agora
    if val["contract_validity"] == "unsupported":
        result["freshness"] = "not_evaluated"
    else:
        synth = tuple(sorted(
            str(s) for s in _as_list(_as_dict(record.get("deliverable"))
                                     .get("authority_sources"))
            if str(s).startswith(SYNTHESIS_DIR)))
        basis = compute_basis(eng, inventory, stage, _as_dict(record.get("target")) or None,
                              authorities=_as_list(_as_dict(record.get("basis"))
                                                   .get("authorities")),
                              readers=readers, synthesis_authorities=synth,
                              graph_consumed=declared_graph_consumed(record))
        fresh = check_freshness(record, basis, current_target(eng, record.get("target")))
        result["freshness"] = fresh["status"]
        result["freshness_detail"] = fresh
        if fresh["status"] == "stale":
            for c in fresh["changed"]:
                diags.append(_diag(COV_STALE, "error", c["message"],
                                   file=str(c.get("what", "")),
                                   resolves="rever os impactos e produzir nova revisão"))
        if fresh.get("contract_version_mismatch"):
            result["contract_validity"] = "unsupported"
            diags.append(_diag(COV_SCHEMA, "error",
                               fresh["contract_version_mismatch"]["message"]))

    # ---- revisão das fontes / das obrigações
    if val["contract_validity"] == "unsupported":
        # Nada deste registo foi interpretado, por isso nada dele é reportado como
        # incompleto: `unsupported` é «não sei ler isto», não «li e falta-lhe coisa».
        result["semantic_review"] = "not_evaluated"
        result["coverage"] = "not_evaluated"
        result["gaps"] = []
        result["diagnostics"] = diags
        result["eligible"], result["reasons"] = _eligibility(result, val, record)
        return result
    if stage == "reconciliation":
        n = _unreviewed_units(inventory, val["source_units"], diags)
        result["source_review"] = "complete" if (n == 0 and val["source_review_ok"]
                                                 and inventory.get("complete", True)) \
            else "incomplete"
        result["unreviewed_units"] = n
    else:
        unreviewed = [d for d in val["diagnostics"] if d["code"] == COV_UNREVIEWED]
        result["source_review"] = "complete" if (not unreviewed and val["source_review_ok"]
                                                 and val["inheritance_ok"]) else "incomplete"
        result["unreviewed_obligations"] = len(unreviewed)
    result["semantic_review"] = val["semantic_review"]

    # ---- obrigações não desaparecem entre revisões sucessivas do mesmo par (§4.4.4)
    # A regra que fecha o esvaziamento PARCIAL: a v02 de uma reconciliação que trata uma
    # obrigação onde a v01 tratava seis não «mudou de opinião» em silêncio — cada uma das
    # cinco tem de reaparecer, nem que seja com `disposition: retire` e autoridade. É a
    # mesma regra que já valia entre etapas, aplicada entre versões.
    earlier = _earlier_same_pair(entries, record, identity,
                                 given=bool(result.get("given_record")))
    if earlier:
        result["previous"] = [e["file"] for e in earlier]
        lost = _dropped_identities(earlier, val["handled"])
        for ident, origin in lost:
            label = ", ".join(ident)
            diags.append(_diag(COV_UNREVIEWED, "error",
                               "obrigação que uma revisão anterior deste passo ({}) tratava "
                               "e esta deixou cair: {} — uma obrigação não desaparece, "
                               "recebe uma disposição; repetir a revisão que a largou não "
                               "a apaga (§4.4.4)".format(origin, label),
                               locator=label, file=origin,
                               resolves="tratar a obrigação, nem que seja com "
                                        "`disposition: retire` e a autoridade que o permite"))
        if lost and result["source_review"] == "complete":
            result["source_review"] = "incomplete"

    # ---- cobertura
    blocking = {COV_UNREVIEWED, COV_DEAD_REF, COV_MISSING_TARGET, COV_INVALID_TARGET,
                COV_EXCLUSION_NO_DECISION, COV_REVIEW_INCOMPLETE, COV_CAPTURE_LIMIT,
                COV_AUTHORITY_MISMATCH}
    has_block = any(d["code"] in blocking and d["severity"] == "error" for d in diags)
    if result["contract_validity"] in ("invalid", "unsupported"):
        result["coverage"] = "not_evaluated"
    elif val["gaps"] or has_block:
        result["coverage"] = "gaps"
    else:
        result["coverage"] = "complete"
    result["gaps"] = val["gaps"]

    # ---- estrutura do alvo (§8.1.4): uma versão que falha a estrutura não é aprovável
    if stage == "blueprint" and (record.get("target") or {}).get("file"):
        result["structural"] = structural_check(eng, record["target"]["file"], readers)

    # ---- a revisão a montante (§8.1): jusante não vale mais do que montante
    result["upstream"] = upstream_health(eng, record, chain, readers, inventory, _depth)
    for up in result["upstream"]:
        if up.get("error"):
            diags.append(_diag(up.get("code", COV_UNEXPECTED), "error",
                               "a revisão de {} em que esta assenta ({}) não se consegue "
                               "avaliar: {}".format(up["stage"] or "montante",
                                                    up["file"], up["error"]),
                               file=up["file"],
                               resolves="corrigir a revisão a montante e reavaliar"))
        broken = [label for label, got, want in (
            ("o registo não é válido", up["contract_validity"], "valid"),
            ("a base mudou desde então", up["freshness"], "current"),
            ("ficou material por rever", up["source_review"], "complete"))
            if got != want]
        if not broken:
            continue
        if not up.get("error"):
            diags.append(_diag(COV_UNREVIEWED, "error",
                               "a revisão de {} em que esta assenta ({}) não está "
                               "fechada: {}".format(up["stage"], up["file"],
                                                    "; ".join(broken)),
                               file=up["file"],
                               resolves="fechar a revisão a montante antes de consumir "
                                        "esta"))
        if result["coverage"] == "complete":
            result["coverage"] = "gaps"
        if result["source_review"] == "complete":
            result["source_review"] = "incomplete"

    result["diagnostics"] = diags
    result["eligible"], result["reasons"] = _eligibility(result, val, record)
    return result


def _eligibility(result: dict, val: dict, record: dict) -> tuple[bool, list[str]]:
    """§8.1 — a severidade do achado é separada da elegibilidade por acção.

    Produzir para discussão não é aprovar, e é por isso que as três acções têm regras
    diferentes sobre exactamente os mesmos achados."""
    reasons: list[str] = []
    stage = result["stage"]
    if result["contract_validity"] != "valid":
        reasons.append("O registo da revisão não se lê como válido ({})."
                       .format(result["contract_validity"]))
        return False, reasons
    if result["freshness"] != "current":
        reasons.append("A base mudou desde a revisão: é preciso rever os impactos antes "
                       "de usar (atualidade `stale`).")
        return False, reasons
    if result["source_review"] != "complete":
        reasons.append("Há material por rever neste passo.")
        return False, reasons
    # Um achado impeditivo é impeditivo em TODAS as etapas. A reconciliação só olhava para
    # as lacunas encaminhadas, e um registo com referências mortas ou um `covered` sem
    # âncora saía elegível para produzir um desenho.
    blocking = [d for d in result.get("diagnostics", [])
                if d.get("severity") == "error" and d.get("code") != COV_KNOWN_GAP]
    if blocking:
        reasons.append("Há {} achado(s) impeditivo(s) por resolver ({})."
                       .format(len(blocking),
                               ", ".join(sorted({d["code"] for d in blocking}))))
        return False, reasons
    if stage == "reconciliation":
        # "toda a unidade tem tratamento e toda a perda identificada foi encaminhada"
        loose = [g for g in val["gaps"]
                 if not g["required_action"] or not g["responsible_role"]]
        if loose:
            reasons.append("Há perdas identificadas sem dono nem próxima acção ({})."
                           .format(", ".join(g["item"] for g in loose)))
            return False, reasons
        if val["gaps"]:
            reasons.append("Pode avançar-se para o desenho com as lacunas à vista e "
                           "encaminhadas ({}).".format(len(val["gaps"])))
        else:
            reasons.append("Todas as unidades revistas e todas as obrigações tratadas.")
        return True, reasons
    if stage == "blueprint":
        if result["semantic_review"] != "completed":
            reasons.append("A leitura nos dois sentidos ainda não está concluída.")
            return False, reasons
        if result["coverage"] != "complete":
            reasons.append("Há obrigações por cobrir ou por fundamentar; a versão pode "
                           "continuar em discussão, mas não se anuncia pronta para "
                           "aprovação.")
            return False, reasons
        st = result.get("structural") or {}
        if st.get("evaluated") and st.get("blocking"):
            reasons.append("O desenho tem {} bloqueio(s) de estrutura por resolver."
                           .format(st["blocking"]))
            return False, reasons
        if not st.get("evaluated"):
            reasons.append("A verificação de estrutura do desenho não pôde correr; sem "
                           "ela não se declara prontidão.")
            return False, reasons
        reasons.append("Revisão actual, leitura nos dois sentidos feita e sem lacunas "
                       "materiais: falta o pedido de aprovação ao negócio, que nenhum "
                       "motor substitui.")
        return True, reasons
    if result["semantic_review"] != "completed":
        reasons.append("A leitura nos dois sentidos ainda não está concluída.")
        return False, reasons
    if result["coverage"] != "complete":
        reasons.append("O documento perde conteúdo que o contrato manda projectar.")
        return False, reasons
    reasons.append("A projecção preserva o que o contrato deste documento selecciona.")
    return True, reasons


# ================================================== relatório determinístico §3

_VERDICT_PT = {
    "valid": "válido", "invalid": "inválido", "unsupported": "schema não suportado",
    "current": "actual", "stale": "a base mudou", "not_evaluated": "por avaliar",
    "complete": "completa", "incomplete": "incompleta", "gaps": "com lacunas",
    "completed": "concluída", "pending": "pendente",
}


def _pt(value) -> str:
    return _VERDICT_PT.get(str(value), str(value))


def render_report(record: dict | None, result: dict) -> str:
    """A projecção Markdown do registo e dos veredictos (contrato §3).

    **Não é autoridade** e não se edita à mão: o JSON é o registo, os veredictos são
    recalculados em cada leitura, e alterar este ficheiro não muda nada (T40). Nada aqui
    depende da hora a que corre — o mesmo estado dá o mesmo texto."""
    record = record or {}
    stage = result.get("stage", record.get("stage", ""))
    out = ["# Revisão de cobertura — {} · etapa {}".format(
        result.get("engagement", ""), stage), ""]
    out.append("> Projecção determinística do registo em JSON. **Não é autoridade**: os "
               "veredictos são recalculados a cada leitura e editar este ficheiro não "
               "muda nenhum deles.")
    out.append("")
    rec_meta = result.get("record") or {}
    out.append("| | |")
    out.append("|---|---|")
    out.append("| registo | `{}` |".format(rec_meta.get("file", "—")))
    out.append("| produzido em | {} |".format(rec_meta.get("generated_at", "—")))
    tgt = record.get("target") or {}
    out.append("| alvo | {} |".format("`{}` ({})".format(tgt.get("file"),
                                                        tgt.get("identity"))
                                      if tgt else "— (reconciliação)"))
    out.append("| revisões anteriores | {} |".format(
        ", ".join("`%s`" % b for b in (record.get("based_on") or [])) or "—"))
    out.append("")
    out.append("## Veredictos")
    out.append("")
    out.append("| dimensão | resultado |")
    out.append("|---|---|")
    for label, key in (("contrato do registo", "contract_validity"),
                       ("actualidade da base", "freshness"),
                       ("revisão das fontes", "source_review"),
                       ("leitura nos dois sentidos", "semantic_review"),
                       ("cobertura", "coverage")):
        out.append("| {} | {} ({}) |".format(label, _pt(result.get(key)),
                                             result.get(key)))
    out.append("| passo a que isto serve | {} |".format(result.get("action", "")))
    out.append("| pode avançar | {} |".format("sim" if result.get("eligible") else "não"))
    out.append("")
    if result.get("reasons"):
        out.append("## Porquê")
        out.append("")
        for r in result["reasons"]:
            out.append("- {}".format(r))
        out.append("")
    if result.get("superseded"):
        out.append("## Revisões anteriores do mesmo passo")
        out.append("")
        out.append("Vale sempre a mais recente; as anteriores ficam para consulta e "
                   "nunca são escolhidas para esconder o que a mais recente diz.")
        out.append("")
        for f in result["superseded"]:
            out.append("- `{}`".format(f))
        out.append("")
    obligations = record.get("coverage") or []
    if obligations:
        out.append("## Obrigações")
        out.append("")
        out.append("| item | requisito | tratamento | estado | destinos |")
        out.append("|---|---|---|---|---|")
        for item in obligations:
            if not isinstance(item, dict):
                continue
            targets = item.get("targets") or []
            out.append("| {} | {} | {} | {} | {} |".format(
                item.get("id", ""),
                ", ".join(str(r) for r in item.get("requirement_refs") or []),
                item.get("disposition", ""),
                (item.get("assessment") or {}).get("status", ""),
                len(targets)))
        out.append("")
    if result.get("gaps"):
        out.append("## Lacunas conhecidas")
        out.append("")
        out.append("| item | requisito | estado | o que falta | a quem toca |")
        out.append("|---|---|---|---|---|")
        for g in result["gaps"]:
            out.append("| {} | {} | {} | {} | {} |".format(
                g["item"], ", ".join(g["requirement_refs"]), g["status"],
                g["required_action"] or "—", g["responsible_role"] or "—"))
        out.append("")
    if result.get("limitations"):
        out.append("## Fontes que não se conseguem ler")
        out.append("")
        for lim in result["limitations"]:
            out.append("- `{}` — {} ({})".format(lim.get("unit_key", ""),
                                                 lim.get("reason", ""),
                                                 lim.get("code", "")))
        out.append("")
    diags = result.get("diagnostics") or []
    if diags:
        out.append("## Achados")
        out.append("")
        out.append("| código | gravidade | onde | o que é | o que o fecha |")
        out.append("|---|---|---|---|---|")
        for d in diags:
            where = d.get("item") or d.get("locator") or d.get("file") or "—"
            out.append("| `{}` | {} | {} | {} | {} |".format(
                d.get("code", ""), d.get("severity", ""), where,
                str(d.get("message", "")).replace("|", "\\|"),
                str(d.get("resolves", "")).replace("|", "\\|") or "—"))
        out.append("")
    sem = record.get("semantic_review") or {}
    if sem:
        out.append("## Quem reviu")
        out.append("")
        who = sem.get("performed_by") or {}
        out.append("- {} ({}), {}".format(who.get("name", "—"), who.get("kind", "—"),
                                          sem.get("method", "—")))
        for lim in _as_list(sem.get("limitations")):
            out.append("- limite declarado: {}".format(lim))
        out.append("")
    out.append("---")
    out.append("")
    out.append("Estrutura, cobertura, aprovação e ponta-a-ponta são quatro perguntas "
               "separadas, de propósito. Esta página responde à segunda.")
    return "\n".join(out) + "\n"


# ============================================================ finalização §6.6

def read_draft(path: Path) -> tuple[object, str]:
    """A ÚNICA porta para um ficheiro que o operador nomeia na linha de comandos.

    Excepção nomeada à porta do engagement, e a razão está aqui: um rascunho é um
    argumento explícito de uma operação explícita, não uma fonte que o motor descobriu
    sozinho. Não lhe aplicamos `safe_path` porque ele vive, por desenho, num temporário
    fora do engagement — e continua a não poder ser lido às cegas: o que se lê é um
    ficheiro regular, e o que não for JSON é `unreadable`, nunca vazio."""
    p = Path(path)
    if not p.is_file():
        return None, "absent"
    text, state = read_source(p)
    if state != "ok":
        return None, state
    try:
        data = json.loads(text)
    except ValueError:
        return None, "unreadable"
    return (data if isinstance(data, dict) else None,
            "ok" if isinstance(data, dict) else "unreadable")


def next_version(eng: Path) -> str:
    taken = {_version_num("v" + _RECORD_RE.match(r.rsplit("/", 1)[-1]).group(1))
             for r in record_files(eng)}
    n = 1
    while n in taken:
        n += 1
    return "v{:02d}".format(n)


def _coverage_dir(eng: Path) -> Path:
    d = eng.resolve() / "_coverage"
    if not _within(d.resolve() if d.exists() else d, eng.resolve()):
        raise CoverageError("`_coverage/` fora do engagement — recusado", 3)
    return d


def finalize(eng: Path, draft_path: Path, readers: ReaderAdapter | None = None,
             max_attempts: int = 99) -> dict:
    """Publica um rascunho como `coverage_vNN.json` + projecção `.md` (contrato §6.6).

    A ÚNICA operação de escrita deste módulo, e escreve **apenas** dentro de
    `_coverage/`: nunca a Shared Understanding, nunca `decisions.md`, nunca um blueprint.

    Três recusas, e cada uma existe por uma razão concreta:

    1. **schema inválido** — publicar um registo ilegível seria publicar um falso verde;
    2. **base alterada** — o rascunho declara a base que diz ter lido; se essa base já
       não é a actual, publicar carimbaria como revista uma fonte que mudou sem ser
       relida. Os digests antigos **nunca** são substituídos pelos actuais;
    3. **base alterada DURANTE a operação** — a reserva é desfeita e nada fica publicado.

    A reserva da versão é **exclusiva** (`O_CREAT|O_EXCL`): duas finalizações concorrentes
    ficam com versões diferentes e nenhuma sobrescreve a outra. Não há `os.replace` sobre
    uma versão publicada em lado nenhum deste ficheiro."""
    readers = readers or ReaderAdapter()
    eng = Path(eng).resolve()
    draft, state = read_draft(Path(draft_path))
    if state != "ok":
        raise CoverageError(
            "rascunho {}: {}".format({"absent": "não encontrado",
                                      "empty": "vazio",
                                      "unreadable": "ilegível ou não é um objecto JSON"}
                                     .get(state, state), draft_path),
            3 if state == "absent" else 2)
    stage = draft.get("stage")
    if stage not in STAGES:
        raise CoverageError("rascunho com etapa desconhecida: {!r}".format(stage), 2)
    inventory = build_inventory(eng, readers)
    chain = {e["name"]: e["record"] for e in load_records(eng) if e["record"] is not None}
    ctx = dict(record_context(eng, inventory, readers), chain=chain)
    val = validate_record(draft, inventory, eng, readers, chain, None, ctx)
    if val["contract_validity"] != "valid":
        return {"published": False, "reason": "schema",
                "contract_validity": val["contract_validity"],
                "diagnostics": val["diagnostics"],
                "message": "o rascunho não é um registo válido ({}) — não se publica um "
                           "registo que ninguém consegue ler"
                           .format(val["contract_validity"])}
    synth = tuple(sorted(
        str(s) for s in _as_list(_as_dict(draft.get("deliverable"))
                                 .get("authority_sources"))
        if str(s).startswith(SYNTHESIS_DIR)))
    before = compute_basis(eng, inventory, stage, draft.get("target"),
                           authorities=_as_list(_as_dict(draft.get("basis"))
                                                .get("authorities")),
                           readers=readers, synthesis_authorities=synth,
                           graph_consumed=declared_graph_consumed(draft))
    fresh = finalize_recheck(draft, before, current_target(eng, draft.get("target")))
    del before                          # a comparação de saída recalcula tudo de novo
    if fresh["status"] != "current":
        return {"published": False, "reason": "stale", "freshness": fresh,
                "diagnostics": val["diagnostics"],
                "message": "a base mudou depois de a revisão ser escrita: {} — publicar "
                           "agora carimbaria como revista uma fonte que mudou sem ser "
                           "relida".format("; ".join(fresh["reasons"]) or "ver `changed`")}
    cdir = _coverage_dir(eng)
    cdir.mkdir(parents=True, exist_ok=True)
    fd = None
    for _ in range(max_attempts):
        version = next_version(eng)
        target = cdir / "coverage_{}.json".format(version)
        try:
            fd = os.open(str(target), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except FileExistsError:
            fd = None                    # concorrência ocupou a versão: repete a reserva
    if fd is None:
        raise CoverageError(
            "não foi possível reservar uma versão em {} após {} tentativas"
            .format(cdir, max_attempts), 5)
    published = dict(draft)
    published["version"] = version       # a identidade é o ficheiro (§4.1); só isto muda
    payload = json.dumps(published, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    md_path = cdir / "coverage_{}.md".format(version)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(payload)
        # A verificação final é EXACTAMENTE a mesma da inicial -- `finalize_recheck`,
        # sobre a base recalculada E sobre o alvo recalculado. A versão anterior
        # comparava à mão só os três digests e o manifesto, e o alvo não está no
        # manifesto (é um alvo, §6.3): mexer no desenho entre a reserva e esta linha
        # passava, e a revisão era publicada já `stale`. Duas definições de «a base
        # mudou» divergem sempre; esta é a única.
        after = compute_basis(eng, build_inventory(eng, readers), stage,
                              draft.get("target"),
                              authorities=_as_list(_as_dict(draft.get("basis"))
                                                .get("authorities")),
                              readers=readers, synthesis_authorities=synth,
                              graph_consumed=declared_graph_consumed(draft))
        moved = finalize_recheck(published, after, current_target(eng,
                                                                 draft.get("target")))
        if moved["status"] != "current":
            target.unlink(missing_ok=True)
            return {"published": False, "reason": "changed-during",
                    "freshness": moved, "changed": moved["reasons"],
                    "message": "a base mudou enquanto a revisão era publicada ({}) — a "
                               "reserva foi desfeita e nada ficou publicado"
                               .format("; ".join(moved["reasons"]) or "ver `changed`")}
        # Avalia-se o registo que ACABOU de ser publicado, por nome, e não «o mais
        # recente da etapa»: com duas finalizações concorrentes, o mais recente é o da
        # outra, e o relatório de uma versão falava da outra.
        result = coverage_state(eng, stage, draft.get("target"), readers,
                                record=published,
                                record_name="_coverage/coverage_{}.json".format(version),
                                record_filename="coverage_{}.json".format(version))
        # O ÚLTIMO veredicto é o que manda, e é o mesmo que vai ser reportado. Há sempre
        # uma janela entre uma verificação e a linha seguinte; o que não pode haver é
        # publicar depois de a ter visto fechada. Se o estado que se ia reportar não está
        # actual, ou não é válido, a reserva desfaz-se aqui -- não se anuncia uma revisão
        # que a própria operação já sabe desactualizada.
        if result["freshness"] != "current" or result["contract_validity"] != "valid":
            target.unlink(missing_ok=True)
            return {"published": False, "reason": "changed-during", "result": result,
                    "changed": result.get("reasons", []),
                    "message": "no fim da operação a revisão já não estava actual "
                               "(atualidade: {} · contrato: {}) — a reserva foi desfeita "
                               "e nada ficou publicado"
                               .format(result["freshness"],
                                       result["contract_validity"])}
        md_path.write_text(render_report(published, result), encoding="utf-8",
                           newline="\n")
    except Exception:                                               # noqa: BLE001
        target.unlink(missing_ok=True)
        md_path.unlink(missing_ok=True)
        raise
    return {"published": True, "version": version,
            "json": "_coverage/coverage_{}.json".format(version),
            "md": "_coverage/coverage_{}.md".format(version),
            "result": result,
            "message": "revisão publicada como {} — o veredicto continua a ser "
                       "recalculado em cada leitura".format(version)}


def finalize_recheck(draft: dict, current: dict, target_now: dict | None) -> dict:
    """O recheck da finalização: compara o snapshot do rascunho com a base actual.

    É `check_freshness` — de propósito. Ter uma segunda comparação aqui seria ter duas
    definições de «a base mudou», e mais cedo ou mais tarde elas divergiriam."""
    return check_freshness(draft, current, target_now)


# ============================================================================ CLI

def _inventory_text(inv: dict) -> str:
    lines = ["engagement: {}".format(inv["engagement"]),
             "unidades: {}".format(inv["total"]), ""]
    width = max((len(c) for c in inv["counts_by_class"]), default=0)
    for cls, n in sorted(inv["counts_by_class"].items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append("  {:<{w}}  {}".format(cls, n, w=width))
    if inv["excluded"]:
        lines.append("")
        lines.append("fora do inventário ({}) — registo de aprovação, contrato §6.1:"
                     .format(len(inv["excluded"])))
        for e in inv["excluded"]:
            lines.append("  {}".format(e["unit_key"]))
    if inv["limitations"]:
        lines.append("")
        lines.append("limitações ({}):".format(len(inv["limitations"])))
        for lim in inv["limitations"]:
            lines.append("  {} — {} ({})".format(lim["unit_key"], lim["reason"],
                                                 lim["code"]))
    if inv["diagnostics"]:
        lines.append("")
        lines.append("diagnósticos ({}, {} impeditivos):".format(
            len(inv["diagnostics"]), inv["blocking_diagnostics"]))
        for d in inv["diagnostics"]:
            lines.append("  [{}{}] {} — {}".format(
                d.get("level", "warn"), " IMPEDITIVO" if d.get("blocking") else "",
                d.get("where", ""), d.get("message", "")))
    if not inv["complete"]:
        lines.append("")
        lines.append("DENOMINADOR INCOMPLETO: há fontes que existem e não foram lidas.")
        lines.append("Uma revisão sobre esta base não pode ser completa.")
    lines.append("")
    lines.append("Isto é o denominador, não uma avaliação: nada aqui diz que a cobertura")
    lines.append("está completa, e nenhuma revisão foi lida.")
    return "\n".join(lines)


def _state_text(result: dict) -> str:
    lines = ["engagement: {} · etapa: {}".format(result.get("engagement", ""),
                                                 result.get("stage", ""))]
    tgt = result.get("target") or {}
    if tgt:
        lines.append("alvo: {} ({})".format(tgt.get("file", ""), tgt.get("identity", "")))
    rec = result.get("record")
    lines.append("revisão: {}".format(rec["file"] if rec else "nenhuma"))
    if result.get("superseded"):
        lines.append("anteriores do mesmo passo: {}".format(
            ", ".join(result["superseded"])))
    lines.append("")
    for label, key in (("contrato do registo", "contract_validity"),
                       ("actualidade da base", "freshness"),
                       ("revisão das fontes", "source_review"),
                       ("leitura nos dois sentidos", "semantic_review"),
                       ("cobertura", "coverage")):
        lines.append("  {:<26} {} ({})".format(label, _pt(result.get(key)),
                                               result.get(key)))
    st = result.get("structural")
    if st and st.get("evaluated"):
        lines.append("  {:<26} {} bloqueio(s), {} aviso(s)".format(
            "estrutura do desenho", st["blocking"], st["warn"]))
    lines.append("")
    lines.append("  passo: {} · pode avançar: {}".format(
        result.get("action", ""), "sim" if result.get("eligible") else "não"))
    for r in result.get("reasons", []):
        lines.append("    - {}".format(r))
    errs = [d for d in result.get("diagnostics", []) if d.get("severity") == "error"]
    warns = [d for d in result.get("diagnostics", []) if d.get("severity") != "error"]
    if errs or warns:
        lines.append("")
        lines.append("achados ({} impeditivos, {} avisos):".format(len(errs), len(warns)))
        for d in errs + warns:
            where = d.get("item") or d.get("locator") or d.get("file") or ""
            lines.append("  [{}] {}{} — {}".format(
                d.get("code", ""), where, " · " if where else "", d.get("message", "")))
    if result.get("limitations"):
        lines.append("")
        lines.append("fontes que não se conseguem ler ({}):".format(
            len(result["limitations"])))
        for lim in result["limitations"]:
            lines.append("  {} — {}".format(lim.get("unit_key", ""), lim.get("reason", "")))
    lines.append("")
    lines.append("Estrutura, cobertura, aprovação e ponta-a-ponta são quatro perguntas")
    lines.append("separadas, de propósito. Isto responde à segunda.")
    return "\n".join(lines)


def _precheck_text(pre: dict) -> str:
    v = pre.get("versions") or {}
    e = pre.get("expected") or {}
    up = pre.get("upstream") or {}
    lines = ["engagement: {} · deliverable: {}".format(pre.get("engagement", ""),
                                                       pre.get("deliverable", "")),
             "template: {} ({})".format(pre.get("template", ""),
                                        pre.get("template_state", "")),
             "",
             "  {:<26} {}".format("versão que o contrato lê",
                                  pre.get("declared") or "(não declarada)"),
             "  {:<26} {}".format("versão resolvida",
                                  e.get("version") or "nenhuma — " + str(e.get("reason", ""))),
             "  {:<26} {}".format("desenho autorizado", v.get("latest_authorized") or "nenhum"),
             "  {:<26} {}".format("desenho aprovado", v.get("approved") or "nenhum"),
             "  {:<26} {}".format("escolhas estruturais", v.get("structural_open", 0)),
             "",
             "  {:<26} {} ({})".format("revisão a montante", up.get("stage", ""),
                                       up.get("record") or "sem registo")]
    for label, key in (("contrato do registo", "contract_validity"),
                       ("actualidade da base", "freshness"),
                       ("revisão das fontes", "source_review"),
                       ("cobertura", "coverage")):
        lines.append("  {:<26} {}".format(label, up.get(key, "not_evaluated")))
    if pre.get("diagnostics"):
        lines.append("")
        lines.append("achados ({} impeditivos):".format(pre.get("blocking", 0)))
        for d in pre["diagnostics"]:
            lines.append("  [{}] {} — {}".format(d.get("code", ""),
                                                 d.get("severity", ""),
                                                 d.get("message", "")))
    lines.append("")
    lines.append("Isto são factos para a declaração do template decidir. Uma ausência")
    lines.append("legítima é *não aplicável*, e não é lacuna.")
    return "\n".join(lines)


def _exit_for(result: dict) -> int:
    """Contrato §7: 0 sem lacunas impeditivas PARA A ETAPA; 2 schema; 4 o resto."""
    if result.get("contract_validity") in ("invalid", "unsupported"):
        return 2
    return 0 if result.get("eligible") else 4


def _target_arg(eng: Path, stage: str, target: str | None) -> dict | None:
    if stage == "reconciliation":
        if target:
            raise CoverageError(
                "a etapa `reconciliation` não tem alvo (contrato §4.6)", 2)
        return None
    if not target:
        raise CoverageError(
            "a etapa {!r} exige `--target <ficheiro>`; antes de renderizar, é "
            "`--deliverable <id>` sem alvo que dá o pré-render (contrato §4.6, §8.2)"
            .format(stage), 2)
    eng_real = eng.resolve()
    p = Path(target)
    rel = target
    if p.is_absolute():
        try:
            rel = p.resolve().relative_to(eng_real).as_posix()
        except ValueError:
            raise CoverageError(
                "alvo fora do engagement, recusado sem ler: {}".format(target), 3)
    elif (Path.cwd() / p).resolve().is_file():
        cand = (Path.cwd() / p).resolve()
        if _within(cand, eng_real):
            rel = cand.relative_to(eng_real).as_posix()
    return {"file": rel, "identity": target_identity(eng, stage, rel)}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="coverage.py",
        description="Inventário, verificação e publicação da revisão de cobertura. "
                    "`inventory`, `check` e `report` não escrevem nada; `finalize` é a "
                    "única operação de escrita, e escreve só em `_coverage/`.")
    parser.add_argument("--version", action="version",
                        version="coverage.py {}".format(TOOL_VERSION))
    sub = parser.add_subparsers(dest="command", required=True)

    inv = sub.add_parser("inventory", help="denominador do engagement")
    chk = sub.add_parser("check", help="veredictos de uma etapa (read-only)")
    rep = sub.add_parser("report", help="projecção Markdown de um registo (read-only)")
    fin = sub.add_parser("finalize", help="publica um rascunho como versão nova")
    for p in (inv, chk, rep, fin):
        p.add_argument("--engagement", default=None,
                       help="slug ou caminho; obrigatório quando há mais do que um")
    for p in (inv, chk, rep, fin):
        p.add_argument("--json", action="store_true", help="JSON em vez de texto")
    for p in (chk, rep):
        p.add_argument("--stage", default="reconciliation", choices=list(STAGES))
        p.add_argument("--target", default=None,
                       help="ficheiro alvo; exigido em `blueprint` e `render`")
    chk.add_argument("--deliverable", default=None,
                     help="id do deliverable, quando a etapa é `render`; sem `--target` "
                          "corre o pré-render (§8.2)")
    chk.add_argument("--template", default=None,
                     help="template do deliverable; por omissão, o do pacote activo")
    rep.add_argument("--record", default=None,
                     help="registo a projectar; por omissão, o aplicável à etapa")
    fin.add_argument("--draft", required=True, help="rascunho JSON a publicar")
    args = parser.parse_args(argv)

    try:
        eng = find_engagement(args.engagement)
        readers = ReaderAdapter()
        if args.command == "inventory":
            inventory = build_inventory(eng, readers)
            print(json.dumps(inventory, ensure_ascii=False, indent=2) if args.json
                  else _inventory_text(inventory))
            # 4 = correu e há lacunas que impedem uma revisão completa sobre esta base.
            return 4 if not inventory["complete"] else 0

        if args.command == "check":
            # §8.2 pré-render: antes de produzir não há alvo nenhum para apontar, e a
            # pergunta é outra — que autoridades é que ESTE deliverable exige.
            if args.stage == "render" and args.deliverable and not args.target:
                pre = render_precheck(eng, args.deliverable, args.template, readers)
                print(json.dumps(pre, ensure_ascii=False, indent=2, default=str)
                      if args.json else _precheck_text(pre))
                return 4 if pre["blocking"] else 0
            target = _target_arg(eng, args.stage, args.target)
            result = coverage_state(eng, args.stage, target, readers)
            if args.deliverable and args.stage == "render":
                result["deliverable_requested"] = args.deliverable
            print(json.dumps(result, ensure_ascii=False, indent=2, default=str)
                  if args.json else _state_text(result))
            return _exit_for(result)

        if args.command == "report":
            target = _target_arg(eng, args.stage, args.target)
            if args.record:
                record, state = read_draft(Path(args.record))
                if state != "ok":
                    raise CoverageError("registo {}: {}".format(state, args.record),
                                        3 if state == "absent" else 2)
                result = coverage_state(eng, record.get("stage", args.stage),
                                        record.get("target") or target, readers,
                                        record=record, record_name=args.record)
            else:
                result = coverage_state(eng, args.stage, target, readers)
                entry = (result.get("record") or {})
                record = None
                if entry:
                    record = guarded_read_json(eng, entry["file"])[0]
            print(json.dumps(result, ensure_ascii=False, indent=2, default=str)
                  if args.json else render_report(record, result))
            return _exit_for(result)

        outcome = finalize(eng, Path(args.draft), readers)
        if args.json:
            print(json.dumps(outcome, ensure_ascii=False, indent=2, default=str))
        else:
            print(outcome["message"])
            for d in outcome.get("diagnostics", []):
                if d.get("severity") == "error":
                    print("  [{}] {}".format(d.get("code", ""), d.get("message", "")))
        if not outcome["published"]:
            return 2 if outcome["reason"] == "schema" else 4
        return _exit_for(outcome["result"])
    except CoverageError as exc:
        print(str(exc), file=sys.stderr)
        return exc.exit_code
    except Exception as exc:                                        # noqa: BLE001
        print("{}: {}".format(COV_UNEXPECTED, exc), file=sys.stderr)
        return 5


def _utf8_console() -> bool:
    """Tenta pôr a consola em UTF-8; devolve se conseguiu. Falhar aqui é normal fora de um
    terminal, e é por isso que devolve um valor em vez de engolir a excepção."""
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        return True
    except Exception:                                               # noqa: BLE001
        return False


if __name__ == "__main__":
    _utf8_console()
    sys.exit(main())
