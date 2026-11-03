# Day 28 — Exam day: GH-600

> No new material. A 25-minute morning pass over the *Know cold* lines, Day 25's matrix and the starred gaps, then 120 minutes with one rule: **the minimum control that still blocks the risk**.

**Deliverable:** GH-600 sat, result and per-domain feedback in [gap-log.md](gap-log.md#exam-result)

## Morning (15 min, paper, closed-book): know cold

Say each answer out loud, then check against the day's note.

- **Day 7** ([d05-controls](d05-controls.md)): instruction-file precedence · custom instructions vs custom agents vs skills · human checkpoints without approving every step.
- **Day 14** ([d08-tools](d08-tools.md), [d09-mcp](d09-mcp.md), [d10](d10-mcp-governance.md), [d11](d11-env.md)): agent frontmatter + tool aliases · MCP config locations · cloud agent limits · firewall defaults · where registry/allowlist policies are set.
- **Day 21** ([practice-exam-1](practice-exam-1.md#know-cold)): which evidence proves which failure class · measuring an agent without trusting its own summary.
- **Domain 5** ([d22](d22-patterns.md), [d23](d23-posthoc.md), [d24](d24-recovery-runbook.md)):
  - Pattern → how it fails: sequential, early errors flow downstream · concurrent, needs a rule for contradictory results · maker-checker, needs an iteration cap + human fallback.
  - Isolation: task → branch → PR on the cloud agent; one worktree per local agent; file scope enforced by a required check.
  - No `handoffs:` on the cloud agent: use the `agent` alias or a human-gated flow.
  - **Stop session** keeps the commits already pushed. `sessionEnd` reasons: `complete`, `error`, `abort`, `timeout`, `user_exit`.
  - Agent version = commit SHA of the profile; name clash → repository wins.
  - Retire = `disable-model-invocation: true` + `user-invocable: false`, then delete; history stays in git.
- **Domain 6** ([d25](d25-autonomy-matrix.md)):
  - Classify by operational / security / compliance risk, then by reversibility.
  - The built-ins already stop agent self-merge (human review, requester can't approve, workflows wait for approval): **don't add approvals there**.
  - Agent config → CODEOWNERS + *Require review from Code Owners*.
  - Environment required reviewers: only on public repos for Free/Pro/Team.
  - Irreversible paths → `preToolUse` deny.
  - A policy a machine can check (synthetic data only) → a **required check**, not a human approval.

Skip anything new: unread docs, new mocks, forum threads.

## Morning (10 min): matrix + starred gaps

- [d25-autonomy-matrix.md](d25-autonomy-matrix.md): cover the Control column, name it, then look.
- Only the gap-log lines starred in [Day 27's read 2](d27-rebuild.md#gap-log).

## Exam rules

- **Closed-book.** No Microsoft Learn on GitHub exams. — [Exam experience](https://learn.microsoft.com/en-us/credentials/support/exam-duration-exam-experience#accessing-microsoft-learn-during-your-certification-exam)
- Unscheduled breaks are allowed but **the clock keeps running**, and after a break you **can't return to any question already seen**, flagged or unanswered. Clear flags before a break. — [Unscheduled breaks](https://learn.microsoft.com/en-us/credentials/support/exam-duration-exam-experience#unscheduled-breaks-on-exams)
- Start a break only with *Take a break* in the exam UI; leaving camera view any other way revokes the exam.

## Tactic and pacing

- *"Which control"* → the **minimum** control that still blocks the risk.
- Read the **last sentence** of each question first.
- Stuck over ~2 min: best guess, flag, move on. Change a flagged answer only for a concrete doc fact. No blanks.
- Pacing marks for the scratch board: **¼ at 30 min · ½ at 60 · ¾ at 90 · first pass done by ~100**, flags after.

## After

- Result and per-domain feedback → [gap-log.md › Exam result](gap-log.md#exam-result).
- Next: NVIDIA NCP-AAI. Rest of the day off.

## Reflection

- Strongest and weakest domain in the real exam, compared with the mocks?
- What from these 28 days do I use at work on Monday?
- Which one guardrail would I propose first for agent use in the department, and who would own it?
