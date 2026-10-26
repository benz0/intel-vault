---
name: brief
description: Weekly roll-up across every subject and the task list. Use when the owner says "brief", "weekly brief", "what's on my plate", "prep for my 1:1", or at the start of a week.
aliases: [weekly-brief]
argument-hint: ""
---

# Weekly brief

Read across every subject plus the task list and produce a prioritized picture. This is what the owner reads before their 1:1 with their manager.

## Steps

1. Read the task list first. It is authoritative for the owner's commitments.
2. Read the newest block of each subject's `Current State.md`, plus any overview file the pack defines.
3. **Find subjects that have gone quiet:** no meeting or update in 30+ days on a subject with a live cadence is itself a signal.
4. Apply the pack's checks (for example the CSE pack checks renewals inside 120 days).

## Output

```markdown
# Weekly Brief ({Date})

## Needs a decision this week
{3-5 items max. If everything is urgent, nothing is.}

## Overdue
{The owner's own commitments first, then everything else. How long overdue, and who is waiting.}

## Moving the wrong way
{Per subject: what changed, why it matters, what to do.}

## Gone quiet
{Subjects with no logged activity in 30+ days.}

{Pack sections}

## For the 1:1 with {manager from config}
{3-5 things worth their time, including anything the owner needs a decision or support on.}

## Open task table
| Priority | Task | Due |
|---|---|---|
```

Priority markers: 🔴 urgent/today, 🟡 monitor/soon, 🟢 ready to act, 🗓 watch/upcoming, ✅ done, 📋 admin.

## Discipline

- **Do not pad the urgent list.**
- **Every item names an owner and a date,** or it goes in a "needs scoping" bucket.
- **Say when the vault is stale.** If half the subjects have not been updated in a month, the brief is unreliable and the owner should know up front.
