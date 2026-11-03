import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "check_rai_data.py"
# Built at runtime so this file never holds a real-format value (the rai-data check scans diffs).
REAL_SSN = "123" + "-45-" + "6789"
LUHN_CARD = "4111" + " 1111" * 3


def run(diff: str):
    return subprocess.run([sys.executable, str(SCRIPT)], input=diff, capture_output=True, text=True)


def test_synthetic_values_pass():
    diff = "+++ b/tests/fixtures/x.json\n+ssn 900-12-3456 card 4111 1111 1111 1112\n"
    assert run(diff).returncode == 0


def test_real_ssn_fails():
    r = run(f"+++ b/app/x.py\n+ssn = '{REAL_SSN}'\n")
    assert r.returncode == 1 and "file=app/x.py" in r.stdout


def test_luhn_card_fails_but_removed_lines_are_ignored():
    assert run(f"+++ b/a.txt\n+{LUHN_CARD}\n").returncode == 1
    assert run(f"+++ b/a.txt\n-{LUHN_CARD}\n").returncode == 0
