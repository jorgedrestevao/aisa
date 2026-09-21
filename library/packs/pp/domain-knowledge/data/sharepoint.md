# SharePoint and Lists as the store — what the list and library store supports

<!--
provenance: RUNTIME (domain knowledge) · class: RESEARCH
authored: 2026-09-04 (Step 4B) · design authority: Step 4A — Domain Knowledge Runtime Model
Pull-based: consulted when a concrete decision question requires it (decision-tree.md §9).
Never preloaded. Canonical research traceability lives in the Step 4B authoring report.
-->

## 0. When to pull this file

- *What does this store not enforce, and what is its documented ceiling on this access path?*
- *Is this one of the shapes for which it is the documented answer?*
- *What happens to this requirement as the list grows — and what is the observable condition that ends it?*
- *What does putting the record here move into the collaboration-site governance model?*

This file states **what the list and library store enforces, what it does not, the mechanics that bound an
access path, and the observable conditions under which it stops being able to support a requirement**. It
does not decide **which store wins** — that belongs to the decision model (`decision-tree.md` S4–S6). There
is no architecture branch named for this store here, and no disqualification threshold: this file carries
capability boundaries, not exclusions.

---

## 1. What this is for · `decision-grade`

Two different questions get asked about this store and they have different answers.

- *"Can the list store hold this data?"* — almost always yes. The per-list item ceiling is orders of
  magnitude above every other boundary in this file, so **capacity is never the binding question**.
- *"Can it support this requirement on the access paths this solution needs?"* — this is the real question,
  and it is answered by the view/query mechanics (§5), the enforcement gaps (§4) and the security
  granularity (§4), not by row count.

The store is a **document and collaboration store with a list surface**, governed by collaboration-site
policy. Where the requirement is document-shaped it is the vendor's own named answer (§3). Where the
requirement is relational, integrity-bearing or per-person-scoped, the gaps in §4 are what decide the
design work — and they are gaps in *enforcement*, which means the app cannot close them.

## 2. When it becomes material · `decision-grade`

- The **document itself is the record** — file plus metadata, versions, and protection that must travel
  with the file when it is downloaded.
- The entity is **flat**, with minimal relational depth, and the audience already holds the seeded
  entitlement for the standard connector class.
- Security is required at **list level or by a few groups**, not per person per row.
- A **form over one list** is the whole solution surface.
- Conversely: the requirement mentions referential integrity, multi-row atomicity, field-change audit,
  per-person row visibility at scale, column confidentiality, a rule that must hold on integration paths,
  or trustworthy BI over the operational store. Each of those is a §4 gap.

## 3. The shapes for which this store is the documented answer · `decision-grade`

These are **positive documented fits**, and they are not consolation prizes.

| Shape | What the store natively provides |
|---|---|
| **The document is the record** | Libraries with metadata columns, versioning, retention labels, and sensitivity labels that keep protection attached to the file after download |
| **Files + metadata + versions + protection** | Full retention coverage on library files; a multi-month recycle-bin window; native version history as a recovery mechanism |
| **Small flat trackers with minimal relational depth** | List surface, forms, views, per-column validation on write, list-level permissions — with no premium connector class required |
| **List-level or few-group security** | Site and list permission scoping, inherited by customised forms |
| **A form over one list** | The whole requirement is a single-entity capture surface with no relational depth and no cross-row rule |

The vendor's own composite pattern pairs this store with the governed relational store — structured business
data in the relational store, documents here — and states plainly that the relational store is the preferred
choice where **more complex relational data** is needed. Read that as a **trigger for the pairing**, not as a
ranking of stores.

> The pairing inherits **two security models that do not synchronise**. The vendor states that the intent of
> the pattern is *not* to enforce security at the item level of this store, and that the pattern is not
> suitable where strict file-level security is required for compliance. A hybrid therefore needs an explicit
> permission-sync design, or an accepted decision to hold document control at discoverability level.

## 4. What this store does not enforce · `decision-grade`

This is the section the file exists for. Each row is a **capability absence**. Where the consequence lands
is stated; the verdict is not.

| Requirement | What the store enforces | Where the consequence lands |
|---|---|---|
| A rule that must hold **whichever client writes** | Single-row, single-column validation formulas evaluated on write, with a user message. The formula engine is **row-local**: it cannot reference another row, another list, or another library | Cross-row, cross-list and aggregate rules have **no declarative option here**; they become code plus an owner. Users holding list edit rights write through the list UI, a spreadsheet export or the graph API regardless of the app's own form |
| **Referential integrity** | Opt-in **per lookup**, and **delete-only** — restrict-delete or cascade-delete. Requires a list-management permission, and stops working past the store's scale threshold | No integrity on insert or update, no composite keys, no native many-to-many. Integrity moves into the app and into automation |
| **Uniqueness** | A single-column *unique values* setting | Multi-column or business-key uniqueness has no store mechanism; idempotent integration has no upsert key here |
| **Multi-row atomicity** | Nothing. There is no transaction | Partial failure leaves orphans. A unit of work over two lists cannot be made all-or-nothing at the store |
| **Concurrent edits on one item** | No conflict setting; **last writer wins**. Version history is *recovery*, not concurrency control | Silent overwrite between two users is a documented outcome, not an edge case. Whether the app client sends a concurrency token on update is **not established** (§11) |
| **Row visibility per person at scale** | Unique per-item permissions up to a supported ceiling of **50,000** scopes per list, with a **recommended** ceiling of **5,000**; inheritance cannot be broken past **100,000** items *(documented reading · read 2026-09-04 · re-verify: `VS-29`)* | "Each requester sees only their own records" needs per-item ACL automation, which the vendor's own pattern calls *significant operational overhead* |
| **Column confidentiality** | **No column-level security.** Hiding a field in the app is cosmetic — the vendor states app-granted permissions do not deny the data-source permissions the user already has | A confidential field in a list is readable by anyone with list read access, through any client |
| **Field-change audit** | Versioning only; **attachment changes are not tracked** | An audit obligation over field values needs a different mechanism, and versioning does not answer *who changed which field when* as a queryable trail |
| **Derived data** | Calculated columns, restricted to the same functions as the validation engine and to the **same row** | No cross-row rollups, no cross-list aggregation. Derived values become scheduled or event-driven automation, with its own loop-prevention and reconciliation concerns |

> The honest form of *"server-enforced rules exist only in the relational store"* is narrower and worth
> carrying exactly: **this store enforces single-row, single-column validation on write; only the governed
> relational store offers cross-column server rules, relational integrity and multi-column uniqueness keys;
> and neither store offers declarative cross-row validation.**

## 5. Indexing, views and the ceiling on an access path · `decision-grade`

The binding constraint is **query shape**, not volume.

- There is a documented **per-view item threshold** which the vendor states **cannot be changed** in the
  online service, and which exists so that tenants sharing infrastructure keep predictable query
  performance. Past it, a view or query without an indexed, selective filter **fails** rather than
  degrading.
  > Documented reading · read 2026-09-04 · re-verify: VS-04 (design time)
  > (per-view item threshold: **5,000** items; per-list item ceiling is in the tens of millions and is not
  > the binding boundary)
- **The list works only if every access path is indexable and selective.** That is a statement about the
  *set of paths*, not about the list: one unindexed sort or one negation in a common view is enough to
  break the surface even though every other path is fine.
- **Join columns per view are capped at a low fixed number** — lookup, person and metadata columns all count
  against it, and the flow actions that retrieve list items and files **fail** above the same ceiling rather
  than returning a partial set. The vendor's own performance guidance for this store is to **denormalise
  people columns** and to **partition a large list across several lists** — the opposite of relational
  design, and a signal in its own right.
  > Documented reading · read 2026-09-04 · re-verify: VS-33 (design time, per access path)
  > (**12** join-type columns per view, counting lookup, person and metadata columns together)
- There is a **row-byte budget** across a list's columns, independent of the column count.
- **The canvas client cannot project columns.** Every column defined on the list is retrieved and
  transmitted, whether the screen uses it or not. Wide lists therefore cost bandwidth on every read.
- **Flow item retrieval pages by default** at a small page size and **fails** past the view threshold
  unless pagination is configured; with a filter that matches nothing inside the first page window, it can
  return **no records** rather than an error.
- **Delegation depth is not restated here.** The delegable operation set for this store is the narrowest of
  the connector-backed stores and the authority for it is `data/query-and-delegation.md`. Read the ceiling
  and the operation table there; do not reconstruct either from memory.
  > Documented reading · read 2026-09-04 · re-verify: VS-02 (design time, per data source)

**Why this is decision-grade rather than build detail.** The failure mode of an unindexed path past the
threshold is a *silently wrong result set*, not a slow one. Where the requirement is *"a missing row is a
business error"* — registers, approvals, inventory, anything reconciled — silence is the disqualifying
property, and it is a property of the access path, which is knowable at Options time.

## 6. Binaries, documents and protection · `decision-grade`

- **Libraries are native at a high per-file size ceiling**, with metadata columns, versioning and a
  multi-month recycle-bin window. This is the store's strongest documented fit.
- **Sensitivity labels attach protection to the file** and keep it attached when the file is downloaded —
  the one mechanism in the platform's store set that does this. It covers the mainstream office document,
  portable-document and video formats.
  - Encrypted files require the service-processing option to be enabled, or co-authoring, discovery,
    loss-prevention and search cannot process them.
  - Large encrypted files **break on move** above a documented size.
  - **There is no label mechanism for list items or list columns**, and none for the governed relational
    store's rows or file columns. Labels are a *file* mechanism.
- **Retention labels apply to list items; retention policies do not.** And a label on an item does **not**
  automatically cover the item's **attachment** — library files get full retention coverage, item
  attachments do not.
- **Attachments on list items are not a document store.** They carry no metadata, no indexing and no
  per-file lifecycle. Where files are the point, the library with metadata columns is the store, not the
  attachment slot.

## 7. Decision-sensitive distinctions · `decision-grade`

- **The store's owner is not the app's owner.** Lists live on a collaboration site, governed by that
  service's administrators and its collaboration policy: **external sharing is on by default** at the
  service level; a guest added as a site member holds edit rights and **can delete lists and items**; and
  an inactive-site policy can set the site read-only or archive it — which locks the application's store as
  a side effect of a policy the app team does not own.
- **Lists sit outside the solution boundary.** The schema does not travel with the application. Moving
  between environments needs site and list environment variables plus a live connection, and if the lists
  are **recreated** in the target rather than the site duplicated, **the internal names do not match** —
  the vendor's own mitigation is to duplicate the site. Internal-name drift is a silent breakage across
  every formula, filter and flow expression that names a column.
- **"Customer-managed keys are not possible here" is wrong.** A dedicated **tenant-or-geo-scoped**
  encryption policy exists for this store's content, with a documented key-revocation path that
  cryptographically deletes the data. What is actually limited is **granularity** — one policy per tenant,
  or per geography in a multi-geography tenant, with **no scoping to a site, a library or one
  application's data** — plus a premium suite entitlement, **paid** cloud subscriptions (the free, trial,
  sponsorship and legacy tiers are ineligible), a separate onboarding path for this store, and key vaults
  configured with soft-delete and purge protection. So: it fails a requirement for a **scoped** key. It
  does not fail a requirement for a customer-held key as such. Any store comparison carrying the old
  wording mis-scores this store.
- **Downstream reporting inherits three documented defects, not one.** Boolean values are represented
  inconsistently unless the column type is set explicitly, which the vendor states *"might result in wrong
  data, incorrect filters, and empty visuals"* — a silent wrongness with a manual, per-column, recurring
  mitigation. The quick export path **refuses to create the model** where a value carries decimal precision
  past a documented limit. And the **sensitivity label of the list is not inherited** by the created model:
  classified data in a list becomes an unclassified semantic model. That last one is a governance
  regression caused purely by the store choice plus the quick path.
- **"Who owns the data" acquires a second, undocumented answer.** What a report shows is determined by the
  **permissions of the identity that established the connection**, and re-authenticating can retroactively
  change what other people's existing reports show. No governance artefact captures that identity.
- **The seeded entitlement pairs the least capable store with the least capable automation profile.** The
  standard connector class is usable on the suite's seeded rights, but the flows that run on it sit in the
  lowest performance profile (bounded loop item counts, a bounded daily request allowance, fewer retries),
  this store's change triggers are **polling-based** with changes coalescing between polls, the delete
  trigger requires a site-collection-administrator identity, and item-menu flows exist only in the default
  environment — the weakest lifecycle surface the platform has. Cost, not fit, is the usual driver for
  choosing this store as a database; the pairing is what that choice actually buys.
  > Documented reading · read 2026-09-04 · re-verify: VS-03 (design time, and on any licence change) ·
  > `VS-14` for the polling interval, `VC-03` for the connector's permissibility posture

## 8. Graduation triggers — the observable conditions that end the fit · `decision-grade`

**These are capability boundaries observed on the requirement, not thresholds, not scores and not
exclusions.** Whether a boundary excludes an option is the decision model's question, and the answer may be
to change the requirement, add engineering, or accept the gap. None of these is a row count.

1. **A missing row is a business error** *and* at least one required access path cannot be made both
   indexed and selective. → §5. The failure is silence, and no app-side control removes it.
2. **A rule must hold on every write path**, including the API and the integration path. → §4. Nothing here
   reaches beyond the row and the single column.
3. **A cross-row or cross-entity rule appears** — no overlapping bookings, sum of lines equals header,
   this code must exist in the reference list. → §4. This converts the work to code **regardless of which
   store is chosen**, and it is the store's *hardest* rule, not its average one, that governs.
4. **Per-person row visibility is required at a scale beyond the recommended unique-permission ceiling**, or
   a field must be visible to some roles only. → §4. There is no column-level mechanism at all.
5. **A queryable field-change audit trail** is an obligation. → §4.
6. **Relational depth grows past a lookup or two per entity**, or the vendor's own mitigation
   (denormalise, partition across lists) becomes necessary. → §5. Needing to partition an entity across
   lists is itself the signal.
7. **Multi-row atomicity** is required. → §4.
8. **Real BI over the operational store, or any classified data reaching a report.** → §7. The remediation
   cost lands downstream, after build.
9. **The store must be owned and lifecycle-managed by the application team**, with controlled dev → test →
   prod schema change. → §7. The schema does not travel; the site governance is not the app team's.

**And the migration is not free.** Where growth past these boundaries is plausible **within the
application's life**, the move must be priced at decision time, not discovered later: the vendor's own
conversion path from a list to the governed relational store is a **one-time copy, not a sync**, and it
**excludes** several column classes outright — image, task-outcome, external-data, managed-metadata,
attachment and unique-value columns among them. Permissions are re-implemented from scratch.

## 9. Failure modes · `decision-grade`

> **Store choice made to stay inside the seeded entitlement, for a requirement the store does not support.**
> The entitlement saved is real. So is the rebuild, and so is the automation profile that comes attached
> (§7). This is the single most common way this store is chosen.

> **An unindexed or non-delegable access path past the view threshold.** The result set is silently
> truncated or empty rather than erroneous. Reconciliation discovers it, weeks later, as missing business
> records.

> **Per-item permission automation as the row-security model.** Breaking inheritance, driving graph
> automation and managing access at scale is described by the vendor's own pattern as significant
> operational overhead — and it degrades as the list grows, because inheritance cannot be broken past a
> higher item count.

> **Hiding a confidential field in the app.** App-granted permissions do not deny the data-source
> permissions the user holds. The field is readable through the list UI, a spreadsheet export or the graph
> API, by anyone with list read access.

> **A calculated column that reaches beyond its own row** — another row, another list, a second calculated
> column. The formula engine is row-local; the outcome is a silent wrong value, not an error.

> **Attachments on list items used as the document store.** No metadata, no indexing, no per-file
> lifecycle — and retention labels on the item do not cover the attachment.

> **Recreating the lists in the target environment instead of duplicating the site.** Internal names do not
> match, and every formula, filter and flow expression that names a column breaks at once.

> **The quick export path to reporting over classified list data.** The sensitivity label is not inherited;
> classified data becomes an unclassified model. The regression is invisible at the moment it happens.

> **A guest with edit rights on the site holding the application's store.** They can delete lists and
> items. External sharing is on by default at the service level, so this is the default posture, not a
> misconfiguration.

## 10. Consequences elsewhere · `decision-grade`

- **→ `data/store-boundaries.md`** — the cross-store capability map and the *view-or-data* question sit
  there; this file is the depth behind this store's column.
- **→ `data/query-and-delegation.md`** — the delegable operation set, the client paging cliff and the
  access-path discipline are that file's authority. **Never restated here.**
- **→ `security/security-controls.md`** — no column-level security, coarse row scoping, app-side filtering
  being cosmetic, the tenant-or-geo granularity of the customer-key policy, and label-based file protection
  as the one mechanism that survives download.
- **→ `governance/governance-and-environments.md`** — the store is governed by collaboration-site policy and
  its administrators, not the app owner: external sharing default, guest edit rights, inactive-site
  read-only and archive policies, site ownership turnover, and the default-environment-only item-menu
  automation.
- **→ `operations/operability-and-support.md`** — index-before-load sequencing, archive and housekeeping
  jobs, the recycle-bin window as a recovery mechanism and not an archive, and an erasure run-book that has
  to reach items, attachments, library files and every downstream model copy.
- **→ `integration/integration-mechanisms.md`** — polling-based change triggers with coalescing changes, the
  per-connection call allowance, pagination as an explicit design decision, and the absence of any store
  uniqueness key to make an integration idempotent.
- **→ `economics/licensing-and-cost-drivers.md`** — the standard connector class rides seeded entitlement,
  which is the store's real gravity; the customer-key path adds a premium suite entitlement and paid
  subscriptions; and the migration out is a priced event. Unit, meter and entitlement shape live there.
- **→ `alm/release-and-lifecycle.md`** — lists outside the solution boundary, environment variables for site
  and list, internal-name drift, and the one-time-copy nature of the conversion out.
- **→ `craft/screen-patterns.md`, `craft/flow-craft.md`, `craft/delivery-conventions.md`** — indexed-column
  budgeting, filtered view sets, validation formula authoring, archive-flow shapes, forbidden internal
  names and loop-prevention patterns are **delivery practice**, not platform limits, and are never an
  Options pull target.

## 11. What must be verified · `decision-grade`

| Fact | Register row |
|---|---|
| The per-view item threshold — the access-path boundary | `VS-04` |
| The unique-permission scope ceilings, and the item count above which inheritance can no longer be broken | `VS-29` |
| Delegation ceilings for this store (default and maximum) | `VS-02` |
| The content-throughput-per-24-hours meter for the seeded owner profile | `VS-03` |
| Change-trigger polling interval, per connector | `VS-14` (also `VC-02`) |
| Whether this store's connector is still in the permissible set for the target environment's policy | `VC-03` |
| Whether the required capability set still fits the seeded entitlement | `VC-05` |
| Preview and general-availability states of any feature relied on | `VC-10` |

**Not established in the baseline — do not fill from general knowledge:**

- **The maximum number of indexed columns for the online service.** Only the on-premises server figures were
  sourced. Any "index budget" number carried into a design here is invention. Read the current support
  page directly.
- **An explicit vendor statement that lists have no column-level security.** The absence is well
  corroborated but rests on the *absence* of a page, not a positive statement. Treat as strongly supported,
  not quoted.
- **Whether the app client sends a concurrency token on item update**, and whether any multi-item
  transaction exists. Do not assert either way.
- **The delete behaviour of an unenforced lookup** — the sources **conflict** on whether the target item is
  removed or the lookup value merely emptied. Verify on the page directly before designing around either.
- **The volume and refresh behaviour of the current reporting connector for this store** past the view
  threshold. Not established.
- **Per-gigabyte storage economics for this store.** No supported figure; and no price belongs in this file
  in any case.

**One live conflict is symmetric and worth naming here.** Where a design fronts this store with a custom
connector to work around a boundary above, the **throughput ceiling of that mechanism is `CONFLICTED`** —
two maintained vendor pages disagree by an order of magnitude. Any sizing or economics resting on it is
**decision-blocked until measured**, and that blockage falls **equally** on every option class, platform and
non-platform alike (`VC-01` / `VS-08`, blocking entry `B-08`, composed row `CD-05`). Encode neither figure.

## 12. What not to infer · `decision-grade`

- **A capability absence is not a verdict.** *"No column-level security"* and *"no transaction"* are domain
  knowledge. *"Therefore unsuitable"* is a selection verdict and belongs to `decision-tree.md`.
- **There are no thresholds here, and none should be reconstructed.** Row-count gates and formula-count
  gates were **removed** from the decision model. Restating one — in any form, however plausible — puts a
  deleted rule back into the reasoning. The graduation triggers in §8 are capability conditions, and every
  one of them can be true at a small volume and false at a large one.
- **There is no architecture branch named for this store**, and this file names none.
- **A documented boundary here is not evidence that another option class performs better.** The baseline
  holds no like-for-like evaluation of hosted software, custom builds, incumbent platforms or other
  low-code stacks against this store. Where that comparison is material, the comparator semantics in
  `decision-model/outcome-classes.md` stand.
- **Do not read the vendor's composite pattern as a ranking.** *"The relational store is preferred where
  more complex relational data is needed"* is a **trigger**, and the pairing it recommends inherits two
  unsynchronised security models (§3).
- **Do not restate the delegation table** from memory or from any other file. It lives in
  `data/query-and-delegation.md` and nowhere else.
- **Do not treat versioning as audit, the recycle bin as an archive, or a validation formula as a
  constraint** — each is a different mechanism with a different guarantee.
