# Rule: library/ is read-only at runtime

`library/` contains the kernel + packs — the canonical, validated assets. Never edit at runtime.

- Do NOT Write/Edit/Delete anything under `library/`.
- Reading is fine (Read, Grep, Glob).
- Out-of-band administrative edits via git commit are the sanctioned path.

Enforced by hook `pre-write-guard.py` (fail-closed) + `settings.json deny`.
