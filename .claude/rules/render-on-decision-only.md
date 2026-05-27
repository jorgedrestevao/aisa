# Rule: render only after /decide

Producing deliverables (`/render`) before the Decision phase is forbidden:

- Discovery, Framing, Options phases do not have complete information to render Implementation Spec, Estimate, Blueprint.
- A render attempt before /decide will fail with explicit `render-gaps.md` warnings.
- The transition is: `/decide` → auto `/synthesize` → manual `/render --all`.

Exception: in development/debugging, `/render --dry-run` can preview against current state without writing to `_render/`.
