# Day 18: the numbers the agent didn't write, for one PR. Usage: ./scripts/pr_signals.ps1 -Pr 91
param([int]$Pr)
gh pr view $Pr --json number,createdAt,mergedAt,reviews,statusCheckRollup,additions,deletions
# New CodeQL alerts = open alerts on the PR's merge ref minus open alerts on main
gh api "repos/{owner}/{repo}/code-scanning/alerts?ref=refs/pull/$Pr/merge&state=open" --jq 'length'
gh api "repos/{owner}/{repo}/code-scanning/alerts?ref=refs/heads/main&state=open" --jq 'length'
# Secret-scanning alerts are repo-wide: count the ones opened since this PR was created
$since = [datetime](gh pr view $Pr --json createdAt --jq .createdAt)
$alerts = gh api "repos/{owner}/{repo}/secret-scanning/alerts?state=open&per_page=100" | ConvertFrom-Json
@($alerts | Where-Object { [datetime]$_.created_at -ge $since }).Count
