---
description: Implements only the approved plan referenced in the issue.
tools: ["read", "search", "edit", "execute", "sanctions/lookup_sanctions"]
mcp-servers:
  sanctions:
    type: local
    command: uv
    args: ["run", "mcp", "run", "app/tools/sanctions_mcp.py"]
    tools: ["lookup_sanctions"]
    env:
      SANCTIONS_API_KEY: ${{ secrets.COPILOT_MCP_SANCTIONS_API_KEY }}
---
Implement only the approved plan referenced in the issue. If there is none, stop and say so.
Change only the files under "Files to change". Never touch `infra/`. Run `uv run pytest -q` before finishing.
