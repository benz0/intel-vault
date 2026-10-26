# Vault conventions

## Vocabulary

- **Subject:** anything the vault tracks in its own folder. A customer account, a direct report, a project, an area of life. Packs define which kinds exist and what their folders are called (the CSE pack uses `Accounts/`).
- **Source:** raw material exactly as received: a transcript, email, chat thread, PDF converted to text, notes the owner pasted.
- **Synthesized file:** anything written from sources: overviews, current state, meeting records, people files.

## Structure

```
{vault}/
├── AGENTS.md                 current state, one row per subject, under 10 KB
├── AGENTS-Archive.md         retired AGENTS.md content
├── {task_list}               the single task list (path in config)
├── {sessions_dir}/           session logs, one per working session
├── {internal_dir}/           the owner's own work: 1:1s, team meetings, career
│   ├── Accomplishments.md
│   ├── Feedback Received.md
│   └── Sources/
├── {inbox_dir}/              pasted raw items waiting to be filed
├── {drafts_dir}/             drafts of outbound messages
├── {subject folders}/        defined by installed packs
└── _system/                  this spec; do not edit except _system/local/ and config.md
```

Every subject folder, whatever the pack, has:

- `Current State.md`: dated status blocks, newest first
- `Sources/`: raw material, read-only
- `Meetings/` and `Meeting Log.md` once meetings exist
- `_Prep/` once a prep brief exists

Packs add more files. Create folders when there is something to put in them, not empty for symmetry.

## Rules

**`Sources/` is read-only.** Raw transcripts, exported emails, PDFs, and chat threads land there unedited and are never changed. Synthesized files live outside it. Read synthesized files first and reach into `Sources/` only to verify a specific claim.

**Never delete history.** Superseded information is marked historical with a date, not removed. Failures, losses, and escalations are the most valuable things in the vault.

**Preserve chronology.** Every meeting file and every material fact carries a date.

**Intake before a subject exists: build the minimum, do not stage.** Create the subject folder with `Current State.md`, the source in `Sources/`, and the meeting file. Leave unknown fields blank and list them as open questions. Say plainly that the subject is thin.

## Naming

- Sources and meetings: `YYYY-MM-DD Short Description.md`
- People: `Firstname Lastname.md`
- Session logs: `YYYY-MM-DD-short-topic.md`

## Frontmatter

Every synthesized file gets YAML frontmatter with real properties, not inline text, so tools like Obsidian Bases can query them. At minimum: `type`, `last_updated`, and the subject it belongs to. Packs define the full sets.

## Wikilinks

Use `[[Wikilinks]]` so the vault navigates in Obsidian or any markdown tool that supports them. Link people, meetings, and subjects in both directions.

**Never write a bare wikilink to a filename that repeats across subjects.** Every subject has a `Current State.md`. A bare `[[Current State]]` has many candidates and resolves silently to one of them, possibly another subject's. Write the full vault-root path with a display alias:

```markdown
[[Accounts/Acme/Current State|Current State]]
```

Bare links are fine only for genuinely unique names, such as dated meeting files. Check before assuming a name is unique.

**Do not link to a file that does not exist.** A link to a missing file renders as text and looks filed. Write the name as plain text instead.

## Check the disk before creating a file you think is missing

**Your memory of this vault is not authoritative. The filesystem is.** Files move and get edited between turns, by the owner or another agent.

1. **Search for it by name** across the whole subject folder before concluding it is gone.
2. **If it exists elsewhere, use it.** Say where you found it.
3. **If it genuinely does not exist, say so and ask** before regenerating. Rebuilding a deliberately moved file destroys whatever was corrected in the meantime.

## Prep files live in `_Prep/`, never in `Meetings/`

`Meetings/` holds records of what happened. A prep brief is written beforehand and is partly speculative. Write prep to `{Subject}/_Prep/YYYY-MM-DD {Meeting} Prep.md` with `type: prep`, never list it in `Meeting Log.md`, and after the meeting add a line at its top pointing to the real record.

## Times are stated in the owner's timezone first

The owner's zone is `timezone` in config. Sources quote times in other zones. Every time in a brief or task carries the owner's zone first, then the others that matter:

`2:00 PM Eastern (your time) | 1:00 PM Central | 3:00 AM Friday in Tokyo`

**Convert, do not copy.** "7pm CST" in a summer month almost certainly means CDT. Recompute rather than repeating a figure from an older note.

## Time discipline (read before writing any vault file)

**Check today's date against the newest source before you write anything.** A vault that reports a stale snapshot in the present tense is worse than no vault, because it reads as current.

1. **Never write a past-dated event as upcoming.** If a date has passed, it either happened or it did not, and you may not know which. Say so.
2. **Never write "this week", "next week", "upcoming", or "soon"** unless anchored to today's actual date. Use explicit dates.
3. **Synthesized overview files carry a source-recency line** at the top: `> Sources span YYYY-MM-DD to YYYY-MM-DD. Today is YYYY-MM-DD.`
4. **If the newest source is more than 30 days old,** say so prominently and list what needs re-confirming.
5. **Past-dated commitments become open questions,** not milestones.
6. **Forward-looking assessments inherit the staleness** of the sources they were made from.

**Use the date inside a source, not its file timestamp.** Files copied in bulk all carry the day they were copied.

## Source authority for names and spellings

**Transcripts are the weakest source for how a name is spelled.** AI note-takers routinely mangle names. Authority, strongest first:

1. Email addresses and signatures
2. Documents the owner wrote or edited by hand
3. Chat display names (Slack, Teams)
4. Meeting transcripts

If sources disagree, prefer the higher tier and say which you chose. Transcripts remain the best source for *what was said*.

**A bare first name is not an identification.** Subjects often contain several people with one first name, sometimes including the owner.

1. Count how many people with that first name appear in the subject. If more than one, treat every bare mention as ambiguous.
2. Look for a role anchor in the same passage.
3. Look for a full name elsewhere in the same document.
4. If it stays ambiguous, write it ambiguous.

**Be especially careful when the fact is personal** (leave, departure, illness). Attributing it to the wrong person, especially the owner, is worse than leaving it unattributed.

## Any rename, move, or delete requires a reference sweep

1. Search the whole subject folder plus portfolio-level files for the old filename and old display text.
2. Update or remove every link to it.
3. Report how many references you found and fixed. If the answer is zero, say so, because zero is suspicious.

**When you correct a name, correct it everywhere in one pass.**

## Do not decide what you cannot decide

If two sources conflict and neither is clearly authoritative, say so and mark it `[unverified]`. Give your best read with its confidence and flag it for the owner. Flip-flopping across turns is worse than admitting uncertainty.

## Always know which subject you are writing to

**Never infer the subject from context and start writing.**

- If the owner names it, use it.
- If not, and more than one could be meant, **ask before writing anything**.
- If the whole task has been about one subject, you may assume continuity, but say so in your first line: "Continuing with Acme."
- When the owner switches subjects mid-task, say so out loud.

## Spreadsheets: `_derived/` is a cache, never a source

The spreadsheet is always authoritative. To read one, convert it into the subject's `_derived/` folder:

```
python3 _system/scripts/sheet-to-md.py --newest <folder> {Subject}/_derived/{Name}.md
```

1. **Never hand-edit `_derived/`.** If it is wrong, fix the spreadsheet and regenerate.
2. **Regenerate before relying on it** if the "Generated" timestamp predates the spreadsheet or is more than a few days old.
3. **Cite the spreadsheet,** never the `_derived/` file.

## The internal folder is not a subject

1:1s, team meetings, training, and career material live in the folder named in `internal_dir`. Never file an internal meeting under a subject folder, even when it is mostly about one subject. Link instead.

## The task list is authoritative

The file named in `task_list` is the single source of truth for the owner's tasks.

- **Never create a competing task file.** Not per subject, not per session, not "just for this." A subject's own `Action Tracker.md`, where a pack defines one, holds actions for that subject including other people's; the owner's own commitments go in the task list.
- **Only owner-owned items** in the main sections. Other people's commitments go under **Waiting on others** with a since-date.
- **Every item carries a source and a date.** No source, no entry. If the owner mentions a task in conversation, the source is the conversation and its date.
- **Read the whole list before adding.** If an existing item describes the same work in other words, update it instead of adding a second one. Duplicates make the list untrustworthy.
- Tag `[unverified]` when carrying an item forward without fresh confirmation.
- When the owner says something is done, move it to **Recently closed** with the date. Do not delete it.

## Hygiene checks after every write session

Before reporting work complete, check every file you wrote or edited:

1. **Forbidden characters** named in the owner's local rules (for example a ban on em dashes). Never replace characters inside `[[ ]]`; that silently breaks the link.
2. **Every wikilink resolves** to a file that exists.
3. **Alias matches target:** in `[[File|Display]]`, the file is the thing the display text names.

`python3 _system/scripts/check-vault.py <files or folder>` does all three. **Report the counts you actually verified.** "Clean" without numbers is not a check, and a wrong zero is worse than no number.

## Every synthesized file ends with

```markdown
---
*Last updated: YYYY-MM-DD | Sources: [[file]], [[file]] | Confidence: High/Medium/Low*
```
