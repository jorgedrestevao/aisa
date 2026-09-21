# Domain knowledge — the use contract

<!--
provenance: RUNTIME (domain knowledge) · class: CONTRACT
authored: 2026-09-04 (Step 4B) · design authority: Step 4A — Domain Knowledge Runtime Model
Pull-based: consulted when a concrete decision question requires it (decision-tree.md §9).
Never preloaded. Canonical research traceability lives in the Step 4B authoring report.
-->

This directory holds **technical knowledge**, not decision logic. It exists so a reasoner holding a
concrete decision question can go deep enough to answer it defensibly.

```text
decision model     →  decides what question needs answering   (decision-tree.md + decision-model/)
domain knowledge   →  provides the technical knowledge to answer it   (this directory)
```

## 1. The pull rule — binding

```text
concrete material question
  → pull ONE relevant knowledge unit
  → deepen
  → pull another ONLY if the first exposes a second material dependency
```

- **Never preloaded.** Not at the start of Options, not per concern, not "to be thorough".
- **A concern is not a question.** *"C4 is material"* is not a reason to pull; *"does this store enforce
  column-level confidentiality?"* is.
- **Cite the file *and* the section.** A filename alone is not a citation.
- **No router.** The directory name is the subject boundary, the filename names the question domain, and
  each file's §0 lists the questions it answers. That is the whole retrieval mechanism.

## 2. Depth rule

Depth is set by `decision-tree.md` §7.2, and it gates the pull:

| Depth | Domain pull |
|---|---|
| **D0 — not material** | none |
| **D1 — brief** | none |
| **D2 — analysed** | only where a relevant boundary is contested or unclear |
| **D3 — deep** | pull the unit that answers the question |

## 3. Grade convention

Every section inside a unit is marked with one grade. **Decision-grade sections come first**, so a D3
Options pull can read them and stop.

| Grade | Serves | Read by |
|---|---|---|
| `decision-grade` | viability · option class · major trade-off · major control · economics · proof obligation | Options (D3), `/simulate` |
| `architecture-grade` | how the mechanism composes once the option class is established | `/blueprint`, `solution-blueprint`, architecture templates |
| `implementation-grade` | how to build it | `implementation-spec`, `claude-design-brief` |

**Options never reads implementation-grade content merely because it exists.** Where a subject's build
body is large it lives in `craft/` instead.

## 4. Two classes of file

| Class | Directories | Authority |
|---|---|---|
| **RESEARCH** | `application/` `data/` `automation/` `integration/` `security/` `governance/` `alm/` `performance/` `economics/` `operations/` `architecture/` | States supported platform and domain knowledge |
| **CRAFT** | `craft/` | States delivery practice — engagement convention, not platform truth |

**`craft/` is never a D3 Options pull target.** A CRAFT file may not state a platform limit, a threshold or
a comparative claim; where one is required it refers to the RESEARCH unit that owns it.

## 5. Stable and volatile — who owns what

| Responsibility | Owner |
|---|---|
| The boundary **question** in decision logic | `decision-tree.md` |
| The stable **explanation** — what the mechanism is, why the boundary exists, what it excludes | the knowledge unit here |
| That a fact **is volatile**, and when to re-verify it | `decision-model/volatility-register.md` |
| The **current value** used for a decision, with its date | the engagement's own SU row (`verificado_em` + `validade`) |

A figure appearing in a unit is stamped as a reading with its re-verify row:

```text
> Documented reading · read 2026-09-04 · re-verify: VS-NN
```

A **conflicted** figure is never carried on either side — the conflict itself is the content, and the
consequence is *decision-blocked until measured*. **No price, SKU or per-unit currency figure appears
anywhere in this directory.**

## 6. Prohibition

> **Domain knowledge never chooses the winning option.**

No option class, no stage order, no exit class, no blocking logic, no comparator or preference semantics,
no fit score, no fit ladder, no architecture "branch". A capability absence is domain knowledge;
*"therefore inappropriate"* is a selection verdict and belongs to `decision-tree.md`.

**An availability verdict that rests on a person is doubly out of contract** — it is a selection verdict,
and it is one this directory could not make even if it were entitled to. A unit here explains what running
a design requires: the **role** that acts, the **identity** it acts as, the **permission** that identity
needs, the **mechanism** that detects the condition, the **alert destination**, and the **recovery
procedure**. Where a design has not defined them, what this directory states is a **requirement with a
cost**. Whether that cost blocks, conditions or merely prices an option is the decision model's ruling:
`decision-tree.md` §6.1 for the technical axes that block, `decision-model/outcome-classes.md` for the
class the finding lands in. Neither "no operator, therefore unavailable" nor "immature, therefore deferred"
is a sentence this directory may write.

The shapes a design states, and which are enough to keep technical control without naming anybody:

```text
Role Operações: reprocessar sincronização
service principal: executar flow
Role Administrador da Plataforma: gerir ambiente
```

Each is an action, on a resource, by an authority, with the identity it executes as. A person may hold
the role; the design does not care which, and says so.

A documented boundary here is **not** evidence that another option class does better. Depth on this
platform raises confidence about *this platform's* boundaries and nothing else; where comparative
evidence is absent, `decision-model/outcome-classes.md`'s comparator semantics are authoritative.
