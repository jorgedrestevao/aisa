# P1 — Mapa de autoridades

Quem manda em cada campo, e quem só lê. Construído por leitura das 24 skills, uma a uma,
mais a camada Python já verificada em `writer-reader-map.md`.

Método: para cada artefacto, extrair **todas** as menções em `.claude/skills/*/SKILL.md`
com contexto, e classificar cada uma pela operação que a skill **declara** — não pela
presença do nome do ficheiro. A maioria das menções são **listas de leitura** no cabeçalho
da skill; contá-las como escrita é o erro que o varrimento por verbos comete.

## 1. `shared-understanding.md` — a fonte da verdade

A regra do kernel («em modo council-independent, `chairman-synthesis` é o único escritor»)
**é verdadeira e é por modo**. Não é global. Lida como global, parece contradita pelas
lentes; lida como escrita, não há contradição nenhuma.

| Escritor | Quando | Operação declarada |
|---|---|---|
| As 7 lentes (`lens-business`, `lens-data`, `lens-financial`, `lens-governance`, `lens-operations`, `lens-user`, `lens-technology`) | Discovery, **inline** | uma linha por achado material, `lens=<nome>`, com evidência + ronda (L29 de cada; L39 na technology) |
| `chairman-synthesis` | Framing e Options, **council-independent** | **append-only** (L113): nunca apaga nem reescreve; transições acrescentam linha nova |
| `aisa-start` | criação do engagement | escreve o **esqueleto** (L95): as 5 secções de estado com os cabeçalhos de coluna. Estrutura, não conteúdo |
| `aisa-status` | qualquer fase | **uma única escrita sancionada** (L41): actualiza o cabeçalho `Saúde epistémica:` a partir de `model.health`. Não toca em linhas |

**Leem e não escrevem:** `aisa-answer`, `aisa-blueprint`, `aisa-decide`, `aisa-frame`,
`aisa-options`, `aisa-premortem`, `aisa-render`, `aisa-revisit`, `aisa-round`,
`aisa-simulate`, `aisa-synthesize`.

`aisa-round` aparece a mexer na SU mas não escreve: o que faz é **varrer** para achar o
próximo id livre por prefixo (`C-`, `A-`, `U-`, `X-`, …) e passá-lo às lentes (L39, L46).
`aisa-frame` e `aisa-options` declaram linhas novas na SU mas atribuem-nas explicitamente
a `chairman-synthesis` («New rows in `shared-understanding.md` (chairman-synthesis)»).

### Correcção a uma leitura anterior

A revisão anterior deste trabalho registou isto como **contradição por resolver** entre o
kernel e as skills. Não é contradição: é uma regra com âmbito de modo, que o varrimento por
verbos achatou. O kernel está certo e as skills também.

## 2. `_state.json` — fase e ronda

**Seis escritores. Os seis declaram escrita atómica.** Zero lacunas.

| Escritor | Onde declara | Padrão |
|---|---|---|
| `aisa-start` | L82 | escreve `_state.json.tmp`, depois renomeia sobre `_state.json` |
| `aisa-frame` | L38, L104 | «atomic write — this skill»; `phase`, `round`, `round_in_progress` |
| `aisa-options` | L36, L103 | «atomic write (this skill)» |
| `aisa-decide` | L32, L78 | «(atomic, this skill)»; secção «Flip state to Decision (atomic)» |
| `aisa-capture` | L68 | «Increment `capture_run` … (atomically: tmp → rename)» |
| `chairman-synthesis` | L117, L478 | «Atomic writes. Update `_state.json` via tmp → rename» |

### Correcção a uma leitura anterior

A revisão anterior disse «7 candidatos a escritor, só 4 declaram `tmp → mv`». Errado nos
dois números. São **6** escritores e **6** declaram o padrão. O varrimento falhou nos dois
sentidos: contou listas de leitura como escrita, e perdeu `aisa-capture`, cujo verbo é
*Increment* e não *escrever*.

O princípio 8 do `CLAUDE.md` — escrita atómica a `_state.json` — está **cumprido em todos
os escritores declarados**.

## 3. Restantes autoridades

| Artefacto | Autoridade | Nota |
|---|---|---|
| `answers.md` | `aisa-answer` | resposta **literal** do utilizador, preservada verbatim |
| `decisions.md` | `aisa-decide` (D-NNN), `aisa-frame` (aprovação do frame) | append |
| `_coverage/` | **só** `coverage.py finalize` | verificado no código: 8 chamadas, todas em L3594-3660 |
| `dashboard.html` | **só** `dashboard.py` | projecção gerada; nunca editar à mão |
| `_capture/` | `xlsx_extract.py`, `text_extract.py`, `fields_draft.py` | via `aisa-capture` |
| `_synthesis/` | `aisa-synthesize` | auto após `/decide` |
| `_blueprint/` | `aisa-blueprint` | iterado até aprovação (D-NNN) |
| `_render/` | `aisa-render` | filtrado pelo tipo de decisão |
| `_simulation/` | `aisa-simulate`, `aisa-revisit` | advisory |
| `_retro/` | `aisa-retro` | **staging**; só entra em agent-memory após aprovação humana |
| `gate-log.md` | hook `phase-gate-check.py` | |
| `lens-outputs/` | as 7 lentes + `chairman-synthesis` | |

## 4. O que isto fixa para P2

O alvo **já tem** as garantias por artefacto:

- escrita atómica a `_state.json`, declarada nos 6 escritores;
- `coverage.py` com uma única porta de escrita, confinada a `_coverage/`;
- `dashboard.py` com escrita atómica (pid no tmp) e um lock próprio;
- SU append-only, com escritores por modo e uma única escrita sancionada fora deles.

O que **não** tem, e que P2 deve acrescentar sem duplicar o que existe:

1. **Atomicidade entre artefactos.** Uma operação de domínio toca SU + `_state.json` +
   `answers.md`; cada escrita é atómica por si, nenhuma o é em conjunto. Falha entre a
   primeira e a segunda deixa estado misto que nada detecta.
2. **Exclusão que valha para mais do que o dashboard.** O único lock existente é do
   `dashboard.py` e não exclui escritas à SU nem ao estado.
3. **Observação de escritas por subprocesso.** Documentado no próprio código
   (`on-su-change.py:38-40`): `PostToolUse` nunca dispara sobre elas.

Os três são a lacuna real. Nenhum se resolve com mais um hook de `Write|Edit`.
