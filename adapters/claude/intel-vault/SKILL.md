---
name: intel-vault
description: Run the owner's intel vault workflow (resume, wrap, intake, prep, brief, internal, review-prep, plus pack commands like risk or gainsight). Use when the owner types one of those words with or without a slash, says "catch me up", "what was I working on", "save this session", or asks to update their vault, accounts, team notes, or task list.
---

# Intel vault (Claude adapter)

This skill holds **no rules of its own.** The vault carries its own spec in `_system/`, and every AI that works the vault follows that one spec. This skill only tells Claude how to find it and how to translate tool language.

## How the owner calls it

The Claude app intercepts unknown `/` commands, so the owner types the command word **without the slash**: `resume`, `wrap up`, `intake Acme`, `prep Acme QBR`. Treat a leading word that matches a workflow name or alias as that workflow; the rest of the message is its arguments.

## Step 1: find the vault

1. Look in the folders connected to this conversation for one containing `_system/config.md`.
   - Desktop app with folder access: use the connected folder directly.
   - Linked computer: use the device shell (`$HOME/mnt/<folder>`).
2. If more than one vault is connected (for example work and personal), route by subject. Never write personal, family, legal, medical, or personal-finance content into a work vault; say so out loud when declining.
3. If no vault is reachable, say so plainly and stop. **Never write vault files somewhere else as a fallback.**

## Step 2: load the spec

Read `_system/README-for-AI.md` and follow its boot order exactly: `AGENTS.md`, `_system/config.md`, then every rule file (core, packs, local). Read them **before any write.**

## Step 3: run the workflow

Find the workflow file (`_system/local/workflows/`, then `_system/packs/*/workflows/`, then `_system/workflows/`) and follow it. Substitute `$1`, `$2` with the owner's arguments.

## Claude-specific notes

- **Session logs** carry `agent: claude`.
- **Run the recent-activity check** in `45-multiple-agents.md`; do not just ask about it.
- **Edit files in place** with short scripts that read the file fresh. Never rebuild a file from earlier tool output.
- **Verify any count you report** (duplicates, broken links, forbidden characters) by running `_system/scripts/check-vault.py` or `grep -c`. A line printed twice by two commands is not two lines.
- **Connectors** (meeting recorders, email, calendar, chat, browser) can supply source material for `intake`. Save the raw content to `Sources/` unedited, as the workflow says.
- **Never act in an external system** through a connector or the browser without the owner's yes for that specific action.
- **Show each proposed change before writing it,** as the workflows require.
