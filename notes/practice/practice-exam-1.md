# Day 21 — Practice exam 1 (Domains 1–4) + the Week 3 gate

> 29 timed questions, closed-book, scored by domain. Every miss and every lucky guess goes to the gap log.

**Deliverable:** this note (scores by domain, know-cold answers, Week 3 gate) + every miss in [gap-log.md](gap-log.md)

## Bet

- **Bet A** — My Domains 1–4 score: **—%**
  - Result: _from Scores_

## The exam room

- Source: the [community mock](https://github.com/jtur671/gh-600-study-guide) (`mock-exam.md`), **unofficial** and community-made. 41 questions: Q1–7 Domain 1 · Q8–17 Domain 2 · Q18–22 Domain 3 · Q23–29 Domain 4 · Q30–41 Domains 5–6.
- Today: **Q1–29 only**, **60 minutes** (≈ 2 min each), closed-book, no AI, phone timer. When the mock and the docs disagree, **the docs win**.
- Answer sheet: question # · answer · confidence (sure / guess) · domain.
- Pacing: Q29 by ~50 min, then flagged questions only; change an answer only for a concrete reason.

## Scores

Official weights ([skills measured](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-600#skills-measured)): 1 Agent architecture & SDLC **15–20%** · 2 Tool use & environment **20–25%** · 3 Memory, state & execution **10–15%** · 4 Evaluation, error analysis & tuning **15–20%** · 5 Multi-agent coordination **15–20%** · 6 Guardrails & accountability **10–15%**. Pass mark: **700** or more.

| Domain | Questions | Correct | % | < 75% → Day 26 list? |
|---|---|---|---|---|
| 1 Agent architecture & SDLC | Q1–7 (7) | | | |
| 2 Tool use & environment | Q8–17 (10) | | | |
| 3 Memory, state & execution | Q18–22 (5) | | | |
| 4 Evaluation, error analysis & tuning | Q23–29 (7) | | | |
| **Domains 1–4 total** | 29 | | | Gate 2 needs **≥ 80%** |

Lucky guesses (marked *guess*, got right): _list them; they count as misses for the gap log_

## Know cold

**Which evidence proves which failure class?** (Days 18–19)

- **Environment:** the firewall warning in the PR body or a comment shows the blocked address and command; setup-step failures show in the workflow run.
- **Reasoning:** the session log's reasoning or the plan shows where it misread or picked between conflicting criteria.
- **Tool misuse:** the session log's tool calls, plus the agent profile, since unrecognized tool names are silently ignored.

**How do you measure an agent without trusting its own summary?**

- CI results, coverage from logs, the **Code scanning results** check (fails on `error` / `critical` / `high` by default), secret-scanning and Dependabot alerts, human review rounds and a rating written before reading the summary, and commits that link back to their session logs.

## Week 3 gate: Domain 3 and 4 bullets

Rate each bullet in the **GH-600 objectives** issue: **green = I did it myself this week** (paste the proof link), amber, or red. Gate: all Domain 3 and 4 bullets green; every amber/red goes on the Day 26 remediation list with the day whose lab to redo.

| Domain | Bullet | Rating | Evidence / redo day |
|---|---|---|---|
| 3 | Manage memory (Copilot Memory, repo facts) | | Day 15 |
| 3 | Durable state across sessions (progress file) | | Day 16 |
| 3 | Detect drift, stale and conflicting context | | Day 17 |
| 4 | Success criteria and evaluation signals | | Day 18 |
| 4 | Identify failures from logs, plans, traces, artifacts; classify root causes | | Day 19 |
| 4 | Tune instructions, tools and memory with measured deltas | | Day 20 |
