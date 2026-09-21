# Glossary — Kernel v0.2.0

Universal aisa vocabulary (not pack-specific). Pack-specific terms live in `library/packs/<id>/glossary.md`.

## Two languages (P-13)

The kernel vocabulary is precise and **stays**: in files, ids, column names and contracts. What the **user reads or answers** — the closing lines of every command, `AskUserQuestion` prompts, `story.md`, the dashboard, the deliverables — goes in business language. The column **Como se diz ao utilizador** is that language. Rules, normative for every command skill (`CLAUDE.md` → *Duas línguas*):

1. A kernel term appears in user-facing text **only between parentheses, after the business phrase**, on its first occurrence — `pergunta em aberto (Unknown)`. Never alone, never as a heading.
2. Ids (`U-nnn`, `C-nnn`, `D-nnn`, `TW-n`, `M-n`, `PM-U-nnn`) appear **between parentheses after the phrase they identify**, never as the subject of a sentence.
3. Commands and paths stay literal, in backticks: `/answer U-012 "…"`, `shared-understanding.md`.
4. `AskUserQuestion`: question and option labels in business language; the id and the kernel term go in the option `description`, not in the `label`.
5. **Technical terminology is never translated** (P-20). Product, vendor, service, surface, store, control and technical-artefact names are **literals** in every user-facing text: `Dataverse`, `Azure SQL`, `SharePoint`, canvas app, model-driven app, custom page, `Power Automate`, `Power BI`, stored procedure, row-level security, column security. They are **not** kernel terms — rule 1 does not apply to them, and there is no business phrase to substitute. Paraphrasing one (`Dataverse` as "loja governada", `Azure SQL` as "a base relacional") is a defect: it destroys the precision the reader needs in order to act, and the paraphrase then leaks into the files, where the vocabulary must stay intact anyway. The pack's `glossary.md` Part B runs the **opposite** direction — a product name a *participant* says converts into the neutral requirement that gets **recorded**; it never licenses paraphrasing a product name back at the reader.

**Forbidden paraphrases** (machine-readable; `.claude/tests/test_user_language.py` fails any user-facing block containing one):

| Literal | Never written as |
|---|---|
| `Dataverse` | loja governada · armazém governado |
| `Azure SQL` | base de dados relacional · base relacional |
| `SharePoint` | listas de colaboração · ferramentas de colaboração |
| canvas app | aplicação de ecrã livre · app de desenho livre |
| model-driven app | aplicação orientada ao modelo |
| custom page | página personalizada |
| `Power Automate` | motor de fluxos |

**Machine-readable contract.** The first column carries the lint tokens: every **bold** term and every `code` token in it is a kernel term the reading test (`.claude/tests/test_user_language.py`) looks for outside parentheses in user-facing text. A plain (non-bold, non-code) word in the first column is an ordinary Portuguese word that also happens to name a column (`custo`, `validade`) — it is not linted. Matching is case-sensitive: `Unknown` is jargon, "unknown" in a sentence is not.

| Term | Definition | Como se diz ao utilizador |
|---|---|---|
| **actors** | Enquadramento theme T1 — the roles that take part, and who owns the process. | quem faz parte disto: que papéis intervêm, e quem manda |
| **trigger** | Enquadramento theme T2 — what starts the process, and how often. | o que faz isto começar, e com que frequência |
| **activities** | Enquadramento theme T3 — what is done, in order, and where something is decided. | o que se faz, por ordem, e onde se decide algo |
| **outcomes** | Enquadramento theme T4 — what comes out, for whom, and how success is known. | o que sai no fim, para quem, e como se sabe que correu bem |
| **invariants** | Enquadramento theme T5 — what must always hold true; the source of the `M-n`. | as regras que ninguém pode quebrar |
| **failure_today** | Enquadramento theme T6 — what goes wrong today and what it costs. | o que corre mal hoje, e quanto custa quando corre mal |
| **change_requested** | Enquadramento theme T7 — what the request wants to change. | o que o pedido quer mudar nisto |
| **INTAKE-SET** | Marker in `enquadramento.md` recording that a conditional theme set was activated by the owner's explicit answer (today: `pricing`). | a marca de que o dono disse que este assunto se aplica |
| **Engagement** | A complete aisa run, from `/start` to `/render --all`, on a single client need. | o projecto (este trabalho de descoberta, do pedido aos documentos finais) |
| **Phase** | One of Discovery, Framing, Options, Decision. See [`phases.md`](phases.md). | a etapa em que estamos |
| **Discovery** | Phase 1 — the lenses read the material and ask, in rounds. | ouvir, ler e perguntar |
| **Framing** | Phase 2 — the council settles the single sentence of the problem. | fixar a frase do problema |
| **Options** | Phase 3 — 3-5 applicable alternatives, each with its order of magnitude and risks; closes with the aisa's recommendation, which is not the decision. The technology lens enters here. | comparar alternativas |
| **Decision** | Phase 4 — the user chooses; then blueprint, synthesis, render. | a escolha — e o que vem depois: o desenho dos ecrãs e os documentos finais |
| **Round** (`ronda`, `R-nn` · `F-nn` · `O-nn` · `D-nn`) | One pass through a phase. Multiple rounds per phase are normal. | uma passagem das perspectivas pelo material |
| **Lens** (`lens`) | A perspective skill (business, operations, ...). Independent, idempotent. | perspectiva (negócio, operações, utilizador, dados, controlo, custo) |
| **Mode** (`inline` · `council-independent`) | Orchestration style: sequential with shared context, or parallel and isolated. See [`orchestration.md`](orchestration.md). | as perspectivas uma a uma · as perspectivas em paralelo |
| **State** | One of Confirmed, Assumed, Unknown, Conflicted, Risky. See [`states.md`](states.md). | o grau de certeza de cada linha do registo |
| **Confirmed** | Claim backed by evidence with a resolvable locator. | o que está verificado (e onde) |
| **Assumed** | Claim held with a declared basis, not yet verified. | o que estamos a assumir (e porquê) |
| **Unknown** | Open question with owner, criticality, cost and swing. | pergunta em aberto |
| **Conflicted** | Two sources disagree; both kept until settled. | duas fontes dizem coisas diferentes |
| **Risky** | Identified risk with impact and proposed mitigation. | risco identificado (com a mitigação proposta) |
| **Critical** (`criticidade`) | Criticality of an open row: Low / Med / Critical. | quão grave é ficar sem resposta — grave = bloqueia o próximo passo |
| **Shared Understanding** (**SU**) | The living artefact `shared-understanding.md` — the single source of truth during an engagement. | o registo do que sabemos |
| **Lens output** | The prose narrative each lens writes in `lens-outputs/<lens>.md`. | a leitura de uma perspectiva, por extenso |
| **Topic pack** | An intermediate synthesized artefact in `_synthesis/`. 5 per engagement. | os resumos por tema que alimentam os documentos finais |
| **Deliverable** | A final rendered artefact for handoff. 6 canonical per engagement. | documento final |
| **Pack** | A domain configuration (pp, outsystems, mendix, generic). | o tipo de solução em vista |
| **Soft gate** (`gate`) | Advisory warning at a phase transition. Overrideable with logged justification. | aviso antes de avançar |
| **Override** | Proceeding past a soft gate with a logged reason. | avançar mesmo assim, com a razão registada |
| **Hard guard** | A hook-enforced rule (only one: `library/` is read-only at runtime). | regra que o sistema não deixa quebrar |
| **Chairman** | The synthesizer in council-independent mode. The only writer to the SU in that mode. | quem junta as conclusões das perspectivas |
| **Council** | The agents (one per lens) running in parallel via Task subagents. | as perspectivas em paralelo |
| **Half-life** (validade) | Decay class of a Confirmed/Assumed row; past it, the row is expired and must be revalidated. See [`states.md`](states.md). | até quando um facto vale sem reconfirmar |
| **Expired** (`expirada`) | A Confirmed/Assumed row past its half-life. | precisa de reconfirmar — não quer dizer que esteja errado |
| **Epistemic health** (`Saúde epistémica`) | Share of Confirmed/Assumed rows still within validity. | quanto do que sabemos ainda está em prazo |
| **Locator** | The anchor that opens the evidence (cell, transcript timestamp, docx section, owner declaration, persisted extraction). | onde exactamente está a prova |
| Custo (`spike` · `reuniao`) | The price of answering an Unknown: `email` · `documento` · `reuniao` · `spike`. | o que custa obter a resposta: resolve-se por email · está num documento · precisa de reunião · precisa de trabalho técnico |
| **Swing** (`decisivo` · `dimensionante` · `cosmético`) | What changes if an Unknown is answered. Drives the meeting agenda and VOI. | o que muda com a resposta: muda o caminho · muda o tamanho · não muda nada — não gastes reunião nisto |
| **Admission of a question** | An Unknown must cite an `M-n`, name ≥ 2 answers **and** name the technical axis each answer moves — the three together. | a pergunta só vale se a resposta mudar algo no que vamos construir — e a linha tem de dizer o quê |
| **Convergence** (`sem convergência`) | Per round: Unknowns created ≤ Unknowns closed. | fechámos mais perguntas do que abrimos · abrimos mais do que fechámos |
| **Meeting agenda** | `/status` output: the questions worth the sponsor's synchronous time, ranked by swing — and the ones explicitly not worth it. | as perguntas que valem o tempo de uma reunião — e as que não valem |
| Enquadramento (`M-n`) | The business mechanism declared by the process owner before round 1; `M-n` are its invariants. | como o negócio funciona, dito pelo dono · uma regra do negócio que a solução tem de respeitar |
| **Funding gate** (`funding_gate`) | Whether going ahead depends on third-party budget approval. | a decisão de avançar depende de aprovação orçamental de terceiros |
| **Tripwire** (`TW-n`) | A revision condition recorded with the decision; when it fires, `/revisit`. | condição que, se acontecer, obriga a rever a decisão |
| **PM-U** | A question raised by the captured process model (`_capture/process-model.md` §6). | pergunta que o ficheiro levantou |
| **Disposition** (`MAP` · `ADOPT` · `DISMISS` · `undisposed`) | What a lens did with a PM-U or material synopsis line. | o que fizemos com essa pergunta: já estava no registo · entrou agora · não interessa · ainda ninguém olhou para esta |
| **Frame** (`frame.md`) | The single sentence of the problem, agreed as D-001. | a frase do problema |
| **Options** artefact (`options.md`) | The 3-5 alternatives compared. | as alternativas |
| **Decision record** (`decisions.md`, `D-nnn`) | The recorded choice with justification, alternatives, accepted risks and tripwires. | a escolha, e porquê |
| **Frame approval** (`D-nnn — Frame agreed`, `Frame sha256`) | The owner's approval of the problem sentence, carrying the fingerprint of the sentence approved. | a aprovação da frase do problema — e de qual versão dela |
| **Supersedes / superseded_by** | A later decision replaces an earlier one; the old block stays, with its counterfactual. | a decisão que substituiu a anterior |
| **Reopen** (`decision → options`) | Putting the alternatives back on the table after a decision, on a fired tripwire or the owner's justified call. | voltar a pôr as alternativas na mesa |
| **Simulate** | Project each option before deciding (screens, effort interval, risks, decision-flipping Unknowns). | ensaiar cada alternativa antes de escolher |
| **Pre-mortem** | The project's obituary written before `/decide`; causes anchored to SU ids, mitigations become requirements/tripwires. | o obituário do projecto, escrito antes de decidir |
| **Blueprint** | The designed screen architecture (`_blueprint/ux-blueprint_vNN.yaml`), iterated to business approval. | o desenho dos ecrãs |
| **Synthesize** | Produce the 5 topic packs from the SU and decisions. | os resumos por tema |
| **Render** (`render-gaps`) | Produce the deliverables; gaps are the slots the SU could not fill. | os documentos finais · o que falta para saírem completos |
| **Revisit** | Compare the present with a frozen counterfactual when a tripwire fires. | reabrir a comparação com o caminho que não seguimos |
| **Retro** | Close-of-engagement diaries of the personas. | as lições do fim, para a próxima vez |
| **Capture** (`_capture`) | Deterministic extraction of the input files plus the process model. | ler os ficheiros e reconstruir o processo como está |
| **Coverage review** (`_coverage/coverage_vNN.json`) | The recorded review that every material obligation of the sources was treated in the artefact under review, and that the review is still current (`coverage-contract.md`). Never an approval, never a proof that the solution works. | a conferência de que o desenho responde a tudo o que foi pedido |
| **Reconciliation** (`reconciliation`) | The coverage stage that runs before designing: the sources against what the record already carries. | conferir as fontes contra o que já está registado |
| **Stale** (`stale`) | A recorded review whose sources, decision or target changed after it was written; it must be redone before being used. It never means the conclusion became false. | a conferência assenta em coisas que entretanto mudaram |
| `not_evaluated` | Nothing was checked here: no record, or the check could not run. Neither a pass nor a failure, and it revokes no approval. | ainda não foi conferido |
| **Structural choice** (`open_architecture_choices`, `structural: true`) | An architecture choice the evidence cannot settle; while open it blocks approval of the blueprint version (`blueprint-contract.md` rule 5), never its production. | escolha de arquitectura que o negócio tem de fechar antes de aprovar o desenho dos ecrãs |
| **Story** | `story.md` — the engagement narrated episode by episode in sponsor language; a projection of the SU, not a source. | a história do projecto, capítulo a capítulo |
| **Read to resume** | Derived per-phase read set `/status` and `/resume` print; never persisted. | o que ler para retomar |
