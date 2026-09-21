# Step 8C fixtures

Bounded fixtures for `.claude/tests/test_step8c_semantic_continuity.py`. They are **test data**, not
engagement state: the `pricing-marinha-*` files are a static re-capture of the Pilot-1 evidence
(the normalized `_capture/*.text.md`, the PM ids of `process-model.md`, the SU ids that exist in the
engagement) rewritten in the 1.8.2 contract shape, so the new contracts can be proven against the real
semantic shape without touching `projects/pricing-marinha/**`. Ids `C-070+`, `U-032+`, `A-010+` are
fixture-added rows (what the disposition step would have created), not engagement rows.

| File | Used by |
|---|---|
| `pricing-marinha-synopsis.md` | CS-1..CS-5, PMU-*, static proof |
| `pricing-marinha-pmu.md` | PMU-1..PMU-5 |
| `pricing-marinha-su-excerpt.md` | PMU, FS, static proof |
| `pricing-marinha-open-evidence.md` | disposition coverage (CS-5, PMU-4) |
| `pricing-marinha-frame-survival.md` | FS-1..FS-5 |
| `c057-blueprint-v01.yaml`, `c057-blueprint-v02.yaml`, `c057-blueprint-v03-defect.yaml` | SI-1..SI-5, C-057 regression |
| `c057-decisions-excerpt.md`, `c057-options-excerpt.md` | SI-3, C-057 regression |
