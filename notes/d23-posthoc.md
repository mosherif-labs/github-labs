# Day 23 — The auditor's replay: multi-agent observability & post-hoc analysis

> Reconstruct Monday's three-agent run from the artifacts alone, then fix the gaps with a handoff block every agent fills in.

**Deliverable:** this note: an audit trail someone else could follow without asking me

## Bets

- **Bet A** — On a cloud agent commit, who is the **author** and who is the **co-author**? **My guess: —**
  - Result: **Copilot is the author, the person who started the task is the co-author**, and every commit message links to its session log ([Trace commits to session logs](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/manage-and-track-agents#trace-commits-to-session-logs))
- **Bet B** — On a **free org**, can one audit-log search qualifier pull every action Copilot took? **My guess: —**
  - Result: _from Mission 4_. The org audit log supports `actor:Copilot`; the agent-specific fields (`actor_is_agent`, `agent_session_id`) are documented for the **enterprise** audit log ([agentic audit events](https://docs.github.com/en/copilot/reference/agentic-audit-log-events))

## Where the evidence lives

| Question an auditor asks | Artifact | Source |
|---|---|---|
| Why did the agent do that? | **Session log**: internal reasoning + the tools it used | [Review session logs](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/manage-and-track-agents#review-session-logs) |
| Which session made this commit, for whom? | Commit: author **Copilot**, co-author **the human**; message links to the session log | [Trace commits](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/manage-and-track-agents#trace-commits-to-session-logs) |
| Is there always a human attached? | Yes: the developer co-authors; for automations, the **person who created the automation** | [Risks: losing sight of agents' work](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations#administrators-can-lose-sight-of-agents-work) |
| What happened org-wide that day? | Org audit log: **owners only**, last **180 days**; `actor:octocat actor:Copilot` = either; `-actor:Copilot` excludes; export JSON/CSV | [Org audit log](https://docs.github.com/en/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/reviewing-the-audit-log-for-your-organization#search-based-on-the-actor) |
| Which session, on whose behalf? (enterprise) | Agentic events carry `actor_is_agent: true`, `agent_session_id`, `user` (the initiator), `action` (e.g. `pull_request.create`); filter `actor:Copilot` | [Agentic audit events](https://docs.github.com/en/copilot/reference/agentic-audit-log-events) |

## Handoff template every agent writes

[`.github/pull_request_template.md`](../.github/pull_request_template.md) gives humans the **Handoff** block (agent/human · inputs with SHAs · decisions · open risks · next owner · evidence). Templates live at the root, `docs/` or `.github/`, several go in `PULL_REQUEST_TEMPLATE/` with the `template` query parameter, and they only take effect **once merged into the default branch** ([PR templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository#adding-a-pull-request-template)).

The docs don't say the cloud agent fills in the PR template, so the same rule is in `.github/copilot-instructions.md` and in the `planner`, `implementer` and `reviewer` profiles: *End every PR description with the Handoff block from `.github/pull_request_template.md`, filled in.*

## Reconstruct Monday's run

| Issue | Branch | PR | Commits | Merge commit | Approved by | Merged by |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |
| | | | | | | |

- One agent commit: author _, co-author trailer _, session-log link _
- From each session log: files read first · tool calls that changed files · tests run before pushing
- The overlap: the conflicted PR _, the resolution commit _, resolved by a human or an agent _

## Audit log pass

- `actor:Copilot` → _what it shows_ · `-actor:Copilot` → _the human side of the same day_
- Export: `notes/evidence/d23-audit.csv` (synthetic org)

## Timeline

| Time | Event | Actor (agent / human) | Artifact link |
|---|---|---|---|
| | | | |

## Decisions & handoffs

| Decision | Who | Recorded where | What they knew at the time |
|---|---|---|---|
| plan approved | | | |
| merge order | | | |
| conflict resolution | | | |

| Handoff | From → to | Artifact that carried it |
|---|---|---|
| plan → implementation | planner → implementer | plan PR + `plans/<issue>.md` at a SHA |
| implementation → review | implementer → reviewer | PR diff + Handoff block |
| review → merge | reviewer → human | review findings in the PR |

## Outcome & gaps

- Outcome: _
- Questions the artifacts could **not** answer (what the Handoff block must fix): which plan SHA an agent implemented · what it chose not to verify · who acts next

Stranger test: reread as someone who wasn't there; any sentence that needs me to explain it gets a link or gets rewritten.
