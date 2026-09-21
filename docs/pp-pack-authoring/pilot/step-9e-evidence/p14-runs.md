# P-14 — entrada em linguagem natural: 5 runs isolados (Sonnet 5, 2026-09-08)

Subagentes `general-purpose` sem `AskUserQuestion`, sem escrita em disco, com acesso ao repo. Cada run leu `CLAUDE.md` (*Duas línguas*, *Entrada sem comando*), `aisa-orient/SKILL.md` e a coluna do glossário. Texto devolvido **verbatim** (só a parte que o utilizador via; a lista «perguntas que faria» fica resumida em §4 do passo). Lint em `accept_p14_runs.py`.

## Teste 1 — mensagem literal de pilot-3, raiz sem engagement

### run 1

```
Não há nenhum projecto (engagement) a decorrer — projects/ está vazio. É arranque do zero.

O que vai acontecer: ouvir quem manda no processo (tu), ler o ficheiro que já existe, fazer perguntas em passagens, chegar a uma frase do problema, comparar alternativas (incluindo não construir nada), escolher, desenhar os ecrãs, entregar os documentos.
Quanto tempo de quem: teu — uma conversa agora, depois respostas curtas por passagem; cada pergunta diz se precisa de reunião ou se um email chega. De quem constrói, nada até à escolha.
O que se espera de ti: dizer como o negócio funciona nas tuas palavras, responder ao que só tu sabes, validar a frase do problema, escolher entre alternativas, aprovar o desenho dos ecrãs.
Os passos, pela ordem: ouvir e perguntar (`/round`) → responder (`/answer`) → ver onde estamos (`/status`) → fixar a frase do problema (`/frame`) → comparar alternativas (`/options`) → ensaiar e testar (`/simulate`, `/premortem`) → escolher (`/decide`) → desenhar os ecrãs (`/blueprint`) → entregar (`/render --all`). Não precisas de decorar nada: o fim de cada resposta diz o que vem a seguir.
O que já ficou dito, sem inventar mais nada: ficheiro de preços que só tu sabes reparar, já corrompeu várias vezes, obrigou-te a mexer nele em férias — dependência de uma pessoa só, risco sério. Precisas de estimar projecções para os dias com poucas cotações conhecidas (2ª e 3ª-feira). E queres alternativa ao ficheiro para o processo de pricing correr mais liso.

Falta a entrevista de enquadramento — como o negócio funciona, dito por ti — antes de propor nome e arrancar. Faz-se normalmente por perguntas de escolha, uma de cada vez. Não tenho essa ferramenta disponível nesta sessão: os temas ficam registados como pergunta em aberto (Unknown), não vou adivinhar respostas.

A seguir: respondes aos temas na lista abaixo → proponho nome do projecto → arranco com `/start`.
```
Perguntas que faria: 10 (7 temas do enquadramento + invariantes + autoridades + orçamento), cada uma com 2-3 opções + *Outro*. Slug: `pricing-cotacoes`.

### run 2

```
O que vai acontecer: ouvir quem manda no processo, ler os ficheiros que já existem, fazer perguntas em passagens, chegar a uma frase do problema, comparar alternativas (incluindo não construir nada), escolher, desenhar os ecrãs, entregar os documentos.
Quanto tempo de quem: do dono do processo, uma conversa agora e depois respostas curtas por passagem — cada pergunta diz se precisa de reunião ou se um email chega; de quem constrói, nada até à escolha.
O que se espera de ti: dizer como o negócio funciona nas tuas palavras, responder ao que só tu sabes, validar a frase do problema, escolher entre alternativas, aprovar o desenho dos ecrãs.
Os passos, pela ordem: ouvir e perguntar (`/round`) → responder (`/answer`) → ver onde estamos (`/status`) → fixar a frase do problema (`/frame`) → comparar alternativas (`/options`) → ensaiar e testar (`/simulate`, `/premortem`) → escolher (`/decide`) → desenhar os ecrãs (`/blueprint`) → entregar (`/render --all`). Não precisas de decorar nada: o fim de cada resposta diz o que vem a seguir.

Já dizes três coisas importantes: um ficheiro que se corrompe e só tu sabes corrigir, tens de estar disponível mesmo de férias para isso, e falta forma de estimar quando ainda há poucas cotações conhecidas (2ª e 3ª feira). Fica registado — não vou inferir mais nada a partir disto.

Nesta sessão não tenho o mecanismo de perguntas estruturadas (uma de cada vez, com opções). Sem ele não avanço a entrevista de enquadramento nem confirmo o arranque — fica em aberto, não assumo respostas.

A seguir: numa sessão com esse mecanismo disponível, respondes à entrevista de enquadramento (um tema de cada vez) e confirmas o nome do projecto → depois corro `/start <slug>`.
```
Perguntas que faria: 9. Slug: `pricing-cotacoes`.

### run 3

```
Percebi o processo: pricing feito num Excel que corrompe às vezes, só tu sabes corrigi-lo (incluindo em férias), há dias da semana (2ª/3ª) com poucas cotações conhecidas para projectar, e queres sair do Excel para outra forma de fazer este processo.

Ainda não há projecto (engagement) aberto para isto. Não vou criar nada sem confirmares.

O que vai acontecer: ouvir quem manda no processo, ler os ficheiros que já existem, fazer perguntas em passagens, chegar a uma frase do problema, comparar alternativas (incluindo não construir nada), escolher, desenhar os ecrãs, entregar os documentos.
Quanto tempo de quem: teu — uma conversa agora e depois respostas curtas por passagem; de quem constrói, nada até à escolha.
O que se espera de ti: dizer como o negócio funciona por palavras tuas, responder ao que só tu sabes, validar a frase do problema, escolher entre alternativas, aprovar o desenho dos ecrãs.
Os passos, pela ordem: ouvir e perguntar (`/round`) → responder (`/answer`) → ver onde estamos (`/status`) → fixar a frase do problema (`/frame`) → comparar alternativas (`/options`) → ensaiar e testar (`/simulate`, `/premortem`) → escolher (`/decide`) → desenhar os ecrãs (`/blueprint`) → entregar (`/render --all`).

A seguir: normalmente vinha aqui uma entrevista de enquadramento (perguntas em passagens, uma de cada vez). Não a posso fazer agora — falta-me aqui a ferramenta de perguntas. Não vou inventar respostas nem assumir factos que não disseste. Fica em aberto (pergunta em aberto — Unknown) até responderes à lista abaixo.

Nome proposto para arrancar: `pricing`. Fica também em aberto até confirmares.
```
Perguntas que faria: 9 (incl. a proposta de arranque como pergunta). Slug: `pricing`. Nota do run: «o que se faz hoje» e «o que o pedido quer mudar» já vieram na mensagem — não entram na lista.

## Teste 2 — «já decidimos, quero a estimativa», só `pricing-marinha-pilot-1` existe

### run 1

```
Onde estamos: a escolha — e o que vem depois: o desenho dos ecrãs e os documentos finais (fase Decision · ronda `D-01`) — projecto `pricing-marinha-pilot-1`, tipo de solução em vista: aplicação deste pacote, record-centric, model-driven, construída de raiz (pack `pp`; escolhida em `D-002`).
O que falta para o próximo passo: aprovar o desenho dos ecrãs actual, versão 06 (a aprovação anterior, `D-004`, cobre a versão 05, não a 06) — 4 pontos a fechar, todos graves.
O que tens de fazer tu: nada agora de decisão — as respostas dependem de IT centralizado, de quem opera a base de dados e de Pedro O.; a aprovação da nova versão é tua assim que essas respostas chegarem.

⚠ Alerta
Resumos por tema anteriores à aprovação do desenho actual (`D-004`) → `/synthesize` antes de `/render`
Documentos finais feitos sobre um desenho antigo (versão 05; a actual é a 06)

O que falta para o próximo passo (resumido)
1. Mecanismo de acesso a dados por domínio material (`U-032`) — quem: IT centralizado / dono da base de dados SQL partilhada / spike de arquitectura — como: `/answer U-032 "..."`
2. Arranjo SQL efectivo — topologia, identidade da ligação, dono do schema (`U-036`) — quem: IT centralizado / equipa que opera a base de dados — como: `/answer U-036 "..." --source "..."`
3. Onde fica a auditoria e o estado de aprovação — nativo da plataforma vs desenhado do lado SQL (`U-040`) — quem: Pedro O. / equipa que opera a base de dados — como: `/answer U-040 "..."`

Para retomar (o que ler para retomar):
  `_state.json`
  `decisions.md` — a escolha (`D-002`) + as aprovações do desenho (`D-003`, `D-004`)
  `_blueprint/ux-blueprint_v06.yaml` — o desenho actual, ainda não aprovado (a aprovada é `_blueprint/ux-blueprint_v05.yaml`, `D-004`)
  `_blueprint/blueprint-log.md` — última entrada
  `options.md` — a alternativa escolhida (`O-004`) e os seus pontos fortes
  `answers.md` — resposta verbatim por pergunta
  `_synthesis/architecture-story.md` — anterior à aprovação `D-004`, por rever
  `shared-understanding.md` — linhas materiais: `X-006`, `U-025`, `U-028`, `U-032`, `U-033`, `U-034`, `U-036`, `U-039`, `U-040`, `R-004`, `R-008`, `R-012`

O que pediste: a estimativa — sai da etapa «os documentos finais» (`/render estimate`); antes disso falta: aprovar o desenho dos ecrãs actual (`/blueprint`, a versão 06 tem 4 escolhas estruturais por fechar) e actualizar os resumos por tema (`/synthesize`, os actuais são anteriores à última aprovação, `D-004`) — a escolha em si já está feita (`D-002`).

A seguir: IT centralizado, quem opera a base de dados e Pedro O. fecham as perguntas estruturais em aberto (`U-032`, `U-036`, `U-040`, `U-039`) → `/answer <id> "..."` → `/blueprint --refresh` → `/synthesize` → `/render estimate`.
```
Classificação: B. Termo sem tradução: nenhum. (Observação: ids em crase dentro e fora de parênteses — o lint apanha os que ficam fora.)

### run 2

```
Onde estamos: a escolha e o que vem depois — a aprovar o desenho dos ecrãs (blueprint v06) (Decision · D-01) — projecto `pricing-marinha`, tipo de solução em vista: plataforma purpose-built (pack pp).
O que falta para o próximo passo: aprovar blueprint v06 — v05 aprovada em D-004 não cobre v06 — 14 pontos a fechar, 8 deles graves.
O que tens de fazer tu: fechar 2 das 4 escolhas estruturais contigo e com quem opera a base de dados (U-040, U-039); as outras 2 (U-032, U-036) pedem resposta de IT centralizado e do dono da base de dados.

⚠ Alerta
Resumos por tema anteriores à aprovação (D-004) → `/synthesize` antes de `/render`
Documentos finais feitos sobre um desenho antigo (versão v05; a actual é v06)

O que falta para o próximo passo
1. Como aceder aos dados de cada área do processo — base de dados SQL vs nativo da plataforma (U-032) — quem: IT centralizado + dono da base de dados + arquitectura — `/answer U-032 "…"`
2. Como está montada hoje a base de dados SQL partilhada (U-036) — quem: IT centralizado / equipa que opera a base de dados — `/answer U-036 "…"`
3. Onde fica o registo de aprovações e auditoria — na plataforma ou do lado da base de dados (U-040) — quem: tu (Pedro O.) / equipa que opera a base de dados — `/answer U-040 "…"`

Para retomar (o que ler para retomar — Decision · arquitectura):
`_state.json` — fase, ronda
`decisions.md` — decisão-solução + aprovações de blueprint
`_blueprint/` — versão actual (+ as versões que referencia)
`_blueprint/blueprint-log.md` — última entrada e revalidações
`options.md` — forças da opção escolhida
`answers.md` — resposta verbatim por id
`_synthesis/architecture-story.md` — portadora da base de autorização
`shared-understanding.md` — linhas materiais: R-001, R-002, R-003, R-004, R-005, R-006, R-007, R-008, R-009, R-010, R-011, R-012, U-025, U-028, U-032, U-033, U-034, U-036, U-040, X-006

Onde estamos: a escolha e o que vem depois — a aprovar o desenho dos ecrãs (Decision · D-01) — projecto `pricing-marinha`.
O que pediste: a estimativa — sai da etapa «os documentos finais» (`/render estimate`); antes disso falta: a escolha já está feita (D-002), mas falta aprovar o desenho dos ecrãs (bloqueado por 4 escolhas estruturais — U-032, U-036, U-040, U-039) e depois actualizar os resumos por tema (`/synthesize`, desactualizados desde a aprovação D-004).
A seguir: fechar as 4 escolhas estruturais — IT centralizado e dono da base de dados para U-032/U-036, tu para U-040/U-039 → `/answer U-032 "…"` (e U-036, U-040, U-039) → `/blueprint --refresh` → `/synthesize` → `/render estimate`.
```
Classificação: B. Termo sem tradução limpa: «escolha estrutural» (structural choice, `blueprint-contract.md` regra 5) — não tem entrada própria no glossário.

## Teste 2 — repetição após correcção dos dois defeitos de template (ids soltos em «Para retomar»; «blueprint vNN»)

### rerun A

```
Onde estamos: a escolha — e o que vem depois: o desenho dos ecrãs e os documentos finais (D-01) — projecto `pricing-marinha`, tipo de solução em vista: plataforma purpose-built, construída de raiz, cobrindo o processo inteiro (pack pp).
O que falta para o próximo passo: aprovar o desenho dos ecrãs, versão 06 — a versão 05 (aprovada em D-004) não cobre a 06 — 26 pontos a fechar, 8 deles graves.
O que tens de fazer tu: responder às escolhas estruturais em aberto — com IT centralizado, o dono da base de dados partilhada, a equipa que a opera, e o Pedro O. — antes de o desenho poder ser aprovado. Resolver a pergunta não fecha a escolha por si só (facto ≠ escolha fechada).

⚠ Alerta
Resumos por tema anteriores à aprovação (D-004) → `/synthesize` antes de `/render`
Documentos finais feitos sobre um desenho antigo (versão 05; a actual é a 06)

O que falta para o próximo passo
1. Mecanismo de acesso a dados por domínio material (U-032) · quem: IT centralizado + dono da base de dados partilhada · `/answer U-032 "…"`
2. Arranjo efectivo da base de dados partilhada (U-036) · quem: IT centralizado + equipa que a opera · `/answer U-036 "…"`
3. Onde fica o estado de aprovação e o trilho de auditoria (U-040) · quem: Pedro O. + equipa que opera a base de dados · `/answer U-040 "…"`

Para retomar:
`_state.json` — etapa, passagem
`decisions.md` — a escolha e as aprovações do desenho dos ecrãs
`_blueprint/` — versão actual do desenho (e as versões que ela cita)
`_blueprint/blueprint-log.md` — última entrada e reconfirmações
`options.md` — pontos fortes da alternativa escolhida
`answers.md` — resposta tal e qual, por pergunta
`_synthesis/architecture-story.md` — o que sustenta a arquitectura aprovada
`shared-understanding.md` — linhas materiais (R-001, R-002, R-003, R-004, R-005, R-006, R-007, R-008, R-009, R-010, R-011, R-012, U-025, U-028, U-032, U-033, U-034, U-036, U-040, X-006)

Onde estamos: a escolha — e o que vem depois: o desenho dos ecrãs e os documentos finais (D-01) — projecto `pricing-marinha`.
O que pediste: os documentos finais com custo e prazo (estimativa) — sai da etapa «os documentos finais» (`/render estimate`); antes disso falta: a escolha já está feita (D-002); o desenho dos ecrãs na versão actual ainda não está aprovado (versão 06 — bloqueado por 4 escolhas estruturais: U-032, U-036, U-039, U-040); e os resumos por tema têm de ser refeitos depois dessa aprovação (`/synthesize`).
A seguir: responder às escolhas estruturais em aberto, com IT centralizado, o dono/equipa da base de dados partilhada e o Pedro O. → `/answer U-032 "…"` (depois U-036, U-039, U-040) → `/blueprint --refresh`.
```
Classificação: B. Nota do run: «purpose-built» mantido tal como em `decisions.md` (descritor de arquitectura registado, não vendor). Contou «26 pontos a fechar, 8 graves» (todos os itens materiais) onde o rerun B contou «4 pontos, 3 graves» (só os que bloqueiam) — ambiguidade do template, corrigida na linha 2 do bloco 1 (`len(milestone.blocking)` · graves · `len(items)`).

### rerun B

```
Onde estamos: a escolha e o que vem depois (Decision · D-01) — projecto `pricing-marinha-pilot-1`, tipo de solução em vista: plataforma construída de raiz, a cobrir o processo inteiro (pack pp).
O que falta para o próximo passo: aprovar o desenho dos ecrãs, versão 06 (blueprint v06) — a versão 05 aprovada (D-004) não cobre esta versão — 4 pontos a fechar, 3 deles graves.
O que tens de fazer tu: responder às perguntas que travam essa aprovação (U-032, U-036, U-040, U-039), com TI central, quem opera a base de dados partilhada e contigo.

⚠ Alerta
Resumos por tema anteriores à aprovação (D-004) → `/synthesize` antes de `/render`
Documentos finais feitos sobre um desenho antigo (versão v05; a actual é v06)

O que falta para o próximo passo
1. mecanismo de acesso a dados por domínio material (U-032) · TI central, dono da BD partilhada, arquitectura · `/answer U-032 "..."`
2. arranjo efectivo da base de dados partilhada — topologia, identidade, dono do esquema (U-036) · TI central, equipa que opera a BD · `/answer U-036 "..."`
3. onde fica o estado de aprovação e o registo de auditoria — no sistema ou na base de dados (U-040) · contigo, equipa que opera a BD · `/answer U-040 "..."`

Para retomar (o que ler para retomar — decision-architecture):
`_state.json` — fase, ronda
`decisions.md` — decisão-solução + aprovações do desenho dos ecrãs
`_blueprint/` — versão actual (+ versões que ela referencia)
`_blueprint/blueprint-log.md` — última entrada e revalidações
`options.md` — forças da alternativa escolhida
`answers.md` — resposta verbatim por id
`_synthesis/architecture-story.md` — portadora da base de autorização
`shared-understanding.md` — linhas materiais (R-001, R-002, R-003, R-004, R-005, R-006, R-007, R-008, R-009, R-010, R-011, R-012, U-025, U-028, U-032, U-033, U-034, U-036, U-040, X-006)

O que pediste: a estimativa — sai da etapa «os documentos finais» (`/render estimate`). Já existe uma versão (v02), mas foi feita sobre um desenho mais antigo (versão 05); a versão actual é a 06 e não está aprovada — falta fechar as 4 perguntas estruturais acima antes de aprovar (blueprint v06). Depois disso, os resumos por tema (`/synthesize`) têm de ser refeitos: são anteriores à última aprovação (D-004).
A seguir: responder às perguntas que travam a aprovação, com TI central, quem opera a base de dados partilhada e contigo → `/answer U-032 "..." /answer U-036 "..." → /blueprint --refresh`.
```
Classificação: B. Nota do run: evitou de propósito citar o vendor que aparece como `owner`/fonte de U-036 no modelo, por não constar em `decisions.md`.
