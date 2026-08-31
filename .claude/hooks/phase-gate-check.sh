#!/usr/bin/env bash
# phase-gate-check.sh — MVP log-only stub.
#
# Intended PostToolUse for the phase-transition skills (aisa-frame, aisa-options, aisa-decide).
# Reads <engagement>/_state.json after a phase transition and warns if the exit criteria
# of the previous phase were not met without an explicit override.
#
# Stage 1 (MVP): log only. Stage 2 (v0.2.0): block hard.

set -euo pipefail

if ! command -v jq >/dev/null 2>&1; then
  echo "[phase-gate-check] jq not found — guard inactive (log-only stub)." >&2
  exit 0
fi

INPUT=$(cat 2>/dev/null || true)

# The hook fires for any tool; we only care when an aisa phase-transition skill ran.
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
SKILL_NAME=$(echo "$INPUT" | jq -r '.tool_input.skill // empty')

case "$SKILL_NAME" in
  aisa-frame|aisa-options|aisa-decide) ;;
  *) exit 0 ;;
esac

echo "[phase-gate-check] $SKILL_NAME ran — soft gate logged. Phase 12 will validate <engagement>/_state.json + SU counts against phases.md exit criteria." >&2
exit 0
