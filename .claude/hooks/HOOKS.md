# Hooks — aisa MVP

The MVP ships 5 hook stubs in `.claude/hooks/`. All run in **log-only mode** until v0.2.0. They are wired in `.claude/settings.json`.

| Hook | Trigger | What it does today (MVP) | What it will do (v0.2.0) |
|---|---|---|---|
| `pre-write-guard.sh` | `PreToolUse` on `Write\|Edit` | Logs writes to `library/*` (graceful no-op if `jq` missing) | Hard-blocks writes to `library/*` when `AISA_GUARD_MODE=enforce` |
| `phase-gate-check.sh` | `PostToolUse` on `aisa-frame\|aisa-options\|aisa-decide` | Logs that a phase transition ran | Validates `_state.json` + SU counts against the prior phase's exit criteria; warns on red gates |
| `on-su-change.sh` | `PostToolUse` on `Write\|Edit` to `shared-understanding.md` | Logs the change | Triggers a background contradiction-scan |
| `synthesis-validate.sh` | `PostToolUse` on `Write` to `_synthesis/*.md` | Logs the change | Validates ≥3 paragraphs, ≥1 SU citation, vendor-neutrality on the technology-neutral packs |
| `render-validate.sh` | `PostToolUse` on `Write` to `_render/*.md` | Logs the change | Validates required slots are non-empty, audience register matches, `render-gaps.md` updated |

## Enforce mode (the only hard guard today)

Set `AISA_GUARD_MODE=enforce` in the environment (or via `.claude/settings.json` `env`) to switch `pre-write-guard.sh` from log to hard-block on `library/*` writes. The other 4 hooks are pure log in MVP; they have no enforce mode yet.

In administrative authoring (populating a pack, editing kernel docs) — temporarily unset `AISA_GUARD_MODE` or work via a `git commit` to `library/` outside the runtime, which is the sanctioned path per `.claude/rules/library-readonly.md`.

## jq dependency

Every hook uses `jq` to parse the JSON payload `Claude Code` pipes in. On Windows machines without `jq`, all hooks degrade gracefully to a no-op (a stderr line). This is intentional MVP behaviour — the durable Windows decision (bundle `jq` vs rewrite hooks in `.ps1`) is deferred to a v0.2.0 task.

## Adding a new hook

1. Drop the script in `.claude/hooks/`. Mark executable (`chmod +x`).
2. Follow the existing pattern: jq presence check first; then parse `tool_name` + `tool_input.file_path` (or `tool_input.skill`); then act.
3. Wire it in `.claude/settings.json` under the right matcher.
4. Default to log-only. Add an `AISA_*_MODE=enforce` env switch when you can promote to a hard block.
