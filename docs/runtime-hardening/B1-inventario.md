# B1 · Inventário antes de editar — fase 2 (bloco B)

> Corrido em 2026-09-11, working tree `337714c`, antes de qualquer edição de B2/B3.
> Método: grep por forma normalizada, **nas duas línguas**, dos sete temas de intake, em
> `.claude/`, `library/`, `docs/`, `CLAUDE.md`, `README.md`, mais `.claude/agent-memory/_universal/*/`.
> A lista de ficheiros do plano é pista, não inventário (`feedback-plan-inventories-are-incomplete`).

## Formas procuradas

`o que é vendido` · `o que se vende` · `what is sold` · `quando o preço` · `when the price` ·
`determina o custo` · `determines the cost` · `valoriza` · `valuation` · `incerteza` ·
`uncertainty comes`

## Canais que impunham os temas de pricing — **editados**

| canal | ficheiro | o que lá estava | o que ficou |
|---|---|---|---|
| skill | `.claude/skills/aisa-start/SKILL.md` (4d) | 7 bullets, **5 de pricing**, perguntados a todos | T1–T7 genéricos + `d1` com a pergunta de activação e os cinco `P1..P5` só quando `Sim` |
| skill | `.claude/skills/aisa-orient/SKILL.md` (passo 3) | a mesma lista em prosa | a mesma tabela T1–T7 + activação; declara que `aisa-start` não repete |
| kernel | `library/kernel/phases.md` | **nada** — o intake não estava no kernel | secção *Enquadramento (P-0)*, com os sete temas e o conjunto condicional |
| kernel | `library/kernel/glossary.md` | sem linha para os temas | 8 linhas: os 7 ids + `INTAKE-SET` |
| pack | `library/packs/{pp,generic,outsystems,mendix}/pack.yaml` | sem chave | `enquadramento.extra_themes: []` nos quatro |
| doc de utilizador | `docs/COMO-USAR.md:21` | «o que se vende, quando se fixa o preço, o que determina…» | os sete temas em linguagem de negócio; pricing descrito como condicional |
| plano histórico | `docs/CONSOLIDATED_PLAN.md` | P-0 com os cinco temas como universais | **errata** no topo; o documento fica como registo |

## Ocorrências que **não** são o intake — falsos positivos, com a razão

Todas verificadas linha a linha. Nenhuma foi editada.

| ficheiro | termo | por que não é o intake |
|---|---|---|
| `.claude/hooks/phase-gate-check.py` | `evaluation` | é a avaliação do portão de fase (`the most recent evaluation of this transition`), não valorização de negócio |
| `.claude/skills/aisa-decide/SKILL.md` | `evaluation` | `candidate evaluation` na nota de serialização das opções |
| `.claude/skills/chairman-synthesis/SKILL.md` | `pricing` | um **exemplo** de restrição estrutural («pricing data must remain in the system of record»), não uma pergunta |
| `library/kernel/synthesis-templates/architecture-story.template.md` | `evaluation` | `reproducible evaluation` da base de architectabilidade |
| `.claude/agent-memory/_universal/solution-architect/universal-constraints.md` | `evaluation` | `ordered evaluation procedure` do decision-tree |
| `.claude/agent-memory/_universal/solution-architect/diary.md` | `incerteza` | nota de diário sobre incerteza de estimativa |
| `library/packs/pp/deliverable-templates/{estimate,executive-report}.template.md` | `incerteza` | banda de incerteza da estimativa |
| `.claude/tests/test_admission_rule.py`, `test_step8c_semantic_continuity.py` | `valoriza`, `valuation` | fixtures do domínio de pricing-marinha, não o banco de perguntas |
| `docs/ARCHITECTURE.md`, `docs/DISCOVERY_CRITICAL_REVIEW.md`, `docs/MVP_IMPLEMENTATION_PLAN.md` | `incerteza` | prosa sobre incerteza epistémica |
| `docs/ADVERSARIAL_REVIEW_2026-09-08.md`, `docs/EXTERNAL_REVIEW_2026-09-10.md`, `docs/TECHNICAL_DECISION_REFOCUS_IMPLEMENTATION_PLAN.md`, `docs/RUNTIME_HARDENING_IMPLEMENTATION_PLAN.md` | vários | **registos de revisão**: citam o defeito para o descrever. Reescrevê-los apagaria a história do achado |

## Exclusões históricas respeitadas

`docs/pp-pack-authoring/**` e `**/archive/**` não foram varridos para edição, conforme o
plano: são relatórios de autoria e de piloto. Onde um documento histórico **prescreve**
runtime — só `docs/CONSOLIDATED_PLAN.md` — recebeu errata em vez de reescrita.

## Leitura dos enquadramentos antigos

Preservada e testada. `projects/pricing-marinha-pilot-3/enquadramento.md` não tem secções
`Tn` e continua a ser lido tal como está. **A presença das secções é o que distingue as duas
formas** — a geração nunca se infere pela data nem pela versão do engagement.
