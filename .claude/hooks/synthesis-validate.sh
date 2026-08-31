#!/usr/bin/env bash
# synthesis-validate.sh — MVP log-only stub.
#
# Intended PostToolUse for any Write to <engagement>/_synthesis/*.md.
# In v0.2.0+ this checks that each topic pack: has ≥3 paragraphs, cites
# ≥1 SU id inline, and respects the topic's vendor-neutrality rule
# (only architecture-story.md may name vendors).
#
# Stage 1 (MVP): log only.

set -euo pipefail

if ! command -v jq >/dev/null 2>&1; then
  echo "[synthesis-validate] jq not found — guard inactive (log-only stub)." >&2
  exit 0
fi

INPUT=$(cat 2>/dev/null || true)

TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [[ "$TOOL_NAME" != "Write" && "$TOOL_NAME" != "Edit" ]]; then
  exit 0
fi

if [[ "$FILE_PATH" == *_synthesis/*.md ]]; then
  echo "[synthesis-validate] Topic pack written: $FILE_PATH — v0.2.0 will validate paragraph count + SU citations + vendor-neutrality." >&2
fi

exit 0
