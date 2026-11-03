# Day 19 — Failure analysis: break it three ways, prove each with a log line

> Plant one environment failure, one reasoning failure and one tool-misuse failure, then classify each from the evidence, never from the agent's own summary.

**Deliverable:** this note: each failure with its class and the log line that proves it

## Bets

- **Bet A** — An agent profile lists a misspelled tool, `tools: ["read", "seach"]`. What happens? **My guess: —**
  - Result: **the unknown name is silently ignored**: «All unrecognized tool names are ignored, which allows product-specific tools to be specified in an agent profile without causing problems.» ([Custom agents configuration: Tools](https://docs.github.com/en/copilot/reference/custom-agents-configuration#tools)). The agent loads with `read` only
- **Bet B** — The firewall blocks the agent's download. Where does the evidence show up first? **My guess: —**
  - Result: **a warning in the PR body (new PR) or a PR comment (existing PR)**, showing the blocked address and the command that tried it ([Firewall overview](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-the-firewall#overview))

## Evidence map

Source: [Study guide: skills measured](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-600#skills-measured) · [Review session logs](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/manage-and-track-agents#review-session-logs)

Session logs show Copilot's **internal reasoning** and the **tools it used**: the two things that separate a reasoning error from tool misuse.

| Class | Evidence to look for |
|---|---|
| **Context / environment** | firewall warning (blocked address + command) in the PR body or a comment; a failed step in `copilot-setup-steps`; missing secret or dependency |
| **Reasoning** | a line in the plan or the session log's reasoning that contradicts the issue, or picks one acceptance criterion over another without saying so |
| **Tool misuse** | wrong, missing or repeated tool calls in the session log's tool list; the agent profile's `tools:` line itself |

A stuck session can start moving again; one that stays stuck **times out after an hour** ([troubleshooting](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/troubleshoot-cloud-agent#based-on-the-agent-session-logs-copilot-appears-to-be-stuck)).

Template per failure: **symptom · class · evidence (artifact + exact line) · fix**

## How the firewall fails

Source: [Customizing the firewall](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-the-firewall#overview) · [Limitations](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-the-firewall#limitations)

- Internet access is limited by default to manage **data exfiltration** risk; GitHub-essential hosts are always allowed, plus an optional recommended allowlist.
- It only covers processes **started by the agent**: not MCP servers, not `copilot-setup-steps` processes. It runs inside the Actions appliance and is **not a comprehensive security control**.

## Failure 1: environment

- **Issue:** *Download the sanctions test list from `https://httpbin.org/anything/sanctions.csv` into `data/` and add a loader with a test.* (synthetic)
- **Class:** context / environment
- **Evidence:** _paste the firewall warning line (blocked address + command) and link the session log_
- **Fix options:** a repository custom allowlist entry for the host · vendor the file into the repo · fetch it in `copilot-setup-steps.yml` (setup steps aren't covered by the firewall)

## Failure 2: reasoning

- **Issue:** *AC1: block every transaction over 10,000. AC2: never block a transaction; only flag it for review.* Contradictory on purpose: the docs say to avoid **ambiguous** tasks ([choosing tasks](https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results#choosing-the-right-type-of-tasks-to-give-to-copilot)).
- **Class:** reasoning error, fed by an ambiguous input
- **Evidence:** _the reasoning line where it noticed the conflict, picked one silently, or implemented both_
- **Fix (one sentence):** *"Transactions over 10,000 are flagged for review (status `review`), never blocked."*

## Failure 3: tool misuse

The broken profile (merged to `main` because custom agents only appear in the dropdown once they're on the **default branch**, [creating custom agents](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/create-custom-agents#creating-a-custom-agent-profile-in-a-repository-on-github)), deleted again in the same PR as this note:

```markdown
---
name: test-writer
description: Writes and runs pytest unit tests for github-labs endpoints
tools: ["read", "seach"]
---
You write pytest unit tests for the screening endpoints and run them until they pass.
```

- **Task:** *Add tests for `GET /alerts` pagination*, with the **test-writer** agent selected
- **Class:** tool misuse (wrong tool set): it must write and run tests but has no `edit` or `execute`, and `seach` is silently dropped
- **Evidence:** _the session-log line showing it couldn't edit/run, or what it did instead_ + the profile's `tools:` line
- **Fix:** `tools: ["read", "search", "edit", "execute"]`. Not `"*"`: omitting `tools` or `["*"]` grants **every** tool, MCP tools included; least privilege lists only what the job needs. `tools: []` grants none. Aliases: `execute` (shell), `read`, `edit`, `search`, `agent`, `web`, `todo` (`web` and `todo` don't apply to the cloud agent)

## Summary

| Failure | Class | Artifact | Exact line | Fix |
|---|---|---|---|---|
| Download from httpbin | environment | PR body / comment warning | _blocked address + command_ | allowlist entry, vendor file, or setup step |
| Block vs flag | reasoning | session log reasoning / plan | _where it chose_ | rewrite the AC as one rule |
| test-writer | tool misuse | session log tool calls + agent profile | _no edit / execute_ | list the four tools it needs |

**Never classify from the agent's own PR summary:** the summary is the agent's narrative of its work, written by the thing being evaluated. The firewall warning, the session log and the profile are evidence it didn't author.
