# Roadmap

## v0.1 (this release)

- Core: rules, workflows (resume, wrap, intake, prep, brief, internal, review-prep), templates
- CSE pack: account structure, customer-success platform rules, risk, cs-update, build-vault
- Adapters: Claude skill, any-LLM starter prompt, and a generic exporter for tools that only read their own rules folder
- Scripts: new-vault, update-vault, export-agent-files, check-vault, sheet-to-md

## Next

1. **Migrate the original CSE vault onto v0.1** (the dogfood test). Anything that breaks becomes a fix here.
2. **`se` pack:** opportunity folders, MEDDPICC as the spine, deal reviews, CRM updates drafted for the owner to paste (no CRM connector assumed).
3. **`people-manager` pack:** first phase shipped in v0.4.0, shaped by an interview with the first user (`docs/design/people-manager-requirements.md`). Shipped: `Team/{Name}/` (Current State, 1-1s, Retrain List), the hard boundary on HR and personal matters, retrain routing from team-meeting intake, the extra inbox buckets, and the core `inbox` and `wins-backfill` workflows. Not yet run with a real assistant: see `docs/inbox-acceptance.md`. Next phases:
   - `prep` for a 1:1 pulls open retrain items, escalations, and follow-ups owed for that person; `brief` flags anyone not met within `one_on_one_days` (the key exists, nothing reads it yet)
   - `review-prep` defaults to a twice-yearly cycle and groups evidence by the owner's goals plan
   - `Accounts/` for accounts the manager assists on
   - Transcripts brought in by paste or via `_Inbox/`
   - Open questions from the interview: can the mail connector read flagged status (test before promising a flagged-mail sweep), and do team-meeting transcripts come through the connector or by paste
   - **Collections fields (aging, disputes, AR-platform events):** per-customer tracking for a receivables team. Separate item, deliberately kept out of core and out of this pack until there is a design for it.
4. **`personal-life` pack:** areas, one personal task list, sessions. No content shipped.
5. **Microsoft 365 Copilot:** first pass shipped in v0.2 (publish, capture notes). Next: test on a real account and on the people-manager pack.

## Feedback queue

- Compare `publish_layout: flat` against `mirror` in a real Copilot Notebook.
- Test `email-to-md.py` on a real Windows `.msg`: plan in [msg-test-plan.md](msg-test-plan.md), not yet run (real Mac Outlook `.eml` files tested 2026-10-27: two threads, headers, signature, and quoted history converted correctly).

## Open design questions

- Should `AGENTS.md` be renamed for tools that look for other entry files (for example `CLAUDE.md`, `.github/copilot-instructions.md`)? Today each adapter points its tool at `AGENTS.md`.
- Test `export-agent-files.py` output against each tool that needs it before calling that tool supported.
