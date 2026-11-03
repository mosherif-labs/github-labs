# Capstone 3 (Day 20) — The tuning loop, one knob at a time

> Measure a baseline, change **one** thing, measure again, keep or revert. Three knobs: instructions, tools, memory.

**Deliverable:** this before/after report, every claim linked to the PRs or rows that back it

## Bets

- **Bet A** — Which single change gives the biggest measured improvement? (tighter instructions / fewer tools / better memory) **My guess: —**
  - Result: _from the Summary_
- **Bet B** — Baseline: of 6 runs (3 tasks × 2), how many meet **all** must-pass criteria? **My guess: —** runs of 6
  - Result: _from the Baseline_

**Rule of the day: one change at a time.** Change two things and you can't say which one moved the number.

## Setup

- **Benchmark tasks** (frozen, mechanically checkable): [t1 filter by country](../benchmarks/tasks/t1-filter-by-country.md) · [t2 whitespace-name bug](../benchmarks/tasks/t2-whitespace-name-bug.md) · [t3 list_name validation](../benchmarks/tasks/t3-list-name-validation.md). Clear problem, **complete acceptance criteria**, which files to change ([well-scoped issues](https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results#making-sure-your-issues-are-well-scoped)).
- **Clean start per run:** a new issue per run, assigned from `main`. Config changes land on `main` as PRs (issue-assigned runs start from `main`), so record the `main` SHA for every config.
- **Must-pass criteria** (from [Day 18's scorecard](d18-scorecard.md)): tests pass · coverage doesn't drop · 0 new CodeQL alerts · 0 secret-scanning hits · `plan-scope` green · every acceptance criterion met.
- The three knobs map one-to-one to the study guide: *revise instructions, workflows or constraints · refine memory usage · refine tool usage and tool access* ([skills measured](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-600#skills-measured)).

| Config | What changed | Where | `main` SHA |
|---|---|---|---|
| baseline | nothing | — | _sha_ |
| C1 | tighter `.github/copilot-instructions.md`: coverage, no-linter rule, no dependency without an ADR, where endpoints/tests live | `tune/d20-c1` | _sha_ |
| C2 | `bench-implementer` agent with `tools: ["read", "search", "edit", "execute"]`, no MCP tools | `tune/d20-c2` | _sha_ |
| C3 | progress-file rule + `docs/decisions/` pointer in the instructions; stale Copilot Memory facts deleted | `tune/d20-c3` | _sha_ |

Why `bench-implementer` and not Day 3's `implementer`: its *"if there is no approved plan, stop"* rule would stop every benchmark issue, which has no plan. Omitting `tools` would grant **all** tools, MCP included; MCP tools are named `server/tool` or `server/*` ([tools](https://docs.github.com/en/copilot/reference/custom-agents-configuration#tools)).

## Runs

| task | config | run # | PR | tests pass | coverage Δ | new CodeQL alerts | secret-scanning hits | review rounds | time to merge | rating (1–5) | must-pass met? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| t1 | baseline | 1 | | | | | | | | | |
| t2 | baseline | 1 | | | | | | | | | |
| t3 | baseline | 1 | | | | | | | | | |
| t1 | baseline | 2 | | | | | | | | | |
| t2 | baseline | 2 | | | | | | | | | |
| t3 | baseline | 2 | | | | | | | | | |
| t1 | C1 | 1 | | | | | | | | | |
| t2 | C1 | 1 | | | | | | | | | |
| t3 | C1 | 1 | | | | | | | | | |
| t1 | C2 | 1 | | | | | | | | | |
| t2 | C2 | 1 | | | | | | | | | |
| t3 | C2 | 1 | | | | | | | | | |
| t1 | C3 | 1 | | | | | | | | | |
| t2 | C3 | 1 | | | | | | | | | |
| t3 | C3 | 1 | | | | | | | | | |

## Baseline

- Must-pass rate: _/6_ · median review rounds: _ · total new CodeQL alerts: _ · mean rating: _
- **Noise floor** (run 1 vs run 2, per metric): _
- How much this can prove: two baseline runs per task and **one** run per change is a tiny sample. A delta inside the noise floor means nothing; one above it is still weak evidence. Today trains the method, not a statistically valid result.

## Hypotheses

From the failed baseline runs (Day 19's classes): instructions problem (missed a convention, added a dependency) · tool problem (wrong or missing tool calls) · memory/state problem (redid work, contradicted a decision).

## C1: instructions

Each metric baseline → C1, and is the delta bigger than the noise floor? Keep or revert (revert = merge GitHub's **Revert** PR, so later changes stack on the kept config).

## C2: tools

Previous kept config → C2; above the noise floor? Did any run fail *because* a needed tool was removed? That's tool misuse I caused: log it.

## C3: memory

Previous kept config → C3. Single-run tasks are fairly stateless, so C3 is expected to move little; its value shows on **multi-session** tasks (stop and resume, Day 16), where Done / Decided / Next prevent repeats and reversals.

## Summary

| Change | Hypothesis | Metric moved | Delta | Beat noise floor? | Kept / reverted |
|---|---|---|---|---|---|
| C1 instructions | | | | | |
| C2 tools | | | | | |
| C3 memory | | | | | |

- Sample size: n = 2 per task for the baseline, 1 per change. Re-test any "win" before trusting it.
- Next: _what I'd change next, and what I'd never tune by feel again_
