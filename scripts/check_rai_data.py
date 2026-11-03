import re
import sys

# Policy (AGENTS.md): synthetic data only. Fail on added lines that look like real PII.
# Synthetic data uses SSN areas 000/666/9xx (never issued) and card numbers that fail Luhn.
# shortcut: two patterns only; add IBANs or watchlist names when the policy names them.
SSN = re.compile(r"\b(\d{3})-\d{2}-\d{4}\b")
CARD = re.compile(r"\b(?:\d[ -]?){12,18}\d\b")


def luhn_ok(digits: str) -> bool:
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch) * (2 if i % 2 else 1)
        total += d - 9 if d > 9 else d
    return total % 10 == 0


hits, path = 0, "?"
for line in sys.stdin:
    if line.startswith("+++ b/"):
        path = line[6:].strip()
    if not line.startswith("+") or line.startswith("+++"):
        continue
    for m in SSN.finditer(line):
        if m.group(1) not in ("000", "666") and not m.group(1).startswith("9"):
            hits += 1
            print(f"::error file={path}::Real-format SSN {m.group(0)}: use 9xx-xx-xxxx")
    for m in CARD.finditer(line):
        if luhn_ok(re.sub(r"\D", "", m.group(0))):
            hits += 1
            print(f"::error file={path}::Card number passes Luhn: use one that fails")
sys.exit(1 if hits else 0)
