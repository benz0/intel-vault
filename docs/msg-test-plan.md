# Test plan: Windows `.msg` emails with `email-to-md.py`

Plan for the roadmap feedback item "Test `email-to-md.py` on a real Windows `.msg`". Running it closes the item; writing it does not. Mac Outlook `.eml` files were tested on 2026-10-27 (two threads, headers, signature, quoted history). No real `.msg` has been run yet, and the self-test only covers a synthetic `.eml`.

**Who runs it:** someone with Windows and classic Outlook (or any client that saves real `.msg` files). Estimated time: 45 minutes.

**What this plan can and cannot show:** it tests the `.msg` code path (`from_msg` in `core/scripts/email-to-md.py`) against the real `extract-msg` package. Anything marked "expected" below comes from reading the script, not from a run. Record what actually happens.

## 0. Rules for the test data

- Use **throwaway emails you wrote yourself**, to and from your own addresses or a test mailbox. Do not use customer or employee mail.
- Work in a scratch folder, for example `C:\temp\msg-test\`, not in a real vault.
- Never commit test emails or their converted output to this repo. Paste results into the table in section 6 with names and addresses replaced by placeholders.

## 1. Setup

Record each value in the results table.

| Item | How to check |
|---|---|
| Windows version | `winver` |
| Outlook | File, Office Account. Note "classic" or "new". The new Outlook may save `.eml` instead of `.msg` on drag-out; if so, record that and use classic or "Save As, Outlook Message Format". |
| Python | `py --version` and `python --version`. The docs say `python3`; on Windows that name is often missing or a Store stub. Record which command works. |
| Install | `py -m pip install extract-msg`, then `py -m pip show extract-msg` for the version |
| Script | copy `core/scripts/email-to-md.py` to the scratch folder |

Run every step below as `py email-to-md.py <file or folder>` (or whichever command worked).

## 2. Preflight checks

| # | Step | Expected | Pass if |
|---|---|---|---|
| P1 | Run the script on a `.msg` **before** installing `extract-msg` (use a fresh venv or `pip uninstall extract-msg`) | Exits with "Reading .msg files needs the extract-msg package: pip install extract-msg" | Message is clear, no traceback |
| P2 | Install `extract-msg`, rerun on any `.msg` | Converts | A `.md` appears next to the `.msg` |
| P3 | Run with no arguments | Prints the usage text, exit code 1 | |

## 3. Test emails

Create each in Outlook, send to yourself, then save or drag the received copy to the scratch folder as `.msg`. Name them `T01.msg` and so on.

| ID | Email | What it tests |
|---|---|---|
| T01 | Plain text, one recipient, short body, subject `Renewal timing` | Baseline: headers, date, body |
| T02 | HTML body with a bold line, a bulleted list, a table, and a link | `m.body` for HTML mail, formatting loss |
| T03 | Rich Text Format message (Outlook, Format Text, Rich Text), body only | Body recovery when there is no plain or HTML part |
| T04 | Subject `[EXTERNAL] RE: FW: Contract update`, with To and Cc each holding three people, one with a display name containing a comma, for example `Lee, Jordan` | Filename tag stripping, To/Cc list formatting |
| T05 | Sent between two internal Exchange users (not an outside address) | Sender shows a display name or an `/O=EXCHANGELABS/...` address instead of an email |
| T06 | Long reply thread: a reply to a reply to a reply, with a signature that includes an image logo | Quoted history kept, signature text kept, inline image does not break the run |
| T07 | Two attachments: a 5 KB `.txt` and a 2 MB `.pdf`, plus one inline image | Attachment names and byte sizes, nothing extracted |
| T08 | An email attached to an email (Outlook, Insert, Attach Item) | Embedded `.msg` attachment size handling |
| T09 | Non-English text: accented letters, Japanese, an emoji, and a curly quote in subject and body | Unicode in file name, front matter, and body |
| T10 | Subject with characters Windows forbids: `Q4: plan / budget? "draft" <v2>` | Safe file name |
| T11 | Subject over 150 characters | File name truncation, Windows path length |
| T12 | Empty subject and empty body | `(no subject)` and `no subject` fallbacks |
| T13 | An unsent draft saved from Outlook (never sent, no date) | Missing date gives `undated` |
| T14 | A meeting invitation (calendar request) | Body of non-mail items |
| T15 | A digitally signed or encrypted message, if you have a certificate | Unsupported content fails cleanly |
| T16 | Message with a very large body (paste about 5,000 lines) | Speed and memory |
| T17 | An email received from another time zone, or sent late evening Pacific | Date and the `%Z` zone label near midnight |

If a case is not possible on your setup, mark it "skipped" with the reason.

## 4. What to check for each converted file

For every test email open the `.md` and compare it with Outlook side by side. Use this checklist.

1. **Name:** `YYYY-MM-DD Email {sender} {subject}.md`. No `[EXTERNAL]`, `RE`, or `FW` prefix, no characters Windows rejects, readable.
2. **Date line:** matches the Outlook "Sent" time **in your local zone**, with a zone label (not blank, not off by hours).
3. **From:** shows a name and an email address you can recognise. Record if it shows an Exchange path instead (T05).
4. **To and Cc:** every recipient present, in order, separated clearly. A name containing a comma is not split in two.
5. **Subject:** exact, including the `[EXTERNAL]` and `RE:` prefixes (only the file name drops them).
6. **Attachments:** each listed once, with the right name and a plausible size. Inline images: record whether they are listed.
7. **Body:** complete, in order, no text from after the signature missing, no HTML tags left, quoted history intact. Note anything lost (tables, links, bold).
8. **Characters:** no stray control characters; accents, CJK, and emoji intact in the body.
9. **Original kept:** the `.msg` is still in place and unchanged (compare size and modified time).
10. **Rerun:** add a short line to one converted `.md` and rename it, then run the script on the folder again. It should print that it skipped the `.msg` as already converted (it finds the copy by the `# Original file:` line) and leave your edited file alone. Then run with `--force` and confirm it converts again.
11. **Console:** no `UnicodeEncodeError` when printing the file name in a Windows console (cp1252). T09 is the likely trigger. Try also with `set PYTHONUTF8=1`.
12. **Intake:** drop one converted email and its `.msg` into a throwaway vault's `_Inbox/` and say `intake`. The assistant should treat the `.md` as the source and move both files into `Sources/`.

## 5. Specific risks to watch (from reading the script)

These are guesses to confirm or rule out, not known bugs.

- **`extract-msg` version differences.** Newer versions can return the date as a string and attachment `data` as an object for embedded messages. The script handles a string date and non-bytes data (size 0), but verify T08 shows a sensible size and no crash.
- **`m.sender` for internal mail** may be a display name only or an Exchange address (T05).
- **`m.to` and `m.cc`** come back as one string, not a list. A display name with a comma (T04) may format poorly.
- **Date zone.** If `m.date` has no zone, `astimezone()` assumes the machine's zone. Compare with Outlook (T17).
- **Body empty for RTF-only mail** (T03).
- **Output encoding** on the console (check 11) and the file (written as UTF-8).
- **Path length.** Windows limits full paths to 260 characters by default. T11 inside a deep scratch folder will show it.
- **`python3` not found on Windows.** If so, the README and `adapters/` instructions need a Windows variant (`py`).

## 6. Results

Copy this table into a reply or a file outside the repo. Fill one row per test.

| ID | Converted (Y/N) | Name ok | Date ok | From ok | To/Cc ok | Attachments ok | Body ok | Notes (what differed, exact error text) |
|---|---|---|---|---|---|---|---|---|
| P1 | | | | | | | | |
| T01 | | | | | | | | |
| T02 | | | | | | | | |
| T03 | | | | | | | | |
| T04 | | | | | | | | |
| T05 | | | | | | | | |
| T06 | | | | | | | | |
| T07 | | | | | | | | |
| T08 | | | | | | | | |
| T09 | | | | | | | | |
| T10 | | | | | | | | |
| T11 | | | | | | | | |
| T12 | | | | | | | | |
| T13 | | | | | | | | |
| T14 | | | | | | | | |
| T15 | | | | | | | | |
| T16 | | | | | | | | |
| T17 | | | | | | | | |

Also record: Windows version, Outlook edition, Python command, `extract-msg` version.

## 7. Pass criteria

- **Pass:** T01, T02, T04, T06, T07, T09, T10, and T12 all convert with correct headers, a correct local date, complete body, and attachments listed. Preflight P1 gives the clear message. Check 12 (intake) works.
- **Pass with notes:** T03, T05, T08, T11, T13 to T17 may degrade (for example an Exchange path for the sender, or a skipped encrypted message) as long as the script does not crash and the `.md` states what is missing.
- **Fail:** any traceback, any wrong date by more than the zone shown, any dropped recipient or attachment, or any lost body text in the required set.

## 8. What happens with the results

Each failure or surprise becomes a roadmap item or a fix, with the finding quoted in the changelog line (see `DEVELOPING.md`, "Where work comes from"). If everything passes, update the roadmap line to say Windows `.msg` was tested, with the date, Outlook edition, and `extract-msg` version, and mention the `py` launcher in the README if that was the only working command. If a real `.msg` fixture can be made from synthetic content with no personal data, add a self-test check for it.
