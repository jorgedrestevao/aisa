# Como usar o aisa

> Para quem tem um processo a melhorar e não construiu esta ferramenta. Uma página. Quem instala ou desenvolve lê `ONBOARDING.md`.

## O que é

<!-- SCOPE-STATEMENT v1 -->
O aisa parte de um processo e leva-te a uma escolha técnica fundamentada: que tecnologia e que padrão, contra que alternativas e a que custo. Não serve para explorar o negócio sem destino — uma pergunta só entra quando a resposta pode mudar a escolha.

Uma forma de perceber um processo antes de decidir o que construir. Ouve quem manda no processo, lê os ficheiros que já existem, faz perguntas em passagens, chega a uma frase do problema, compara alternativas — incluindo não construir nada — e só depois escolhe, desenha os ecrãs e entrega documentos.

Nenhuma tecnologia é nomeada antes da etapa das alternativas. Primeiro o problema, depois a solução.

## O que dá

- Um registo do que sabemos, com o grau de certeza de cada linha: verificado (e onde), assumido (e porquê), pergunta em aberto, duas fontes que se contradizem, risco.
- A frase do problema, acordada contigo.
- Alternativas comparadas, uma escolha registada com as razões e as condições que a obrigam a rever.
- O desenho dos ecrãs, iterado até o negócio aprovar.
- Seis documentos finais para quem vai construir.

## O que se espera de mim

1. Dizer como o negócio funciona, nas tuas palavras, antes da primeira passagem — quem intervém, o que faz isto começar, o que se faz, o que sai no fim, as regras que ninguém pode quebrar, o que corre mal hoje e o que o pedido quer mudar. Se a saída do teu processo for um preço, uma cotação ou uma valorização, é-te perguntado, e só então vêm as perguntas sobre preço e custo. O que determina o custo, de onde vem a incerteza.
2. Responder a perguntas. Cada uma diz quem responde, o que custa responder (email, documento, reunião, trabalho técnico) e o que muda com a resposta — as que não mudam nada não gastam reunião.
3. Validar a frase do problema, escolher entre alternativas, aprovar o desenho dos ecrãs. Ninguém decide por ti.

## Como começo

Descreve o processo e o que te incomoda. Sem comandos. Exemplo: *«Precisamos de ajuda a melhorar o processo de pricing; o Excel corrompe-se e só eu sei pô-lo a funcionar.»*

A resposta explica o que vai acontecer, faz-te as perguntas de enquadramento e propõe o arranque. Confirmas, e começa.

## Como sei o que fazer a seguir

O fim de cada resposta diz **A seguir:** — o passo humano, se houver, e o comando exacto. Não precisas de decorar comandos.

Quando voltas noutro dia: escreve o que queres («quero a estimativa») ou `/resume`. Ficas a saber onde estás, o que falta e o que tens de fazer tu.

## Os passos, pela ordem

| Etapa | O que acontece | Comando |
|---|---|---|
| Ouvir, ler e perguntar | as perspectivas (negócio, operações, utilizador, dados, controlo, custo) passam pelo material e levantam perguntas | `/round` |
| Responder | cada resposta tua entra no registo | `/answer` |
| Ver onde estamos | o que falta, quem tem de fazer o quê, a agenda da próxima reunião | `/status` |
| Fixar a frase do problema | as perspectivas em paralelo; tu validas | `/frame` |
| Comparar alternativas | 3 a 5, incluindo não construir; entra a perspectiva tecnológica | `/options` |
| Ensaiar e testar | ensaiar cada alternativa; escrever o obituário do projecto antes de decidir | `/simulate` · `/premortem` |
| Escolher | tu escolhes; razões, alternativas rejeitadas e condições de revisão ficam registadas | `/decide` |
| Desenhar os ecrãs | iterado com o negócio até aprovar | `/blueprint` |
| Entregar | os documentos finais | `/render --all` |

## Uma palavra sobre certeza

Um facto verificado tem prazo. Passado o prazo, pede-se para reconfirmar — não quer dizer que esteja errado. Uma pergunta em aberto só vale se a resposta mudar algo no que vamos construir; se não muda, dizemos isso e não gastamos reunião com ela.

## Quatro perguntas que não se confundem

Quando o desenho dos ecrãs ou os documentos ficam prontos, há quatro perguntas diferentes, e responder a uma **não** responde às outras:

| A pergunta | O que significa responder «sim» |
|---|---|
| Está bem feito? | o ficheiro está bem construído — nada em falta, nada mal formado |
| Carrega o que pedimos? | tudo o que disseste que era preciso aparece mesmo no desenho ou no documento |
| Aprovaste? | tu — ou quem manda no processo — validaste **esta** versão |
| Funciona? | a solução foi experimentada a sério, com dados e pessoas reais |

O aisa responde às duas primeiras e regista a terceira. **A quarta fica fora**: prova-se a construir e a testar, não a escrever documentos — e nenhum relatório daqui a vai declarar por ti.

Isto existe por causa de um caso real: um desenho que estava impecavelmente construído tinha deixado cair uma coisa que já estava no registo. Estava bem feito e não carregava o que tinha sido pedido. Desde então são perguntas separadas, cada uma com a sua linha.

Quando ainda ninguém verificou, a resposta é **«ainda não foi visto»** — nunca «está bem» nem «está mal». E nada disto revoga uma aprovação que já deste.
