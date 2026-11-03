# txn-screening-rebuild

Python 3.13 + FastAPI. Synthetic data only.

- Install: `uv sync --locked` · Test: `uv run pytest -q` (same as CI job `test`)
- Endpoints in `app/main.py`, tests in `tests/`, one behaviour per test
- Never touch `infra/`: it is human-only
- No new dependency without an ADR in `docs/decisions/`
