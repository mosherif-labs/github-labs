# Day 22 — Three agents, one module: orchestration & parallel isolation

> Fan out three agent tasks (two on purpose in the same module), resolve the overlap, then isolate two local agents with worktrees and prove `plan-scope` enforces the boundary.

**Deliverable:** this note: when to use each pattern, my conflict-resolution steps, and how worktrees + `plan-scope` isolated two parallel agents

## Bets

- **Bet A** — Two agent PRs change the **same lines** of the screening module. Which PR shows the merge conflict? **My guess: —**
  - Result: **whichever you merge second**. Conflicts come from different changes to the same line of the same file; the first merge is clean and the second PR then conflicts with the new `main` ([About merge conflicts](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/about-merge-conflicts#resolving-merge-conflicts))
- **Bet B** — Can you wire planner → implementer → reviewer on the **cloud agent** with `handoffs:` in the frontmatter? **My guess: —**
  - Result: **no**. `argument-hint` and `handoffs` are VS Code / IDE properties, **not supported for Copilot cloud agent**. On GitHub use the `agent` tool alias (one custom agent invokes another) or a human-gated flow ([tool aliases](https://docs.github.com/en/copilot/reference/custom-agents-configuration#tool-aliases))

## When to use each pattern

Source: [AI agent orchestration patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)

| Pattern | Use when | Avoid when | Failure to watch |
|---|---|---|---|
| **Sequential** (pipeline, prompt chaining) | clear linear dependencies; draft → review → polish. The next agent is fixed by the workflow, not chosen by agents | stages are parallel, agents must collaborate, you need backtracking | early low-quality output flows downstream |
| **Planner → workers** | a manager builds and adapts a task ledger (**magentic**) when the plan is dynamic; sequential + concurrent when it's fixed | simple tasks (don't add agents without real specialization) | slow to converge, stalls on ambiguous goals |
| **Fan-out / fan-in** (concurrent, scatter-gather) | independent subtasks; aggregate by vote, weighted merge or a synthesized summary | agents **can't coordinate changes to shared state**, or there's **no conflict-resolution rule** | contradictory results, inconsistent shared state (two agents in one module) |
| **Reviewer-gated** (maker-checker, evaluator-optimizer) | output must meet defined criteria before it moves on | the checker has no clear acceptance criteria | endless loops: needs an **iteration cap** and a **human fallback** |

Also on the exam: group chat → conversation loops; handoff → infinite handoff loops. Top pitfall: **sharing mutable state between concurrent agents**. Combining patterns is fine (sequential early stages, concurrent for the parallel part).

Mission 3 used **fan-out with no coordinator**. For two tasks in one module it should have been **sequential** (merge one, then start the other) or fan-out with **disjoint scopes**.

## Isolation primitives GitHub gives you

- Cloud agent: **one repository, one branch, one PR per task**; it can't make cross-repo changes; each session has a hard **59-minute** maximum ([limitations](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent#limitations-in-copilot-cloud-agents-software-development-workflow)). Isolation **between** tasks is my job: separate issues, non-overlapping scopes.
- Several sessions can run **concurrently**; the Agents tab lists them and each opens its session log; you can steer a running session without stopping it ([agent management](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/agent-management#managing-agents)).
- **CODEOWNERS:** owners are auto-requested on PRs touching their files; **last matching pattern wins**; owners need explicit **write** access or the line is ignored ([syntax](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners#codeowners-syntax)). Our root `CODEOWNERS` already routes the hot module (`/app/screening.py`) and `/.github/` to one owner, so overlapping agent PRs meet the same reviewer.

## Fan-out run

| Issue | Scope | Branch | PR | Session | Overlaps with |
|---|---|---|---|---|---|
| | screening module | | | | B |
| | screening module | | | | A |
| | elsewhere | | | | — |

Expected collision (written before any PR finished): _the lines both plans touch_

## Conflict-resolution steps

1. **Detect:** overlapping paths under `## Files to change` in two plans: the earliest signal, before any code exists.
2. **Order:** review and merge the **smaller** overlapping PR first.
3. **Resolve:** a simple line conflict on GitHub; complex ones in a local clone; or **Fix with Copilot** in the merge box / an `@copilot` comment ([resolving conflicts](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-on-github#resolving-merge-conflicts)). The merge button stays disabled until all conflicts are resolved.
4. **Prevent:** scope split (each issue names its files and lists the other's under *Out of scope*) + CODEOWNERS routing to one reviewer.
5. **Duplicated effort / contradictory outputs:** before merge, diff the plans for shared helpers and compare validation rules for the same field across PRs.

## Two local agents, two worktrees, one scope check

```bash
git switch main; git pull
git worktree add ../tss-wt-a -b agent/d22-a
git worktree add ../tss-wt-b -b agent/d22-b
# one terminal each: cd ../tss-wt-a; copilot   and   cd ../tss-wt-b; copilot
git push -u origin HEAD
gh pr create --fill --label agent --body "Plan: plans/<issue>.md"
git worktree remove ../tss-wt-a; git worktree remove ../tss-wt-b; git worktree prune
```

- A worktree keeps an agent's changes out of my workspace and starts from the base branch's **committed** state; it **isn't a security boundary** (no limit on commands or network) ([VS Code: code isolation](https://code.visualstudio.com/docs/agents/run/agent-harnesses#_choose-code-isolation)).
- Copilot CLI only accesses files **in and below** the directory it was started from ([responsible use §9](https://docs.github.com/en/copilot/responsible-use/agents#9-safety-components-and-mitigations)).
- Stray-file test: add one of A's files in worktree B, push, and `plan-scope` goes red on B's PR. Then `git reset --hard HEAD~1; git push --force-with-lease`.
- **Isolation vs scope:** worktrees stop agents trampling each other's working files; the plan's file list, enforced by a required check, stops an agent changing files it shouldn't. Parallel agents in one repo need both.

| | Cloud agent | Local agents |
|---|---|---|
| Isolation unit | task → branch → PR | one worktree (and branch) per agent |
| What enforces scope | `plan-scope` required check on the PR | the same check, once the PR is opened as an agent PR |

## The chain: planner → implementer → reviewer

- `implementer` now has the `agent` alias (aliases `custom-agent`, `Task`), so it invokes `reviewer` on its diff and pastes the findings under **Handoff** before a human merges.
- Anything that writes code stays **human-gated**: plan PR approved → assign with `implementer` → reviewer findings in the PR → a human merges.
