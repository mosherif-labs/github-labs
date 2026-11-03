# Benchmark task 2: whitespace-only watchlist name (bug fix with a failing test)

Frozen task for the Day 20 tuning loop.

## Problem
`POST /watchlist` accepts a name made only of spaces.

## Acceptance criteria (checked mechanically)
- First commit: a test in `tests/test_watchlist.py` that posts `{"name": "   "}` and expects **422** (fails on `main`).
- Then the fix, as a Pydantic constraint on the model in `app/models.py` (no hand-written check in the route).
- Leading/trailing spaces around a real name are stripped before storing.
- `uv run pytest -v` passes; no new dependency.

## Files to change
- `app/models.py`
- `tests/test_watchlist.py`
