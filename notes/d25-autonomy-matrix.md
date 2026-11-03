# Day 25 — The autonomy dial: risk classes & the guardrails matrix

> Autonomy is set per action, not per agent. Each action gets a risk class (how bad, how reversible), and the risk class picks the autonomy level and the control that enforces it. A rule only in prose is a wish; every row below names a mechanism.

**Deliverable:** a 15-row autonomy matrix for this repo, with the three controls it needed that didn't exist yet: a `preToolUse` hook for `migrations/`, CODEOWNERS for `scripts/` and `migrations/`, and the `rai-data` CI check.

## Autonomy levels

| Tier | Agent may | Human does |
|---|---|---|
| 1 — Autonomous | edit, test, open the PR | normal review and merge |
| 2 — Supervised | edit; a named owner must approve | Code Owner review on the path |
| 3 — Human-only | propose in the issue or plan; no write | the change itself |

## The matrix

| # | Action | Risk class | Reversible | Autonomy | Control |
|---|---|---|---|---|---|
| 1 | Edit tests | Low | Yes (revert) | 1 | CI `test` + review |
| 2 | Edit docs | Low | Yes | 1 | review |
| 3 | Refactor within one module | Low | Yes | 1 | CI `test`, coverage rule |
| 4 | Add an endpoint | Medium | Yes | 1 | `api.instructions.md`, CI `test`, reviewer agent |
| 5 | Bump a dependency | Medium | Yes | 2 | Dependabot alerts, "no dependency without an ADR", `uv sync --locked` in CI |
| 6 | Change screening thresholds | High | Yes, but alerts already missed are not | 2 | CODEOWNERS `/app/screening.py`, `/app/rules.py` |
| 7 | Change auth code | High | Yes | 2 | Code Owner review, security-reviewer agent, CodeQL |
| 8 | Modify CI (`.github/workflows/`) | High | Yes | 2 | CODEOWNERS `/.github/`; agent-triggered workflows wait for approval |
| 9 | Change an agent profile | High | Yes | 2 | CODEOWNERS `/.github/` |
| 10 | Edit hooks | High | Yes | 2 | CODEOWNERS `/.github/` (covers `/.github/hooks/`) and `/scripts/` |
| 11 | Add an MCP server | High | Yes | 2 | CODEOWNERS `/.github/`; firewall allowlist change is admin-only |
| 12 | Touch `infra/` | Critical | **No** (live resources) | 3 | `block-infra.sh` hook + CODEOWNERS `/infra/` |
| 13 | Delete or edit a data migration | Critical | **No** (data loss) | 3 | `block-migrations.sh` hook + CODEOWNERS `/migrations/` |
| 14 | Deploy to prod | Critical | **No** (users see it) | 3 | environment `production` with required reviewers |
| 15 | Rotate or add a secret | Critical | **No** (exposure can't be undone) | 3 | secrets are admin settings; push protection blocks committed secrets |

### Authorization paths for the irreversible rows

- **12 `infra/`:** the agent writes the proposal in the plan; a human makes the change in a human-authored PR, reviewed by @sheriffMoose.
- **13 Migrations:** agent labels the issue `needs-human` and stops; a human writes the migration, with a backup and a tested rollback named in the PR.
- **14 Deploy:** merge does not deploy. The `production` environment needs one approval from its required reviewers; "Prevent self-review" is on, so whoever triggered the run cannot approve it.
- **15 Secrets:** only repo admins add or rotate them in Settings → Secrets; the agent's MCP secrets are repo **Agents** secrets named `COPILOT_MCP_*`. The agent never sees a secret value in the prompt.

## Built-ins I don't have to build

- Only users with **write access** can assign work to the Copilot cloud agent; comments from users without write access aren't passed to it.
- It pushes only to branches that start with `copilot/`; it can't push to `main`.
- A human must review and merge; **the person who asked Copilot to make the PR can't approve it** (where approvals are required).
- GitHub Actions workflows on Copilot's PRs **don't run until someone with write access approves them** ("Approve and run workflows").

## Ruleset options that matter here

- **Require review from Code Owners**: makes CODEOWNERS a gate, not a suggestion. Last matching pattern wins.
- **Require approval of the most recent reviewable push**: a later push by someone else needs a fresh approval.
- **Require an additional approval for unattributed Copilot PRs** (preview, on by default): a Copilot PR with no human author needs one more approval.

## Environment reviewers

- Up to **6** people or teams; **one** approval is enough.
- **Prevent self-review** stops the person who triggered the deployment approving it.
- Required reviewers on private repos need GitHub Enterprise (or Team for some features); on Free/Pro/Team they work **only on public repos**.

## Responsible AI principles (Microsoft)

Fairness · Reliability & safety · Privacy & security · Inclusiveness · Transparency · Accountability. "Keep a human in the loop" is how accountability is applied: the human who merges owns the change.

## Bets

- **Bet:** the hook alone is enough for `migrations/`; CODEOWNERS is belt-and-braces.
  **Result:** no. Hooks run only inside the agent's session. A human PR (or an agent run without the hook file on its branch) skips it. CODEOWNERS plus "Require review from Code Owners" is what holds for every author. Two layers, different failure modes. — [Hooks](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-hooks), [CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- **Bet:** a `deny` from one `preToolUse` hook stops the tool even if another hook allows it.
  **Result:** not settled by the docs: the hooks reference says all entries run but doesn't state how decisions merge. What it does settle: a command hook that crashes or exits non-zero **denies** (fail-closed) even if its stdout says allow; an `http` hook that errors or times out **falls through** to the normal permission flow (fail-open); and on the cloud agent `ask` is treated as `deny` because nobody is there to answer. So keep each guard in its own script that denies on its own. — [Hooks reference](https://docs.github.com/en/copilot/reference/hooks-configuration)
- **Bet:** `rai-data` catches the fixture PII issue from Day 18.
  **Result:** for SSNs and cards, yes (`tests/test_check_rai_data.py`). Names and IBANs aren't covered; logged as a shortcut in the script.

## Files changed today

- `.github/hooks/guardrails.json`, `scripts/hooks/block-infra.sh`, `block-migrations.sh`, `log-tool.sh`
- `migrations/0001_placeholder.sql`
- `.github/workflows/rai-data.yml`, `scripts/check_rai_data.py`, `tests/test_check_rai_data.py`
- `AGENTS.md` (synthetic-data and migrations rules), `CODEOWNERS` (`/scripts/`, `/migrations/`)
