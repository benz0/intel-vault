# When more than one AI works this vault

The owner may use several AI tools on the same files (for example Claude in one app and a different assistant in another). They all follow this spec. The tools are listed in `agents` in `_system/config.md`.

- **One agent per subject at a time.** Never run two agents on the same subject in parallel.
- **The disk is authoritative.** Re-read a file immediately before editing it; another agent may have changed it since you last looked.
- **Edit in place.** Never rebuild a file from earlier tool output, which may be truncated or stale.
- **Say which agent wrote what.** Session logs carry `agent: {tool name}` in frontmatter, lowercase (`claude`, `copilot`, `chatgpt`).

## Writers and readers

Not every assistant can change the vault.

- **Writers** can edit files in the vault itself (for example a desktop assistant with folder access, or an editor-based agent). They run `intake`, `wrap`, and anything else that changes files.
- **Readers** see only a published copy (`publish_dir`, made by `_system/scripts/publish-vault.py`) or attached files. They are good for `resume`, `prep`, `brief`, answering questions, and searching the owner's mail, calendar, and chat for what is new.

**Rules for readers:**

1. **Never say a file was updated.** You cannot update it.
2. **Say how fresh your copy is** when it matters. The time is in `_PUBLISHED.md` at the top of the copy.
3. **When the owner tells you something new, answer with a capture note** in the format in `_system/templates/capture.md`, so a writer can apply it later. Do not scatter the update across loose suggestions.
4. **Name your source for every new fact** (the owner in this chat, or a specific email, meeting, or chat you found), and leave out anything you cannot source.

## Recent-activity check

Before your first write to a subject in a task, and again before each later write if more than a few minutes have passed:

1. Check the modification time of the subject's `Current State.md` and of the task list.
2. Check today's session logs that name this subject, and their `agent:` value.

```bash
find "{Subject folder}/Current State.md" "{task_list}" -mmin -60
grep -l "{Subject}" {sessions_dir}/$(date +%F)-*.md 2>/dev/null | xargs -r grep -H "^agent:"
```

If a file changed in the last 60 minutes and you did not change it in this task, or another agent's log covers this subject in that window: **stop before writing.** Tell the owner what changed and when, re-read the changed files, and ask whether the other agent is still working. Then merge into what is there. **Never write a second block for the same date and topic.**

## Verify other agents' claims

An agent's file edits are usually reliable; its counts, citations, and "verified clean" reports often are not. Before relaying another agent's report, check the files it claims to have changed.
