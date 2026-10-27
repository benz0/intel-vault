---
name: cs-update
description: Draft a customer-success platform timeline entry, sentiment change, or risk record (CTA) from vault content. Use when the owner says "draft a Gainsight entry", "write this up for timeline", "update sentiment for X", or after a meeting when the vault has changed and the platform has not.
aliases: [gainsight, timeline]
argument-hint: "<account>"
---

# Customer-success platform update

Draft content for the owner to paste into the platform named in `cs_platform`. **Never submit anything. Never claim anything was logged.**

## Timeline entry

Start with the activity fields the platform asks for, filled from the meeting record or source:

```
Meeting title:        {exact title from the invite or source}
Activity date:        YYYY-MM-DD
Time:                 {start time, owner's timezone first}
Duration:             {minutes}
Internal attendees:   {names}
External attendees:   {names}
```

- **Never cite the transcript or source file inside the entry.** The platform readers cannot open it.
- **Never turn contact names into links.**
- If a field is unknown, write "unknown" rather than guessing.

```
[YYYY-MM-DD {owner_initials}] {One-line headline}

KEY GOALS AND OBJECTIVES
...

MAIN DISCUSSION POINTS
...

RISKS AND BLOCKERS
...

FOLLOW-UP ITEMS
- {Owner}: {item} (due {date})

NEXT STEPS
{Our side}: ...
Customer: ...
```

Keep it tight. Timeline entries get skimmed. If the vault file runs long, the entry is the executive cut of it. **No figures the customer should not see** if the platform is customer-visible.

## Sentiment change

Always give:

1. Current and proposed sentiment
2. The specific evidence driving the change, with dates
3. What would have to happen to move it back
4. Whether it changes the update cadence

Do not propose a change from a single data point. Say when you have only one.

## Risk record (CTA)

Include:

- **Root cause type** matched to the actual risk: technical, consumption, or commercial. If it is commercial, say so and route it to sales leadership rather than drafting it as a technical record.
- **Who resolves it,** named
- **Evidence,** with vault file references
- **Recovery plan** if the risk is live, passing the credible-plan test in the `risk` workflow
- **Closure criteria:** what has to be true to close it

## Always end with

1. An ordered checklist of exactly what the owner needs to do in the platform.
2. Which risk signals this touches.
3. A task-list entry for the update, if the owner will not do it right away.
