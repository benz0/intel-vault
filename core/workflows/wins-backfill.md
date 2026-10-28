---
name: wins-backfill
description: Read a source of past wins once (a mail folder, exported emails, or notes) and propose accomplishments-log entries from it, in checked batches. Use when the owner says "backfill my wins", "build my wins from my saved emails", or has a folder of praise and results to turn into evidence.
aliases: [backfill-wins]
argument-hint: "[source]"
---

# Wins backfill

Many people keep a folder of thank-you notes and results and never turn it into a log. This workflow reads that source **once** and proposes entries for the accomplishments log (`accomplishments` in config), in batches the owner can stop and resume. It is the same shape as `intake-batch`.

## 1. Inventory and plan (no writes yet)

1. **Choose the source** and say which you used and what it returned (how many items, what date range):
   - a mail folder through the tool's email connector (never assume it can read more than it returned),
   - saved `.eml` and `.msg` files (run `python3 _system/scripts/email-to-md.py {folder}` first; it skips emails already converted),
   - a folder or file of notes.
2. **Read the accomplishments log first.** Note what it already holds, so nothing is proposed twice.
3. **Apply the data rules** (`20-data-handling.md`, `data_policy`, pack and local rules) to every item. Excluded items are **counted only:** `Skipped 2 under data rules.` Never quote, summarize, or name the sender or subject of a skipped item, and never carry its content into an entry.
4. **Size the batches** by length, about 20,000 tokens each, oldest first.
5. Show the plan and stop:

   ```
   Source: saved emails, 64 items, 2025-11-03 to 2026-10-24 (skipped 3 under data rules)
   Already in the log: 9 entries
   Batches: 4. Batch 1 = 2025-11-03 to 2026-01-15 (17 items)
   ```

6. Write the plan to `{inbox_dir}/_wins-progress.md`. It is the checkpoint: which items are done, which batch is next.

## 2. Each batch

1. Read the batch, one item at a time, from the files, not from memory of earlier batches.
2. **Propose entries.** Each one has:
   - **The outcome first,** with a number where the source has one: `Cut average onboarding time from 9 days to 4 by rebuilding the intake checklist, 2026-03.`
   - **A date** (the date of the outcome, from the source, not today's).
   - **The evidence:** the source item (sender, date, subject, or file) and the sentence that supports the entry.
   - **Where it goes** in the log (Results, Delivery, Built for others, Recognition).
3. **Test each candidate:** what changed because the owner was there? Attending, being copied, or being thanked for routine work is not an accomplishment. Say so and leave it out, or move praise to the feedback log (`feedback_log`) as one row with its source.
4. **Skip duplicates:** anything already in the log, or already proposed in an earlier batch. Report how many you skipped.
5. **Show the batch and stop.** The owner approves **each entry** (yes, no, or edit). Write only the approved ones.
6. **Spot-check** 2 approved entries against their sources and report what matched. Fix mismatches before going on.
7. Run the hygiene checks on the log and report the counts.
8. Update `_wins-progress.md`, say what the next batch is, and stop. Continue only when the owner says so.

## 3. Finish

- Report: items read, entries proposed, approved, skipped as duplicates, skipped under data rules, items with no outcome.
- List the gaps: periods or topics with thin evidence.
- Delete `_wins-progress.md` only when nothing is left.

## Rules

- **No source, no entry.** Do not infer a number or a date.
- **Never record another person's performance** in the accomplishments log.
- **Read the source once.** The progress file is how a later session resumes without re-reading finished batches.
- **Older material is history.** State the date of each outcome; do not present an old result as recent.
