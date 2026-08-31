#!/usr/bin/env bash
# pre-write-guard.sh — enforces library/ read-only at runtime (the one hard guard).
#
# Receives JSON via stdin with tool name + parameters.
# Blocks writes to library/* unless AISA_GUARD_MODE=log (administrative override).
# Default is enforce (fail-closed); .claude/settings.json env sets it explicitly,
# and the settings.json permissions.deny rules are the second layer.

set -euo pipefail

# Graceful degradation: this hook parses the payload with jq. If jq is absent
# (e.g. minimal Windows setup), no-op instead of erroring on every Write/Edit —
# the settings.json deny rules remain as the backstop. The durable Windows story
# (.ps1 hook or bundled jq) is a v0.2.0 task.
if ! command -v jq >/dev/null 2>&1; then
  echo "[pre-write-guard] jq not found — hook guard inactive; settings.json deny rules are the only layer." >&2
  exit 0
fi

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Only inspect Write/Edit
if [[ "$TOOL_NAME" != "Write" && "$TOOL_NAME" != "Edit" ]]; then
  exit 0
fi

# Check if path is under library/
if [[ "$FILE_PATH" == */library/* ]] || [[ "$FILE_PATH" == ./library/* ]] || [[ "$FILE_PATH" == library/* ]]; then
  if [[ "${AISA_GUARD_MODE:-enforce}" != "log" ]]; then
    echo "library/ is read-only at runtime (rule: .claude/rules/library-readonly.md). Administrative edits go out-of-band via git, or set AISA_GUARD_MODE=log temporarily: $FILE_PATH" >&2
    exit 2
  else
    echo "[pre-write-guard] WARN (log mode): write to library/ — denied when AISA_GUARD_MODE=enforce: $FILE_PATH" >&2
  fi
fi

exit 0
