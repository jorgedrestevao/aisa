Review Status: COMPLETE (adversarial cross-block review, pass 1)
Review Confidence: HIGH on the mechanical findings; MEDIUM on the severity calibration
Reviewed Corpus Status: all eight files DRAFT, Gate NOT RUN / PENDING
Review date: 2026-09-03

# Cross-Block Review — Power Platform Research Corpus

Scope: Block A (`integration-architecture.md`, `architecture-patterns.md`), Block B (`security.md`, `governance.md`, `alm-devops.md`), Block C (`performance-scale.md`, `licensing-cost.md`, `operations-support.md`), read against `../README.md`, `../research-prompt.md`, `../source-policy.md`, `../research-areas.md`.

This is a **research review**. It authors no pack content, and `library/packs/pp/` was not touched.

**Method.** Each file was read in full. Every cross-block claim in this review was then verified mechanically (filename-citation matrix, id-namespace extraction, term-frequency counts per file, deferral-target resolution). Counts quoted below are reproducible. Where a suspected contradiction did not survive verification it is recorded as **not a contradiction** rather than dropped, so that a later reader does not re-raise it.

**Id convention for this review.** Findings here are `XB-nn`. All other ids belong to the file named beside them. Note that the corpus's own id namespaces collide across files — this is itself finding XB-03 — so every id below is qualified by its file.

---

## 1. Review Status

| Item | State |
|---|---|
| Files read in full | 8 of 8 |
| Meta files read | 4 of 4 (`README.md`, `research-prompt.md`, `source-policy.md`, `research-areas.md`) |
| Cross-block citation matrix | Built and verified (§16) |
| Id-namespace collision check | Run; collisions found (XB-03) |
| Deferral-target resolution | All 14 inter-area deferrals traced to their named target |
| Contradiction candidates raised | 11 |
| Contradiction candidates confirmed | 4 (XB-01, XB-07, XB-09, XB-12) |
| Contradiction candidates **rejected** on evidence | 3 (§5.4) |
| Findings recorded | 19 (4 CRITICAL, 7 HIGH, 7 MEDIUM, 1 LOW) |
| Gate run on any reviewed file | **No** — all eight are DRAFT with Gate NOT RUN or PENDING |

---

## 2. Overall Research Confidence

**Per block, as self-declared and as assessed.**

| Block | File | Self-declared | This review's assessment | Basis |
|---|---|---|---|---|
| A | `integration-architecture.md` | MEDIUM-HIGH | **MEDIUM-HIGH — sustained** | 40 of 47 sources Tier 1 fetched with `ms.date`; boundaries stated as crossing conditions; nine explicit "not the integration layer" conditions; conflicts registered rather than resolved silently |
| A | `architecture-patterns.md` | MEDIUM | **MEDIUM — sustained** | Honest about its two unequal evidence classes; AP-10 self-flagged as synthesis; every pattern carries *When NOT to use* |
| B | `security.md` | MEDIUM | **MEDIUM-HIGH within its own scope** | Five-plane model is the best organising device in the corpus; residuals stated explicitly; 40 Tier 1 sources |
| B | `governance.md` | MEDIUM | **MEDIUM — sustained** | Seven levers with the preventive/detective split; GOV-C2 surfaces a genuine economic tension rather than absorbing it |
| B | `alm-devops.md` | MEDIUM | **MEDIUM — sustained** | Four-rung ladder; irreversibility findings (publisher, ownership type) are decision-grade |
| C | `performance-scale.md` | MEDIUM | **MEDIUM — sustained; best epistemic discipline in the corpus** | §0's limits-not-benchmarks rule; five-meter map; `UNPUBLISHED` used as a first-class verdict |
| C | `licensing-cost.md` | MEDIUM | **MEDIUM — sustained** | LC-01 (no Cost Optimization pillar) and §0.2 (Learn is not authoritative) are structurally important negative findings |
| C | `operations-support.md` | MEDIUM | **MEDIUM-HIGH within its own scope** | 100 numbered limitations; OP-05's ownership cascade is the best synthesis in the corpus |

**Corpus-level confidence: LOW-MEDIUM.**

This is deliberately *below* the lowest individual file. The reason is not the quality of any block but the **absence of the joins between them**. Confidence in a knowledge base used for cross-cutting architecture decisions cannot exceed confidence in its weakest cross-cutting reasoning, and the cross-cutting reasoning between blocks is largely absent by construction (XB-01, XB-02). Three of the corpus's own deferrals resolve to files that either never pick them up or explicitly deny existing (XB-01, XB-08, XB-10).

---

## 3. Executive Assessment

**What this corpus is.** Individually, these are unusually disciplined research documents. They do the four things most technology research fails to do: they express findings as REQUIREMENT → CONSTRAINT → CONSEQUENCE chains rather than descriptions; they collect negative evidence deliberately and at length; they record Unknowns and Conflicts instead of resolving them silently; and they fence vendor-side positioning (the `MS-V` tag, with the standing rule that Logic Apps-team *capability* facts are usable and its *scale adjectives* are not). `performance-scale.md` §0 states the single most important epistemic fact in the whole domain — Microsoft publishes limits, not benchmarks, so a design that violates no documented limit is not thereby known to be fast. `licensing-cost.md` §0.2 refuses to treat Learn as authoritative on entitlement. Both are the right call and both are rare.

**What this corpus is not, yet.** It is not one knowledge base. It is three knowledge bases that share four ancestors (`platform-suitability.md`, `application-architecture.md`, `data-architecture.md`, `automation-architecture.md`) and cite each other zero times. The filename-citation matrix is perfectly block-diagonal: Block A → Block B: 0. Block A → Block C: 0. Block B → Block C: 0. And in every direction of reverse. Cross-area analysis sections exist — SECURITY↔GOVERNANCE, SECURITY↔ALM, GOVERNANCE↔ALM, PERFORMANCE↔COST, PERFORMANCE↔OPERATIONS, COST↔OPERATIONS — and every one of them is *within* a block. There is no A↔B, A↔C or B↔C cross-area analysis anywhere in the corpus.

**The mechanical proof of parallel isolation.** `operations-support.md` §9.3 defers governance, security operations and ALM to *"governance and security areas (not yet researched)"* and *"ALM area (not yet researched)"*. `licensing-cost.md` §10.3 defers environment strategy and DLP to *"governance area (not yet researched)"*. All eight files are dated **2026-09-03**. `security.md`, `governance.md` and `alm-devops.md` exist, are dated the same day, and answer precisely those topics — `alm-devops.md` ALM-22 even documents the deprecation of the ALM Accelerator that `operations-support.md` lists as unresearched. Block C did not merely omit citations to Block B; it recorded, in writing, that Block B does not exist. This one fact explains almost every other finding below.

**The consequence for the review question.** Asked directly — *can an architect use the combined research to reason from requirements to architecture without contradictory or incomplete guidance?* — the answer is **yes for a Power-Platform-only solution, and no for anything else.**

Five of Block A's ten patterns (AP-02 API-mediated, AP-04 Queue-based, AP-05 Hybrid, AP-08 Facade, AP-10 Enterprise boundary) require components outside Power Platform. For those five patterns the corpus provides: no governance model (`governance.md` mentions Azure zero times), no ALM treatment, essentially no cost basis (`licensing-cost.md` U-06 records gateway infrastructure cost as unknown and asks for *"cross-area with the integration work"* — which exists, unlinked), and no operations content (`operations-support.md` mentions gateway, Service Bus, APIM and dead-letter zero times each). Block A knows this is a problem and says so repeatedly — Y-13 rules that a pattern with no named operator is *unavailable, not merely expensive* — but the corpus cannot tell an architect what that operator costs, who governs them, or how their half is deployed and monitored.

**The three findings that would produce materially wrong work today.** (1) A security-driven design is under-costed by its largest line: `security.md` says the IP firewall's licence cost is *"often larger than the Power Platform cost itself"*, and `licensing-cost.md` contains the string "E5" zero times (XB-04). (2) Block A's universal seam artefact — the custom connector — is the artefact Block B documents as most ALM-hostile, including a workaround that deliberately creates an unmanaged layer inside a managed solution and thereby defeats the production-integrity control that two other findings depend on (XB-05). (3) Block C encodes as settled envelope values the two custom-connector figures Block A registers as CONFLICTED with an explicit *"Do not encode either figure without verification"*, one of them with a 20× spread (XB-07).

**What is genuinely absent rather than unlinked.** Most corrections below are joins, not new research. Three are not: an availability SLA percentage exists nowhere in the corpus and `operations-support.md` U-01 correctly calls this *"the largest weakness"*; the comparative economics of alternatives — the half of the platform decision that keeps the corpus rule *"Power Platform must NOT be assumed to be the answer"* operative — sits at LOW-MEDIUM confidence on unsourced inference; and governance of the non-Power-Platform estate has no evidence base at all.

**Verdict rationale.** The blocks are architecturally sound and epistemically honest. The failure is in the seams, and the seams are mostly closable by one bounded cross-block pass plus two targeted research items. That is the definition of PASS WITH CORRECTIONS — but the corrections in §17 marked **BLOCKING** must land before pack authoring begins, because a pack authored on the current corpus would ship a wrong cost model and a wrong ALM story for half its own pattern catalogue.

---

## 4. Critical Contradictions

### XB-01 — Block C states in writing that Block B has not been researched, on the same date Block B was written

**Severity:** CRITICAL

**Type:** CONTRADICTION

**Affected Areas:** whole corpus; all deferral routing; Areas 06/07/08 ↔ 09/10/11

**Evidence:**
- `operations-support.md` §9.3 *Where this file defers*: *"DLP policies, tenant governance, environment strategy as governance topics, security operations | **governance and security areas (not yet researched)**"* and *"ALM in depth (source control, branching, solution layering, ALM Accelerator) | **ALM area (not yet researched)** — this file covers only what pipelines and solutions impose on the operating model"*.
- `licensing-cost.md` §10.3: *"Environment strategy, DLP and tenant governance as governance topics | **governance area (not yet researched)**"*.
- `security.md` line 8, `governance.md` line 8, `alm-devops.md` line 8 all carry *"Draft date: **2026-09-03**"*. `performance-scale.md`, `licensing-cost.md`, `operations-support.md` all carry *"Research date: **2026-09-03**"*.
- `alm-devops.md` ALM-22 documents the ALM Accelerator deprecation that `operations-support.md` lists as unresearched.
- Block C contains **zero** references to "Area 06", "Area 07" or "Area 08". `security.md` §8 by contrast defers *forward* to *"Area 09 (Performance and Scale)"*, *"Area 10 (Licensing and Cost)"* and *"Area 11 (Operations and Support)"* — so Block B anticipated Block C, while Block C denied Block B.

**Why It Matters:** This is not a missing citation; it is false state information inside the corpus. A pack author following Block C's deferral map concludes that governance, security operations and ALM are open work and either re-researches them or, worse, authors pack content in those areas from Block C's incidental treatment — `operations-support.md` covers ALM only *"what pipelines and solutions impose on the operating model"*, which is a fraction of `alm-devops.md`'s four-rung ladder. It also establishes the mechanism behind XB-02 and most findings below: Blocks B and C were produced in parallel isolation with no reconciliation step, so every coupling that crosses that boundary is unexamined by construction.

**Required Correction:** Correct the three deferral rows to name the actual files and finding ids. Then run one reconciliation pass over every Block B ↔ Block C deferral in both directions, and record its completion in each file's header. Add a corpus-level manifest listing every file, its area number, its status and its date, so a "not yet researched" claim cannot survive a later file being written.

---

### XB-02 — The corpus has no A↔B, A↔C or B↔C cross-area reasoning, and the citation matrix is perfectly block-diagonal

**Severity:** CRITICAL

**Type:** GAP

**Affected Areas:** all seven review dimensions; the entire cross-cutting reasoning layer

**Evidence:** Filename-mention counts (row cites column), verified by grep over the eight files:

| cites → | integration-arch | arch-patterns | security | governance | alm-devops | performance-scale | licensing-cost | operations-support |
|---|---|---|---|---|---|---|---|---|
| integration-architecture | — | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| architecture-patterns | 25 | — | 0 | 0 | 0 | 0 | 0 | 0 |
| security | 0 | 0 | — | 7 | 10 | 0 | 0 | 0 |
| governance | 0 | 0 | 9 | — | 15 | 0 | 0 | 0 |
| alm-devops | 0 | 0 | 20 | 14 | — | 0 | 0 | 0 |
| performance-scale | 0 | 0 | 0 | 0 | 0 | — | 2 | 2 |
| licensing-cost | 0 | 0 | 0 | 0 | 0 | 3 | — | 3 |
| operations-support | 0 | 0 | 0 | 0 | 0 | 3 | 4 | — |

Every off-block cell is zero. The cross-area analysis sections are `security.md` §12 (SEC↔GOV, SEC↔ALM), `governance.md` §12 (GOV↔SEC, GOV↔ALM), `alm-devops.md` §12 (ALM↔GOV, ALM↔SEC), `performance-scale.md` §11 (PERF↔COST, PERF↔OPS), `licensing-cost.md` §10 (COST↔PERF, COST↔OPS), `operations-support.md` §9 (OPS↔PERF, OPS↔COST). Block A has no cross-area section at all — its §13 / §11 are evidence-quality notes. The only shared reference frame is the four ancestor files (PS / AA / DA / AT2), cited by all three blocks.

**Why It Matters:** The review model in the brief — REQUIREMENT → CONSTRAINT → ARCHITECTURAL CONSEQUENCE → SECURITY → GOVERNANCE → ALM → PERFORMANCE → COST → OPERATIONS → DECISION — is a chain that crosses all three blocks. The corpus supplies the chain in three disconnected segments. An architect can complete the chain for a Power-Platform-only workload because the ancestors carry enough shared ground. For a workload whose architecture crosses the platform boundary, the chain breaks after "architectural consequence" and every downstream stage must be reasoned from first principles by whoever reads the pack. This is the structural finding from which XB-04, XB-05, XB-06, XB-08, XB-10, XB-11 and XB-13 all follow.

**Required Correction:** Add a cross-block reconciliation artefact (one document, or one section per file) covering the nine missing pairings: A↔SEC, A↔GOV, A↔ALM, A↔PERF, A↔COST, A↔OPS, B↔PERF, B↔COST, B↔OPS. It should not restate findings; it should record, per pairing, the couplings, the contradictions, and the deferrals in both directions — the same discipline the intra-block §12 / §11 / §9 sections already demonstrate. That discipline exists in the corpus; it simply was not applied across blocks.

---

### XB-03 — `AP-nn` carries five different meanings, and `C-nn` / `U-nn` are file-local namespaces that collide in all eight files

**Severity:** CRITICAL

**Type:** SEMANTIC DRIFT

**Affected Areas:** every downstream artefact that consumes finding ids; traceability; pack authoring

**Evidence:**
- `architecture-patterns.md` §4: `AP-01`…`AP-10` are **architecture patterns**. `AP-01` = *Direct integration*.
- `performance-scale.md` §6: `AP-01`…`AP-18` are **anti-patterns**. `AP-01` = *"Non-delegable query over a large table"*.
- `licensing-cost.md` §5: `AP-01`…`AP-15` are **anti-patterns**. `AP-01` = *"Choosing the architecture by licence price"*.
- `operations-support.md` §5: `AP-01`…`AP-21` are **anti-patterns**. `AP-01` = *"No owner"*.
- Block A additionally maintains two *further* anti-pattern namespaces: `integration-architecture.md` §6 `X-01`…`X-18` (implementation anti-patterns) and `architecture-patterns.md` §7 `Y-01`…`Y-14` (pattern-selection anti-patterns), and §11.2 explicitly warns that *"conflating them would lose the distinction between choosing wrong and building wrong"*.
- `C-nn` and `U-nn` are file-local in all eight files, and the same underlying item carries different ids: `integration-architecture.md` C-04 == `architecture-patterns.md` C-01 (Power Automate scale positioning); `integration-architecture.md` U-22 == `architecture-patterns.md` U-03; `integration-architecture.md` U-14 == `architecture-patterns.md` U-11 (dual-write failure semantics); `performance-scale.md` C-01 == `licensing-cost.md` C-01 (two published PPR sets); `licensing-cost.md` C-03 == `operations-support.md` C-01 (managed environments "included" vs premium-required).
- Block C also cites `AP-nn` 19, 16 and 21 times respectively while citing `architecture-patterns.md` zero times — so the collision is live in the text, not merely latent.

**Why It Matters:** Three of the corpus's five citation-bearing namespaces are ambiguous. "AP-01" resolves to a recommended architecture in one file and to three different things-not-to-do in three others. A pack that ingests findings by id will silently mis-resolve; a human reading Block C's `AP-06` against Block A's `AP-06` gets *"Massive per-record loop in a flow"* where the corpus meant *Data virtualization*. Because `AP-nn` appears in Block C's anti-pattern tables — the most quotable content in those files — the failure mode is a pack rule that recommends an anti-pattern or forbids a pattern.

**Required Correction:** Assign each file a unique finding prefix and each *kind* of finding a unique prefix, corpus-wide, before any pack ingestion. Anti-patterns need distinct namespaces per file (e.g. `PF-AP-nn`, `LC-AP-nn`, `OP-AP-nn`) or a single corpus-wide anti-pattern register. Conflicts and Unknowns need file-qualified ids (`IA-C-01`, `PF-U-07`) and a corpus-level index that maps duplicate items to one canonical id. Add the id convention to `source-policy.md` so later files inherit it — Block A already publishes a per-file *"Id convention"* paragraph and its discipline should be lifted to corpus level.

---

### XB-04 — The external licence dependencies of Power Platform's strongest security controls are absent from the cost model, and one of them is stated to exceed the platform cost

**Severity:** CRITICAL

**Type:** GAP (with a contradiction in magnitude between two files)

**Affected Areas:** SECURITY ↔ COST; COST ↔ GOVERNANCE; TCO; every security-driven or compliance-driven design

**Evidence:**
- `security.md` SEC-27 (IP firewall), licensing clause: managed environments **plus** users holding *"Microsoft 365 or Office 365 A5/E5/G5"* or an M365 A5/E5/F5/G5 Compliance / F5 Security & Compliance / Information Protection and Governance / Insider Risk Management subscription. Decision impact, verbatim: *"'restrict to corporate network' is achievable for Dataverse, **at a licensing cost that is often larger than the Power Platform cost itself**"*.
- `security.md` SEC-29 (CMK): *"the same E5-class licence list as the IP firewall"*.
- `security.md` SEC-02: location/device/user-based Conditional Access for Power Apps and Power Automate *"requires Entra ID P1/P2"*, and *"Licensing dependency (P1/P2) is an architectural cost"*.
- `security.md` SEC-34: read and export logging *"requires activity logging into Purview"*, and *"The option to turn on activity logging is only visible when the minimum Microsoft Office licensing requirements are met"*.
- `security.md` §8 routes it explicitly: *"Licensing arithmetic of the E5-class prerequisites for IP firewall/CMK, and of managed environments → **Area 10 (Licensing and Cost)**; only the existence of the dependency is recorded here."*
- `security.md` §10: *"Several controls carry **licence dependencies outside Power Platform** (E5-class for IP firewall/CMK; Entra P1/P2 for Conditional Access; Purview for read auditing). **These belong in the financial lens**, not only the governance lens."*
- Term counts in `licensing-cost.md`: **"E5" = 0. "Entra ID P1"/"P2" = 0. "Purview" = 0.** "IP firewall" = 3, "CMK" = 3, "Conditional Access" = 1 — and all seven of those occurrences sit inside the single LC-23 quotation of the managed-environments feature list, i.e. costed as a Power Platform premium licence and nothing more.
- `licensing-cost.md` §2.5 / LC-21 enumerates the costs Microsoft *"states but does not price"*: non-production environments, monitoring, log storage and query, personnel, optimisation expertise, testing effort, support plans, Azure dependencies, governance tooling. The E5-class, Entra P1/P2 and Purview dependencies appear in none of them.

**Why It Matters:** For any workload with a network-restriction, customer-managed-key, immediate-revocation or read-audit requirement, the largest single cost line is an identity or compliance licence upgrade for the whole user population — and the file whose job is cost does not contain the word. `security.md` did the right thing: it identified the dependency, declined to do the arithmetic, and named the owner. The owner never received it (XB-01). The consequence is not a rounding error: an option compared on `licensing-cost.md`'s TCO model will show a security-hardened design as costing a premium Power Platform licence per user when the true increment may be an E5 upgrade per user. This is exactly the "hidden licensing/cost problem" the review brief asks for, and the corpus contains both halves of it.

**Required Correction:** `licensing-cost.md` must add the non-Power-Platform licence dependencies as first-class cost drivers, sourced from `security.md` SEC-02 / SEC-27 / SEC-29 / SEC-34 and re-verified against the Licensing Guide per its own §0.2 rule: E5-class prerequisites for IP firewall and CMK, Entra ID P1/P2 for Conditional Access, Purview licensing for activity logging. Each should carry the population-scope question ("which users must hold it?") because that is what makes it large. Add a cost decision criterion of the form *security control required → external licence prerequisite → population scope → cost*, mirroring the existing DC-11 criticality chain. `security.md` §8 should then cite the resulting `LC-nn` ids so the handoff is verifiable in both directions.

---

## 5. Major Contradictions

### XB-05 — The custom connector is Block A's universal seam and Block B's most ALM-hostile artefact; neither file says so

**Severity:** HIGH

**Type:** CONTRADICTION (unacknowledged incompatibility between a recommended structure and a documented lifecycle constraint)

**Affected Areas:** INTEGRATION ↔ ALM; INTEGRATION ↔ SECURITY; INTEGRATION ↔ OPERATIONS; patterns AP-02, AP-05, AP-08, AP-10

**Evidence:**
- Block A makes the custom connector the seam artefact for four of ten patterns. `architecture-patterns.md` AP-02 structure: *"Power Platform artefact → custom connector → APIM gateway (or a plain API) → backend service(s)"*. AP-05: *"The seam artefact is a custom connector (synchronous) or a queue (asynchronous)"*. AP-10 Risks: *"Power Platform artefacts see a custom connector over an API over a backend; three contracts must stay aligned"*. `integration-architecture.md` §4.2 and IA-49 name it as the mechanism for consuming a published contract, and §12.1 recommends it as the shape when integration is owned elsewhere.
- Block A's ALM vocabulary counts: *"connection reference"* — `integration-architecture.md` 2, `architecture-patterns.md` **0**. *"unmanaged layer"* — **0 / 0**. *"managed solution"* — **0 / 0**. *"restore"* — **0 / 0**. *"backup"* — **0 / 0**. *"block unmanaged"* — **0 / 0**.
- `alm-devops.md` ALM-14 (source D-16) documents four failure modes, verbatim: *"**Canvas apps don't recognize connection references on custom connectors.** To work around this limitation, after a solution is imported… the app must be edited to remove and then readd the custom connector connection. Note, if this app is in a managed solution, **proceeding to edit the app will create an unmanaged layer**"*; *"**Copy environment breaks connection references for custom connectors**"*; *"**Custom connectors need to be imported in a separate solution from their connection references**"*. Its own decision impact: *"custom connectors materially complicate ALM; the documented workaround for canvas apps deliberately creates an unmanaged layer in a managed solution — i.e. **the fix breaks the production-integrity rule** (ALM-03, ALM-15)"*.
- `alm-devops.md` ALM-18 and `operations-support.md` §6.2 items 47–48: after a restore, *"connection references require new connections"* and custom connectors may need to be *"delete[d] and reinstall[ed]"*.
- `security.md` SEC-19: the documented known issue where a secure implicit connection imported via a connection reference has *"the security… not set properly in the target environment"* — *"the control that protects production is established by the deployment, not by the app"*.
- The unmanaged layer that the ALM-14 workaround creates is precisely what `alm-devops.md` ALM-15 and `governance.md` lever 6 / GOV-15 exist to prevent; GOV-15's production support model (*"effectively read-only to them"*) depends on block-unmanaged-customizations being on.

**Why It Matters:** Block A escalates to an API-mediated, hybrid, facade or boundary pattern on well-evidenced grounds and hands the reader a custom connector. Block B establishes that this artefact breaks canvas connection references, cannot survive an environment copy, must be split into its own solution, needs deletion and reinstallation after a restore, can silently lose a security control in transit, and has a documented workaround that defeats the strongest production-integrity control in the platform. None of that appears in Block A's *Operational implications*, *Security implications*, or anywhere in either Block A file. An architect selecting AP-02 from Block A inherits an ALM problem the corpus documents in full and never connects.

**Required Correction:** Add the custom-connector ALM consequences to `architecture-patterns.md` as an explicit precondition and cost on AP-02, AP-05, AP-08 and AP-10, citing `alm-devops.md` ALM-14 / ALM-15 / ALM-18 and `security.md` SEC-19. Add the reciprocal note in `alm-devops.md` ALM-14 naming the patterns that depend on the artefact. Where the workaround conflicts with block-unmanaged-customizations, record it as a **decision boundary**, not a footnote: either the pattern uses a queue seam rather than a connector seam, or the production-integrity control is relaxed for that environment and the residual is accepted.

---

### XB-06 — Five of Block A's ten patterns require a non-Power-Platform estate for which the corpus has no governance, ALM, cost or operations evidence

**Severity:** CRITICAL

**Type:** GAP

**Affected Areas:** INTEGRATION ↔ GOVERNANCE; INTEGRATION ↔ ALM; INTEGRATION ↔ COST; INTEGRATION ↔ OPERATIONS; patterns AP-02, AP-04, AP-05, AP-08, AP-10

**Evidence:** Term counts across Blocks B and C:

| term | security | governance | alm-devops | performance-scale | licensing-cost | operations-support |
|---|---|---|---|---|---|---|
| gateway | 10 | **0** | **0** | 2 | 4 | **0** |
| Service Bus | **0** | **0** | **0** | 5 | **0** | **0** |
| API Management / APIM | **0** | **0** | **0** | 1 | **0** | **0** |
| dead-letter | **0** | **0** | **0** | **0** | **0** | **0** |
| dual-write | **0** | **0** | **0** | **0** | **0** | **0** |
| virtual table | 1 | **0** | **0** | **0** | **0** | **0** |
| webhook | 1 | **0** | **0** | 3 | **0** | 1 |

`governance.md` additionally contains **"Azure" 0 times**, "on-premises" 0 times, "custom connector" 2, "integration" 3. Its seven governance levers (§1) are all tenant-internal Power Platform configuration: environment topology, managed environments, environment groups, data policies, sharing limits, solution-checker/block-unmanaged, ownership-inventory-actions.

Block A demands exactly the governance and operations this evidence does not exist for:
- `integration-architecture.md` §2.1 row 11: *"Every integration stream needs three named owners (data, endpoint, pipeline) recorded as a decision. An integration whose throughput depends on an individual's personal licence is not production-grade."*
- IA-29: a private-connectivity requirement *"must be costed as a joint Power Platform + network engineering workstream with named owners"*.
- IA-27 / §7 items 28–29: gateway estate for business-critical use is *"≥ 2 nodes per cluster, separate dev and prod clusters, 8 GB RAM minimum per node, recovery-key custody 'a significant business risk'"*, and *"Microsoft doesn't investigate poor performance when a gateway … is overloaded"*; VNet requires an Azure subscription linked to the tenant, subnet delegation in both paired regions, 25–30 production IPs, one dedicated subnet per enterprise policy.
- `architecture-patterns.md` Y-13: *"Adopting a pattern with no operator — AP-04, AP-05 or AP-10 without a named team for the non-Power-Platform half"* → corrective: *"Treat 'no operator' as making the pattern **unavailable**, not merely expensive."*
- Y-12: *"Assuming Azure is the boundary — standing up APIM beside an existing enterprise integration platform"*.
- `licensing-cost.md` U-06, verbatim: *"Cost of on-premises data gateway infrastructure at scale (hosts, clustering, HA) | A real cost line for any on-premises integration, **absent from every fetched page** | Gateway sizing documentation; **cross-area with the integration work**"*.

**Why It Matters:** Half the pattern catalogue is unreviewable against five of the seven dimensions the brief requires. The corpus can route a requirement to AP-04 with well-sourced justification and then cannot say who governs the broker, how the worker is deployed and rolled back, what the Azure estate costs, who is paged when the dead-letter queue fills, or how the two halves are correlated. Block A is honest about the existence of this cost — *"a hop, a bill and a team"*, *"two operating models… two on-call rotations"* — but a decision-support pack needs the content, not the acknowledgement. The `licensing-cost.md` U-06 entry is the sharpest illustration: the cost is recorded as unknown and routed to "the integration work", and the integration work contains the full sizing requirement, unlinked.

**Required Correction:** Two actions, one cheap and one not. (1) **Linkage, immediately:** connect `licensing-cost.md` U-06 to `integration-architecture.md` IA-27 / IA-29 / §7 items 28–29, which supply the sizing basis the unknown asks for; connect `architecture-patterns.md` Y-13 to `operations-support.md` §1.1's maturity classes and OP-05's ownership cascade, which is the same argument from the operations side. (2) **New research, scoped:** a governance and operations treatment of the non-Power-Platform half — ownership and change control for APIM/broker/Function/gateway assets, their deployment lifecycle relative to the Power Platform solution, and their cost basis. Until (2) exists, the pack must mark AP-02, AP-04, AP-05, AP-08 and AP-10 as carrying an **unquantified** operating-model cost, and Y-13's "unavailable without an operator" must be encoded as a hard precondition rather than advice.

---

### XB-07 — Block C encodes as settled the two custom-connector figures Block A registers as CONFLICTED and do-not-encode

**Severity:** HIGH

**Type:** CONTRADICTION

**Affected Areas:** INTEGRATION ↔ SCALE; every API-mediated or hybrid design; sizing arithmetic

**Evidence:**
- `performance-scale.md` §2 meter map, meter 3: *"SharePoint 600/60 s; **custom 500/min**"*. §3.C row 29: *"Custom connector rate | **500 requests/min per connection; 50 connectors/user** | CONDITIONAL — and requires premium licensing (→ LC)"*. PF-27 evidence quotes source P-16, `ms.date` 2026-07-17: *"Number of requests per minute for a custom connector | 500 requests per minute per connection"* and *"Number of custom connectors | 50 per user"*. No conflict is registered; §9 of that file records C-01…C-04 and none concerns the custom connector.
- `integration-architecture.md` C-01: *"**Custom connector requests per minute per connection: 500 or 10,000?**"* — Source A (I-13, the same limits page, `ms.date` 2026-07-17) says 500; Source B (I-08, Custom connector FAQ, `ms.date` 2025-03-13) says *"10000 requests for each connection created by the connector"* for Power Automate and Power Apps. Status: *"**CONFLICTED. Do not encode either figure without verification.**"* U-02: *"20× sizing error risk on the main extensibility mechanism."* Decision impact: *"A design sized at 10,000/min that is actually capped at 500/min fails by a factor of twenty."*
- `integration-architecture.md` C-02 (RESOLVED) and IA-13 establish that the **count** is licence-conditional, not 50: *"Free plan: one; **Office 365 and Dynamics 365 plans: one**; Per user plan: 50"*, with the consequence *"on seeded Microsoft 365 rights the count is **one**"* and *"An API-per-capability strategy implemented as one custom connector per API hits a per-user ceiling, and on Microsoft 365 / Dynamics 365 seeded rights the ceiling is one."*

**Why It Matters:** Two distinct defects. First, an **epistemic** contradiction: the same figure from the same page on the same date is a do-not-encode conflict in one file and a settled envelope value in the file whose tables a pack would encode. Block C never fetched I-08 and so never saw the 10,000 figure; nothing in Block C signals that the number is disputed. Second, a **substantive** error: "50 connectors/user" is the per-user-plan case presented as general, and the commonest enterprise licence position is one. That inverts an architecture decision — Block A concludes that a low connector ceiling *pushes designs toward one connector fronting many operations, which is an argument for a real API gateway*. A pack built on Block C's row 29 would size a connector-per-capability estate that the licence forbids.

**Required Correction:** `performance-scale.md` must either register the 500-vs-10,000 conflict and mark row 29 CONFLICTED, or carry the resolution once `integration-architecture.md` U-02 is closed — the two files must not hold different epistemic states for one number. The count must be restated as licence-conditional per IA-13 / C-02, not as 50. Add a corpus-level rule: a figure registered as CONFLICTED in any file is CONFLICTED corpus-wide until resolved, and the resolution is recorded once. This is the general remedy for XB-03's duplicate-conflict problem as well.

---

### XB-08 — The performance cost of the security model is deferred in a circle and answered nowhere

**Severity:** HIGH

**Type:** GAP

**Affected Areas:** SECURITY ↔ SCALE; Dataverse authorization design; SEC-10, SEC-11, SEC-12, SEC-13

**Evidence:**
- `security.md` §8 defers: *"Delegation/query behaviour of security filters at scale (performance of BU/team/sharing models) → **Area 09 (Performance and Scale)**; S-02 warns that sharing and excessive column security 'add overhead'."*
- `security.md` SEC-12 (source S-02, Microsoft): sharing *"should be an exception… because it's a less performant way of controlling access"*. SEC-13: *"Column-level security should be used as needed and not excessively as it can add overhead that is detrimental if over used"*.
- `performance-scale.md` §8.3 *What negative evidence is still missing*: *"No Microsoft statement on the performance cost of security-model complexity (row-level sharing volume, hierarchy depth) — `data-architecture.md` carries the PrincipalObjectAccess storage angle but **not a latency figure** (U-07)."*
- `performance-scale.md` U-07: *"Performance cost of Dataverse security-model complexity (sharing volume, hierarchy depth, business-unit count) at scale | A common real-world cause of degradation; `data-architecture.md` covers storage but not latency | **Cross-area work with DA**; Microsoft engagement."*
- Term counts in `performance-scale.md`: *"security filter"* 0, *"column security"* 0, *"security role"* 0, *"business unit"* 2 (neither about performance). The file does not name `security.md` and does not know the question was routed to it.

**Why It Matters:** `security.md` recommends the group-team pattern (SEC-11), modernised business units for matrix access (SEC-10) and column-level security with masking (SEC-13/SEC-14), and Microsoft's own text attaches an unquantified performance penalty to two of them. The question goes to Area 09, which records it as an unknown and redirects it to `data-architecture.md`, which — per Area 09's own words — has storage and not latency. The chain terminates without an answer and without either end knowing the other participated. Security-model complexity is one of the commonest real-world causes of Dataverse degradation, and a pack authored now would recommend the patterns with no way to bound their cost.

**Required Correction:** Close the loop explicitly. `performance-scale.md` U-07 should name `security.md` SEC-10 / SEC-11 / SEC-12 / SEC-13 as the requesting findings and record that the answer is **not available from Microsoft documentation**, so the design consequence is a *validation obligation* rather than a threshold: any BU/team/sharing-heavy model must be volume-tested against representative row and share counts before commitment. `security.md` should carry the reciprocal statement so a reader of SEC-10 knows the migration programme's performance impact is unquantified. This is a case where the honest correction is to convert a dangling deferral into a stated Unknown with a named validation action, not to invent a figure.

---

### XB-09 — Three files give three incompatible positions on how a design is validated, and Block A prescribes tests the platform has no harness for

**Severity:** HIGH

**Type:** CONTRADICTION

**Affected Areas:** ARCHITECTURE ↔ ALM; ARCHITECTURE ↔ SCALE; ARCHITECTURE ↔ OPERATIONS; every pattern's validation step

**Evidence:**
- Block A prescribes testing as the validation route. `architecture-patterns.md` §11.2: *"for AP-01, volume-test at projected peak frequency…; for AP-04, load-test the leveling and monitor queue and dead-letter depth…; for AP-02/AP-08, load-test the gateway to avoid cascading failure…; for AP-07, prove the reconciliation pass actually converges"*. AP-02 Risks quotes Microsoft: *"Perform load testing against the gateway to ensure that you don't introduce cascading failures for services"*. `integration-architecture.md` X-15 corrective: *"Volume-test at projected peak frequency, not at test-data volume"*.
- `alm-devops.md` ALM-17: *"**Effective April 2026, Test Engine is deprecated. The documentation and GitHub repository are no longer maintained by Microsoft**"*; *"there is no supported first-party low-code functional test framework"*; solution checker *"is explicitly not a test"*; pipelines give prevalidation of dependencies and configuration *"but no functional testing"*; the documented guidance requires a test environment for end-to-end validation, *"i.e. manual by default"*. Decision impact: *"any requirement for automated regression testing forces pro-dev capability (Playwright, custom harnesses) and a budget line."*
- `performance-scale.md` PF-15 / B-17 / DC-17 take a third position: Microsoft *constrains* load testing — *"Limit tests to avoid unintended consequences"*; no concurrent-user figure is published; *"Peak confidence comes from limit arithmetic + a bounded pilot + production throttling monitoring + a degradation plan — **not from a load test**"*; and B-17 makes it an out-of-platform boundary: *"A workload whose peak is validated only by full-scale load testing against the production service… the design must be provable from limits, or hosted where load testing is permitted."* Its own C-03 records the underlying documentation conflict as unresolved.
- `operations-support.md` C-03 adds a fourth constraint: PE:05 requires mirroring production, but managed-environment behaviour exists only in managed environments while pipelines permit non-managed development environments — *"some production behaviour is only testable at extra cost"*, marked **unresolved**.
- Block A term counts: *"Test Engine"* 0, *"Playwright"* 0 in both files.

**Why It Matters:** Validation is the last stage of the review model and the corpus disagrees with itself about whether it is possible. Block A's validation instructions are not executable as written: there is no supported low-code functional test framework, Microsoft constrains the load testing Block A prescribes, and Block C's own position is that peak confidence must come from limit arithmetic and production monitoring rather than a test. Nobody costs or owns the test capability the architecture depends on, and `alm-devops.md` is explicit that supplying it *"forces pro-dev capability… and a budget line"*. A pack that carries Block A's validation column will instruct engagements to do something the corpus elsewhere says they cannot.

**Required Correction:** Reconcile the three positions into one validation model, stated once. It should distinguish: what is provable from published limits (the majority, per `performance-scale.md` §0); what requires a bounded pilot with production monitoring and a degradation plan (per PF-15 / DC-17); what requires a genuine test harness and therefore a pro-dev budget line (per ALM-17); and what is not testable without a managed test environment (per `operations-support.md` C-03). Block A's per-pattern validation instructions must then be rewritten against that model, and any residual load-testing instruction must carry `performance-scale.md`'s constraint. Where the three sources genuinely conflict, keep it CONFLICTED — `performance-scale.md` C-03 already does, and that treatment should be adopted corpus-wide rather than contradicted by Block A's confident instructions.

---

## 5.4 Contradiction candidates examined and **rejected**

Recorded so they are not re-raised. Per the brief, evidence must actually conflict.

1. **Managed-environment dates.** Not a contradiction. February 2026 = Microsoft begins auto-enabling managed environments on pipeline *target* environments (`alm-devops.md` ALM-10 / D-06; `operations-support.md` O-06; `licensing-cost.md` §7.2 item 36). February 2027 = licence enforcement blocks users without a qualifying licence from *opening apps* in a managed environment (`governance.md` GOV-11 / G-11; `alm-devops.md` D-22; `security.md` §12.1). Two distinct dated events, consistently reported in all five files that mention them. `governance.md` GOV-C2 correctly frames the real tension (Microsoft recommends managed environments broadly while every active user needs a premium licence) as a genuine trade-off rather than a documentation defect.

2. **"Managed environments are included as an entitlement" vs "premium licences required".** Not a contradiction, and both `licensing-cost.md` C-03 and `operations-support.md` C-01 resolve it identically and correctly: the *feature* costs nothing extra, but every user of the environment must hold a qualifying standalone licence. Both files record it precisely because *"included as an entitlement"* is routinely misread as free. This is the corpus working as intended.

3. **Power Automate's scale positioning.** Not an unresolved contradiction. `integration-architecture.md` C-04 and `architecture-patterns.md` C-01 both register Microsoft's *"Scales well for most business scenarios"* against the Logic Apps team's *"Small to medium scale workflows"*, tag the latter `MS-V`, and resolve it the same way: **encode neither adjective**; encode the documented limits and escalation conditions. `automation-architecture.md` C-03 is the same conflict, carried forward with attribution. This is the corpus's best example of vendor-side positioning being fenced rather than absorbed, and it should be preserved as a model.

---

## 6. Critical Gaps

### XB-10 — No availability SLA exists anywhere in the corpus, and RTO/RPO figures are the only availability numbers on offer

**Severity:** CRITICAL

**Type:** GAP

**Affected Areas:** AVAILABILITY across all seven dimensions; mission-critical suitability; any commitment made to a business sponsor

**Evidence:**
- `operations-support.md` §6.6: *"**No published availability SLA percentage** for Power Platform services was located in this pass. The Online Services SLA and the Product Terms were not retrieved (**U-01**) — a material gap, because an availability commitment to the business cannot be sourced without it."*
- `operations-support.md` §10: *"**The availability SLA gap is the largest weakness.** … Any gate on this area should require the Microsoft Online Services SLA / Product Terms to be fetched, because an availability commitment to a business cannot otherwise be sourced. **RTO/RPO figures (PF-40) are *not* an uptime SLA and must not be presented as one.**"*
- The only availability figures in the corpus are `performance-scale.md` §3.D: in-region RPO *"approximately near zero"*, RTO *"under five minutes"*, cross-region RTO **UNPUBLISHED** (*"Microsoft doesn't publish a cross-region RTO commitment"*).
- Verified by grep: no *"99.9"*, *"99.99"*, *"uptime SLA"* or *"availability SLA"* claim appears anywhere in the eight files.
- Block A asks the question it cannot answer: `integration-architecture.md` §2.1 row 10 — *"What is the availability of the *weakest link in the integration path*, including the parts the customer operates?"* — and IA-27/IA-28 establish that introducing a gateway *"converts a SaaS availability profile into a customer-operated one"*.
- `operations-support.md` §1.1 makes *"24×7 expectation, RTO/RPO commitments, drills, incident command"* the defining characteristic of the mission-critical class.

**Why It Matters:** The corpus defines a mission-critical maturity class, gates architecture and licensing decisions on it, and cannot source the one number a sponsor will ask for. The risk is not the absence — the corpus is honest about it — but the substitution: RTO/RPO are conveniently available, sit in a table headed *Availability layer*, and will be lifted into an availability commitment by anyone who does not read `operations-support.md` §10. `operations-support.md` anticipates exactly this and warns against it, from a file Block A and Block C's other members never cite.

**Required Correction:** Retrieve the Microsoft Online Services SLA / Product Terms and reconcile against `operations-support.md` OP-19 and `performance-scale.md` §3.D — `operations-support.md` already names this as a mandatory gate condition and it should be treated as blocking. Until then, encode the prohibition as a corpus-level rule, not a per-file note: **no availability commitment may be derived from RTO/RPO figures**. The pack must carry the distinction between recovery objectives and an uptime commitment as an explicit constraint, because it is the single most likely place for a research gap to become a contractual error.

---

### XB-11 — Comparative economics of the alternatives — the half of the platform decision that keeps the corpus rule operative — is the least-evidenced section in the corpus

**Severity:** HIGH

**Type:** WEAK EVIDENCE

**Affected Areas:** COST; platform-suitability decision; the corpus's own core rule

**Evidence:**
- `../README.md` core rule: *"Power Platform must NOT be assumed to be the answer"*, and the research must identify *"what alternatives should be considered"*.
- `licensing-cost.md` §6 *Economic comparison with alternatives* compares custom development, Azure services, SaaS, an existing enterprise platform and other low-code platforms. Its own classification: *"**Origin:** INF (the Power Platform column is MS-sourced; the comparators are not priced in this pass) · **Confidence:** LOW-MEDIUM — see U-04"*. Four of the five rows carry *"— **U-04**"* against their evidence basis, three of them with the note *"unsourced on the custom side"*, *"the Azure side is not priced here"*, *"no comparative source fetched"*.
- `licensing-cost.md` U-04: *"§6's comparator columns are unsourced inference, so the crossover points are **directional only**"*, with the remedy *"Fetch pricing for the named alternatives; or **reframe §6 as a *method* for comparison rather than a comparison**"*.
- `licensing-cost.md` §7.3 item 51: *"**Gap** — No independent comparative TCO study of Power Platform against named alternatives was found in this pass."*
- The rest of the platform decision is distributed: `platform-suitability.md` owns the fit verdict (outside this review's scope, self-declared MEDIUM); `integration-architecture.md` §12 supplies nine integration-side EXTERNAL conditions at HIGH confidence per condition; `performance-scale.md` §4.3 supplies four out-of-platform boundaries. Only the economics is LOW-MEDIUM.

**Why It Matters:** A decision-support pack must answer *should we use this platform*, and cost is normally the deciding input once fit is established. The corpus's capability boundaries are strong — Block A §12 and `performance-scale.md` §4.3 are genuinely usable — but the economic crossover rests on inference against unpriced comparators. That is the one place where the corpus rule could quietly invert: an architect with a strong capability case and a directional-only cost case will default to the platform. `licensing-cost.md` names the honest fix itself.

**Required Correction:** Take `licensing-cost.md`'s own second option and reframe §6 as a comparison **method** — the questions, the units, the crossover drivers — rather than a comparison with filled-in verdicts, unless comparator pricing is actually fetched. The one durable finding in §6 should be preserved and promoted, because it survives price movement: *"Power Platform's cost scales primarily with **people**, and secondarily with **actions** and **stored bytes**. Alternatives scale primarily with **compute, transactions or build effort**… the crossover is driven by the ratio of users to work."* Mark every comparator verdict as requiring per-engagement pricing, and route it to the same validation owner as LC-02's entitlement questions.

---

## 7. Major Gaps

### XB-12 — Correlation across service boundaries is prescribed by Block A and documented as experimental and custom-connector-only by Block C

**Severity:** HIGH

**Type:** CONTRADICTION

**Affected Areas:** INTEGRATION ↔ OPERATIONS; patterns AP-03, AP-04, AP-05; IA-47's status resource

**Evidence:**
- `architecture-patterns.md` AP-05 *Operational implications*: *"Requires telemetry on both halves and **a correlation identifier across the seam**"*. `integration-architecture.md` IA-47 requires every asynchronous integration to define a status entity with *"correlation id, state, attempt count, last error, timestamps"*.
- `operations-support.md` OP-03 quotes Microsoft requiring it: *"**Include a correlation ID that flows across service boundaries.**"* — and immediately records the platform reality: *"Power Platform's own correlation capability is **experimental and limited to custom connectors** (OP-11)."*
- `operations-support.md` §6.1 item 29: *"Unhandled-error reporting and correlation tracing are **experimental** — *'not meant for production use'*"*. Item 30: *"Correlation tracing works **only with custom connectors**. Other connector types aren't supported."*
- `operations-support.md` §6.1 items 1–3: flow telemetry export is *"managed environments only"*, *"not 100% lossless"*, and unavailable in sovereign clouds.

**Why It Matters:** For AP-03 (event-driven) and AP-04 (queue-based) the seam is a broker, not a custom connector, so the platform's own correlation tracing does not apply — and for any pattern it is experimental and explicitly not for production. Block A prescribes a capability the corpus documents as unavailable in exactly the cases where multi-hop diagnosis matters most. Since AP-04 is Block A's recommended answer to durability, ordering, spike absorption and poison-message handling, this affects the pattern the corpus most often escalates to.

**Required Correction:** State the correlation constraint once, in Block A's pattern operational implications and in `operations-support.md` OP-03, with the honest consequence: correlation across a Power Platform ↔ broker seam must be **hand-built** (a correlation id carried in the message envelope and written to the status resource of IA-47, emitted to a shared sink from both halves), and its cost belongs in the pattern. Remove any implication that the platform supplies it.

---

### XB-13 — The pattern catalogue evaluates three of the seven required dimensions, and the selection matrix has no cost, ALM or maturity row

**Severity:** HIGH

**Type:** GAP

**Affected Areas:** ARCHITECTURE ↔ COST; ARCHITECTURE ↔ GOVERNANCE; ARCHITECTURE ↔ ALM; all ten patterns

**Evidence:**
- Mechanically verified: all ten patterns in `architecture-patterns.md` §4 carry exactly these fields — *Problem solved*, *Appropriate conditions*, *Architectural structure*, *Strengths*, *Weaknesses*, *Risks*, **Operational implications**, **Security implications**, **Scalability implications**, *When NOT to use*, *Alternatives*, *Evidence*. **No pattern carries a Cost implications, Governance implications or ALM implications field.**
- Prose counts inside the catalogue (lines 132–776): *cost* 32, *licen* 9, *premium* 6, *bill* 1, *ALM* 2, *governance* 15, *"connection reference"* **0**, *"managed environment"* **0**.
- §5 *Pattern selection matrix* is 30 requirement rows × 10 patterns. There is no row for cost or budget envelope, deployment maturity, operational maturity, or the licence profile of the user population. Row 30 (*"Governance across many makers and artefacts"*) is the only governance row. The only cost handling is a reading note above the matrix: *"Where the only STRONG is AP-05, AP-07 or AP-10, the requirement carries an operating-model cost that belongs in the option."*
- Cost is present but unstructured and unquantified: *"A hop, a bill and a team"* (AP-02), *"Storage cost. The copy consumes the Dataverse database meter"* (AP-07), *"More components, more cost"* (AP-09), *"Boundary controls are Managed-Environments-gated… which requires every active user to hold a premium licence"* (AP-10, sourced to DA-55/PS-33 rather than to `governance.md` GOV-11 or `licensing-cost.md` LC-23).

**Why It Matters:** The brief's §17 test is that a pattern must not appear recommended because its technical structure works. Block A applies that test rigorously on three dimensions and not at all on three others, in a file whose §5 matrix is the most directly encodable artefact in the corpus. A pack that ingests the matrix selects patterns without cost, governance burden or ALM burden being visible, and Block A's mitigating reading note is a sentence a machine will not carry. AP-10 is the clearest case: it is the pattern with the largest governance and cost consequence, it is self-flagged as the weakest-evidenced (U-08, *"AP-10 is synthesis"*), and its governance and cost content is two prose clauses sourced to files outside its own block.

**Required Correction:** Add *Cost implications*, *Governance implications* and *ALM implications* as required fields on all ten patterns, populated from `licensing-cost.md`, `governance.md` and `alm-devops.md` — the content largely exists and needs linking (LC-03 premium boundary, LC-23 managed-environment gating, GOV-11 licence enforcement, ALM-10 pipeline limits, ALM-14 connection references, ALM-18 no rollback). Add matrix rows for budget constraint, deployment maturity, operational maturity and licence profile of the user population, so that "no operator" and "no pro-dev budget" appear as verdict-changing requirements rather than as a reading note.

---

### XB-14 — Governance of the non-Power-Platform estate does not exist as a lever

**Severity:** HIGH

**Type:** GAP

**Affected Areas:** INTEGRATION ↔ GOVERNANCE; maker vs IT responsibility; API and connector governance; ownership

**Evidence:** `governance.md` §1's seven levers are environment topology, managed environments, environment groups and rules, data policies, sharing limits, solution-checker plus block-unmanaged-customizations, and ownership/inventory/actions. All seven configure Power Platform. Term counts: *"Azure"* **0**, *"gateway"* **0**, *"API Management"* **0**, *"Service Bus"* **0**, *"on-premises"* **0**, *"custom connector"* 2, *"API"* 4. GOV-11b covers connector governance in the DLP/ACP sense and records that *"ACP does not cover custom or HTTP connectors"* — the two mechanisms Block A relies on most. `governance.md` §4 row 6 (*"Bespoke API integration"*) resolves to *"Custom-connector governance stays on classic policy + endpoint filtering + target-side control"*, i.e. to controls `security.md` SEC-25 documents as not enforced for dynamic endpoints.

Against this, `integration-architecture.md` §12.1 states the governance failure mode the corpus is meant to prevent: skipping the ownership question produces *"business-critical integrations owned by a maker, throttled by a personal licence (IA-16, AT2-01), monitored through a portal (X-18), and **invisible to the team that owns integration**"*.

**Why It Matters:** This is the review brief's §2 test — *identify cases where Power Platform is implicitly being used as an enterprise integration platform without acknowledging governance requirements*. Block A passes that test on its own terms: it asks the ownership question first (§2.2 step 1), names the anti-pattern (X-01, Y-12), and makes an absent operator disqualifying (Y-13). What is missing is the other half: the corpus asserts a governance requirement for the external estate and provides no model for it — no maker/IT responsibility split for the non-Power-Platform half, no API governance, no gateway-estate governance, no change control for a service whose contract Power Platform consumes.

**Required Correction:** Extend `governance.md` with an eighth lever covering the non-Power-Platform estate, or state explicitly that it is out of scope and name the owner. Either is acceptable; silence is not, because Block A's decision boundaries already depend on it. At minimum, connect `governance.md` §4 row 6 to `integration-architecture.md` §12.1 and `architecture-patterns.md` Y-12/Y-13, and record the ACP custom/HTTP gap (GOV-11b, SEC-24) as a governance constraint on the API-mediated patterns specifically.

---

### XB-15 — Transactions are architecturally well covered and have no security, governance or ALM treatment

**Severity:** MEDIUM

**Type:** GAP

**Affected Areas:** TRANSACTIONS ↔ SECURITY / GOVERNANCE / ALM

**Evidence:** `integration-architecture.md` IA-19/IA-20/IA-21 and §12.3 establish the atomicity boundary decisively — atomicity stops at the Dataverse boundary; `$batch` change sets are Dataverse-only with a 1,000-request cap and abort-on-first-error by default; synchronous webhooks are a documented dual-write hazard; no saga or compensating-transaction construct exists in Power Platform (`architecture-patterns.md` §8 item 28). `performance-scale.md` contributes the plug-in service-protection exemption (PF-22, B-09) and batch sizing (PF-23). But: a compensating design implies a reversal path with its own authorization question, and `security.md` has no treatment of authorization across a multi-system unit of work; `governance.md` has no ownership model for a compensation process; `alm-devops.md` has no treatment of deploying a compensating flow and its reconciliation job as a coupled unit. `integration-architecture.md` U-14 (dual-write failure semantics) is self-marked *"**Material.** A dual-write decision cannot be made responsibly without this"* and remains open, with *"dual-write"* appearing **0 times** in Blocks B and C.

**Why It Matters:** The corpus tells an architect that multi-system atomicity is unavailable and that the remedy is compensation plus reconciliation. It does not say who is authorized to run a compensation, who owns the reconciliation job, or how the two halves are deployed together. For a financial or regulated process — precisely where the requirement arises — those are the questions a reviewer will ask.

**Required Correction:** Add the security, governance and ALM consequences of the compensating-transaction and reconciliation shape: the identity that performs a reversal and its privilege, the ownership of the reconciliation job, and the deployment coupling between the forward path, the compensation and the reconciliation. Close U-14 or mark it decision-blocking in the pack, since Block A already grades it material.

---

### XB-16 — Recovery is absent from Block A: no pattern accounts for backup, restore or the absence of rollback

**Severity:** MEDIUM

**Type:** GAP

**Affected Areas:** RECOVERY ↔ ARCHITECTURE; patterns AP-02, AP-04, AP-05, AP-07, AP-10

**Evidence:** Block A term counts: *"restore"* 0 / 0, *"backup"* 0 / 0, *"rollback"* 1 / 4. Against this, `alm-devops.md` ALM-18 establishes that *"there is no rollback"* and documents restore's side effects: solution flows deleted and turned off, *"connection references require new connections"*, custom connectors possibly *"delete[d] and reinstall[ed]"*, *"apps shared with Everyone aren't shared with Everyone"*, canvas app IDs change, restore cannot target production directly, managed-to-managed only, CMK and VNet parity required. `operations-support.md` §6.2 lists 21 restore constraints. `licensing-cost.md` LC-10: storage overage *"blocks environment create, copy, restore, recover"* — *"a capacity problem discovered during an incident is a recovery problem"*.

**Why It Matters:** A replication pattern (AP-07), a hybrid (AP-05) or a boundary architecture (AP-10) has a recovery story that spans Power Platform and at least one external store, and restoring one side without the other is a divergence event. Block A's synchronization risk register (§8) covers duplicate processing, lost updates, ordering and backlog but not recovery-induced divergence. The corpus has all the constraints and never applies them to a pattern.

**Required Correction:** Add recovery to each pattern's implications: what a Power Platform restore does to the pattern's external half, and whether the two halves can be recovered to a consistent point. Add a row to `integration-architecture.md` §8's synchronization risk register for restore-induced divergence, citing ALM-18 and `operations-support.md` §6.2.

---

## 8. Cross-Block Findings

The nine pairings absent from the corpus (XB-02), with what the corpus *does* contain on each and what is missing. This is the work list for the reconciliation pass.

| Pairing | Present | Missing |
|---|---|---|
| **A ↔ SECURITY** | `integration-architecture.md` §5.7 covers identity, secrets and authorization *"only where they change the integration topology"*, deliberately. IA-31/SEC-06 and IA-28/SEC-30 independently establish the same facts | Reciprocal citation; SEC-07's three-consumer Key Vault limit (canvas apps cannot read a secret) never reaches AP-01/AP-02; SEC-24's ACP custom/HTTP gap never reaches the API-mediated patterns; SEC-25's dynamic-endpoint non-enforcement never reaches IA's HTTP/custom-connector mechanisms |
| **A ↔ GOVERNANCE** | Block A asks the ownership question first and disqualifies operator-less patterns (Y-13) | Any governance model for the external estate (XB-14); "count pipelines as a governance metric" (IA X-01) has no lever in `governance.md`; the DLP/ACP posture is never applied to a pattern verdict |
| **A ↔ ALM** | Nothing beyond AP-02/AP-05's *"deployment coupling"* clause | The whole of it (XB-05): connection references, solution boundaries, publisher, no-rollback, restore effects, test harness (XB-09) |
| **A ↔ PERFORMANCE** | Strong overlap through the shared AT2/DA/PS ancestors; both files carry the three/five-meter model consistently | The custom-connector conflict is held at two different epistemic states (XB-07); `performance-scale.md` §11.3 routes broker and idempotency questions to `automation-architecture.md`, bypassing Block A entirely |
| **A ↔ COST** | Qualitative only: *"a hop, a bill and a team"*; IA U-22 / AP U-03 ask whether an APIM-fronted connector meters differently | No cost field on any pattern (XB-13); gateway and VNet infrastructure cost is an open unknown that Block A can source (XB-06) |
| **A ↔ OPERATIONS** | IA-45/IA-47 (throttle-rate monitoring, status resource) and AP's per-pattern *Operational implications* are genuinely good | Correlation contradiction (XB-12); no operations content for broker, gateway, APIM or dead-letter (XB-06); `operations-support.md` OP-05's ownership cascade and Y-13 are the same argument, unlinked |
| **B ↔ PERFORMANCE** | — | Security-model performance is a circular deferral (XB-08); environment-count capacity/performance is deferred by `governance.md` §8 to Area 09 and absent there |
| **B ↔ COST** | `governance.md` GOV-11/GOV-18/GOV-C2 handle managed-environment economics well, and `licensing-cost.md` LC-23 mirrors it | E5-class / Entra P1-P2 / Purview dependencies (XB-04); Azure DevOps or GitHub tooling cost for ALM rung 3 is not priced |
| **B ↔ OPERATIONS** | — | Denied outright: `operations-support.md` §9.3 records security, governance and ALM as *"not yet researched"* (XB-01). Security operations, incident response for a security event, and ALM-driven operational duties are unowned |

**Two couplings the corpus gets right and should keep as models.** `governance.md` GOV-C2 surfaces the Microsoft-recommends-broadly vs licence-cost tension as a trade-off to be decided rather than a defect to be reconciled. `licensing-cost.md` LC-23 → DC-11 encodes *criticality → operational requirements → managed environment → premium licences for that environment's users*, with the conclusion *"this is why a departmental solution becomes expensive the day it matters"*. That is a complete requirement-to-cost chain crossing three dimensions, and it is the shape every pairing above should produce.

---

## 9. Architecture Pattern Cross-Check

Per §17 of the brief: each pattern against all seven dimensions. ✅ addressed with evidence · ⚠️ partial or unquantified · ❌ absent · ⚠️**C** conflicting.

| Pattern | Architecture | Security | Governance | ALM | Scale | Cost | Operations |
|---|---|---|---|---|---|---|---|
| **AP-01** Direct | ✅ | ✅ | ⚠️ | ⚠️ | ✅ | ⚠️ | ✅ |
| **AP-02** API-mediated | ✅ | ✅ | ❌ | ⚠️**C** | ⚠️**C** | ⚠️ | ⚠️ |
| **AP-03** Event-driven | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ⚠️**C** |
| **AP-04** Queue-based | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ⚠️**C** |
| **AP-05** Hybrid | ✅ | ✅ | ❌ | ⚠️**C** | ✅ | ⚠️ | ⚠️**C** |
| **AP-06** Data virtualization | ✅ | ✅ | ❌ | ⚠️ | ✅ | ⚠️ | ⚠️ |
| **AP-07** Replication | ✅ | ✅ | ⚠️ | ⚠️ | ✅ | ⚠️ | ⚠️ |
| **AP-08** Facade / BFF | ✅ | ✅ | ❌ | ❌ | ⚠️ | ❌ | ⚠️ |
| **AP-09** Background | ✅ | ✅ | ❌ | ❌ | ✅ | ⚠️ | ✅ |
| **AP-10** Enterprise boundary | ⚠️ | ⚠️ | ❌ | ❌ | ⚠️ | ⚠️ | ⚠️ |

**Reading of the matrix.** Architecture, Security and Scalability are the three dimensions the catalogue actually carries as fields, and they hold up — every pattern's *Security implications* is populated and evidenced, and the scalability verdicts are correctly framed as limit-compliance rather than endorsement. Governance is ❌ for seven of ten patterns and the seven are exactly those requiring an external component (XB-06, XB-14). ALM is ❌ or ⚠️**C** for eight of ten (XB-05, XB-09). Cost is never a field (XB-13).

**Per-pattern notes where the verdict needs qualifying.**

- **AP-01 Direct.** The best-covered pattern, and correctly positioned as the default. ALM ⚠️ only because the connector contract-change cost (republish plus reconnect in every consumer) is stated without the connection-reference consequences of ALM-14. Cost ⚠️: the licence-profile dependency (retry depth, content throughput, request ceiling, leaver reversion) is named but not costed against `licensing-cost.md`.
- **AP-02 / AP-08.** ALM ⚠️**C** — the deployment-coupling clause is present, the custom-connector ALM hazard is not (XB-05). AP-02's Scale is ⚠️**C** because of XB-07's throttle conflict and its own open U-03/U-04 (whether an APIM-fronted call meters differently). AP-08's Cost ❌: its own U-04 asks whether the facade's backend calls are metered at all, unresolved.
- **AP-03 / AP-04.** The strongest structural evidence in the file (Microsoft's own *"not suitable when"* sections) and the weakest cross-dimension support. Governance, ALM and Cost are ❌ because the corpus has no evidence for Service Bus, Event Grid, Event Hubs or dead-lettering outside Block A. Operations ⚠️**C** because of XB-12 — the correlation identifier these patterns need across a broker seam is documented elsewhere as experimental and custom-connector-only.
- **AP-05 Hybrid.** Two operating models is correctly named as *"the pattern's dominant cost"*, and the in-platform vs out-of-platform variant distinction is genuinely useful. But the cost is never quantified, the ALM story for the two halves is a single clause, and the pattern depends on both a pro-dev team (`platform-suitability.md` PS-40) and a test harness that `alm-devops.md` ALM-17 says does not exist (XB-09).
- **AP-06 Data virtualization.** The best-evidenced limitation list in the corpus (thirteen documented exclusions, and two documented rejections in a Microsoft reference architecture, both on row-level security). Its own C-02 correctly refuses to upgrade write-through virtualization to STRONG without instantiation evidence. Governance ❌ only in that the external data platform's ownership is unaddressed.
- **AP-07 Replication.** Governance ⚠️ rather than ❌ because `governance.md` covers the Dataverse-side environment topology. The synchronization risk register (§8, 13 rows) is strong; it lacks recovery-induced divergence (XB-16).
- **AP-10 Enterprise boundary.** Architecture ⚠️ by the file's own admission: U-08 records that *"'enterprise integration boundary' is a recognised pattern"* is unestablished, §11.1 states *"AP-10 is synthesis"*, and §1 names it as the pattern needing independent checking because *"its evidence is the thinnest in the file"*. It is simultaneously the pattern with the largest governance, cost and operations consequence and the one with least evidence on all three. The pack must not present it as Microsoft terminology, and the file says so.

**One conclusion the matrix supports.** The catalogue is safe to use for pattern *shape* and pattern *exclusion* today. It is not safe to use for pattern *selection* in any case where the answer is AP-02, AP-03, AP-04, AP-05, AP-08 or AP-10, because the selection would be made without governance, ALM or cost visibility on six of the ten options.

---

## 10. Evidence Quality Findings

### XB-17 — Evidence discipline is high and consistently applied; three specific weaknesses are self-declared and should be carried forward, not discovered later

**Severity:** LOW

**Type:** WEAK EVIDENCE (assessment, not defect)

**Affected Areas:** all files

**Evidence and assessment.** Recommendation-level grading, per the brief's four categories:

| Claim class | Grade | Basis |
|---|---|---|
| Published platform limits (throttles, timeouts, payload caps, batch semantics, retention) | **SUPPORTED** | Tier 1, fetched, `ms.date` recorded. 40/47 in `integration-architecture.md`; 25/31 in `performance-scale.md`; 24/26 in `operations-support.md` |
| Microsoft's own "not suitable when" and exclusion statements | **SUPPORTED** — the strongest evidence in the corpus | e.g. *"Financial posting entities… are deliberately excluded from dual-write, avoiding any shadow-ERP behavior"* (IA-37); the five Azure pattern pages' exclusion sections; SEC-25's dynamic-endpoint gap; `operations-support.md`'s 100 numbered limitations |
| Pattern boundaries and escalation ladders | **CONDITIONALLY SUPPORTED** | Tagged INF over MS facts and labelled as such (`architecture-patterns.md` §3.2, `integration-architecture.md` §2.2, `performance-scale.md` §1) |
| Any "this will perform adequately" claim | **UNSUPPORTED** — and the corpus says so | `performance-scale.md` §0 and U-01: no empirical measurement exists anywhere for any component; every `WITHIN ENVELOPE` verdict means only "no documented limit violated" |
| Licence entitlement specifics | **UNSUPPORTED as fact, correctly handled** | `licensing-cost.md` §0.2: Learn is not authoritative; *"the pack must never assert a licence entitlement as a Confirmed fact"* |
| Comparative economics vs alternatives | **WEAKLY SUPPORTED** | `licensing-cost.md` §6, LOW-MEDIUM, U-04 (see XB-11) |
| Sprawl and cost-shock magnitudes | **UNSUPPORTED, correctly fenced** | `governance.md` GOV-26 (*"never as a benchmark to quote"*); `licensing-cost.md` §7.3 (*"must not be encoded as figures"*) |

**Marketing language is handled correctly and consistently.** The corpus does not treat Microsoft documentation as proof of suitability. `integration-architecture.md` IA-23 records Microsoft's *"Scales well for most business scenarios"* and then rules *"Do not encode the adjective"*; `performance-scale.md` C-02 refuses to reconcile *"secure, scalable, and highly available"* with a limits page that publishes no limits; the `MS-V` tag fences the Logic Apps team's positioning on both sides of the argument. This meets `source-policy.md` §7 without exception in the files reviewed.

**Three self-declared weaknesses that must survive into the pack.**
1. **No measurement anywhere.** Stated in every file. Any pack verdict on performance must be paired with a pilot or monitoring requirement, never presented as a capability claim.
2. **Dating weakness on load-bearing numbers.** `integration-architecture.md` §13.1 item 2: the three connector reference pages carrying the most decision-relevant throttles (I-33, I-34, I-35) all show `ms.date: 2024-03-01` with 2026 update stamps. `performance-scale.md` §12 flags five pages older than 18 months, two of which (P-07, P-08) carry the only network-latency and deployment-window numbers in the corpus.
3. **Single author, single session.** Declared in all eight files, each naming its highest-value independent checks. This review is the first independent read of any of them, and it confirms the concern was warranted: XB-01, XB-03, XB-04 and XB-07 are exactly the class of defect a second reader catches and a single author cannot.

**Required Correction:** None to the evidence handling, which is sound. Carry the three weaknesses into the pack as standing epistemic constraints rather than as research notes, and treat each file's *Verification list before pack encoding* as a gate precondition rather than advice — `security.md` §9, `governance.md` §9 and `alm-devops.md` §9 already use the word *mandatory*.

---

## 11. Negative Evidence Findings

**Assessment: this is the corpus's strongest attribute.** The brief's §22 test — *where does the research explain when NOT to use this, and when NOT to use Power Platform* — is met more thoroughly than in most vendor-adjacent research.

Present and well-evidenced:
- `integration-architecture.md` §12: nine conditions under which Power Platform should **not** be the integration layer, each with evidence and a confidence grade, led by the one Microsoft never prompts — *"The integration responsibility already has an owner"* — plus §12.9 *What is not a reason to move the integration out*, which guards the boundary in the other direction (scale anxiety without a number, a preference for code, one difficult step, resemblance to a reference architecture).
- `integration-architecture.md` §7: a 39-item negative evidence register, and §6: 18 implementation anti-patterns each with the documented evidence that it is one.
- `architecture-patterns.md` §8: Microsoft's own *"not suitable when"* statements for six patterns, plus *"Documented costs stated by Microsoft in the same breath as the benefit"* — the most useful framing in the file — plus a *When NOT to use* section on every pattern.
- `performance-scale.md` §4.3: four boundaries that put the workload outside Power Platform; §8: 48 negative items; §6: 18 anti-patterns.
- `licensing-cost.md` §7.2: 38 *"cost mechanics that work against the customer"*.
- `operations-support.md` §6: 100 numbered limitations across observability, backup/restore, DR, support and lifecycle — including the support-scope statements (*"Technical support doesn't conduct RCAs as part of any support experience"*, *"Microsoft doesn't help correct damaged data"*, four hours then closure) that contradict widely-held assumptions in quotable terms.
- `security.md` §13: the documented weak points listed as prominently as the capabilities, with the rule *"A design that states these residuals explicitly is defensible. A design that presents any of them as containment is not."*

### XB-18 — Negative evidence is per-block and never composed, so the strongest cross-cutting disqualifiers are not stated anywhere

**Severity:** MEDIUM

**Type:** MISSING NEGATIVE EVIDENCE

**Affected Areas:** the "when should we not use Power Platform" answer; §12 of `integration-architecture.md`; §4.3 of `performance-scale.md`

**Evidence:** Each block's negative register is complete within its own scope and cites only its own block. The consequence is that the disqualifiers which arise only from a *combination* of dimensions are absent. Three examples that the corpus fully supports but never states:
1. **Security requirement × cost.** A requirement for network restriction or customer-managed keys forces managed environments *and* an E5-class licence for the whole population (`security.md` SEC-27/SEC-29). For a large, thinly-licensed population this may disqualify the platform on cost — and nothing in `integration-architecture.md` §12, `performance-scale.md` §4.3 or `platform-suitability.md`'s remit composes it (XB-04).
2. **Criticality × ALM × operations.** A mission-critical classification requires solution-aware artefacts, service-principal ownership, telemetry export, managed environments, cross-region DR and a premium support plan (`operations-support.md` §1.1) — while `alm-devops.md` ALM-17 establishes there is no automated functional test framework and ALM-18 that there is no rollback. A workload needing automated regression plus reliable rollback plus 24×7 is not well served, and no file says it.
3. **External estate × no operator.** `architecture-patterns.md` Y-13 makes an operator-less pattern unavailable; `operations-support.md` OP-05's ownership cascade proves the failure mode end to end. Together they are a platform-level disqualifier for organisations without a platform team, stated as neither.

**Why It Matters:** The corpus rule is that Power Platform must not be assumed to be the answer. Single-dimension disqualifiers are covered well. Real engagements are disqualified by combinations, and the combination logic is exactly what the missing cross-block layer would have produced.

**Required Correction:** Add a composed disqualifier register to the reconciliation artefact of XB-02: conditions that are acceptable on any single dimension and disqualifying in combination. Draw on the material already present — `security.md` §12.1's *"a security requirement can force a licensing decision for an entire user population"*, `operations-support.md` §1.1's criticality ladder, `licensing-cost.md` DC-11, `architecture-patterns.md` Y-13.

---

## 12. Terminology / Semantic Drift

### XB-19 — Four load-bearing terms carry different meanings across blocks, and the one that gates the most decisions is defined once, as inference, in one file

**Severity:** MEDIUM

**Type:** SEMANTIC DRIFT

**Affected Areas:** all cross-block reasoning; any decision criterion that references criticality, latency class or volume

**Evidence:**

| Term | Usage counts (IA / AP / SEC / GOV / ALM / PF / LC / OP) | Drift |
|---|---|---|
| **"pipeline"** | 16 / 7 / — / — / high / — / — / high | Block A uses it predominantly for an **integration stream**: *"per-pair pipelines multiply combinatorially"*, *"the answer is not a better sync pipeline"*, *"**Count pipelines as a governance metric**; a rising pipeline count with a flat system count is the signal"*, *"Each new requirement adds one more direct pipeline"*. Minority use = deployment pipeline. Block B uses it **exclusively** for Pipelines in Power Platform, the ALM product (rung 2, ALM-10, ALM-11). A governance metric expressed in Block A's sense will be read in Block B's |
| **"business-critical"** | 3 / 2 / 1 / 2 / 0 / 11 / 9 / 11 | 39 uses, in load-bearing conditionals: *"any business-critical integration must…"* (IA-16), *"Business-critical workload in a non-production environment"* (PF anti-pattern), *"the moment a workload is classified as business-critical, the licence model is implicated"* (LC DC-11). **One definition exists**: `operations-support.md` §1.1's four maturity classes, Origin *"MS (the two-column table and definitions) + **INF** (the four-class extension)"*, Confidence **MEDIUM**. The Microsoft source behind it has **two** classes (productivity vs mission-critical), not four. No other file references the four classes |
| **"real-time" / "near-real-time"** | 8+4 / 6+1 / 0 / 0 / 1 / 2 / 0 / 7+1 | Block A uses it as a **latency class with numbers** (§2.1 row 5: interactive / near-real-time / eventually consistent, against 120 s / 180 s / 2 min ceilings) and correctly reports Microsoft's caution that *"Many requests for real-time access lack a strong business case"*. `operations-support.md` uses it for **monitoring latency** (*"Don't use this information for real-time monitoring"*). Zero uses in `security.md` and `governance.md`, so a real-time requirement has no security or governance reading at all |
| **"high volume"** | 4 / 0 / 0 / 0 / 0 / 10 / 7 / 2 | Quantified only in Block C, against the five meters. Zero uses in security, governance and ALM — so "high volume" has no governance, security or lifecycle consequence anywhere in the corpus, despite Block A's IA-16 (auto-off after 14 days) and IA-17 (retry depth by licence) making it an availability and ownership matter |
| **"enterprise"** | — | Three distinct senses: a **maturity class** (`operations-support.md` §1.1), a **delivery model** (`governance.md` GOV-01: centralised / decentralised / hybrid), and an **Azure resource type** (*"enterprise policy"*, `security.md` SEC-29/SEC-30, `integration-architecture.md` IA-29). Also *"enterprise boundary"* as a pattern name (AP-10) and *"enterprise-grade"* once in Block A |
| **"production-ready"** | 0 across all eight | Not used. Recorded because the brief lists it: the corpus avoids the term, which is correct |

**Why It Matters:** "business-critical" gates the licence model (LC DC-11), the operational feature set (OP-21), the ALM rung (ALM-01), the environment type (GOV boundary 1) and the integration reliability design (IA-16). It is the corpus's most consequential term and it has one MEDIUM-confidence, partly-inferred definition in a file that two of the three blocks do not cite. "pipeline" is worse in kind because both meanings are legitimate and both appear in governance-relevant sentences.

**Required Correction:** Establish a canonical glossary for the corpus — not the pack — covering at minimum: *integration stream* vs *deployment pipeline*; the criticality classes (promote `operations-support.md` §1.1 to corpus level, keep its INF tag and its MEDIUM confidence, and require every file that uses "business-critical" to cite it); latency classes with their numeric boundaries (adopt `integration-architecture.md` §2.1 row 5); volume expressed in the five meters of `performance-scale.md` §2; and the three senses of "enterprise", disambiguated. This is a corpus-hygiene action, distinct from and prior to authoring the pack's own glossary, which remains out of scope.

---

## 13. Candidate Decision Criteria

Statements that should become reusable decision criteria. The corpus already supplies four well-formed criteria sets — `integration-architecture.md` §9 (28 variables), `architecture-patterns.md` §3.1 (variable → pattern boundary), `security.md` §4 (20), `governance.md` §4 (15), `alm-devops.md` §4, `performance-scale.md` §7 (DC-01…DC-20), `licensing-cost.md` §3 (DC-01…DC-13), `operations-support.md` §3. These are strong and should be preserved. What follows is only the **cross-block** criteria that no single file can state, since those are what the review is for. No decision tree is constructed here.

| # | Candidate criterion | Why it matters | Decisions it influences | Evidence |
|---|---|---|---|---|
| 1 | **Criticality class of the workload** (departmental / business-critical / enterprise / mission-critical) | It is the master criterion: it determines artefact structure, ownership model, environment type, licence footprint of the whole population, DR posture and support tier — and it must be set in Discovery because discovering it later means rework | Everything downstream | `operations-support.md` §1.1 (INF, MEDIUM); `licensing-cost.md` DC-11; `governance.md` boundary 1; `alm-devops.md` ALM-01 |
| 2 | **Does the architecture require a component outside Power Platform, and is there a named operator for it?** | Y-13 makes the answer binary: no operator makes the pattern unavailable, not expensive. It also triggers the second operating model, the second pipeline, the second on-call rotation and the unquantified cost of XB-06 | AP-02, AP-04, AP-05, AP-08, AP-10 selection; option costing; governance scope | `architecture-patterns.md` Y-13; `integration-architecture.md` §2.1 row 11, IA-24, IA-29; `licensing-cost.md` U-06 |
| 3 | **Which security controls are required, and what non-Power-Platform licence do they presuppose?** | Converts a security requirement into a population-scoped licence decision — the largest cost line in a hardened design, and currently missing from the cost model | Environment topology; managed-environment decision; option economics; go/no-go | `security.md` SEC-02, SEC-27, SEC-29, SEC-34, §10; XB-04 |
| 4 | **Is a custom connector on the critical path?** | It is simultaneously the standard seam for four patterns, a premium-licence trigger, a count-capped resource (one on seeded M365 rights), a CONFLICTED throughput figure, and the corpus's most ALM-hostile artefact | Pattern selection; ALM rung; licence model; deployment and restore procedures | `integration-architecture.md` IA-13, C-01, C-02; `alm-devops.md` ALM-14; `licensing-cost.md` LC-03; XB-05, XB-07 |
| 5 | **What is the licence profile of the identity that will own each automation?** | Retry depth, loop ceilings, content throughput, request entitlement and continued existence all follow the owner's licence, and revert on a leaver event. Resilience is a licensing property, not a design property | Integration reliability design; ownership model; cost; operations alerting | `integration-architecture.md` IA-16, IA-17; `performance-scale.md` PF-29, DC-18; `operations-support.md` OP-04; `licensing-cost.md` LC-08 |
| 6 | **How will the design be validated, given that no low-code test harness exists and load testing is constrained?** | Determines whether the architecture is provable from limits, needs a bounded pilot, or needs a pro-dev test capability with a budget line — and whether a managed test environment is required | Option feasibility; ALM rung; cost; go-live gate | `alm-devops.md` ALM-17; `performance-scale.md` PF-15, B-17, DC-17; `operations-support.md` C-03; XB-09 |
| 7 | **What availability is being committed to, and on what evidence?** | The corpus has RTO/RPO and no uptime SLA. A commitment must not be derived from recovery objectives | Mission-critical suitability; DR architecture; contractual exposure | `operations-support.md` U-01, §10; `performance-scale.md` §3.D; XB-10 |
| 8 | **Where does the system of record sit, per entity, per field and per lifecycle phase?** | Microsoft's own reference architecture excludes financial posting entities from bidirectional sync to avoid a shadow ERP. Sync scope defaults to minimum | Virtualization vs replication; sync topology; reconciliation obligation | `integration-architecture.md` IA-36, IA-37; `architecture-patterns.md` Y-06 |
| 9 | **What is the binding meter, the projected consumption at horizon, and the redesign trigger?** | Converts an unbounded "will it scale?" into a dated, monitorable claim with a tripwire — the single most useful reframing in the corpus | Sizing; pattern escalation; monitoring design; revalidation cadence | `performance-scale.md` PF-47 (*"reachable limits"*), §2; `integration-architecture.md` IA-01, IA-10 |
| 10 | **Does an enterprise integration capability already exist, with a published contract?** | Nothing in Microsoft's documentation prompts this question, which is precisely why it must be asked first. Skipping it produces the point-to-point estate nobody chose | EXTERNAL vs in-platform verdict; governance scope; ownership | `integration-architecture.md` §2.2 step 1, §12.1; `architecture-patterns.md` Y-12 |
| 11 | **Which requirements are irreversible at creation time?** | Table ownership type, solution publisher, environment region, Dynamics 365 apps installed, and the non-subtractability of Dataverse grants are all one-way doors that belong in Discovery, not Options | Data model; environment provisioning; security model; ALM plan | `security.md` SEC-08, SEC-09, §10; `alm-devops.md` ALM-05, ALM-24 |
| 12 | **What delivery guarantee, ordering and duplicate tolerance does the business actually require?** | Five answers select the transport, and no configuration inside Power Automate supplies any of them | Broker selection; AP-03 vs AP-04; idempotency design; cost of the external half | `integration-architecture.md` IA-15, IA-46; `architecture-patterns.md` AP-04 |

---

## 14. Candidate Anti-Patterns

The corpus already carries five anti-pattern registers, and they are good: `integration-architecture.md` §6 (X-01…X-18, implementation), `architecture-patterns.md` §7 (Y-01…Y-14, pattern selection), `security.md` §5 (SEC-A1…A15), `governance.md` §5 (GOV-A1…A12), `alm-devops.md` §5, plus the three anti-pattern tables in Block C. Those should be preserved with their namespaces disambiguated per XB-03. Listed here are only the anti-patterns that arise from a **cross-block** combination and therefore appear in none of them.

| # | Candidate anti-pattern | Why the evidence justifies it | Evidence |
|---|---|---|---|
| 1 | **Escalating to a pattern whose non-Power-Platform half has no owner, budget or pipeline.** Adopting AP-02/AP-04/AP-05/AP-08/AP-10 on architectural merit alone | Y-13 already rules it makes the pattern *unavailable*; OP-05 documents the resulting failure chain end to end; the cost is unquantified corpus-wide | `architecture-patterns.md` Y-13; `operations-support.md` OP-05; `licensing-cost.md` U-06; XB-06 |
| 2 | **Costing a hardened design on Power Platform licences alone.** Pricing an IP-firewall, CMK, Conditional-Access or read-audit requirement without the E5-class, Entra P1/P2 or Purview prerequisite | `security.md` states the increment is *"often larger than the Power Platform cost itself"*; `licensing-cost.md` contains none of the three dependencies | `security.md` SEC-02, SEC-27, SEC-29, SEC-34; XB-04 |
| 3 | **Building the integration seam on a custom connector without planning its ALM.** Choosing the seam for architectural fit and meeting the connection-reference behaviour at deployment | Four documented failure modes, one of whose workarounds creates an unmanaged layer inside a managed solution and defeats the production-integrity control | `alm-devops.md` ALM-14, ALM-15, ALM-18; `security.md` SEC-19; XB-05 |
| 4 | **Deriving an availability commitment from RTO/RPO.** Presenting *"RPO ≈ 0, RTO < 5 min"* as an uptime commitment | `operations-support.md` states the prohibition verbatim and records the SLA absence as the area's largest weakness | `operations-support.md` U-01, §10; XB-10 |
| 5 | **Planning validation by load test.** Writing a go-live gate that depends on full-scale load testing or an automated low-code regression suite | Microsoft constrains load testing against the shared service; Test Engine is deprecated with no first-party low-code successor; `performance-scale.md` B-17 makes load-test-only validation an out-of-platform boundary | `performance-scale.md` PF-15, B-17; `alm-devops.md` ALM-17; XB-09 |
| 6 | **Designing multi-hop diagnosis around platform correlation tracing.** Assuming the platform supplies the correlation id the architecture requires | Correlation tracing is experimental, *"not meant for production use"*, and works only with custom connectors — excluding the broker seams that need it most | `operations-support.md` §6.1 items 29–30, OP-03; `architecture-patterns.md` AP-05; XB-12 |
| 7 | **Recommending a BU / owner-team / sharing-heavy security model without a volume test.** Adopting SEC-10/SEC-11/SEC-12 at scale on functional grounds alone | Microsoft attaches an unquantified performance penalty to sharing and to excessive column security; the corpus's own attempt to quantify it terminates in an unanswered deferral | `security.md` SEC-12, SEC-13, §8; `performance-scale.md` U-07; XB-08 |
| 8 | **Encoding a figure that another file registers as CONFLICTED.** Sizing against a corpus number without checking its epistemic state elsewhere | The custom-connector throttle is do-not-encode in one file and a settled envelope value in another, with a 20× spread | `integration-architecture.md` C-01, U-02; `performance-scale.md` §3.C row 29; XB-07 |
| 9 | **Treating a corpus deferral as evidence that the target is unresearched.** Following Block C's *"not yet researched"* routing | Three such rows point at files written the same day that answer them in depth | `operations-support.md` §9.3; `licensing-cost.md` §10.3; XB-01 |

---

## 15. Volatile Information

Per §25 of the brief. The corpus handles this well: `licensing-cost.md` §0.3 publishes a five-point volatility protocol, `performance-scale.md` §0 and `integration-architecture.md` §1 both carry volatility notes with named warnings, `security.md` §19 states that *"Security is the fastest-moving Power Platform surface in 2025–2026"*, and every file carries a *Verification list before pack encoding*. Two additions are needed: the classification is not stated uniformly as STATIC vs VOLATILE, and the dated commitments are not held in one place.

**STATIC PRINCIPLE — safe to encode as durable.**
- Dataverse privileges are additive and cannot be subtracted (`security.md` SEC-08).
- The environment is simultaneously the security boundary, governance unit, DLP scope, residency unit and licence unit (`security.md` SEC-15; `governance.md` §13).
- The application is never an authorization layer; the user's rights on the data source decide (`security.md` SEC-18).
- Atomicity stops at the Dataverse boundary; there is no cross-system transaction or saga construct (`integration-architecture.md` IA-19; `architecture-patterns.md` §8 item 28).
- Delivery guarantee, ordering, duplicate detection and dead-lettering are properties of the transport, not of the flow (`integration-architecture.md` IA-15).
- Three (or five) independent meters are evaluated separately, and the binding one is the smallest (`integration-architecture.md` IA-10; `performance-scale.md` §2).
- Non-delegable queries return silently truncated results — a correctness failure, not a performance one (`performance-scale.md` PF-01).
- Ownership is a runtime dependency on an individual's employment status and licence (`operations-support.md` OP-04).
- There is no solution rollback; recovery is redeploy, restore or fix-forward (`alm-devops.md` ALM-18).
- Cost scales primarily with people, secondarily with actions and stored bytes (`licensing-cost.md` §6).
- Microsoft publishes limits, not benchmarks (`performance-scale.md` §0).
- Learn is not authoritative on licence entitlement (`licensing-cost.md` §0.2).
- Solutions carry metadata, not business data; deleting a managed solution destroys data in its custom tables and columns (`alm-devops.md` ALM-02, ALM-07).
- Weakest-link governs: the availability and throughput of an integration path is that of its worst participant, including the parts the customer operates (`integration-architecture.md` IA-06, IA-27).

**VOLATILE VALUE — must carry a date and a revalidation trigger; must not be hardcoded.**
- Every connector throttle. Specifically flagged: the three reference pages carrying the most decision-relevant numbers show `ms.date: 2024-03-01` with 2026 update stamps (`integration-architecture.md` §13.1 item 2).
- The custom-connector throughput figure — **CONFLICTED**, 500 vs 10,000 (XB-07). Do not encode either.
- All Power Platform request entitlements. The request model is *"explicitly mid-transition with no announced enforcement date"* (`integration-architecture.md` §1; `performance-scale.md` §0).
- All prices. Microsoft labels its own *"illustrative only"* (`licensing-cost.md` §0.3).
- All capacity accrual rates per licence.
- Preview and GA states — a large set: ACP design-time enforcement per maker portal, endpoint filtering, security score, app access control, administrator privileges, guest-access GA state (`security.md` §19, SEC-C1); PPR usage reporting; Power Automate flow-run, Power Pages and PPR meters; canvas correlation tracing.
- VNet supported-connector list (`security.md` §9 item 6: *"changes often"*).
- The CMK exclusion list (`security.md` §9 item 7: *"it grew during the research window"*).
- Site Checker thresholds (`performance-scale.md` U-04: page from 2023).
- Backup retention values and their environment-type conditions.
- Support-plan tiers and response times.

**DATED COMMITMENTS — belong in a tripwire, not a static rule.** Both `governance.md` §10 and `alm-devops.md` §10 already say this; the list should be held once, corpus-wide.
- **February 2026** — Microsoft begins auto-enabling managed environments on pipeline target environments (`alm-devops.md` ALM-10; `operations-support.md` O-06; `licensing-cost.md` §7.2 item 36).
- **June 2026** — end-user in-app licence notifications begin (`governance.md` GOV-11).
- **April 2026** — Test Engine deprecated (`alm-devops.md` ALM-17).
- **1 November 2026** — 5,000 bundled AI Builder credits removed (`licensing-cost.md` §7.2 item 29).
- **February 2027** — users without a qualifying licence blocked from opening apps in a managed environment (`governance.md` GOV-11).
- **Undated but committed** — PPR enforcement, six months after usage reporting reaches GA, with *"no current ETA"* (`licensing-cost.md` LC-09). This is the corpus's most consequential undated commitment: a compliant design today can be throttled on a date outside the customer's control.

**DEPRECATIONS that invalidate circulating prior art** — these are neither static nor merely volatile; they retire third-party guidance wholesale and should be flagged as such.
- CoE Starter Kit *"no longer actively maintained"* (`governance.md` GOV-12; `licensing-cost.md` §7.2 item 48; `operations-support.md` §6.5 item 85).
- ALM Accelerator deprecated (`alm-devops.md` ALM-22).
- Test Engine deprecated (`alm-devops.md` ALM-17).

---

## 16. Cross-Block Coverage Matrix

✅ covered with evidence · ⚠️ partial or unquantified · ❌ missing · ⚠️**C** conflicting.

Columns map to the corpus as: **Architecture** = Block A; **Security / Governance / ALM** = Block B; **Scale / Cost / Operations** = Block C.

| Decision Dimension | Architecture | Security | Governance | ALM | Scale | Cost | Operations |
|---|---|---|---|---|---|---|---|
| **Identity** | ✅ | ✅ | ⚠️ | ✅ | ✅ | ⚠️ | ✅ |
| **Integration** | ✅ | ⚠️ | ❌ | ⚠️ | ⚠️**C** | ⚠️ | ⚠️ |
| **Data** | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ⚠️ |
| **Transactions** | ✅ | ❌ | ❌ | ❌ | ⚠️ | ⚠️ | ⚠️ |
| **Performance** | ✅ | ❌ | ❌ | ⚠️ | ✅ | ✅ | ✅ |
| **Availability** | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ✅ | ✅ | ⚠️ |
| **Security** | ⚠️ | ✅ | ✅ | ✅ | ❌ | ❌ | ⚠️ |
| **Compliance** | ⚠️ | ✅ | ⚠️ | ⚠️ | ❌ | ⚠️ | ⚠️ |
| **Environment** | ⚠️ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| **Deployment** | ⚠️ | ✅ | ✅ | ✅ | ⚠️ | ⚠️ | ✅ |
| **Monitoring** | ⚠️ | ⚠️ | ✅ | ⚠️ | ✅ | ✅ | ⚠️**C** |
| **Cost** | ❌ | ❌ | ✅ | ⚠️ | ✅ | ✅ | ✅ |
| **Ownership** | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ |
| **Lifecycle** | ⚠️ | ⚠️ | ✅ | ✅ | ❌ | ⚠️ | ⚠️ |
| **Recovery** | ❌ | ✅ | ⚠️ | ✅ | ⚠️ | ✅ | ✅ |
| **External dependencies** | ✅ | ⚠️ | ❌ | ❌ | ⚠️ | ⚠️ | ⚠️ |
| **Scale (growth / headroom)** | ✅ | ⚠️ | ⚠️ | ⚠️ | ✅ | ✅ | ⚠️ |

**Justification for the ❌ and ⚠️C cells** — the matrix is meant to expose weakness, so each is traceable.

- **Integration / Governance ❌** — `governance.md`: Azure 0, gateway 0, APIM 0, Service Bus 0, on-premises 0 (XB-14).
- **Integration / Scale ⚠️C** — custom-connector throttle held at two epistemic states (XB-07).
- **Integration / ALM ⚠️** — ALM-14 covers the artefact thoroughly and never reaches the patterns that depend on it (XB-05).
- **Transactions / Security, Governance, ALM ❌** — no authorization, ownership or deployment model for a compensating unit of work; *"dual-write"* appears 0 times in Blocks B and C (XB-15).
- **Performance / Security ❌** — the circular deferral (XB-08); `performance-scale.md` contains *"security filter"* 0, *"column security"* 0, *"security role"* 0.
- **Performance / Governance ❌** — `governance.md` §8 defers environment-count capacity and performance to Area 09, which has no environment-count content.
- **Security / Scale ❌** — same as Performance / Security, from the other side.
- **Security / Cost ❌** — E5 / Entra P1-P2 / Purview all 0 in `licensing-cost.md` (XB-04).
- **Compliance / Scale ❌** — audit and retention have no throughput or latency treatment; `security.md` SEC-34 notes audit consumes capacity, and no file sizes its performance impact.
- **Environment / Scale ❌** — dangling deferral from `governance.md` §8.
- **Cost / Architecture ❌** — no Cost field on any of the ten patterns (XB-13).
- **Cost / Security ❌** — as XB-04.
- **Lifecycle / Scale ❌** — no treatment of how growth triggers retirement or re-platforming; `performance-scale.md` PF-47's *"reachable limit"* and redesign trigger is the closest, and it is framed as sizing, not lifecycle.
- **Recovery / Architecture ❌** — Block A: *"restore"* 0, *"backup"* 0 (XB-16).
- **External dependencies / Governance, ALM ❌** — no governance or lifecycle model for a consumed external service (XB-06, XB-14).
- **Monitoring / Operations ⚠️C** — the correlation contradiction (XB-12), inside otherwise the strongest monitoring content in the corpus.
- **Availability row is ⚠️ across five columns** because the underlying commitment cannot be sourced at all (XB-10).

**The shape of the weakness.** Reading down the columns: Architecture and Operations are strong, Security is strong inside its own scope, Governance and ALM are strong for a Power-Platform-only estate, Scale and Cost are strong on their own meters. Reading across the rows: Integration, Transactions, External dependencies, Cost and Recovery each have at least two ❌. Those five rows are precisely the dimensions that cross the platform boundary or cross a block boundary — which is XB-02 restated as a matrix.

---

## 17. Required Corrections

**BLOCKING — pack authoring must not begin until these land.**

| # | Correction | Finding | Effort |
|---|---|---|---|
| **C1** | Correct the three *"not yet researched"* deferral rows in `operations-support.md` §9.3 and `licensing-cost.md` §10.3 to name the actual files and finding ids. Add a corpus manifest (file, area, status, date, confidence) so the claim cannot recur | XB-01 | Small |
| **C2** | Disambiguate the id namespaces corpus-wide before any ingestion: unique finding prefix per file, unique prefix per finding *kind*, file-qualified `C-nn` and `U-nn`, and a corpus index mapping duplicate conflicts and unknowns to one canonical id. Add the convention to `source-policy.md` | XB-03 | Small–Medium |
| **C3** | Add the non-Power-Platform licence dependencies to `licensing-cost.md` as first-class cost drivers — E5-class for IP firewall and CMK, Entra ID P1/P2 for Conditional Access, Purview for activity logging — with population scope, and a decision criterion of the form *security control → external licence prerequisite → population → cost*. Cite back from `security.md` §8 | XB-04 | Medium |
| **C4** | Resolve or propagate the custom-connector figures: `performance-scale.md` §2 and §3.C row 29 must not present as settled what `integration-architecture.md` C-01 marks do-not-encode, and the count must be restated as licence-conditional per IA-13. Add the corpus rule that a CONFLICTED figure is CONFLICTED corpus-wide | XB-07 | Small |
| **C5** | Run the cross-block reconciliation pass over the nine missing pairings in §8, using the discipline already demonstrated by the intra-block cross-area sections. Record its completion in each file's header | XB-02 | Large |

**HIGH — required before the pack's pattern and cost content is authored.**

| # | Correction | Finding |
|---|---|---|
| **C6** | Add the custom-connector ALM consequences to AP-02, AP-05, AP-08 and AP-10 as preconditions and costs, with the reciprocal note in `alm-devops.md` ALM-14. Where the documented workaround defeats block-unmanaged-customizations, record it as a decision boundary | XB-05 |
| **C7** | Link `licensing-cost.md` U-06 to `integration-architecture.md` IA-27 / IA-29 / §7 items 28–29, which supply the gateway and VNet sizing basis the unknown asks for. Link `architecture-patterns.md` Y-13 to `operations-support.md` §1.1 and OP-05 | XB-06 |
| **C8** | Add *Cost implications*, *Governance implications* and *ALM implications* as required fields on all ten patterns, and add matrix rows for budget constraint, deployment maturity, operational maturity and licence profile of the user population | XB-13 |
| **C9** | Reconcile the four positions on validation into one model (provable from limits / bounded pilot with monitoring / pro-dev test harness with a budget line / not testable without a managed test environment), and rewrite Block A's per-pattern validation instructions against it | XB-09 |
| **C10** | Retrieve the Microsoft Online Services SLA / Product Terms and reconcile against `operations-support.md` OP-19. Until then, encode corpus-wide that no availability commitment may be derived from RTO/RPO | XB-10 |
| **C11** | Close the security-model performance loop honestly: name the requesting findings in `performance-scale.md` U-07, record that no Microsoft figure exists, and convert the deferral into a stated validation obligation on any BU/team/sharing-heavy model | XB-08 |
| **C12** | State the correlation constraint once in both Block A and `operations-support.md` OP-03: correlation across a broker seam must be hand-built, and its cost belongs in the pattern | XB-12 |
| **C13** | Extend `governance.md` with a lever for the non-Power-Platform estate, or declare it out of scope and name the owner. Connect §4 row 6 to `integration-architecture.md` §12.1 and `architecture-patterns.md` Y-12/Y-13 | XB-14 |
| **C14** | Reframe `licensing-cost.md` §6 as a comparison **method** unless comparator pricing is fetched, preserving the durable users-to-work crossover framing and marking every comparator verdict as requiring per-engagement pricing | XB-11 |

**MEDIUM — required before the pack is validated.**

| # | Correction | Finding |
|---|---|---|
| **C15** | Establish a corpus glossary: *integration stream* vs *deployment pipeline*; criticality classes promoted from `operations-support.md` §1.1 with their INF tag intact; latency classes with numeric boundaries; volume in the five meters; the three senses of *enterprise* | XB-19 |
| **C16** | Add a composed-disqualifier register: conditions acceptable on one dimension and disqualifying in combination | XB-18 |
| **C17** | Add the security, governance and ALM consequences of the compensating-transaction and reconciliation shape; close or mark decision-blocking `integration-architecture.md` U-14 (dual-write failure semantics), which the file itself grades material | XB-15 |
| **C18** | Add recovery to each pattern's implications, and a restore-induced-divergence row to `integration-architecture.md` §8's synchronization risk register | XB-16 |
| **C19** | Correct the `automation-architecture.md` peer confidence grade in `performance-scale.md`, `licensing-cost.md` and `operations-support.md` from MEDIUM-HIGH to MEDIUM (the source file's header reads MEDIUM), and reconcile the two meanings of *"Block A"* across the corpus | XB-20, XB-21 |
| **C20** | Consolidate the dated commitments and the deprecations-that-invalidate-prior-art into one corpus-level register, per §15 | XB-19 / §15 |

**Two supporting findings recorded here for completeness, referenced by C19.**

### XB-20 — All three Block C files misreport a peer's confidence grade while claiming to have verified it

**Severity:** MEDIUM · **Type:** WEAK EVIDENCE · **Affected Areas:** confidence propagation; provenance

**Evidence:** `automation-architecture.md` line 2 reads *"Research Confidence: MEDIUM"*. `integration-architecture.md` and `architecture-patterns.md` report it correctly as MEDIUM. `performance-scale.md`, `licensing-cost.md` and `operations-support.md` each report *"`automation-architecture.md` (VALIDATED, Gate PASS, **MEDIUM-HIGH**) as **AT2-nn**"*, in a sentence beginning *"Cross-references to peer files, statuses verified 2026-09-03"*.

**Why It Matters:** Small in itself, diagnostic in aggregate. Block C's findings inherit confidence from AT2 — `performance-scale.md` cites AT2 25 times, `operations-support.md` twice, `licensing-cost.md` via the shared meter model — and the inheritance rule in each file is that HIGH confidence may be *"inherited from a VALIDATED peer"*. An over-stated peer grade over-states every finding that inherits from it, and the "statuses verified" claim means the error will not be re-checked.

**Required Correction:** Correct the grade in all three files. Re-check every Block C finding whose confidence rests on inheritance from AT2.

### XB-21 — "Block A" denotes two different sets of files

**Severity:** MEDIUM · **Type:** SEMANTIC DRIFT · **Affected Areas:** all cross-references using the phrase

**Evidence:** `security.md`, `governance.md` and `alm-devops.md` each state *"Cross-references to Block A use the canonical files `platform-suitability.md`, `application-architecture.md`, `data-architecture.md`, `automation-architecture.md`"* — and cite accordingly (*"Block A, AA-50"*, *"Block A AA-05, AA-06, AA-08"*, *"Block A `data-architecture.md`"*). `integration-architecture.md` and `architecture-patterns.md` both open with *"Research Status: DRAFT (**Block A**, first pass)"* and refer throughout to *"the Block A brief"*, meaning themselves.

**Why It Matters:** A pack author resolving *"Block A AA-50"* against the review brief's definition of Block A (integration + patterns) finds nothing, and may conclude the reference is broken. It also makes any instruction of the form "reconcile Block A with Block C" ambiguous.

**Required Correction:** Retire the phrase in favour of file names and area numbers, or fix one definition in `research-areas.md` and use it everywhere.

---

## 18. Recommended Research Follow-Ups

Ordered by decision impact. Items 1–4 are new research; 5–8 are closures of the corpus's own highest-value open Unknowns; 9–10 are hygiene.

1. **Governance and operations of the non-Power-Platform estate.** The single largest content gap (XB-06, XB-14). Scope: ownership and change control for APIM, broker, Function, worker and gateway assets; their deployment lifecycle relative to the Power Platform solution; monitoring and on-call; and the cost basis. Without it, six of ten patterns cannot be reviewed against five of seven dimensions.
2. **Microsoft Online Services SLA / Product Terms.** `operations-support.md` already names this a mandatory gate item (XB-10). Availability is the one dimension where a research gap becomes a contractual error.
3. **The Power Platform Licensing Guide PDF.** `licensing-cost.md` U-02: the authoritative document for every entitlement claim in the area, not retrieved. Closing it also closes U-05 (whether one premium connector obliges premium licensing for every user of the artefact), which the file grades *"load-bearing for LC-03, the file's largest finding"*.
4. **Comparator pricing, or the decision to reframe.** `licensing-cost.md` U-04 (XB-11). Either fetch pricing for the five named alternatives or convert §6 to a method. The second is cheaper and arguably more durable.
5. **Custom-connector throttle: 500 or 10,000 per minute per connection.** `integration-architecture.md` U-02 / C-01 (XB-07). A 20× sizing error on the platform's main extensibility mechanism, and now propagated into Block C as settled.
6. **Dual-write failure semantics under sustained far-side failure.** `integration-architecture.md` U-14, self-graded *"Material. A dual-write decision cannot be made responsibly without this"*, and absent from Blocks B and C entirely.
7. **Re-verification of the three connector reference pages** carrying the corpus's most decision-relevant throttle numbers (`ms.date: 2024-03-01` with 2026 update stamps) — `integration-architecture.md` §13.1 item 2.
8. **The four Block A checks and the four Block C checks each file nominates.** `integration-architecture.md` §1 names IA-12 (the 100 calls/60 s throttle), IA-22 (concurrency control can drop triggers), IA-31 (managed identity scope) and IA-45 (the SAP authorization self-contradiction); `architecture-patterns.md` §1 names AP-06, AP-07 and AP-10; `performance-scale.md` §12 names PF-22, PF-16, PF-41/PF-42 and PF-01/PF-02. Each file asked for independent verification; this review is structural and did not perform source-level re-verification.
9. **Whether Power Platform VNet support covers inbound calls** (`integration-architecture.md` U-09) and whether a VNet-supported plug-in can publish to Service Bus satisfying both private egress and transaction-scoped eventing (U-19 / `architecture-patterns.md` U-05). Both bear on the AP-03 private-network collision, which Block A calls *"the pattern's least-known and most consequential limitation"*.
10. **Cloud flow run-history retention from Tier 1** (`integration-architecture.md` U-21; `architecture-patterns.md` U-07). Currently a T3 claim of 30 days, load-bearing for every message-audit and replay verdict.

**One process recommendation.** Every file declares single-author, single-session research with self-review, and each names the checks a second reader should run. This review confirms the concern: the four CRITICAL findings are all defects that only a cross-file reader can see. Whatever gate is run on these files should be run **across** them, not file by file — a per-file gate would have passed all eight and found none of XB-01 through XB-04.

---

## 19. Final Review Verdict

## PASS WITH CORRECTIONS

**Why not PASS.** Four CRITICAL findings would produce materially wrong downstream work. A pack authored on the current corpus would: cost a security-hardened design without its largest licence line (XB-04); select six of ten architecture patterns with no governance, ALM or cost visibility (XB-06, XB-13); hand architects a seam artefact whose ALM hazards the corpus documents and never connects (XB-05); mis-resolve finding ids across five colliding namespaces (XB-03); and route readers to files it wrongly declares unresearched (XB-01). None of that is a matter of polish.

**Why not FAIL.** The failure is in the seams, not the substance. Each block is architecturally sound, epistemically disciplined and unusually honest about its own limits — negative evidence is collected deliberately and at length, Unknowns and Conflicts are recorded rather than resolved silently, vendor positioning is fenced on both sides of the argument, marketing adjectives are refused as evidence, and the absence of any empirical measurement is stated as a standing constraint rather than papered over. The specific test the brief sets — *can an architect reason from requirements to architecture without contradictory or incomplete guidance* — is met today for a Power-Platform-only solution. Where it fails, it fails for an identifiable class (architectures that cross the platform boundary) for an identifiable reason (Blocks B and C were produced in parallel isolation, and Block C recorded in writing that Block B did not exist). Most corrections are joins between findings that already exist; only three require new research, and two of those are document retrievals the corpus already nominates as mandatory gate items.

**The conditions attached to this verdict.**

1. Corrections **C1–C5** are blocking. Pack authoring must not begin until they land, because each one would otherwise be encoded.
2. Corrections **C6–C14** must land before the pack's pattern-selection and cost content is authored.
3. The gate must be run **across** the corpus, not file by file. Every one of the four CRITICAL findings is invisible from inside a single file, and all eight files currently read Gate NOT RUN or PENDING.
4. Until C6–C8 land, patterns AP-02, AP-03, AP-04, AP-05, AP-08 and AP-10 must be marked as carrying an **unquantified** governance, ALM and cost burden, and `architecture-patterns.md` Y-13 (*no operator makes the pattern unavailable*) must be encoded as a hard precondition rather than as advice.
5. The three self-declared corpus-wide epistemic constraints must survive into the pack as standing constraints, not research notes: no empirical measurement exists for any component; licence entitlements are never Confirmed facts; and no availability commitment may be derived from RTO/RPO figures.

**One closing observation, offered as a compliment rather than a caveat.** The best evidence in this corpus is Microsoft bounding its own products — *"Financial posting entities… are deliberately excluded from dual-write, avoiding any shadow-ERP behavior"*; *"To ensure all triggers result in flow runs, leave the Concurrency Control setting off"*; *"Don't use this information for real-time monitoring"*; *"Technical support doesn't conduct RCAs as part of any support experience"*; *"we recommend using the security score for evaluation purposes only at this time"*. Two files noticed this pattern independently and recorded it: the platform documents its own boundaries better than the independent commentary does. That observation is worth preserving, because it tells the next researcher where to look — and it is the reason this corpus, once its seams are closed, will support a defensible decision rather than an adoption case.
