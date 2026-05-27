#!/usr/bin/env bash
# pre-write-guard.sh — MVP version. Stage 1: log only; Stage 2 (Fase 11): enforce.
#
# Receives JSON via stdin with tool name + parameters.
# Blocks writes to library/* once AISA_GUARD_MODE=enforce.

set -euo pipefail

# Graceful degradation: this stub parses the hook payload with jq.
# If jq is absent (e.g. minimal Windows setup), no-op instead of erroring on every
# Write/Edit. Phase 11 decides the durable Windows story (.ps1 hook or bundled jq).
if ! command -v jq >/dev/null 2>&1; then
  echo "[pre-write-guard] jq not found — guard inactive (log-only stub). Resolve in Phase 11." >&2
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
  if [[ "${AISA_GUARD_MODE:-log}" == "enforce" ]]; then
    echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"library/ is read-only at runtime\"}}" >&2
    exit 2
  else
    echo "[pre-write-guard] WARN: write to library/ — will be denied in enforce mode: $FILE_PATH" >&2
  fi
fi

exit 0
