# Diary — compliance-officer

> Entradas aprovadas na curadoria do /retro (uma por engagement). Anonimizado: domínio genérico, sem nomes de pessoas/cliente. Detalhe proprietário → _tenant/ (repo privado).
> Formato por entrada: `## <slug-anonimizado> — <data>` + (a) o que apanhei que importou · (b) onde falhei · (c) padrões a rever · (d) conselho ao futuro eu.

<!-- entrada de validação v3.0 (fixture galp-adv-val, drill §6.4.2 do V3_IMPLEMENTATION_PLAN): aprovação de curadoria simulada e anotada; substituir/remover na primeira curadoria real. -->

## aprovacoes-financeiras-midcap — 2026-09-01

**(a)** O driver real era compliance, não eficiência: o relatório de auditoria exigia trilho por evento e o próprio registo provava o gap (aprovações sem aprovador identificado). Elevei o conflito offline-vs-dados-financeiros para adjudicação do responsável de segurança em vez de o resolver eu; obter o documento da auditoria deu ao caso a sua única data dura e desqualificou duas opções antes do debate. A migração do histórico incompleto virou mitigação obrigatória na decisão.

**(b)** Fui ingénuo. A antítese do business fez-me conceder que sem adopção não há trilho — "o rasto só existe se o fluxo for vivido" — e que o momentum político era da eficiência; eu tratava o trilho como fim em si. O 1.º mês pós-go-live deu-lhe razão: só 38% dos pedidos pequenos entraram pela aplicação. Pior: classifiquei a delegação na ausência do aprovador como Med, e o premortem apontou o aprovador único como causa de morte mais provável — subavaliei a continuidade como tema de governance.

**(c)** Padrões a rever: sponsor cita a auditoria sem lhe chamar driver; gap de auditoria visível nos dados do próprio cliente; pedido de offline a colidir com dados financeiros; aprovador único sem delegação; circuito paralelo de email a renascer pós-go-live.

**(d)** Futuro eu: exige o documento de auditoria na primeira ronda; trata delegação e ausências como Critical; instrumenta a adopção como controlo de governance — o trilho tem de nascer como subproduto do fluxo vivido; um trilho impecável num fluxo morto é um finding adiado.
