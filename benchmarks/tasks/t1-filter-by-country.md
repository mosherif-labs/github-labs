# Benchmark task 1: filter alerts by country (new filter)

Frozen task for the Day 20 tuning loop. Open it as a new issue per run, assigned from `main`.

## Problem
`GET /alerts` can't be filtered by the transaction's counterparty country.

## Acceptance criteria (checked mechanically)
- `GET /alerts?beneficiary_country=XX` returns only alerts whose transaction `beneficiary_country` is `XX`.
- A value that isn't 2 uppercase letters returns **422**.
- Without the parameter, the response is unchanged.
- New tests in `tests/test_alerts.py` cover: match, no match, 422, and no filter.
- `uv run pytest -v` passes; no new dependency.

## Files to change
- `app/routers/alerts.py`
- `tests/test_alerts.py`
