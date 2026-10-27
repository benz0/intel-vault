# Using an intel vault with any AI tool

The vault is plain markdown, so any assistant that can read files can work it. How much it can do depends on what the tool can touch.

| Tool can... | Then it can... |
|---|---|
| Read and write the vault folder, and run commands | Everything, including the scripts |
| Read and write files, no shell | Everything except the scripts; it checks by hand and says so |
| Read files only (uploads, attachments) | Resume, prep, brief, review-prep. For anything that writes, it gives you file contents to save yourself |
| Chat only | Paste in what it needs; it gives you file contents to save |

## Starter prompt

Paste this at the start of a session (or into the tool's custom instructions or project instructions):

```
You are working in my intel vault, a folder of markdown files that is my system of
record. Before doing anything else, read _system/README-for-AI.md and follow its boot
order: AGENTS.md, _system/config.md, then every rule file in _system/rules/,
_system/packs/*/rules/, and _system/local/rules/ in that order. Local rules win.

When I type a command word (resume, wrap, intake, prep, brief, internal, review-prep,
or a pack command), find the matching workflow file and follow it exactly.

If you cannot write files, give me the full new content of each file and the exact
path to save it to, and never say a file was written. Never fabricate. Never act in an
external system without my yes for that specific action.
```

## Tool notes

- **Claude (desktop app, folder access):** install `adapters/claude/intel-vault` as a skill instead of pasting the prompt. Attach only the vault folder.
- **Tools that only load rules or commands from their own folder:** set `export_rules_dir`, `export_skills_dir`, and `export_commands_dir` in `_system/config.md` to that tool's folders and run `python3 _system/scripts/export-agent-files.py`. Re-run it after every change to `_system/`. Never edit the exported copies; put your own rules in `_system/local/` instead.
- **Microsoft 365 Copilot:** a read-only partner that works from a published copy in OneDrive or SharePoint and hands back capture notes. Tested on the demo vault; see [m365-copilot.md](m365-copilot.md).
- **Saved emails:** drop `.eml` (Mac Outlook, Apple Mail, Gmail) or `.msg` (Windows Outlook) files into `_Inbox/` and run `python3 _system/scripts/email-to-md.py _Inbox`. `.msg` needs `pip install extract-msg`.
- **Meeting transcripts that live only in Teams or another tool:** copy the transcript or recap into `_Inbox/` (or paste it into the conversation) and run `intake`.
