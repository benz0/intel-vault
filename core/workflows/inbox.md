---
name: inbox
description: Sort the owner's email into what needs attention and show a table before anything is written. Use when the owner says "inbox", "triage my email", "evaluate my emails", "what needs my attention", or "what did I miss in email".
aliases: [triage]
argument-hint: "[date range]"
---

# Inbox

Email is where asks, promises, and wins get lost. This workflow reads a stretch of mail, sorts every message into one bucket, shows the result, and stops. It changes nothing until the owner says yes.

To file a backlog of saved emails into the vault, use `intake-batch`; this workflow sorts and proposes, it does not file.

## 1. Pick the date range

The argument is a date range ("this week", "2026-10-20 to 2026-10-27"). With no argument, use **since the last inbox run**:

1. Search the session logs in `sessions_dir`, newest first, for the line `**Inbox run:**` in the Quick Reference block. Its end date is where this run starts.
2. If no session log has that line, **ask the owner for the start date.** Do not guess.

State today's date and the range you will use before reading any mail.

## 2. Choose the source

Use the first one that is available, and **say which you used and what it returned** (how many messages, what date range, what fields). Do not guess at what a source can do.

1. **The tool's email connector,** if it has one. Never assume it can read read/unread or flagged status. If the owner asks for flagged mail, try it, and say plainly whether the connector returned that information.
2. **Saved `.eml` and `.msg` files in `inbox_dir`.** Run `python3 _system/scripts/email-to-md.py {inbox_dir}` first. It skips emails already converted.
3. **Text the owner pastes.**

If a source returns nothing for the range, say so. An empty result is not "nothing needs attention" unless the owner confirms the range was right.

## 3. Skip what the data rules exclude

Before sorting, check each message against `20-data-handling.md`, the `data_policy` line in config, and any pack or local rule that restricts content.

- **Anything excluded is counted only,** in one line at the end: `Skipped 3 under data rules.`
- **Never quote, summarize, paraphrase, or name the sender or subject** of a skipped message, in the table, in a task, in the session log, or anywhere else. Do not say what kind of matter it was beyond the count.
- A message that is partly excluded: use the parts that are not, and count the message as partly skipped. Say how many, with no detail.

## 4. Sort every message into one bucket

Each message goes in **exactly one** bucket, the first that fits in this order:

1. **Asks from my manager or priority senders.** The sender is the `manager` in config, or anyone in `priority_senders`, and the message asks the owner for something or needs an answer.
2. **Needs my reply.** Someone else asked the owner a question or for an action.
3. **Follow-ups owed to me.** The owner asked or was promised something, and someone else still owes it.
4. **Win candidates.** Thanks, praise, a result, or a milestone that may belong in the accomplishments log.
5. **FYI.** Nothing for the owner to do.

Installed packs may add buckets in an `## Inbox buckets` section of their rules. Each pack says where its buckets sit in the order. If a pack gives no position, put them after bucket 3 and before Win candidates.

A message that fits more than one bucket appears **once,** in the first bucket that fits. Any task or commitment in it still follows step 6, whichever bucket it sits in. A message that is only part of a long thread is sorted by the newest message that is not from the owner.

## 5. Show the table, then stop

```
INBOX, 2026-10-20 to 2026-10-27 (source: saved files, 12 messages, 11 shown, 1 skipped)

| Bucket | From | Date | Subject | What is being asked or reported |
|---|---|---|---|---|

Counts: asks from manager/priority 2, needs reply 3, follow-ups owed 1, win candidates 2, FYI 3
Skipped 1 under data rules.
```

- **The counts must add up** to the messages shown, and shown plus skipped must equal what the source returned. Report any difference.
- One line per message in "What is being asked or reported", taken from the message. No invented dates, names, or numbers. If a due date is not stated, say so.
- Then stop and wait.

## 6. On the owner's yes

The owner may approve all of it or pick items. Do only what they approved.

1. **The owner's tasks** go to the task list (`task_list`), each with the email as its source: `Source: email from {sender}, {date}, "{subject}"`. Read the list first and merge duplicates.
2. **Other people's commitments** go under **Waiting on others** in the task list, with who, what, since when, and the same email source.
3. **Win candidates** are **proposed** for the accomplishments log, outcome-first with a date. Do not write them until the owner approves each one. For a large batch of old wins, use `wins-backfill`.
4. **Save the sources.** An email that produced a task, a commitment, or an accepted win goes to the subject's `Sources/` through `intake` if the owner wants it filed. Otherwise leave it where it is.
5. **Record the run** in the session log at `wrap`: add the line `**Inbox run:** YYYY-MM-DD to YYYY-MM-DD` to the Quick Reference block, with the range you covered.

## Never, without a yes for that specific action

- **Send** a reply or forward anything.
- **Draft** a reply in the mail client.
- **Move, flag, label, mark read, or delete** any message.

A yes to the table is not a yes to any of these. If the owner wants a reply drafted, ask which message, write the text in the conversation or in `drafts_dir`, and show it. Nothing goes into the mail client unless the owner says so for that draft.

## Discipline

- **Every statement traces to a message.** If you are unsure who owes what, say so and put the message under FYI with the question, not under a guess.
- **Older mail is history.** A request from before the range, found while reading, is an open question, not a live task, until a newer message confirms it.
- **Say what you could not see:** attachments (listed, never read), messages the connector would not return, threads cut off at the range start.
