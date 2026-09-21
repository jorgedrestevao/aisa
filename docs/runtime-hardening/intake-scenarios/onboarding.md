# Cenário de intake — onboarding

> Camada 2 de B4, **corrida interactiva**. `## INPUT` e `## OWNER-SCRIPT` foram fixados antes;
> `## ASKED` regista as perguntas **efectivamente emitidas** e a resposta escolhida em cada
> uma; `## ENQUADRAMENTO` é o ficheiro que a corrida escreveu, lido do disco.
>
> **Como foi corrido.** Cada pergunta desta lista foi emitida por `AskUserQuestion` nesta
> sessão, uma a uma, pela ordem que `aisa-orient` passo 3 declara. O dono respondeu ao vivo,
> escolhendo entre as opções apresentadas; a resposta registada é o texto da opção escolhida,
> verbatim. Nenhuma resposta foi lida de um guião durante a corrida — o `OWNER-SCRIPT` serve
> agora de **baseline**, e onde a resposta viva divergiu dele, diz-se em `## DIVERGENCES`.
>
> Engagement de teste isolado: `docs/runtime-hardening/intake-scenarios/_runs/onboarding-colaboradores/`.
> Nenhum engagement real foi tocado.

## INPUT

```
Temos um problema com a entrada de gente nova. Quando entra alguém, o responsável manda um email ao IT a pedir acessos, outro ao facilities para a secretária e o cartão, e depois anda atrás de toda a gente durante duas semanas. Já aconteceu alguém chegar no primeiro dia e não ter computador. Queríamos organizar isto.
```

## OWNER-SCRIPT

Baseline fixada **antes** da corrida, para se poder ver o que divergiu.

- **activation (`A saída deste processo é um preço, cotação, margem ou valorização?`)**: **Não**
- **T1 actors**: "O responsável da equipa que recebe a pessoa é quem manda no processo. Entram o IT para os acessos, o facilities para o espaço e o cartão, e os recursos humanos para o contrato."
- **T2 trigger**: "Começa quando o contrato é assinado, e normalmente é uma ou duas pessoas por mês, com picos em Setembro."
- **T3 activities**: "Pedir os acessos, pedir o posto e o cartão, preparar o contrato, marcar a formação de segurança, e no primeiro dia apresentar a equipa. Quem decide o que a pessoa pode aceder é o responsável da equipa."
- **T4 outcomes**: "No fim a pessoa está a trabalhar. Corre bem quando no primeiro dia tem computador, acessos e alguém à espera dela."
- **T5 invariants**: "Ninguém entra sem contrato assinado. Ninguém tem acesso a um sistema sem o responsável da equipa aprovar. A formação de segurança tem de estar feita nos primeiros cinco dias."
- **T6 failure_today**: "Perde-se a primeira semana da pessoa. Já aconteceu duas vezes este ano alguém chegar sem computador, e isso custa-nos uma semana de trabalho mais a impressão que fica."
- **T7 change_requested**: "Queremos que os pedidos saiam sozinhos quando o contrato é assinado, e ver num sítio só o que falta para cada pessoa."
- **autoridades**: "O responsável de recursos humanos também pode confirmar."
- **funding gate**: Não

## ASKED

As 10 perguntas emitidas, por ordem, com a resposta escolhida. `[orient]` = `aisa-orient`
passo 3 · `[start]` = `aisa-start` passo 4.

1. `[orient]` T1 `actors` — Quem faz parte disto, que papéis intervêm, e quem manda no processo?
   → **Responsável da equipa manda**: "O responsável da equipa que recebe a pessoa é quem manda no processo. Entram o IT para os acessos, o facilities para o espaço e o cartão, e os recursos humanos para o contrato."
2. `[orient]` T2 `trigger` — O que faz este processo começar, e com que frequência?
   → **Contrato assinado**: "Começa quando o contrato é assinado, e normalmente é uma ou duas pessoas por mês, com picos em Setembro."
3. `[orient]` T3 `activities` — O que se faz, por ordem, e onde é que se decide alguma coisa?
   → **Acessos, posto, contrato, formação**: "Pedir os acessos, pedir o posto e o cartão, preparar o contrato, marcar a formação de segurança, e no primeiro dia apresentar a equipa. Quem decide o que a pessoa pode aceder é o responsável da equipa."
4. `[orient]` T4 `outcomes` — O que sai no fim, para quem, e como se sabe que correu bem?
   → **Pessoa a trabalhar no dia 1**: "No fim a pessoa está a trabalhar. Corre bem quando no primeiro dia tem computador, acessos e alguém à espera dela."
5. `[orient]` **activation** — A saída deste processo é um preço, cotação, margem ou valorização?
   → **Não**
6. `[orient]` T5 `invariants` — O que tem de se manter sempre verdadeiro, as regras que ninguém pode quebrar?
   → **Contrato, aprovação, formação**: "Ninguém entra sem contrato assinado. Ninguém tem acesso a um sistema sem o responsável da equipa aprovar. A formação de segurança tem de estar feita nos primeiros cinco dias."
7. `[orient]` T6 `failure_today` — O que corre mal hoje, e quanto custa quando corre mal?
   → **Perde-se a primeira semana**: "Perde-se a primeira semana da pessoa. Já aconteceu duas vezes este ano alguém chegar sem computador, e isso custa-nos uma semana de trabalho mais a impressão que fica."
8. `[orient]` T7 `change_requested` — O que é que o pedido quer mudar nisto?
   → **Pedidos automáticos e visão única**: "Queremos que os pedidos saiam sozinhos quando o contrato é assinado, e ver num sítio só o que falta para cada pessoa."
9. `[orient]` **autoridades** — Para além de ti, quem tem autoridade para confirmar factos sobre este processo?
   → **Responsável de RH também**: "O responsável de recursos humanos também pode confirmar."
10. `[orient]` **funding gate** — A decisão de avançar depende de aprovação orçamental de terceiros?
   → **Não**
11. `[start]` — **nenhuma pergunta emitida**. Recebeu tudo de `aisa-orient` e não repetiu (passo 4: «do not ask again»).

Nenhuma das cinco perguntas de pricing foi emitida — a resposta à activação foi *Não*.

## DIVERGENCES

Nenhuma: as respostas vivas coincidiram com a baseline em todos os temas.

## ENQUADRAMENTO

Escrito em `_runs/onboarding-colaboradores/enquadramento.md` a partir das respostas acima, lido do disco:

```markdown
## T1 · actors
O responsável da equipa que recebe a pessoa é quem manda no processo. Entram o IT para os acessos, o facilities para o espaço e o cartão, e os recursos humanos para o contrato.

## T2 · trigger
Começa quando o contrato é assinado, e normalmente é uma ou duas pessoas por mês, com picos em Setembro.

## T3 · activities
Pedir os acessos, pedir o posto e o cartão, preparar o contrato, marcar a formação de segurança, e no primeiro dia apresentar a equipa. Quem decide o que a pessoa pode aceder é o responsável da equipa.

## T4 · outcomes
No fim a pessoa está a trabalhar. Corre bem quando no primeiro dia tem computador, acessos e alguém à espera dela.

## T5 · invariants
Ninguém entra sem contrato assinado. Ninguém tem acesso a um sistema sem o responsável da equipa aprovar. A formação de segurança tem de estar feita nos primeiros cinco dias.

## T6 · failure_today
Perde-se a primeira semana da pessoa. Já aconteceu duas vezes este ano alguém chegar sem computador, e isso custa-nos uma semana de trabalho mais a impressão que fica.

## T7 · change_requested
Queremos que os pedidos saiam sozinhos quando o contrato é assinado, e ver num sítio só o que falta para cada pessoa.

## Invariantes
Lidos de **T5**, verbatim, uma linha por frase declarada.

| id | invariante | o que orienta | fonte |
|---|---|---|---|
| M-1 | Ninguém entra sem contrato assinado. | o gatilho do processo | declaração do dono, 2026-09-11 |
| M-2 | Ninguém tem acesso a um sistema sem o responsável da equipa aprovar. | o plano de imposição de permissões | declaração do dono, 2026-09-11 |
| M-3 | A formação de segurança tem de estar feita nos primeiros cinco dias. | o prazo que qualquer solução tem de respeitar | declaração do dono, 2026-09-11 |
```

Não existe secção `## pricing` e não existe o marcador `INTAKE-SET` em parte nenhuma do ficheiro.

## EVIDENCE-LEVEL

`interactive`

As 10 perguntas foram **emitidas** por `AskUserQuestion` e as 10 respostas foram escolhidas
ao vivo pelo dono. A passagem entre skills está registada: tudo foi recolhido em
`aisa-orient` passo 3 e `aisa-start` não repetiu nenhuma pergunta, como o seu passo 4 manda.

Limite honesto do que isto prova: é **uma** corrida, nesta sessão, com este modelo. Não
demonstra que qualquer sessão futura emita exactamente estas perguntas — demonstra que esta
emitiu, e deixa o registo para se poder comparar.

## CHECKS

CHECK-1: PASS — a pergunta de activação foi emitida exactamente uma vez, e em nenhum outro ponto do percurso. É a excepção explícita à regra do CHECK-2.
CHECK-2: PASS — resposta *Não*: zero perguntas de pricing emitidas, e o `enquadramento.md` não tem `## pricing` nem `INTAKE-SET`.
CHECK-3: PASS — `aisa-start` não emitiu pergunta nenhuma (último item de `ASKED`): recebeu tudo de `aisa-orient`; nenhum texto de pergunta aparece duas vezes na lista.
CHECK-4: PASS — os 3 `M-n` são as 3 frases de T5, verbatim, nem mais nem menos.
