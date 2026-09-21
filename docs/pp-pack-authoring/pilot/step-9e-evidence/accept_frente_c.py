"""Frente C (P-13 / P-14) — deterministic acceptance, before vs after.

Same lint as `.claude/tests/test_user_language.py` (imported, never re-implemented): kernel terms
and ids outside parentheses in what the user reads. "Before" is read from git (`--ref`, default the
last freeze tag) with a heuristic extractor for the old, unmarked output lines; "after" is the
working tree's ```user-output blocks, the dashboard's rendered labels (static source and the page
actually built for pilot-3), and `docs/COMO-USAR.md`.

    python docs/pp-pack-authoring/pilot/step-9e-evidence/accept_frente_c.py [--ref step-9d-frente-b]
"""

import argparse
import importlib.util
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
TEST = os.path.join(ROOT, ".claude", "tests", "test_user_language.py")
spec = importlib.util.spec_from_file_location("ul", TEST)
ul = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ul)

SKILLS = list(ul.COMMAND_SKILLS)


def git_show(ref, path):
    try:
        return subprocess.check_output(["git", "show", "{}:{}".format(ref, path)], cwd=ROOT,
                                       stderr=subprocess.DEVNULL).decode("utf-8")
    except subprocess.CalledProcessError:
        return None


def legacy_blocks(md):
    """Heuristic for the pre-P-13 skills: the text after `Output:` / `Output to the user:` /
    `Wrap-up output` — a quoted string on the same line, a quoted paragraph, or the fenced block
    that follows. Baseline only; the after-state needs no heuristic (```user-output)."""
    lines = md.splitlines()
    out = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        if re.search(r"(\*\*Output\*\*|Output|Wrap-up output|Tell the user)( to the user| summary)?:?", ln) \
                and not ln.lstrip().startswith("-") or re.match(r"\s*- `--all`:", ln):
            q = re.findall(r'"([^"]{20,})"', ln)
            if q:
                out.append("\n".join(q))
                i += 1
                continue
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and lines[j].strip().startswith("```"):
                k = j + 1
                buf = []
                while k < len(lines) and not lines[k].strip().startswith("```"):
                    buf.append(lines[k])
                    k += 1
                out.append("\n".join(buf))
                i = k + 1
                continue
            if j < len(lines) and lines[j].strip().startswith('"'):
                k = j
                buf = []
                while k < len(lines) and lines[k].strip():
                    buf.append(lines[k])
                    k += 1
                out.append("\n".join(buf))
                i = k
                continue
        i += 1
    return out


def html_labels(html):
    """Labels the page renders: section headings, table headers, tabs, the Panorama/Agenda box
    titles. Not content: narrative entry titles, phase-document titles and drawer ids are the
    engagement's own text (council-log, frame.md, SU ids) and are excluded."""
    html = ul.HTML_TITLE_RE.sub("", html)
    # phase documents rendered by extenso (Etapas tab) are the engagement's own markdown
    html = re.sub(r'<details class="doc".*?</details>', "", html, flags=re.S)
    labels = []
    for pat in (r'<h2 class="sec"[^>]*>(.*?)</h2>', r"<th[^>]*>(.*?)</th>",
                r'<button class="tab"[^>]*>(.*?)</button>', r'data-title="([^"]+)"',
                r'<div class="(?:box|bucket)[^"]*"><h3[^>]*>(.*?)</h3>', r"<div><h3>(.*?)</h3>"):
        labels += re.findall(pat, html, flags=re.S)
    return [ul.TAG_RE.sub("", l).replace("&middot;", "·").strip() for l in labels if l.strip()]


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")   # Windows consoles default to cp1252
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default="step-9d-frente-b")
    ap.add_argument("--engagement", default="pricing-marinha-pilot-3")
    a = ap.parse_args()
    terms = ul.glossary_terms()
    fails = 0
    rows = []

    for name in SKILLS:
        rel = ".claude/skills/{}/SKILL.md".format(name)
        before = git_show(a.ref, rel)
        if before is None:
            b_blocks, b_v = "—", "—"
        else:
            blocks = legacy_blocks(before)
            b_blocks = len(blocks)
            b_v = sum(len(ul.violations(b, terms)) for b in blocks)
        after = ul.read(*rel.split("/"))
        ab = ul.user_output_blocks(after)
        a_v = sum(len(ul.violations(b, terms)) for b in ab)
        closes = bool(ab) and [l for l in ab[-1].splitlines() if l.strip()][-1].lstrip().startswith("A seguir:")
        fails += a_v + (0 if closes else 1)
        rows.append((name, b_blocks, b_v, len(ab), a_v, "sim" if closes else "NÃO"))

    print("| skill | blocos antes (heurística) | violações antes | blocos `user-output` depois | violações depois | fecha com «A seguir:» |")
    print("|---|---|---|---|---|---|")
    for r in rows:
        print("| {} | {} | {} | {} | {} | {} |".format(*r))
    tb = sum(r[2] for r in rows if isinstance(r[2], int))
    ta = sum(r[4] for r in rows)
    print("| **total** | | **{}** | | **{}** | |".format(tb, ta))

    # dashboard: static labels before/after
    rel = "library/kernel/tools/dashboard.py"
    before = git_show(a.ref, rel) or ""
    after = ul.read(*rel.split("/"))
    bv = sum(len(ul.violations(l, terms)) for l in ul.dashboard_labels(before))
    av = sum(len(ul.violations(l, terms)) for l in ul.dashboard_labels(after))
    fails += av
    print("\n| dashboard.py | etiquetas lidas | violações |\n|---|---|---|")
    print("| antes ({}) | {} | {} |".format(a.ref, len(ul.dashboard_labels(before)), bv))
    print("| depois | {} | {} |".format(len(ul.dashboard_labels(after)), av))

    # dashboard: the page actually built for the engagement
    tmp = tempfile.mkdtemp(prefix="accept-c-")
    out = os.path.join(tmp, "dash.html")
    rc = subprocess.call([sys.executable, os.path.join(ROOT, rel), "--engagement", a.engagement,
                         "--out", out, "--json", os.path.join(tmp, "m.json"), "--quiet", "--force"], cwd=ROOT)
    if rc == 0 and os.path.exists(out):
        with open(out, encoding="utf-8") as fh:
            labels = html_labels(fh.read())
        hv = [(l, t) for l in labels for _, t, _ in ul.violations(l, terms)]
        fails += len(hv)
        print("| página construída ({}) | {} | {} {} |".format(a.engagement, len(labels), len(hv), hv[:6] if hv else ""))
    else:
        print("| página construída | motor falhou rc={} | — |".format(rc))
        fails += 1

    # COMO-USAR, status opening, resume
    como = ul.read("docs", "COMO-USAR.md")
    body = re.sub(r"```.*?```", "", como, flags=re.S)
    cv = ul.violations(body, terms)
    n_lines = len([l for l in body.splitlines() if l.strip()])
    fails += len(cv) + (0 if n_lines <= 70 else 1)
    print("\nCOMO-USAR.md: {} linhas não vazias (≤ 70), {} violações {}".format(n_lines, len(cv), cv[:5] if cv else ""))
    st = ul.user_output_blocks(ul.read(".claude", "skills", "aisa-status", "SKILL.md"))[0]
    first = [l.strip() for l in st.splitlines() if l.strip()][:3]
    ok3 = (first[0].startswith("Onde estamos:") and first[1].startswith("O que falta para o próximo passo:")
           and first[2].startswith("O que tens de fazer tu:"))
    fails += 0 if ok3 else 1
    print("/status abre com as três linhas: {}".format("sim" if ok3 else "NÃO"))
    resume = ul.read(".claude", "commands", "resume.md")
    okr = "Onde estamos" in resume and "como se diz" in resume.lower()
    fails += 0 if okr else 1
    print("/resume herda a língua e a abertura: {}".format("sim" if okr else "NÃO"))
    print("\nRESULTADO: {}".format("PASSA (0 violações depois)" if fails == 0 else "FALHA ({} problemas)".format(fails)))
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
