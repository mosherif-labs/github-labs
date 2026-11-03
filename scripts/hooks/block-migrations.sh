#!/bin/bash
# preToolUse guardrail: deny any write whose arguments touch migrations/ (Day 25).
# Same shape as Day 13's block-infra.sh, so both hooks agree on what a write is.
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.toolName')
ARGS=$(echo "$INPUT" | jq -r '.toolArgs')

case "$TOOL" in
  create|edit|str_replace_editor|apply_patch|bash|powershell)
    if echo "$ARGS" | grep -Eq '(^|["/ ])migrations/'; then
      echo '{"permissionDecision":"deny","permissionDecisionReason":"Data migrations need a human. Label the issue needs-human."}'
      exit 0
    fi
    ;;
esac
# Reads (view, grep, rg, glob) fall through: no output = no decision.
exit 0
