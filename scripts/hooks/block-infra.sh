#!/bin/bash
# preToolUse guardrail: deny any write whose arguments touch infra/ (infra is human-only).
# Writes are matched by runtime tool name; reads (view, grep, rg, glob) fall through.
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.toolName')
ARGS=$(echo "$INPUT" | jq -r '.toolArgs')

case "$TOOL" in
  create|edit|str_replace_editor|apply_patch|bash|powershell)
    if echo "$ARGS" | grep -Eq '(^|["/ ])infra/'; then
      echo '{"permissionDecision":"deny","permissionDecisionReason":"infra/ is human-only (AGENTS.md)."}'
      exit 0
    fi
    ;;
esac
exit 0
