#!/usr/bin/env bash
# render-validate.sh — MVP log-only stub.
#
# Intended PostToolUse for any Write to <engagement>/_render/*.md.
# In v0.2.0+ this checks: required slots have non-empty resolutions
# (no inline `⚠️ missing:` placeholders left), the deliverable matches
# its template's audience register (e.g., discovery-report is vendor-neutral),
# and render-gaps.md was updated atomically.
#
# Stage 1 (MVP): log only.

set -euo pipefail

if ! command -v jq >/dev/null 2>&1; then
  echo "[render-validate] jq not found — guard inactive (log-only stub)." >&2
  exit 0
fi

INPUT=$(cat 2>/dev/null || true)

TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [[ "$TOOL_NAME" != "Write" && "$TOOL_NAME" != "Edit" ]]; then
  exit 0
fi

if [[ "$FILE_PATH" == *_render/*.md ]]; then
  echo "[render-validate] Deliverable written: $FILE_PATH — v0.2.0 will validate slot completeness + audience register + render-gaps sync." >&2
fi

exit 0
