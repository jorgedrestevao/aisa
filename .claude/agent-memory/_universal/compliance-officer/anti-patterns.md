# compliance-officer — anti-patterns (universal)

## How to read this file — binding

Nothing here opens a question by itself. Every pattern below is a **hypothesis**: it fires
only where the requirement it names is present, and it says which technical axis moves when
it does. Turning one into an `Unknown` still owes the three declarations of
`library/kernel/states.md` → *Admission of a question*: what the answer serves (an `M-n`, or
the marker `TO-BE DIVERGENCE`), ≥ 2 answers, and which of the eight axes each answer moves.
Where the organisation has simply never decided something, the finding is **the target's
requirement**, not a question waiting on somebody.

## Separation of duties — only where an obligation requires it
That one role both submits and approves is a fact about the as-is, not a defect to fix by default. **Fires when**: a regulation, contract or internal policy in scope requires the split — cite it. **Technical consequence**: the split is a permission model (two roles, two actions, one enforcement plane) and it moves `plano de imposição de permissões`, often `modelo de dados` (the state a record sits in between the two). With no obligation cited, whether to split is a design choice the target makes — not a Risky, not a question.

## Approval ladder undefined
"Whoever is available approves" describes the organisation, and an organisational gap is not this project's pending work. **Fires when**: approval is behaviour of the process in scope — a transition the target must implement. **Technical consequence**: states, transitions and the role authorised at each, which moves `modelo de dados` and `plano de imposição de permissões`. The ladder the target will enforce is then a **requirement to define** — `Assumed` with its basis, settled by the owner at `/decide`. Where approval is not process behaviour, nothing is written: no `Unknown`, no Critical.

## Offline + sensitive data
The collision is **not intrinsic**: it is a question about what the target can enforce on a local cache — encryption at rest, remote wipe, the subset that may be cached, retention on the device. Check that first. Where the platform enforces it, there is no conflict and the answer is a control. Only where it cannot is the row **Conflicted**, with the enforcement gap named and the axes it moves (`tecnologia` · `componentes` · `plano de imposição de permissões`); the owner resolves it at `/decide` (cached subset / no offline / re-classify). Never choose silently — and never open the conflict before checking what can be enforced.

## DLP-blind design
For organisations with tenant-level DLP (data-loss-prevention) policies governing external integrations: every required external data-flow needs a DLP classification check up front. A discovery that assumes "we can just add an integration to X" without surfacing the DLP question lands the engagement in a 4-8 week wait while IT changes policy. Always probe the DLP classification of any external integration the as-is implies.

## Audit "after-the-fact"
Designing audit as a quarterly export rather than per-event is a discovery anti-pattern. The audit-on-Approve / Audit-on-Delete / Audit-on-Export pattern (see `library/packs/pp/domain-knowledge/craft/security-craft.md`) is an architectural property of the write path, not a feature added later. **Fires when**: an audit obligation is in scope, named, with the events it covers. **Technical consequence**: capture point, retention and export path — it moves `padrão arquitetural` and `modelo de dados`, and a quarterly export cannot retrofit evidence that was never captured. With no obligation in scope, no trail is proposed by default. Whether the required control is available at all, on which enforcement plane, and over what population is a separate question owned by `library/packs/pp/domain-knowledge/security/security-controls.md`.
