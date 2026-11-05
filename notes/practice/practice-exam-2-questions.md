# Practice exam 2 — docs-based set (Q13–45)

> 33 questions for Day 26, weighted like the exam: 7 Domain 1 · 11 Domain 2 · 6 Domain 3 · 9 Domain 4. Q1–12 are the community mock's Q30–41. Not official. Answer key at the bottom: don't scroll until the timer ends.

## Domain 1 — Agent architecture & SDLC

**13.** Where does a repository-level custom agent profile live?
A) `.github/copilot/agents.yml` · B) `.github/agents/<name>.agent.md` · C) `AGENTS.md` · D) `.copilot/agents/<name>.json`

**14.** Which frontmatter property is **required** in a custom agent profile?
A) `name` · B) `tools` · C) `description` · D) `model`

**15.** A repository and its organization both define a custom agent called `reviewer`. Which one does the cloud agent use in that repository?
A) The organization's · B) The repository's · C) The newer one · D) Neither; the name clash disables both

**16.** Which agent-profile feature does the Copilot **cloud agent** not support?
A) `tools` · B) `mcp-servers` · C) `handoffs` · D) `model`

**17.** A rule must apply only to files under `tests/`. Where does it go?
A) `AGENTS.md` · B) `.github/copilot-instructions.md` · C) `.github/instructions/tests.instructions.md` with `applyTo: "tests/**"` · D) the agent profile's `description`

**18.** Which branches can the Copilot cloud agent push to?
A) Any non-protected branch · B) Only branches that start with `copilot/` · C) The default branch, if rulesets allow · D) Only the branch the issue names

**19.** Who can assign an issue to the Copilot cloud agent and have it act on PR comments?
A) Anyone who can see the repo · B) Users with write access · C) Org owners only · D) Anyone with a Copilot license

## Domain 2 — Tool use & environment

**20.** What makes the cloud agent install dependencies before it starts?
A) `.github/copilot-setup.sh` · B) A workflow `.github/workflows/copilot-setup-steps.yml` with a job named `copilot-setup-steps` · C) The `setup` key in `AGENTS.md` · D) A `sessionStart` hook only

**21.** A setup step exits non-zero. What happens?
A) The session aborts · B) Copilot retries the step · C) Copilot skips the remaining setup steps and starts with the environment as it is · D) The PR is closed

**22.** Which runners can the cloud agent use?
A) Any GitHub-hosted runner · B) Ubuntu x64 and Windows 64-bit GitHub-hosted runners, or self-hosted · C) macOS only for iOS repos · D) ARM runners only

**23.** You move the cloud agent to self-hosted runners. What about the integrated firewall?
A) Add the runner host to the allowlist · B) It works unchanged · C) It isn't compatible: disable it and use your own network controls · D) It's enforced by the runner group

**24.** What does the cloud agent's firewall cover?
A) Setup steps and MCP servers · B) Only processes the agent starts through its Bash tool · C) All network traffic on the runner · D) Only `web_fetch`

**25.** The custom allowlist contains `packages.contoso.corp`. Which host is allowed?
A) `contoso.corp` · B) `artifacts.contoso.corp` · C) `eu.packages.contoso.corp` · D) All of `*.contoso.corp`

**26.** Who sets the repository's MCP configuration for the cloud agent?
A) Enterprise owners · B) Org owners only · C) Repository admins · D) Any writer

**27.** Which MCP capability does the cloud agent use?
A) Tools only · B) Tools and resources · C) Tools, resources and prompts · D) Prompts only

**28.** Which tool alias lets a custom agent run shell commands?
A) `shell` · B) `bash` · C) `execute` · D) `run`

**29.** A profile lists `tools: ["read", "deploy"]`. What happens to `deploy`?
A) The profile fails to load · B) It's silently ignored · C) It's treated as `execute` · D) The agent asks the user

**30.** A `preToolUse` guard on the cloud agent returns `permissionDecision: "ask"`. Result?
A) The user gets a prompt · B) Treated as `allow` · C) Treated as `deny`: nobody is there to answer · D) The hook is skipped

## Domain 3 — Memory, state & execution

**31.** How long does Copilot Memory keep a fact that is never used?
A) 7 days · B) 28 days · C) 90 days · D) Until a repo owner deletes it

**32.** Before using a repository fact, Copilot Memory…
A) asks the user · B) checks its citations against the current branch · C) re-reads `AGENTS.md` · D) uses it as is

**33.** Which memories does Copilot **code review** use?
A) Repository facts only · B) Repository facts + the PR author's preferences · C) All users' preferences · D) None

**34.** Copilot CLI is near its token limit. When does background compression start?
A) ~50% · B) ~65% · C) ~80% · D) Only on `/compact`

**35.** Across sessions, a progress file stops repeats with *Done* and reversals with *Decided*. What stops **drift** from the original goal?
A) A longer *Next* section · B) The issue's acceptance criteria kept in the file · C) Copilot Memory · D) Shorter sessions

**36.** Two local agent sessions edit the same repo at once. The cleanest isolation?
A) Two branches in one working copy · B) A git worktree per session · C) Stash between turns · D) One session read-only

## Domain 4 — Evaluation, error analysis & tuning

**37.** Copilot code review leaves a review on a PR in a repo that requires one approval. Does it count?
A) Yes, always · B) No: by default it leaves a *Comment* review, not an approval · C) Only for Copilot PRs · D) Only from a code owner

**38.** A Copilot PR body shows a firewall warning with a blocked address. Failure class?
A) Reasoning · B) Tool misuse · C) Environment · D) Evaluation

**39.** An agent never ran the tests, though its profile lists `tools: ["read", "edit", "tests"]`. First place to look?
A) Copilot Memory · B) The profile: `tests` isn't an alias and is silently ignored, so it has no `execute` · C) The firewall log · D) The ruleset

**40.** The best evidence that an agent's PR is good, without trusting its own summary?
A) The PR description · B) CI results, coverage, code-scanning check and alerts, human review rounds · C) The agent's self-rating · D) The number of commits

**41.** You're tuning an agent profile against a benchmark. The sound method?
A) Change instructions and tools together to save runs · B) Same fixed task set, change one variable per run, compare measured deltas · C) A new task set per version · D) Judge by reading the summaries

**42.** Before finishing, which checks does the cloud agent run on its own changes?
A) None; that's CI's job · B) CodeQL, secret scanning and a dependency check against the Advisory Database · C) Only unit tests · D) Only linting

**43.** On a `preToolUse` command hook, the script prints `allow` and exits `2`. Result?
A) Allow with a warning · B) Deny: exit code beats stdout · C) The hook is retried · D) Ignored

**44.** A `preToolUse` guard **times out**. Result?
A) Deny (fail-closed) · B) Fail-open: the call skips the guard and goes through the normal permission flow · C) The session aborts · D) Retried once

**45.** A `postToolUse` hook exits `1`. Result?
A) The next tool call is denied · B) The session stops · C) Logged; the run continues · D) The last call is rolled back

---

## Answer key

| Q | Ans | Why | Doc |
|---|---|---|---|
| 13 | B | Repo profiles are `.github/agents/*.agent.md` | [Custom agents](https://docs.github.com/en/copilot/reference/custom-agents-configuration) |
| 14 | C | `description` is the only required property; `name` defaults from the file name | [Custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration) |
| 15 | B | On a name clash the lower level wins: repository over organization over enterprise | [Custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration) |
| 16 | C | `handoffs` is an IDE feature; the cloud agent ignores it | [Custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration) |
| 17 | C | Path-specific instructions use `applyTo` globs | [Repository custom instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions) |
| 18 | B | It can only push to `copilot/` branches | [Risks and mitigations](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations) |
| 19 | B | Only write-access users can trigger it; others' comments aren't passed to it | [Risks and mitigations](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations) |
| 20 | B | The job name must be `copilot-setup-steps` | [Customize the agent environment](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/customize-the-agent-environment) |
| 21 | C | No abort, no retry: check the setup-steps run is green | same |
| 22 | B | Ubuntu x64 / Windows 64-bit hosted; no macOS or ARM | same |
| 23 | C | Firewall isn't compatible with self-hosted runners | same |
| 24 | B | Only Bash-tool processes; not setup steps, not MCP servers | [Customize the firewall](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-the-firewall#limitations) |
| 25 | C | A domain entry allows itself and subdomains, never siblings or the parent | same |
| 26 | C | Repo admins (org owners only because they're admin everywhere) | [MCP and cloud agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/mcp-and-cloud-agent) |
| 27 | A | Cloud agent supports MCP tools only | same |
| 28 | C | Aliases: `read`, `edit`, `search`, `execute`, `agent`, `web`, `todo` | [Custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration) |
| 29 | B | Unknown tool names are silently ignored | same |
| 30 | C | On the cloud agent `ask` = deny | [Hooks reference](https://docs.github.com/en/copilot/reference/hooks-reference) |
| 31 | B | Deleted after 28 days unused; use after validation can reset the timer | [Copilot Memory](https://docs.github.com/en/copilot/concepts/agents/copilot-memory) |
| 32 | B | Citations checked against the current branch; only validated facts are used | same |
| 33 | A | Review = facts only; CLI = facts + the initiating user's preferences | same |
| 34 | C | ~80% (blocks at ~95% until compaction finishes); `/compact` any time | [Copilot CLI context management](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/overview#context-management) |
| 35 | B | Done stops repeats, Decided stops reversals, acceptance criteria stop drift | [Get the best results](https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results) |
| 36 | B | A worktree gives each session its own working copy on its own branch | [git worktree](https://git-scm.com/docs/git-worktree) |
| 37 | B | Copilot reviews don't count toward required approvals (a *Copilot approvals* setting is preview) | [About Copilot code review](https://docs.github.com/en/copilot/concepts/agents/code-review) |
| 38 | C | Firewall block = environment | [Customize the firewall](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-the-firewall) |
| 39 | B | No `execute` → can't run tests; the bad name fails silently | [Custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration) |
| 40 | B | Measure with signals the agent can't write | [Get the best results](https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results) |
| 41 | B | One variable at a time on a fixed set, or the delta means nothing | Day 20 tuning report |
| 42 | B | Built-in security validation on its own code | [About cloud agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent) |
| 43 | B | On `preToolUse` / `permissionRequest`, exit 2 denies | [Hooks reference — exit codes](https://docs.github.com/en/copilot/reference/hooks-reference#exit-codes-for-command-hooks) |
| 44 | B | Timeouts are always fail-open | [Hooks reference — preToolUse](https://docs.github.com/en/copilot/reference/hooks-reference#pretooluse--pretooluse) |
| 45 | C | Only gate events can block; others log and continue | [Hooks reference — exit codes](https://docs.github.com/en/copilot/reference/hooks-reference#exit-codes-for-command-hooks) |
