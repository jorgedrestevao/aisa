---
description: Regenerate the living dashboard; --serve keeps it live over http with no blind reloads.
argument-hint: "[slug] [--serve] [--open] [--watch]"
---

Run, from the repo root:

`python library/kernel/tools/dashboard.py [--engagement <slug>] [--serve] [--open]`

**Preferred way to keep a page open while working**: `--serve` (implies `--watch`).
It binds `http://127.0.0.1:8787` to the engagement folder — localhost only, never the
network, because an engagement holds client material. Over HTTP the page polls
`/__build` and reloads **only when the build hash actually changes**; on `file://` it
cannot fetch at all and falls back to a blind timed reload, which some browsers and
embedded previews refuse outright (the page then shows a red banner saying so).

**Lost the link?** `--url` prints where to open it — a running server's URL if there is
one, otherwise the `file://` path — and builds nothing. Add `--open` to any invocation to
launch the browser. Both resolve the engagement on their own, so no link is ever needed:

```
python library/kernel/tools/dashboard.py --url            # most recent engagement
python library/kernel/tools/dashboard.py --url --open      # and open it
python library/kernel/tools/dashboard.py --engagement kam-onboarding --url
```

Flags:
- No slug: resolves the most recently touched engagement.
- `--url`: print where to open it and exit. Nothing is built.
- `--serve [port]`: serve + watch. **Idempotent** — if a server for this engagement is
  already up it reattaches, prints the URL and rebuilds nothing. Walks forward only when
  the port itself is taken by something else. `--force` starts a second one anyway.
- `--watch [secs]`: rebuild on change without serving (default poll 2s).
- `--open`: opens the served URL, or the file, in the default browser.
- `--json <path>` (debug), `--force` (ignore the mtime debounce),
  `--today <ISO>` (pin the expiry maths, for tests).
- `--authority-stamp [vNN]`: print the line `aisa-synthesize` writes at the head of
  `architecture-story.md` — `authority: _blueprint/ux-blueprint_vNN.yaml#architecture @ sha256:<hex>`
  — for the given version, else the approved one, else the latest authorized. Nothing is built;
  the motor later compares this stamp with the approved version (freshness by identity).

Why `--serve`/`--watch` matter: `on-su-change.py` is a `PostToolUse` hook, so it only
sees **this agent's** `Write`/`Edit` calls. A human in an editor, a script, or another
session leaves the page stale and the browser reloads the old build forever.

**One watcher per engagement.** Two concurrent processes race on the output file and an
older build can win. `--serve` now enforces this by reattaching; the lock lives in the
system temp dir (keyed by the engagement path), never inside the engagement folder.

Report the served URL (or output path) plus the one-line summary the tool prints. Do not
analyse the engagement — the page is the analysis.

Args: $ARGUMENTS
