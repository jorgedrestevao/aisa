# Power Platform Research — Source Policy

## Objective

The research must be evidence-based.

Sources must be evaluated according to their authority,
technical relevance and proximity to the subject being investigated.

---

# 1. Source hierarchy

Use sources in this order of preference.

## Tier 1 — Primary / authoritative

Highest priority:

- Microsoft Learn
- Microsoft Power Platform documentation
- Microsoft Architecture Center
- Microsoft Well-Architected Framework
- Microsoft technical documentation
- Microsoft official product documentation
- Microsoft official engineering documentation
- Microsoft official licensing documentation

These should be the primary sources for:

- platform capabilities;
- technical limits;
- supported architectures;
- security;
- governance;
- ALM;
- licensing;
- performance;
- product behaviour.

---

## Tier 2 — Microsoft technical material

Use when Tier 1 does not provide sufficient detail:

- Microsoft Tech Community
- Microsoft official technical blogs
- Microsoft engineering blogs
- Microsoft conference material
- Microsoft architecture guidance
- Microsoft official GitHub repositories

---

## Tier 3 — Independent technical sources

Use reputable sources when they provide:

- practical implementation experience;
- independent architectural analysis;
- real-world limitations;
- performance observations;
- implementation patterns;
- comparisons.

Prefer technically credible authors and organisations.

---

## Tier 4 — Community sources

Examples:

- Reddit
- Stack Overflow
- community forums
- personal blogs
- YouTube

These may be useful for discovering:

- recurring problems;
- developer experiences;
- practical limitations;
- unusual edge cases.

However:

Community sources MUST NOT be treated as authoritative evidence
for platform capabilities, limits, licensing or official architecture.

Use them as signals that may require validation against stronger sources.

---

# 2. Search behaviour

Do not search only for positive Power Platform guidance.

For every important area search for:

1. Recommended approach
2. Limitations
3. Known problems
4. Anti-patterns
5. Alternatives
6. Real-world failure cases

Example:

Instead of only searching:

"Power Automate architecture best practices"

also search:

"Power Automate limitations"
"Power Automate anti-patterns"
"Power Automate high volume limitations"
"Power Automate alternatives"

---

# 3. Evidence classification

Every important finding must be classified.

Use:

### FACT

Directly supported by authoritative documentation.

### RECOMMENDATION

A documented or strongly supported recommended approach.

### CONSTRAINT

A technical, licensing, governance or operational limitation.

### TRADE-OFF

A situation where one benefit requires accepting another cost or limitation.

### RISK

A condition that could negatively affect the solution.

### ANTI-PATTERN

An approach that should generally be avoided.

### DECISION CRITERION

A requirement or measurable characteristic that should influence
an architectural decision.

### PATTERN

A recurring architecture or implementation approach.

---

# 4. Source recording

For every significant finding record:

- title;
- source URL;
- source type;
- publication/update date when available;
- relevant section;
- finding;
- evidence classification;
- confidence;
- implications.

Do not save only the URL.

The useful part is the knowledge extracted from the source.

---

# 5. Conflicting sources

If credible sources disagree:

DO NOT silently choose one.

Record:

- Source A says...
- Source B says...
- Why they may differ.
- Which source is more authoritative.
- Whether the difference depends on version, architecture,
  licensing or context.

Mark the finding:

`CONFLICTED`

until the conflict is understood.

---

# 6. Version sensitivity

Power Platform changes frequently.

For information that may change over time:

- record the date;
- record the product/service involved;
- record the relevant version or current state when available.

Treat the following as potentially volatile:

- licensing;
- limits;
- pricing;
- features;
- connector capabilities;
- AI capabilities;
- governance features;
- ALM capabilities.

Do not assume today's value is permanent.

---

# 7. Avoid marketing content

Do not use marketing claims as technical evidence.

Statements such as:

- "build faster";
- "enterprise ready";
- "scales effortlessly";
- "low code means lower cost";

are NOT evidence by themselves.

Translate marketing claims into concrete technical questions.

Example:

"Scales effortlessly"

must become questions such as:

- How many users?
- How much data?
- What throughput?
- What API limits?
- What concurrency?
- Under which architecture?

---

# 8. Research depth

Do not collect hundreds of sources simply to increase volume.

Prefer:

few strong sources
+
cross-validation
+
clear implications

over:

many weak sources.

The final research corpus must be useful for architectural decisions,
not merely comprehensive documentation.

---

# 9. Stop condition

An area is sufficiently researched when:

- the main capabilities are understood;
- the important constraints are understood;
- the relevant decision criteria are identified;
- important alternatives are identified;
- major anti-patterns are identified;
- significant conflicts have been investigated.

Do not continue researching indefinitely once these conditions are met.