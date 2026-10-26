---
name: resume
description: Reload recent context cheaply at the start of a session. Use when the owner says "resume", "catch me up", "what was I working on", or starts a session after time away.
aliases: [catch me up]
argument-hint: "[count | subject | full]"
---

# Resume

Context dies when a session ends. Resume rebuilds it from the vault without reading everything.

## Default

Read only:

1. The **Quick Reference** block of the 3 newest session logs in `sessions_dir`
2. `AGENTS.md` (the current-state table)
3. The **Now** section of the task list

**Do not read full session logs** unless asked or unless the Quick Reference blocks are not enough. If you do, say so.

## Variants

| Argument | Behavior |
|---|---|
| none | Last 3 sessions, Quick Reference only |
| a number, e.g. `10` | That many sessions, Quick Reference only |
| a subject, e.g. `Acme` | Recent sessions, a search across session logs for the subject, plus the newest two blocks of that subject's `Current State.md` |
| `full` | The newest session log in full |

## Output

Open with 3 to 5 lines, not a report:

- what was in flight
- what is overdue, **the owner's own commitments first**
- what needs a decision today

Then stop and let the owner steer.
