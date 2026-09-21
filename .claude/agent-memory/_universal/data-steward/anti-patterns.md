# data-steward — anti-patterns (universal)

## How to read this file — binding

Nothing here opens a question by itself. Every pattern below is a **hypothesis**: it fires
only where the requirement it names is present, and it says which technical axis moves when
it does. Turning one into an `Unknown` still owes the three declarations of
`library/kernel/states.md` → *Admission of a question*: what the answer serves (an `M-n`, or
the marker `TO-BE DIVERGENCE`), ≥ 2 answers, and which of the eight axes each answer moves.
Where the organisation has simply never decided something, the finding is **the target's
requirement**, not a question waiting on somebody.

## "We'll figure out master data later"
What blocks a build is not an unnamed owner: it is an undecided **system of record** — which store holds the authoritative copy of an entity, which role or service identity may write to it, and how the others learn it changed. **Fires when**: two candidate options put the authority in different places. **Technical consequence**: `modelo de dados`, `componentes`, `padrão arquitetural`. Written that way it is decisive. Written as "who owns master data" it is a name, and a name settles nothing.

## Sensitivity classified by intuition
"This data is sensitive" without a formal classification (Public / Internal / Confidential / Restricted) leaks downstream into governance decisions. Probe the explicit class; if absent, raise Unknown rather than letting the engagement default to "Confidential" out of caution.

## "Volume is small"
Self-reported data volumes under 1k records are usually accurate. Over 1k they are usually wrong by 2-5×. Profile the actual input artefact; never accept the volume claim without a count.

## "It lives in the spreadsheet"
A single Excel file as the system of record for a business-critical entity is a load-bearing single point of failure. Raise Risky on `systems_of_record`; the mitigation must address it explicitly in /decide.

## Migration treated as zero-cost
Historical data migration is almost always under-estimated. If the chosen architecture changes the system of record, the migration is a discrete work package; surface it as a Risky if no migration plan is in the SU.
