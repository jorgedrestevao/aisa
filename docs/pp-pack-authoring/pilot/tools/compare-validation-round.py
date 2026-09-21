# -*- coding: utf-8 -*-
"""compare-validation-round.py -- frente A, sessão de validação (step-9c §5).

Corre `dashboard.py --json` nas duas cópias de validação, compara com a linha de base
registada em `step-9c-frente-a-codigo.md` §5.1, e imprime as sete aceitações da frente A
lado a lado.

O que este script faz: **factos**. Contagens do motor, presença de declarações por regex,
invariantes aritméticos. O que NÃO faz: julgar se uma pergunta é material, se uma
afirmação está ao nível da evidência, ou se uma resposta é boa. Cada aceitação que exige
leitura humana imprime a lista exacta de ids a ler, e diz que é para ler.

Uso:
    python docs/pp-pack-authoring/pilot/tools/compare-validation-round.py
    python .../compare-validation-round.py --ronda R-05
    python .../compare-validation-round.py --engagements slug-a slug-b --json-out <dir>
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
MOTOR = REPO / "library" / "kernel" / "tools" / "dashboard.py"
BASELINE = Path(__file__).resolve().parent / "baseline-val-R04.json"
DEFAULT_ENGAGEMENTS = ("pricing-marinha-pilot-3-val-sonnet",
                       "pricing-marinha-pilot-3-val-opus")

# Zero regex aqui por desenho. Toda a regra determinística vive no motor
# (`library/kernel/tools/dashboard.py` 1.3.0+) e chega por JSON com o seu próprio
# padrão, a sua postura de falsos negativos e o que deixa para julgamento. Duas casas
# para a mesma regra divergem — foi por isso que estes três regex saíram daqui.


def run_motor(slug: str, out_dir: Path) -> dict:
    out = out_dir / (slug + ".json")
    cmd = [sys.executable, str(MOTOR), "--engagement", slug, "--json", str(out), "--quiet"]
    r = subprocess.run(cmd, cwd=str(REPO), capture_output=True, text=True)
    if not out.is_file():
        raise SystemExit("motor falhou em {}:\n{}{}".format(slug, r.stdout, r.stderr))
    return json.loads(out.read_text(encoding="utf-8"))


def novas(model: dict, ronda: str, state: str | None = None) -> list[dict]:
    return [r for r in model["su"]["rows"]
            if r["ronda"] == ronda and (state is None or r["state"] == state)]


def veredicto(ok: bool | None) -> str:
    return {True: "PASSA", False: "FALHA", None: "LER"}[ok]


def avalia(model: dict, ronda: str, base: dict) -> dict:
    """As sete aceitações. `ok=None` = precisa de leitura humana; a lista de ids vai junto."""
    rows = model["su"]["rows"]
    u_novas = novas(model, ronda, "Unknown")
    c_novas = novas(model, ronda, "Confirmed")
    a_novas = novas(model, ronda, "Assumed")
    ids_ronda = {r["id"] for r in novas(model, ronda)}
    res: dict = {}

    # --- P-0 enquadramento ---------------------------------------------------
    enq = model["enquadramento"]
    arb = model["arbiter"]
    sem_m = [x["id"] for x in arb["sem_citacao_m"] if x["ronda"] == ronda]
    res["P-0"] = {
        "ok": None if u_novas else True,
        "facto": "enquadramento presente: {} · invariantes {} · R-00 rotulada `{}`"
                 .format(enq["presente"], len(enq["invariantes"]), enq["rotulo"]),
        "ler": ("{} de {} Unknown novas não citam nenhum M-n — ler se alguma pergunta o "
                "PORQUÊ que M-1/M-2 já respondem: {}"
                .format(len(sem_m), len(u_novas), ", ".join(sem_m) or "—")),
    }

    # --- P-1 teste de divergência -------------------------------------------
    sem_decl = [x for x in arb["sem_declaracao"] if x["ronda"] == ronda]
    decisivas = [r for r in u_novas if r["swing_class"] == "decisivo"]
    sem_ref = [x["id"] for x in arb["decisivo_sem_referente"]
               if x["ronda"] == ronda]
    res["P-1"] = {
        "ok": (not sem_decl) and (not sem_ref) if u_novas else True,
        "facto": ("{} de {} Unknown novas sem declaração · {} `decisivo`, {} sem referente "
                  "nomeado".format(len(sem_decl), len(u_novas), len(decisivas),
                                   len(sem_ref))),
        "ler": ("sem declaração: {} · decisivo sem referente: {}"
                .format(", ".join(x["id"] for x in sem_decl) or "—",
                        ", ".join(sem_ref) or "—")),
    }

    # --- P-2 convergência ----------------------------------------------------
    rd = model["round_delta"]
    ent = next((x for x in rd["por_ronda"] if x["ronda"] == ronda), None)
    res["P-2"] = {
        "ok": (not ent["sem_convergencia"]) if ent else None,
        "facto": ("{}: {} criadas / {} fechadas · {} abertas ({} Critical){}"
                  .format(ronda, ent["criadas"], ent["fechadas"], rd["abertas"],
                          rd["critical_abertas"],
                          " · SEM CONVERGÊNCIA" if ent["sem_convergencia"] else "")
                  if ent else "{} não aparece em round_delta".format(ronda)),
        "ler": ("{} fecho(s) sem data determinável".format(len(rd["indeterminadas"]))
                if rd["indeterminadas"] else "0 fechos indetermináveis"),
    }

    # --- P-3 PM-U por conteúdo ----------------------------------------------
    pm = (REPO / "projects" / model["engagement"]["slug"] /
          "_capture" / "process-model.md")
    pm_txt = pm.read_text(encoding="utf-8") if pm.is_file() else ""
    # A ÚNICA regra que ainda vive aqui e não no motor: o motor não lê
    # `process-model.md`. Mover isto exige dar-lhe um parser de PM-U, que é
    # feature, não limpeza — fica nomeado em vez de escondido.
    # a coluna vive na tabela do §6 (a que tem `id` e `question`), não em qualquer
    # tabela do ficheiro -- §2 também tem uma coluna chamada `classe`, de classes de
    # coluna do Excel, que não é esta.
    hdr = re.search(r"^\|\s*id\s*\|\s*(?:question|pergunta)\s*\|.*$",
                    pm_txt, re.M | re.I)
    cols = ([c.strip().lower() for c in hdr.group(0).strip().strip("|").split("|")]
            if hdr else [])
    idx = cols.index("classe") if "classe" in cols else None
    tem_classe = idx is not None
    classes = {}
    for pid in ("PM-U-026", "PM-U-003"):
        m = re.search(r"^\|\s*" + pid + r"\s*\|.*$", pm_txt, re.M)
        if not m:
            continue
        cells = [c.strip() for c in m.group(0).strip().strip("|").split("|")]
        classes[pid] = (cells[idx] if idx is not None and idx < len(cells)
                        else "sem coluna `classe`")
    res["P-3"] = {
        "ok": (None if not tem_classe else
               classes.get("PM-U-026") == "mecânica"
               and classes.get("PM-U-003") == "dados"),
        "facto": ("§6 com coluna `classe`: {} · PM-U-026 = {} · PM-U-003 = {}"
                  .format(tem_classe, classes.get("PM-U-026", "—"),
                          classes.get("PM-U-003", "—"))),
        "ler": ("a disposição de cada PM-U Critical está nos `Open evidence` de "
                "lens-outputs/ desta ronda — o motor não a lê; ver o output do /round "
                "(step 5e, `undisposed`)"),
    }

    # --- P-4 funding_gate ----------------------------------------------------
    fg = model["funding_gate"]
    gate = fg["funding_gate"]
    fin = [r for r in u_novas if "financial" in r["lens"].lower()]
    infring = [x["id"] for x in fg["infracoes"] if x["ronda"] == ronda]
    res["P-4"] = {
        "ok": (not infring) if gate is False else None,
        "facto": ("funding_gate = {} · {} Unknown novas da lente financeira · {} de "
                  "envelope/limiar/imputação".format(gate, len(fin), len(infring))),
        "ler": ", ".join(infring) or "—",
    }

    # --- P-12 limiar de Confirmed -------------------------------------------
    cl = model["confirmed_locator"]
    avisos = cl["sem_locator"] + cl["alvo_ausente"]
    avisos_novos = [x for x in avisos if x["id"] in ids_ronda]
    res["P-12"] = {
        "ok": not avisos_novos,
        "facto": ("{} Confirmed novas · {} sem prova localizável nesta ronda · {} no "
                  "engagement todo ({} abertas, {} com prova)"
                  .format(len(c_novas), len(avisos_novos), len(avisos),
                          cl["total"], cl["com_locator"])),
        "ler": ("novas sem prova: {} · conclusões de cadeia entraram como Assumed? "
                "ler as {} Assumed novas: {}"
                .format(", ".join(x["id"] for x in avisos_novos) or "—",
                        len(a_novas), ", ".join(r["id"] for r in a_novas) or "—")),
    }

    # --- invariantes ---------------------------------------------------------
    sec = model["su"]["sections"]
    ca = sec["Confirmed"]["open"] + sec["Assumed"]["open"]
    total = sum(sec[s]["open"] + sec[s]["resolved"] for s in sec)
    res["INV"] = {
        "ok": total >= base["total_rows"],
        "facto": ("total de rows {} (base {}, nunca desce) · Confirmed+Assumed abertas {} "
                  "(base {}) · saúde {}% · {} diagnostics"
                  .format(total, base["total_rows"], ca, base["confirmed_mais_assumed"],
                          model["health"]["pct"], len(model["diagnostics"]))),
        "ler": "—",
    }

    # --- material para os dois critérios do plano §5.1 ------------------------
    nao_aplicadas = []
    for r in u_novas:
        faltas = [k for k, v in (("swing", r["swing_inferred"]),
                                 ("custo", r["custo_inferred"]),
                                 ("criticidade", not r["criticidade"])) if v]
        if faltas:
            nao_aplicadas.append("{} ({})".format(r["id"], "+".join(faltas)))
    for r in c_novas + a_novas:
        if not r["verificado_em"] or r["validade_inferred"]:
            nao_aplicadas.append("{} (epistémicas)".format(r["id"]))
    res["_criterios"] = {
        "nao_aplicadas": nao_aplicadas,
        "contornadas": ([x["id"] for x in avisos_novos] + sem_ref),
    }
    return res


def bloco(slug: str, model: dict, res: dict, ronda: str) -> None:
    print("\n" + "=" * 78)
    print("{}  ·  motor {}  ·  fase {} ronda {}"
          .format(slug, model["tool_version"], model["engagement"]["phase"],
                  model["engagement"]["round"]))
    print("=" * 78)
    for k in ("P-0", "P-1", "P-2", "P-3", "P-4", "P-12", "INV"):
        r = res[k]
        print("\n[{}] {}".format(veredicto(r["ok"]).ljust(5), k))
        print("      {}".format(r["facto"]))
        if r["ler"] and r["ler"] != "—":
            print("      ler: {}".format(r["ler"]))
    c = res["_criterios"]
    print("\n--- material para os critérios de §5.1 do plano ---")
    print("  regras NÃO APLICADAS (critério do lado Sonnet): {} — {}"
          .format(len(c["nao_aplicadas"]), ", ".join(c["nao_aplicadas"]) or "nenhuma"))
    print("  regras CONTORNADAS  (critério do lado Opus):   {} — {}"
          .format(len(c["contornadas"]), ", ".join(c["contornadas"]) or "nenhuma"))
    print("  (as duas listas são candidatos deterministas; a contagem final é de leitura)")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--engagements", nargs=2, default=list(DEFAULT_ENGAGEMENTS))
    ap.add_argument("--ronda", default="R-05")
    ap.add_argument("--json-out", default=None,
                    help="onde guardar os JSON do motor (default: temporário)")
    args = ap.parse_args()

    if not BASELINE.is_file():
        raise SystemExit("linha de base ausente: {}".format(BASELINE))
    base = json.loads(BASELINE.read_text(encoding="utf-8"))

    out_dir = Path(args.json_out) if args.json_out else Path(tempfile.mkdtemp())
    out_dir.mkdir(parents=True, exist_ok=True)

    print("linha de base: {} (ronda {}) — {}".format(
        BASELINE.name, base["ronda"], base["nota"]))
    print("ronda avaliada: {}".format(args.ronda))

    resultados = []
    for slug in args.engagements:
        model = run_motor(slug, out_dir)
        res = avalia(model, args.ronda, base)
        bloco(slug, model, res, args.ronda)
        resultados.append((slug, model, res))

    print("\n" + "=" * 78)
    print("LADO A LADO")
    print("=" * 78)
    hdr = "{:<12}".format("") + "".join("{:<34}".format(s.split("val-")[-1])
                                        for s, _, _ in resultados)
    print(hdr)
    for k in ("P-0", "P-1", "P-2", "P-3", "P-4", "P-12", "INV"):
        line = "{:<12}".format(k)
        for _s, _m, res in resultados:
            line += "{:<34}".format(veredicto(res[k]["ok"]))
        print(line)
    for label, key in (("não aplic.", "nao_aplicadas"), ("contorn.", "contornadas")):
        line = "{:<12}".format(label)
        for _s, _m, res in resultados:
            line += "{:<34}".format(len(res["_criterios"][key]))
        print(line)
    print("\nJSON do motor em: {}".format(out_dir))
    m0 = resultados[0][1]
    print("Motor {} · regras e regex vivem lá, não aqui · calibração: {}"
          .format(m0["tool_version"], ", ".join(m0["arbiter"]["calibracao"])))
    print("`LER` NUNCA é passe: é a aceitação que exige leitura humana. Uma lista\nvazia significa 'nada em falta que o regex saiba ver', nunca 'aprovado' — ver\n`julgamento` em cada bloco do JSON.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
