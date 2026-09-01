# Diary — operations-lead

> Entradas aprovadas na curadoria do /retro (uma por engagement). Anonimizado: domínio genérico, sem nomes de pessoas/cliente. Detalhe proprietário → _tenant/ (repo privado).
> Formato por entrada: `## <slug-anonimizado> — <data>` + (a) o que apanhei que importou · (b) onde falhei · (c) padrões a rever · (d) conselho ao futuro eu.

<!-- entrada de validação v3.0 (fixture galp-adv-val, drill §6.4.2 do V3_IMPLEMENTATION_PLAN): aprovação de curadoria simulada e anotada; substituir/remover na primeira curadoria real. -->

## aprovacoes-financeiras-midcap — 2026-09-01

**(a)** O que importou foi ler o registo contra a narrativa: o as-is era um passo único por email, com uma folha partilhada a servir de registo e de workflow ao mesmo tempo. Valeu insistir que o pico dimensiona, não a média (R-001: Jun=20 vs Mai=6), e que o aprovador único sem delegação (R-005) tornava o SLA inatingível independentemente da ferramenta — ambos entraram na decisão e no premortem como causa de morte n.º 1.

**(b)** Falhei em deixar morrer as minhas perguntas de excepção. U-004 (o que acontece a um rejeitado) ficou aberta desde R-01 — classifiquei-a Med quando bloqueava o desenho do formulário, e o blueprint congelou com ela pendente. U-009 (porquê 7 pendentes ~95k€ parados há meses) só a formulei em F-01, com os pendentes visíveis no CSV desde R-01; morreu aberta e acabou tripwire que bloqueia a migração. As Unknowns de infra fecharam no próprio dia; as de excepção ninguém respondeu — e eu não as persegui.

**(c)** Padrões a rever: o registo visível é subconjunto do volume real (X-001 — ambos os números verdadeiros); o happy-path responde-se depressa, o caminho de excepção nunca; digitalizar um gargalo dá-lhe apenas um login; a adopção morre primeiro nos pedidos pequenos (C-025: 38% no mês 1).

**(d)** Conselho: trata pós-rejeição, delegação e pendentes órfãos como Critical e design-blocking desde a primeira ronda; agenda o fecho das tuas Unknowns na mesma reunião em que as fáceis fecham.
