# -*- coding: utf-8 -*-
"""extract-direct.py -- extracções directas sobre a fonte crua, persistidas em `_capture/`.

Decisão do dono (2026-09-08, step-9c §4): uma lente pode ir à fonte crua para lá do que
a extracção guardada cobre, mas **o que de lá retirar fica escrito em `_capture/`** com
nome próprio, e a evidência aponta para esse ficheiro. Sem isso o facto não cumpre a
regra 1 do limiar de `Confirmed` ("o alvo tem de existir").

Duas extracções, as que a ronda R-05 da cópia Sonnet produziu sem persistir:

  weekly   -- `Market View` agregado por semana ISO (suporta C-162). A extracção
              guardada só tem estatística por coluna, não por linha.
  vba      -- texto dos módulos VBA via `oletools.olevba` (suporta C-163). A extracção
              deste engagement nunca descompila VBA (`process-model.md` §7).

Determinístico e idempotente: correr outra vez sobre a mesma fonte reescreve os mesmos
bytes (o SHA-256 da fonte vai no cabeçalho de cada artefacto).

Uso:
    python docs/pp-pack-authoring/pilot/tools/extract-direct.py <engagement-slug> <ficheiro.xlsm>
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
TOOL = "extract-direct.py"

SERIES = ("fx", "PUMFD00", "AAWZC00", "PUAAY00", "AAYWS00")


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:8]


def weekly(src: Path, out: Path) -> dict:
    """`Market View` por semana ISO.

    O cabeçalho da folha ocupa duas linhas e não nomeia os instrumentos -- os códigos
    (`#PUMFD00`, `#fxUSDEURECB`, ...) só existem dentro das fórmulas do add-in de
    mercado. Por isso a coluna de cada série é resolvida pela FÓRMULA, não pelo texto
    do cabeçalho, e só depois se contam os valores em cache.
    """
    import re
    import warnings
    import openpyxl
    warnings.filterwarnings("ignore")

    wbf = openpyxl.load_workbook(src, data_only=False)
    ws = wbf["Market View"]
    col_code: dict[str, str] = {}
    code_row = 0
    for row in ws.iter_rows(max_col=12):
        for c in row:
            v = c.value
            if isinstance(v, str) and "GvDaily" in v:
                codes = re.findall(r'"(#[A-Za-z0-9]+)"', v)
                if codes and c.column_letter not in col_code:
                    col_code[c.column_letter] = codes[0]
                    code_row = code_row or c.row
    wbf.close()
    if not col_code:
        raise SystemExit("nenhuma coluna de instrumento encontrada em Market View")

    wb = openpyxl.load_workbook(src, data_only=True, read_only=True)
    ws = wb["Market View"]
    idx = {openpyxl.utils.column_index_from_string(k) - 1: v
           for k, v in col_code.items()}
    codes = [col_code[k] for k in sorted(col_code)]
    weeks: dict[str, dict[str, int]] = {}
    n_rows = 0
    for row in ws.iter_rows(values_only=True):
        if not row or row[0] is None or not hasattr(row[0], "isocalendar"):
            continue
        n_rows += 1
        iso = row[0].isocalendar()
        key = "{}-W{:02d}".format(iso[0], iso[1])
        bucket = weeks.setdefault(key, {c: 0 for c in codes})
        for i, code in idx.items():
            if i < len(row) and row[i] is not None:
                bucket[code] += 1
    wb.close()

    ordered = dict(sorted(weeks.items()))
    vazias = {c: [w for w, b in ordered.items() if b[c] == 0] for c in codes}
    per_week = [sum(b.values()) / len(codes) for b in ordered.values()]
    payload = {
        "artefact": "aisa.extract-direct.weekly",
        "tool": TOOL,
        "extracted_at": date.today().isoformat(),
        "source": {"file": src.name, "sha256": sha256(src), "sheet": "Market View",
                   "range": ws.calculate_dimension() if hasattr(ws, "calculate_dimension")
                            else "A1:N416"},
        "method": ("coluna->instrumento resolvida pela formula do add-in na linha {} "
                   "(`_xll...GvDaily(\"<codigo>\")`), porque o cabecalho de duas linhas "
                   "nao nomeia os instrumentos; contagem de valores em cache nao-nulos "
                   "por serie e por dia (openpyxl data_only=True), agrupada pela semana "
                   "ISO da coluna A".format(code_row)),
        "colunas": col_code,
        "series": codes,
        "linhas_de_data_lidas": n_rows,
        "semanas": len(ordered),
        "primeira": next(iter(ordered), ""),
        "ultima": next(reversed(ordered), ""),
        "semanas_vazias_por_serie": vazias,
        "observacoes_por_semana_media": round(sum(per_week) / len(per_week), 2)
                                        if per_week else 0,
        "observacoes_por_semana_min": min((min(b.values()) for b in ordered.values()),
                                          default=0),
        "observacoes_por_semana_max": max((max(b.values()) for b in ordered.values()),
                                          default=0),
        "por_semana": ordered,
    }
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
    return payload


def vba(src: Path, out: Path) -> dict:
    """Texto dos módulos VBA. O que a extracção do engagement não decompõe (§7)."""
    from oletools.olevba import VBA_Parser
    p = VBA_Parser(str(src))
    mods = []
    if p.detect_vba_macros():
        for _f, _s, name, code in p.extract_macros():
            code = (code or "").replace("\r\n", "\n")
            subs = [l.strip() for l in code.split("\n")
                    if l.strip().lower().startswith(("sub ", "function ",
                                                     "private sub ", "public sub "))]
            mods.append({"modulo": name, "linhas": len(code.split("\n")),
                         "rotinas": subs, "codigo": code})
    p.close()

    lines = [
        "# Extracção directa — VBA de `{}`".format(src.name),
        "",
        "> Artefacto: `aisa.extract-direct.vba` · gerado por `{}` · {}".format(
            TOOL, date.today().isoformat()),
        "> Fonte: `inputs/{}` (sha256 `{}`)".format(src.name, sha256(src)),
        "> Método: `oletools.olevba` `VBA_Parser.extract_macros()`, texto integral, sem edição.",
        "> Porquê aqui: a extracção deste engagement nunca descompila VBA "
        "(`process-model.md` §7). Esta é a evidência que faltava existir para a citar.",
        "",
        "## Sumário",
        "",
        "| módulo | linhas | rotinas com lógica |",
        "|---|---|---|",
    ]
    for m in mods:
        lines.append("| `{}` | {} | {} |".format(
            m["modulo"], m["linhas"],
            ", ".join("`{}`".format(s) for s in m["rotinas"]) or "— (nenhuma)"))
    lines += ["", "## Texto integral", ""]
    for m in mods:
        lines += ["### `{}`".format(m["modulo"]), "", "```vb", m["codigo"].rstrip(),
                  "```", ""]
    out.write_text("\n".join(lines), encoding="utf-8")
    return {"modulos": len(mods),
            "com_rotinas": [m["modulo"] for m in mods if m["rotinas"]],
            "rotinas": [s for m in mods for s in m["rotinas"]]}


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    slug, fname = sys.argv[1], sys.argv[2]
    eng = REPO / "projects" / slug
    src = eng / "inputs" / fname
    cap = eng / "_capture"
    if not src.is_file():
        raise SystemExit("fonte inexistente: {}".format(src))

    w_out = cap / (fname + ".market-view-weekly.json")
    v_out = cap / (fname + ".vba.md")
    w = weekly(src, w_out)
    v = vba(src, v_out)

    vazias = {s: len(x) for s, x in w["semanas_vazias_por_serie"].items()}
    log = cap / "_capture-log.md"
    with open(log, "a", encoding="utf-8") as f:
        f.write(
            "| {} | XD | {} | written | {} semanas ISO ({} a {}), {} linhas de data; "
            "semanas sem observação por série: {}; média {} obs/semana | fonte sha256 {} |\n"
            .format(date.today().isoformat(), w_out.name, w["semanas"], w["primeira"],
                    w["ultima"], w["linhas_de_data_lidas"], vazias,
                    w["observacoes_por_semana_media"], w["source"]["sha256"]))
        f.write(
            "| {} | XD | {} | written | {} módulos, {} com rotinas ({}); rotinas: {} | "
            "fonte sha256 {} |\n"
            .format(date.today().isoformat(), v_out.name, v["modulos"],
                    len(v["com_rotinas"]), ", ".join(v["com_rotinas"]) or "nenhum",
                    ", ".join(v["rotinas"]) or "nenhuma", w["source"]["sha256"]))

    print("weekly -> {}".format(w_out.name))
    print("  {} semanas ISO, {} a {}; linhas de data {}".format(
        w["semanas"], w["primeira"], w["ultima"], w["linhas_de_data_lidas"]))
    print("  semanas sem observação, por série: {}".format(vazias))
    print("  obs/semana: min {} · max {} · média {}".format(
        w["observacoes_por_semana_min"], w["observacoes_por_semana_max"],
        w["observacoes_por_semana_media"]))
    print("vba -> {}".format(v_out.name))
    print("  {} módulos, com rotinas: {}".format(
        v["modulos"], ", ".join(v["com_rotinas"]) or "nenhum"))
    print("  rotinas: {}".format(", ".join(v["rotinas"]) or "nenhuma"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
