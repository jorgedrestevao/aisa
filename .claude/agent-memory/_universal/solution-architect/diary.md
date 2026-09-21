# Diary — solution-architect

> Entradas aprovadas na curadoria do /retro (uma por engagement). Anonimizado: domínio genérico, sem nomes de pessoas/cliente. Detalhe proprietário → _tenant/ (repo privado).
> Formato por entrada: `## <slug-anonimizado> — <data>` + (a) o que apanhei que importou · (b) onde falhei · (c) padrões a rever · (d) conselho ao futuro eu.

<!-- A entrada de validação v3.0 (fixture galp-adv-val) foi REMOVIDA no Step 7 (cleanup limitado):
     narrava um engagement através de um modelo de decisão que já não existe, e este agente é
     instruído a citar padrões do diário. A própria entrada dizia "substituir/remover na primeira
     curadoria real". As lições genéricas que sobreviveram estão abaixo, re-expressas no modelo
     actual. Sem entradas reais até ao primeiro /retro curado. -->

## Notas gerais — anteriores a qualquer engagement real

Não são entradas de diário: são as duas lições que sobreviveram à limpeza do fixture simulado,
reescritas no modelo em vigor. Substituir por entradas reais assim que o primeiro `/retro` for curado.

- **Prazo sem documento é `Unknown` com dono, não `Assumed`.** Uma data inferida de «ainda este ano»
  não tem base; dar-lhe cara de facto verificado põe uma opção a passar por um requisito temporal que
  ninguém se comprometeu a cumprir. Se a data importa para a decisão, abre-se `Unknown` com dono e
  custo de fecho; se não importa, não entra na avaliação.

- **As incertezas de infra chegam sempre por fechar a Options e fecham-se depressa.** Capacidade da
  equipa de administração, o modelo de ALM e a postura de política de dados costumam faltar à entrada
  e resolvem-se numa conversa com quem opera a plataforma. São input material de S5 e S7 — perguntar
  cedo custa uma reunião, descobrir tarde custa a arquitectura.
