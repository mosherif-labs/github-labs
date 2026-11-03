# Day 26 — Practice exam 2 (all six domains) + go/no-go

> 45 timed questions in 90 minutes, closed-book, scored by domain. The gate decides whether Sunday is exam day, not the mood after the last question.

**Deliverable:** this note (scores by domain, remediation, gate) + every miss in [gap-log.md](gap-log.md)

## Bet

- **Bet** — My overall score: **—%** (win if within ±5 points)
  - Result: _from Score by domain_

## The exam room

- **Q1–12:** the [community mock](https://github.com/jtur671/gh-600-study-guide) (`mock-exam.md`) **Q30–41** (Domains 5–6, unseen on Day 21). Unofficial.
- **Q13–45:** the docs-based set in [practice-exam-2-questions.md](practice-exam-2-questions.md): 7 Domain 1 · 11 Domain 2 · 6 Domain 3 · 9 Domain 4. Each answer cites the doc that settles it. Don't scroll to the key until the timer ends.
- Microsoft's free practice assessments have no GH-600 entry (checked 2026-10-08), so the set is self-built. Where any question contradicts the docs, **the docs win**.
- **90 minutes**, phone timer, VS Code / docs / notes closed. Answer sheet: # · answer · sure/guess · domain.
- Pacing: ~15 questions at 30 min, ~30 at 60 min, first pass done by ~80 min. Over ~2 min on one question: best answer, **flag**, move on. Change a flagged answer only if you can name the doc fact. No blanks.
- *"Which control"* questions: pick the **minimum** control that still blocks the risk.

## Score by domain

| Domain | Weight | Questions | Correct | % | Day 21 % |
|---|---|---|---|---|---|
| 1 Agent architecture & SDLC | 15–20% | 7 | | | |
| 2 Tool use & environment | 20–25% | 11 | | | |
| 3 Memory, state & execution | 10–15% | 6 | | | |
| 4 Evaluation, error analysis & tuning | 15–20% | 9 | | | |
| 5 Multi-agent coordination | 15–20% | mock Q30–41 (split by the mock's tags) | | | — |
| 6 Guardrails & accountability | 10–15% | | | | — |
| **Total** | | 45 | | | |

Lucky guesses (marked *guess*, got right) count as misses: log them too.

## Study guide re-read

Read each [skills measured](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-600#skills-measured) bullet against the **GH-600 objectives** issue; relabel anything not green.

- Domain 2 is the heaviest (**20–25%**); Domains 3 and 6 are the lightest (**10–15%** each).
- Domain 5 bullets map to Days 22–24, Domain 6 bullets to Day 25's [autonomy matrix](d25-autonomy-matrix.md).
- Most questions cover **GA** features, but commonly used **Preview** features can appear.
- The study guide's guardrails link is two URLs glued together: open *Building guardrails for GitHub Copilot cloud agent* and *Risks and mitigations* separately.

## Remediation

Two lists, from the docs only: today's weakest domain, then the **Day 26 remediation list** in [gap-log.md](gap-log.md) (Day 21's list first if time runs short: those gaps are a week older). Re-read only the section behind each miss, then re-answer the question closed-book.

| Miss | Domain | Doc section re-read | Re-answer ✓ |
|---|---|---|---|
| | | | |

## Gate: go / no-go

| Gate | Rule | Status |
|---|---|---|
| G1 | Every objective green in the objectives issue | |
| G2 | Today's set **≥ 85%** and Day 21's Domains 1–4 **≥ 80%** | |
| G3 | Day 27's timed rebuild under **2 h** (checked tomorrow). A fail means a focused review of what slowed me, **not** a reschedule | rule set |
| G4 | Per domain, I can explain why each control beats the alternatives | |

**If G1, G2 or G4 is red, decide today.** A reschedule is free only [at least 24 hours before the appointment](https://learn.microsoft.com/en-us/credentials/support/reschedule-and-cancellation-policy#rescheduling-and-cancellation-policy-details), so Friday is the last safe day. Moving GH-600 a week means repeating Days 25–27 and eating NCP-AAI's study window, so only a badly failed gate justifies it.

**Decision:** _go / no-go, and why_

## Reflection

- Which kind of question cost the most time, and why?
- Was the score bet calibrated? What does that say about Sunday?
- Which scenario sounded most like a real change-control argument at the bank, and would I pick the same control at work?
