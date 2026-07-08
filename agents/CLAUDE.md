# Agents — Contributor Guide

## Purpose

Agent files define reusable role perspectives for multi-agent skill discussions (e.g. `dtb:plan-review`). Each agent provides a distinct, non-redundant viewpoint.

## File format

- **Filename**: `{rolle}.md`, lowercase (e.g. `architekt.md`, `pragmatiker.md`)
- **Location**: `agents/` in repository root

## Required structure

Each agent file should contain:

0. **Leitsatz** (optional) — a one-line motto giving the role a sharp, opinionated stance. Keeps the role thin but pointed (not a full persona — no voice/filters/risks).
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
| `architekt.md` | System design (macro), technical feasibility, dependencies | `dtb:plan-review` |
| `pragmatiker.md` | Scope, MVP cut, effort-value tradeoffs, spec coverage | `dtb:plan-review` |
| `senior-dev.md` | Implementation feasibility (micro), time estimates, test strategy | `dtb:plan-review` |
| `betriebs-waechter.md` | Deployment, observability, hardening — **conditional** (Ops/Security relevance only) | `dtb:plan-review` |

**Conditional agents:** Architekt, Pragmatiker and Senior Dev are always active. The
Betriebs-Waechter joins only when the plan touches Ops/Security concerns — activation
heuristic lives in `dtb:plan-review` Schritt 2c. Keeps the ensemble at three voices for
plans without operational or security relevance (refactors, docs, internal tooling).

## Language

- Agent files: **German**
- Filenames: **English/lowercase**
