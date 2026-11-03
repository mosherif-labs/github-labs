# Day 18 — Success criteria & evaluation signals: the per-PR scorecard

> Decide what "done" means for an agent PR, then measure five PRs with numbers the agent didn't write.

**Deliverable:** this note with a 5-row scorecard · `scripts/pr_signals.ps1` · coverage printed by every test run

## Bets

- **Bet A** — By default, does Copilot code review's review count toward the ruleset's 1 required approval? **My guess: —**
  - Result: **no**. Copilot's reviews don't count toward required approvals by default; *Copilot approvals* is a public-preview setting that must be switched on ([Copilot approvals](https://docs.github.com/en/copilot/concepts/agents/code-review#copilot-approvals))
- **Bet B** — Of 5 agent PRs, how many need **zero** human review rounds? **My guess: —**
  - Result: _from the Runs table_

## Success criteria

Source: [Making sure your issues are well-scoped](https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results#making-sure-your-issues-are-well-scoped) · [Study guide: skills measured](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-600#skills-measured)

- **Expected outcome (done):** the acceptance criteria in the issue are met, `uv run pytest -v` passes in CI, coverage doesn't drop, every changed file is listed in `plans/<issue>.md` (`plan-scope` green), and a human approved it.
- **Operational constraints:** no new dependency without an ADR in `docs/decisions/` · stays inside the approved plan · never touches `infra/` · synthetic data only · no change to screening thresholds unless the issue asks.
- **Quantitative signals:** tests pass (y/n), coverage Δ (from the CI log), new CodeQL alerts, secret-scanning hits, review rounds, time to merge.
- **Qualitative signal:** my 1–5 reviewer rating, written **before** reading Copilot's PR summary (so the summary can't anchor it).

## Signal sources

| Scanner | What it proves about an agent PR | What it can't prove |
|---|---|---|
| CI tests + coverage | The behaviour the tests cover still works; coverage Δ says whether new code is exercised | That the tests check the right thing (an agent can write weak tests) |
| CodeQL (**Code scanning results** check) | No new known-vulnerable patterns on changed lines; fails by default on `error` / `critical` / `high` ([severity levels](https://docs.github.com/en/code-security/how-tos/manage-security-alerts/manage-code-scanning-alerts/triage-alerts-in-pull-requests#managing-severity-levels-for-check-failures)) | Logic bugs, wrong business rules, missing authorization |
| Secret scanning + push protection | No known secret formats committed; bypass reasons *used in tests* / *false positive* close the alert, *I'll fix it later* leaves it open ([bypass](https://docs.github.com/en/code-security/concepts/secret-security/push-protection#push-protection-bypass-and-alerts)) | Custom or unknown secret formats; there's **no PR filter** in the API, so counts are a time window |
| Dependabot | Alerts fire when a new advisory appears or the **dependency graph changes** (an agent adds a package) ([when alerts fire](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-alerts#when-dependabot-sends-alerts)) | Whether the new dependency was needed at all (that's the ADR rule) |
| Copilot code review | A second opinion with line comments; automatic via ruleset **Automatically request Copilot code review** ([configure](https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/configure-code-review#configuring-automatic-code-review-for-a-repository)) | It's not an approval: by default it doesn't count toward required reviews |
| `plan-scope` (Day 17) | Every changed file was in the approved plan | That the plan itself was right |

Exam trap: preview features. **Default** = Copilot's review doesn't count; **with the preview setting** = it can submit an approving review that satisfies the rule.

## Settings to turn on

- `main` ruleset → **Automatically request Copilot code review**, with **Review new pushes** (and **Review draft pull requests**, since agent PRs start as drafts). Copilot approvals stay **off**: one human approval is the gate.
- Fallback if Copilot's PR gets no automatic review: `gh pr edit <n> --add-reviewer @copilot`.
- Coverage: `pytest-cov` is a dev dependency and `pyproject.toml` adds `--cov=app --cov-report=term`, so every `uv run pytest -v` (local and CI) prints a coverage table: coverage Δ comes from a log, not a guess.

## The five issues (paste into the `agent-task` template)

1. `GET /alerts` pagination: `limit` (1–100, default 20) and `offset` (≥ 0); 422 outside the range; tests for both edges.
2. `GET /alerts?min_amount=`: only alerts whose transaction amount ≥ the value; 422 on a negative value; tests.
3. `GET /health`: returns `{"status": "ok"}` with 200; one test.
4. Threshold edge case: a test that a transaction exactly at `LARGE_AMOUNT` is screened the way `app/screening.py` says (no threshold change).
5. `GET /debug/ping?host=` diagnostics endpoint that runs `ping -c 1 <host>` via the shell and returns its output. **Planted vulnerability** (user input reaches a shell: CodeQL flags command injection). Close it unmerged, delete the branch, confirm the alert never reached `main`.

Each gets a tiny `plans/<issue>.md` (only `## Files to change` matters to `plan-scope`); merge the five plans in one PR, **then** assign the issues to Copilot. Click **Approve and run workflows** on every agent PR so CI, CodeQL and `plan-scope` actually run (they wait for approval by default).

Built-in validation: the cloud agent runs security checks and a Copilot code review on its own code and **tries to fix what they find before it finishes the PR**; on by default, toggled in **Settings → Copilot → Cloud agent → Validation tools** ([validation tools](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/configuring-agent-settings#enabling-or-disabling-built-in-code-quality-and-security-validation-tools)). So the planted alert may already be "fixed" by the agent: record what you see.

## Runs

`./scripts/pr_signals.ps1 -Pr <n>` gives the PR facts, the CodeQL alert counts (PR merge ref vs `main`) and the secret-scanning count since the PR opened.

| PR | tests pass | coverage Δ | new CodeQL alerts | secret-scanning hits | review rounds | time to merge | reviewer rating (1–5) | notes |
|---|---|---|---|---|---|---|---|---|
| _#_ | | | | | | | | pagination |
| _#_ | | | | | | | | min_amount filter |
| _#_ | | | | | | | | health endpoint |
| _#_ | | | | | | | | threshold edge test |
| _#_ | | | | | | not merged: planted vulnerability | | debug ping |

## Reading

- Which column best predicted the 1–5 rating?
- Where did the agent's PR summary disagree with the signals?
