# `/status pricing-marinha-pilot-3` — output real, 2026-09-08 (frente C, bloco reestruturado)

> Produzido pela skill `aisa-status` reescrita (P-13), sobre o motor 1.5.0 (`round_delta.novas`). Todos os números são do modelo; nenhum recontado. Material do teste de leitura (§4 do passo 9e).

```
Onde estamos: a ouvir, ler e perguntar (Discovery · R-04) — projecto `pricing-marinha-pilot-3`, tipo de solução em vista: declarado no arranque, não se nomeia antes de comparar alternativas (pack pp).
O que falta para o próximo passo: fechar a etapa de ouvir e perguntar — 10 pontos graves a fechar antes de fixar a frase do problema (9 perguntas e 1 contradição entre fontes), num total de 65 pontos materiais.
O que tens de fazer tu: uma reunião com o Responsável de Pricing Marinha (Pedro O.) e a gestão comercial — 4 perguntas, a primeira é o volume e a margem em risco; em paralelo, a equipa de entrega verifica em meio dia as séries de cotações — isso não depende de ti.

O que falta para o próximo passo
1. As cotações diárias dos cinco instrumentos guardados chegam para reconstruir a média semanal que serve de base de valorização — e há histórico suficiente? (U-085)
   Bloqueia: fechar a etapa de ouvir e perguntar — é a premissa do que já se concluiu sobre o modelo poder ser construído (A-028, C-155) · Afeta: sem ligação registada a decisão, alternativa ou entrega — ainda não existem
   Falta: a própria verificação, feita sobre a extracção já persistida
   Quem: equipa de entrega   (executa a prova: a mesma)
   Fecha quando: muda o caminho — se as séries não reconstroem a média, cai a conclusão de que o modelo é construível — critério formal por definir
   Como: `/answer U-085 "<resultado da verificação>"`
   Fonte: o registo (linha U-085)
2. Quantas toneladas por ciclo são abastecidas a estes preços, e que margem por tonelada está em risco num erro de preço? (U-033)
   Bloqueia: fechar a etapa — é o que transforma o custo de não fazer nada de qualitativo em número · Afeta: sem ligação registada — ainda não existem decisão nem alternativas
   Falta: a resposta — toneladas por ciclo e margem por tonelada
   Quem: Responsável de Pricing Marinha + gestão comercial
   Fecha quando: muda o tamanho — sem este número nenhum retorno é defensável — critério formal por definir
   Como: `/answer U-033 "<toneladas por ciclo, margem por tonelada>"`
   Fonte: o registo (linha U-033)
3. O mesmo interlocutor disse duas coisas incompatíveis sobre o que se perde antes de 4ª feira: em reunião, que se perde o negócio para quem oferece preço firme; hoje, que não se perde venda e o prejuízo é de valorização (X-009)
   Bloqueia: fechar a etapa — a contradição atravessa o custo de não fazer nada e o volume em risco · Afeta: a leitura do negócio, a da operação (C-070, A-021) e a do custo (C-136)
   Falta: uma declaração única do dono sobre o que se perde, e quando
   Quem: por atribuir — o registo nomeia perspectivas e fontes, não uma pessoa
   Fecha quando: critério por definir — sem critério registado
   Como: `/answer X-009 "<declaração final do dono>"`
   Fonte: o registo (linha X-009)
Também importa: a linha `180 HS` está viva comercialmente? — se está, está sem preço produzível há sete meses (U-065); existe glossário ou mapa das colunas da tela, ou só na cabeça do dono? — decide a natureza da reconstrução (U-068); o que contém o módulo VBA de Agosto e de onde veio? — se participa na formação do preço, há uma regra fora de qualquer folha (U-079); por que mecanismo entra a cedência do acordo anual do Supply no processo? — é o primeiro termo do preço (U-080); que autorização existe de facto na base de dados de pricing para os dois perfis? — a capacidade foi registada por declaração, não por prova (U-081); o que acontece quando o carregamento diário falha — alerta ou silêncio? — separa mudar a degradação de mudar o sítio dela (U-082); quantas pessoas na equipa e quantos KAMs recebem a comunicação? — grave no registo, mas não muda nada: 3 ou 6 utilizadores dão o mesmo requisito (U-044).

Agenda da próxima reunião
Muda o caminho: nenhuma das perguntas de reunião — a única que muda o caminho (U-085) é trabalho técnico da equipa de entrega e não gasta reunião.
Muda o tamanho: «Num ciclo típico, quantas toneladas são abastecidas a estes preços — e quanto é a margem por tonelada que um erro de preço põe em risco?» (U-033) → quem: Responsável de Pricing Marinha + gestão comercial → ver «o que falta» 2
Muda o tamanho: «Quem recebe o preço precisa de ver como ele foi composto — cotação, prémio, piso, custo logístico, margem — ou basta o número?» (U-039) → quem: Responsável de Pricing Marinha + destinatários do preço
Muda o tamanho: «Quando se reemite um preço no mesmo dia, o que acontece ao preço já comunicado e às consultas já respondidas?» (U-055) → quem: Responsável de Pricing Marinha + destinatários do preço
Muda o tamanho: «Se a solução assenta na base de dados de pricing e reutiliza a aplicação que já existe, quem governa essa base e essa aplicação — e aceita?» (U-061) → quem: Governance / IT + dono da plataforma
Teach-back do processo [reunião] — «é assim que entendemos que funciona: o preço compõe-se cedência → base → venda → mínimo; a cedência vem do acordo anual do Supply; um módulo de código de Agosto, de autor desconhecido, participa ou não no preço; a linha `180 HS` emite erro há sete meses — o que está errado ou em falta?» — cobre quatro perguntas (U-080, U-079, U-065, U-068); cada uma fecha por si via `/answer`
Por outro canal — trabalho técnico: as séries de cotações reconstroem a média? (U-085) · conteúdo e origem do módulo VBA (U-079). Documento: mecanismo de entrada da cedência (U-080) · autorização real na base de dados de pricing (U-081) · comportamento quando o carregamento falha (U-082) · famílias de cliente e produtos vivos vs legado (U-019). Email: a linha `180 HS` está viva? (U-065) · glossário das colunas (U-068) · quem aprova a entrada em produção e a reversão (U-029) · a referência de concorrência decide ou só informa? (U-036) · a janela de 5 dias termina 3 dias antes — regra ou artefacto? (U-037) · o extracto que nenhuma fórmula lê é resíduo ou consulta manual? (U-040) · os ratios de blend são estáveis ou mudam por ciclo? (U-042) · o apuramento de swap (U-050) · quem recebe os preços de biocombustível por porto e a tabela logística (U-052) · o ficheiro das 9:09 de Espanha é entrada ou saída? (U-054) · dono e regra dos prémios e SLIs (U-058) · o «+3» é constante, parâmetro ou tabela? (U-059) · a família `HS B10` está em âmbito? (U-064) · sobre que variáveis simula o comercial (U-083) · política de saída de dados para serviços externos (U-084)
Não gastes reunião nisto: número de pessoas na equipa e de KAMs (U-044) · a que consequência datada ancora a urgência (U-006) · quanto dura um dia de pricing e quando é o pico (U-010) · o que aconteceu nas corrupções do ficheiro (U-011) · taxa carregada e centro de custo (U-030) · quanto se paga hoje pelo feed e pelo add-in (U-032) · ordem correcta de recálculo (U-038) · a janela fixa de 12 linhas (U-043) · substituições manuais com a protecção levantada? (U-063) · folhas protegidas na cópia em vigor? (U-070) · limiar de subida de aprovação (U-072) · limitação do sistema de propostas registada junto do dono? (U-078) · idioma e acessibilidade (U-017) · imputação a centro de custo (U-034)
Banco de perguntas do tipo de solução consultado: nenhum gatilho de aprofundamento observado no registo para estas quatro; as perguntas vêm das próprias linhas.

Desde a última passagem (R-04)
22 perguntas novas · 33 fechadas · 39 em aberto no total (9 graves) — fechámos mais do que abrimos
Factos novos nesta passagem: 62 verificados · 29 assumidos · 2 contradições entre fontes · 14 riscos

Confiança no que sabemos
verificado 139 (+22 já resolvidos) · assumido 51 (+1 resolvido) · em aberto 39 (9 graves, +46 resolvidas) · em conflito 1 (1 grave, +8 resolvidas) · riscos 25 (+9 resolvidos)
Em prazo: 100% — 0 factos por reconfirmar (Saúde epistémica) — mede a validade da prova, não a prontidão
Factos sem prova localizável: 0 de 139 — uma excepção aceite, o pedido literal; o motor verifica que a âncora existe, não que a afirmação fica dentro da prova
Riscos registados: 25 (R-001 a R-004, R-006 a R-014, R-016, R-018, R-021, R-023, R-024, R-026, R-027, R-029, R-031 a R-034) — com mitigação proposta; não são pendências
Perguntas de orçamento que não deviam estar abertas — a decisão de avançar não depende de aprovação de terceiros (funding_gate = false): 4 (U-072, U-030, U-033, U-034); a terceira é volume e margem, apanhada pela palavra «ROI» no texto
Perguntas que ainda não dizem o que muda com a resposta: 21 de 39 (lista no motor) — o árbitro só verifica a presença da declaração e reclassifica-as na próxima passagem (P-1)
Como o negócio funciona, dito pelo dono: 5 regras declaradas (M-1 a M-5), registadas no arranque (R-00)
Leitura incompleta: nenhuma

A seguir: reunião com Pedro O. (Responsável de Pricing Marinha) e a gestão comercial — as 4 perguntas de reunião e o teach-back do processo → `/answer U-033 "<toneladas por ciclo e margem por tonelada em risco>"` e `/answer X-009 "<o que se perde antes de 4ª feira, em definitivo>"`; em paralelo, a equipa de entrega verifica as séries → `/answer U-085 "<resultado>"`. Depois, outra passagem para o árbitro fechar as 21 perguntas sem declaração → `/round`, antes de `/frame`.
```
