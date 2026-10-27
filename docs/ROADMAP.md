# Roadmap

## v0.1 (this release)

- Core: rules, workflows (resume, wrap, intake, prep, brief, internal, review-prep), templates
- CSE pack: account structure, customer-success platform rules, risk, cs-update, build-vault
- Adapters: Claude skill, any-LLM starter prompt, and a generic exporter for tools that only read their own rules folder
- Scripts: new-vault, update-vault, export-agent-files, check-vault, sheet-to-md

## Next

1. **Migrate the original CSE vault onto v0.1** (the dogfood test). Anything that breaks becomes a fix here.
2. **`se` pack:** opportunity folders, MEDDPICC as the spine, deal reviews, CRM updates drafted for the owner to paste (no CRM connector assumed).
3. **`people-manager` pack:** shaped by an interview with the first user. Expected pieces:
   - `Team/{Name}/` per direct report: 1:1 notes, goals, coaching, wins, follow-ups owed
   - `Accounts/` for accounts the manager assists on
   - Teams transcripts brought in by paste or via `_Inbox/`
   - strict defaults for HR-sensitive content
4. **`personal-life` pack:** areas, one personal task list, sessions. No content shipped.
5. **Microsoft 365 Copilot:** first pass shipped in v0.2 (publish, capture notes). Next: test on a real account and on the people-manager pack.

## Feedback queue

- Compare `publish_layout: flat` against `mirror` in a real Copilot Notebook.
- Test `email-to-md.py` on a real Mac Outlook `.eml` and a real Windows `.msg` (tested so far on synthetic files and public sample `.msg` files).

## Open design questions

- Should `AGENTS.md` be renamed for tools that look for other entry files (for example `CLAUDE.md`, `.github/copilot-instructions.md`)? Today each adapter points its tool at `AGENTS.md`.
- Test `export-agent-files.py` output against each tool that needs it before calling that tool supported.
