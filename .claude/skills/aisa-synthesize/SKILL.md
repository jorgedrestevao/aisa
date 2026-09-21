---
name: aisa-synthesize
description: Produce the 5 topic packs in <engagement>/_synthesis/ from the Shared Understanding, lens-outputs, and decisions. Auto-runs at the end of aisa-decide; can also be invoked manually. Uses templates in library/kernel/synthesis-templates/.
---

# aisa-synthesize

## Usage

`/synthesize [<topic>]`

- No argument: produce all 5 topic packs.
- `<topic>`: produce only one — `business-story`, `as-is`, `architecture-story`, `risks-and-assumptions`, `financial-story`.

## When it runs

- **Automatically** as the last step of `/decide`.
- **Manually** when a topic pack failed and must be retried, or when the user wants to refresh the synthesis after editing the SU.

## Inputs (read)

- `<engagement>/_state.json` (must be `phase == decision` to produce the full set; manual single-topic runs allowed earlier with a warning).
- `<engagement>/context.json`, `<engagement>/shared-understanding.md`, `<engagement>/decisions.md`, `<engagement>/frame.md`, `<engagement>/options.md`.
- `<engagement>/lens-outputs/*.md` (every lens narrative and every chairman synthesis log).
- `library/kernel/synthesis-templates/<topic>.template.md` (one per topic — defines sources + the synthesis prompt).
- `library/packs/<pack>/pack.yaml` (for any pack-specific synthesis hooks).

## Outputs (written)

- `<engagement>/_synthesis/<topic>.md` — one file per topic, overwritten on re-synthesis.
- `<engagement>/_synthesis/_synthesis-log.md` — append-only audit of each synthesis run (timestamp, topics produced, source counts, warnings).

## The 5 topic packs and their sources

| Topic pack | Primary sources |
|---|---|
| `business-story.md` | SU rows where `lens ∈ {business}` (Confirmed + Assumed) + `lens-outputs/business.md` + `frame.md` |
| `as-is.md` | SU rows where `lens ∈ {operations, user}` + `lens-outputs/{operations,user}.md` |
| `architecture-story.md` | `decisions.md` (chosen option + selected solution + the uncollapsed `(scope, outcome)` pairs) + the approved blueprint's `architecture` block + SU rows where `lens ∈ {technology, data}` + `lens-outputs/{technology,data}.md` + the pack's **fixed** architecture entry point (`library/packs/<pack>/architecture-templates/architecture-core.md`) |
| `risks-and-assumptions.md` | SU sections `Risky` + `Assumed` + `Unknown` (Critical only) + unresolved `Conflicted` + **expired** `Confirmed` + `decisions.md` (Accepted risks + Conditions + Preconditions + Proof obligations + Revision conditions) |
| `financial-story.md` | SU rows where `lens ∈ {financial}` + `lens-outputs/financial.md` + `decisions.md` (economic anchors) + `options.md` S8 — **decision economics ONLY** |

## Synthesis computes no implementation estimate

The implementation-effort calculation is **semantically owned by the `estimate` deliverable** and **executed by `aisa-render`** under that deliverable's projection contract (`library/kernel/render-contract.md`). It was removed from the synthesis layer.

```text
financial synthesis   → decision economics narrative ONLY
Estimate deliverable  → implementation effort calculation and projection
```

`financial-story.md` therefore carries: as-is cost baseline · cost of doing nothing · budget envelope and funding · recorded economic attractiveness (S8 altitude) · entitlement and cost **drivers** · payback/ROI · financial revision triggers.

It must **not** produce: a phased build plan · a per-phase effort table · a timeline or Gantt · an effort summary in days · a team-by-profile effort table · an operational-impact delta table · any person-day figure · any derived total duration · delivery recommendations. **No second synthesis file is created for implementation effort.**

Any implementation-effort sentence surviving in synthesis may only **reference or project an already-produced Estimate**, citing it — never the calculation source, and never where a figure first appears. Prices, SKUs, platform rate cards and quotas-as-cost-facts are prohibited; **drivers only**.

## I-1 — architecture-story is a durable carrier, not architecture authority

```text
outcome basis           semantic owner: the Options layer that emitted the sentence
                        durable source: decisions.md

architectability basis  semantic owner: THE ARCHITECTURE-ENTRY GATE RULE
                        (the recorded selected solution × the frozen
                         active-pack architectability boundary)
                        durable carrier: _synthesis/architecture-story.md
                        § Authorized scope and outcome basis
```

Where the architecture-entry gate yielded `not-authorized`, no blueprint version exists to hold the pair, and that section is its **durable carrier**. As carrier it does **not** own the rule, may **not** change the wording's meaning, may **not** widen or narrow the active pack's architecture authority, may **not** introduce a new basis, and must carry a result **reproducible** from the already-recorded selected solution × the frozen architectability boundary.

**`architecture-story.md` is never the semantic authority for architectability, and this skill never re-evaluates it.** This is the only carriage exception in the model; it does not generalize to any other architecture field.

## I-2 — no fresh comparison

`architecture-story.md` reproduces **the justification the decision recorded** (`decisions.md# D-NNN — Justification`), plus the recorded per-alternative *why not* lines where cited. It does **not** explain why an architecture "won over alternatives". Where the decision recorded no comparison, record none — the absence is honest, not a gap. Creating a new comparison, ranking, score or superiority claim is prohibited in every topic pack.

Stating a comparator's **recorded status** (`COMPARATIVE FIT UNEVALUATED`, `INCUMBENT FIT UNEVALUATED`, class 9's single-axis evidence) is not a comparison: those are recorded facts and they render verbatim.

## Epistemic carriage

Synthesis narrates; it never re-grades. Every item is carried **with its id and its state**:

- `Assumed` never becomes `Confirmed`. An **expired** `Confirmed` is a **re-verification obligation**, never a fact.
- `Unknown` stays open — never resolved, never converted into an assumption or a finding.
- `Conflicted` renders the conflict **or** omits the value. **Choosing a side is prohibited**, with or without a caveat.
- `Risky` keeps its accepted-risk identity: an accepted risk is not a mitigated risk.
- **Proof obligations** are quoted in their five-part shape (*claim · level V1–V4 · method · owner · funded?*) — never re-graded, re-methoded, re-owned or marked satisfied.
- **Conditions and preconditions** are never rendered as already satisfied; a condition becomes satisfied only through engagement evidence.
- Every **volatile value** carries `verificado_em` and `validade`, or renders as a verification obligation.

**Open coverage findings are carried, not closed.** Where a coverage review
(`library/kernel/coverage-contract.md`) left an obligation `partial` or `missing` with a
`required_action` and a `responsible_role`, `risks-and-assumptions.md` carries it **as that
pending item**, with its owner and what would close it. Synthesis never closes one, never
re-judges a disposition, and never turns a routed gap into a resolved one by narrating around
it. A coverage record is **not** an architecture authority and **not** a source of facts: the
architecture block stays the architecture authority, the Shared Understanding stays the
source of facts, and the coverage review says only what was reviewed and what it found.

**Architecture source is fixed.** There is one architecture entry point — `architecture-templates/architecture-core.md` — and no per-decision template selection, no branch-derived path and no router. The synthesis states the **authorized scope**, its **outcome basis**, the **architecture intent**, the **composition**, the **boundaries** and the **imported obligations**. Authorization is read from the recorded architecture block, never derived, upgraded or downgraded.

**No architecture authorization for any scope**: `architecture-story.md` is still produced, but it describes the chosen intervention — process-change scope, roles affected, the do-nothing baseline and its revision triggers, or the selected non-platform solution — instead of a platform architecture. No architecture template is read, and the no-vendor rule then applies to this pack too. State the actual reason: the outcome forbade an architecture, **or** the selected solution is outside the active pack's architecture authority. The two reasons stay distinct, and neither is relabelled *decision blocked*.

## Execution steps

### For each topic to synthesise:

1. Read `library/kernel/synthesis-templates/<topic>.template.md`. The template declares `sources` (paths to read), `prose_structure` (the markdown skeleton), and `synthesis_prompt` (what to do with the sources).
2. Read the engagement files in `sources` (per the table above).
3. Apply the `synthesis_prompt` to produce 3–6 short paragraphs (no fluff; cite SU ids inline like `C-007`).
4. Compose the final markdown by filling the `prose_structure` skeleton.
5. Write `<engagement>/_synthesis/<topic>.md` (overwrite if exists). **`architecture-story.md` opens with its
   authority stamp** (P-18 / F04), on the line after the H1, exactly as the motor prints it:
   ```
   python library/kernel/tools/dashboard.py --engagement <slug> --authority-stamp
   → <!-- authority: _blueprint/ux-blueprint_v<NN>.yaml#architecture @ sha256:<hex> -->
   ```
   The stamp names the blueprint version whose `architecture` block this topic projected (the **approved**
   one; the latest authorized only where no approval exists yet, and the text then says so) and the
   fingerprint of that block. `dashboard.py` compares it with the approved version: a stamp naming
   another version, or a block that changed since, makes the topic **stale by identity**, whatever
   the timestamps say. Never write the stamp by hand. **Where no architecture was authorized**, the stamp is `<!-- authority: none — outcome-forbade -->` or `<!-- authority: none — outside-pack-authority -->`, and it is checked **structurally** against the `(scope, outcome)` pairs in `decisions.md`: absent pairs come back as *not evaluated* (never as verified), malformed pairs or a contradiction (an authorized version on disk) come back as `SYN-STAMP`, and complete pairs pass with a note saying the *meaning* of the reason was not judged (`blueprint-contract.md` → *O carimbo de autoridade*). State which of the two reasons applies — that part is yours; the motor checks the basis, not the meaning. **Exit 5 / a stamp ending in ` INVALID`** means the approved (or latest authorized) version fails the structural check (`blueprint-contract.md` → *Validação estrutural*): **stop** — write no `architecture-story.md`, say which version and which codes (the motor prints them), and name the fix: refazer o desenho → `/blueprint`, aprovar de novo, depois `/synthesize`. An approval recorded over an invalid version is history, not a source.
6. Append a line to `<engagement>/_synthesis/_synthesis-log.md` — one line **per topic**, the topic
   token first (the motor reads freshness **per topic** from these lines; a topic without a line is
   `desconhecido`, never "posterior à aprovação"):
   ```
   <ISO timestamp> — <topic> — sources: <count> SU rows, <count> lens-outputs, <count> decisions — <N> paragraphs, <N> SU ids cited
   <ISO timestamp> — architecture-story — sources: … — authority: _blueprint/ux-blueprint_v<NN>.yaml#architecture
   ```

### After all topics:

7. **Read the contract check** instead of repeating it in prose: `python library/kernel/tools/dashboard.py --engagement <slug> --json` → `status.synthesis_checks`. It recomputes, per topic, `SYN-PARAS` (≥3 paragraphs), `SYN-NO-IDS` / `SYN-DEAD-ID` (every id cited has a row in the SU or a block in `decisions.md`), `SYN-VENDOR` (a term from the pack's `vendor_terms.solution` in a neutral topic — and here too when no architecture was authorized) and `SYN-STAMP`. The `synthesis-validate.py` hook already wrote what it saw to `_synthesis/_synthesis-checks.md`; that file is **history**, the verdict is the recomputed one. Surface any code in the wrap-up output, in business language. **Never** write a check line into `_synthesis-log.md`: the motor reads those lines as synthesis runs, and a check dated today would make a stale pack look fresh.
8. Wrap-up output (business language — `CLAUDE.md` → *Duas línguas*):
   ```user-output
   Resumos por tema: <N>/5 produzidos em `_synthesis/` <| falharam: <lista> — aviso em `_synthesis/_synthesis-log.md`>.
   A seguir: os documentos finais → `/render --all` (ou um só: `/render <nome>`).
   ```

## Hard rules

1. **Never invent claims.** Every sentence in a topic pack must be traceable to a source artefact. If a topic has thin source material, write less — do not fabricate.
2. **Cite SU ids inline.** Each non-trivial claim should anchor to `C-NNN`, `A-NNN`, `R-NNN`, `X-NNN`, or `D-NNN`. Topic packs that omit citations are flagged in the synthesis log.
3. **No vendor names** in `business-story.md`, `as-is.md`, `risks-and-assumptions.md`, `financial-story.md` (these mirror Discovery's neutrality). Vendor names only appear in `architecture-story.md`, anchored to the decision and the recorded architecture.
4. **Idempotence.** Re-running `/synthesize` overwrites the topic packs cleanly. The log is append-only.
5. **Narrate; never decide.** Synthesis may narrate, compress, order, cite ids and **refuse to write where sources are thin**. It may not decide, compare afresh, select an interpretation, re-grade epistemics, resolve an Unknown, **compute the implementation estimate**, pull Domain Knowledge to make prose richer, or infer a new architecture field.
6. **Coverage is neither authority nor eraser.** A coverage review does not settle an architecture field, does not grade a claim, and does not remove a pending item; its open findings are carried forward with their owners. Synthesis reads it as a record of what was reviewed — never as a source of truth about the solution.
7. **No Domain Knowledge pulls for prose.** The architecture layer already consumed the knowledge it needed and the architecture record carries the result. Project the recorded consequence; never re-open a unit to enrich a narrative, and never preload or scan the catalogue.
