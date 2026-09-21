# 05-OUTPUT-CONTRACT

Binding on the **output** of any pack authoring — this pack re-authored, or a new one
(`outsystems`, `mendix`, any other). It is not a research instruction; it is the shape the
research is allowed to leave behind. Written 2026-09-10, refoco em decisão técnica, fase 3.

## 1. Roles, identities and mechanisms — never persons

A runtime unit describes what running a design requires, as **design objects**:

| Object | What it is | What it is not |
|---|---|---|
| **Role** | the authority that acts, defined by what it may do | a person, a team name, a job title |
| **Identity** | what the action executes as (service principal, capacity-licensed identity, personal licence) | who holds the account |
| **Permission** | what that identity must hold for the action to succeed | an approval, a sign-off |
| **Mechanism** | what detects the condition and what repairs it | an intention, a commitment |
| **Alert destination** | where the signal lands, shared and already existing | a mailbox belonging to somebody |
| **Recovery procedure** | the ordered steps, with the role assigned to each | an on-call name |

**The two sentences no unit may write**, whatever the pack:

```text
no operator, therefore unavailable
immature, therefore deferred
```

Both are selection verdicts, and both rest on a fact about the organisation rather than
about the design. Where a design has not defined the objects above, the unit states a
**requirement with a cost**, priced into the option that carries it. Whether that cost
blocks, conditions or merely prices an option belongs to the decision model —
`decision-tree.md` §6.1 for the technical axes that block, `decision-model/outcome-classes.md`
for the class the finding lands in, and class 15 (*viable if the rule is changed*) where an
organisational rule is what stands in the way.

**Preserved, because they are technical, and not to be removed by a sweep:** the artefact
`owner` as a runtime dependency (throughput, suspension, licensing), authority over data,
provenance, and any retention or audit obligation a rule in scope actually imposes.

## 2. Evidence stands; conclusions are corrected

Where a source legitimately says something organisational — a vendor checklist about team
practice, for example — the **citation stays**. What is corrected is the conclusion drawn
from it, and the correction is written as an errata beside the unit, dated. Historical
authoring is not rewritten as though it had never existed (`docs/TECHNICAL_DECISION_REFOCUS_IMPLEMENTATION_PLAN.md` §2).

## 3. Discovery output stays vendor-neutral

Signals, questions and requirements produced for Discovery name no vendor and no product
(`00-MISSION.md`, *Critical distinction*). A unit that answers a Discovery question in
product terms is an authoring defect, not a shortcut.
