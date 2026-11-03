# Ruleset on `main` (Settings → Rules → Rulesets → New branch ruleset)

Public repo: on GitHub Free, rulesets only work on public repos.

- Enforcement: **Active** · Target: **Default branch**
- **Require a pull request before merging**
  - Required approvals: **1**
  - **Require review from Code Owners**
  - **Require approval of the most recent reviewable push**
- **Require status checks to pass**: add `test` (the CI job name, not the workflow name)
- **Block force pushes** · **Restrict deletions** (on by default)
- Bypass list: empty (or repo admins "for pull requests only")

`mcp-config.json` here is pasted into Settings → Copilot → MCP servers (not committed in the rebuild repo).
The secret is a repo **Agents** secret `COPILOT_MCP_SANCTIONS_API_KEY`.
