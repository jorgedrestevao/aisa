# aisa — Framework de Discovery Digital (visão de negócio)

## O que é

<!-- SCOPE-STATEMENT v1 -->
O aisa faz discovery de um processo para chegar a uma decisão técnica fundamentada: que tecnologia e que padrão, com que alternativas e a que custo. Não é uma plataforma de discovery de negócio sem destino; uma pergunta só entra quando a resposta pode mudar a decisão.

Estrutura a fase de descoberta de projetos de digitalização (Power Platform, OutSystems, Mendix, custom) **antes** de escolher tecnologia. Objetivo: decisão informada, não implementação apressada.

Princípio central: **primeiro entender o problema a fundo, só depois falar de solução.**

## Porquê existe

Problema clássico: equipas saltam para "vamos fazer em Power Apps" no dia 1, sem mapear processo real, donos de dados, riscos de compliance, custo do "não fazer nada". Resultado: retrabalho, requisitos a mudar a meio, soluções que não servem o negócio.

aisa força sequência: **Descoberta → Enquadramento → Opções → Decisão → Especificação**.

## Pipeline end-to-end

```
1. START      → abre projeto, regista pedido original
2. CAPTURE    → extrai evidência de ficheiros (Excel, docs, PDFs, transcrições)
3. DISCOVERY  → 6 lentes de negócio exploram o problema (rondas)
4. FRAMING    → conselho sintetiza numa frase-problema única
5. OPTIONS    → conselho gera 3-5 opções (tecnologia entra só aqui)
6. SIMULATE   → projeta cada opção (esforço, riscos, ecrãs) antes de decidir
7. PREMORTEM  → escreve o "obituário" do projeto — porque falharia
8. DECIDE     → escolha final, com justificação e riscos aceites
9. SYNTHESIZE → consolida em 5 pacotes temáticos
10. BLUEPRINT → arquitetura de ecrãs (UX)
11. RENDER    → gera os 6 entregáveis finais
```

## As 6 lentes de Descoberta

Cada lente olha o mesmo problema de um ângulo diferente. Nenhuma pode nomear tecnologia.

| Lente | Pergunta central |
|---|---|
| **Negócio** | Impacto, urgência, prioridade estratégica, KPIs |
| **Operações** | Como o processo funciona hoje, de facto (não o "devia") |
| **Utilizador** | Quem usa, como, onde dói |
| **Dados** | Quem é dono, qualidade, sensibilidade, onde vive |
| **Governança** | Compliance, acessos, auditoria |
| **Financeiro** | Custo atual, custo de não fazer nada, orçamento, ROI |

Lente de **Tecnologia** só entra na fase Options — é a única que pode nomear Power Platform / OutSystems / Mendix / etc.

## Estados do conhecimento (5, só 5)

Cada facto capturado tem um estado:

- **Confirmado** — validado, tem data de validade (expira)
- **Assumido** — hipótese de trabalho, também expira
- **Desconhecido** — pergunta em aberto
- **Conflituoso** — versões contraditórias das lentes
- **Arriscado** — sabido, mas perigoso

Conhecimento **expira**. Perguntas têm **preço** (custo de descobrir vs. valor da resposta). Decisões guardam o **contrafactual** (o que teria acontecido se escolhesse a outra opção) — permite rever mais tarde sem reabrir tudo.

## O artefacto vivo: Shared Understanding

Documento único, fonte da verdade durante todo o projeto. Todas as lentes escrevem lá. Nunca se apaga uma linha — transições criam nova linha referenciando a anterior.

Dashboard HTML gerado a partir dele — nunca editado à mão.

## Dois modos de conselho

- **Discovery**: lentes correm sequencialmente, inline, numa conversa.
- **Framing/Options**: lentes correm em paralelo (subagentes), depois um "chairman" sintetiza — evita groupthink, cada persona pensa isolada.

## Os 6 entregáveis finais

Só gerados **depois** da Decisão (nunca antes — regra dura):

1. Especificação de implementação
2. Estimativa de esforço
3. Blueprint UX (arquitetura de ecrãs)
4. Pacotes de síntese por tópico
5. Registo de decisão (com riscos aceites e condições de revisão)
6. Dashboard consolidado

## Regras duras (não negociáveis)

- Nunca inventar dados/IDs — desconhecido fica desconhecido.
- Nunca nomear tecnologia antes de Options.
- Nunca gerar entregáveis antes de Decide.
- `library/` (motor do sistema) é só leitura em runtime.
- Shared Understanding é sempre a verdade — se outro ficheiro discordar, SU ganha.

## Valor para o negócio

- Decisão de tecnologia informada por evidência, não por moda.
- Risco e custo de não-fazer-nada tornados explícitos antes de comprometer orçamento.
- Rastreabilidade total: cada linha do blueprint final aponta para a evidência que a originou.
- Revisão de decisão barata: contrafactual congelado permite comparar sem refazer discovery.
