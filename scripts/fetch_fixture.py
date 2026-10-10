"""Downloads a public test page. Exists only to trip the agent firewall on Day 11."""

import urllib.request
from pathlib import Path

URL = "https://example.com/"
OUT = Path("tests/fixtures/example.html")
OUT.parent.mkdir(parents=True, exist_ok=True)
with urllib.request.urlopen(URL, timeout=10) as r:
    OUT.write_bytes(r.read())
print("fetched", URL)
