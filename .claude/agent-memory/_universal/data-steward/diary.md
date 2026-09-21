# Diary — data-steward

> Entradas aprovadas na curadoria do /retro (uma por engagement). Anonimizado: domínio genérico, sem nomes de pessoas/cliente. Detalhe proprietário → _tenant/ (repo privado).
> Formato por entrada: `## <slug-anonimizado> — <data>` + (a) o que apanhei que importou · (b) onde falhei · (c) padrões a rever · (d) conselho ao futuro eu.

<!-- entrada de validação v3.0 (fixture galp-adv-val, drill §6.4.2 do V3_IMPLEMENTATION_PLAN): aprovação de curadoria simulada e anotada; substituir/remover na primeira curadoria real. -->

## aprovacoes-financeiras-midcap — 2026-09-01

**(a)** O profiling do registo pagou o engagement: 4 aprovações sem aprovador (C-007) tornaram o finding de auditoria observável nos próprios dados; a distribuição de valores (C-005) antecipou o corte natural de dupla aprovação nos 10k€ antes de alguém o declarar (C-009 confirmou-o exactamente aí); e o campo de tempo-até-decisão preenchido à mão virou requisito «calculado, não digitado». Fornecedores só por código levaram à assumption certa (A-003): referenciar o master, não duplicar.

**(b)** Falhei em três sítios. Perfilei valores mas não a idade dos estados abertos — a cauda de 7 pendentes ≈95k€ (C-014) foi o chair que a viu, e a coluna era minha. Tratei o registo como censo quando era amostra com limiar de captura >500€ (X-001→C-012); nunca perguntei «o que não entra neste ficheiro?». E deixei U-016 (sistema financeiro; conector do master) em Med — morreu aberta e a decisão fechou com A-003 ainda assumption.

**(c)** Padrões a rever: registo-sombra com regra de captura não declarada; gap de compliance visível no próprio dado; campos derivados manuais; pendentes-fantasma a envenenar a migração (TW-4 nasceu daí); circuito paralelo a renascer pós-go-live (C-025: 38% de captura no mês 1).

**(d)** Ao futuro eu: profila idades e caudas, não só distribuições; a primeira pergunta a qualquer registo é a regra de captura; e sobe a Critical qualquer Unknown de system-of-record antes de Options fechar — lineage não se remenda depois da decisão.
