#!/bin/bash
# postToolUse logger: one JSON line per tool call on stdout, so it lands in the session log.
# The cloud agent's filesystem is discarded when the job ends, so a local log file would be lost.
jq -c '{tool: .toolName, args: .toolArgs}'
exit 0
