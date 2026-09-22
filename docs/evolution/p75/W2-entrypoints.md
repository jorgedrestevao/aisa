# W2 — os 14 entrypoints, classificados

> Fonte da lista: `U04_ComandosCompletos` em `.claude/tests/test_projection_ux.py`, que a
> fixa contra o mapa de P1 e falha se algum deixar de existir.
>
> Fonte da classificação: a tabela de comandos do `CLAUDE.md` — documentação do projecto,
> não inferência. Onde o `CLAUDE.md` é explícito, é citado.

## Critério

| classe | quando |
|---|---|
| **obrigatório** | produz efeito persistente no conhecimento do engagement **e** depende do estado actual para estar correcto |
| **condicional** | não escreve conhecimento, mas a resposta é falsa se o estado estiver inconsistente — tem de **declarar** a pendência em vez de mostrar estado velho |
| **não aplicável** | não há estado anterior para reconstruir |

## Classificação

| entrypoint | classe | fundamento |
|---|---|---|
| `start` | **não aplicável** | «New engagement». Cria o estado; não há nada anterior a reconstruir. |
| `orient` | **não aplicável** | `CLAUDE.md` §*Entrada sem comando*: «`aisa-orient` não escreve nada; `aisa-start` escreve.» |
| `resume` | **obrigatório** | «Resume from `_state.json` and name the next command» — reconstruir **é** a sua função. |
| `status` | **obrigatório** | «O que falta para o próximo passo». Sobre estado inconsistente, a resposta é falsa. |
| `answer` | **obrigatório** | «state transition + `answers.md`». |
| `frame` | **obrigatório** | «Transit to Framing phase» — escreve SU e `_state.json`. |
| `options` | **obrigatório** | «Transit to Options phase» — idem. |
| `decide` | **obrigatório** | «Capture decision; auto-runs `/synthesize`». |
| `synthesize` | **obrigatório** | «Produce topic packs» — projecção do estado. |
| `blueprint` | **obrigatório** | «Produce the UX blueprint … iterate to business approval». |
| `render` | **obrigatório** | «Render the deliverables (filtered by decision type)». |
| `premortem` | **obrigatório** | «mitigations → requirements/tripwires» — escreve na SU. |
| `simulate` | **condicional** | «before `/decide`» — consultivo; escreve `_simulation/`, não conhecimento. |
| `revisit` | **condicional** | «recommend keep/adapt/reopen» — consultivo; «never changes the decision». |

**12 obrigatórios · 2 condicionais · 2 não aplicáveis** (14 entradas; `start` e `orient` são
as não aplicáveis, e contam na lista de 14).

### Excepções, justificadas por escrito

`ACCEPTANCE.md` §2 exige que uma excepção tenha precondição realmente ausente e
justificação — não serve para evitar testar o que está implementado.

- **`start`**: a precondição de um bootstrap é um engagement que já existe. Aqui não existe
  — é este comando que o cria. Correr bootstrap antes seria correr sobre um directório
  vazio, e `ABSENT` é o estado esperado, não uma limitação a reportar.
- **`orient`**: não escreve. A regra do projecto é explícita e há uma divisão de trabalho
  declarada com `aisa-start`. Um bootstrap aqui não protegeria nada, porque não há efeito a
  proteger.

Nenhuma das duas dispensa o guarda descrito abaixo: ele actua sobre a **escrita**, e estas
duas não escrevem conhecimento.

## Como se prova — e porque não é editando os 14 ficheiros

A forma óbvia seria acrescentar um passo «corre o bootstrap» a cada `SKILL.md`. Não serve,
por duas razões:

1. **Não é testável.** `ACCEPTANCE.md` §1: «Um teste de estrutura de prompts é insuficiente
   para provar comportamento de runtime.» Um teste só poderia afirmar que o texto existe no
   ficheiro — não que o agente o executou.
2. **Não cobre a exigência.** O próprio W2 pede «testar que nenhum entrypoint contorna o
   bootstrap por uma chamada indirecta». Instruções em prosa não impedem um contorno; só
   pedem que não aconteça.

A imposição tem de ser programática, como já é para `library/` ser read-only. O projecto tem
a infra-estrutura montada:

```
PreToolUse   Write|Edit   pre-write-guard.py      (library/ read-only)
PreToolUse   Skill        phase-gate-check.py · pre-lens-order-check.py
PostToolUse  Write|Edit   on-su-change.py · su-confirmed-guard.py · …
Stop         *            phase-completeness.py
```

Então W2 entrega **um guarda**, não catorze edições: um `PreToolUse` sobre `Write|Edit` que
recusa escrever numa autoridade do engagement enquanto o bootstrap desse engagement não
estiver pronto. A recusa nomeia a limitação e a recuperação.

### O que o guarda cobre, e o que não cobre

Cobre a escrita do **agente** por `Write`/`Edit` — que é exactamente o caminho que hoje
contorna o kernel, já que nenhuma das 24 skills invoca `bootstrap.py`.

**Não cobre escrita por subprocesso.** É limitação conhecida e documentada no próprio
código do projecto (`on-su-change.py`: `PostToolUse` nunca dispara sobre escrita por
subprocesso). Os motores que escrevem por subprocesso — `resolve`, `migrate` — já passam
pelo coordenador, que tem o seu próprio bloqueio por pendência. As duas camadas não se
substituem: o guarda apanha o agente, o coordenador apanha os motores.
