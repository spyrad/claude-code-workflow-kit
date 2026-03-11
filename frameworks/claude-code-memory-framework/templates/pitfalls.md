# Pitfalls (do not repeat)

<!--
Record non-obvious technical issues here as you encounter them.
Format: short description of the trap and the fix/workaround.
Group by technology or domain.
-->

## Example entries (delete these and add your own)

### Git
- Pre-commit hook runs linting - fix issues, don't skip with --no-verify
- Main branch is protected, always use feature branches

### APIs
- Rate limits may differ from documentation - verify empirically
- OAuth tokens expire - track expiry dates in MEMORY.md

### File encoding
- CSV from Windows/Excel has BOM (`\ufeff`) - use `encoding='utf-8-sig'` not `utf-8`
- JSON with trailing commas won't parse with standard parsers

### Docker
- `docker compose` (v2) not `docker-compose` (v1) on modern systems
- Bind mounts may have permission issues on Linux - check UID/GID
