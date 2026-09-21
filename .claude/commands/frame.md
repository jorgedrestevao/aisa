---
description: Transition Discovery → Framing (council-independent synthesis of the single problem sentence).
argument-hint: "[--override \"<reason>\"]"
---

Invoke the `aisa-frame` skill with `--engagement <slug>` **plus** the arguments provided (resolve the slug first — see below).

Args: $ARGUMENTS

## Antes de invocar a skill

Resolve o engagement e passa-o à skill, para o portão da fase ficar registado no projecto
certo (`.claude/hooks/phase-gate-check.py` escreve em `<engagement>/gate-log.md`):

```bash
python library/kernel/tools/dashboard.py --which-engagement
```

- **Sai 0** com o slug → invoca a skill com `--engagement <slug>` **à frente** dos argumentos
  do utilizador.
- **Sai 4** (vários montados) → o comando **não adivinha**: pergunta ao utilizador qual, por
  `AskUserQuestion`, com os slugs listados como opções, e usa a resposta. Repetir a chamada
  com `--engagement <slug>` confirma a resolução.
- **Sai 3** (nenhum montado) → pára e diz que não há engagement; `/start` cria um.

Quando o utilizador já escreveu `--engagement <slug>` nos argumentos, usa esse e não voltes
a resolver.

