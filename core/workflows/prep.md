---
name: prep
description: Build a pre-meeting brief from the vault. Use when the owner says "prep me for X", "I have a call with X tomorrow", "what do I need to know before this meeting", or names a meeting type such as a review, 1:1, or sync.
aliases: [call-prep]
argument-hint: "<subject> <meeting type>"
---

# Prep

The owner reads this on the way into the meeting. Lead with what matters and keep it scannable.

## Ask first, if not given

- Which subject
- Meeting type
- Who is attending on each side
- What the owner wants out of it
- The time, so you can state it in the owner's timezone

## Before you brief

**Say when the meeting is, relative to today:** "tomorrow, Wednesday Oct 28, 10:00" or "in 3 days". Never call it "today's call" unless it is today. Check today's date first.

Check the newest source date behind every file you are about to use. **If the subject has not been updated in more than 30 days, open the brief with that fact.** The owner needs to know they are walking in with a stale picture before reading anything else.

## Output

Write to `{Subject}/_Prep/YYYY-MM-DD {Meeting} Prep.md` with `type: prep`. Never into `Meetings/`, never listed in `Meeting Log.md`.

```markdown
# Prep: {Subject}, {Meeting}, {Date}, {time in owner's zone first}

## The one thing
{What the owner must not leave without. One sentence.}

## Where things stand
{3-4 bullets. Status, key dates, open risks.}

## Who's in the room
{Per attendee: name, role, what they care about, last interaction, one thing to say to them.}

## Since last time
{What changed. Actions closed, actions still open.}

## Open commitments the owner owes
{Explicit. Missed commitments are the most common source of credibility damage.}

## Landmines
{What could go sideways.}

## Questions to ask
{5-7, ordered by value. At least one that tests a vault assumption.}

## If it goes well / if it goes badly
{Next step in each case.}
```

Packs may add sections for their meeting types (the CSE pack adds QBR sections).

## Discipline

- **Everything sourced.** Cite the vault file and date. Flag facts older than 60 days.
- **Do not invent** attendee backgrounds, titles, or interests. "Unknown, worth asking" is the right entry.
- **Separate what the owner knows from what they assume.**
- After the meeting, the real record goes in `Meetings/` and a pointer line goes at the top of the prep file.
