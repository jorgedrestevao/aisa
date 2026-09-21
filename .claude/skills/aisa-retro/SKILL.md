---
name: aisa-retro
description: Close-of-engagement retro — each council persona writes its diary entry for this engagement (what its lens got right, where it was naive, patterns to watch, one advice to its future self). Entries are STAGED in <engagement>/_retro/ for human curation; only after explicit user approval are they appended to .claude/agent-memory/_universal/<persona>/diary.md (tracked — the append goes through the repo's normal git flow). Personas cite their diaries in future engagements.
---

# aisa-retro

## Usage

`/retro` — tipicamente após o render final. Qualquer fase é aceite, com aviso se cedo ("a retro captura mais depois do /render; continuar?").

## Execution

1. **Launch the 7 personas in PARALLEL** (Task calls in one message): `business-analyst`, `operations-lead`, `user-advocate`, `data-steward`, `compliance-officer`, `cfo-lens`, `solution-architect`. Each receives: the final SU, its own accumulated `lens-outputs/<lens>.md`, `answers.md`, `decisions.md`, `premortem.md` (se existir), and its current `diary.md`. Prompt:

   ```
   Escreve a entrada de diário deste engagement: 2-4 parágrafos —
   (a) o que a tua lens apanhou que importou;
   (b) onde falhaste ou foste ingénuo (sê específico — datas, ids, o que não perguntaste);
   (c) padrões que esperas rever noutros engagements;
   (d) um conselho ao teu futuro eu.
   Sem nomes de pessoas ou de cliente; domínio genérico (ex.: "procurement de mid-cap").
   Formato: ## <slug-anonimizado> — <data>. Máx. 250 palavras.
   ```

2. **Stage** each return in `<engagement>/_retro/diary-<persona>.md`. Nothing touches agent-memory yet.
3. **Present the set to the user** and ask for curation: aprovar tudo / editar entradas / excluir personas. List each entry's (b) — the failure paragraph — explicitly: an all-wins diary is suspect and should be pushed back on.
4. **ONLY after explicit approval**: append each approved entry to `.claude/agent-memory/_universal/<persona>/diary.md`. Remind the user that agent-memory is tracked — the append lands in the repo via the normal git flow (a skill prepares the change; the human owns the commit). Tenant-proprietary detail belongs in `_tenant/` (private repo), never in `_universal/`.
5. Final episode in `story.md` ("o council fecha o caderno e guarda o que aprendeu") + `council-log.md` line. Output to the user, after step 2 and before the curation question (business language — `CLAUDE.md` → *Duas línguas*):
   ```user-output
   Lições do fim — <7> perspectivas escreveram o seu diário; as entradas estão em `_retro/`, à espera da tua curadoria.
   Onde cada uma diz que falhou: <perspectiva — uma linha> …
   A seguir: aprovar tudo · editar · excluir — a pergunta vem já a seguir; só depois disso as entradas entram na memória das perspectivas.
   ```

## Hard rules

1. **NUNCA escrever em agent-memory sem aprovação humana nesta sessão** — a regra do repo é "memória editada pelos consultores"; esta skill só reduz o custo da curadoria.
2. **Anonimização**: zero nomes de pessoas/cliente nas entradas `_universal`; domínio genérico apenas.
3. **O diário é falível por design**: registar erros é o objectivo — uma entrada só de vitórias é suspeita e a curadoria deve devolvê-la.
4. Nos engagements seguintes, as personas citam o diário quando um padrão se repete («num engagement anterior de <domínio>, vi…») — nunca detalhe proprietário fora do tenant.
