# Memory

## Autonomy Rules
Three levels: ALLOWED / REQUIRES APPROVAL / NEVER / ESCALATE.
Summary in `CLAUDE.md`, full list -> `memory/autonomy-rules.md`

## Memory Update Algorithm
Save: new conventions, discovered pitfalls, new services/scripts, config changes.
Do NOT save: current tasks, temporary state, one-off things.
Details in topic files `memory/` - read them when work touches that domain.

**After every write to MEMORY.md: check `wc -l`. If > 150 lines -> immediately extract largest sections into topic files. Don't wait for 200.**

## Date Format - absolute rule
Format: `YYYY-MM-DD`. NEVER words like "tomorrow", "Thursday". Applies to: all records.

## Project Structure
<!-- Customize for your project -->
- Source: `src/`
- Tests: `tests/`
- Config: `.env` (chmod 600, never commit)

## Pitfalls
All technical traps -> `memory/pitfalls.md`

## Topic files - read when relevant
`autonomy-rules.md` | `pitfalls.md`
<!-- Add more as your project grows -->
