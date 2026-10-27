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
- **A saved email** (`.eml` from Mac Outlook, Apple Mail, or Gmail; `.msg` from Windows Outlook) dropped in `inbox_dir`. Run `python3 _system/scripts/email-to-md.py {inbox_dir}` first: it writes a markdown copy with sender, recipients, date, and an attachment list, and keeps the original. **Move both** into `Sources/`: the markdown copy and the original `.eml` or `.msg`, side by side with the same base name, so nothing is left in `inbox_dir`. Attachments are listed, never read.
- **A capture note** from a read-only assistant (`_system/templates/capture.md`), usually pasted into `inbox_dir`. See "Capture notes" below.

## Steps

**1. Confirm the subject.** If the owner did not name it and more than one could be meant, ask.

**2. Save the raw source** to `{Subject}/Sources/YYYY-MM-DD {description}.md`, unedited, with a short header: date, type (meeting, email, chat), who captured it, which tool it came from. Never modify it afterward. If it came from `inbox_dir`, move it rather than copying it.

**3. Date it.** State today's date and the source's date. If the source is more than 30 days old, say so and treat it as historical. Do not carry its forward-looking commitments into any plan as live.

**4. Scan for excluded content** (`20-data-handling.md`). If found, stop and tell the owner where. Do not propagate it.

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

**9. Run the hygiene checks** (`40-vault-conventions.md`) on every file you wrote or edited, and report the counts. For a saved email, the same run reports **Leftover emails**: a `.eml` or `.msg` still in `inbox_dir` whose markdown copy is already in a `Sources/` folder. The count must be 0. If not, you moved only one of the two files; move the other into the same `Sources/` folder.

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
