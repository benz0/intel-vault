---
name: intake-batch
description: Work through a backlog of saved sources (weeks of transcripts, a folder of saved emails) in checked batches instead of one giant pass, filing each into the vault. Use when the owner says "catch up on these transcripts", "batch intake", "file this backlog", or drops many files at once.
aliases: [batch-intake, process-inbox]
argument-hint: "[folder]"
---

# Batch intake

One unchecked pass over weeks of material is the most common way an AI-maintained vault goes wrong: it burns through usage limits, files notes under the wrong subject, and nobody checks the result. This workflow does the same job in batches you can stop, check, and resume.

## 1. Inventory and plan (no writes yet)

1. List every unprocessed file in the folder (default `inbox_dir`). Convert saved emails first with `python3 _system/scripts/email-to-md.py {folder}`.
2. For each file: the date **inside** it, the likely subject, its type, and a rough size.
3. **Group by subject, oldest first.** Flag anything whose subject is unclear; those wait for the owner.
4. **Size the batches by length, not by file count:** about 20,000 tokens per batch (roughly 15,000 words).
5. Show the plan and stop:

   ```
   Files: 37 (31 transcripts, 6 emails), 2026-09-02 to 2026-10-24
   Subjects: Acme (14), Globex (9), Initech (8), unclear (6, need you)
   Batches: 9. Batch 1 = Acme 2026-09-02 to 2026-09-19 (5 files)
   ```

6. Write the plan to `{inbox_dir}/_batch-progress.md`. It is the checkpoint: which files are done, which batch is next.

## 2. Each batch

1. Run the normal `intake` steps for every file in the batch, **one subject per batch**.
2. Show one combined CHANGES DETECTED for the batch and wait for approval before writing to existing files.
3. On approval, write, then move the processed sources into the subject's `Sources/`.
4. **Spot-check:** pick 2 facts per file you just wrote, re-read them against the source, and report what matched and what did not. Fix mismatches before going on.
5. Run the hygiene checks on the files you wrote and report the counts.
6. Update `_batch-progress.md`, then stop and say what the next batch is. Continue only when the owner says so (or has said "run them all", in which case still stop at any mismatch or unclear subject).

## 3. Finish

- Publish once at the end, if `publish_dir` is set.
- Report: files processed, batches, facts spot-checked and how many failed, files still waiting on the owner.
- Delete `_batch-progress.md` only when nothing is left.

## Rules

- **Never load the whole backlog at once.** Read one batch, write it, then start the next from the files, not from memory.
- **Older material is history.** A commitment from three weeks ago is an open question, not a live task, unless a newer source confirms it.
- **When usage limits matter,** say so in the plan, and offer to do the newest batches first so the vault reflects the current state soonest.
