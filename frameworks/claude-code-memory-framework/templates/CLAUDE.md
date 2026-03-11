# Global Instructions

# Uncomment and customize:
# - Always respond in [your language].
# - Code, commands, and file names stay in English.
# - [Your formatting preferences here]

## Agent Autonomy Rules

Three permission levels. Full list -> `memory/autonomy-rules.md`

- **ALLOWED**: reading, editing files, exploration, tests, diagnostics, local git, memory updates
- **REQUIRES APPROVAL**: sending emails, git push, restart services, deploy, publication, expenses, destructive git
- **NEVER**: secrets in memory, skipping safety hooks, destructive shortcuts
- **ESCALATE**: if unsure which category an action belongs to - ASK
