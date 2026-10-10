"""Tiny MCP server: one tool over a SYNTHETIC sanctions list. Nothing from the bank."""

import json
import os
from pathlib import Path

from mcp.server import (
    MCPServer,
)  # mcp 2.x; on 1.x use: from mcp.server.fastmcp import FastMCP

DATA = Path(__file__).parent / "data" / "sanctions_synthetic.json"
mcp = MCPServer("sanctions")


@mcp.tool()
def lookup_sanctions(name: str) -> dict:
    """Case-insensitive lookup of a person or entity name on the synthetic sanctions list."""
    if not os.environ.get("SANCTIONS_API_KEY"):
        return {
            "error": "SANCTIONS_API_KEY not set"
        }  # proves the secret reached the server
    entries = json.loads(DATA.read_text())
    hits = [e for e in entries if name.lower() in e["name"].lower()]
    return {"query": name, "hits": hits, "match": bool(hits)}
