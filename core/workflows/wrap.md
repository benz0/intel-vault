---
name: wrap
description: Save the session to a searchable log and update the task list and subject state. Use when the owner says "wrap", "wrap up", "save this session", or is ending a working session.
aliases: [wrap up, save this session]
argument-hint: ""
---

# Wrap

## 1. Write the session log

Write `{sessions_dir}/YYYY-MM-DD-{short-topic}.md` from `_system/templates/session.md`. Fill `agent:` with your tool's name.

**The Quick Reference block is for fast scanning.** Resume reads only that block, which keeps the reload cheap. Write it so it stands alone.

The session log is a record, **not a task list**. Tasks go to the task list.

## 2. Propose the updates, then show them

Before writing anything other than the session log, show the owner every proposed change:

1. **New tasks** for the task list, each with source and date. Read the whole list first and merge duplicates.
2. **For each subject touched:** a dated block for the top of its `Current State.md` (`**{Subject} notes (YYYY-MM-DD, topic):**` then the detail, newest first), and a refreshed one-line row in the `AGENTS.md` table. Subject detail never goes in `AGENTS.md`.
3. **Accomplishments:** ask whether anything from this session belongs in the accomplishments log. Propose the entry outcome-first, with a date and a number. Asking every time is the only reliable way that file stays current.
4. **External systems:** flag anything that needs to reach a CRM or other system of record (packs define which), and which cadence rule applies.
5. **Low-confidence claims:** list anything you wrote this session that should be verified before it is relied on.

Run the recent-activity check (`45-multiple-agents.md`) before writing to shared files. Then write what the owner approves.

## 3. Publish the read-only copy

If `publish_dir` is set in config, run `python3 _system/scripts/publish-vault.py` after the approved writes and report its one-line result. If you cannot run scripts, remind the owner to run it. Skip this step if nothing in the vault changed.

## 4. Keep AGENTS.md small

`AGENTS.md` loads on every message. When it passes **10 KB** (`wc -c AGENTS.md`):

1. Move completed items, resolved notes, and superseded state to `AGENTS-Archive.md`, newest first, with a line saying what moved and when.
2. Never archive the current-state table or anything still live.

Size, not line count: one long line costs as much as fifty short ones.

## Boundaries

- Session logs follow vault rules. In a work vault, **no personal, family, legal, or medical content.** If a session touched those, note only that it happened and where the record lives.
- Never create a task list inside a session log.
