## 6. Interrogation list (PM-U-NNN)

| id | question | why it matters | suggested respondent (role) | criticidade | custo | swing |
|---|---|---|---|---|---|---|
| PM-U-001 | Who else can currently repair the workbook when it breaks? | single-point-of-failure claim | requester / team lead | Critical | reuniao | decisivo: continuity is a requirement of any to-be |
| PM-U-002 | On Monday and Tuesday, which input columns are typically still empty at pricing time, and what does the process do today when a quote is missing? | the sponsor's second ask | requester / pricing analyst | Critical | spike | decisivo: fill gaps vs replace the estimation method |
| PM-U-003 | Is there a documented or tribal method today for estimating a missing quote? | estimation feature exists informally vs from zero | pricing analyst | Critical | reuniao | decisivo: formalize vs design |
| PM-U-004 | Where is the weekday/port table actually consumed? | unused vs manual glance | file maintainer | Med | spike | dimensionante |
| PM-U-005 | What was the dead add-in link meant to provide, when did it stop, was it replaced? | prior automation attempt | requester / IT | Critical | email | decisivo: what not to repeat |
| PM-U-006 | Are the two market series actually read downstream? | two unreconciled feeds | requester / pricing analyst | Med | spike | dimensionante |
| PM-U-007 | Why do the base sheets' dates stop advancing? | dead weight or missed step | file maintainer | Low | email | cosmético |
| PM-U-008 | What should the broken named range point to? | orphan reference | file maintainer | Med | spike | dimensionante |
| PM-U-009 | Why six structurally identical copies of the same report? | root cause of corruption | requester / file maintainer | Critical | reuniao | decisivo: primary root-cause candidate |
| PM-U-010 | Is the broken reference table a known, tolerated break? | half the sheet broken | requester | Low | email | cosmético |
| PM-U-011 | What is the cadence/deadline for producing the output — who reads it, by when, in what format? | sizes urgency | requester / operations lead | Critical | reuniao | dimensionante: SLA |
