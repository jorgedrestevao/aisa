# aisa — Philosophy & Position

**Por que existe esta ferramenta, e o que ela recusa fazer.**

<!-- SCOPE-STATEMENT v1 -->
> O aisa faz discovery de um processo para chegar a uma decisão técnica fundamentada: que tecnologia e que padrão, com que alternativas e a que custo. Não é uma plataforma de discovery de negócio sem destino; uma pergunta só entra quando a resposta pode mudar a decisão.
>
> É nesta direcção que se resolve a tensão entre *discovery de negócio* e *decisão técnica*: um problema de negócio sem consequência técnica visível **não é ignorado** — entra como invariante do enquadramento (`M-n`) ou como requisito do que o alvo tem de garantir, nunca como pergunta pendente do projecto. A organização não saber uma coisa descreve a organização; não é trabalho do projecto.

> Versão: v0.1.0 — DRAFT para revisão da equipa
> Data: 2026-05-27
> Audiência: sponsors, executivos, equipa alargada — qualquer pessoa que precise de perceber **por que** existe aisa sem ler arquitectura técnica.
> Companion docs: [`ARCHITECTURE.md`](ARCHITECTURE.md), [`MIGRATION_FROM_AISA.md`](MIGRATION_FROM_AISA.md), [`ONBOARDING.md`](ONBOARDING.md).

---

## O padrão que vemos vez após vez

Uma área de negócio levanta uma necessidade. "Precisamos de digitalizar este processo." Reunião de 30 minutos. O sponsor articula o pedido com confiança. Há urgência.

O consultor leva o pedido para a equipa. Diz "isto é Power Platform. Tu fazes Canvas, eu faço Power Automate, estimamos 80 dias, levamos a aprovar".

Três meses depois:

- A solução está construída, mas não é usada como esperado.
- Há um stakeholder que ninguém ouviu — IT/Security, Compliance, ou aquela equipa de campo de 12 pessoas que faz o trabalho real — que descobriu a app no UAT e levantou bloqueios que mudaram metade dos requisitos.
- O processo digital herdou as disfuncionalidades do processo manual (que ninguém mapeou bem).
- A direcção pergunta "afinal isto resolveu o problema?". A resposta honesta é "resolveu um problema, mas não tenho a certeza se era o problema certo".

Este padrão repete-se de tal forma que parou de ser uma anomalia. É a norma.

A indústria tem uma narrativa conveniente: a culpa é da execução, falta-nos uma framework, precisamos de mais governance, devíamos ter feito mais sprints de discovery. Mas observados em conjunto, estes projectos partilham um traço comum que não é sobre execução. **Eles começam errado.**

---

## Por que os projectos falham antes de começarem

O fluxo dominante na maioria das organizações é:

```
Necessidade → Selecção de tecnologia → Implementação
```

Aparenta racional. É linear. Permite começar rapidamente.

E está estruturalmente errado.

O fluxo correcto, que poucos seguem, é:

```
Necessidade → Entendimento operacional →
Discovery multi-perspectiva → Alinhamento →
Análise de causa-raiz → Framing da solução →
Selecção de tecnologia → Implementação
```

Os passos intermédios são tipicamente saltados. Saltam-se não por má-fé — saltam-se porque **parecem desnecessários** quando o pedido inicial chega articulado, com sponsor presente, com urgência.

Mas o pedido inicial é quase sempre:
- Filtrado pela pessoa que o levantou (a sua perspectiva específica).
- Influenciado por uma assumpção implícita sobre a solução ("é um app, é um workflow").
- Desfasado da realidade operacional (o pedido vem do gestor; o trabalho real é feito por quem não está na sala).
- Acumulação de duas ou três tentativas anteriores que nunca foram concluídas (e cujo histórico ninguém na sala lembra).

Quando se salta directamente para "tecnologia", **estamos a construir solução para a articulação do pedido**, não para o problema real.

E como a articulação do pedido sobreviveu porque é razoável, a solução também é razoável. Just useless.

---

## O conforto enganador do "já sabemos o que queremos"

A frase mais perigosa que um sponsor pode dizer é "já sabemos o que precisamos, é só implementar".

Tipicamente, o que o sponsor está realmente a dizer é:
- "Já decidimos. Não quero ser questionado."
- "Estamos sob pressão. Não há tempo para refazer este pensamento."
- "Confio na minha leitura. Vamos."

Mas as 3 razões pelas quais o projecto vai falhar estão escondidas no que ele *não* sabe que não sabe:
1. **Stakeholders sombra** — pessoas afectadas pela solução que ele nunca considerou.
2. **Constraints invisíveis** — regras, sistemas legados, políticas internas que vão emergir quando o construir começar.
3. **Contradições internas** — entre o que diferentes stakeholders precisam (e que ninguém ainda mapeou).

A `aisa` existe para criar o espaço protegido em que estes 3 itens emergem **antes** de qualquer linha de código (ou Power FX) ser escrita.

---

## O que muda quando paramos para ouvir

aisa introduz uma pausa estruturada entre "alguém levantou uma necessidade" e "começamos a desenhar a solução". Esta pausa tem duração variável (4-15 dias úteis, dependendo do tamanho do desafio) e tem **um único objectivo**: criar **entendimento partilhado** entre o sponsor, os stakeholders sombra, e quem vai implementar.

Note-se: o objectivo **não é**:
- Validar reasoning de AI.
- Produzir um relatório bonito.
- Recolher requisitos.
- Justificar decisões já tomadas.

O objectivo é literalmente: **toda a gente envolvida no projecto consegue completar a mesma frase da mesma forma**.

> "O problema que estamos a resolver é X, sentido por Y, hoje custa Z, e a evidência é W."

Se ao fim de discovery o sponsor diz uma versão dessa frase e o stakeholder de operações diz outra versão, o projecto **não está pronto** para entrar em selecção de tecnologia. Vai falhar, na fase em que o capital, equipa, e tempo estão a ser comprometidos.

Discovery, neste sentido, **não é** uma fase opcional. É a única coisa que diferencia projectos que entregam valor de projectos que entregam software.

---

## As 7 perspectivas (lenses)

`aisa` analisa cada necessidade através de 7 perspectivas independentes, cada uma fazendo perguntas que a outra não faria. Não é "vamos pensar em tudo" — é "vamos garantir que cada ângulo distinto fala".

| Lens | A pergunta-chave |
|---|---|
| **Business** | "Qual é o impacto disto? Quem o sente? Qual é a urgência real?" |
| **Operations** | "Como é o trabalho hoje? Onde estão as fricções reais? O que sabe quem o faz?" |
| **User** | "Quem o usa? Como se sente? O que falha para eles?" |
| **Data** | "De quem são os dados? Onde estão? Qual a qualidade real?" |
| **Technology** | (só corre tarde, em Options) "Que opções viáveis temos? Quais os trade-offs?" |
| **Governance** | "Que regras se aplicam? Compliance? Auditoria? RBAC?" |
| **Financial** | "Quanto custa não fazer? Quanto custa fazer? Qual o ROI real?" |

Em fases críticas (Framing, Options, Decision), estas 7 perspectivas correm **independentemente** — cada uma vê o problema sem ser contaminada pelas outras. Depois uma síntese central (chairman) integra. Esta arquitectura é deliberada: existe para detectar **divergências genuínas** entre perspectivas, que são onde a maioria dos projectos morre silenciosamente.

---

## Os 5 estados do conhecimento

À medida que o entendimento cresce, cada item de conhecimento é marcado em exactamente 1 de 5 estados:

| Estado | O que significa |
|---|---|
| **Confirmed** | Verificado por evidência directa ou pelo sponsor |
| **Assumed** | Inferência razoável; **declarada como tal** |
| **Unknown** | Lacuna identificada que precisa de resposta |
| **Conflicted** | Stakeholders ou fontes discordam — **tem de ser resolvido** antes de avançar |
| **Risky** | Alta incerteza com impacto material; sabido mas não dimensionado |

Esta visualização — uma página única com 5 secções — é o **artefacto vivo** durante toda a engagement. Qualquer pessoa (sponsor, exec, dev) pode abrir e perceber em 5 minutos: onde estamos, o que sabemos com certeza, o que está em conflito, o que falta.

Não há jargão técnico. Não há schemas. É uma página que tem que ser legível por um director comercial.

---

## As 4 fases da clareza

A engagement progride em 4 fases:

1. **Discovery** — Mapeamos contexto operacional, stakeholders, dados, governance, custo do as-is. **Nenhuma tecnologia é nomeada.**
2. **Framing** — Sintetizamos a "frase única" do problema. Validamos com sponsor + stakeholders sombra. Resolvemos contradições.
3. **Options** — **Pela primeira vez**, geramos opções concretas. Incluindo `não fazer nada`, `mudar o processo sem tecnologia`, e (depois) as opções tecnológicas (Power Platform, OutSystems, custom, etc.).
4. **Decision** — Escolha registada com justificação, alternativas consideradas, riscos aceites, condições de revisão. Output: 6 entregas prontas para handoff a implementação.

Entre as fases há gates *advisory* (sugestões; o sponsor pode overrider com justificação registada). Não há gates rígidos. aisa não bloqueia o trabalho — sinaliza risco.

---

## Por que nos recusamos a nomear tecnologia até à Fase 3

Esta é a decisão mais contra-intuitiva de aisa e a mais importante.

Razão: quando uma tecnologia entra em discussão cedo demais, ela:

1. **Filtra a recolha de informação.** Se a equipa pensa "isto é Power Platform", as perguntas que faz a stakeholders mudam — e mudam para perguntas que a tecnologia já sabe responder. O contexto que NÃO se encaixa fica invisível.
2. **Torna o "não fazer" inaceitável.** Quando há tecnologia na mesa, o status quo deixa de ser opção viável. Mas frequentemente a melhor resposta é "este processo não devia ser digitalizado, devia ser eliminado/simplificado".
3. **Bloqueia opções superiores.** "Excel + Forms + Power Query" pode resolver o problema. Não é sexy, não justifica budget, mas é a resposta certa. Difícil chegar lá se a equipa entrou na sala a pensar Power Platform.
4. **Pré-empta stakeholders críticos.** IT/Security pode ter uma palavra fortíssima a dizer sobre Power Platform Premium licensing que muda completamente a equação — mas se a decisão "é PP" já está implícita, IT vem tarde demais.

A regra `nenhuma lens nomeia vendor/produto antes de Options` não é purismo. É operacional: aumenta a probabilidade de chegar à solução certa em ~40% (estimativa baseada em 18 engagements observados em equipas que adoptaram esta disciplina).

---

## O que aisa **é**

Em uma frase:

> Uma plataforma de **discovery multi-perspectiva** que produz **entendimento partilhado** antes da escolha tecnológica, e emite, no fim, **6 entregas prontas para implementação**.

Em uma analogia:

> aisa é à digitalização o que due diligence é a M&A. Não compra a empresa por ti; **não te deixa comprar a empresa errada**.

---

## O que aisa **não** é

- ❌ Não é um motor determinístico que produz a "decisão correcta" a partir de inputs.
- ❌ Não é um substituto de consultor experiente. É um amplificador: torna 1 consultor mais eficaz em discovery que 3 numa reunião desestruturada.
- ❌ Não é um sistema de governance burocrática. Os gates são advisory; o consultor pode sempre overrider com justificação registada.
- ❌ Não é IA "decisora". É IA **facilitadora**: gera perguntas, sintetiza contexto, detecta inconsistências. As decisões são humanas.
- ❌ Não substitui o raciocínio natural por cognição determinística. O determinismo existe para que o entendimento produzido pelo raciocínio natural se torne **estado durável e epistemicamente honesto** — que sobrevive à compressão, às transições de fase, à mudança de evidência e ao reinício de sessão. Governa *o que* tem de sobreviver, *quem* é a autoridade, *o que* não pode ser promovido ou perdido em silêncio, *o que* tem de ser revalidado e *o que* uma sessão nova recarrega — nunca *como* se pensa: `reason deeply → persist selectively → claim conservatively → rehydrate selectively → revalidate when premises change`.
- ❌ Não é um wrapper de chat sobre Claude. É um pipeline opinated com fases declaradas, perspectivas isoladas, e entregas first-class.
- ❌ **Não é prova de que a solução funciona.** O aisa verifica que um artefacto está bem formado e que carrega o que as fontes pediram; regista que o negócio aprovou uma versão concreta. Nenhuma destas três é a quarta — *funciona ponta-a-ponta?* —, que se prova a construir e a testar, e que este framework nunca declara por ninguém. São quatro perguntas separadas de propósito, cada uma com a sua resposta e a sua linha: a distinção nasceu de um desenho que passou a verificação estrutural com zero problemas e tinha deixado cair um requisito que o registo já carregava (`library/kernel/coverage-contract.md`).

---

## A inversão filosófica em uma tabela

| Approach tradicional (e do aisa) | aisa |
|---|---|
| AI como árbitro da verdade | AI como facilitador de discovery |
| AI como motor determinístico | AI como sintetizador contextual + detector de inconsistências |
| Governance pesada com invariantes | Soft gates + hooks-enforcement nas raras invariantes hard |
| Pipeline determinístico (claim ledger, event ordering, etc.) | Council híbrido com 7 perspectivas independentes |
| Output como 5 deliverables forçados | Shared Understanding vivo + 6 deliverables na transição |
| Foco em "validar reasoning de AI" | Foco em criar entendimento humano partilhado |
| Tecnologia entra no passo 1 | Tecnologia entra no passo 11 (de 13) |

---

## Conclusão

aisa existe porque a indústria continua a vender "implementação rápida" como solução para problemas que são, na sua essência, **problemas de alinhamento e entendimento**. Os problemas de alinhamento e entendimento não se resolvem com mais tecnologia, mais sprints, ou mais governance. Resolvem-se criando o espaço estruturado em que o entendimento partilhado pode emergir.

A maioria das organizações não precisa de:

> "reasoning determinístico"

Precisa de:

> **entendimento partilhado**.

aisa é a infraestrutura para isso.

---

**Para detalhe técnico → [`ARCHITECTURE.md`](ARCHITECTURE.md).**
**Para guia de migração desde aisa → [`MIGRATION_FROM_AISA.md`](MIGRATION_FROM_AISA.md).**
**Para começar a usar → [`ONBOARDING.md`](ONBOARDING.md).**
