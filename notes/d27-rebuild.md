# Day 27 — Final pass: sandbox, speed rebuild, gap log

> An empty public repo and a stopwatch: instructions, agents, MCP, setup steps, hooks and a ruleset, from memory, in under 2 hours. Then the gap log twice, and stop by early evening.

**Deliverable:** this note (sandbox notes, rebuild time, what I got wrong) + the answer files in [d27-rebuild-reference/](d27-rebuild-reference/) to diff the rebuild against

## Bet

- **Bet** — Full rebuild, no notes: **— min** (win if under 120 **and** within 20% of the guess)
  - Result: _stopwatch time_

## Exam sandbox

- Use the **GitHub** sandbox: [ghcertdemo.starttest.com](https://ghcertdemo.starttest.com/) (the GH-600 page's *Launch the sandbox*). `aka.ms/examdemo` is the Microsoft one.
- It shows the question types, where the timer and the questions-remaining counter sit, **mark for review**, and the review screen. — [Prepare for an exam](https://learn.microsoft.com/en-us/credentials/certifications/prepare-exam#explore-the-exam-sandbox)
- **Closed-book.** Role-based Microsoft exams allow Microsoft Learn, but *"access to Learn is NOT available on Fundamentals exams or GitHub exams."* — [Exam experience](https://learn.microsoft.com/en-us/credentials/support/exam-duration-exam-experience#accessing-microsoft-learn-during-your-certification-exam)
- Things that would cost seconds on Sunday: _(flag button position, review screen, counter)_

## The rebuild (`txn-screening-rebuild`, public)

Public because the org is on GitHub Free: rulesets, code scanning, secret scanning and push protection are free only on public repos there. Synthetic code and data only.

| Block | Target | Files | Time |
|---|---|---|---|
| 1 · 0–30 | repo + tiny app + 1 test + CI `test` | [`copilot-instructions.md`](d27-rebuild-reference/.github/copilot-instructions.md), [`tests.instructions.md`](d27-rebuild-reference/.github/instructions/tests.instructions.md) (`applyTo`), [`AGENTS.md`](d27-rebuild-reference/AGENTS.md) | |
| 2 · 30–60 | planner + implementer + code owners | [`planner.agent.md`](d27-rebuild-reference/.github/agents/planner.agent.md), [`implementer.agent.md`](d27-rebuild-reference/.github/agents/implementer.agent.md), [`CODEOWNERS`](d27-rebuild-reference/.github/CODEOWNERS) | |
| 3 · 60–90 | MCP + setup steps + firewall | [`mcp-config.json`](d27-rebuild-reference/mcp-config.json) (Settings → Copilot → MCP servers), [`copilot-setup-steps.yml`](d27-rebuild-reference/.github/workflows/copilot-setup-steps.yml) | |
| 4 · 90–120 | hooks + ruleset + smoke test | [`guardrails.json`](d27-rebuild-reference/.github/hooks/guardrails.json), [`ruleset.md`](d27-rebuild-reference/ruleset.md); issue assigned to Copilot with `planner`, session starts | |
| **Total** | **< 120 min** | | |

**Gate 3:** under 2 h = green. Over 2 h = **no reschedule** (Day 26's rule); every slow step goes into the gap log now and gets starred in read 2.

## Facts to diff against

**Agent profile frontmatter** — [Custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration#yaml-frontmatter-properties)

- `description` is the **only required** property.
- Optional: `name`, `target` (`vscode` / `github-copilot`), `tools` (unset = all tools), `model`, `disable-model-invocation`, `user-invocable`, `mcp-servers`, `metadata`. `infer` is retired.
- `mcp-servers` and `metadata` are **not used** by VS Code / IDE custom agents.
- MCP tools in `tools:` are `server/tool` (`server/*` = all of that server's tools).

**Hooks file** — [Use hooks](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/use-hooks#creating-a-hook-in-a-repository-on-github)

- `.github/hooks/NAME.json` with `"version": 1` and a `hooks` object keyed by event: `sessionStart`, `sessionEnd`, `userPromptSubmitted`, `preToolUse`, `postToolUse`, `errorOccurred`.
- Each command entry: `type: "command"`, `bash` / `powershell`, optional `cwd`, `timeoutSec`, `env`.

**MCP for the cloud agent** — [Extend cloud agent with MCP](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/extend-cloud-agent-with-mcp)

- Repo **Settings → Copilot → MCP servers**, top-level `mcpServers`; every server needs `type` and `tools`.
- Secret = repo **Agents** secret named `COPILOT_MCP_*`; in the JSON, `$COPILOT_MCP_...`; in a profile, `${{ secrets.COPILOT_MCP_... }}` also works.

**Setup steps**

- `.github/workflows/copilot-setup-steps.yml` on the **default branch**, job named **`copilot-setup-steps`**, `timeout-minutes` at most 59.

**CODEOWNERS**

- GitHub reads the first of `.github/CODEOWNERS`, root `CODEOWNERS`, `docs/CODEOWNERS`. In `github-labs` the root file exists, so a `.github/` one would shadow it. In the new repo `.github/CODEOWNERS` is fine.
- Last matching pattern wins.

## What I got wrong

Every field name, path or setting I got wrong or looked up. Each one also goes into [gap-log.md](gap-log.md).

| Slip | Right answer | Doc |
|---|---|---|
| | | |

## Gap log

- **Read 1 (understand):** top to bottom, say out loud why each answer is right; open the doc only when I can't.
- **Read 2 (recall, paper):** cover the answer column; star anything still missed. The starred list is tomorrow morning's only extra reading.

Starred: _…_

## Stop

Stop by early evening. Check the appointment time, ID and check-in instructions, then rest.

## Reflection

- Which part of the rebuild still needed the docs, and is it starred?
- How does the exam interface change the pacing plan?
- At the bank, which two steps of this setup would take longer than 2 hours because of approvals, and why?
