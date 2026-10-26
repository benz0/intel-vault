---
name: internal
description: Log a 1:1, team meeting, training, or other internal session, and keep the accomplishments and feedback logs current. Use when the owner says "log my 1:1", "team meeting notes", "internal session", or pastes notes from a meeting that is about their own work rather than a subject.
aliases: [internal-notes]
argument-hint: "<1-1 | team | training | other>"
---

# Internal notes

Internal meetings are about the owner's own work. They go in the folder named in `internal_dir`, never in a subject folder.

```
{internal_dir}/
├── Accomplishments.md       evidence for reviews
├── Feedback Received.md     every instance of praise, with its source
├── 1-1s/                    YYYY-MM-DD {Manager} 1on1.md
├── Team Meetings/           YYYY-MM-DD {Meeting}.md
├── Career/                  goals, development, review cycles
└── Sources/                 raw material, read-only
```

## Logging an internal meeting

1. Save the raw source to `{internal_dir}/Sources/`, unedited.
2. Write `{internal_dir}/{folder}/YYYY-MM-DD {name}.md` from `_system/templates/internal-meeting.md`.
3. Then, in order, and show each proposed change before writing:
   1. **Every commitment the owner made goes to the task list** with source and date. A commitment made in a 1:1 is as real as one made to a customer.
   2. **Anything review-worthy goes to the accomplishments log** (rules below).
   3. **Any praise the owner received goes to the feedback log,** one row per instance, newest first: date, who, their words (quote when the source has them), context, source file. Praise only; coaching stays in the meeting note. Do this for chat and email too, whenever you see it.
   4. **Process or rule changes** (how something is classified, a new cadence, a new template) go to the relevant rule file in `_system/local/rules/`, not just the meeting note, or the vault stops reflecting reality.
   5. **Subjects discussed:** link to their files and add a dated block to their `Current State.md` if something material changed. Do not duplicate subject content in the internal note.

## The accomplishments log

**The highest-value file in the internal folder and the easiest to neglect.** Reconstructing a year at review time produces a thin, vague list.

Add an entry whenever:

- something closes or is won, or a risk is surfaced and correctly routed
- something is delivered: an analysis, a fix, an escalation resolved
- something is built that others use: a process, a tool, a template, training
- a crisis is absorbed or managed
- something goes wrong and the owner handles it well

**Outcome first, with a number and a date.**

- Good: `Cut average onboarding time from 9 days to 4 by rebuilding the intake checklist, 2026-03. Source: Q1 ops report.`
- Bad: `Worked on onboarding.`

**Include the difficult ones.** Escalations and recoveries carry more weight at review than clean wins.

**Attending is not contributing.** Before writing an entry, answer: what changed because the owner was there? If nothing, it is context for the meeting note, not an accomplishment. A short credible file beats a long padded one.

**Never record another person's performance in this file.**

## Data handling

The internal folder may hold compensation, quota, ratings, and manager feedback. Those are fine here. **Health details, accommodations, and anything about another person's performance or job security** are not; note that a conversation happened and move on (`20-data-handling.md`).
