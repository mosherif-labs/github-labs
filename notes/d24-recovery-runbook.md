# Day 24 — Stall, recover, swap the reviewer: failures & agent lifecycle

> Force a stall and resume from the progress file, add a security reviewer, move `reviewer` v1 → v2 without disturbing open work, retire v1, and catch a stale handoff.

**Deliverable:** this runbook + git history showing add → update → retire

## Bets

- **Bet A** — **Stop session** on a run that already pushed 2 commits: what happens to them? **My guess: —**
  - Result: **kept on the branch**: «Stopping a session ends the GitHub Actions run and preserves any commits already pushed.» ([Stop a session](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/manage-and-track-agents#stop-a-session))
- **Bet B** — Repo `reviewer.agent.md` and an org agent named `reviewer`: which is used? **My guess: —**
  - Result: **the repository one**: on a name clash the lowest level wins, repository > organization > enterprise ([Versioning](https://docs.github.com/en/copilot/reference/custom-agents-configuration#versioning))

## Failed, partial, stalled: the signals

Sources: [Troubleshooting: Copilot appears stuck](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/troubleshoot-cloud-agent#based-on-the-agent-session-logs-copilot-appears-to-be-stuck) · [Won't respond to comments](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/troubleshoot-cloud-agent#copilot-wont-respond-to-my-pull-request-comments) · [Hooks: sessionEnd](https://docs.github.com/en/copilot/reference/hooks-reference#sessionend--sessionend)

- A session can look stuck and start again; one that stays stuck **times out after an hour** (the cloud agent's hard cap is **59 minutes**, and it can't be extended: size tasks to fit).
- Retry a stuck run by **unassigning and reassigning** the issue; if it stalled on a PR comment, post the comment again. *Copilot started work* → **View session** streams the live log.
- Copilot only responds to people with **write access**, and only on **open** PRs; 👀 means the `@copilot` comment was received.
- **Steer** = redirect without stopping. **Stop** = end the run from **Stop session**; pushed commits stay. Stopped sessions can be archived, not deleted.
- `sessionEnd` hook gets a `reason`: `complete` · `error` · `abort` · `timeout` · `user_exit`. `errorOccurred` gets `errorContext` (`model_call` · `tool_execution` · `system` · `user_input`) and `recoverable`. On the cloud agent, files hooks write are **discarded** when the job ends: send the signal somewhere durable.

## Failures

| Symptom | Signal / artifact | First response | Recovery |
|---|---|---|---|
| **Failed** | `sessionEnd` reason `error`; red CI; error in the session log | read the log's last tool call and error | fix the cause (env / plan / tool set, Day 19), then unassign → reassign |
| **Partial** | some commits on the branch; progress file lists items under **Next** | don't start over | on the open PR: `@copilot Resume from plans/<issue>-progress.md. Do only the items under Next; don't redo or reverse anything under Done or Decided.` Verify by diffing the progress file |
| **Stalled** | no new log lines; no commits for many minutes; `timeout` | steer with a comment, or wait for the hour | **Stop session** (keeps commits), then resume from the progress file or unassign → reassign |
| **Bad merge** | regression on `main` traced to an agent PR | stop new work on that area | **Revert** the PR: a new PR that reverts the merge commit (write access); revert single commits if the revert conflicts ([reverting a PR](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/reverting-a-pull-request#about-reverting-a-pull-request)) |
| **Degraded: stale handoff** | PR head SHA ≠ the SHA under the reviewer's Handoff **Inputs** (a follow-up commit landed after review) | label `needs-human` | rerun the review step on the head commit; merge only when Inputs SHA = head SHA |
| **Degraded: contradictory reviewers** | `reviewer-v2` says no issues, `security-reviewer` says `NEEDS-HUMAN` | the **stricter** finding stands | a human decides and records it in the PR |

Detect a stale handoff:

```powershell
gh pr view <n> --json headRefOid --jq .headRefOid
gh pr view <n> --json body,comments --jq '.body, .comments[].body' | Select-String -Pattern 'Inputs'
```

## Forced stall run

- Issue: multi-step, with *after each step, commit and update `plans/<issue>-progress.md` (Done / Decided / Next)*
- Stopped after _ commits. Classified **partial** from: branch _, progress file _, session log _
- Resumed with the comment above; progress file diff before/after: _repeated nothing / reversed nothing?_

## Agent lifecycle

Sources: [Versioning](https://docs.github.com/en/copilot/reference/custom-agents-configuration#versioning) · [Frontmatter properties](https://docs.github.com/en/copilot/reference/custom-agents-configuration#yaml-frontmatter-properties) · [Agent lifecycle stages](https://learn.microsoft.com/en-us/agents/center-of-excellence/agent-lifecycle#the-lifecycle-stages)

- A version is the **Git commit SHA of the profile file**: keep versions on branches or tags (`git tag reviewer-v1 <sha>`).
- Lifecycle: Intake → Triage → Build → Deploy → Monitor → Improve → **Retire**. Retire = remove access and dependencies cleanly; it's a healthy outcome.
- `disable-model-invocation: true` → Copilot won't pick it automatically; `user-invocable: false` → users can't select it. `infer` is **retired** (classic distractor).

| Step | What I did | Commit message convention | How auditability is kept |
|---|---|---|---|
| **Add** | `security-reviewer.agent.md`: read-only (least privilege for a checker), flags `infra/`, auth and migrations as `NEEDS-HUMAN`; added to the chain implementer → reviewer → security-reviewer → human merge | `agents: add security-reviewer` | the profile's first SHA |
| **Update** | `reviewer-v2.agent.md` next to v1: cites the plan line for every finding and names the reviewed head SHA under Inputs | `agents: reviewer v2 (update)` | `reviewer-v1` tag on v1's last SHA; side-by-side files make the switch visible in a diff |
| **Replace** | `implementer` now invokes `reviewer-v2`, then `security-reviewer`; in-flight PRs finish on v1 | `agents: cut over to reviewer v2` | open PRs keep their session logs |
| **Deprecate** | v1 gets `disable-model-invocation: true` + `user-invocable: false` | `agents: deprecate reviewer v1` | file still present, unreachable |
| **Retire** | `reviewer.agent.md` deleted once no open PR referenced it | `agents: retire reviewer v1 (retire)` | file, tag and every old session log stay in history |

Trade-off: side-by-side + cut-over is visible and easy to revert with a revert PR; editing in place is simpler but the switch only shows up in SHA history. The docs don't say how a **running** session reacts to a profile change, so record what happens rather than assume.

```bash
git log --oneline --follow -- .github/agents/reviewer.agent.md
git log --oneline -- .github/agents/
```

_Paste the output here after the PRs merge._
