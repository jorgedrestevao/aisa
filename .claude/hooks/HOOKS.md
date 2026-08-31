# Hooks — aisa MVP

The MVP ships 5 hooks in `.claude/hooks/`, wired in `.claude/settings.json`. `pre-write-guard.sh` **enforces** (hard-blocks writes to `library/`); the other 4 are log-only stubs until v0.2.0.

| Hook | Trigger | What it does today (MVP) | What it will do (v0.2.0) |
|---|---|---|---|
| `pre-write-guard.sh` | `PreToolUse` on `Write\|Edit` | **Hard-blocks** writes to `library/*` (`AISA_GUARD_MODE=enforce` is the default; graceful no-op if `jq` missing — the `settings.json` deny rules remain as backstop) | Durable Windows story (bundled `jq` or `.ps1` rewrite) |
| `phase-gate-check.sh` | `PostToolUse` on `aisa-frame\|aisa-options\|aisa-decide` | Logs that a phase transition ran | Validates `_state.json` + SU counts against the prior phase's exit criteria; warns on red gates |
| `on-su-change.sh` | `PostToolUse` on `Write\|Edit` to `shared-understanding.md` | Logs the change | Triggers a background contradiction-scan |
| `synthesis-validate.sh` | `PostToolUse` on `Write` to `_synthesis/*.md` | Logs the change | Validates ≥3 paragraphs, ≥1 SU citation, vendor-neutrality on the technology-neutral packs |
| `render-validate.sh` | `PostToolUse` on `Write` to `_render/*.md` | Logs the change | Validates required slots are non-empty, audience register matches, `render-gaps.md` updated |

## Enforce mode (the only hard guard)

`pre-write-guard.sh` runs in **enforce** mode by default: `.claude/settings.json` sets `AISA_GUARD_MODE=enforce` in `env`, and the script itself fails closed (an unset variable also means enforce). Two layers back it up: the hook (exit 2 blocks the tool call) and the `permissions.deny` rules for `Write/Edit(./library/**)` in `settings.json`. The other 4 hooks are pure log in MVP; they have no enforce mode yet.

For administrative authoring (populating a pack, editing kernel docs), the sanctioned path per `.claude/rules/library-readonly.md` is an out-of-band edit + `git commit`. If you must work in-session, temporarily set `AISA_GUARD_MODE=log` — and remember the `settings.json` deny rules still apply until removed locally.

## jq dependency

Every hook uses `jq` to parse the JSON payload `Claude Code` pipes in. On Windows machines without `jq`, all hooks degrade gracefully to a no-op (a stderr line). This is intentional MVP behaviour — the durable Windows decision (bundle `jq` vs rewrite hooks in `.ps1`) is deferred to a v0.2.0 task.

## Adding a new hook

1. Drop the script in `.claude/hooks/`. Mark executable (`chmod +x`).
2. Follow the existing pattern: jq presence check first; then parse `tool_name` + `tool_input.file_path` (or `tool_input.skill`); then act.
3. Wire it in `.claude/settings.json` under the right matcher.
4. Default to log-only. Add an `AISA_*_MODE=enforce` env switch when you can promote to a hard block.
