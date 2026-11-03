# Copilot instructions: github-labs

A toy transaction-screening service: FastAPI, in-memory storage (`app/store.py`), Python 3.12+, managed with `uv`.

## Build and test

- Install: `uv sync --locked`
- Test: `uv run pytest -v` (the same command CI runs in `.github/workflows/ci.yml`, job `test`)
- Run locally: `uv run uvicorn app.main:app --reload`
- Run the full test suite before finishing any change, and only finish when it passes. Every run prints a coverage table (`--cov=app` in `pyproject.toml`); don't let coverage drop.
- There is no linter configured: don't add one, and don't reformat files you didn't change.

## Coding standards

- Put routes in `app/routers/`, request/response models in `app/models.py`, screening logic in `app/screening.py`.
- Validate input with Pydantic `Field` constraints on the models in `app/models.py` (as `TransactionIn` does), not with hand-written checks in the route.
- Get the store through the `StoreDep` dependency, and hold `store.lock` while reading or writing it.
- Use type hints on all functions. Keep changes small and focused on the issue.
- Every behaviour change comes with tests in `tests/`.
- Never add a dependency without an ADR in `docs/decisions/` that the issue links to. If you need one, stop and say so. Update `uv.lock` only with `uv`, never by hand.
- Endpoints live in `app/routers/<resource>.py`; their tests live in `tests/test_<resource>.py`.

## State and decisions

- Before working on an issue, read `plans/<issue>-progress.md` if it exists, and update its **Done / Decided / Next** at the end. Never redo Done or reverse Decided without a new Decided entry.
- Read `docs/decisions/` before changing behaviour; never contradict an Accepted ADR without a new ADR.

## Pull requests

- End every PR description with the Handoff block from `.github/pull_request_template.md`, filled in.

## Boundaries

- **Never create, modify or delete anything in `infra/`.** It is human-only.
- Don't change `.github/workflows/` unless the issue explicitly asks for it.
- Don't change `RULES` scores, `RISK_SCORE_REVIEW_THRESHOLD`, `NAME_MATCH_THRESHOLD` or `LARGE_AMOUNT` in `app/screening.py` unless the issue explicitly asks for it. Those are compliance decisions.
- **Synthetic data only.** Never add real names, account numbers or customer data.
