# Capture note template

Read-only assistants use this to hand new information to an assistant that can write the vault. The owner pastes the note into the vault's inbox folder; the next `intake` or `wrap` applies it after the owner approves.

**Rules:** one capture note per subject. Every fact has a source. Owner and due date are required for every task; if unknown, ask the owner before producing the note. Never propose writing new facts into a prep file.

```markdown
---
type: capture
subject: {Subject}
date: YYYY-MM-DD
captured_by: {tool}, read-only
---

# Capture: {Subject}, YYYY-MM-DD, {short topic}

## New facts
- {fact, in the owner's or source's own words}. Source: {owner in {tool} chat, YYYY-MM-DD | email from {name}, YYYY-MM-DD | Teams meeting "{title}", YYYY-MM-DD}

## Tasks for the owner
- {what}. Due: YYYY-MM-DD. Source: {as above}

## Waiting on others
- {who} to {what}. Since: YYYY-MM-DD. Source: {as above}

## Proposed changes
- `{Subject}/Current State.md`: new dated block with the facts above
- Meeting record for {meeting, date}: {what to add}
- Task list: the tasks above

## Not found / unsure
- {anything the owner mentioned that no source supports, kept word for word}
```
