# P3 — Bootstrap técnico universal

Estado: **GO** — técnico. Não se afirma que toda a experiência já preserva conhecimento
(o plano proíbe-o expressamente nesta fase).

## Identidade e precondições

- **Data/ambiente:** 2026-09-22 · Linux 6.18.44-fc-v37 · Python 3.11.15
- **GO anterior:** P2 **GO** técnico — `docs/evolution/P2-report.md`, 16/16 casos K e W.
- **Estado à entrada:** 50 ficheiros / 2067 testes, verde.
- **Contrato:** `WRITES_AND_RECOVERY.md` §B5 (bootstrap e contexto), §B6 (orçamento).
- **Casos:** B01–B07 — 7 dos 61.

## Nota pré-alteração

- **Problema:** P2 deu atomicidade e recuperação, mas nada obriga um ponto de entrada a
  **ler** antes de agir. Sem isso, um comando pode operar sobre estado pendente ou sobre um
  grafo corrompido e nem saber.
- **Hipótese verificável:** a ordem do B5 pode ser imposta por uma função read-only, e a sua
  natureza read-only pode ser **provada**, não afirmada.
- **Autoridades afectadas:** nenhuma. Continua sem escritor de negócio ligado.
- **Risco:** um bootstrap que reparasse tornaria «estava bem» indistinguível de «foi
  consertado». Daí a prova de read-only ser o teste central.
- **Reversão:** dois ficheiros novos. Remover reverte P3 por inteiro.

## Alterações realizadas

| Ficheiro | Linhas | Papel |
|---|---:|---|
| `library/kernel/tools/bootstrap.py` | 250 | a leitura que precede qualquer efeito |
| `.claude/tests/test_bootstrap.py` | — | B01–B07, 34 testes em 7 classes |

Zero ficheiros existentes alterados. Zero testes existentes alterados, saltados ou desactivados.

### A ordem, e onde pára

    1. identificar engagement
    2. detectar pendência        <- PÁRA AQUI se houver
    3. snapshot das autoridades
    4. validar grafo             <- PÁRA AQUI se corrupto ou com integridade quebrada
    5. construir contexto
    6. devolver revisão, digests e limitações

Onde pára é tão contratual como o que faz. Pendência no passo 2 fecha tudo a jusante:
`ready` é falso, `context` fica vazio, e o chamador não tem por onde avançar um gate.

**A recuperação nunca é efeito lateral de ler.** Há um teste que o afirma: encontrar
pendência e o marcador continuar lá depois do bootstrap.

## Verificação

| Runner | Collected | Passed | Failed | Skipped | Xfail | Errors |
|---|---:|---:|---:|---:|---:|---:|
| `python3 <ficheiro>` × 51 | **2101** | 2084 | **0** | 14 | 3 | **0** |

2067 → 2101 = +34, exactamente os testes novos. Zero regressões.

Contagem por classe conferida contra o ficheiro antes de correr: 5+3+4+6+6+5+5 = 34, e
**nenhuma classe depois do bloco `main`** — a verificação que o P2 ensinou a fazer.

### Casos → evidência

| Caso | Afirma |
|---|---|
| B01 | bootstrap precede efeitos; projecto e revisão observáveis mesmo sem `/start`; pendência pára no passo 2; recuperação não é efeito lateral |
| B02 | subprocesso vê o **mesmo** snapshot; mutação por shell move-o para todos; pendência criada por subprocesso bloqueia o leitor do pai |
| B03 | troca detectada; contextos não se contaminam; voltar a A dá A inalterado |
| B04 | **hash da árvore inteira** (caminhos + bytes + `mtime_ns`) igual antes e depois; não cria `_graph/`; modo legacy declarado e não apresentado como migrado |
| B05 | críticos primeiro; truncagem explícita com críticos nomeados; **excerto nunca abre gate** |
| B06 | dependência em falta e dependência fora do orçamento são assinaladas **em separado**; conclusão limitada em ambas; proveniência viaja com o item |
| B07 | deriva localizada arranca com aviso; corrupção não arranca e **não** é modo legacy; um teste afirma que os dois não colapsam |

### Duas provas que carregam a fase

**B04 é provado, não afirmado.** O teste hasheia a árvore completa — caminhos, bytes e
`mtime_ns` — antes e depois de dois bootstraps. Qualquer escrita, qualquer toque num
timestamp, faz falhar. Não falha.

**B02 é o que torna isto mais do que um helper.** Os testes lançam subprocesso real: um
muta por shell e o snapshot do pai move-se; outro escreve pendência e o leitor do pai
bloqueia. É exactamente o ponto cego que `on-su-change.py:38-40` documenta — `PostToolUse`
nunca dispara sobre escrita de subprocesso. Uma barreira dependente dos hooks `Write|Edit`
não seguraria. **Esta não depende deles.**

## Resultado e limitações

### GO/NO-GO por critério

| Critério de saída (P3) | Veredicto | Evidência |
|---|---|---|
| Bootstrap corre antes dos efeitos, em qualquer entrada | **Cumprido** | B01, incluindo chamada sem `/start` |
| Não repara nem inicializa em silêncio | **Cumprido** | B04, por hash da árvore |
| Cobre subprocessos e leitores directos | **Cumprido** | B02, com subprocessos reais |
| Troca de projecto invalida contexto | **Cumprido** | B03 |
| Orçamento, proveniência, parcialidade | **Cumprido** | B05, B06 |
| Fallback legacy preservado; corrupção não o autoriza | **Cumprido** | B04 + B07 |
| Casos B01–B07 | **Cumprido** | 7/7 |
| Regressão de skills/hooks e suite completa | **Cumprido** | 51/51, 2101 testes |

**GO técnico.**

### Limitações, declaradas

1. **Não lê a Shared Understanding.** O contexto vem do grafo, que ainda não tem
   conhecimento real. O **mecanismo** — orçamento, proveniência, premissas — está testado
   por si; falta-lhe a fonte, não a lógica. Ligar as autoridades é P4/P6.
2. **Nenhum ponto de entrada real o chama ainda.** As 24 skills e os 9 hooks continuam sem
   passar por aqui. B01 prova que o bootstrap *funciona* chamado directamente; não prova que
   *toda a experiência* o chama. Essa é a diferença entre este GO técnico e P7.
3. **`items_from_graph()` é provisório.** Deriva criticidade do estado do nó
   (`Unknown`/`Conflicted`/`Risky` → crítico). É a regra que `states.md` sugere, mas não foi
   confrontada com a SU real.
4. **Um só sistema operativo.** Linux.

### Métricas

| | antes de P3 | depois |
|---|---:|---:|
| Motores | 7 · 16 759 linhas | 8 · 17 009 |
| Ficheiros de teste | 50 | 51 |
| Testes | 2067 | 2101 |
| Casos do plano cobertos | 16/61 | **23/61** |
| Dependências de runtime | stdlib | stdlib |

### Próxima acção concreta

**P4 — primeira operação completa de negócio** (casos L01–L05). É a fase que liga o que P2 e
P3 construíram a Capture/Discovery, ao registo na SU e ao `/answer`, e que tem de provar a
sequência entre sessões: capturar → persistir → responder → transitar → verificar Coverage →
**terminar a sessão** → nova sessão sem histórico → mesmo estado, proveniência e próxima acção.

P4 é também onde as limitações 1 e 2 acima deixam de ser aceitáveis.
