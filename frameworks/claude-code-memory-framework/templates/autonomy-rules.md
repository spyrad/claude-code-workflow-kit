# Agent Autonomy Rules - three levels

## ALLOWED - no confirmation needed

Local, reversible actions that don't affect external systems:

- **Reading and exploration**: Read, Glob, Grep, browsing code, analyzing logs
- **Editing local files**: Edit, Write - creating/modifying code, notes, configs
- **Tests and diagnostics**: running tests, linting, local scripts
- **Web browsing**: WebFetch, WebSearch for looking up documentation
- **Git read-only**: status, diff, log, branch --list
- **Git local**: commit (when asked), creating branches, staging
- **Memory updates**: writing to memory/*.md per the update algorithm
- **File organization**: within the defined workspace

## REQUIRES APPROVAL - needs explicit "yes" / "send" / "push"

Actions visible to others, hard to reverse, or costly:

- **Sending emails/messages**: ALWAYS show draft, wait for "send"
- **Git push**: don't push without instruction, even after commit
- **Creating PRs/issues**: on GitHub - show plan, wait for approval
- **Restarting services**: systemctl restart, etc.
- **Deploy**: any deployment target - confirm before each
- **Publication**: posts, comments on external services
- **Expenses**: anything that costs money (beyond free-tier APIs)
- **New cron jobs**: first `--dry-run` + code review, then approval
- **Destructive git**: force push, reset --hard, branch -D - describe what it does, wait
- **Infrastructure changes**: firewall, SSL, ports, DNS

## NEVER - absolute ban, even if user forgets

- **Secrets in memory/docs**: NEVER tokens, passwords, API keys in memory/*.md, CLAUDE.md, commits
- **Committing .env or .bak**: may contain hardcoded credentials
- **Relative date words**: NEVER "tomorrow", "Thursday" - ALWAYS YYYY-MM-DD format
- **Skipping hooks**: NEVER --no-verify, --no-gpg-sign without explicit request
- **Force push main/master**: NEVER - warn even if asked
- **Destructive shortcuts**: don't delete lockfiles, don't bypass safety checks

## ESCALATE - when uncertain

If an action doesn't clearly fit ALLOWED -> **ASK**.
Better to ask once too many than to do something irreversible.

Specifically escalate when:
- Unsure if a file is used before deleting
- Merge conflict - ask about strategy instead of guessing
- Lock file exists - investigate who holds it, don't delete
- Unknown files/branches - may be user's work in progress
- Operation touches multiple systems simultaneously

## Customization

Add your own rules to each section. Examples:
- ALLOWED: "Run docker compose up/down in dev environment"
- REQUIRES APPROVAL: "Modify database migrations"
- NEVER: "Drop database tables without backup"
