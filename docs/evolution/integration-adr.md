# ADR-001 — Linguagem de runtime: Python, stdlib-only

Estado: **aceite** · 2026-09-21 · fase P1

## Contexto

O alvo (aisa) é Python. O doador (`ai-solution-architect`) é Node. O plano manda portar
conceitos do doador — grafo, storage, checks, query, mutations, context, bootstrap,
projection — sem sobrepor o doador ao alvo. Antes de portar qualquer coisa é preciso fixar
em que linguagem o runtime vive, porque a resposta condiciona P2 a P10.

A pergunta foi posta explicitamente: *fazer tudo em Node ou usar Python — o que é melhor
em runtime?*

## Decisão

**Python, stdlib-only, sem excepção.** Node não entra no alvo. O doador contribui com
desenho e testes, não com código nem com toolchain.

## Fundamentação

### 1. O plano já o determina

`README.md:36` do pacote:

> *O alvo mantém Python quando coerente com o kernel. **Não adicionar Node**, serviços, uma
> base de dados, um gestor de tarefas persistente ou um novo comando por cada função interna.*

`CLAUDE_CODE_PROMPT.md:7`:

> *Não introduzas estados concorrentes, filas persistentes, serviços ou **dependências Node
> só porque existem no doador**.*

O doador é Node porque foi escrito em Node. Isso não é argumento de engenharia.

### 2. Medição: Python arranca 2,2× mais depressa, e aqui só há arranques

Node está instalado neste ambiente (v22.22.2), portanto isto é medido, não estimado.

| | mediana de 10 |
|---|---:|
| `python3 -c pass` | **19,0 ms** |
| `node -e ''` | **41,9 ms** |

Num serviço de longa duração a diferença não conta. **Este sistema não tem serviços.** Todo
o runtime é subprocesso por invocação:

- Seis hooks de `PostToolUse` disparam em **cada** `Write|Edit`. Só de arranque:
  6 × 19 ms ≈ **114 ms por escrita**. Em Node seriam ≈ 252 ms.
- Motores por chamada: `coverage.py` carrega em 42,7 ms; `dashboard.py` em 67,3 ms.
- `dashboard.py --json` ponta-a-ponta sobre um engagement real: **334 ms**.

Node tornaria cada escrita do agente ~140 ms mais lenta sem contrapartida nesta carga.

### 3. O custo decisivo é a segunda toolchain, não a velocidade

- `requirements-dev.txt:3` declara o runtime **stdlib-only por desenho**: os motores têm de
  correr num Python 3.11 nu.
- Os nove hooks são invocados pelo harness com `python`, literal, em `.claude/settings.json`.
  Trocar isso é mexer no contrato com o Claude Code, não numa preferência interna.
- 48 ficheiros de teste, 2009 testes, todos Python.
- Node traria `package.json`, `node_modules` e gestão de versões a um repositório cujo
  runtime hoje não instala **nada**.

## O que o doador dá, e que não depende de Node

Inspeccionado, não aceite por descrição. O doador **não tem `package.json`**: é Node stdlib
puro (`node:fs`, `node:path`, `node:os`, `node:url`, `node:child_process`) — a mesma
disciplina de dependência zero que o alvo já tem. Isso torna o porte de conceitos limpo.

Núcleo portável — **2917 linhas** de `.mjs`:

| Módulo | Linhas | O que dá ao alvo |
|---|---:|---|
| `lib/ops/projection.mjs` | 502 | projecção rastreável a partir do grafo |
| `lib/pkg/context.mjs` | 461 | montagem de contexto com orçamento e proveniência |
| `lib/pkg/storage.mjs` | 375 | `.project-knowledge/` com `graph.jsonl` + `meta.json` + `.lock`; serialização determinística (`ordered`, `normalise`, `byTypeThenId`, `byTriple`) |
| `lib/ops/render.mjs` | 302 | render a partir de projecção |
| `lib/pkg/checks.mjs` | 277 | validação de coerência |
| `lib/pkg/schema.mjs` | 234 | esquema versionado, ids estáveis, relações tipadas |
| `lib/pkg/mutations.mjs` | 217 | entradas de mutação |
| `lib/pkg/propose.mjs` | 204 | proposta antes de escrita |
| `lib/ops/documents.mjs` | 188 | documentos |
| `lib/pkg/bootstrap.mjs` | 88 | arranque verificado |
| `lib/pkg/query.mjs` | 69 | consulta |

O modelo de storage — JSONL append + ficheiro de lock + ordenação determinística — mapeia
directamente para a stdlib do Python. Nada nele precisa de Node.

## Consequências

1. P2 implementa o grafo em Python, sobre `pathlib`, `json` e `os.replace`. Sem serviço,
   sem base de dados, sem fila persistente.
2. O que se reutiliza do doador é **desenho e casos de teste**, traduzidos. Não se copia
   `.mjs` para o alvo.
3. As ferramentas existentes reutilizam-se antes de se criar novas: `dashboard.py` já tem
   escrita atómica (`atomic_write`, pid no tmp) e um lock; `coverage.py` já tem `finalize`
   como única escrita.
4. Node continua disponível no ambiente para **ler** o doador. Ler não é depender.

## O problema que mudar de linguagem NÃO resolveria

`dashboard.py` tem 7939 linhas e gasta 334 ms por chamada `--json`. É um monólito, e esse
custo é pago em cada `/status` e em cada hook que o carrega por `runpy`. Quando P2
acrescentar o grafo, cresce.

Isto é dívida de arquitectura, não de linguagem: resolve-se com carga incremental e cache,
e reaparece igual em Node. **Qualquer proposta de adoptar Node por razões de desempenho
está a diagnosticar mal** e deve ser recusada com esta medição.

## Alternativas consideradas

| Alternativa | Porque não |
|---|---|
| Portar tudo para Node, alinhando com o doador | Deita fora 2009 testes e 15 954 linhas de motores que funcionam; quebra o contrato de hooks com o harness; 2,2× mais lento no único padrão que existe aqui |
| Híbrido — grafo em Node, resto em Python | Duas toolchains, dois arranques por operação, fronteira de serialização entre elas, e nenhuma vantagem medida |
| Python com dependências externas para o grafo | Quebra o stdlib-only declarado; o modelo do doador não precisa delas |
