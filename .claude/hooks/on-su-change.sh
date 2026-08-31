#!/usr/bin/env bash
# on-su-change.sh — MVP log-only stub.
#
# Intended PostToolUse for any Write/Edit to <engagement>/shared-understanding.md.
# In v0.2.0+ this triggers a background contradiction-scan that surfaces silent
# conflicts (e.g., a Confirmed row collides with another lens's Risky row).
#
# Stage 1 (MVP): log only — observe SU writes so we can audit volume.

set -euo pipefail

if ! command -v jq >/dev/null 2>&1; then
  echo "[on-su-change] jq not found — guard inactive (log-only stub)." >&2
  exit 0
fi

INPUT=$(cat 2>/dev/null || true)

TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [[ "$TOOL_NAME" != "Write" && "$TOOL_NAME" != "Edit" ]]; then
  exit 0
fi

if [[ "$FILE_PATH" == *shared-understanding.md ]]; then
  echo "[on-su-change] SU written: $FILE_PATH — v0.2.0 will scan for contradictions in background." >&2
fi

exit 0
