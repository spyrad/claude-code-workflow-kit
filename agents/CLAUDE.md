# Agents — Contributor Guide

## Purpose

Agent files define reusable role perspectives for multi-agent skill discussions (e.g. `dtb:plan-review`). Each agent provides a distinct, non-redundant viewpoint.

## File format

- **Filename**: `{rolle}.md`, lowercase (e.g. `architekt.md`, `pragmatiker.md`)
- **Location**: `agents/` in repository root

## Required structure

Each agent file should contain:

1. **Rolle** — Name and one-line description of the perspective
2. **Perspektive** — What this agent focuses on (technical design, scope, implementation feasibility, etc.)
3. **Verhalten** — How the agent argues: what it prioritizes, what it challenges
4. **Typische Fragen** — Example questions this agent would ask

## Design principles

- Every agent must have a **unique perspective** — no overlap with other agents
- Agents argue **from their role**, not generically
- Questions must be **decision-relevant** — no rhetorical questions
- Keep agent files **concise** (under 40 lines)

## Current agents

| Agent | Perspective | Used by |
|-------|-------------|---------|
| `architekt.md` | System design, technical feasibility, dependencies | `dtb:plan-review` |
| `pragmatiker.md` | Scope, MVP cut, effort-value tradeoffs | `dtb:plan-review` |
| `senior-dev.md` | Implementation feasibility, time estimates, test strategy | `dtb:plan-review` |

## Language

- Agent files: **German**
- Filenames: **English/lowercase**
