# Hooks — aisa

All hooks are written in **Python 3** (single source-of-truth, cross-platform: Windows, macOS, Linux). Wired in `.claude/settings.json` via `python "${CLAUDE_PROJECT_DIR:-.}/.claude/hooks/<name>.py"` (see *Invocation and the project root* below — a relative command breaks the moment the session's cwd moves). `pre-write-guard.py` **enforces** (hard-blocks writes to `library/`), `pre-lens-order-check.py` is always on, and `on-su-change.py` regenerates the living dashboard, `su-confirmed-guard.py` warns on `Confirmed` rows without a resolvable locator; the other 3 are log-only stubs until they gain validation logic. **No hook is the mechanism**: every check a hook surfaces also runs explicitly from the skill that owns it, with the CLI command printed in its own steps — a session where no hook fired loses visibility, never enforcement.

| Hook | Trigger | Behaviour |
|---|---|---|
| `pre-write-guard.py` | `PreToolUse` on `Write\|Edit` | **Hard-blocks** writes to `library/*` (exit 2 + `permissionDecision=deny`). **Fails closed**: enforce is the default, an unset `AISA_GUARD_MODE` also means enforce. `AISA_GUARD_MODE=log` is the administrative override (warn only). |
| `pre-authority-guard.py` | `PreToolUse` on `Write\|Edit` | **Hard-blocks** a write to an engagement's authority when the kernel has not reconstructed its state (exit 2 + `permissionDecision=deny`). The authorities are `shared-understanding.md`, `decisions.md`, `answers.md` and `_state.json` at the engagement root, plus everything under `_graph/` and `_ops/` — the graph is operational authority (the context is built from it) and `_ops/` is the barrier (pending marker + receipts). Both are written by `operation.py` in Python, which does not pass through this hook, so a `Write`/`Edit` against those paths is by construction a hand edit of coordinated state. It calls `bootstrap.py` and refuses unless `ready`; the refusal carries the limitation AND the action that clears it. **Fails closed**: a bootstrap that cannot be evaluated is not the same as one that was evaluated. A folder with no `_state.json` is `/start` creating it — nothing to reconstruct, so it passes. `AISA_GUARD_MODE=log` is the administrative override. |
| `pre-lens-order-check.py` | `PreToolUse` on `Skill` | **Always active, full rounds only.** Blocks invocation of `lens-N` if `lens-(N-1)` has not written a section header for the in-progress round (`## R-NN …` in `lens-outputs/<prev>.md` — header match via `dashboard.py::lens_wrote_round`, never a substring; round = `round_in_progress` when ahead of `round`, else `round + 1`). Stands aside when `_state.json.round_lenses` names this round, says `modo: single` and lists the lens (`/round <lens>`: any lens, alone, any order); a free-text `round mode: single` in the invocation is a secondary signal. No record for this round and this lens → polices (fail-closed). Only triggers when an engagement is in `phase: discovery`. |
| `phase-completeness.py` | `Stop` | **Active.** When the turn ends, checks whether the current phase's skill wrote everything its `Outputs (written)` section promises — `frame.md` + the single sentence + `chairman-synthesis-F-NN.md` + 6 `_council-prep` excerpts + SU rows for the round + council-log (and, separately, the validation closure: `D-001` and the story episode). Same for Options (7 personas, ≥3 options, the recommendation section, and the `DO-NOTHING` / `PROCESS-CHANGE` class-coverage lines declared in the round's log — the **declaration**, never the class) and Decision (`D-NNN`, 5 topic packs, SU row, frozen counterfactuals — plus, **only once a non-draft blueprint version actually exists**, the reconciliation review and the coverage review of the current version; right after `/decide` there is no design to cover, so nothing is asked and nothing is reported). Reports to stderr, **never blocks**, always exits 0. Silent when the phase is complete. Runs standalone too: `python .claude/hooks/phase-completeness.py --engagement <slug>`. |
| `phase-gate-check.py` | `PreToolUse` on `Skill` | **Active.** Before `aisa-frame`/`aisa-options`/`aisa-decide` runs, evaluates the exit criteria of the phase that is ENDING (`library/kernel/phases.md`, via `dashboard.py::gate_state`). Each criterion carries its **mode** — `codigo` (a count, a presence, a marker), `juizo` (the skill judges: the comprehension test), `n/a` (nothing mechanical to read: `decision-tree.md` consulted). Coverage is declared as *n de m por codigo*, never as *gate OK*, and a per-option criterion with zero options is `n/a`, never a vacuous ok. Writes one append-only line to `<engagement>/gate-log.md` — the only writer of that file — with an id that fingerprints the STATE judged (ids of the open rows, sha of `decisions.md`/`options.md`/`frame.md`/the lens outputs, plus each criterion's result), so a later `--override` line carries `refers: <same id>` when nothing moved and a new id with `refers: none` when it did. The engagement is explicit (`--engagement <slug>`, passed by the three commands); with several mounted and no slug it writes NOTHING and says `not evaluated (ambiguous engagement)`. Reports, never blocks, exits 0. **Since the audit of `212cdc6` it also consults the kernel** (`bootstrap.py`) and appends `· kernel: <limitation>` to the line when the state is not reconstructed — the criteria are still computed and written. The limitation rides ALONGSIDE the verdict, never instead of it: this is a soft METHODOLOGICAL gate, and turning it into an integrity block is a different thing. What blocks on integrity is `pre-authority-guard.py`. |
| `on-su-mirror.py` | `PostToolUse` on `Write\|Edit` | **Active.** After a write to an engagement's `shared-understanding.md`, calls `resolve.sync_mirror`, which puts the graph back to what the SU says **through the coordinator** (same `flock`, same receipt). The writer that was missing: lenses append rows with the Edit tool, nothing mirrored them, and the **second** lens write of a Discovery round was denied by `pre-authority-guard.py` (`AUTHORITY_UNMIRRORED`). Mirrors only what a mirror can fix — `AUTHORITY_UNMIRRORED` and `AUTHORITY_DRIFT`; a pending operation, an unreadable graph or legacy mode is refused, with the recovery on stderr. The SU enters the write set with the bytes that were READ, so a SU that moves between the read and the lock is `BASE_CHANGED`, never a mirror of a file that no longer exists. Registered **before** `on-su-change.py`, so the dashboard reads the mirrored state. Never blocks — always exits 0. |
| `on-su-change.py` | `PostToolUse` on `Write\|Edit` | **Active.** On a write to any engagement artefact (`shared-understanding.md`, `_state.json`, `decisions.md`, `story.md`, `council-log.md`, `answers.md`, `options.md`, `frame.md`, `context.json`, `premortem.md`, or anything under `_capture/ _synthesis/ _render/ _blueprint/ _simulation/ _retro/ lens-outputs/ _coverage/`), spawns `library/kernel/tools/dashboard.py` **detached** and regenerates `<engagement>/dashboard.html`. Debounced (default 2 s). Never blocks — always exits 0. |
| `su-confirmed-guard.py` | `PostToolUse` on `Write\|Edit` | **Active.** On a write to an engagement's `shared-understanding.md`, checks the deterministic half of the *Confirmed threshold* (`library/kernel/states.md` rule 1): every new or changed `C-` row carries a locator of the five classes **and** its target exists (`inputs/`, `_capture/` — including a persisted direct extraction under its own name —, an `answers.md` section, an `enquadramento.md` `M-n`). An `Edit` names the rows it touched; a `Write` replaces the file, so the audit covers every open `Confirmed` and says so. The rule lives once, in `library/kernel/tools/dashboard.py` (`audit_confirmed_locators`), which this hook imports. Warns on stderr and appends an idempotent `Confirmed sem locator: C-nnn` line to `council-log.md`. Judgement — whether the claim says more than the evidence — stays with the round arbiter (`aisa-round` step 5f). Never blocks — always exits 0. |
| `synthesis-validate.py` | `PostToolUse` on `Write\|Edit` | **Active.** On a write to `<engagement>/_synthesis/<topic>.md` (never to `_synthesis-log.md` or `_synthesis-checks.md`), checks the contract of `aisa-synthesize`: `SYN-PARAS` (< 3 paragraphs) · `SYN-NO-IDS` · `SYN-DEAD-ID` (an id with no row in the SU nor block in `decisions.md`) · `SYN-VENDOR` (a term from the pack's `vendor_terms.solution` in a neutral topic — and in `architecture-story` too when no architecture was authorized) · `SYN-TEMPLATE` · `SYN-STAMP` (no `authority:` stamp, or one naming a structurally invalid version; `authority: none — <reason>` is the legitimate no-architecture case). All warnings. Writes to `_synthesis/_synthesis-checks.md` — **never** to `_synthesis-log.md`, whose lines `synthesis_entries()` reads as synthesis runs, so a validation line there would make a stale pack look fresh. The record is history (`sha` of the text, `deps` of the sources); the VERDICT is recomputed on every read (`dashboard.py::synthesis_checks`) because three of the checks depend on the SU, the pack and the blueprint. Exits 0. |
| `blueprint-validate.py` | `PostToolUse` on `Write\|Edit` | **Active.** On a write to `<engagement>/_blueprint/ux-blueprint_vNN.yaml`, runs the kernel's structural check (`dashboard.py::bp_validate` — `blueprint-contract.md` → *Validação estrutural*, 25 codes: YAML subset Y1-Y7, required keys and container types, `architecture` internals, provenance `su_refs`/`su_ref`, `structural`/`resolved`/closure basis, draft, version). Reports to stderr, writes nothing, always exits 0. A `block` issue makes the version non-approvable (aisa-blueprint step 15 refuses mechanically) and an approval already recorded over it non-consumable (`blueprint_state.approved.valid = false`; `render-validate.py`, `--authority-stamp` and the synthesis freshness read that flag). Standalone: `python .claude/hooks/blueprint-validate.py <file>`; the same check by CLI: `python library/kernel/tools/dashboard.py --blueprint-check <file>` (exit 4 when blocking). **It also reports coverage, separately and never merged with structure** (`coverage-contract.md` §8.1): the review published for that exact version, its freshness and its gaps — the F06 case is a version the structural check calls valid that dropped a requirement the SU carried. No record → one line saying it was **not evaluated**, which is neither a pass nor a failure and revokes no approval. The coverage read is read-only: it never finalizes a review. |
| `render-validate.py` | `PostToolUse` on `Write\|Edit` | **Sufficiency by content (P-7).** On a Write to `_render/<slug>_<deliverable>_v<NN>.md`, executes the rules the deliverable template declares in `sufficiency:` against the APPROVED blueprint's record (following `SEE_Vnn` back-references) and the rendered text — §4 entities without `authority`/dictionary, §6 `(none)` with state machines, §8 without a role matrix, §7 without authentication + secret custody or a named gap. Fails → appends a `## Validação …` block to `render-gaps.md` (owner named) and one stderr line; never blocks the write. CLI: `python .claude/hooks/render-validate.py --engagement <slug> [--dry-run] [--json]`. **It also reports coverage, on its own line and never merged with sufficiency** (`coverage-contract.md` §8.2): the five verdicts of the stage-`render` review of that same file, read through `coverage.py` — the rules are not duplicated here. A sufficient document is not a covered one. No record → one line saying it was **not evaluated**, which is neither a pass nor a failure. The coverage read is read-only, and this hook never writes a coverage finding to `render-gaps.md`: the owner of that finding is the review, recorded by `aisa-render` step 9b. |


## Invocation and the project root

A hook command runs with the **session's** cwd, not the repository root — and the cwd
moves: a single `cd` inside a Bash call is enough. With the relative form
`python .claude/hooks/pre-write-guard.py`, Python then looks for the script under the
new cwd, does not find it, and the `PreToolUse` hook never starts. It fails closed, so
nothing is corrupted — but `Write`, `Edit` and every aisa `Skill` stop working, and the
message names a file that does not exist instead of saying what happened (DEF-P1-02,
measured live in the pilot campaign):

```
PreToolUse:Write hook error: [python .claude/hooks/pre-write-guard.py]:
can't open file '...\projects\smoke\.claude\hooks\pre-write-guard.py'
```

So every command resolves from the project root:

```json
{ "type": "command",
  "command": "python \"${CLAUDE_PROJECT_DIR:-.}/.claude/hooks/pre-write-guard.py\"" }
```

- `CLAUDE_PROJECT_DIR` is provided to hooks by Claude Code and expanded by the shell —
  verified in the real environment, including roots whose path carries spaces and
  accents. Hence the quotes: this repository's own path has both.
- `:-.` is the fallback for the variable being absent: the command degrades to the old
  relative behaviour instead of pointing at the root of the disk.
- The **scripts** never depended on the cwd (each resolves its root through
  `Path(__file__).resolve().parents[2]`). The defect was in the registration line only.

**A different condition, which this does not fix.** A session *started* in a subfolder
does not load the repository's `.claude/settings.json` at all — the init event reports
`hooks: null` and no hook is registered, without a warning. Hooks not loaded and hooks
loaded whose command does not resolve are two different states: open the session at the
repository root.

`.claude/tests/test_hook_invocation.py` holds both ends — the registered form, and each
hook actually starting and deciding from the root, from an engagement folder and from a
folder outside the repository.

## Shared code

`_common.py` holds what more than one hook needs: engagement resolution (`find_engagement`, whose ambiguity policy is a parameter — a hook that WRITES refuses to guess, one that only reports keeps the tolerant default), `load_dashboard`, stdin parsing and the `--engagement` / `--override` argument readers.

## Enforcement modes

| Mode | Activation | What enforces |
|---|---|---|
| **Enforce (default)** | Unset or `AISA_GUARD_MODE=enforce` — `.claude/settings.json` sets it explicitly in `env` | `pre-write-guard.py` hard-blocks `library/*` writes. Backed by the `permissions.deny` rules for `Write/Edit(./library/**)` — two independent layers. `pre-authority-guard.py` hard-blocks a write to an engagement authority over unreconstructed state; it has no `deny` backup because the decision depends on the state, not on the path. |
| Log (administrative override) | `AISA_GUARD_MODE=log` | Warnings to stderr, no blocking. The `settings.json` deny rules still apply until removed locally. |
| Always-on | n/a | `pre-lens-order-check.py` — the order of a **full** round is enforced (the skill already runs it by construction; the hook is the net for a model that skipped the MUST). A single lens (`round mode: single`) is never policed. No log mode. |

For administrative authoring (populating a pack, editing kernel docs), the sanctioned path per `.claude/rules/library-readonly.md` is an out-of-band edit + `git commit`. The `library/kernel/tools/*.py` scripts are read and **executed** at runtime — execution is never a write, so the guard does not apply to running them.

## Why completeness is checked at `Stop`, not `PostToolUse`

`PostToolUse` on `Skill` fires when the Skill tool **returns** — that is when the instructions are loaded, long before the agent has executed them. At that instant `frame.md` does not exist, so any completeness assertion there is guaranteed to be wrong. `Stop` fires when the turn ends, with every write already on disk; that is the only point at which "did it write everything?" is a fact rather than a guess. `phase-gate-check.py` keeps its `PostToolUse` slot for what it can legitimately observe (which skill ran).

The checks are derived from each skill's own `Outputs (written)` section, not invented — see the citations in the hook's docstring. Being a soft gate is deliberate: CLAUDE.md principle 5 says the only hard rule is `library/` read-only.

## Hooks that spawn subprocesses

`on-su-change.py` is the only hook that launches another process. Three properties make that safe:

- **No loop.** `PostToolUse` fires on the *agent's* `Write`/`Edit` tool calls. The generator writes with `open()` + `os.replace()` inside a subprocess — filesystem I/O, not a tool invocation — so it cannot re-enter the hook. Two cheap guards cover a future model hand-editing the page anyway: the hook returns early on a path ending in `dashboard.html`, and on `AISA_DASHBOARD_RUNNING=1` (set in the child's env).
- **Detached, never awaited.** `subprocess.Popen` with `DEVNULL` on all three streams, plus `CREATE_NO_WINDOW | DETACHED_PROCESS` on Windows and `start_new_session=True` elsewhere. A synchronous run would add ~250 ms to each of the 7 writes a `/round` performs, and any generator bug would become a user-facing hang.
- **Debounced.** The hook skips when `dashboard.html` was written less than `AISA_DASHBOARD_DEBOUNCE` seconds ago (default 2), collapsing a burst of writes into one or two rebuilds. Concurrent generators are still possible; the generator's tmp file carries its pid and lands via `os.replace`, so the worst case is "older build wins for ~2 s", self-corrected on the next write.

**What the hook cannot see.** `PostToolUse` fires on the *agent's* `Write`/`Edit` tool calls and nothing else. A human editing `shared-understanding.md` in an editor, a script, a `git checkout`, or another Claude session writing through Bash all leave the dashboard stale — and because the page reloads itself on a timer, the browser then shows the same old build forever, which reads as "the refresh is broken". For those writers run the generator's own poll loop: `python library/kernel/tools/dashboard.py --engagement <slug> --serve` (stdlib mtime polling, default 2 s, plus an `http://127.0.0.1:8787` server bound to localhost only). Serving matters beyond convenience: over `file://` the page cannot `fetch`, so it can only reload blindly on a timer — and sandboxed contexts refuse even that. Over HTTP it polls `/__build` and reloads only when the build hash changes. Run **one** watcher per engagement: two racing processes let an older build win. The hook stays useful for agent writes: it is instant and costs nothing when idle.

If the generator itself throws, it writes an **error page** to the same path (traceback + the same reload script) and exits 1 — an open browser tab shows the failure instead of silently going stale. The hook ignores the exit code.

## Environment variables

| Variable | Default | Effect |
|---|---|---|
| `AISA_ENGAGEMENTS_ROOT` | `projects/` | Where engagement folders live. Honoured by `pre-lens-order-check.py`, `on-su-change.py` and `dashboard.py`. |
| `AISA_GUARD_MODE` | `enforce` | `log` downgrades `pre-write-guard.py` **and `pre-authority-guard.py`** to warn-only (administrative override). |
| `AISA_DASHBOARD_RELOAD` | `5` | Browser auto-reload interval, in seconds, baked into the generated page. `0` disables it. |
| `AISA_DASHBOARD_DEBOUNCE` | `2` | Seconds during which `on-su-change.py` skips a rebuild after the last one. |
| `AISA_DASHBOARD_RUNNING` | unset | Set to `1` in the generator's own env; makes the hook a no-op inside it. |

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
