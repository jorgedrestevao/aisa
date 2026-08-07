# Hooks — aisa

All hooks are written in **Python 3** (single source-of-truth, cross-platform: Windows, macOS, Linux). Wired in `.claude/settings.json` via `python .claude/hooks/<name>.py`.

| Hook | Trigger | Behaviour |
|---|---|---|
| `pre-write-guard.py` | `PreToolUse` on `Write\|Edit` | **Log mode (default):** warns on writes to `library/*`. **Enforce mode** (`AISA_GUARD_MODE=enforce`): hard-blocks (exit 2) with `permissionDecision=deny`. |
| `pre-lens-order-check.py` | `PreToolUse` on `Skill` | **Always active.** Blocks invocation of `lens-N` if `lens-(N-1)` has not written `lens-outputs/<prev>.md` containing the in-progress round ID (`_state.json.round + 1`). Only triggers when an engagement is in `phase: discovery`. |
| `phase-gate-check.py` | `PostToolUse` on `Skill` | **Log only (MVP).** Logs when `aisa-frame`/`aisa-options`/`aisa-decide` ran. v0.2.0 will validate `_state.json` + SU counts against phase exit criteria. |
| `on-su-change.py` | `PostToolUse` on `Write\|Edit` | **Log only (MVP).** Logs Writes/Edits to `shared-understanding.md`. v0.2.0 will trigger a background contradiction-scan. |
| `synthesis-validate.py` | `PostToolUse` on `Write\|Edit` | **Log only (MVP).** Logs Writes to `_synthesis/*.md`. v0.2.0 will validate ≥3 paragraphs, ≥1 SU citation, vendor-neutrality on technology-neutral packs. |
| `render-validate.py` | `PostToolUse` on `Write\|Edit` | **Log only (MVP).** Logs Writes to `_render/*.md`. v0.2.0 will validate slot completeness, audience register, `render-gaps.md` sync. |

## Enforcement modes

| Mode | Activation | What enforces |
|---|---|---|
| Log-only | Default (`AISA_GUARD_MODE=log` or unset) | All warnings to stderr; no blocking except the order check below. |
| Enforce | `AISA_GUARD_MODE=enforce` | `pre-write-guard.py` hard-blocks `library/*` writes. |
| Always-on | n/a | `pre-lens-order-check.py` — the lens-order rule is a correctness invariant, not a preference. No log mode. |

## Why Python (and not bash / PowerShell)

The original MVP shipped bash `.sh` hooks parsing JSON via `jq`. On Windows machines without `jq` (common), the hooks degraded silently to no-op — the lens-order rule wasn't enforced and `pre-write-guard` couldn't run in enforce mode. The fix considered three options:

| Option | Verdict |
|---|---|
| Bundle `jq` for Windows | Adds binary dependency; still leaves PowerShell-vs-bash divergence on Win. |
| Maintain `.sh` + `.ps1` in parallel | Drift-prone: any logic change must be applied twice; bugs diverge silently. |
| **Port to Python** | Single source of truth, no external deps (stdlib `json` + `pathlib`), works on every dev machine, faster startup than PowerShell. ✓ |

Python 3.6+ on `PATH` is the only runtime requirement.

## Robustness notes

- **Stdin BOM tolerance.** When PowerShell pipes JSON to a native process, the byte stream may include a UTF-8 BOM (or worse, the BOM re-encoded through Windows-1252 → `ï»¿` as three characters). Each hook strips any leading characters before the first `{`/`[` before calling `json.loads`. Without this, hooks silently failed on Windows in early testing.
- **Engagement root resolution.** `pre-lens-order-check.py` honours `$AISA_ENGAGEMENTS_ROOT` if set, otherwise falls back to `projects/`. Finds the active engagement among children whose `_state.json.phase == "discovery"`. When several are in discovery at once (e.g. stale test fixtures alongside a live engagement), it picks the **most recently touched** one — newest mtime across `_state.json`, `shared-understanding.md`, and `lens-outputs/*.md` — so the round in progress always resolves to the engagement actually being written. A single discovery engagement resolves exactly as before.
- **No active engagement → silent pass.** A hook never blocks when there is no active Discovery engagement — running unrelated skills outside an engagement is always allowed.

## Adding a new hook

1. Create `.claude/hooks/<name>.py`. Follow the existing pattern:
   - Read stdin, strip leading non-JSON bytes, parse with `json.loads`.
   - Inspect `tool_name` + `tool_input.*` fields.
   - To block: print a `{"hookSpecificOutput": {"permissionDecision": "deny", "permissionDecisionReason": "..."}}` JSON to stderr and `sys.exit(2)`.
   - To allow: `sys.exit(0)`. Print informational logs to stderr.
2. Register it in `.claude/settings.json` under the appropriate matcher.
3. Test by piping JSON via `<payload> | python .claude/hooks/<name>.py` and asserting the exit code + stderr.
