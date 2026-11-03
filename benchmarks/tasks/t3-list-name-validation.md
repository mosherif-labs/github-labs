# Benchmark task 3: watchlist list_name format (validation rule)

Frozen task for the Day 20 tuning loop.

## Problem
`POST /watchlist` accepts any non-empty `list_name`, e.g. `"my list!"`.

## Acceptance criteria (checked mechanically)
- `list_name` must be 3–32 characters of uppercase letters, digits and hyphens (`^[A-Z0-9-]{3,32}$`); anything else returns **422**.
- The default `SYNTH-SANCTIONS` still works when `list_name` is omitted.
- New tests in `tests/test_watchlist.py`: `"my list!"`, `"AB"`, lowercase `"synth"` → 422; `"SYNTH-PEP"` → 201.
- Validation lives on the model in `app/models.py` (Pydantic `Field` constraint), not in the route.
- `uv run pytest -v` passes; no new dependency.

## Files to change
- `app/models.py`
- `tests/test_watchlist.py`
