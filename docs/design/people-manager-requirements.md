# People-manager pack: requirements

> From an interview with the first user, 2026-10-26 and 2026-10-27. Names, employer, and figures that would identify the user are removed. This file holds requirements only, never vault content.

## The user

- Supervisor in accounts receivable (credit and collections) with about 9 direct reports, all collectors. Supports the collectors; does not collect.
- Assists on about **40 customer accounts** at any time.
- Meets each collector one-on-one **twice a month**; some reach out almost daily.
- Uses an AR platform (BlackLine) and a BI tool (Power BI). Meeting notes live in SharePoint.
- Company Claude plan, desktop app with folder access. **Microsoft 365 connector is connected** (individual authorization). Slack, Atlassian Rovo, Lucid, and Sigma connectors are available but not connected.
- The vault lives on the work laptop's local disk.

## Ranked needs

1. **"Evaluate my emails."** The one thing that must work. Emails needing attention and disputed-invoice follow-ups fall through the cracks. Flagged emails are rarely revisited.
2. **One task list.** Today tasks live on paper and in her head. Tasks come mostly from her manager and director.
3. **Per-collector tracking:** 1:1 notes, escalation requests, and **items from team meetings that each collector must be retrained on**.
4. **Per-customer tracking:** aging, disputes, last payment date, last AR-platform event date and note.
5. **Review evidence,** twice a year (December and June), as a self-assessment against an Individual Performance Objective (goals plan). Already keeps a "My Wins" email folder.

## Hard boundaries (from the user)

Never written into the vault:

- HR matters
- Personal struggles of team members
- Issues between team members

## Data policy

The employer has an AI policy, but it says nothing either way about customer or employee data. **Silence is not permission.** Default `data_policy`:

> Customer names, aging, balances, and dispute status are OK. No bank or full customer account numbers. Nothing HR-related or personal about team members.

## What counts as a win (examples the user gave)

- System implementation and user acceptance testing completed
- High-value accounts (above a monthly billing threshold) with collection issues, where she played a major role in getting the customer back to current (no invoices more than 30 days past due)

## Design decisions

| Need | Pack piece |
|---|---|
| Email triage | `inbox` workflow. Reads via the Microsoft 365 connector when present, otherwise from pasted or exported emails. Sorts into: needs a reply, dispute follow-ups, asks from manager or director, win candidates, FYI. Owner tasks go to the task list with the email as source. HR and personal threads are skipped entirely and never quoted or saved. **Never sends, drafts in Outlook, moves, or flags mail without a yes for that action.** |
| My Wins backfill | `wins-backfill` workflow: reads the wins folder once, proposes accomplishments entries outcome-first with dates, owner approves each. |
| Per-collector tracking | `Team/{Name}/` with `Current State.md`, `1-1s/`, and `Retrain List.md`. Team-meeting intake routes each retrain item to the right person's list. |
| 1:1 cadence | `prep` for a 1:1 pulls open retrain items, escalations, and follow-ups owed for that person. `brief` flags anyone not met in more than 3 weeks. |
| Per-customer tracking | `Accounts/{Customer}/` with frontmatter: `aging_current`, `aging_30`, `aging_60`, `aging_90_plus`, `open_disputes`, `last_payment_date`, `last_ar_event_date`, `last_ar_event_note`, `collector`. Exports converted with `sheet-to-md.py` into `_derived/`. |
| Review cycle | `review-prep` defaults to the June and December cycles and groups evidence by the goals plan. |

## Open questions

- Can the connector read flagged status? The help article does not say. Test before promising a "flagged email sweep."
- Is the AR platform data reachable by export or report? If not, account fields are updated by paste.
- Does she want team-meeting transcripts from SharePoint pulled through the connector, or pasted?
