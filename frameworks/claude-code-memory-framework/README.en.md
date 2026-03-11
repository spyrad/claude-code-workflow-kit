# Claude Code Memory Framework

Patterns for effective AI agent memory management in Claude Code - developed through daily production use. Not another `CLAUDE.md` tutorial, but specific techniques missing from the default setup.

> **[Wersja polska (domyslna)](README.md)**

## What You'll Find Here (That Claude Code Doesn't Give You)

Claude Code has a built-in memory system - `CLAUDE.md`, `memory/` directory, auto-loaded `MEMORY.md`. It works. But after a few weeks of intensive use, you'll hit problems the defaults don't solve:

- The agent does something destructive because it "assumed" it could
- Memory grows until it gets truncated mid-sentence
- The same technical bugs repeat every few sessions
- The agent saves current tasks instead of lasting knowledge

This framework addresses these problems with three patterns:

## 1. Agent Autonomy Model

**Problem:** Claude Code has a general "ask before risky actions" guideline, but doesn't define what's risky in *your* environment. The agent guesses - sometimes right, sometimes not.

**Solution:** An explicit taxonomy with four permission levels.

```markdown
## ALLOWED - no confirmation needed
- Read files, explore codebase, run tests
- Edit local files, create commits (when asked)
- Update memory files
- Local git operations (status, diff, log, branch)

## REQUIRES APPROVAL - wait for explicit "yes" / "send" / "push"
- Send emails or messages
- Git push, create PRs/issues
- Restart services, deploy
- Anything that costs money
- Destructive git (force push, reset --hard)
- Infrastructure changes (firewall, SSL, DNS)

## NEVER - hard ban, even if user forgets
- Secrets in memory files or commits
- Expensive API calls without consent
- Destructive operations as shortcuts (deleting lockfiles, --no-verify)
- Skipping safety hooks

## ESCALATE - when uncertain
If an action doesn't clearly fit ALLOWED -> ASK.
Better to ask once too many than to do something irreversible.
```

**Why it works:** The agent follows clear, explicit rules. "NEVER commit .env" is more effective than "be careful with .env". The ESCALATE level is key - it gives the agent a safe "I don't know, let me ask" option instead of guessing.

**How to customize:** The template in `templates/autonomy-rules.md` has a Customization section. Add rules specific to your environment. The more cases you cover, the less the agent guesses.

## 2. Institutional Knowledge (Pitfalls File)

**Problem:** The agent hits a non-obvious technical issue, solves it after 15 minutes of trial and error, and the next session starts from scratch and falls into the same trap.

**Solution:** A dedicated `pitfalls.md` file that turns mistakes into institutional knowledge.

```markdown
# Pitfalls (do not repeat)

## Docker
- `docker compose` (v2) not `docker-compose` (v1) on this system
- Port 3000 is used by dev server, don't bind to it

## APIs
- Rate limit on endpoint X is 10/min, not 100/min as docs suggest
- OAuth token expires every 60 days, monitor and refresh

## File encoding
- CSV from Windows/Excel has BOM (`\ufeff`) - use `encoding='utf-8-sig'` not `utf-8`
- JSON with trailing commas won't parse with standard parsers

## Git
- Pre-commit hook runs linting - fix issues, don't skip with --no-verify
- Main branch is protected, always use feature branches
```

**Why it works:** Claude Code doesn't suggest creating such a file. CC's memory system is generic - "save conventions and patterns." A pitfalls file is a specific knowledge category with an extremely high value-to-size ratio. One entry (2 lines) saves 15 minutes of debugging in every future session.

**How to maintain:** Record the pitfall immediately after solving the problem. Don't postpone - you'll forget the context. Group by technology. Review quarterly and remove outdated entries.

## 3. Proactive Memory Size Management

**Problem:** `MEMORY.md` grows with each session. At 200 lines, Claude Code truncates it - you lose context without warning, often mid-section.

**Solution:** The 150-line rule and an update algorithm.

### Overflow rule

```
After every write to MEMORY.md, check line count.
If > 150 -> immediately extract largest sections into topic files.
Never let it reach 200 (truncation threshold).
```

The 50-line buffer gives you a safety margin. At 150 lines you have time to reorganize. At 200 it's already too late.

### Update algorithm

```
SAVE:
  - Conventions confirmed across multiple interactions
  - Technical pitfalls (-> pitfalls.md)
  - New services, scripts, integrations
  - Configuration changes affecting future work

DO NOT SAVE:
  - Current tasks or work in progress
  - Temporary state or one-off fixes
  - Anything that duplicates CLAUDE.md
  - Unverified conclusions from reading a single file
```

**Why it works:** CC says "max 200 lines" and stops there. It doesn't say what to do to stay under that limit. The update algorithm solves "what to save" (most users save too much or too little), and the 150 rule solves "when to extract" (before it's too late).

### MEMORY.md as index pattern

```markdown
# Memory

## Agent autonomy
Three levels: ALLOWED / REQUIRES APPROVAL / NEVER / ESCALATE.
Full list -> `memory/autonomy-rules.md`

## Production server
Stack, ports, backup, SSL. Details -> `memory/server.md`

## Technical pitfalls
All -> `memory/pitfalls.md`

## Topic files - read when relevant
`autonomy-rules.md` | `pitfalls.md` | `server.md` | `tools.md`
```

One-line summary + pointer to file. Never copy content - single source of truth.

## Quick Start

### 1. Create the structure

```bash
mkdir -p ~/.claude/projects/$(basename "$PWD")/memory
```

### 2. Copy the templates

```bash
git clone https://github.com/pawel-wyszomirski/claude-code-memory-framework.git /tmp/ccmf

# Global instructions (if you don't have CLAUDE.md yet):
cp /tmp/ccmf/templates/CLAUDE.md ~/.claude/CLAUDE.md

# Memory files for your project:
cp /tmp/ccmf/templates/MEMORY.md ~/.claude/projects/$(basename "$PWD")/memory/
cp /tmp/ccmf/templates/autonomy-rules.md ~/.claude/projects/$(basename "$PWD")/memory/
cp /tmp/ccmf/templates/pitfalls.md ~/.claude/projects/$(basename "$PWD")/memory/

rm -rf /tmp/ccmf
```

### 3. Customize

- `CLAUDE.md` - language, formatting, behavioral preferences
- `autonomy-rules.md` - add rules specific to your environment
- `pitfalls.md` - fill in as you work
- `MEMORY.md` - grows organically, enforce the 150-line rule

## Best Practices

### Absolute rules, not soft guidelines
"NEVER commit .env" instead of "be careful with .env." The agent follows clear rules. It interprets vague ones on its own.

### Date format
Use `YYYY-MM-DD` in memory files. Never "tomorrow" or "next week" - meaningless across sessions.

### Pointers, not copies
Don't duplicate content between files. `Details -> memory/file.md`. Single source of truth.

### Security audit
Record in MEMORY.md when you last reviewed secrets. Set a monthly reminder.

```markdown
## Security
- Last secrets audit: 2025-06-01 (2 leaks fixed)
- Next review: 2025-07-01
```

### Monthly memory review
Memory degrades. Once a month, review files, remove outdated entries, update what changed. Pitfalls file - once a quarter.

## What This Framework Does NOT Do

For clarity - these things are built into Claude Code and don't need separate configuration:

- Loading `CLAUDE.md` every session (built-in)
- Auto-loading `MEMORY.md` (built-in)
- `memory/` directory with topic files (built-in)
- Semantic memory organization (suggested by CC)
- Truncation at 200 lines (built-in)

This framework builds **on top of** these mechanisms, it doesn't replace them.

## Why Not a Database?

| Approach | Pros | Cons |
|----------|------|------|
| **SQLite + vectors** | Semantic search | Complex setup, opaque, noisy |
| **Auto-capture everything** | Zero effort | Low signal/noise, bloated context |
| **Markdown + curation (this)** | Readable, versionable, auditable | Requires manual curation |

Manual curation is the feature, not the bug. `cat memory/pitfalls.md` and you see exactly what the agent knows. Version with git. Transfer with `scp`.

## Contributing

This framework emerged from daily production use. If you've discovered patterns that work well with Claude Code's memory, PRs and issues are welcome.

## License

MIT
