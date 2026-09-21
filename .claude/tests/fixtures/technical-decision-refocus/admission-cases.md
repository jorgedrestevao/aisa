# Fixture — casos de admissão (P-26) e da forma de `quem responde` (F1.1)

Sintético. Nenhuma linha vem de um engagement real: `projects/` é um ponto de montagem
gitignored para o repositório privado, e nenhum engagement pode ser comitado como fixture
(a mesma regra que `test_status_model.py` declara no seu cabeçalho).

Cada linha existe para exercitar **um** caso, e o seu id diz qual. As colunas são as de
`library/kernel/states.md` → *Schema of Shared Understanding rows*.

## Unknown

| id | lens | pergunta | quem responde | criticidade | custo | swing | ronda |
|---|---|---|---|---|---|---|---|
| U-901 | data | Qual é o volume mensal de pedidos? | role: dono do processo | Med | email | dimensionante: entre 50 e 500 por mês o padrão é o mesmo; muda a faixa de esforço. Eixo: esforço de alto nível | R-01 |
| U-902 | governance | A identidade externa que chega ao armazenamento é partilhada ou por utilizador? | fonte: configuração da ligação | Critical | spike | decisivo: TO-BE DIVERGENCE — o alvo tem de decidir o plano de imposição. Partilhada, ou por utilizador. Elimina o ramo «segurança por linha imposta no armazenamento». Eixos: plano de imposição de permissões · padrão arquitetural | R-01 |
| U-903 | business | Serve M-2. Quem assina a acta da reunião de arranque? | role: dono do processo | Critical | reuniao | serve M-2 | R-01 |
| U-904 | operations | Onde está a pasta diária do ficheiro antigo? | | Low | email | cosmético | R-01 |
| U-905 | data | O armazenamento é o A ou o B? | role: equipa de plataforma | Critical | spike | decisivo: TO-BE DIVERGENCE — A ou B. Elimina o ramo «um só armazenamento». Eixos: modelo de dados · componentes | F-01 |
| U-906 | technology | Serve M-1. O padrão é simples ou composto? | role: arquitectura | Critical | reuniao | serve M-1 | O-01 |
| U-907 | chair | Serve M-3. Quem valida a acta do enquadramento? | role: dono do processo | Critical | reuniao | serve M-3 | F-01 |

## Assumed

| id | lens | claim | base da assumption | verificado_em | validade | ronda |
|---|---|---|---|---|---|---|
| A-901 | data | O volume mensal está entre 50 e 500 pedidos | duas observações do dono, não uma série. Condição de revisão: uma extracção do histórico contradiz a ordem de grandeza | 2026-09-10 | organizacional | R-01 |
