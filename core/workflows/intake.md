---
name: intake
description: Ingest a meeting transcript, notes, email thread, or chat thread and propagate everything it changes across the vault. Use when the owner pastes or points at source material, says "process this meeting", "here are my notes from X", or "update the vault with this".
aliases: [meeting-intake]
argument-hint: "<subject>"
---

# Intake

Take one piece of raw source material and update every file it touches. This is the workhorse; it runs after most meetings.

**Internal meetings** (1:1s, team meetings) use the `internal` workflow instead.

## Where source material comes from

- **Pasted** into the conversation.
- **A file** the owner dropped in `inbox_dir` or the subject's `Sources/`. For anything long, dropping the file first is cheaper than pasting it.
- **A connector** your tool has (a meeting recorder, email, chat). Pull the raw content, not just an AI summary, when the connector offers both.
- **A saved email** (`.eml` from Mac Outlook, Apple Mail, or Gmail; `.msg` from Windows Outlook) dropped in `inbox_dir`. Convert it to a **temporary folder outside the vault**, not into `inbox_dir`: `python3 _system/scripts/email-to-md.py {inbox_dir} --out {temp_dir}`. The markdown copy has sender, recipients, date, and an attachment list; the original is kept. Scan the copy (step 2). Then save the copy into `Sources/` and **move the original `.eml` or `.msg` there too,** side by side with the same base name, so nothing is left in `inbox_dir`, and delete the temporary folder. Attachments are listed, never read.
- **A capture note** from a read-only assistant (`_system/templates/capture.md`), usually pasted into `inbox_dir`. See "Capture notes" below.

## Steps

**1. Confirm the subject.** If the owner did not name it and more than one could be meant, ask.

**2. Scan for excluded content before saving anything** (`20-data-handling.md`, the `data_policy` line in config, and any `HARD BOUNDARY` in an installed pack or local rule). Excluded content must not reach `Sources/` or any other vault file. If you find some:

- Tell the owner how many parts and what kind (a credential, an HR matter), without repeating them. Where a rule says to count only, give the count and nothing else.
- **Part of the source is excluded:** remove those parts, and put one marker line directly under the header: `[2 parts removed under data rules]`, with the real count and no detail about what was removed. Save the rest in step 3.
- **The whole source is excluded:** save nothing, and write nothing from it. Say so, with the count.
- **A saved email with anything removed:** the original `.eml` or `.msg` still holds the excluded content and cannot be edited, so it never goes into `Sources/`. Save only the cleaned copy, and add this line to its header, directly under `# Original file:`: `# Original withheld: contained excluded content, delete it`. Leave the original in `inbox_dir`. `check-vault.py` then reports it as a **withheld original** ("delete this original, never move it into Sources"), separately from an ordinary leftover. Tell the owner to delete it outside the vault. Do not delete it yourself without a yes for that action.
- **A saved email wholly excluded:** save nothing, write nothing from it, leave the original in `inbox_dir`, and do not name it. Count it for the closing line below.
- **At the end of the run,** if any saved email was excluded entirely, say once: `N saved emails in _Inbox/ were excluded; delete them from the vault yourself (they are the ones not listed above).` Never name them, never say what they were about, and never delete them without a yes for that action.

**3. Save the raw source** to `{Subject}/Sources/YYYY-MM-DD {description}.md`, as received except for what step 2 removed, with a short header: date, type (meeting, email, chat), who captured it, which tool it came from. The removal in step 2 is the only edit ever made to a raw source (`40-vault-conventions.md`); never modify it afterward. If it came from `inbox_dir`, move it rather than copying it.

**4. Date it.** State today's date and the source's date. If the source is more than 30 days old, say so and treat it as historical. Do not carry its forward-looking commitments into any plan as live.

**5. Write the meeting file** in the subject's `Meetings/` folder, from `_system/templates/meeting.md` or the pack's template. **Not every source earns a file:** a routine sync where nothing moved gets a dated row in `Meeting Log.md` with a one-line summary and a link to its source. Write a full file when the meeting produced a decision, a commitment, a new or changed risk, or a contradiction of the vault. When in doubt, write the file.

**6. Identify what changed.** Produce this before touching any existing file:

```
CHANGES DETECTED
New people:              ...
People updates:          ...
New/changed risks:       ...
New opportunities:       ...
Decisions:               ...
Owner's new commitments: ...
Others' commitments:     ...
Actions now complete:    ...
Contradicts vault:       ...
{rows the pack adds}
```

**7. Show the summary and stop.** Let the owner confirm before you write to existing files. They often know context that is not in the source.

**8. On approval, propagate** to: `Meeting Log.md`, the subject's `Current State.md`, affected people files, any files the pack lists for this subject type, the task list for anything the owner owns, and **Waiting on others** for anything someone else committed to.

**9. Run the hygiene checks** (`40-vault-conventions.md`) on every file you wrote or edited, and report the counts. For a saved email, the same run reports **Leftover emails**: a `.eml` or `.msg` still in `inbox_dir` whose markdown copy is already in a `Sources/` folder. The count must be 0. If not, you moved only one of the two files; move the other into the same `Sources/` folder. A **withheld original** (step 2) is reported separately and is the opposite case: never move it into `Sources/`, only delete it, and only after the owner says yes.

**10. Publish.** If `publish_dir` is set in config, run `python3 _system/scripts/publish-vault.py` and report its one-line result (or remind the owner, if you cannot run scripts).

**11. Close with the external-system prompt** if a pack defines one (for example the CSE pack asks whether to draft a CRM timeline entry).

## Capture notes

A capture note is a **proposal**, written by an assistant that can read the vault but not change it. Handle it like any other source:

- Save it to `Sources/` unedited, like a transcript.
- Its facts carry the source **the capture note names** (usually "owner, via {tool} chat, {date}"), never "confirmed" by the tool that wrote it.
- Its "proposed changes" are suggestions. Run the normal CHANGES DETECTED step, show the owner, and apply only what they approve. Fix anything that breaks vault rules (for example a fact proposed for a prep file belongs in a meeting record or `Current State.md`).
- Once applied, move the note from `inbox_dir` into the subject's `Sources/`.

## Judgment rules

- **Attribute quotes to named speakers only when the source labels them.** Transcripts often say "Me" and "Them". If you cannot attribute confidently, say so.
- **AI meeting summaries drop nuance.** If a raw transcript and a summary both exist, the transcript is authoritative for anything specific.
- **Contradictions are signal.** If the source contradicts the vault, surface it prominently rather than quietly overwriting.
- **Never drop a commitment because the meeting was routine.** A log-row-only meeting with an owner action still puts that action on the task list.
- **Do not link to a person who has no file.** Write the name as plain text or add them to the subject's people index.
- **Watch for tool identifiers in titles.** A document ID or UUID in a filename means the title came from a tool's internal reference, not the meeting.
