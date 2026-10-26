---
name: build-vault
description: Build or rebuild the full account folder from a set of raw sources, in phases. Use when the owner says "build the vault for X", "set up account X", or points at a folder of transcripts, notes, and emails for an account with no vault yet.
aliases: [account-vault-build]
argument-hint: "<account>"
---

# Build an account

Build a complete account folder from everything in `Accounts/{Account}/Sources/`.

## Phase 0: date the sources (always first)

**Use the date inside each file, not its modification time.** Files copied in bulk all carry the day they were copied. State the time frame out loud:

```
Today: YYYY-MM-DD
Oldest source: YYYY-MM-DD
Newest source: YYYY-MM-DD
Staleness: N weeks since the newest source
```

**If the newest source is more than 30 days old,** warn the owner that this build will be a historical snapshot and ask whether newer material exists before spending effort on old ground.

List every dated commitment in the sources that falls before today. Those are unknowns for the open-questions list, not milestones.

## Before you build

1. List what is in `Sources/` and flag anything that looks like excluded content (`20-data-handling.md`).
2. **Propose the structure and stop for approval:** which product relationships get folders, the stakeholder list (customer vs internal), the product and competitor inventory.

## Phases

Run **one phase per conversation** for large accounts. Announce the phase and stop at its end.

| Phase | Produces |
|---|---|
| 1 | `Account Overview.md` and `Current State.md` |
| 2 | `Stakeholders/` files and `Stakeholder Index.md` |
| 3 | Product folder notes and product/competitor files |
| 4 | `Customer Intelligence Dashboard.md` |
| 5 | `MEDDPICC.md` per product relationship |
| 6 | `Account Plan.md` and `Success Plan.md` per product |
| 7 | `Architecture.md` per product |
| 8 | `Risks and Opportunities.md` per product |
| 9 | `Action Tracker.md` |
| 10 | `Meeting Log.md` and a file per meeting that changed something |
| 11 | Verification (mandatory) |

Templates: `_system/packs/cse/templates/account-files.md`.

## Large source sets

Measure before you read. If the sources are more than about a third of your context window, read them in **chronological batches sized by tokens, not file count** (about 20,000 tokens each). State the plan ("12 batches, batch 1 covers 2026-02-10 to 2026-03-05"), append findings after each batch, note which files are consumed, and never re-read a consumed file. Consolidate over the output file, not the sources.

## Content requirements

- **Use all the sources, not just the newest.** Failed upgrades, churn stories, and competitive losses are often the most valuable material.
- **Label every material claim** Confirmed / Assumption / Historical / Unknown.
- **Preserve conflicts.** Keep both, date them, say which you weighted.
- **Separate product motions.**
- **Document the full churn or migration story** if the account is leaving.
- **A source with no attendees line is usually not a meeting.** Trackers, analyses, and prep documents are working material; list them in the verification file as sources used.

## Run the hygiene checks at the end of every phase

Not just in Phase 11. A mass fix at the end is the dangerous kind (replacing a character inside a link target breaks the link), and violations piling up within a phase are a sign the output is drifting on substance too. Re-read that phase's output for sourcing and confidence labels if the count is more than a handful.

## Phase 11: verification

Write `Accounts/{Account}/_Build Verification.md`:

1. Unsourced claims
2. Assumptions a reader might mistake for fact
3. Conflicts left open
4. Coverage gaps (MEDDPICC sections with no evidence, stakeholders with no role, products with no adoption data)
5. Sources not used, and why
6. **Stale-as-current errors:** every past-dated event written as upcoming, and every "this week" or "soon" that is wrong as of today. Mandatory.
7. Questions only the owner can answer

Then two mandatory writes:

**A. Every owner-owned action goes into the task list,** with source and date. Read the whole list first; update existing items instead of duplicating them. Report the split ("7 actions, 4 new, 3 merged"). **A build that leaves actions only in a chat summary is not done.**

**B. Run the hygiene checks over the whole account folder, including `_Build Verification.md`,** and report the counts: forbidden characters, broken wikilinks, alias mismatches, files missing frontmatter. Fix forbidden characters before checking links. After Phase 10, re-check every meeting link written in earlier phases against the files that actually exist.

Do not call the build complete until both writes are done, the counts are reported, and the owner has read the verification file.
