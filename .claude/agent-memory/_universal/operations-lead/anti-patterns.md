# operations-lead — anti-patterns (universal)

## Digitalizing a broken process
The strongest single signal that an engagement will fail is a request to digitalize a process the operations team itself describes as broken. Digital tooling on top of broken work amplifies the dysfunction. If the as-is reconstruction surfaces "this used to be done differently and we don't know why we do it this way" → raise Risky (`impacto: amplifies dysfunction at scale`).

## "It's all in the Excel"
A single load-bearing spreadsheet — owned by one person, undocumented — is a tribal-knowledge anchor. Reproducing it inside the new system without first reverse-engineering the rules is a classic failure mode. Flag as Risky and demand the spreadsheet be opened and profiled before /options.

## The happy path is 60% of the volume
When the documented process covers ~60% of cases, the remaining 40% are exceptions handled by discretion. The discretion is the actual work. Discovery that records only the happy path will produce a deliverable the dev team builds, then the real volume hits it and it falls over.

## Handoff via email
"And then we email Finance to validate" is a discovery red flag — it almost always means latent SLA, no audit, no observability. Surface as Unknown on `audit_requirements` if not already there.

## "It only takes 5 minutes per case"
Self-reported cycle times under 10 minutes are usually wrong by 2-3×. Cross-check against volume × team size × hours/week if any of those are known.
