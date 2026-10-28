# People management

## HARD BOUNDARY: what never goes in the vault

**Never write any of the following anywhere in this vault, from any source:**

- **HR matters** (discipline, performance-improvement or warning conversations, complaints, investigations, pay or leave grievances, terminations, hiring decisions about a named person, and anything an HR process owns)
- **A team member's personal struggles** (health, family, finances, legal, mental or emotional state, anything private they shared or that was shared about them)
- **Issues between team members** (conflicts, complaints about each other, who said what to whom)

This applies to every file and every workflow: `Team/`, session logs, the task list, accomplishments, feedback, prep briefs, meeting notes, `Sources/`, drafts, and capture notes. It applies whether the source is a transcript, an email, a chat, a pasted note, or something the owner says in conversation.

**This is a HARD BOUNDARY.** A local rule cannot loosen, narrow, or remove it, and neither can a request in conversation. If a local rule conflicts with it, follow this and tell the owner which local rule you did not apply. A local rule may add restrictions beyond this.

### What to do when a source contains them

1. **Skip those parts.** Do not copy, quote, paraphrase, summarize, or hint at them. Do not name the person they concern in a way that reveals why. Do not save the raw source to `Sources/` if the whole thing is one of these matters.
2. **Use the rest.** If a message or transcript also holds ordinary work content (a task, a decision, a retrain item), process that part normally.
3. **Tell the owner how many were skipped, with no detail:** `Skipped 2 under the people-management boundary.` Nothing about who, what, or when.
4. **Do not record that it was skipped in a place that identifies it.** The count goes in your reply and, if the owner wants it, in the session log as a bare number.
5. **If a skipped part contains a commitment the owner made** (for example "call HR by Friday"), do not create a task from it. Tell the owner that a skipped part may hold something they owe, so they can track it where the official record lives.

The test: if the owner's team member read the vault, would anything in it be something they would not want written down about them, or about a colleague? If yes, it does not go in.

## Layout

```
{vault}/
└── Team/
    └── {Name}/
        ├── Current State.md       dated work-status blocks, newest first
        ├── 1-1s/                  YYYY-MM-DD {Name} 1on1.md
        ├── Retrain List.md        items this person must be retrained on
        └── Sources/               raw material, read-only (only when there is something to keep)
```

Templates are in `_system/packs/people-manager/templates/team-files.md`. Create a person's folder when there is something to put in it. `{Name}` is `Firstname Lastname`.

**What belongs in a person's files:** work only. Role, what they own, the work they are doing, requests they made, items they need training on, commitments either side made, and recognition they earned. Write every note as though that person may one day read it (`20-data-handling.md`).

**Their performance** is the one place to be careful. Record observable work facts with a date and a source (what was done, what was delivered). Do not record evaluations, ratings, comparisons between people, or opinions. A formal review or improvement process is an HR matter and is covered by the boundary above.

**Never record a team member's performance in the accomplishments log** (`accomplishments`); that file is the owner's own evidence.

## The 1:1 note

One file per 1:1 in `Team/{Name}/1-1s/`, from the template. Its sections: what was discussed, what was decided, what the owner committed to, what the person committed to, items added to the retrain list.

- The owner's commitments go to the task list with the 1:1 as the source.
- The person's commitments go under **Waiting on others** with the same source.
- Anything that falls under the hard boundary above is left out of the note. Count it and move on.

## Team-meeting intake and the retrain list

When the owner brings a team meeting (a transcript, notes, or an email), run the normal `internal` workflow, which files the meeting under `{internal_dir}/Team Meetings/`. Then, in addition:

1. **Find every retrain item:** something the meeting says a person or the whole team must be shown again, corrected, or trained on. Include the meeting date and the source.
2. **Route each item to the person's list.** Append to `Team/{Name}/Retrain List.md` for each person it names. If it applies to the whole team, add it to every person's list who is on the team, and say so in the summary. If you cannot tell who it concerns, **ask; do not guess.**
3. **Show the routing before writing,** in the summary the `internal` workflow already requires:

   ```
   RETRAIN ITEMS
   {Person}: {item}   (source: {meeting file}, {date})
   Whole team: {item}  -> {N} lists
   Unclear who: {item}
   ```

4. **State the item neutrally.** Describe the process or skill to be retrained, not the person's failing. `Refresh the steps for logging a customer call` is fine. `{Name} keeps skipping the logging step` is an evaluation: leave it out.
5. **Anything under the hard boundary** that came up in the meeting is skipped and counted. Never route it to a list.
6. Never create a second task list. Items the owner must act on (for example "schedule the training") go to the task list; the retrain item itself stays on the person's list.

Retrain items are closed, never deleted: mark the item done with the date and how it was closed.

## Inbox buckets

These extra buckets are added to the `inbox` workflow. Position matters; the workflow puts each email in the first bucket that fits.

- **Escalation requests from team** (after the manager and priority senders, before Needs my reply). A person on the team asks the owner to take something up the chain or to decide something they cannot. Name the item and, if `escalation_chain` is set in config, who it would go to. Never decide or forward it without a yes. If the request is itself an HR matter, a personal matter, or a complaint about a colleague, it is skipped and counted under the boundary above, not shown here.
- **Retrain items** (after Follow-ups owed to me, before Win candidates). An email that says a person or the team needs to be shown or corrected on how to do something. On the owner's yes, route each to the right `Retrain List.md` as above, stated neutrally.

Email from a team member about work is ordinary mail and follows the normal buckets. Anything that falls under the hard boundary is skipped and counted: `Skipped 3 under the people-management boundary.` Never name the sender or subject.
