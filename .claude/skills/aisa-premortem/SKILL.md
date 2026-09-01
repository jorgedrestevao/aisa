---
name: aisa-premortem
description: Write the project's obituary before deciding — a post-mortem dated N months in the future explaining why the initiative failed, every cause anchored to SU ids (Risky, Assumed with weak/expired validity, open Unknowns, surviving tensions). Run in Options or Decision, before /decide; its mitigations become requirements and tripwire candidates.
---

# aisa-premortem

## Usage

`/premortem [--horizon <meses>]` (default: 12)

## Phase gate

Options ou Decision. Antes disso não há opções para matar — stop com mensagem clara: "/premortem corre em Options ou Decision; fase actual: `<phase>`. Corre /options primeiro."

## Inputs (read)

`_state.json`, `shared-understanding.md` (Risky, Assumed com validade fraca/expirada, Unknown abertas,
Conflicted resolvidas com tensão residual), `frame.md`, `options.md`, `_simulation/*` (a mais recente),
`decisions.md` (se já houver decisão, o obituário mira a opção escolhida; senão, a líder da simulação).

`<engagement>` resolves to `$AISA_ENGAGEMENTS_ROOT/<slug>` if set, otherwise `projects/<slug>`.

## Execution

1. Escolher o alvo (opção escolhida ou líder da simulação mais recente; sem simulação, a opção mais forte de `options.md` — dizer qual e porquê) e a data do obituário (hoje + horizon).
2. Construir 3–6 CAUSAS DE MORTE combinando (não repetindo) o material: cada causa é uma NARRATIVA de
   como 2+ fraquezas se combinaram (ex.: "a delegação nunca definida (U-011) encontrou o pico de Junho
   (R-001) e o SLA morreu no primeiro fecho de trimestre"). PROIBIDO: parafrasear rows Risky uma a uma.
3. Para cada causa: probabilidade subjectiva (baixa/média/alta), o primeiro sinal observável, e a
   mitigação — classificada como REQUISITO (entra no implementation-spec), TRIPWIRE candidato
   (entra no /decide como condição de revisão), ou ACEITAÇÃO consciente.
4. Escrever `<engagement>/premortem.md` (overwrite; audit no council-log):

   ```markdown
   # Post-mortem de <app/opção> — <data futura>

   > ("escrito" como se o projecto tivesse falhado; horizonte: <N> meses; alvo: <O-NNN>)

   ## O que matou o projecto (causas narradas, ids inline)

   ## Os sinais que estavam à vista desde o início (ids)

   ## O que teria evitado (mitigação → classificação)

   ## Probabilidades e o que vamos fazer com isto
   ```

5. Se `story.md` existir (engagements v2.3+), appendar um episódio; sempre: linha ao `council-log.md`.
6. Output: as causas em 1 linha cada + "leva isto ao /decide: N tripwires candidatos, M requisitos".

## Hard rules

1. Cada afirmação ancora em ids — um obituário sem proveniência é ficção, não análise.
2. Tom: narrativa sóbria de post-mortem real, não lista. É para ser LIDO pelo sponsor antes de assinar.
3. Nunca bloqueia o /decide — é soft por construção; a skill de decide apenas o sugere.
4. Rows expiradas contam como fraquezas de pleno direito (uma "certeza" caducada é combustível de
   causa de morte); cita-as com a data do último `verificado_em`.
