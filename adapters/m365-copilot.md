# Microsoft 365 Copilot (read-only partner)

Microsoft 365 Copilot can read files in OneDrive and SharePoint, and it can search your Outlook mail, Teams chats, and meetings. As of October 2026 it has no documented way to edit files. That makes it a strong **reader** for an intel vault: prep, questions, decisions, and finding what is new in your mail and meetings. Another assistant with folder access (the **writer**) applies changes to the vault.

```
your vault (local) ──publish, one way──> OneDrive copy ──> Copilot reads, searches M365
      ^                                                         │
      └──── writer applies it after you approve ── capture note ┘ (you paste into _Inbox/)
```

## What we tested (2026-10-27, fictional demo vault)

| Worked | Did not |
|---|---|
| Read `.md` files from OneDrive and cited them | Write to any file (it said so, correctly) |
| Built a correct prep brief, time in the owner's zone first | Follow vault rules for its suggested updates (proposed a fact for a prep file, a task with no owner or date). The capture note format below fixes this |
| Flagged new information the owner gave as "not found in files, email, meetings, or chats" instead of guessing | |
| Searched mail, meetings, and chats alongside the vault | |

## Setup

1. **Pick an empty folder in OneDrive** (or a SharePoint library) that syncs to your computer, for example `OneDrive/intel-vault-published`. It must be outside the vault.
2. **Set it in `_system/config.md`:**

   ```yaml
   publish_dir: ~/Library/CloudStorage/OneDrive-YourCompany/intel-vault-published
   publish_exclude: [_system/local, _Internal]
   ```

   `_Internal` (1:1s, compensation, reviews) is excluded by default. Add anything else that should not leave your machine.
3. **Publish once:** `python3 _system/scripts/publish-vault.py`. After that, `intake` and `wrap` publish automatically.
4. **Create a Copilot Notebook** (one per account works well, or one for everything) and add the published folder, or the account's subfolder, as a reference.
5. **Paste the reader instructions below** as the first message in each notebook chat (or into the notebook's instructions, if your version has them).

## Reader instructions

```
You are a READ-ONLY assistant for my intel vault. The files you can see are a
published copy; _PUBLISHED.md says when it was made. Follow
_system/README-for-AI.md and the rule files, with these changes:

- You cannot edit files. Never say a file was updated.
- Commands I may use: resume, prep, brief, risk, review-prep. Follow the matching
  workflow file. For intake or wrap, explain that a writer must do it and give me
  a capture note instead.
- When I tell you something new, or you find something new in my email, Teams, or
  meetings, answer with ONE capture note per account in the exact format in
  _system/templates/capture.md. Every fact needs a source. Every task needs an
  owner and a due date; ask me if you do not know them.
- If the published copy is more than a day old, say so before answering.
```

## Finding what is new (the M365 sweep)

Copilot can see mail and meetings that never reached the vault. Ask:

```
For {Account}: what has changed in my email, Teams chats, and meetings since
{date of the newest Current State block}? Ignore anything already in the vault.
Output one capture note in the format in _system/templates/capture.md.
```

Paste the note into the vault's `_Inbox/`. The next `intake` or `wrap` by your writer assistant shows you the proposed changes and applies the ones you approve.

## Limits to know

- **Not every file gets read for every answer.** A notebook grounds on up to 300 of the most relevant files. For a large vault, reference the account's folder rather than the whole copy.
- **The copy can be stale** until the next publish. Answers about the last hour may miss things.
- **Capture notes are proposals.** The writer treats them as a source, not as fact.
- **Check your employer's policy** before publishing customer data to cloud storage, and keep excluded what should stay local.
