# Diary — cfo-lens

> Entradas aprovadas na curadoria do /retro (uma por engagement). Anonimizado: domínio genérico, sem nomes de pessoas/cliente. Detalhe proprietário → _tenant/ (repo privado).
> Formato por entrada: `## <slug-anonimizado> — <data>` + (a) o que apanhei que importou · (b) onde falhei · (c) padrões a rever · (d) conselho ao futuro eu.

<!-- entrada de validação v3.0 (fixture galp-adv-val, drill §6.4.2 do V3_IMPLEMENTATION_PLAN): aprovação de curadoria simulada e anotada; substituir/remover na primeira curadoria real. -->

## aprovacoes-financeiras-midcap — 2026-09-01

(a) O que importou: mostrar cedo que o conflito de volume (declarado ~47/mês vs registado ~15/mês) fazia o business case variar 3× — elevou o conflito a Critical e revelou o limiar de registo (só >500€ entravam no ficheiro). O envelope orçamental (U-002→C-010) ancorou a decisão e virou tripwire de TCO. E R-003 — payback de 2,4–6 anos se justificado só por eficiência — reposicionou o caso a tempo: a âncora passou a ser o prazo regulatório e o custo do do-nothing, não as horas poupadas.

(b) Onde falhei: A-002 nasceu em R-01 com "validar taxa interna" escrito na própria linha e morreu sem validação — deixei a taxa dentro de uma Assumed em vez de a promover a Unknown com dono e criticidade, e ela acabou âncora do frame e de uma condição de revisão. A causa 5 do premortem é minha: benefício real mas indemonstrável, sem baseline de dia 0, sistema sem dono orçamental no ano 2.

(c) Padrões a rever: registos que só capturam acima de um limiar (volume real 3× o visível); payback de eficiência fraco em processos de aprovação midcap — o valor está no compliance; custo de run órfão na transição build→run.

(d) Conselho: todo o "validar X" numa Assumed vira Unknown nomeado na mesma ronda, com dono. Baseline capturada no dia 0 como requisito. Se a âncora é um prazo regulatório, di-lo e pára de vender payback — mas mede na mesma: o ano 2 precisa de um número.
