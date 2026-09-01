# Diary — business-analyst

> Entradas aprovadas na curadoria do /retro (uma por engagement). Anonimizado: domínio genérico, sem nomes de pessoas/cliente. Detalhe proprietário → _tenant/ (repo privado).
> Formato por entrada: `## <slug-anonimizado> — <data>` + (a) o que apanhei que importou · (b) onde falhei · (c) padrões a rever · (d) conselho ao futuro eu.

<!-- entrada de validação v3.0 (fixture galp-adv-val, drill §6.4.2 do V3_IMPLEMENTATION_PLAN): aprovação de curadoria simulada e anotada; substituir/remover na primeira curadoria real. -->

## aprovacoes-financeiras-midcap — 2026-09-01

Aprovações de adiantamentos a fornecedores em procurement de mid-cap. O que importou: desconfiar do impacto declarado. O driver real era o prazo de auditoria, não a eficiência (A-001 → C-016/C-017 — a única data dura do engagement); e o conflito de volume (X-001) resolveu-se com "ambos verdadeiros": o registo só via >500€, o volume real era 3x — sem isso, âmbito (C-024) e dimensionamento nasciam errados. Ver cedo que a autoridade do sponsor não cobria o deploy (C-001) preparou R-004.

Onde falhei: levantei U-005 (tentativas anteriores), chamei-lhe "arqueologia habitual" e deixei-a morrer aberta — nunca fiz a arqueologia. Ancorei-me na média e no volume; a cauda de 7 pendentes ≈95k€ (C-014) estava no mesmo CSV e foi o chair que a viu, em F-01. Confirmei âmbito total (C-024) sem exigir validação em contexto como condição — o drill C-025 (38% de captura <500€ no mês 1, abaixo do TW-2) mostra a doença original (C-012) a renascer. E não pressionei a revalidação de A-002, deixando o payback órfão (R-003).

Padrões a rever: driver declarado a mascarar compliance com prazo duro; registos truncados por limiar (o volume visível é subconjunto); stakeholders-sombra com veto — co-aprovador financeiro, gate de IT — ausentes do arranque; circuito paralelo de email a sobreviver à digitalização.

Conselho: em R-01 pergunta sempre o que está parado (cauda, não média), quem bloqueia o deploy e o que matou a tentativa anterior — e nunca deixes morrer aberta uma pergunta a que tu próprio chamaste "habitual".
