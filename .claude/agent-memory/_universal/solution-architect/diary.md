# Diary — solution-architect

> Entradas aprovadas na curadoria do /retro (uma por engagement). Anonimizado: domínio genérico, sem nomes de pessoas/cliente. Detalhe proprietário → _tenant/ (repo privado).
> Formato por entrada: `## <slug-anonimizado> — <data>` + (a) o que apanhei que importou · (b) onde falhei · (c) padrões a rever · (d) conselho ao futuro eu.

<!-- entrada de validação v3.0 (fixture galp-adv-val, drill §6.4.2 do V3_IMPLEMENTATION_PLAN): aprovação de curadoria simulada e anotada; substituir/remover na primeira curadoria real. -->

## aprovacoes-financeiras-midcap — 2026-09-01

**(a)** A árvore aplicada regra a regra pagou-se: sharepoint-first caiu no gate R0 (trilho auditável regulatório, C-017→C-019) antes de qualquer debate de UX, e dataverse-first (model-driven + Power Automate Approvals) venceu R0–R6 com licenciamento a 2–6% do envelope. O protocolo de missing-inputs disparou como devia: capability, ALM e DLP em falta viraram A-004 + U-012/U-013/U-014 Critical; o /simulate mostrou que os dois verdictos "risky" flipavam o ranking e uma reunião com IT fechou os três (C-020..C-022) antes do /decide. Levantei X-004 (reversibilidade baixa vs mobilidade) e a mitigação — O-002 non-tech como fase 0 — entrou na decisão.

**(b)** Fui ingénuo com o tempo: A-005 — 16 semanas inferidas de «ainda este ano», sem data escrita nem compromisso — sustentou sozinha o «✓ Prazo Q2 2027» da opção líder na tabela comparativa. O premortem fê-la causa de morte n.º 3 e foi preciso um tripwire (TW-5) para a conter. A-004 também nasceu sem SU id, mas essa o protocolo cobre e declarei-a como assumption; ao prazo dei-lhe cara de facto verificado.

**(c)** Padrões a rever: infra Unknowns (capability/ALM/DLP) sempre ausentes à entrada de Options e resolúveis numa hora com IT; trilho auditável a matar sharepoint-first no R0 em domínios financeiros; aprovador único a sobreviver intacto dentro da ferramenta nova.

**(d)** Futuro eu: prazo sem documento é Unknown com dono, não Assumption — e qualquer verdicto de prazo na comparação fica marcado como condicional.
