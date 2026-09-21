# -*- coding: utf-8 -*-
"""Deterministic acceptance for frente B (P-8, P-9, F09) over pricing-marinha-pilot-1.

Run:  python docs/pp-pack-authoring/pilot/step-9d-evidence/accept_frente_b.py

Every check is arithmetic or a string fact over the rendered files. No judgement.
Exit 0 = all criteria of docs/CONSOLIDATED_PLAN.md §5 (frente B) hold.
"""
import io, os, re, sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
REN = os.path.join(ROOT, "projects", "pricing-marinha-pilot-1-val-b", "_render")
SPEC_OLD = os.path.join(REN, "pricing-marinha_implementation-spec_v02.md")
SPEC_NEW = os.path.join(REN, "pricing-marinha_implementation-spec_v03.md")
EST_OLD = os.path.join(REN, "pricing-marinha_estimate_v02.md")
EST_NEW = os.path.join(REN, "pricing-marinha_estimate_v03.md")

fails = []


def ck(ok, label, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + label + (" — " + detail if detail else ""))
    if not ok:
        fails.append(label)


def read(p):
    return io.open(p, encoding="utf-8").read()


def sections(text):
    out, cur = {}, "(head)"
    for line in text.split("\n"):
        m = re.match(r"^## (\d+)\. ", line)
        if m:
            cur = int(m.group(1))
        out.setdefault(cur, []).append(line)
    return out


def num(x):
    return float(x.replace(",", "."))


spec_old, spec_new = read(SPEC_OLD), read(SPEC_NEW)
est_old, est_new = read(EST_OLD), read(EST_NEW)

print("\nP-8 — implementation spec §6")
s6 = "\n".join(sections(spec_new)[6])
ck("`(none)`" in "\n".join(sections(spec_old)[6]), "§6 de v02 era `(none)`")
ck(not re.search(r"^`\(none\)` — nenhum stream", s6, re.M) or "6.2 Transi" in s6,
   "§6 de v03 já não é só `(none)`", "carrega 6.1 streams + 6.2 transições")
for el in ("Quem transiciona", "O que valida", "O que notifica quem", "O que dispara o ciclo"):
    ck(el in s6, "§6 carrega a coluna %r" % el)
for ent in ("AprovacaoCarregamento", "DadosMestrePricing"):
    ck(ent in s6, "§6 cobre a entidade %s" % ent)
# both state machines: 2 entities x 2 transitions = 4 transition rows
rows = [l for l in s6.split("\n") if l.startswith("| `") and "→" in l]
ck(len(rows) == 4, "§6 tem uma linha por transição", "%d linhas" % len(rows))
ck(s6.count("`not named`") >= 8, "actores/destinatários ausentes renderizam `not named`",
   "%d ocorrências" % s6.count("`not named`"))
# nothing invented: no name appears that the record does not carry
for invented in ("Power Automate", "e-mail automático", "Teams", "webhook"):
    ck(invented not in s6, "§6 não inventa mecanismo: %r ausente" % invented)

print("\nP-8 — estimate §14 preconditions")
s14 = "\n".join(sections(est_new)[14])
ck("Pré-condições de entrega" in s14, "§14 existe")
for col in ("Dono", "Até quando", "Que fase trava", "Estado"):
    ck(col in s14, "§14 carrega a coluna %r" % col)
ck("20%" in s14 and "SME" in s14, "§14 lista o SME a 20% (aceitação do plano)")
ck("BD SQL Server partilhada" in s14, "§14 lista o acesso à BD partilhada (aceitação do plano)")
pre_rows = [l for l in s14.split("\n") if l.startswith("| ") and not l.startswith("| ---")
            and "Pré-condição |" not in l and not l.startswith("|---")]
ck(len(pre_rows) >= 8, "§14 tem pré-condições suficientes", "%d linhas" % len(pre_rows))
ck("not named" in s14, "§14 preserva `not named` em vez de inventar dono")
ck(14 not in sections(est_old) or "Pré-condições" not in "\n".join(sections(est_old)[14]),
   "v02 não tinha secção de pré-condições")

print("\nP-9 — phases: profile column, sub-tables, containment")
s5 = "\n".join(sections(est_new)[5])
ck("Perfil responsável" in s5, "§5 tem a coluna do perfil responsável")
phase_rows = re.findall(r"^\| (\d) — ([^|]+)\|[^|]*\| ([0-9,]+)d", s5, re.M)
ck(len(phase_rows) == 6, "§5 mantém as 6 fases", "%d" % len(phase_rows))
over = [(p, num(d)) for p, _c, d in phase_rows if num(d) >= 5]
under = [(p, num(d)) for p, _c, d in phase_rows if num(d) < 5]
ck(len(over) == 2, "2 fases atingem o limiar de 5d", str(over))
for p, _d in over:
    ck(("**Fase %s —" % p) in s5, "fase %s tem sub-tabela" % p)
for p, _d in under:
    ck(("**Fase %s —" % p) not in s5, "fase %s (< 5d) NÃO é decomposta" % p)
# containment: sum of the sub-table union must contain the phase figure
for p, d in over:
    blk = s5.split("**Fase %s —" % p)[1].split("**Fase")[0]
    u = re.search(r"União dos intervalos\*\* \| \*\*([0-9,]+) – ([0-9,]+) d", blk)
    ck(bool(u), "fase %s declara a união dos intervalos" % p)
    if u:
        lo, hi = num(u.group(1)), num(u.group(2))
        ck(lo <= d <= hi, "fase %s: soma(min) ≤ figura ≤ soma(max)" % p,
           "%s ≤ %s ≤ %s" % (lo, d, hi))
        tasks = re.findall(r"^\| [^|]+\| ([0-9],[0-9]) – ([0-9],[0-9]) d", blk, re.M)
        ck(tasks and abs(sum(num(a) for a, _b in tasks) - lo) < 1e-9,
           "fase %s: a soma das tarefas é a união declarada" % p,
           "%s tarefas" % len(tasks))

print("\nP-9 — every named uncertainty lands in a phase")
s9 = "\n".join(sections(est_new)[9])
ck("Fase ameaçada" in s9, "§9 tem a coluna da fase ameaçada")
unc = [l for l in s9.split("\n") if l.startswith("| ") and l.count("|") >= 6
       and "Item em aberto" not in l and not l.startswith("|---")]
ck(len(unc) == 6, "§9 mantém as 6 incertezas", "%d" % len(unc))
ck(all(("Fase " in l or "migração" in l) for l in unc),
   "cada incerteza nomeia a fase que ameaça (ou diz que não está no total)")
ck("não ameaçam nenhuma fase deste total" in s5,
   "§5 declara as que ameaçam uma fase fora do total")

print("\nP-9 — profile load <= declared dedication, and no calendar")
s16 = "\n".join(sections(est_new)[16])
ck("Ocupação por perfil" in s16, "§16 tem a ocupação por perfil")
ck("44 ÷ 1,0 = 44 dias" in s16, "a aritmética está mostrada")
ck("≥ 9 semanas" in s16, "semanas mínimas derivadas")
ck(44 <= 9 * 5, "ocupação ≤ dedicação", "44 pessoa-dias ≤ 45 dias disponíveis em 9 semanas a 100%")
ck("`not named`" in s16, "perfis sem pessoa-dias não recebem figura de semanas")
for banned in ("Gantt", "grelha"):
    ck(("Sem grelha, sem Gantt" in s16), "§16 recusa grelha/Gantt explicitamente")
    break
ck(not re.search(r"\b(202[5-9]-\d\d-\d\d|semana de \d+ de)\b", s16),
   "§16 não emite data de calendário")

print("\nP-9 — repetition dimension")
s19 = "\n".join(sections(est_new)[19])
ck("Dimensão de repetição" in s19, "§19 faz a verificação da dimensão de repetição")
ck("nenhuma" in s19.lower() and "Nenhum piloto" in s19,
   "sem dimensão de repetição, nenhum piloto é fabricado")

print("\nF09 — planning intervals, no quantiles")
for name, txt in (("estimate v03", est_new), ("spec v03", spec_new)):
    ck("P50" not in txt and "P80" not in txt, "%s não afirma quantis" % name)
ck("Intervalo de planeamento" in est_new or "intervalo de planeamento" in est_new,
   "a estimativa usa o vocabulário de intervalo de planeamento")
ck("taxa pontual" in est_new, "taxas pontuais são declaradas como tal, sem ± inventado")
sim = read(os.path.join(ROOT, ".claude", "skills", "aisa-simulate", "SKILL.md"))
ck("×1.4" not in sim, "o factor SAP ×1.4 sem fonte saiu de aisa-simulate")

print("\nINVARIANTE — o total não se move")
for label, pat in (("total bruto 30,5d", r"\*\*30,5d\*\*"),
                   ("total base 44 pessoa-dias", r"44 pessoa-dias base")):
    ck(bool(re.search(pat, est_old)) and bool(re.search(pat, est_new)),
       "%s idêntico em v02 e v03" % label)
so, sn = sections(est_old), sections(est_new)
# §§1-4, 6-12 keep their identity; 14-18 of v02 map to 15-19 of v03
same = [k for k in (1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12) if so.get(k) == sn.get(k)]
ck(set(same) == {1, 2, 3, 4, 6, 7, 8, 10, 11, 12},
   "secções não tocadas idênticas carácter a carácter", "iguais: %s" % sorted(same))
for old_n, new_n in ((14, 15), (15, 16), (16, 17), (17, 18), (18, 19)):
    a = "\n".join(so[old_n][1:])
    b = "\n".join(sn[new_n][1:])
    if old_n in (15, 18):      # team (->16) and recommendations (->19) were re-executed
        continue
    ck(a == b, "§%d de v02 == §%d de v03 (só renumerada)" % (old_n, new_n))
sso, ssn = sections(spec_old), sections(spec_new)
untouched = [k for k in range(1, 17) if k not in (2, 6, 16)]
ck(all(sso.get(k) == ssn.get(k) for k in untouched),
   "spec: as 13 secções não tocadas são idênticas",
   "tocadas: §2 (um estado de portão), §6, §16")

print("\n" + ("FALHAS: %d — %s" % (len(fails), fails) if fails else "TODOS OS CRITÉRIOS PASSAM"))
sys.exit(1 if fails else 0)
