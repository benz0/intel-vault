# Instructions for any AI assistant working in this vault

This folder (`_system/`) is the operating spec for an intel vault: a folder of plain markdown files that is the owner's system of record for the people, accounts, and work they track. The spec is written for **any** AI assistant (Claude, Copilot, ChatGPT, or whatever comes next). It does not depend on any one tool's memory, so the work survives a change of tool.

**If you are an AI and you are reading this, follow it.** The owner should never have to restate these rules.

---

## Boot order (every session)

**If the folder you are reading has a `_PUBLISHED.md` at the top, you are reading a one-way copy.** You are a reader: follow the reader rules in `_system/rules/45-multiple-agents.md`, never claim to edit files, and hand new information back as a capture note (`_system/templates/capture.md`).

1. **`AGENTS.md`** at the vault root. Current state: what is in flight, one row per subject. Small on purpose.
2. **`_system/config.md`**. Who the owner is, their timezone, which packs are installed, and where the key files live. Every rule below refers to paths by their config name (for example **the task list** means the file named in `task_list`).
3. **Every rule file, in this order.** Later files win where they conflict, with one exception (below):
   1. `_system/rules/*.md` (core)
   2. `_system/packs/{pack}/rules/*.md` (one folder per installed pack)
   3. `_system/local/rules/*.md` (the owner's own overrides; they win over the two layers above, except for hard boundaries)

   **Hard boundaries.** A rule marked `HARD BOUNDARY` in core or in a pack cannot be loosened, narrowed, or removed by a local rule. If a local rule conflicts with one, follow the boundary and tell the owner which local rule you did not apply. A local rule may add restrictions beyond a boundary. This holds when your tool loads rules from its own folder in a different order.
4. **Read nothing else yet.** Load workflows and subject files only when the task needs them.

Some tools load rules from their own folder instead. If `export_rules_dir` is set in config, that folder holds generated copies of these same files (made by `_system/scripts/export-agent-files.py`). Never edit the copies.

---

## Commands

The owner may type a command word, with or without a leading slash. Treat a leading word that matches a workflow's `name` or one of its `aliases` as that workflow; the rest of the message is its arguments (`$1`, `$2`, ...).

**Where to find a workflow,** most specific first:

1. `_system/local/workflows/{name}.md`
2. `_system/packs/{pack}/workflows/{name}.md`
3. `_system/workflows/{name}.md`

Core commands:

| Command | Does |
|---|---|
| `resume [n \| subject \| full]` | Reload recent context cheaply |
| `wrap` | Save the session, update the task list and subject state |
| `intake <subject>` | Process one transcript, email, chat thread, or note into the vault |
| `intake-batch [folder]` | Work through a backlog in checked, resumable batches |
| `prep <subject> <meeting type>` | Pre-meeting brief |
| `brief` | Weekly roll-up across everything tracked |
| `internal <type>` | Log a 1:1, team meeting, or other internal session |
| `inbox [date range]` (alias `triage`) | Sort email into what needs attention, show a table, and stop for the owner's yes |
| `wins-backfill [source]` | Turn a folder of past wins into accomplishments-log entries, in checked batches |
| `review-prep [period]` | Assemble evidence for a review from the accomplishments log |

Packs add more (for example the CSE pack adds `risk`, `cs-update`, `build-vault`). List them by reading the workflow folders. If the owner uses a command that has no workflow file, say so and list the ones that exist.

**Templates layer the same way.** When a workflow names a template such as `_system/templates/session.md`, use `_system/local/templates/session.md` if it exists, then `_system/packs/{pack}/templates/`, then the core one.

**No command is required.** Plain language works. Commands exist to load a specific checklist.

---

## Tool translation

The spec says "run", "search", "check the modification time". Use whatever your tool offers:

- **Shell access** (a linked computer, a terminal tool, a coding agent): run the command or script.
- **File access but no shell:** do the check by reading files, and say that you checked by hand.
- **Chat only, no file access** (a plain chat window): you cannot write the vault. Produce each file's full new content, tell the owner the exact path to save it to, and never claim a file was written.

Scripts in `_system/scripts/` are plain Python 3 with no dependencies unless noted.

---

## The rules that matter most

These are in the rule files in detail. They are repeated here because breaking them does the most damage.

1. **Never fabricate.** No invented names, dates, ticket numbers, links, quotes, or citations. "I don't know" is a correct answer.
2. **Draft, show, wait.** Never send, submit, log, or change anything in an external system (email, CRM, chat, ticketing) without the owner's explicit yes for that specific action.
3. **One task list.** The file named in `task_list` is the only place the owner's tasks live. Every task has a source and a date.
4. **`Sources/` is read-only.** Raw material is saved unedited and never changed.
5. **Check today's date before writing.** Never write a past-dated event as upcoming.
6. **The disk is authoritative,** not your memory of it. Re-read a file right before editing it.
7. **Know which subject you are writing to.** If more than one could be meant, ask.
